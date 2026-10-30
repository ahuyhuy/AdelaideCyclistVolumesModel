"""
Example script for retrieving Adelaide bicycle network graph and 
adding cycle route edge attributes based on OSM route:bicycle relations.

This version uses OVERPY (more modern, actively maintained) with:
- Alternative Overpass endpoints for better reliability
- Configurable timeouts and retries
- Better error handling
"""

import osmnx as ox
import pandas as pd
import numpy as np
import time
import sys
import os

# Add local venv to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.venv', 'lib', 'python3.13', 'site-packages'))

try:
    import overpy
    OVERPY_AVAILABLE = True
except ImportError:
    OVERPY_AVAILABLE = False


# Alternative Overpass API endpoints (public instances)
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",      # Main (Germany)
    "https://overpass.kumi.systems/api/interpreter", # Switzerland
    "https://overpass.openstreetmap.ru/api/interpreter", # Russia
    "https://api.openstreetmap.fr/overpass/api/interpreter", # France
]


def get_adelaide_boundary():
    """Get the Adelaide boundary using the R11381689 OSM relation ID."""
    gdf_boundary = ox.geocode_to_gdf("R11381689", by_osmid=True)
    polygon = gdf_boundary.geometry.iloc[0]
    return polygon


def query_with_retry(query, max_retries=3):
    """
    Query Overpass with multiple endpoints and retries.
    
    Args:
        query: Overpass QL query string
        max_retries: Number of retry attempts per endpoint
        timeout: Query timeout in seconds
        
    Returns:
        overpy.Result or None if all attempts fail
    """
    if not OVERPY_AVAILABLE:
        print("Error: overpy not installed. Run: pip install overpy")
        return None
    
    for endpoint in OVERPASS_ENDPOINTS:
        print(f"Trying endpoint: {endpoint}")
        api = overpy.Overpass(url=endpoint)
        
        for attempt in range(max_retries):
            try:
                print(f"  Attempt {attempt + 1}/{max_retries}...")
                result = api.query(query)
                print(f"  ✓ Success! Got {len(result.ways)} ways, {len(result.relations)} relations")
                return result
            except Exception as e:
                print(f"  Error: {type(e).__name__}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        
        print(f"  Endpoint failed, trying next...")
    
    print("All endpoints and retries exhausted")
    return None


def get_cycle_route_way_ids(boundary_polygon):
    """
    Get OSM way IDs that are part of bicycle route relations using overpy.
    
    Args:
        boundary_polygon: Shapely polygon defining the search area
        
    Returns:
        Set of OSM way IDs that belong to bicycle routes
    """
    if not OVERPY_AVAILABLE:
        print("Warning: overpy package not available. Returning empty set.")
        return set()
        
    try:
        # Extract bounding box from polygon
        minx, miny, maxx, maxy = boundary_polygon.bounds
        
        # Overpass query - using bbox format (south, west, north, east)
        query = f"""
        [out:json];
        (
          relation["route"="bicycle"]({miny},{minx},{maxy},{maxx});
        );
        way(r);
        out ids geom;
        """
        
        print(f"Querying Overpass for bicycle routes in bbox: ({miny:.4f}, {minx:.4f}, {maxy:.4f}, {maxx:.4f})")
        result = query_with_retry(query, max_retries=2)
        
        if result is None:
            return set()
        
        # Extract way IDs from the result
        way_ids = {str(way.id) for way in result.ways}
        print(f"Found {len(way_ids)} ways in bicycle route relations")
        return way_ids
        
    except Exception as e:
        print(f"Warning: Error querying Overpass API: {type(e).__name__}: {e}")
        print("Returning empty set - no cycle route attributes will be added")
        return set()


def add_cycle_route_attribute_to_graph(G, cycle_way_ids):
    """
    Add IS_CYCLE_ROUTE edge attribute to graph based on OSM way IDs.
    """
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    
    def is_cycle_route(osmid):
        try:
            if pd.isna(osmid):
                return False
            elif hasattr(osmid, '__len__') and not isinstance(osmid, (str, bytes)):
                if len(osmid) == 0:
                    return False
                return any(str(osm_id) in cycle_way_ids for osm_id in osmid)
            else:
                return str(osmid) in cycle_way_ids
        except (TypeError, ValueError):
            return False
    
    edges['IS_CYCLE_ROUTE'] = edges['osmid'].apply(is_cycle_route).astype(int)
    G_with_attr = ox.graph_from_gdfs(nodes, edges)
    return G_with_attr


def get_adelaide_bike_network_with_cycle_routes():
    """
    Main function to get Adelaide bike network with cycle route attributes.
    """
    print("Getting Adelaide boundary...")
    adelaide_polygon = get_adelaide_boundary()
    
    print("Fetching bicycle network graph...")
    ox.settings.useful_tags_way += [
        "cycleway", "cycleway:left", "cycleway:right", 
        "cycleway:both", "bicycle",
    ]
    
    G = ox.graph_from_polygon(adelaide_polygon, network_type="bike")
    
    print("Fetching cycle route relations from OSM (via overpy)...")
    cycle_way_ids = get_cycle_route_way_ids(adelaide_polygon)
    print(f"Found {len(cycle_way_ids)} ways that are part of bicycle routes")
    
    print("Adding cycle route attributes to graph edges...")
    G_with_routes = add_cycle_route_attribute_to_graph(G, cycle_way_ids)
    
    total_edges = len(G_with_routes.edges())
    cycle_edges = sum(1 for u, v, k, data in G_with_routes.edges(keys=True, data=True) 
                      if data.get('IS_CYCLE_ROUTE', 0) == 1)
    
    print(f"\nSummary:")
    print(f"- Total edges: {total_edges}")
    print(f"- Cycle route edges: {cycle_edges} ({cycle_edges/total_edges*100:.1f}%)")
    
    return G_with_routes


def example_usage():
    G = get_adelaide_bike_network_with_cycle_routes()
    
    print("\nExample edge data with IS_CYCLE_ROUTE attribute:")
    for u, v, k, data in list(G.edges(keys=True, data=True))[:5]:
        is_cycle_route = data.get('IS_CYCLE_ROUTE', 0)
        print(f"  Edge {u}-{v} (key {k}): IS_CYCLE_ROUTE = {is_cycle_route}")
    
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    print(f"\nEdges GeoDataFrame shape: {edges.shape}")
    print(f"IS_CYCLE_ROUTE value counts:\n{edges['IS_CYCLE_ROUTE'].value_counts()}")
    
    return G


if __name__ == "__main__":
    try:
        example_usage()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure you have the required packages installed:")
        print("  pip install osmnx overpy pandas")