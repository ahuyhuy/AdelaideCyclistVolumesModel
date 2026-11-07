# Segment variables

Decisions have been made on what vars to drop based on column holdout validation - invididual columns were withheld from different segments based on correlation and coefficient values.

## CBD

- POW_CTW: N people who work in this DZN and cycle to work
- POW_FE: N people who work in this DZN and are fully engaged in employment or study
- PD_MB: MB population density
- DNL_DZN: Distance to nearest large DZN
- M_30_40, F_15_25: Age demographics, males 30-40 and females 15-25
- INF_CR: Listed cycle routes
- MBI_PTL: Painted bike lane, Painted bike lane (single-side)

__Dropped__

- MBI_SZ: Shared zone // NA
- MBI_Bus: Bus lane with cycling allowed // NA
- MBI_Mx: Mixed traffic // NA
- H_3500: Households with a THI of > 3500, place of enumeration, MB // CORRELATED (less relevant for CBD cos most cycle traffic originates from outside of CBD)
- MBI_BP: Dedicated bike path, Shared bike path // CORRELATED

## CBDP

- POW_CTW: N people who work in this DZN and cycle to work
- POW_FE: N people who work in this DZN and are fully engaged in employment or study
- DNL_DZN: Distance to nearest large DZN
- INF_CR: Listed cycle routes
- MBI_BP: Dedicated bike path, Shared bike path
- MBI_PTL: Painted bike lane, Painted bike lane (single-side)
- MBI_SZ: Shared zone
- MBI_Bus: Bus lane with cycling allowed

__Dropped__

- MBI_PP: Pedestrian path/street with cycling allowed // NA
- MBI_Sh: Sharrow // NA
- MBI_Mx: Mixed traffic // NA
- All MB related cols cos empty

## S

- POW_CTW: N people who work in this DZN and cycle to work
- POW_FE: N people who work in this DZN and are fully engaged in employment or study
- PD_MB: MB population density
- DNL_DZN: Distance to nearest large DZN
- M_30_40, F_15_25: Age demographics, males 30-40 and females 15-25 (best from Dadshova's)
- H_3500: Households with a THI of > 3500, place of enumeration, MB
- INF_CR: Listed cycle routes


__Dropped__

- MBI_BP: Dedicated bike path, Shared bike path // CORRELATED
- MBI_Sh: Sharrow // BAD
- MBI_PTL: Painted bike lane, Painted bike lane (single-side) // BAD
- MBI_PP: Pedestrian path/street with cycling allowed // NA
- MBI_SZ: Shared zone // NA
- MBI_Bus: Bus lane with cycling allowed // NA
- MBI_Mx: Mixed traffic // NA

## SP

- POW_CTW: N people who work in this DZN and cycle to work
- POW_FE: N people who work in this DZN and are fully engaged in employment or study
- PD_MB: MB population density
- DNL_DZN: Distance to nearest large DZN
- M_30_40, F_15_25: Age demographics, males 30-40 and females 15-25 (best from Dadshova's)
- H_3500: Households with a THI of > 3500, place of enumeration, MB
- INF_CR: Listed cycle routes
- MBI_BP: Dedicated bike path, Shared bike path
- MBI_PP: Pedestrian path/street with cycling allowed
- MBI_PTL: Painted bike lane, Painted bike lane (single-side)
- MBI_Sh: Sharrow
- MBI_SZ: Shared zone
- MBI_Bus: Bus lane with cycling allowed
- MBI_Mx: Mixed traffic

__Dropped__

