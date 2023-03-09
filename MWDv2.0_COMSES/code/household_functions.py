
#!/usr/bin/env python
# coding: utf-8

# for use with Modern Wage Dynamics Model
# version 2.0
#
# March 2023
# J M Applegate
#
# houses all household-specific functions, called by main.py
# 5 of 7

import numpy as np

def tribute_hours(p, S_N, omega, m, H_max):
    return np.maximum((p * S_N - m) / omega, 0)

def optimal_hours(beta, alpha, H_max, omega, m, p, S_N):
    return beta * H_max + alpha / omega * (p * S_N - m)

def plan_consumption(S_N, omega, p, hours, m):
    income = hours * omega
    demand = np.maximum((income + m) / p, S_N)
    return demand, income

def calculate_utility(H_max, H_W, S_C, S_N, alpha, beta):
    return (H_max - H_W) ** alpha * np.maximum(0, S_C - S_N) ** beta

def update_ledger(income, p, s, m):
    expenditure = p * s
    m += income - expenditure
    return m, expenditure