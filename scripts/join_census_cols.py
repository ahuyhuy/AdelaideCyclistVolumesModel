import csv

def join_pow_ctw():
    return None;

def join_pow_fe():
    return None;

def join_age_dems():
    return None;

def join_h_3500():
    return None;

def join_all(G):
    G = join_pow_ctw(G)
    G = join_pow_fe(G)
    G = join_age_dems(G)
    G = join_h_3500(G)
    return G;