#!/usr/bin/env python3
"""
Test script to verify Overpass API connectivity and query functionality.
Tests basic queries against the Overpass API to diagnose timeout issues.
"""

import sys
import os

# Add local venv to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.venv', 'lib', 'python3.13', 'site-packages'))

try:
    from overpass import API
    print(f"Overpass version: {API.__module__}")
except ImportError as e:
    print(f"Failed to import overpass: {e}")
    sys.exit(1)

# Test 1: Simple API initialization
print("\n=== Test 1: API Initialization ===")
try:
    api = API()
    print("✓ API initialized successfully")
    print(f"  Endpoint: {api._endpoint}")
    print(f"  Timeout: {api._timeout}")
except Exception as e:
    print(f"✗ API initialization failed: {e}")
    sys.exit(1)

# Test 2: Very simple query (just get a single node)
print("\n=== Test 2: Simple Node Query ===")
try:
    query = """
    [out:json][timeout:10];
    node(50.745, 7.17, 50.75, 7.18);
    out count;
    """
    result = api.get(query, responseformat='json')
    print(f"✓ Simple query succeeded")
    print(f"  Elements returned: {len(result.get('elements', []))}")
except Exception as e:
    print(f"✗ Simple query failed: {type(e).__name__}: {e}")

# Test 3: Bicycle route query (smaller bbox for testing)
print("\n=== Test 3: Bicycle Route Query (Small Area) ===")
try:
    # Small test area in Adelaide
    query = """
    [out:json][timeout:30];
    (
      relation["route"="bicycle"](-34.93, 138.59, -34.92, 138.61);
    );
    way(r);
    out ids;
    """
    result = api.get(query, responseformat='json')
    way_ids = {str(element['id']) for element in result.get('elements', []) if element['type'] == 'way'}
    print(f"✓ Bicycle route query succeeded")
    print(f"  Ways found: {len(way_ids)}")
except Exception as e:
    print(f"✗ Bicycle route query failed: {type(e).__name__}: {e}")

# Test 4: Same query with larger timeout
print("\n=== Test 4: Bicycle Route Query (Larger Area, Longer Timeout) ===")
try:
    # Larger area covering more of Adelaide
    query = """
    [out:json][timeout:60];
    (
      relation["route"="bicycle"](-35.0, 138.5, -34.8, 138.7);
    );
    way(r);
    out ids;
    """
    result = api.get(query, responseformat='json')
    way_ids = {str(element['id']) for element in result.get('elements', []) if element['type'] == 'way'}
    print(f"✓ Large area query succeeded")
    print(f"  Ways found: {len(way_ids)}")
except Exception as e:
    print(f"✗ Large area query failed: {type(e).__name__}: {e}")

# Test 5: Test with the search method (alternative API)
print("\n=== Test 5: Using API.search() method ===")
try:
    query = """
    [out:json][timeout:30];
    relation["route"="bicycle"](-34.93, 138.59, -34.92, 138.61);
    out ids;
    """
    result = api.search(query)
    print(f"✓ Search method succeeded")
    print(f"  Result type: {type(result)}")
except Exception as e:
    print(f"✗ Search method failed: {type(e).__name__}: {e}")

print("\n=== Summary ===")
print("If all tests passed, Overpass is working correctly.")
print("If queries timeout, consider:")
print("  - Using a smaller bounding box")
print("  - Increasing timeout in query")
print("  - Using a different Overpass endpoint (api._endpoint)")
print("  - Querying during off-peak hours")