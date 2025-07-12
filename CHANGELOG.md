# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2025-07-11

### Added
- Added `__main__.py` to support `python -m gtime` execution
- Added comprehensive changelog documentation

### Changed
- Compressed demo.gif for faster downloads

## [0.3.2] - 2025-07-11

### Fixed
- Fixed clock emoji display issues on kitty and ghostty terminals
- Improved terminal compatibility for various terminal emulators

## [0.3.1] - 2025-07-07

### Added
- **Major Feature**: 4-tier fuzzy search algorithm with priority-based matching
  - Exact match (highest priority)
  - Starts with match
  - Substring match  
  - Fuzzy match (lowest priority)
- **Major Feature**: 24-hour format support for meeting times
  - Support for formats like "15:30", "21:00"
  - Hour-only formats: "15", "3 PM"
  - Maintains backward compatibility with 12-hour formats
- **Major Feature**: Comprehensive timezone support
  - Support for timezone abbreviations (UTC, EST, PST, JST, CET, etc.)
  - Automatic timezone conversion for meeting times
  - Clear timezone explanation messages
- **Enhancement**: Improved meeting time parsing
  - Enhanced `parse_meeting_time()` function
  - Better error handling for invalid time formats
  - Support for both "at" and "on" keywords
- **Enhancement**: Timezone conversion clarity
  - Added "✓ Meeting time converted from X" messages
  - Full timezone name explanations (e.g., "Japan Standard Time (JST)")
  - Better user feedback for timezone operations

### Fixed
- **Critical Bug**: Fixed fuzzy search returning incorrect cities
  - "pairs" now correctly returns "Paris" instead of "Buenos Aires"
  - Algorithm now focuses on city names rather than full "City (Country)" strings
- **Bug**: Fixed timezone conversion issues in meeting mode
  - Proper handling of naive datetime objects
  - Improved local timezone detection
- **Bug**: Fixed print_favorites() function timezone handling
  - Resolved crashes when converting between timezones
  - Better error handling for timezone edge cases

### Changed
- **Performance**: Added LRU caching for city searches (@lru_cache(maxsize=256))
- **Performance**: Optimized city name indexing with global cache
- **Performance**: Lazy loading of city database for faster startup
- **UX**: Improved error messages for invalid cities and suggestions
- **UX**: Enhanced help text with new feature examples
- **UX**: Better formatting for timezone information display

### Testing
- **Added**: Comprehensive test suite with 40 tests
- **Added**: Tests for fuzzy search improvements (6 tests)
- **Added**: Tests for 24-hour format support (6 tests)
- **Added**: Tests for timezone support (8 tests)
- **Added**: Integration tests for complex scenarios (7 tests)
- **Added**: Error handling tests (4 tests)
- **Added**: Backward compatibility tests (3 tests)
- **Added**: Performance tests for large city databases
- **Coverage**: 100% test pass rate

### Documentation
- **Enhanced**: Complete README.md rewrite with professional styling
- **Added**: Multiple star encouragement sections
- **Added**: Comprehensive usage examples
- **Added**: Feature highlights and "Why gtime?" section
- **Added**: PyPI badges and project metadata
- **Enhanced**: Help system with new feature documentation
- **Added**: Demo files and configuration updates

### Development
- **Added**: PyPI classifiers for better package discovery
- **Added**: Proper Python version support declarations (3.7-3.12)
- **Added**: Performance profiling tools
- **Enhanced**: Package metadata and keywords
- **Added**: Comprehensive dependency management

## [0.2.0] - 2025-07-06

### Added
- Initial release of Global Time Utility (gtime)
- Basic city lookup functionality
- Fuzzy search for city names
- Favorites management (add, remove, list, clear)
- Multi-city comparison
- Meeting time conversion
- Watch mode for real-time updates
- Colorful terminal output with Rich library
- Support for 200+ cities worldwide
- Emoji representations for cities
- Time-based greetings and fun facts

### Features
- **City Lookup**: Search for any city with fuzzy matching
- **Favorites**: Save frequently used cities
- **Compare**: Side-by-side time comparisons
- **Meetings**: Convert meeting times across favorite cities
- **Watch Mode**: Live updates with countdown timer
- **Rich Output**: Beautiful terminal interface with colors and emojis

### Dependencies
- rich: For colorful terminal output
- python-dateutil: For date/time parsing
- thefuzz: For fuzzy string matching
- pytz: For timezone handling (Python < 3.9)

### Supported Platforms
- Linux
- macOS
- Windows
- Python 3.7+

---

## Development Notes

### Version Numbering
- **Major (X.0.0)**: Breaking changes or major new features
- **Minor (0.X.0)**: New features, enhancements, significant improvements
- **Patch (0.0.X)**: Bug fixes, small improvements, compatibility updates

### Release Process
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with new changes
3. Run full test suite: `pytest tests/`
4. Create git tag: `git tag vX.X.X`
5. Push to GitHub: `git push origin main --tags`
6. Build and upload to PyPI: `python -m build && twine upload dist/*`

### Contributing
- All changes should be documented in this changelog
- Follow semantic versioning principles
- Include tests for new features
- Update documentation as needed 