#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance profiling for city lookup functions in Global Time Utility (gtime) for large city datasets
"""

import timeit
from gtime.core import get_city_by_name, fuzzy_search_city
from gtime.data import CITY_DB

# Generate a large fake city DB for stress test
large_db = CITY_DB + [
    (f"FakeCity{i}", f"Country{i}", f"Continent/FakeZone{i}", "🏙️") for i in range(10000)
]

def profile_lookup():
    # Patch the CITY_DB in the imported module
    import gtime.data
    gtime.data.CITY_DB = large_db

    print("Testing get_city_by_name (exact match)...")
    t = timeit.timeit(lambda: get_city_by_name("FakeCity9999"), number=100)
    print(f"Exact match (100x): {t:.4f} seconds")

    print("Testing get_city_by_name (fuzzy match)...")
    t = timeit.timeit(lambda: get_city_by_name("FakeCty9999"), number=100)
    print(f"Fuzzy match (100x): {t:.4f} seconds")

    print("Testing fuzzy_search_city (fuzzy)...")
    t = timeit.timeit(lambda: fuzzy_search_city("FakeCty9999"), number=100)
    print(f"fuzzy_search_city (100x): {t:.4f} seconds")

if __name__ == "__main__":
    profile_lookup()
