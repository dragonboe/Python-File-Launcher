# 🚀 App Launcher Pro

<div align="center">

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue.svg?style=for-the-badge&logo=python)](https://github.com/TomSchimansky/CustomTkinter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/dragonboe/Python-File-Launcher)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

<p align="center">
  <img src="https://raw.githubusercontent.com/dragonboe/Python-File-Launcher/main/preview.gif" alt="App Preview" width="600"/>
</p>

### A modern, sleek application launcher with category management and delayed launch capabilities.

[Features](#-features) • [Installation](#%EF%B8%8F-installation) • [Usage](#-usage) • [Contributing](#-contributing) • [License](#-license)

</div>

## ✨ Features

<table>
  <tr>
    <td>🎨 <b>Modern Dark Theme</b></td>
    <td>Sleek and easy on the eyes with customizable appearance</td>
  </tr>
  <tr>
    <td>📁 <b>Category Management</b></td>
    <td>Organize applications into custom categories for better workflow</td>
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
    <td>💾 <b>Persistent Storage</b></td>
    <td>Your categories and applications are saved automatically and securely</td>
  </tr>
  <tr>
    <td>⌨️ <b>Keyboard Shortcuts</b></td>
    <td>Quick actions with intuitive keyboard shortcuts for power users</td>
  </tr>
</table>

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Windows/macOS/Linux

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/dragonboe/Python-File-Launcher.git
cd Python-File-Launcher
```

2. **Install dependencies:**
```bash
pip install customtkinter pillow
```

3. **Launch the application:**
```bash
python de.py
```

### Troubleshooting

- If you encounter any dependency issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

- For CustomTkinter display issues:
```bash
pip uninstall customtkinter
pip install customtkinter --upgrade
```

## 🎯 Usage

### 1. Category Management
- **Create Categories** 📂
  - Click "Add Category"
  - Enter category name
  - Organize your apps logically

### 2. Application Management
- **Add Applications** ➕
  - Select target category
  - Click "Add App"
  - Choose executable file
  - Apps are saved automatically

### 3. Launch Configuration
- **Single/Batch Launch** 🚀
  - Select multiple apps (Ctrl+Click)
  - Set launch delay
  - Click "Launch Selected"

### 4. Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| Ctrl+A | Select all apps |
| Delete | Remove selected |
| Enter | Launch selected |

## 🖥️ Interface

<div align="center">
<img src="https://raw.githubusercontent.com/dragonboe/Python-File-Launcher/main/screenshot.png" alt="Interface Screenshot" width="600"/>
</div>

The modern interface includes:
- 📋 Category Management Panel
- 📱 Application List View
- ⚙️ Launch Control Center
- 📊 Status Dashboard

## 🤝 Contributing

We love your input! We want to make contributing as easy and transparent as possible. Please:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/dragonboe/Python-File-Launcher.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -r requirements-dev.txt
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Inspired by the need for a modern, efficient application launcher

---

<div align="center">

[![Stargazers](https://img.shields.io/github/stars/dragonboe/Python-File-Launcher.svg?style=social)](https://github.com/dragonboe/Python-File-Launcher/stargazers)
[![Follow](https://img.shields.io/github/followers/dragonboe.svg?style=social&label=Follow)](https://github.com/dragonboe)

Made with ❤️ by dragonboe aka marla :)

</div>
