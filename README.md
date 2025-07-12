# 🌍 Global Time Utility (gtime)

[![PyPI version](https://badge.fury.io/py/gtime.svg)](https://badge.fury.io/py/gtime)
[![Python Support](https://img.shields.io/pypi/pyversions/gtime.svg)](https://pypi.org/project/gtime/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A modern, colorful Python CLI utility for global time zone lookup, comparison, and management**

Sick of Googling time zones every day?! Stop wasting time figuring out the time. 🕐 gtime makes it effortless to work across time zones with fuzzy search, favorites, real-time updates, and beautiful terminal output.

## ⭐ **Love this project? Give it a star!**

If gtime helps you manage time zones more efficiently, please consider giving it a ⭐ on GitHub! Your support helps us improve and motivates continued development.

[⭐ **Star this project**](https://github.com/savitojs/gtime) • [🐛 Report issues](https://github.com/savitojs/gtime/issues) • [💡 Request features](https://github.com/savitojs/gtime/issues)

---

## 🎯 Why gtime?

- **⚡ Lightning fast** - Optimized for large city databases
- **🔍 Smart search** - Fuzzy matching finds cities even with typos
- **❤️ Favorites** - Save your most-used cities for quick access
- **🔄 Live updates** - Watch mode for real-time monitoring
- **🎨 Beautiful output** - Colorful, rich terminal interface
- **🤝 Meeting helper** - Convert meeting times across all favorites with timezone support
- **🌐 Global team ready** - Supports UTC, EST, PST, JST, CET and more timezones
- **📊 Compare easily** - Side-by-side time comparisons

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install gtime
```

### From Source
```bash
git clone https://github.com/savitojs/gtime.git
cd gtime
pip install .
```

## 🚀 Quick Start

```bash
# Get the time in any city
gtime London

# Add cities to your favorites
gtime add Tokyo Singapore "New York"

# See all your favorite cities at once
gtime list

# Compare times across multiple cities
gtime compare London Tokyo Sydney

# Find the perfect meeting time
gtime meeting at "2:00 PM"

# Live monitoring mode
gtime watch
```

## 🎬 Demo

**See gtime in action:**

![demo](./assets/demo.gif)

*Note: Some command output may appear broken in the demo, but it works perfectly in real terminal usage*

## 🎯 Features

### 🏙️ City Lookup
- **Fuzzy search**: `gtime toky` finds Tokyo
- **Suggestions**: Get helpful suggestions for misspelled cities
- **Instant results**: Lightning-fast lookups even with huge databases

### ⭐ Favorites Management
```bash
gtime add "Los Angeles" Berlin Mumbai    # Add multiple cities
gtime remove Tokyo                       # Remove a city
gtime list                              # View all favorites
gtime clear                             # Clear all favorites
```

### 🔍 Multi-City Comparison
```bash
gtime compare London Tokyo "New York"   # Compare specific cities
gtime compare                           # Compare all favorites
```

### 📅 Meeting Time Conversion
```bash
gtime meeting at "10:00 AM"            # Convert across favorites
gtime meeting at "15:30"               # 24-hour format supported
gtime meeting at "3 PM UTC"            # Shows "Coordinated Universal Time (UTC)"
gtime meeting at "9:00 AM EST"         # Shows "Eastern Standard Time (EST)"
```

### 👀 Live Watch Mode
```bash
gtime watch                             # Monitor all favorites
gtime watch London Tokyo                # Watch specific cities
```

### 🌐 Timezone Support
When you specify a timezone, gtime shows the full timezone name for clarity:
```bash
gtime meeting at "10:00 AM JST"         # Shows: "Japan Standard Time (JST)"
gtime meeting at "3 PM UTC"             # Shows: "Coordinated Universal Time (UTC)"
gtime meeting at "2:00 PM EST"          # Shows: "Eastern Standard Time (EST)"
```

## 📚 Usage Examples

### Basic Usage
```bash
# Simple city lookup
gtime Paris
gtime "San Francisco"
gtime mumbai                    # Case insensitive

# With fuzzy matching
gtime pairs                     # Finds Paris
gtime newyork                   # Finds New York
```

### Managing Favorites
```bash
# Build your favorite cities list
gtime add London Tokyo "San Francisco" Berlin
gtime add Mumbai                # Add one more
gtime list                      # See your collection

# Remove cities you no longer need
gtime remove Berlin
gtime clear                     # Start fresh
```

### Advanced Features
```bash
# Compare multiple cities
gtime compare London Tokyo Sydney Mumbai

# Perfect for planning meetings
gtime meeting at "9:00 AM"      # What time is 9 AM across favorites?
gtime meeting at "14:30"        # 24-hour format supported
gtime meeting at "3 PM UTC"     # Timezone support for global teams

# Real-time monitoring
gtime watch                     # Live updates every second
```

## 🛠️ Development

### Running Tests
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run performance tests
python tests/perf/profile_lookup.py
```

### Contributing
We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 🚀 GitHub Actions

This project includes automated workflows:
- **🧪 Tests**: Runs on every push/PR across Python 3.8-3.12
- **📦 Publish**: Automatically publishes to PyPI upon new GitHub release

## 🎨 Screenshots

*Coming soon - we're working on adding more visual examples!*

## 🤝 Support

- 📖 **Documentation**: Check out our [Wiki](https://github.com/savitojs/gtime/wiki)
- 🐛 **Bug Reports**: [Create an issue](https://github.com/savitojs/gtime/issues)
- 💡 **Feature Requests**: [Suggest new features](https://github.com/savitojs/gtime/issues)
- 💬 **Discussions**: [Join the conversation](https://github.com/savitojs/gtime/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Show Your Support

If gtime makes your life easier, please consider:
- ⭐ **Starring this repository**
- 🐦 **Sharing it on social media**
- 📝 **Writing a review**
- 🤝 **Contributing to the project**

**Made with ❤️ for developers working across time zones**

---

*Happy time zone management! 🌍*