# PyLauncher V2.2

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-FreeSimpleGUI-blue?style=for-the-badge" alt="FreeSimpleGUI">
  <img src="https://img.shields.io/badge/Free%20to%20Modify-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge" alt="PRs Welcome">
</div>

**Fast, minimal application launcher** with categories, favorites, usage stats, delayed/batch launching, real-time search, customizable shortcuts, and clean dark theme - built with Python + FreeSimpleGUI.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Keyboard Shortcuts](#-keyboard-shortcuts) • [Contributing](#-contributing) • [License](#-license)

<img width="1852" height="1080" alt="{68F7E330-1D2B-4857-B331-A1B56066F0D0}" src="https://github.com/user-attachments/assets/fe930867-2b84-43fc-81fc-8d8f82dfc9e9" />

## ✨ Features

- 🎨 **Clean, minimal dark theme** - no clutter, just functionality
- 📁 **Custom categories** - organize apps any way you want  
- ⭐ **Favorites system** - pin important apps to the top (marked with *)
- 📊 **Usage statistics** - tracks launch count + last used date  
- ⏰ **Delayed launching** - add seconds between apps for sequential startup
- 🔄 **Batch launch** - start multiple programs with one click  
- 🔍 **Real-time search** - type to filter apps instantly  
-  **Auto-save** - all data persisted in JSON  
- ⌨️ **Customizable keyboard shortcuts** - configure your own hotkeys
- 📖 **Built-in help system** - comprehensive user guide included
- ⚙️ **Settings dialog** - customize shortcuts to your preference

## 🛠️ Installation

**Requirements**  
- Python 3.7 or higher  
- FreeSimpleGUI (free, no licensing restrictions)

**Quick start**  
1. Clone or download this repository
2. Install FreeSimpleGUI:
   ```bash
   pip install FreeSimpleGUI
   ```
3. Run the launcher:
   ```bash
   python launcher.py
   ```
4. First launch creates `launcher_cfg.json` for all your data

**File structure**
```
PyLauncher/
├── launcher.py          # Main application
└── launcher_cfg.json    # Auto-generated config (categories, apps, shortcuts)
```

Works on Windows, macOS, and Linux.

## 🎯 Usage

### Category Management
- **Add category** → click `+` button below categories list
- **Remove category** → select category → click `-` button
- **Switch category** → click any category to view its apps

### App Management
- **Add app** → select category → click `Add` → browse for executable
- **Remove app** → select app(s) → click `Remove` or press `Delete`
- **Favorite app** → select app(s) → click `Favorite` (favorites show `*` and appear at top)

### Launching Apps
- **Single app** → select → click `LAUNCH` or press `Ctrl+L`
- **Multiple apps** → Ctrl+click to select multiple → click `LAUNCH`
- **With delay** → set delay in seconds → click `LAUNCH` (useful for sequential startup)
- **Search** → type in search box to filter apps in real-time

### Keyboard Shortcuts (Customizable)
- **Ctrl+L** - Launch selected app(s)
- **Ctrl+A** - Add new application
- **Ctrl+F** - Focus search box
- **Ctrl+N** - Create new category
- **Delete** - Remove selected app(s)
- **Ctrl+Q** - Quit application

**Customize shortcuts**: Go to `Settings` → `Shortcuts` to change any hotkey

### Help & Settings
- **Help** → `User Guide` - comprehensive documentation
- **Help** → `About` - application info
- **Settings** → `Shortcuts` - customize keyboard shortcuts
- **Settings** → `Quit` - exit application

## 📊 Features in Detail

### Statistics Tracking
Every app shows:
- **Runs** - total number of launches
- **Last Used** - date and time of last launch
- Automatically updated on each launch

### Favorites System
- Mark apps as favorites with the `Favorite` button
- Favorites appear at the top of the list
- Marked with `*` in the Fav column
- Perfect for frequently used applications

### Batch Launching
1. Select multiple apps (Ctrl+click)
2. Set delay (optional, in seconds)
3. Click `LAUNCH`
4. Apps launch sequentially with specified delay

### Search & Filter
- Type in search box to filter apps instantly
- Case-insensitive search
- Searches app names only
- Clear search to see all apps

## 🎨 Design Philosophy

PyLauncher V2.2 follows a **minimal, clean design**:
- No unnecessary emojis or visual clutter
- Compact layout (800x500 default)
- Fast and responsive
- Simple, clear labels
- Focus on functionality over decoration

## 🤝 Contributing

**Completely free to modify, fork, redistribute, or use commercially - no restrictions.**

1. Fork the repo  
2. Create your branch (`git checkout -b feature/amazing-feature`)  
3. Commit changes (`git commit -m 'Add amazing feature'`)  
4. Push (`git push origin feature/amazing-feature`)  
5. Open a Pull Request  

All contributions welcome - bug fixes, features, UI improvements, documentation, etc.

## 📝 License

**Free to modify • Free to distribute • No restrictions**  
Do whatever you want - change it, sell it, fork it, whatever.

## � Technical Details

- **GUI Framework**: FreeSimpleGUI 5.2.0+ (free PySimpleGUI fork)
- **Data Storage**: JSON (launcher_cfg.json)
- **Threading**: Background threads for app launching
- **Platform Support**: Windows (primary), macOS, Linux
- **Code**: ~400 lines of clean, well-documented Python

## 🙏 Acknowledgments

- Built with FreeSimpleGUI (free PySimpleGUI fork)
- Dark theme via FreeSimpleGUI's built-in themes
- JSON-based persistence for simplicity
- No external dependencies beyond FreeSimpleGUI

---

<div align="center">
  <b>PyLauncher V2.2</b> - Simple. Fast. Minimal.<br>
  <small>Free forever • Built with ♥ using Python</small>
</div>
