import os
import json
import time
import tkinter as tk
import subprocess
from threading import Thread
from tkinter import messagebox
import customtkinter as ctk

class AppLauncher:
    def __init__(self):
        self.APP_LIST_FILE = "app_paths.json"
        self.app_paths = self.load_app_paths()
        self.setup_gui()

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
        self.root = ctk.CTk()
        self.root.title("App Launcher Pro")
        self.root.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill='both', expand=True, padx=15, pady=15)

        self.category_frame = ctk.CTkFrame(self.main_container, width=250)
        self.category_frame.pack(side='left', fill='y', padx=(0, 15))

        self.category_label = ctk.CTkLabel(self.category_frame, text="Categories", font=("Segoe UI", 14, "bold"))
        self.category_label.pack(pady=10)

        self.category_listbox = tk.Listbox(
            self.category_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            selectmode='single',
            width=25,
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor='#3d3d3d',
            selectbackground='#2c5282',
            activestyle='none'
        )
        self.category_listbox.pack(fill='both', expand=True, pady=10)
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)

        self.add_category_btn = ctk.CTkButton(
            self.category_frame,
            text="Add Category",
            command=self.add_category,
            font=("Segoe UI", 12),
            height=35
        )
        self.add_category_btn.pack(pady=10, padx=10, fill='x')

        self.app_frame = ctk.CTkFrame(self.main_container)
        self.app_frame.pack(side='left', fill='both', expand=True)

        self.app_label = ctk.CTkLabel(self.app_frame, text="Applications", font=("Segoe UI", 14, "bold"))
        self.app_label.pack(pady=10)

        self.app_listbox = tk.Listbox(
            self.app_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            selectmode='extended',
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor='#3d3d3d',
            selectbackground='#2c5282',
            activestyle='none'
        )
        self.app_listbox.pack(fill='both', expand=True, pady=10)
        self.app_listbox.bind('<Control-a>', self.select_all)

        self.control_frame = ctk.CTkFrame(self.app_frame)
        self.control_frame.pack(fill='x', pady=10)

        self.add_app_btn = ctk.CTkButton(
            self.control_frame,
            text="Add App",
            command=self.add_app_path,
            font=("Segoe UI", 12),
            height=35
        )
        self.add_app_btn.pack(side='left', padx=5)

        self.remove_app_btn = ctk.CTkButton(
            self.control_frame,
            text="Remove App",
            command=self.remove_app_path,
            font=("Segoe UI", 12),
            height=35
        )
        self.remove_app_btn.pack(side='left', padx=5)

        self.delay_label = ctk.CTkLabel(self.control_frame, text="Delay (sec):", font=("Segoe UI", 12))
        self.delay_label.pack(side='left', padx=5)

        self.delay_entry = ctk.CTkEntry(self.control_frame, width=70, height=35)
        self.delay_entry.pack(side='left', padx=5)
        self.delay_entry.insert(0, "5")

        self.launch_btn = ctk.CTkButton(
            self.control_frame,
            text="Launch Selected",
            command=self.launch_apps_with_delay,
            font=("Segoe UI", 12),
            height=35
        )
        self.launch_btn.pack(side='left', padx=5)

        self.status_label = ctk.CTkLabel(self.root, text="Ready", anchor="w", font=("Segoe UI", 11))
        self.status_label.pack(fill='x', padx=15, pady=10)

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
            self.app_listbox.insert(tk.END, os.path.basename(path))

    def get_current_category(self):
        selection = self.category_listbox.curselection()
        return self.category_listbox.get(selection[0]) if selection else "Uncategorized"

    def add_app_path(self):
        path = tk.filedialog.askopenfilename(
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
        try:
            selected_indices = self.app_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("No Selection", "Please select an application to remove.")
                return

            category = self.get_current_category()
            for index in reversed(selected_indices):
                self.app_paths[category].pop(index)

            self.save_app_paths()
            self.update_app_list(category)
            messagebox.showinfo("Success", "Selected applications removed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove application: {e}")

    def launch_apps_with_delay(self):
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one application to launch.")
            return

        try:
            delay_seconds = float(self.delay_entry.get())
            if delay_seconds < 0:
                raise ValueError("Delay must be positive")
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Please enter a valid positive number for delay.")
            return

        category = self.get_current_category()
        Thread(target=self.launch_thread, args=(selected_indices, category, delay_seconds)).start()

    def launch_thread(self, selected_indices, category, delay_seconds):
        for index in selected_indices:
            app_path = self.app_paths[category][index]
            self.status_label.configure(
                text=f"Launching in {delay_seconds} seconds: {os.path.basename(app_path)}"
            )
            time.sleep(delay_seconds)
            try:
                subprocess.Popen(app_path)
                self.status_label.configure(
                    text=f"Launched: {os.path.basename(app_path)}"
                )
            except Exception as e:
                self.status_label.configure(
                    text=f"Failed to launch: {os.path.basename(app_path)}"
                )
                messagebox.showerror("Error", f"Failed to launch {app_path}: {e}")

        self.status_label.configure(text="All applications launched.")

    def select_all(self, event=None):
        self.app_listbox.select_set(0, tk.END)
        return "break"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppLauncher()
    app.run()
