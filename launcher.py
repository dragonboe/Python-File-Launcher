import os
import json
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread
from datetime import datetime
from collections import defaultdict
import subprocess
import sys

class AppLauncher:
    def __init__(self):
        self.APP_LIST_FILE = "app_paths.json"
        self.STATS_FILE = "app_stats.json"
        self.FAVORITES_FILE = "favorites.json"
        
        # Initialize data
        self.app_paths = self.load_app_paths()
        self.app_stats = self.load_stats()
        self.favorites = set(self.load_favorites())
        self.filtered_apps = []
        self.current_category = "Uncategorized"
        
        # Ensure Uncategorized exists
        if "Uncategorized" not in self.app_paths:
            self.app_paths["Uncategorized"] = []
        
        # Setup GUI
        self.root = tk.Tk()
        self.root.title("PyLauncher v2.1")
        self.root.geometry("900x500")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, True)
        
        # Set window icon
        try:
            self.root.iconbitmap(default="")
        except:
            pass
        
        self.setup_styles()
        self.setup_gui()
        self.setup_hotkeys()
        
        # Initialize display
        self.status_label.configure(text="PyLauncher v2.1")
        self.update_category_tree()
        
        # Select first category if available
        if self.category_tree.get_children():
            first_cat = self.category_tree.get_children()[0]
            self.category_tree.selection_set(first_cat)
            self.on_category_select(None)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        """Setup modern dark theme styles"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure colors
        bg_dark = "#1e1e1e"
        bg_medium = "#2d2d2d"
        bg_light = "#3a3a3a"
        fg_primary = "#ffffff"
        fg_secondary = "#b0b0b0"
        accent = "#0078d4"
        
        # General styles
        style.configure(".", background=bg_dark, foreground=fg_primary, font=("Segoe UI", 9))
        style.configure("TFrame", background=bg_dark)
        style.configure("TLabel", background=bg_dark, foreground=fg_primary)
        style.configure("Title.TLabel", background=bg_dark, foreground=fg_primary, font=("Segoe UI", 11, "bold"))
        
        # Button styles
        style.configure("TButton", 
                       background=bg_medium, 
                       foreground=fg_primary, 
                       padding=(8, 4),
                       borderwidth=1,
                       focuscolor="none")
        style.map("TButton", 
                 background=[("active", bg_light), ("pressed", accent)],
                 foreground=[("active", fg_primary)])
        
        # Entry styles
        style.configure("TEntry", 
                       fieldbackground=bg_medium, 
                       foreground=fg_primary, 
                       insertcolor=fg_primary,
                       borderwidth=1)
        style.map("TEntry", focuscolor=[("!focus", "none")])
        
        # Treeview styles
        style.configure("Treeview", 
                       background=bg_medium, 
                       foreground=fg_primary, 
                       fieldbackground=bg_medium,
                       rowheight=24,
                       borderwidth=1)
        style.map("Treeview", 
                 background=[("selected", accent)],
                 foreground=[("selected", fg_primary)])
        
        # Treeview headings
        style.configure("Treeview.Heading", 
                       background=bg_light, 
                       foreground=fg_primary,
                       borderwidth=1)

    def setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        self.root.bind("<Control-n>", lambda e: self.add_app_path())
        self.root.bind("<Delete>", lambda e: self.remove_app_path())
        self.root.bind("<F5>", lambda e: self.refresh_display())
        self.root.bind("<Control-f>", lambda e: self.search_entry.focus())
        self.root.bind("<Return>", lambda e: self.launch_selected_apps())
        self.root.bind("<Control-q>", lambda e: self.on_closing())

    def load_stats(self):
        """Load application usage statistics"""
        if not os.path.exists(self.STATS_FILE):
            return defaultdict(lambda: {'launches': 0, 'last_used': None})
        try:
            with open(self.STATS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return defaultdict(lambda: {'launches': 0, 'last_used': None}, data)
        except Exception as e:
            print(f"Error loading stats: {e}")
            return defaultdict(lambda: {'launches': 0, 'last_used': None})

    def save_stats(self):
        """Save application usage statistics"""
        try:
            with open(self.STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(dict(self.app_stats), f, indent=2, default=str, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save stats: {e}")

    def load_favorites(self):
        """Load favorite applications"""
        if not os.path.exists(self.FAVORITES_FILE):
            return []
        try:
            with open(self.FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading favorites: {e}")
            return []

    def save_favorites(self):
        """Save favorite applications"""
        try:
            with open(self.FAVORITES_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(self.favorites), f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save favorites: {e}")

    def load_app_paths(self):
        """Load application paths from file"""
        if not os.path.exists(self.APP_LIST_FILE):
            return {"Uncategorized": []}
        try:
            with open(self.APP_LIST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure all paths exist
                cleaned_data = {}
                for category, paths in data.items():
                    cleaned_paths = [p for p in paths if os.path.exists(p)]
                    if cleaned_paths or category == "Uncategorized":
                        cleaned_data[category] = cleaned_paths
                return cleaned_data
        except Exception as e:
            print(f"Error loading app paths: {e}")
            return {"Uncategorized": []}

    def save_app_paths(self):
        """Save application paths to file"""
        try:
            with open(self.APP_LIST_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.app_paths, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save app paths: {e}")
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Categories
        left_panel = ttk.Frame(main_container, width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Category header
        cat_header = ttk.Frame(left_panel)
        cat_header.pack(fill="x", pady=(0, 5))
        ttk.Label(cat_header, text="📁 Categories", style="Title.TLabel").pack(side="left")
        
        # Category buttons
        cat_buttons = ttk.Frame(cat_header)
        cat_buttons.pack(side="right")
        ttk.Button(cat_buttons, text="➕", width=3, command=self.add_category).pack(side="left", padx=1)
        ttk.Button(cat_buttons, text="➖", width=3, command=self.remove_category).pack(side="left")
        
        # Category tree
        cat_frame = ttk.Frame(left_panel)
        cat_frame.pack(fill="both", expand=True)
        
        self.category_tree = ttk.Treeview(cat_frame, show="tree", selectmode="browse")
        cat_scrollbar = ttk.Scrollbar(cat_frame, orient="vertical", command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=cat_scrollbar.set)
        
        self.category_tree.pack(side="left", fill="both", expand=True)
        cat_scrollbar.pack(side="right", fill="y")
        
        self.category_tree.bind("<<TreeviewSelect>>", self.on_category_select)
        
        # Right panel - Applications
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side="left", fill="both", expand=True)
        
        # Search frame
        search_frame = ttk.Frame(right_panel)
        search_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(search_frame, text="🔍").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10))
        self.search_entry.pack(fill="x", expand=True)
        
        # App header
        app_header = ttk.Frame(right_panel)
        app_header.pack(fill="x", pady=(5, 5))
        ttk.Label(app_header, text="📱 Applications", style="Title.TLabel").pack(side="left")
        
        # Stats display
        self.stats_label = ttk.Label(app_header, text="", foreground="#b0b0b0")
        self.stats_label.pack(side="right")
        
        # Application tree with columns
        app_frame = ttk.Frame(right_panel)
        app_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        columns = ("name", "launches", "last_used")
        self.app_tree = ttk.Treeview(app_frame, columns=columns, show="tree headings", selectmode="extended")
        
        # Configure columns
        self.app_tree.heading("#0", text="Application", anchor="w")
        self.app_tree.heading("name", text="Name", anchor="w")
        self.app_tree.heading("launches", text="Launches", anchor="center")
        self.app_tree.heading("last_used", text="Last Used", anchor="center")
        
        self.app_tree.column("#0", width=250, minwidth=200)
        self.app_tree.column("name", width=200, minwidth=150)
        self.app_tree.column("launches", width=80, minwidth=60)
        self.app_tree.column("last_used", width=120, minwidth=100)
        
        # Scrollbars for app tree
        app_v_scrollbar = ttk.Scrollbar(app_frame, orient="vertical", command=self.app_tree.yview)
        app_h_scrollbar = ttk.Scrollbar(app_frame, orient="horizontal", command=self.app_tree.xview)
        self.app_tree.configure(yscrollcommand=app_v_scrollbar.set, xscrollcommand=app_h_scrollbar.set)
        
        self.app_tree.pack(side="left", fill="both", expand=True)
        app_v_scrollbar.pack(side="right", fill="y")
        app_h_scrollbar.pack(side="bottom", fill="x")
        
        # Double-click to launch
        self.app_tree.bind("<Double-1>", lambda e: self.launch_selected_apps())
        self.app_tree.bind("<Return>", lambda e: self.launch_selected_apps())
        
        # Control frame
        control_frame = ttk.Frame(right_panel)
        control_frame.pack(fill="x")
        
        # Left controls
        left_controls = ttk.Frame(control_frame)
        left_controls.pack(side="left")
        
        ttk.Button(left_controls, text="➕ Add App", command=self.add_app_path).pack(side="left", padx=(0, 5))
        ttk.Button(left_controls, text="➖ Remove", command=self.remove_app_path).pack(side="left", padx=(0, 5))
        ttk.Button(left_controls, text="⭐ Favorite", command=self.toggle_favorite).pack(side="left", padx=(0, 5))
        ttk.Button(left_controls, text="📁 Open Folder", command=self.open_app_folder).pack(side="left", padx=(0, 5))
        
        # Right controls
        right_controls = ttk.Frame(control_frame)
        right_controls.pack(side="right")
        
        ttk.Label(right_controls, text="Delay (s):").pack(side="left", padx=(0, 5))
        self.delay_var = tk.StringVar(value="0")
        delay_entry = ttk.Entry(right_controls, textvariable=self.delay_var, width=8)
        delay_entry.pack(side="left", padx=(0, 5))
        
        ttk.Button(right_controls, text="▶ Launch", command=self.launch_apps_with_delay).pack(side="left", padx=(0, 5))
        ttk.Button(right_controls, text="🔄 Refresh", command=self.refresh_display).pack(side="left")
        
        # Status bar
        self.status_label = ttk.Label(self.root, text="Ready", anchor="w", relief="sunken", padding=(5, 2))
        self.status_label.pack(fill="x", side="bottom")

    def add_category(self):
        """Add a new category"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Category")
        dialog.geometry("300x120")
        dialog.configure(bg="#1e1e1e")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 300) // 2
        y = (dialog.winfo_screenheight() - 120) // 2
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(dialog, text="Category name:").pack(pady=10)
        
        entry_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=entry_var, width=30)
        entry.pack(pady=5)
        entry.focus()
        
        def on_ok():
            category = entry_var.get().strip()
            if category and category not in self.app_paths:
                self.app_paths[category] = []
                self.save_app_paths()
                self.update_category_tree()
                # Select the new category
                for item in self.category_tree.get_children():
                    if self.category_tree.item(item, "text") == category:
                        self.category_tree.selection_set(item)
                        self.on_category_select(None)
                        break
                dialog.destroy()
            elif category in self.app_paths:
                messagebox.showwarning("Duplicate", "Category already exists!")
        
        def on_cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side="left", padx=5)
        
        entry.bind("<Return>", lambda e: on_ok())
        dialog.bind("<Escape>", lambda e: on_cancel())

    def remove_category(self):
        """Remove selected category"""
        selection = self.category_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a category to remove.")
            return
        
        category = self.category_tree.item(selection[0], "text")
        if category == "Uncategorized":
            messagebox.showwarning("Cannot Remove", "The 'Uncategorized' category cannot be removed.")
            return
        
        app_count = len(self.app_paths[category])
        if messagebox.askyesno("Confirm Removal", 
                              f"Remove category '{category}' and its {app_count} applications?"):
            # Remove from favorites
            for app_path in self.app_paths[category]:
                self.favorites.discard(app_path)
            
            del self.app_paths[category]
            self.save_app_paths()
            self.save_favorites()
            self.update_category_tree()
            
            # Select Uncategorized
            for item in self.category_tree.get_children():
                if self.category_tree.item(item, "text") == "Uncategorized":
                    self.category_tree.selection_set(item)
                    self.on_category_select(None)
                    break

    def update_category_tree(self):
        """Update the category tree display"""
        # Clear existing items
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        # Add categories (Uncategorized first, then alphabetical)
        categories = sorted(self.app_paths.keys())
        if "Uncategorized" in categories:
            categories.remove("Uncategorized")
            categories.insert(0, "Uncategorized")
        
        for category in categories:
            app_count = len(self.app_paths[category])
            display_text = f"{category} ({app_count})"
            self.category_tree.insert("", "end", iid=category, text=display_text)

    def on_category_select(self, event):
        """Handle category selection"""
        selection = self.category_tree.selection()
        if selection:
            category = selection[0]
            self.current_category = category
            self.update_app_tree(self.app_paths[category])
            self.search_var.set("")  # Clear search when changing category
    def update_app_tree(self, paths):
        """Update the application tree display"""
        # Clear existing items
        self.app_tree.delete(*self.app_tree.get_children())
        self.filtered_apps = paths[:]
        
        # Sort paths by favorites first, then by name
        sorted_paths = sorted(paths, key=lambda p: (p not in self.favorites, os.path.basename(p).lower()))
        
        for path in sorted_paths:
            if not os.path.exists(path):
                continue
                
            name = os.path.basename(path)
            display_name = f"⭐ {name}" if path in self.favorites else name
            
            # Get stats
            stats = self.app_stats[path]
            launches = stats['launches']
            last_used = stats['last_used']
            
            # Format last used
            if last_used:
                try:
                    dt = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
                    last_used_str = dt.strftime("%m/%d %H:%M")
                except:
                    last_used_str = "Unknown"
            else:
                last_used_str = "Never"
            
            # Insert into tree
            self.app_tree.insert("", "end", iid=path, text=display_name,
                               values=(name, launches, last_used_str))
        
        # Update stats display
        total_apps = len(paths)
        favorite_count = len([p for p in paths if p in self.favorites])
        self.stats_label.configure(text=f"Apps: {total_apps} | Favorites: {favorite_count}")

    def on_search(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.update_app_tree(self.app_paths.get(self.current_category, []))
            return
        
        # Filter apps based on search term
        all_paths = self.app_paths.get(self.current_category, [])
        filtered_paths = []
        
        for path in all_paths:
            name = os.path.basename(path).lower()
            if search_term in name:
                filtered_paths.append(path)
        
        self.update_app_tree(filtered_paths)

    def toggle_favorite(self):
        """Toggle favorite status for selected apps"""
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select applications to favorite/unfavorite.")
            return
        
        changed = False
        for app_path in selected:
            if app_path in self.favorites:
                self.favorites.remove(app_path)
            else:
                self.favorites.add(app_path)
            changed = True
        
        if changed:
            self.save_favorites()
            # Refresh display
            if self.search_var.get():
                self.on_search()
            else:
                self.update_app_tree(self.app_paths[self.current_category])

    def add_app_path(self):
        """Add new application path"""
        file_path = filedialog.askopenfilename(
            title="Select Application",
            filetypes=[
                ("Executable files", "*.exe"),
                ("Batch files", "*.bat"),
                ("Command files", "*.cmd"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # Check if already exists in current category
            if file_path in self.app_paths[self.current_category]:
                messagebox.showinfo("Already Exists", "This application is already in the current category.")
                return
            
            # Add to current category
            self.app_paths[self.current_category].append(file_path)
            self.save_app_paths()
            
            # Refresh displays
            self.update_category_tree()
            self.update_app_tree(self.app_paths[self.current_category])
            
            # Select the new app
            self.app_tree.selection_set(file_path)
            self.app_tree.see(file_path)

    def remove_app_path(self):
        """Remove selected application paths"""
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select applications to remove.")
            return
        
        if messagebox.askyesno("Confirm Removal", f"Remove {len(selected)} selected application(s)?"):
            for app_path in selected:
                # Remove from category
                if app_path in self.app_paths[self.current_category]:
                    self.app_paths[self.current_category].remove(app_path)
                
                # Remove from favorites
                self.favorites.discard(app_path)
            
            self.save_app_paths()
            self.save_favorites()
            
            # Refresh displays
            self.update_category_tree()
            self.update_app_tree(self.app_paths[self.current_category])

    def open_app_folder(self):
        """Open folder containing selected application"""
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select an application.")
            return
        
        app_path = selected[0]
        if os.path.exists(app_path):
            folder_path = os.path.dirname(app_path)
            try:
                os.startfile(folder_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {e}")
        else:
            messagebox.showwarning("Not Found", "Application file not found.")

    def launch_selected_apps(self):
        """Launch selected applications immediately"""
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select applications to launch.")
            return
        
        self.launch_apps(selected, 0)

    def launch_apps_with_delay(self):
        """Launch selected applications with delay"""
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one application to launch.")
            return
        
        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                raise ValueError("Delay must be non-negative")
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Please enter a valid non-negative number for delay.")
            return
        
        self.launch_apps(selected, delay)

    def launch_apps(self, app_paths, delay):
        """Launch applications with specified delay"""
        def launch_thread():
            success_count = 0
            total_count = len(app_paths)
            
            for i, app_path in enumerate(app_paths, 1):
                if not os.path.exists(app_path):
                    self.update_status(f"Error: File not found - {os.path.basename(app_path)}")
                    continue
                
                if delay > 0:
                    self.update_status(f"Launching in {delay}s ({i}/{total_count}): {os.path.basename(app_path)}")
                    time.sleep(delay)
                
                try:
                    # Launch the application
                    if sys.platform == "win32":
                        os.startfile(app_path)
                    else:
                        subprocess.Popen([app_path])
                    
                    # Update stats
                    self.update_app_stats(app_path)
                    success_count += 1
                    
                    self.update_status(f"Launched ({i}/{total_count}): {os.path.basename(app_path)}")
                    
                except Exception as e:
                    self.update_status(f"Error launching {os.path.basename(app_path)}: {str(e)}")
            
            # Final status
            if success_count == total_count:
                self.update_status(f"Successfully launched all {total_count} applications")
            else:
                self.update_status(f"Launched {success_count}/{total_count} applications")
            
            # Refresh app tree to show updated stats
            self.root.after(1000, lambda: self.update_app_tree(self.app_paths[self.current_category]))
        
        # Run in separate thread to prevent GUI freezing
        Thread(target=launch_thread, daemon=True).start()

    def update_app_stats(self, app_path):
        """Update application usage statistics"""
        self.app_stats[app_path]['launches'] += 1
        self.app_stats[app_path]['last_used'] = datetime.now().isoformat()
        self.save_stats()

    def update_status(self, message):
        """Update status bar message"""
        self.root.after(0, lambda: self.status_label.configure(text=message))

    def refresh_display(self):
        """Refresh all displays"""
        # Clean up non-existent files
        cleaned = False
        for category in list(self.app_paths.keys()):
            original_count = len(self.app_paths[category])
            self.app_paths[category] = [p for p in self.app_paths[category] if os.path.exists(p)]
            if len(self.app_paths[category]) != original_count:
                cleaned = True
        
        # Clean up favorites
        self.favorites = {f for f in self.favorites if os.path.exists(f)}
        
        if cleaned:
            self.save_app_paths()
            self.save_favorites()
            self.update_status("Cleaned up non-existent files")
        
        # Refresh displays
        self.update_category_tree()
        if self.current_category in self.app_paths:
            self.update_app_tree(self.app_paths[self.current_category])
        
        self.update_status("Display refreshed")

    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit PyLauncher Pro?"):
            self.root.destroy()

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = AppLauncher()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unexpected error occurred:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
