import os, json, time, subprocess, sys
import FreeSimpleGUI as sg
from datetime import datetime
from threading import Thread

class PyLauncher:
    def __init__(self):
        self.DATA_FILE = "launcher_cfg.json"
        self.data = self.load_data()
        self.current_cat = "Uncategorized"
        
        # Default keyboard shortcuts
        self.shortcuts = self.data.get("shortcuts", {
            "launch": "l",
            "add_app": "a",
            "remove_app": "Delete",
            "search": "f",
            "new_category": "n",
            "quit": "q"
        })
        
        # Minimal theme
        sg.theme('DarkGrey13')
        sg.set_options(font=("Segoe UI", 9))
        
        self.window = None
        self.create_main_window()

    def load_data(self):
        default = {"Uncategorized": {}, "shortcuts": {}}
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f: 
                    return json.load(f)
            except: 
                pass
        return default

    def save_data(self):
        self.data["shortcuts"] = self.shortcuts
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def create_main_window(self):
        """Create the main application window"""
        
        # Menu definition
        menu_def = [
            ['Help', ['User Guide', 'About']],
            ['Settings', ['Shortcuts', '---', 'Quit']]
        ]
        
        # Get categories and apps for initial display
        categories = sorted(self.data.keys())
        if "shortcuts" in categories:
            categories.remove("shortcuts")
        
        apps_data = self.get_apps_for_category(self.current_cat)
        
        # Compact layout
        layout = [
            [sg.Menu(menu_def, background_color='#161B22', text_color='#F0F6FC')],
            
            # Search bar - compact
            [sg.Text('Search:', size=(7, 1)), 
             sg.Input(key='-SEARCH-', size=(70, 1), enable_events=True)],
            
            # Main content area - compact
            [
                # Categories column - smaller
                sg.Column([
                    [sg.Listbox(categories, size=(20, 18), key='-CATEGORIES-', 
                               enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                               background_color='#161B22',
                               default_values=[self.current_cat])],
                    [sg.Button('+', size=(3, 1), key='-ADD_CAT-'),
                     sg.Button('-', size=(3, 1), key='-REM_CAT-')]
                ], vertical_alignment='top', pad=(5, 5)),
                
                # Apps table - compact
                sg.Column([
                    [sg.Table(values=apps_data,
                             headings=['Fav', 'Application', 'Runs', 'Last Used'],
                             key='-APPS-',
                             auto_size_columns=False,
                             col_widths=[4, 35, 6, 18],
                             num_rows=18,
                             justification='left',
                             enable_events=True,
                             select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                             background_color='#161B22')]
                ], expand_x=True, expand_y=True, pad=(5, 5))
            ],
            
            # Bottom controls - compact
            [
                sg.Button('Add', key='-ADD_APP-', size=(6, 1)),
                sg.Button('Remove', key='-REM_APP-', size=(7, 1)),
                sg.Button('Favorite', key='-FAV-', size=(8, 1)),
                sg.Text('Delay:', size=(5, 1)),
                sg.Input('0', key='-DELAY-', size=(4, 1)),
                sg.Push(),
                sg.Button('LAUNCH', key='-LAUNCH-', size=(8, 1), button_color=('#FFFFFF', '#3FB950'))
            ],
            
            # Status bar - compact
            [sg.Text('Ready', key='-STATUS-', size=(80, 1), relief=sg.RELIEF_FLAT, 
                    background_color='#161B22', text_color='#3FB950')]
        ]
        
        self.window = sg.Window('PyLauncher V2.2', layout, size=(800, 500), 
                               finalize=True, resizable=True, 
                               background_color='#0D1117',
                               return_keyboard_events=True)
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()

    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        if self.window:
            self.window.bind(f'<Control-{self.shortcuts.get("launch", "l")}>', '-LAUNCH-')
            self.window.bind(f'<Control-{self.shortcuts.get("add_app", "a")}>', '-ADD_APP-')
            self.window.bind(f'<{self.shortcuts.get("remove_app", "Delete")}>', '-REM_APP-')
            self.window.bind(f'<Control-{self.shortcuts.get("search", "f")}>', '-FOCUS_SEARCH-')
            self.window.bind(f'<Control-{self.shortcuts.get("new_category", "n")}>', '-ADD_CAT-')
            self.window.bind(f'<Control-{self.shortcuts.get("quit", "q")}>', '-QUIT-')

    def get_apps_for_category(self, category):
        """Get apps data for table display"""
        apps = self.data.get(category, {})
        if category == "shortcuts":
            return []
        
        # Sort by favorite then name
        sorted_apps = sorted(apps.items(), key=lambda x: (not x[1].get('fav', False), os.path.basename(x[0]).lower()))
        
        result = []
        for path, info in sorted_apps:
            name = os.path.basename(path)
            fav = '*' if info.get('fav') else ''
            launches = info.get('launches', 0)
            last = info.get('last', 'Never')
            if last != 'Never':
                last = last[5:16].replace('T', ' ')
            result.append([fav, name, launches, last])
        
        return result

    def get_selected_app_paths(self):
        """Get full paths of selected apps"""
        try:
            selected_rows = self.window['-APPS-'].SelectedRows
            if not selected_rows:
                return []
            
            apps = self.data.get(self.current_cat, {})
            sorted_apps = sorted(apps.items(), key=lambda x: (not x[1].get('fav', False), os.path.basename(x[0]).lower()))
            
            paths = []
            for idx in selected_rows:
                if idx < len(sorted_apps):
                    paths.append(sorted_apps[idx][0])
            return paths
        except:
            return []

    def refresh_apps(self, search_term=""):
        """Refresh the apps table"""
        apps = self.data.get(self.current_cat, {})
        sorted_apps = sorted(apps.items(), key=lambda x: (not x[1].get('fav', False), os.path.basename(x[0]).lower()))
        
        result = []
        for path, info in sorted_apps:
            name = os.path.basename(path)
            if search_term and search_term.lower() not in name.lower():
                continue
            
            fav = '*' if info.get('fav') else ''
            launches = info.get('launches', 0)
            last = info.get('last', 'Never')
            if last != 'Never':
                last = last[5:16].replace('T', ' ')
            result.append([fav, name, launches, last])
        
        self.window['-APPS-'].update(values=result)

    def refresh_categories(self):
        """Refresh the categories list"""
        categories = sorted(self.data.keys())
        if "shortcuts" in categories:
            categories.remove("shortcuts")
        self.window['-CATEGORIES-'].update(values=categories, set_to_index=[categories.index(self.current_cat)] if self.current_cat in categories else [0])

    def add_category(self):
        """Add a new category"""
        name = sg.popup_get_text('Category name:', title='New Category')
        if name and name not in self.data:
            self.data[name] = {}
            self.save_data()
            self.refresh_categories()

    def remove_category(self):
        """Remove selected category"""
        if self.current_cat == "Uncategorized":
            sg.popup_error("Cannot delete 'Uncategorized'")
            return
        
        if sg.popup_yes_no(f"Delete '{self.current_cat}'?", title='Confirm') == 'Yes':
            del self.data[self.current_cat]
            self.current_cat = "Uncategorized"
            self.save_data()
            self.refresh_categories()
            self.refresh_apps()

    def add_app(self):
        """Add a new application"""
        path = sg.popup_get_file('Select application', title='Add Application', 
                                file_types=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if path:
            self.data[self.current_cat][path] = {"launches": 0, "last": "Never", "fav": False}
            self.save_data()
            self.refresh_apps()

    def remove_app(self):
        """Remove selected applications"""
        paths = self.get_selected_app_paths()
        for path in paths:
            if path in self.data[self.current_cat]:
                del self.data[self.current_cat][path]
        self.save_data()
        self.refresh_apps()

    def toggle_favorite(self):
        """Toggle favorite status for selected apps"""
        paths = self.get_selected_app_paths()
        for path in paths:
            if path in self.data[self.current_cat]:
                self.data[self.current_cat][path]['fav'] = not self.data[self.current_cat][path].get('fav', False)
        self.save_data()
        self.refresh_apps()

    def launch_apps(self):
        """Launch selected applications"""
        paths = self.get_selected_app_paths()
        if not paths:
            return
        
        try:
            delay = float(self.window['-DELAY-'].get() or 0)
        except:
            delay = 0
        
        def run():
            for p in paths:
                if delay > 0:
                    self.window['-STATUS-'].update(f'Waiting {delay}s...', text_color='#F0F6FC')
                    time.sleep(delay)
                try:
                    if sys.platform == "win32":
                        os.startfile(p)
                    else:
                        subprocess.Popen([p])
                    
                    self.data[self.current_cat][p]['launches'] += 1
                    self.data[self.current_cat][p]['last'] = datetime.now().isoformat()
                    self.window['-STATUS-'].update(f'Launched: {os.path.basename(p)}', text_color='#3FB950')
                except Exception as e:
                    self.window['-STATUS-'].update(f'Error: {str(e)}', text_color='#F85149')
                    sg.popup_error(f'Error: {str(e)}')
            
            self.save_data()
            self.refresh_apps()
        
        Thread(target=run, daemon=True).start()

    def show_help(self):
        """Show help dialog"""
        help_text = """PyLauncher V2.2 - User Guide

CATEGORIES
• Organize applications into categories
• Click a category to view its apps
• Use + to create, - to delete

APPLICATIONS
• Double-click or select and press Ctrl+L to launch
• Ctrl+Click for multiple selection
• Favorites (marked with *) appear at top

SEARCH
• Filter apps by name in real-time
• Clear search to see all apps

KEYBOARD SHORTCUTS
Ctrl+L     Launch selected apps
Ctrl+A     Add new app
Ctrl+F     Focus search
Ctrl+N     New category
Delete     Remove selected apps
Ctrl+Q     Quit

TIPS
• Use categories to organize by workflow
• Mark frequently used apps as favorites
• Set delays for sequential app launches"""
        
        sg.popup_scrolled(help_text, title='User Guide', size=(60, 25))

    def show_about(self):
        """Show about dialog"""
        sg.popup('PyLauncher V2.2\n\n' +
                'A fast, minimal application launcher\n\n' +
                'Features:\n' +
                '• Category organization\n' +
                '• Usage statistics\n' +
                '• Keyboard shortcuts\n' +
                '• Batch launching\n' +
                '• Favorites\n\n' +
                '2026',
                title='About')

    def open_settings(self):
        """Open settings dialog"""
        shortcut_labels = {
            "launch": "Launch",
            "add_app": "Add App",
            "remove_app": "Remove",
            "search": "Search",
            "new_category": "New Category",
            "quit": "Quit"
        }
        
        layout = [
            [sg.Text('Keyboard Shortcuts', font=("Segoe UI", 11, "bold"))],
            [sg.Text('Enter key for Ctrl+ shortcuts (e.g., "l" for Ctrl+L)')],
            [sg.HorizontalSeparator()],
        ]
        
        for key, label in shortcut_labels.items():
            layout.append([
                sg.Text(label + ':', size=(15, 1)),
                sg.Input(self.shortcuts.get(key, ''), key=f'-SC_{key}-', size=(15, 1))
            ])
        
        layout.extend([
            [sg.HorizontalSeparator()],
            [sg.Button('Save', key='-SAVE_SC-'), 
             sg.Button('Reset', key='-RESET_SC-'),
             sg.Button('Cancel', key='-CANCEL_SC-')]
        ])
        
        settings_window = sg.Window('Shortcuts', layout, modal=True)
        
        while True:
            event, values = settings_window.read()
            
            if event in (sg.WIN_CLOSED, '-CANCEL_SC-'):
                break
            
            if event == '-RESET_SC-':
                defaults = {
                    "launch": "l",
                    "add_app": "a",
                    "remove_app": "Delete",
                    "search": "f",
                    "new_category": "n",
                    "quit": "q"
                }
                for key in shortcut_labels.keys():
                    settings_window[f'-SC_{key}-'].update(defaults[key])
            
            if event == '-SAVE_SC-':
                for key in shortcut_labels.keys():
                    self.shortcuts[key] = values[f'-SC_{key}-']
                self.save_data()
                self.bind_shortcuts()
                sg.popup('Saved!', title='Success')
                break
        
        settings_window.close()

    def run(self):
        """Main event loop"""
        while True:
            event, values = self.window.read(timeout=100)
            
            if event in (sg.WIN_CLOSED, '-QUIT-', 'Quit'):
                break
            
            if event == '-CATEGORIES-' and values['-CATEGORIES-']:
                self.current_cat = values['-CATEGORIES-'][0]
                self.refresh_apps()
            
            if event == '-SEARCH-':
                self.refresh_apps(values['-SEARCH-'])
            
            if event == '-FOCUS_SEARCH-':
                self.window['-SEARCH-'].set_focus()
            
            if event == '-ADD_CAT-':
                self.add_category()
            
            if event == '-REM_CAT-':
                self.remove_category()
            
            if event == '-ADD_APP-':
                self.add_app()
            
            if event == '-REM_APP-':
                self.remove_app()
            
            if event == '-FAV-':
                self.toggle_favorite()
            
            if event == '-LAUNCH-':
                self.launch_apps()
            
            if event == 'User Guide':
                self.show_help()
            
            if event == 'About':
                self.show_about()
            
            if event == 'Shortcuts':
                self.open_settings()
        
        self.window.close()

if __name__ == "__main__":
    launcher = PyLauncher()
    launcher.run()
