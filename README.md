# Global Time Utility (gtime) 🌐

Global Time Utility (gtime) is a modern, colorful Python CLI utility for global time zone lookup, comparison, and management. It supports fuzzy search, favorites, city comparison, meeting time conversion, and a live/watch mode

## Features
- Fast city lookup with fuzzy search and suggestions
- Add/remove/list favorite cities
- Compare times for multiple cities
- Meeting time conversion across favorites
- Live/watch mode for real-time updates
- Colorful, user-friendly output (using Rich)
- Comprehensive test suite (pytest)
- Performance-optimized for large city databases

## Installation (from source)
Clone the repo and install locally:

```sh
pip install .
```

Or, install from PyPI:

```sh
pip install gtime
```
## Demo

**Note:** Some command output may appear broken in the demo, but it works correctly in real use

![demo](./assets/demo.gif)

## Usage
After installation, run the CLI:

```sh
gtime [command] [arguments]
```

Or as a module:

```sh
python -m gtime.cli [command] [arguments]
```

Example commands:
- `gtime London` — Show time for London
- `gtime add Tokyo` — Add Tokyo to favorites
- `gtime list` — List favorite cities
- `gtime compare London Tokyo` — Compare cities
- `gtime meeting at 10:00 AM` — Meeting time conversion
- `gtime watch` — Live mode

## Development & Publishing

### GitHub Actions
This project includes automated workflows:
- **Tests**: Runs on every push/PR across Python 3.8-3.12
- **Publish**: Automatically publishes to PyPI upon new GitHub release

## License
MIT