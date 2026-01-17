# 🚀 PyLauncher v2.1

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge&logo=python" alt="Tkinter">
  <img src="https://img.shields.io/badge/Free%20to%20Modify-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge" alt="PRs Welcome">
</div>

**Modern application launcher** with categories, favorites, usage stats, delayed/batch launching, real-time search, and clean dark theme - built with pure Python + tkinter (zero external dependencies).

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Keyboard Shortcuts](#-keyboard-shortcuts) • [Contributing](#-contributing) • [License](#-license)

## ✨ Features

- 🎨 Sleek dark theme with modern ttk styling  
- 📁 Custom categories - organize apps any way you want  
- ⭐ Favorites - pin important apps to the top  
- 📊 Usage statistics - shows launch count + last used date  
- ⏰ Delayed launching - add seconds between apps (great for heavy startup sequences)  
- 🔄 Batch launch - start multiple programs with one click  
- 🔍 Real-time search & filter - type to narrow down instantly  
- 📂 Open containing folder - right from the launcher  
- 💾 Auto-save everything - categories, favorites & stats in JSON  
- ⌨️ Full keyboard support - fast navigation for power users  

## 🛠️ Installation

**Requirements**  
- Python 3.7 or higher  
- Only standard library modules (tkinter, json, os, threading) - **no pip installs needed**

**Quick start**  
1. Download `la.py`  
2. Run: python la.py
3. First launch creates:
- `app_paths.json` - categories + app paths  
- `app_stats.json` - launch counts & dates  
- `favorites.json` - favorite apps  

**File structure**

Tested primarily on Windows, works on macOS & Linux too.

## 🎯 Usage

### Category Management
- Add category → click ➕ next to "Categories"  
- Remove category → select it → click ➖ (apps inside get removed too)

### App Management
- Add app → pick category → click ➕ Add App → select .exe / .bat / etc.  
- Remove app → select (Ctrl+click for multiple) → click ➖ Remove or press Delete  
- Favorite app → select → click ⭐ (favorites move to top with star icon)

### Launching
- Single app → double-click / select + Enter / click ▶ Launch  
- Batch + delay → multi-select → set delay (seconds) → click ▶ Launch  
- Search → type in the top search box (filters live as you type)

### Extra Tools
- 📁 Open Folder → select app → click button or right-click  
- 🔄 Refresh → removes missing files & refreshes stats  
- Status bar shows current category count & total apps

## ⌨️ Keyboard Shortcuts

| Key            | Action                        |
|----------------|-------------------------------|
| Ctrl + N       | Add new application           |
| Delete         | Remove selected apps          |
| F5             | Refresh list                  |
| Ctrl + F       | Focus search bar              |
| Enter          | Launch selected app(s)        |
| Ctrl + Q       | Quit PyLauncher               |
| Double-click   | Launch app                    |

## 🤝 Contributing

**Completely free to modify, fork, redistribute, or use commercially - no restrictions at all.**

1. Fork the repo  
2. Create your branch (`git checkout -b feature/my-cool-addition`)  
3. Commit changes (`git commit -m 'Add amazing feature'`)  
4. Push (`git push origin feature/my-cool-addition`)  
5. Open a Pull Request  

Even small improvements (bug fixes, UI tweaks, better Linux support) are very welcome.

## 📝 License

**Free to modify • Free to distribute • No restrictions**  
Do whatever you want - change it, sell it, fork it, whatever.

## 🙏 Acknowledgments

- Pure Python standard library only  
- Dark theme via `ttk.Style`  
- Simple JSON-based persistence  

---

<div align="center">
  <b>PyLauncher v2.1</b> - Simple. Fast. Yours to hack.<br>
  <small>Free forever • Built with ♥ by emy using python</small>
</div>
