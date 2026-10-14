# Attempt 2!

So the first attempt was bad but thats expected. Going to look into what factors might be better for next one. Looking at Dadshova report, age demographic is a big one. Also want to try __edge-based__ approach instead of node-based, since infrastructure data is primarily edge-based.

# Kept Vars from model-1:

- POW_CTW: N people who work in this DZN and cycle to work
    - ```all-data/census-formatted/greater-adelaide/MTW-Bicycle-POW-DZN.csv``` [Bicycle]
- POW_FE: N people who work in this DZN and are fullly engaged in employment or study
    - ```all-data/census-formatted/greater-adelaide/EETP-POW-DZN.csv``` [Fully Engaged]
- INF_CW: 1 if the edge the count point lies on is a cycleway, else 0
- D_CBD: Distance from CBD polygon (0 for in CBD)

# New Vars to try:

- 

# Looking at DZN more closely

`destination-zones` folder in the workspace is used for viewing Adelaide's destination zones closely to see how they interact better, so I can gauge how to use them better.