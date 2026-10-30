# Cycle Route Relations Extraction

This module provides functionality to extract OpenStreetMap route:bicycle relations 
and integrate them as edge attributes in a street network graph for regression analysis.

## Files

- `find-cycle-route-relations.py`: Main script to get Adelaide bike network with cycle route attributes
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Usage

```python
from infrastructure.find_cycle_route_relations import get_adelaide_bike_network_with_cycle_routes

# Get the graph with IS_CYCLE_ROUTE edge attribute
G = get_adelaide_bike_network_with_cycle_routes()

# The graph now has an IS_CYCLE_ROUTE attribute on edges:
# - 1 if the edge is part of a bicycle route relation
# - 0 otherwise

# Example usage in regression analysis:
import osmnx as ox
nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)

# Now you can use edges['IS_CYCLE_ROUTE'] as a dummy variable in your regression model
```

## How it Works

1. **Boundary Definition**: Uses OSM relation ID R11381689 to get the Adelaide boundary
2. **Graph Retrieval**: Fetches the bicycle network using `ox.graph_from_polygon()` with network_type="bike"
3. **Cycle Route Extraction**: Queries Overpass API for all route:bicycle relations within the boundary
4. **Attribute Assignment**: Marks edges that are part of bicycle route relations with IS_CYCLE_ROUTE = 1
5. **Return**: Returns NetworkX graph with the new edge attribute

## Dependencies

- osmnx: For street network retrieval and manipulation
- overpass: For querying OpenStreetMap via Overpass API
- pandas: For data manipulation

Install with:
```bash
pip install -r requirements.txt
```

## Note on Performance

The Overpass API query may take some time depending on the size of the area and number of relations.
The script includes timeout settings to prevent hanging requests.