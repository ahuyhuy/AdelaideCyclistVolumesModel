# POW_CTW: N people who work in this DZN and cycle to work
# POW_FE: N people who work in this DZN and are fullly engaged in employment or study
# M_30_40, F_15_25: Age demographics - males 30-40 and females 15-25
# H_3500: Households with a THI of > 3500, place of enumeration, MB

import pandas as pd

def join_pow_ctw(
        G,
        csv_path="../all-data/census-formatted/greater-adelaide/MTW-Bicycle-POW-DZN.csv"
):
    df = pd.read_csv(csv_path)
    dzn_col = 'DZN (POW)' if 'DZN (POW)' in df.columns else df.columns[0]
    bicycle_col = 'Bicycle' if 'Bicycle' in df.columns else df.columns[1]

    return None;

def join_pow_fe(
        G,
        csv_path="../all-data/census-formatted/greater-adelaide/EETP-POW-DZN.csv"
):
    df = pd.read_csv(csv_path)
    dzn_col = 'DZN (POW)' if 'DZN (POW)' in df.columns else df.columns[0]
    fe_col = 'Fully Engaged' if 'Fully Engaged' in df.columns else df.columns[1]

    return None;

def join_age_dems(
        G,
        csv_path="../all-data/census-formatted/greater-adelaide/A5YG-S-UR-MB.csv"
):
    df = pd.read_csv(csv_path)
    mb_col = 'MB (UR)' if 'MB (UR)' in df.columns else df.columns[0]
    males_30_34_col = 'M 30-34 years' if 'M 30-34 years' in df.columns else df.columns[7]
    males_35_39_col = 'M 35-39 years' if 'M 35-39 years' in df.columns else df.columns[8]
    females_15_19_col = 'F 15-19 years' if 'F 15-19 years' in df.columns else df.columns[25]
    females_15_19_col = 'F 20-24 years' if 'F 20-24 years' in df.columns else df.columns[26]

    return None;

def join_h_3500(
        G,
        csv_path="../all-data/census-formatted/greater-adelaide/THI-PE-MB.csv"
):
    df = pd.read_csv(csv_path)
    mb_col = 'MB (UR)' if 'MB (UR)' in df.columns else df.columns[0]
    target_cols = # THI_3500 is the sum of each of these cols: [17, 18, 19, 20, 21, 22] 
    return None;

def join_all(G):
    G = join_pow_ctw(G)
    G = join_pow_fe(G)
    G = join_age_dems(G)
    G = join_h_3500(G)
    return G;