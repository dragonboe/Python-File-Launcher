# 🚀 PyLauncher v2.1

<div align="center">

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=python)](https://www.python.org/)

[![GUI Framework](https://img.shields.io/badge/GUI-Tkinter-blue.svg?style=for-the-badge&logo=python)](https://docs.python.org/3/library/tkinter.html)

[![License: Free](https://img.shields.io/badge/License-Free%20to%20Modify-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

### A modern application launcher with category management, favorites, usage statistics, and delayed launch capabilities.

[Features](#-features) • [Installation](#%EF%B8%8F-installation) • [Usage](#-usage) • [Keyboard Shortcuts](#-keyboard-shortcuts) • [Contributing](#-contributing) • [License](#-license)

</div>

## ✨ Features

<table>
  <tr>
    <td>🎨 <b>Modern Dark Theme</b></td>
    <td>Sleek dark interface with modern styling using native tkinter</td>
  </tr>
  <tr>
    <td>📁 <b>Category Management</b></td>
    <td>Organize applications into custom categories with add/remove functionality</td>
  </tr>
  <tr>
    <td>⭐ <b>Favorites System</b></td>
    <td>Mark frequently used applications as favorites for quick access</td>
  </tr>
  <tr>
    <td>📊 <b>Usage Statistics</b></td>
    <td>Track launch counts and last used dates for all applications</td>
  </tr>
  <tr>
    <td>⏰ <b>Delayed Launch</b></td>
    <td>Set custom delays between application launches for optimal system performance</td>
  </tr>
  <tr>
    <td>🔄 <b>Batch Launch</b></td>
    <td>Launch multiple applications with a single click - perfect for workflow automation</td>
  </tr>
  <tr>
    <td>🔍 <b>Search & Filter</b></td>
    <td>Quickly find applications with real-time search functionality</td>
  </tr>
  <tr>
    <td>📁 <b>Folder Integration</b></td>
    <td>Open application folders directly from the launcher</td>
  </tr>
  <tr>
    <td>💾 <b>Persistent Storage</b></td>
    <td>Categories, favorites, and statistics saved automatically in JSON format</td>
  </tr>
  <tr>
    <td>⌨️ <b>Keyboard Shortcuts</b></td>
    <td>Full keyboard navigation and shortcuts for power users</td>
  </tr>
</table>

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Standard Python libraries (tkinter, json, os, threading)
- Windows (primary support), macOS and Linux compatible

### Quick Start

1. **Download the script:**
```bash
# Clone or download la.py
python la.py
```

2. **No additional dependencies required** - uses only Python standard library

3. **First run will create necessary files:**
   - `app_paths.json` - Application categories and paths
   - `app_stats.json` - Usage statistics
   - `favorites.json` - Favorite applications

### File Structure
```
PyLauncher/
├── la.py              # Main application
├── app_paths.json     # Categories and app paths (auto-created)
├── app_stats.json     # Usage statistics (auto-created)
└── favorites.json     # Favorite apps (auto-created)
```

## 🎯 Usage

### 1. Category Management
- **Create Categories** 📂
  - Click "➕" next to Categories
  - Enter category name
  - Organize your apps logically
  - Default "Uncategorized" category always available

- **Remove Categories** ➖
  - Select category in left panel
  - Click "➖" button
  - Confirm removal (apps will be deleted)

### 2. Application Management
- **Add Applications** ➕
  - Select target category
  - Click "➕ Add App"
  - Choose executable file (.exe, .bat, .cmd)
  - Apps are saved automatically

- **Remove Applications** ➖
  - Select apps in main view (Ctrl+Click for multiple)
  - Click "➖ Remove" or press Delete
  - Confirm removal

### 3. Favorites & Statistics
- **Mark as Favorite** ⭐
  - Select applications
  - Click "⭐ Favorite" button
  - Favorites appear with star icon and sort to top

- **View Statistics** 📊
  - Launch count and last used date shown for each app
  - Statistics update automatically on launch
  - Displayed in application tree view

### 4. Launch Options
- **Quick Launch** 🚀
  - Double-click application
  - Or select and press Enter
  - Or click "▶ Launch"

- **Delayed Launch** ⏰
  - Set delay in seconds (bottom right)
  - Select multiple apps
  - Click "▶ Launch" for sequential launch with delays

### 5. Additional Features
- **Search** 🔍
  - Use search box to filter applications in current category
  - Real-time filtering as you type

- **Open Folder** 📁
  - Select application
  - Click "📁 Open Folder" to open containing directory

- **Refresh** 🔄
  - Click "🔄 Refresh" to clean up missing files
  - Updates all displays and statistics

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Add new application |
| `Delete` | Remove selected applications |
| `F5` | Refresh display |
| `Ctrl+F` | Focus search box |
| `Enter` | Launch selected applications |
| `Ctrl+Q` | Quit application |
| `Double-Click` | Launch application |

## �️p Interface

The modern interface includes:
- 📋 **Left Panel**: Category tree with app counts
- � **Mtain View**: Application list with statistics
- 🔍 **Search Bar**: Real-time application filtering  
- ⚙️ **Control Panel**: Launch options and management buttons
- 📊 **Status Bar**: Current operation status and app counts

### Data Files
- `app_paths.json` - Categories and application paths
- `app_stats.json` - Launch statistics and usage data
- `favorites.json` - Favorite application list

## 🤝 Contributing

**Copyright is free to modify, no publishing restrictions or commercial limitations. Anyone can pull request, modify, and update parts.**

We welcome contributions! This project is open for:

1. **Fork and modify freely** - No restrictions on modifications
2. **Submit pull requests** - All improvements welcome
3. **Update and enhance** - Add features, fix bugs, improve UI
4. **Share modifications** - No publishing restrictions

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Make your changes to `la.py`
4. Test your modifications
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing`)
7. Open a Pull Request

### Development Notes
- Uses only Python standard library (tkinter, json, os, threading, etc.)
- Modern dark theme implemented with ttk.Style
- JSON-based data persistence
- Cross-platform compatible (Windows primary, macOS/Linux supported)

## 📝 License

**Free to modify and distribute. No commercial restrictions.**

This project is released under a free license:
- ✅ Modify freely
- ✅ Distribute modifications  
- ✅ Commercial use allowed
- ✅ No attribution required
- ✅ Pull requests welcome

## 🙏 Acknowledgments

- Built with Python's standard tkinter library
- Modern dark theme styling with ttk
- JSON-based configuration for simplicity
- Cross-platform compatibility focus

---

<div align="center">

**PyLauncher v2.1** - Modern Application Launcher

*Free to modify • No restrictions • Pull requests welcome*

</div>
