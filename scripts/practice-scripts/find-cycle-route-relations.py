"""
Example script for retrieving Adelaide bicycle network graph and 
adding cycle route edge attributes based on OSM route:bicycle relations.

This version works with overpass 0.8.2 (the latest on PyPI).
For a more modern alternative, see find-cycle-route-relations-overpy.py
"""

import osmnx as ox
import pandas as pd
import numpy as np

# Handle overpass imports - version 0.8.2 uses API class
try:
    from overpass import API
    OVERPASS_AVAILABLE = True
except ImportError:
    OVERPASS_AVAILABLE = False
    # Mock for documentation purposes
    class API:
        def __init__(self, *args, **kwargs):
            raise ImportError("Overpass API package not available. Install with: pip install overpass")


def get_adelaide_boundary():
    """
    Get the Adelaide boundary using the R11381689 OSM relation ID.
    
    Returns:
        Shapely polygon of Adelaide boundary
    """
    gdf_boundary = ox.geocode_to_gdf("R11381689", by_osmid=True)
    polygon = gdf_boundary.geometry.iloc[0]
    return polygon


def get_cycle_route_way_ids(boundary_polygon):
    """
    Get OSM way IDs that are part of bicycle route relations.
    
    Args:
        boundary_polygon: Shapely polygon defining the search area
        
    Returns:
        Set of OSM way IDs that belong to bicycle routes
    """
    if not OVERPASS_AVAILABLE:
        print("Warning: Overpass package not available. Returning empty set.")
        return set()
        
    try:
        # Initialize Overpass API with longer timeout
        api = API(timeout=120)
        
        # Extract bounding box from polygon
        minx, miny, maxx, maxy = boundary_polygon.bounds
        
        # Overpass query to find route:bicycle relations and their ways
        # Note: overpass 0.8.2 expects (south, west, north, east) = (miny, minx, maxy, maxx)
        query = f"""
        [out:json][timeout:120];
        (
          relation["route"="bicycle"]({miny},{minx},{maxy},{maxx});
        );
        way(r);
        out ids;
        """
        
        print(f"Querying Overpass API with bbox: ({miny:.4f}, {minx:.4f}, {maxy:.4f}, {maxx:.4f})")
        result = api.get(query, responseformat='json')
        
        way_ids = {str(element['id']) for element in result.get('elements', []) 
                  if element.get('type') == 'way'}
        print(f"Found {len(way_ids)} ways in bicycle route relations")
        return way_ids
        
    except Exception as e:
        print(f"Warning: Error querying Overpass API: {type(e).__name__}: {e}")
        print("Returning empty set - no cycle route attributes will be added")
        return set()


def add_cycle_route_attribute_to_graph(G, cycle_way_ids):
    """
    Add IS_CYCLE_ROUTE edge attribute to graph based on OSM way IDs.
    
    Args:
        G: NetworkX graph from OSMnx
        cycle_way_ids: Set of OSM way IDs that are part of bicycle routes
        
    Returns:
        Graph with IS_CYCLE_ROUTE edge attribute
    """
    # Convert graph to edges GeoDataFrame for easy manipulation
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    
    # Function to check if edge is part of a cycle route
    def is_cycle_route(osmid):
        # Handle pandas NA values and numpy arrays properly
        try:
            # Handle scalar NA values
            if pd.isna(osmid):
                return False
            # Handle numpy arrays and pandas Series
            elif hasattr(osmid, '__len__') and not isinstance(osmid, (str, bytes)):
                if len(osmid) == 0:
                    return False
                return any(str(osm_id) in cycle_way_ids for osm_id in osmid)
            # Handle scalar values (strings, numbers, etc.)
            else:
                return str(osmid) in cycle_way_ids
        except (TypeError, ValueError):
            # Fallback for any unexpected cases
            return False
    
    # Apply the function to create the IS_CYCLE_ROUTE attribute
    edges['IS_CYCLE_ROUTE'] = edges['osmid'].apply(is_cycle_route).astype(int)
    
    # Convert back to graph
    G_with_attr = ox.graph_from_gdfs(nodes, edges)
    
    return G_with_attr


def get_adelaide_bike_network_with_cycle_routes():
    """
    Main function to get Adelaide bike network with cycle route attributes.
    
    Returns:
        NetworkX graph with IS_CYCLE_ROUTE edge attribute (1 if part of cycle route, 0 otherwise)
        
    Note:
        This function requires:
        - osmnx package for street network retrieval
        - overpass package for querying OSM relations  
        - pandas for data manipulation
        
        If overpass API is unavailable, the function will still return the bike network
        but with all IS_CYCLE_ROUTE attributes set to 0.
    """
    print("Getting Adelaide boundary...")
    adelaide_polygon = get_adelaide_boundary()
    
    print("Fetching bicycle network graph...")
    # Get the base bike network graph with customized settings
    ox.settings.useful_tags_way += [
        "cycleway",
        "cycleway:left",
        "cycleway:right", 
        "cycleway:both",
        "bicycle",
    ]
    
    G = ox.graph_from_polygon(adelaide_polygon, network_type="bike")
    
    print("Fetching cycle route relations from OSM...")
    cycle_way_ids = get_cycle_route_way_ids(adelaide_polygon)
    print(f"Found {len(cycle_way_ids)} ways that are part of bicycle routes")
    
    print("Adding cycle route attributes to graph edges...")
    G_with_routes = add_cycle_route_attribute_to_graph(G, cycle_way_ids)
    
    # Print summary statistics
    total_edges = len(G_with_routes.edges())
    cycle_edges = sum(1 for u, v, k, data in G_with_routes.edges(keys=True, data=True) 
                      if data.get('IS_CYCLE_ROUTE', 0) == 1)
    
    print(f"\nSummary:")
    print(f"- Total edges: {total_edges}")
    print(f"- Cycle route edges: {cycle_edges} ({cycle_edges/total_edges*100:.1f}%)")
    
    return G_with_routes


def example_usage():
    """
    Example showing how to use the function in your regression model workflow.
    """
    # Get the graph with cycle route attributes
    G = get_adelaide_bike_network_with_cycle_routes()
    
    # Example: Accessing the IS_CYCLE_ROUTE attribute for regression
    print("\nExample edge data with IS_CYCLE_ROUTE attribute:")
    for u, v, k, data in list(G.edges(keys=True, data=True))[:5]:  # Show first 5 edges
        is_cycle_route = data.get('IS_CYCLE_ROUTE', 0)
        print(f"  Edge {u}-{v} (key {k}): IS_CYCLE_ROUTE = {is_cycle_route}")
    
    # Example: Convert to GeoDataFrame for easier analysis in regression
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    print(f"\nEdges GeoDataFrame shape: {edges.shape}")
    print(f"IS_CYCLE_ROUTE value counts:\n{edges['IS_CYCLE_ROUTE'].value_counts()}")
    
    return G


if __name__ == "__main__":
    # Run the example when script is executed
    # Note: This requires osmnx and overpass to be installed in your environment
    # If you encounter import errors, please install:
    # pip install osmnx overpass pandas
    try:
        example_usage()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure you have the required packages installed:")
        print("  pip install osmnx overpass pandas")
        print("\nThe core logic is implemented and will work when packages are available.")