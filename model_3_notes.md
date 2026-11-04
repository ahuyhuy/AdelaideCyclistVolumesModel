# Exploring Segmented Regression For Cyclist Volume in the Adelaide CBD

`investigation/adelaide-model-2/model_2_X_y.csv` shows the regression table for model 2, which used plain negative binomial regression for its prediction model. An outstanding issue was the parklands count locations, because the mesh blocks they fall in have no people in them, just parklands.

Segmented regression allows for different 'variations' of a regression model to be applied to different segments of the data. For this model, which will focus on the just the Adelaide CBD boundary (R3114051), the data will be segmented into PARKLANDS and CBD. Formally, this is done by creating a duplicate set of vars, eg. POW_FE becomes POW_FE_CBD and POW_FE_PARKLANDS, but for this model, just going to instead run different models to see the effectiveness. Variables for the PARKLANDS segment will be a reduced set, since MB is useless here.

## Variables:

Some of the MBI classifier columns from model 2 had no variance. Some of these are because this type of bike infrastructure doesn't exist in Adelaide, and some are because everything in OSM is marked as this: `['MBI_PL', 'MBI_BL', 'MBI_Ad', 'MBI_PkPt', 'MBI_No']`.

- POW_CTW: N people who work in this DZN and cycle to work
- POW_FE: N people who work in this DZN and are fully engaged in employment or study
- PD_MB: MB population density
- DNL_DZN: Distance to nearest large DZN
- M_30_40, F_15_25: Age demographics, try males 30-40 and females 15-25 (best from Dadshova's)
- H_3500: Households with a THI of > 3500, place of enumeration, MB
- INF_CR: Listed cycle routes

__Monash Bicycle Infrastructure Classification__ - Binary dummy variables for every type of bicycle infrastructure

- MBI_BP: Dedicated bike path, Shared bike path
- MBI_PP: Pedestrian path/street with cycling allowed
- MBI_PTL: Painted bike lane, Painted bike lane (single-side)
- MBI_Sh: Sharrow
- MBI_SZ: Shared zone
- MBI_Bus: Bus lane with cycling allowed
- MBI_Mx: Mixed traffic

## Segmentation Approach

The model will be split into parklands and CBD just by separating the 0-population mesh block rows of the joined table. Because there are two separate models, it's not actually 'proper' segmentation, but this model is a feasibility test.