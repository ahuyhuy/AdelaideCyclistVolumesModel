# Monash Bicycling Infrastructure Classifiers:
# • Dedicated bike path
# • Shared bike path
# • Pedestrian path/street with cycling allowed
# • Protected bike lane
# • Buffered bike lane (kerb-side)
# • Buffered bike lane (road-side)
# • Buffered bike lane (both sides)
# • Painted bike lane
# • Painted bike lane (single-side)
# • Advisory bike lane
# • Advisory bike lane (single-side)
# • Peak hour painted bike lane
# • Peak hour painted bike lane (single-side)
# • Peak hour advisory bike lane
# • Peak hour advisory bike lane (single-side)
# • Sharrow
# • Shared zone
# • Bus lane with cycling allowed
# • Mixed traffic
# • Bicyclists dismount
# • Pedestrian path/street with cycling not allowed

# These classifiers are aggregated into the following dummy variables, which should be loaded into the Graph

# - MBI_BP: Dedicated bike path, Shared bike path
# - MBI_PP: Pedestrian path/street with cycling allowed
# - MBI_PL: Protected bike lane
# - MBI_BL: Buffered bike lane (kerb-side), Buffered bike lane (road-side), Buffered bike lane (both sides)
# - MBI_PTL: Painted bike lane, Painted bike lane (single-side)
# - MBI_Ad: Advisory bike lane, Advisory bike lane (single-side), Peak hour advisory bike lane, Peak hour advisory bike lane (single-side)
# - MBI_PkPt: Peak hour painted bike lane, Peak hour painted bike lane (single-side)
# - MBI_Sh: Sharrow
# - MBI_SZ: Shared zone
# - MBI_Bus: Bus lane with cycling allowed
# - MBI_Mx: Mixed traffic
# - MBI_No: Bicyclists dismount, Pedestrian path/street with cycling not allowed

def enrich_graph_with_monash_classifiers(G):
    return 0