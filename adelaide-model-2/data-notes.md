# Attempt 2!

So the first attempt was bad but thats expected. Going to look into what factors might be better for next one. Looking at Dadshova report, age demographic is a big one. Also want to try __edge-based__ approach instead of node-based, since infrastructure data is primarily edge-based. I want to also avoid correlation as much as possible now.

# Kept Vars from model-1:

- POW_CTW: N people who work in this DZN and cycle to work
    - ```all-data/census-formatted/greater-adelaide/MTW-Bicycle-POW-DZN.csv``` [Bicycle]
- POW_FE: N people who work in this DZN and are fullly engaged in employment or study
    - ```all-data/census-formatted/greater-adelaide/EETP-POW-DZN.csv``` [Fully Engaged]
- INF_CW: 1 if the edge the count point lies on is a cycleway, else 0

# Looking at DZN more closely

`destination-zones` folder in the workspace is used for viewing Adelaide's destination zones closely to see how they interact better, so I can gauge how to use them better. Marking large DZNs may also be good (8000+ perhaps), try replacing D_CBD with distance to nearest large DZN. DZNs vary in size a bit so DZN job density may also be great. May have to try these separately because they are a bit correlated.

*Just had the idea of doing a '10000 jobs radius' for each DZN - how large do you have to make a circle radius from the centre of your DZN to get to 10000 jobs from DZNs captured in the circle. Gives a good idea of how far people in that DZN may have to travel to their job.*

# Improving infrastructure classifcation

Want to do a series of dummy vars for different types of roads according to OSM, such as existing INF_CW which is OSM highway:cycleway. Will take:
 - highway:trunk (Greenhill, Dequetteville, Portrush, N/S Motorway)
 - highway:primary (Fullarton, Payneham, Donald Bradman)
 - highway:secondary (Grenfell, Wakefield, Magill, Prospect)
 - highway:tertiary
 - highway:residential
 - cycleway:lane (left and right, not separate)
 - route=bicycle (the edge may also be part of a cycling route relation in OSM, eg. Norwood - Magill Bikeway, see `infrastucture/` on how these are being retrieved)

# New Vars to try:

- MB population density: PD_MB
- Distance to nearest large DZN: DNL_DZN
- Age demographics, try males 30-40 and females 15-25 (best from Dadshova's): M_30_40, F_15_25
- Households with a THI of > 3500, place of enumeration, MB: H_3500
- OSM highway=trunk: INF_LRG_RD
- OSM highway={primary, secondary}: INF_MED_RD
- OSM highway={tertiary, residential}: INF_SML_RD
- OSM cycleway:{left, right}=lane, not separate, just a normal bike lane: INF_CL
- OSM route=bicycle: INF_CR