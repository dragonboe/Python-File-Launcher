import os
import json
import time
import tkinter as tk
import subprocess
from threading import Thread
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image
from datetime import datetime
import pystray
from keyboard import add_hotkey, remove_hotkey
from collections import defaultdict

class AppLauncher:
    def __init__(self):
        self.APP_LIST_FILE = "app_paths.json"
        self.STATS_FILE = "app_stats.json"
        self.FAVORITES_FILE = "favorites.json"
        self.app_paths = self.load_app_paths()
        self.app_stats = self.load_stats()
        self.favorites = self.load_favorites()
        self.root = ctk.CTk()
        self.root.title("App Launcher Pro")
        self.root.geometry("800x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        self.setup_gui()
        self.setup_system_tray()
        self.setup_hotkeys()

    def load_stats(self):
        if not os.path.exists(self.STATS_FILE):
            return defaultdict(lambda: {'launches': 0, 'last_used': None})
        with open(self.STATS_FILE, 'r') as f:
            return defaultdict(lambda: {'launches': 0, 'last_used': None}, json.load(f))

    def save_stats(self):
        with open(self.STATS_FILE, 'w') as f:
            json.dump(self.app_stats, f, indent=4, default=str)

    def load_favorites(self):
        if not os.path.exists(self.FAVORITES_FILE): return []
        with open(self.FAVORITES_FILE, 'r') as f:
            return json.load(f)

    def save_favorites(self):
        with open(self.FAVORITES_FILE, 'w') as f:
            json.dump(self.favorites, f, indent=4)

    def load_app_paths(self):
        if not os.path.exists(self.APP_LIST_FILE):
            return {"Uncategorized": []}
        try:
            with open(self.APP_LIST_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {"Uncategorized": []}

    def save_app_paths(self):
        with open(self.APP_LIST_FILE, 'w') as file:
            json.dump(self.app_paths, file, indent=4)

    def setup_gui(self):
        self.main_container = ctk.CTkFrame(self.root, fg_color="#000000")
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)

        self.category_frame = ctk.CTkFrame(self.main_container, width=200, fg_color="#0a0a0a")
        self.category_frame.pack(side='left', fill='y', padx=(0, 10))

        category_header = ctk.CTkFrame(self.category_frame, fg_color="transparent")
        category_header.pack(fill='x', pady=5)
        
        ctk.CTkLabel(category_header, text="Categories", font=("Segoe UI", 12, "bold")).pack(side='left', padx=5)
        
        category_buttons = ctk.CTkFrame(category_header, fg_color="transparent")
        category_buttons.pack(side='right', padx=5)
        
        ctk.CTkButton(category_buttons, text="+", width=25, command=self.add_category).pack(side='left', padx=2)
        ctk.CTkButton(category_buttons, text="-", width=25, command=self.remove_category).pack(side='left', padx=2)

        self.category_listbox = tk.Listbox(
            self.category_frame,
            bg='#000000',
            fg='#ffffff',
            selectmode='single',
            font=("Segoe UI", 10),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor='#1a1a1a',
            selectbackground='#0d47a1',
            activestyle='none'
        )
        self.category_listbox.pack(fill='both', expand=True, pady=5)
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)

        self.app_frame = ctk.CTkFrame(self.main_container, fg_color="#0a0a0a")
        self.app_frame.pack(side='left', fill='both', expand=True)

        search_frame = ctk.CTkFrame(self.app_frame, fg_color="transparent")
        search_frame.pack(fill='x', pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search...",
            textvariable=self.search_var,
            height=30
        )
        self.search_entry.pack(fill='x', padx=5)

        app_header = ctk.CTkFrame(self.app_frame, fg_color="transparent")
        app_header.pack(fill='x', pady=5)
        
        ctk.CTkLabel(app_header, text="Applications", font=("Segoe UI", 12, "bold")).pack(side='left', padx=5)

        self.app_listbox = tk.Listbox(
            self.app_frame,
            bg='#000000',
            fg='#ffffff',
            selectmode='extended',
            font=("Segoe UI", 10),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor='#1a1a1a',
            selectbackground='#0d47a1',
            activestyle='none'
        )
        self.app_listbox.pack(fill='both', expand=True, pady=5)
        self.app_listbox.bind('<Control-a>', self.select_all)

        control_frame = ctk.CTkFrame(self.app_frame, fg_color="transparent")
        control_frame.pack(fill='x', pady=5)

        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(side='left')

        ctk.CTkButton(button_frame, text="Add", width=60, command=self.add_app_path).pack(side='left', padx=2)
        ctk.CTkButton(button_frame, text="Remove", width=60, command=self.remove_app_path).pack(side='left', padx=2)

        launch_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        launch_frame.pack(side='right')

        self.delay_entry = ctk.CTkEntry(launch_frame, width=50, height=30, placeholder_text="Delay")
        self.delay_entry.pack(side='left', padx=2)
        self.delay_entry.insert(0, "5")

        ctk.CTkButton(launch_frame, text="Launch", width=70, command=self.launch_apps_with_delay).pack(side='left', padx=2)

        self.status_label = ctk.CTkLabel(self.root, text="Ready", anchor="w", font=("Segoe UI", 10))
        self.status_label.pack(fill='x', padx=10, pady=5)

        self.update_category_list()
        if self.category_listbox.size() > 0:
            self.category_listbox.select_set(0)
            self.on_category_select(None)

    def add_category(self):
        dialog = ctk.CTkInputDialog(text="Enter category name:", title="New Category")
        category = dialog.get_input()
        if category and category not in self.app_paths:
            self.app_paths[category] = []
            self.save_app_paths()
            self.update_category_list()

    def remove_category(self):
        selection = self.category_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a category to remove.")
            return
        category = self.category_listbox.get(selection[0])
        if category == "Uncategorized":
            messagebox.showwarning("Cannot Remove", "The Uncategorized category cannot be removed.")
            return
        if messagebox.askyesno("Confirm Removal", f"Remove category '{category}' and all its applications?"):
            del self.app_paths[category]
            self.save_app_paths()
            self.update_category_list()
            self.category_listbox.select_set(0)
            self.on_category_select(None)

    def update_category_list(self):
        self.category_listbox.delete(0, tk.END)
        for category in self.app_paths.keys():
            self.category_listbox.insert(tk.END, category)

    def on_category_select(self, event):
        selection = self.category_listbox.curselection()
        if selection:
            category = self.category_listbox.get(selection[0])
            self.update_app_list(category)

    def update_app_list(self, category):
        self.app_listbox.delete(0, tk.END)
        for path in self.app_paths[category]:
            app_name = os.path.basename(path)
            display_name = f"★ {app_name}" if path in self.favorites else app_name
            self.app_listbox.insert(tk.END, display_name)

    def get_app_path_from_display_name(self, display_name, category):
        app_name = display_name.replace('★ ', '')
        for path in self.app_paths[category]:
            if os.path.basename(path) == app_name:
                return path
        return None

    def toggle_favorite(self, event=None):
        selection = self.app_listbox.curselection()
        if not selection: return
        category = self.get_current_category()
        display_name = self.app_listbox.get(selection[0])
        app_path = self.get_app_path_from_display_name(display_name, category)
        if app_path:
            if app_path in self.favorites:
                self.favorites.remove(app_path)
            else:
                self.favorites.append(app_path)
            self.save_favorites()
            self.update_app_list(category)

    def get_current_category(self):
        selection = self.category_listbox.curselection()
        return self.category_listbox.get(selection[0]) if selection else "Uncategorized"

    def add_app_path(self):
        path = filedialog.askopenfilename(
            title="Select Application",
            filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*"))
        )
        if path:
            category = self.get_current_category()
            if path not in self.app_paths[category]:
                self.app_paths[category].append(path)
                self.save_app_paths()
                self.update_app_list(category)
                messagebox.showinfo("Success", f"Application added to {category}")
            else:
                messagebox.showwarning("Duplicate", "This application is already in the list.")

    def remove_app_path(self):
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select an application to remove.")
            return
        category = self.get_current_category()
        for index in reversed(selected_indices):
            self.app_paths[category].pop(index)
        self.save_app_paths()
        self.update_app_list(category)

    def launch_apps_with_delay(self):
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one application to launch.")
            return
        try:
            delay_seconds = float(self.delay_entry.get())
            if delay_seconds < 0: raise ValueError("Delay must be positive")
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Please enter a valid positive number for delay.")
            return
        category = self.get_current_category()
        Thread(target=self.launch_thread, args=(selected_indices, category, delay_seconds)).start()

    def launch_thread(self, selected_indices, category, delay_seconds):
        for index in selected_indices:
            app_path = self.app_paths[category][index]
            self.status_label.configure(text=f"Launching in {delay_seconds}s: {os.path.basename(app_path)}")
            time.sleep(delay_seconds)
            try:
                subprocess.Popen(app_path)
                self.status_label.configure(text=f"Launched: {os.path.basename(app_path)}")
                self.update_app_stats(app_path)
            except Exception as e:
                self.status_label.configure(text=f"Failed to launch: {os.path.basename(app_path)}")
                messagebox.showerror("Error", f"Failed to launch {app_path}: {e}")
        self.status_label.configure(text="All applications launched.")

    def update_app_stats(self, app_path):
        self.app_stats[app_path]['launches'] += 1
        self.app_stats[app_path]['last_used'] = datetime.now()
        self.save_stats()

    def show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def quit_app(self):
        remove_hotkey('ctrl+shift+space')
        remove_hotkey('ctrl+shift+q')
        remove_hotkey('ctrl+f')
        self.root.destroy()

    def setup_system_tray(self):
        try:
            icon_image = Image.new('RGB', (64, 64), '#0d47a1')
            self.icon = pystray.Icon(
                'app_launcher',
                icon_image,
                menu=pystray.Menu(
                    pystray.MenuItem('Show', self.show_window),
                    pystray.MenuItem('Quit', self.quit_app)
                )
            )
            self.icon.run_detached()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to setup system tray: {e}')
            self.quit_app()
    def setup_hotkeys(self):
        add_hotkey('ctrl+shift+space', self.show_window)
        add_hotkey('ctrl+shift+q', self.quit_app)
        add_hotkey('ctrl+f', lambda: self.search_entry.focus_force())

    def on_search(self, *args):
        search_term = self.search_var.get().lower()
        category = self.get_current_category()
        self.app_listbox.delete(0, tk.END)
        for path in self.app_paths[category]:
            app_name = os.path.basename(path)
            if search_term in app_name.lower():
                display_name = f"★ {app_name}" if path in self.favorites else app_name
                self.app_listbox.insert(tk.END, display_name)
    def select_all(self, event):
        self.app_listbox.select_set(0, tk.END)
        return "break"

if __name__ == "__main__":
    app = AppLauncher()
    app.root.mainloop()
