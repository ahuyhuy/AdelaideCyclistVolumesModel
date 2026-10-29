# Attempt 2!

So the first attempt was bad but thats expected. Going to look into what factors might be better for next one. Looking at Dadshova report, age demographic is a big one. Also want to try __edge-based__ approach instead of node-based, since infrastructure data is primarily edge-based. I want to also avoid correlation as much as possible now.

# Kept Vars from model-1:

- POW_CTW: N people who work in this DZN and cycle to work
    - ```all-data/census-formatted/greater-adelaide/MTW-Bicycle-POW-DZN.csv``` [Bicycle]
- POW_FE: N people who work in this DZN and are fullly engaged in employment or study
    - ```all-data/census-formatted/greater-adelaide/EETP-POW-DZN.csv``` [Fully Engaged]

# Looking at DZN more closely

`destination-zones` folder in the workspace is used for viewing Adelaide's destination zones closely to see how they interact better, so I can gauge how to use them better. Marking large DZNs may also be good (8000+ perhaps), try replacing D_CBD with distance to nearest large DZN. DZNs vary in size a bit so DZN job density may also be great. May have to try these separately because they are a bit correlated.

*Just had the idea of doing a '10000 jobs radius' for each DZN - how large do you have to make a circle radius from the centre of your DZN to get to 10000 jobs from DZNs captured in the circle. Gives a good idea of how far people in that DZN may have to travel to their job.*

# Improving infrastructure classifcation

Sustainable Mobility and Safety Research Group, Monash University. (2023). Bicycling infrastructure classification using OpenStreetMap. https://github.com/SustainableMobility/bicycling-infrastructure-classification

This project is a most complete classification system for biycle infrastructure with 21 different classes. For this model, these classes will be directly ported over and used as binary dummy variables, but after assessing correlations, the final model may use less, or aggregate the classes. Their repo is located in `bicycling-infrastructure-classification/`

The last bit of bike infrastructure they don't have is cycle routes. These include the Norwood-Magill Bikeway, etc. These are retrieved using the function from `infrastructure/cycle_routes.py`.

# New Vars to try:

- MB population density: PD_MB
- Distance to nearest large DZN: DNL_DZN
- Age demographics, try males 30-40 and females 15-25 (best from Dadshova's): M_30_40, F_15_25
- Households with a THI of > 3500, place of enumeration, MB: H_3500
- OSM route=bicycle: INF_CR

__Monash Bicycle Infrastructure Classification__ - Binary dummy variables for every type of bicycle infrastructure

- MBI_BP: Dedicated bike path, Shared bike path
- MBI_PP: Pedestrian path/street with cycling allowed
- MBI_PL: Protected bike lane
- MBI_BL: Buffered bike lane (kerb-side), Buffered bike lane (road-side), Buffered bike lane (both sides)
- MBI_PTL: Painted bike lane, Painted bike lane (single-side)
- MBI_Ad: Advisory bike lane, Advisory bike lane (single-side), Peak hour advisory bike lane, Peak hour advisory bike lane (single-side)
- MBI_PkPt: Peak hour painted bike lane, Peak hour painted bike lane (single-side)
- MBI_Sh: Sharrow
- MBI_SZ: Shared zone
- MBI_Bus: Bus lane with cycling allowed
- MBI_Mx: Mixed traffic
- MBI_No: Bicyclists dismount, Pedestrian path/street with cycling not allowed