"""
Reusable module for fetching OSM bicycle route relations and adding them as edge attributes.
Works with overpy and uses reliable Overpass endpoints with retry logic.
"""

import time
import overpy
from typing import Set


# Reliable Overpass endpoint (kumi.systems works well)
OVERPASS_ENDPOINT = "https://overpass.kumi.systems/api/interpreter"


def get_cycle_route_way_ids(bbox: tuple, timeout: int = 180, max_retries: int = 2) -> Set[str]:
    """
    Get OSM way IDs that are part of bicycle route relations within a bounding box.
    Retries on server load errors (503, 429, etc.).
    
    Args:
        bbox: Tuple of (minx, miny, maxx, maxy) - note: minx=west, miny=south
        timeout: Query timeout in seconds
        max_retries: Number of retry attempts (default 2 = 1 retry after initial)
        
    Returns:
        Set of OSM way IDs (as strings) that belong to bicycle routes
    """
    minx, miny, maxx, maxy = bbox
    
    # Overpass QL query: (south, west, north, east) = (miny, minx, maxy, maxx)
    query = f"""
    [out:json][timeout:{timeout}];
    (
      relation["route"="bicycle"]({miny},{minx},{maxy},{maxx});
    );
    way(r);
    out ids;
    """
    
    api = overpy.Overpass(url=OVERPASS_ENDPOINT)
    
    for attempt in range(max_retries):
        try:
            result = api.query(query)
            return {str(way.id) for way in result.ways}
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s...
                print(f"Error: {type(e).__name__}: {e} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"Failed after {max_retries} attempts: {type(e).__name__}: {e}")
                raise
    
    return set()


def add_cycle_route_attribute(edges, cycle_way_ids: Set[str]):
    """
    Add IS_CYCLE_ROUTE column to edges GeoDataFrame.
    
    Args:
        edges: GeoDataFrame with 'osmid' column (from ox.graph_to_gdfs)
        cycle_way_ids: Set of way IDs from get_cycle_route_way_ids()
        
    Returns:
        Modified edges GeoDataFrame with IS_CYCLE_ROUTE column (0/1)
    """
    import pandas as pd
    
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
    
    edges = edges.copy()
    edges['IS_CYCLE_ROUTE'] = edges['osmid'].apply(is_cycle_route).astype(int)
    return edges


# Convenience function for common workflow
def enrich_graph_with_cycle_routes(G, bbox: tuple = None):
    """
    Add IS_CYCLE_ROUTE edge attribute to an OSMnx graph.
    
    Args:
        G: NetworkX graph from OSMnx
        bbox: Optional (minx, miny, maxx, maxy). If None, uses graph's bounding box.
        
    Returns:
        Graph with IS_CYCLE_ROUTE edge attribute
    """
    import osmnx as ox
    
    if bbox is None:
        nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
        bbox = edges.total_bounds  # (minx, miny, maxx, maxy)
    
    cycle_way_ids = get_cycle_route_way_ids(bbox)
    print(f"Found {len(cycle_way_ids)} ways in bicycle routes")
    
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    edges = add_cycle_route_attribute(edges, cycle_way_ids)
    
    return ox.graph_from_gdfs(nodes, edges)