#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive test script for Global Time Utility (gtime)
Tests all city and country combinations to ensure search accuracy.
"""

import sys
import os
import datetime
import json
from collections import defaultdict
from pathlib import Path

# Add the gtime package to path (from tests directory, go up one level)
sys.path.insert(0, '..')

from gtime.data import CITY_DB, COUNTRY_CAPITALS
from gtime.core import get_city_by_name, fuzzy_search_city, suggest_cities

def analyze_city_db():
    """Analyze the CITY_DB structure to extract all cities and countries."""
    cities = set()
    countries = set()
    country_to_cities = defaultdict(list)

    for city, country, timezone, emoji in CITY_DB:
        cities.add(city)
        countries.add(country)
        country_to_cities[country].append((city, timezone, emoji))

    return cities, countries, country_to_cities

def identify_capitals(country_to_cities):
    """Identify which city should be the capital for each country."""
    capitals = {}

    # Use the imported COUNTRY_CAPITALS mapping
    known_capitals = COUNTRY_CAPITALS

    # Check if the known capital is in the database
    for country, cities in country_to_cities.items():
        city_names = [city[0] for city in cities]
        if country in known_capitals:
            if known_capitals[country] in city_names:
                capitals[country] = known_capitals[country]
            else:
                # If known capital not in DB, use the first city
                capitals[country] = city_names[0]
        else:
            # If country not in known capitals, use first city
            capitals[country] = city_names[0]

    return capitals

def test_city_searches(cities):
    """Test searching for all cities."""
    results = []

    for city in cities:
        # Test exact city name
        result = get_city_by_name(city)
        if result:
            found_city, found_country, found_tz, found_emoji = result
            results.append({
                "test_type": "exact_city",
                "query": city,
                "result": result,
                "status": "PASS" if found_city == city else "FAIL",
                "expected": city,
                "actual": found_city,
                "issue": None if found_city == city else f"Expected '{city}' but got '{found_city}'"
            })
        else:
            results.append({
                "test_type": "exact_city",
                "query": city,
                "result": None,
                "status": "FAIL",
                "expected": city,
                "actual": None,
                "issue": f"City '{city}' not found"
            })

    return results

def test_country_searches(countries, capitals):
    """Test searching for all countries."""
    results = []

    for country in countries:
        # Test exact country name
        result = get_city_by_name(country)
        expected_capital = capitals.get(country)

        if result:
            found_city, found_country, found_tz, found_emoji = result
            is_correct_country = found_country == country
            is_correct_capital = found_city == expected_capital

            if is_correct_country and is_correct_capital:
                status = "PASS"
                issue = None
            elif is_correct_country and not is_correct_capital:
                status = "WARN"
                issue = f"Country '{country}' returned '{found_city}' instead of expected capital '{expected_capital}'"
            else:
                status = "FAIL"
                issue = f"Country '{country}' returned city from wrong country: '{found_city}' from '{found_country}'"

            results.append({
                "test_type": "exact_country",
                "query": country,
                "result": result,
                "status": status,
                "expected": f"{expected_capital} ({country})",
                "actual": f"{found_city} ({found_country})",
                "issue": issue
            })
        else:
            results.append({
                "test_type": "exact_country",
                "query": country,
                "result": None,
                "status": "FAIL",
                "expected": f"{expected_capital} ({country})",
                "actual": None,
                "issue": f"Country '{country}' not found"
            })

    return results

def test_fuzzy_searches(cities, countries):
    """Test fuzzy search with variations and typos."""
    results = []

    # Test common typos and variations
    test_cases = [
        ("toky", "Tokyo"),
        ("londn", "London"),
        ("pairs", "Paris"),
        ("newyork", "New York"),
        ("losangeles", "Los Angeles"),
        ("sanfrancisco", "San Francisco"),
        ("usa", "USA"),
        ("uk", "UK"),
        ("germany", "Germany"),
        ("france", "France"),
        ("japan", "Japan"),
        ("china", "China"),
        ("india", "India"),
        ("australia", "Australia"),
        ("brazil", "Brazil"),
        ("moscow", "Moscow"),
        ("bejing", "Beijing"),
        ("mumbai", "Mumbai"),
        ("delhi", "Delhi"),
        ("sidney", "Sydney"),
        ("melbourn", "Melbourne"),
    ]

    for typo, expected in test_cases:
        result = get_city_by_name(typo)
        if result:
            found_city, found_country, found_tz, found_emoji = result
            # Check if the found city or country matches expected
            if found_city == expected or found_country == expected:
                status = "PASS"
                issue = None
            else:
                status = "FAIL"
                issue = f"Fuzzy search for '{typo}' expected '{expected}' but got '{found_city}' ({found_country})"

            results.append({
                "test_type": "fuzzy_search",
                "query": typo,
                "result": result,
                "status": status,
                "expected": expected,
                "actual": f"{found_city} ({found_country})",
                "issue": issue
            })
        else:
            results.append({
                "test_type": "fuzzy_search",
                "query": typo,
                "result": None,
                "status": "FAIL",
                "expected": expected,
                "actual": None,
                "issue": f"Fuzzy search for '{typo}' returned no results"
            })

    return results

def test_case_sensitivity(cities, countries):
    """Test case insensitive searches."""
    results = []

    test_cases = [
        ("TOKYO", "Tokyo"),
        ("london", "London"),
        ("PaRiS", "Paris"),
        ("new york", "New York"),
        ("USA", "USA"),
        ("uk", "UK"),
        ("GerMaNy", "Germany"),
    ]

    for query, expected in test_cases:
        result = get_city_by_name(query)
        if result:
            found_city, found_country, found_tz, found_emoji = result
            if found_city == expected or found_country == expected:
                status = "PASS"
                issue = None
            else:
                status = "FAIL"
                issue = f"Case insensitive search for '{query}' expected '{expected}' but got '{found_city}' ({found_country})"

            results.append({
                "test_type": "case_insensitive",
                "query": query,
                "result": result,
                "status": status,
                "expected": expected,
                "actual": f"{found_city} ({found_country})",
                "issue": issue
            })
        else:
            results.append({
                "test_type": "case_insensitive",
                "query": query,
                "result": None,
                "status": "FAIL",
                "expected": expected,
                "actual": None,
                "issue": f"Case insensitive search for '{query}' returned no results"
            })

    return results

def test_suggestions(cities, countries):
    """Test suggestion functionality."""
    results = []

    test_cases = [
        ("tokio", ["Tokyo"]),
        ("pris", ["Paris"]),
        ("newyok", ["New York"]),
        ("londn", ["London"]),
        ("xyz123", []),  # Should return empty
    ]

    for query, expected_suggestions in test_cases:
        suggestions = suggest_cities(query)

        if not expected_suggestions:
            # Expecting no suggestions
            status = "PASS" if not suggestions else "FAIL"
            issue = None if not suggestions else f"Expected no suggestions for '{query}' but got {suggestions}"
        else:
            # Check if any expected suggestion is in the results
            found_expected = any(exp in suggestion for exp in expected_suggestions for suggestion in suggestions)
            status = "PASS" if found_expected else "FAIL"
            issue = None if found_expected else f"Expected suggestions containing {expected_suggestions} for '{query}' but got {suggestions}"

        results.append({
            "test_type": "suggestions",
            "query": query,
            "result": suggestions,
            "status": status,
            "expected": expected_suggestions,
            "actual": suggestions,
            "issue": issue
        })

    return results

def generate_markdown_report(all_results, cities, countries, capitals):
    """Generate a comprehensive markdown report."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Count results by status
    status_counts = defaultdict(int)
    for result in all_results:
        status_counts[result["status"]] += 1

    # Group results by test type
    results_by_type = defaultdict(list)
    for result in all_results:
        results_by_type[result["test_type"]].append(result)

    report = f"""# Global Time Utility (gtime) - Comprehensive Test Report

**Generated:** {timestamp}
**Database Size:** {len(CITY_DB)} cities across {len(countries)} countries

## Executive Summary

| Status | Count | Percentage |
|--------|-------|------------|
| PASS   | {status_counts['PASS']}    | {status_counts['PASS'] / len(all_results) * 100:.1f}% |
| WARN   | {status_counts['WARN']}    | {status_counts['WARN'] / len(all_results) * 100:.1f}% |
| FAIL   | {status_counts['FAIL']}    | {status_counts['FAIL'] / len(all_results) * 100:.1f}% |
| **Total** | **{len(all_results)}** | **100.0%** |

## Test Coverage

- **Cities Tested:** {len(cities)} unique cities
- **Countries Tested:** {len(countries)} unique countries
- **Fuzzy Search Cases:** {len(results_by_type['fuzzy_search'])} test cases
- **Case Sensitivity Tests:** {len(results_by_type['case_insensitive'])} test cases
- **Suggestion Tests:** {len(results_by_type['suggestions'])} test cases

## Critical Issues Found

"""

    # Add critical issues
    critical_issues = [result for result in all_results if result["status"] == "FAIL"]
    if critical_issues:
        report += f"**{len(critical_issues)} Critical Issues Found:**\n\n"
        for issue in critical_issues[:10]:  # Show first 10 critical issues
            report += f"- **{issue['test_type'].title()}**: Query `{issue['query']}` - {issue['issue']}\n"
        if len(critical_issues) > 10:
            report += f"\n... and {len(critical_issues) - 10} more issues (see detailed results below)\n"
    else:
        report += "✅ No critical issues found!\n"

    report += "\n## Warning Issues\n\n"
    warning_issues = [result for result in all_results if result["status"] == "WARN"]
    if warning_issues:
        report += f"**{len(warning_issues)} Warning Issues Found:**\n\n"
        for issue in warning_issues[:10]:
            report += f"- **{issue['test_type'].title()}**: Query `{issue['query']}` - {issue['issue']}\n"
        if len(warning_issues) > 10:
            report += f"\n... and {len(warning_issues) - 10} more warnings (see detailed results below)\n"
    else:
        report += "✅ No warning issues found!\n"

    # Add detailed results for each test type
    for test_type, results in results_by_type.items():
        report += f"\n## {test_type.replace('_', ' ').title()} Results\n\n"

        pass_count = sum(1 for r in results if r["status"] == "PASS")
        warn_count = sum(1 for r in results if r["status"] == "WARN")
        fail_count = sum(1 for r in results if r["status"] == "FAIL")

        report += f"**Summary:** {pass_count} passed, {warn_count} warnings, {fail_count} failed\n\n"

        # Show failures first
        failures = [r for r in results if r["status"] == "FAIL"]
        if failures:
            report += "### Failures\n\n"
            report += "| Query | Expected | Actual | Issue |\n"
            report += "|-------|----------|--------|-------|\n"
            for result in failures:
                query = result["query"]
                expected = result["expected"] or "N/A"
                actual = result["actual"] or "None"
                issue = result["issue"] or "No issue"
                report += f"| `{query}` | {expected} | {actual} | {issue} |\n"
            report += "\n"

        # Show warnings
        warnings = [r for r in results if r["status"] == "WARN"]
        if warnings:
            report += "### Warnings\n\n"
            report += "| Query | Expected | Actual | Issue |\n"
            report += "|-------|----------|--------|-------|\n"
            for result in warnings:
                query = result["query"]
                expected = result["expected"] or "N/A"
                actual = result["actual"] or "None"
                issue = result["issue"] or "No issue"
                report += f"| `{query}` | {expected} | {actual} | {issue} |\n"
            report += "\n"

        # Show sample passes (first 5)
        passes = [r for r in results if r["status"] == "PASS"]
        if passes:
            report += "### Sample Successful Tests\n\n"
            report += "| Query | Result | Status |\n"
            report += "|-------|--------|--------|\n"
            for result in passes[:5]:
                query = result["query"]
                actual = result["actual"] or "None"
                report += f"| `{query}` | {actual} | ✅ PASS |\n"
            if len(passes) > 5:
                report += f"| ... | ... | ... and {len(passes) - 5} more |\n"
            report += "\n"

    # Add country-capital mapping
    report += "\n## Country-Capital Mapping\n\n"
    report += "| Country | Expected Capital | Status |\n"
    report += "|---------|------------------|--------|\n"

    for country in sorted(countries):
        capital = capitals.get(country, "Unknown")
        # Check if this capital is actually in the database
        capital_result = get_city_by_name(country)
        if capital_result and capital_result[0] == capital:
            status = "✅ Correct"
        elif capital_result:
            status = f"⚠️ Returns {capital_result[0]}"
        else:
            status = "❌ Not found"

        report += f"| {country} | {capital} | {status} |\n"

    report += f"""

## Database Statistics

### Cities by Country
| Country | City Count |
|---------|------------|
"""

    # Count cities per country
    country_counts = defaultdict(int)
    for city, country, tz, emoji in CITY_DB:
        country_counts[country] += 1

    for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"| {country} | {count} |\n"

    report += f"""

### Timezones Used
| Timezone | City Count |
|----------|------------|
"""

    # Count timezones
    tz_counts = defaultdict(int)
    for city, country, tz, emoji in CITY_DB:
        tz_counts[tz] += 1

    for tz, count in sorted(tz_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"| {tz} | {count} |\n"

    report += f"""

## Recommendations

Based on the test results, here are the recommended actions:

### High Priority (Critical Issues)
"""

    if critical_issues:
        report += f"1. **Fix {len(critical_issues)} critical search failures** - These prevent basic functionality\n"
        report += "2. **Implement better fuzzy matching** - Several typos are not handled correctly\n"
        report += "3. **Review country-to-capital mappings** - Some countries return unexpected cities\n"
    else:
        report += "✅ No critical issues found - system is functioning well!\n"

    report += """

### Medium Priority (Warnings)
"""

    if warning_issues:
        report += f"1. **Review {len(warning_issues)} capital city mappings** - Some countries return non-capital cities\n"
        report += "2. **Consider adding more city aliases** - Some common name variations are missed\n"
    else:
        report += "✅ No warning issues found!\n"

    report += """

### Low Priority (Improvements)
1. **Add more comprehensive test cases** - Expand fuzzy search testing
2. **Implement better suggestion algorithms** - Improve typo tolerance
3. **Add support for alternative city names** - Handle common aliases and local names

---

*This report was generated automatically by the gtime test suite.*
"""

    return report

def main():
    """Main test execution function."""
    print("🧪 Starting comprehensive Global Time Utility tests...")
    print(f"📊 Database contains {len(CITY_DB)} cities")

    # Analyze database structure
    print("📋 Analyzing database structure...")
    cities, countries, country_to_cities = analyze_city_db()
    print(f"✅ Found {len(cities)} unique cities in {len(countries)} countries")

    # Identify capitals
    print("🏛️  Identifying capital cities...")
    capitals = identify_capitals(country_to_cities)
    print(f"✅ Mapped {len(capitals)} capitals")

    # Run all tests
    all_results = []

    print("🔍 Testing exact city searches...")
    city_results = test_city_searches(cities)
    all_results.extend(city_results)
    print(f"✅ Tested {len(city_results)} city searches")

    print("🌍 Testing country searches...")
    country_results = test_country_searches(countries, capitals)
    all_results.extend(country_results)
    print(f"✅ Tested {len(country_results)} country searches")

    print("🔤 Testing fuzzy searches...")
    fuzzy_results = test_fuzzy_searches(cities, countries)
    all_results.extend(fuzzy_results)
    print(f"✅ Tested {len(fuzzy_results)} fuzzy searches")

    print("🔠 Testing case sensitivity...")
    case_results = test_case_sensitivity(cities, countries)
    all_results.extend(case_results)
    print(f"✅ Tested {len(case_results)} case sensitivity tests")

    print("💡 Testing suggestion system...")
    suggestion_results = test_suggestions(cities, countries)
    all_results.extend(suggestion_results)
    print(f"✅ Tested {len(suggestion_results)} suggestion tests")

    # Generate report
    print("📝 Generating comprehensive report...")
    report = generate_markdown_report(all_results, cities, countries, capitals)

    # Save report
    report_file = "gtime_comprehensive_test_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Report saved to {report_file}")

    # Print summary
    status_counts = defaultdict(int)
    for result in all_results:
        status_counts[result["status"]] += 1

    print(f"\n📊 Test Summary:")
    print(f"   ✅ PASS: {status_counts['PASS']}")
    print(f"   ⚠️  WARN: {status_counts['WARN']}")
    print(f"   ❌ FAIL: {status_counts['FAIL']}")
    print(f"   📋 TOTAL: {len(all_results)}")

    if status_counts['FAIL'] > 0:
        print(f"\n🚨 {status_counts['FAIL']} critical issues found! Please review the report.")
        return 1
    elif status_counts['WARN'] > 0:
        print(f"\n⚠️  {status_counts['WARN']} warnings found. Review recommended.")
        return 0
    else:
        print(f"\n🎉 All tests passed! System is working correctly.")
        return 0

if __name__ == "__main__":
    sys.exit(main())