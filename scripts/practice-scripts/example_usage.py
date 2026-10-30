"""
Example usage of the cycle route relations functionality.
This demonstrates how to integrate the IS_CYCLE_ROUTE attribute into your regression workflow.
"""

import osmnx as ox
import pandas as pd


def demonstrate_workflow():
    """
    Demonstrate the complete workflow for adding cycle route attributes
    to your Adelaide street network graph for regression analysis.
    """
    
    print("=== Adelaide Cycling Route Regression Workflow ===\n")
    
    # Step 1: Get Adelaide boundary (as you specified in your query)
    print("1. Getting Adelaide boundary using OSM relation R11381689...")
    gdf_boundary = ox.geocode_to_gdf("R11381689", by_osmid=True)
    adelaide_polygon = gdf_boundary.geometry.iloc[0]
    print(f"   Boundary obtained: {adelaide_polygon}\n")
    
    # Step 2: Get the bicycle network graph (your existing code)
    print("2. Retrieving bicycle network graph...")
    # Apply your custom OSMnx settings
    ox.settings.useful_tags_way += [
        "cycleway",
        "cycleway:left",
        "cycleway:right",
        "cycleway:both",
        "bicycle",
    ]
    
    # This is your existing code block:
    G = ox.graph_from_polygon(adelaide_polygon, network_type="bike")
    print(f"   Graph retrieved: {len(G.nodes())} nodes, {len(G.edges())} edges\n")
    
    # Step 3: Add cycle route attributes (the new functionality)
    print("3. Adding IS_CYCLE_ROUTE edge attributes...")
    
    # In practice, this would query Overpass API for route:bicycle relations
    # For demonstration, we'll simulate having some cycle route ways
    # In the real implementation, see infrastructure/find-cycle-route-relations.py
    
    # Convert to GeoDataFrame for attribute manipulation
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    
    # Simulate finding some cycle route ways (in practice, this comes from Overpass)
    # For demonstration, let's say we found these OSM way IDs are part of bicycle routes
    example_cycle_way_ids = {'123456789', '987654321', '456789123'}  # Example IDs
    
    # Function to check if an edge is part of a cycle route
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
                return any(str(osm_id) in example_cycle_way_ids for osm_id in osmid)
            # Handle scalar values (strings, numbers, etc.)
            else:
                return str(osmid) in example_cycle_way_ids
        except (TypeError, ValueError):
            # Fallback for any unexpected cases
            return False
    
    # Add the IS_CYCLE_ROUTE attribute
    edges['IS_CYCLE_ROUTE'] = edges['osmid'].apply(is_cycle_route).astype(int)
    
    # Convert back to graph
    G_with_attributes = ox.graph_from_gdfs(nodes, edges)
    
    # Step 4: Summary statistics
    total_edges = len(edges)
    cycle_route_edges = edges['IS_CYCLE_ROUTE'].sum()
    
    print(f"   Found {len(example_cycle_way_ids)} example cycle route ways")
    print(f"   Total edges in graph: {total_edges}")
    print(f"   Edges marked as cycle routes: {cycle_route_edges} "
          f"({cycle_route_edges/total_edges*100:.2f}%)")
    print()
    
    # Step 5: Show how to use in regression analysis
    print("4. Using IS_CYCLE_ROUTE in regression analysis:")
    print("   The edges GeoDataFrame now contains:")
    print(f"   - Shape: {edges.shape}")
    print(f"   - Columns: {list(edges.columns)}")
    print("   - IS_CYCLE_ROUTE column: dummy variable (1=cycle route, 0=not cycle route)")
    print()
    
    # Show first few rows as example
    print("   Example edge data:")
    display_cols = ['osmid', 'highway', 'IS_CYCLE_ROUTE']
    if all(col in edges.columns for col in display_cols):
        print(edges[display_cols].head(10).to_string(index=False))
    else:
        # Fallback if columns don't exist exactly
        sample_cols = [col for col in edges.columns[:4] if not col.startswith('geometry')]
        if 'IS_CYCLE_ROUTE' in edges.columns:
            sample_cols.append('IS_CYCLE_ROUTE')
        print(edges[sample_cols].head(10).to_string(index=False))
    
    print("\n=== Ready for Regression Analysis ===")
    print("You can now use edges['IS_CYCLE_ROUTE'] as a dummy variable in your regression model")
    print("to capture whether each street segment is part of a designated cycling route.")
    
    return G_with_attributes, edges


def show_actual_implementation():
    """
    Show what the actual implementation looks like.
    """
    print("\n=== Actual Implementation ===")
    print("See infrastructure/find-cycle-route-relations.py for the complete implementation")
    print("that includes:")
    print("  • Proper Overpass API querying for route:bicycle relations")
    print("  • Robust handling of OSM IDs (single values, lists, arrays)")
    print("  • Error handling for API timeouts and connectivity issues")
    print("  • Integration with your existing osmnx workflow")
    print()
    print("Usage in your code:")
    print("  from infrastructure.find_cycle_route_relations import get_adelaide_bike_network_with_cycle_routes")
    print("  G = get_adelaide_bike_network_with_cycle_routes()")
    print("  nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)")
    print("  # Now use edges['IS_CYCLE_ROUTE'] in your regression")


if __name__ == "__main__":
    demonstrate_workflow()
    show_actual_implementation()