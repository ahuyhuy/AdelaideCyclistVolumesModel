#!/usr/bin/env python3
"""
Export Adelaide bike network nodes/edges and DZN boundaries with POW population
as GeoPackages for viewing in QGIS.
"""

import osmnx as ox
import geopandas as gpd
import pandas as pd
import networkx as nx

# Settings
ox.settings.log_console = True
ox.settings.use_cache = True

print("Loading Greater Adelaide boundary...")
gdf_boundary = ox.geocode_to_gdf("R11381689", by_osmid=True)
polygon = gdf_boundary.geometry.iloc[0]

print("Loading bike network graph...")
G = ox.graph_from_polygon(polygon, network_type="bike")
print(f"Nodes: {len(G.nodes)}. Edges: {len(G.edges)}")

print("Loading DZN boundaries...")
dzns_aus = gpd.read_file("../all-data/australia-destination-zones-raw/DZN_2021_AUST_GDA2020.shp")
dzn_gdf_boundary_crs = gdf_boundary.to_crs(dzns_aus.crs)
dzns = gpd.clip(dzns_aus, dzn_gdf_boundary_crs)
print(f"DZN Adelaide count: {len(dzns)}")

print("Joining DZN_CODE21 to graph nodes...")
nodes_gdf = ox.graph_to_gdfs(G, nodes=True, edges=False)[["geometry"]]

nodes_dzns = gpd.sjoin(
    nodes_gdf.to_crs(dzns.crs),
    dzns[["DZN_CODE21", "geometry"]],
    how="left",
    predicate="within",
)
node_dzn_codes = nodes_dzns["DZN_CODE21"].dropna().to_dict()
nx.set_node_attributes(G, node_dzn_codes, "DZN_CODE21")
print(f"Nodes with DZN_CODE21: {len(node_dzn_codes)} / {len(G.nodes)}")

print("Loading POW population data...")
pow_df = pd.read_csv(
    "../all-data/census-formatted/greater-adelaide/EETP-POW-DZN.csv",
    usecols=["DZN (POW)", "Total"]
)
pow_df.columns = ["DZN_CODE21", "POW_Population"]
pow_df["DZN_CODE21"] = pow_df["DZN_CODE21"].astype(str)

pow_mapping = pow_df.set_index("DZN_CODE21")["POW_Population"].to_dict()

node_dzn = nx.get_node_attributes(G, "DZN_CODE21")
node_pow_pop = {}
for node, dzn in node_dzn.items():
    dzn_str = str(dzn)
    node_pow_pop[node] = pow_mapping.get(dzn_str, 0)

nx.set_node_attributes(G, node_pow_pop, "POW_Population")
nodes_with_pop = sum(1 for v in node_pow_pop.values() if v > 0)
print(f"Nodes with POW Population data: {nodes_with_pop} / {len(G.nodes)}")
print(f"POW Population range: {min(node_pow_pop.values())} - {max(node_pow_pop.values())}")

print("\nExporting to GeoPackage...")

# Export nodes
nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)
nodes_gdf = nodes_gdf.reset_index()
edges_gdf = edges_gdf.reset_index()

node_cols = ['osmid', 'geometry', 'x', 'y', 'DZN_CODE21', 'POW_Population']
nodes_export = nodes_gdf[[c for c in node_cols if c in nodes_gdf.columns]].copy()

edge_cols = ['u', 'v', 'key', 'geometry', 'length', 'highway', 'name', 'oneway']
edges_export = edges_gdf[[c for c in edge_cols if c in edges_gdf.columns]].copy()

nodes_export.to_file("adelaide_nodes_pow.gpkg", layer='nodes', driver='GPKG')
edges_export.to_file("adelaide_edges.gpkg", layer='edges', driver='GPKG')

# Export DZN boundaries with POW population joined
dzn_pow = dzns[['DZN_CODE21', 'geometry']].copy()
dzn_pow['DZN_CODE21'] = dzn_pow['DZN_CODE21'].astype(str)
dzn_pow = dzn_pow.merge(pow_df, on='DZN_CODE21', how='left')
dzn_pow['POW_Population'] = dzn_pow['POW_Population'].fillna(0).astype(int)
dzn_pow.to_file("adelaide_dzn_pow.gpkg", layer='dzn', driver='GPKG')

print(f"Exported {len(nodes_export)} nodes to adelaide_nodes_pow.gpkg")
print(f"Exported {len(edges_export)} edges to adelaide_edges.gpkg")
print(f"Exported {len(dzn_pow)} DZNs to adelaide_dzn_pow.gpkg")

print("\nNode POW Population stats:")
print(f"  Min: {nodes_export['POW_Population'].min()}")
print(f"  Max: {nodes_export['POW_Population'].max()}")
print(f"  Mean: {nodes_export['POW_Population'].mean():.1f}")
print(f"  Nodes with POW > 0: {(nodes_export['POW_Population'] > 0).sum()}")

print("\nDZN POW Population stats:")
print(f"  Min: {dzn_pow['POW_Population'].min()}")
print(f"  Max: {dzn_pow['POW_Population'].max()}")
print(f"  Mean: {dzn_pow['POW_Population'].mean():.1f}")
print(f"  DZNs with POW > 0: {(dzn_pow['POW_Population'] > 0).sum()}")

print("\nDone! Open the .gpkg files in QGIS.")
print("In QGIS:")
print("  1. Load adelaide_dzn_pow.gpkg as base layer")
print("  2. Style with Graduated symbology on POW_Population (Reds color ramp)")
print("  3. Add Labels > Single Labels > POW_Population")
print("  4. Load adelaide_nodes_pow.gpkg and adelaide_edges.gpkg on top")