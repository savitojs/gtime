#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
City and country search helpers for Global Time Utility (gtime).
"""

from functools import lru_cache
from typing import List, Optional, Tuple

from .data import CITY_DB, COUNTRY_CAPITALS


def _get_city_names():
    names = [f"{city} ({country})" for city, country, _, _ in CITY_DB]
    name_to_idx = {name: i for i, name in enumerate(names)}
    return names, name_to_idx


@lru_cache(maxsize=256)
def fuzzy_search_city(query: str) -> Optional[Tuple[str, str, str, str]]:
    from thefuzz import process
    names, name_to_idx = _get_city_names()

    # First priority: exact match (case insensitive)
    query_lower = query.lower()
    for name in names:
        city_name = name.split(" (")[0].lower()
        if city_name == query_lower:
            idx = name_to_idx[name]
            return CITY_DB[idx]

    # Second priority: starts with (case insensitive)
    for name in names:
        city_name = name.split(" (")[0].lower()
        if city_name.startswith(query_lower):
            idx = name_to_idx[name]
            return CITY_DB[idx]

    # Third priority: exact country match (case insensitive)
    # If searching for a country name, return the capital city
    for city, country, tz, emoji in CITY_DB:
        if country.lower() == query_lower:
            # Check if we have a specific capital for this country
            capital = COUNTRY_CAPITALS.get(country)
            if capital:
                # Find the capital city in the database
                for cap_city, cap_country, cap_tz, cap_emoji in CITY_DB:
                    if cap_city == capital and cap_country == country:
                        return (cap_city, cap_country, cap_tz, cap_emoji)
            # If no capital mapping or capital not found, return the first city
            return (city, country, tz, emoji)

    # Fourth priority: country starts with or contains query (case insensitive)
    for city, country, tz, emoji in CITY_DB:
        if country.lower().startswith(query_lower) or query_lower in country.lower():
            # Check if we have a specific capital for this country
            capital = COUNTRY_CAPITALS.get(country)
            if capital:
                # Find the capital city in the database
                for cap_city, cap_country, cap_tz, cap_emoji in CITY_DB:
                    if cap_city == capital and cap_country == country:
                        return (cap_city, cap_country, cap_tz, cap_emoji)
            # If no capital mapping or capital not found, return the first city
            return (city, country, tz, emoji)

    # Fifth priority: substring match (case insensitive) - only for queries with 5+ characters
    # This avoids false matches like "usa" matching "Busan"
    if len(query) >= 5:
        for name in names:
            city_name = name.split(" (")[0].lower()
            if query_lower in city_name:
                idx = name_to_idx[name]
                return CITY_DB[idx]

    # Sixth priority: fuzzy match on city names only (not including country)
    city_names_only = [name.split(" (")[0] for name in names]
    match, score = process.extractOne(query, city_names_only)
    if score > 60:
        for name in names:
            if name.split(" (")[0] == match:
                idx = name_to_idx[name]
                return CITY_DB[idx]

    return None


@lru_cache(maxsize=256)
def get_city_by_name(city_name: str) -> Optional[Tuple[str, str, str, str]]:
    for city, country, tz, emoji in CITY_DB:
        if city.lower() == city_name.lower():
            return (city, country, tz, emoji)

    return fuzzy_search_city(city_name)


def suggest_cities(city_name: str) -> List[str]:
    from thefuzz import process
    names, _ = _get_city_names()

    # First, check if the query exactly matches a country name
    query_lower = city_name.lower()
    country_matches = []
    for city, country, tz, emoji in CITY_DB:
        if country.lower() == query_lower:
            country_matches.append(f"{city} ({country})")

    # If we found exact country matches, return them
    if country_matches:
        return country_matches[:3]

    city_names_only = [name.split(" (")[0] for name in names]
    matches = process.extract(city_name, city_names_only, limit=3)

    # Convert back to full names for suggestions
    suggestions = []
    for match, score in matches:
        if score > 40:
            for name in names:
                if name.split(" (")[0] == match:
                    suggestions.append(name)
                    break

    # If we don't have good city suggestions, try partial country matches
    if not suggestions or (suggestions and max(score for _, score in matches) < 60):
        # Check if query partially matches any country name
        partial_country_matches = []
        for city, country, tz, emoji in CITY_DB:
            if (country.lower().startswith(query_lower) or
                query_lower in country.lower()):
                partial_country_matches.append(f"{city} ({country})")

        # Add up to 3 cities from matching countries
        if partial_country_matches:
            suggestions.extend(partial_country_matches[:3])

    return suggestions
