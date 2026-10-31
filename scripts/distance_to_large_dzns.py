import osmnx as ox

def join_dnl_dzn(G):
    nodes, edges = ox.graph_to_gdfs(G)
    