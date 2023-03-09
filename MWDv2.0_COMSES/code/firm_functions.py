#!/usr/bin/env python
# coding: utf-8

# for use with Modern Wage Dynamics Model
# version 2.0
#
# March 2023
# J M Applegate
#
# houses all firm-specific functions, called by main.py
# 4 of 7

import numpy as np

def profit(omega, p, S_M, H_M):
    return p * S_M - omega * H_M

def determine_hours(S_D, A, gamma, S_N, n, I):
    if S_D >= S_N * n:
        S_P = S_D
        #S_P = max(0, S_D - I)
    else:
        S_P = S_N * n
        #S_P = max(0, S_N * n - I)
    H = (S_P / A) ** ( 1 / gamma)
    return H, S_P

def produce_supply(A, N, gamma, I):
    return A * N ** gamma + I

def adjust_inventory(S_S, S_M, I):
    if S_M < S_S:
        I += max(0, S_S - S_M)
    return I

def update_wage_price(omega, p, pi, S_S, S_D, S_M, H_M):
    omega_new = omega
    if S_S > S_D:
        if pi >= 0:
            p = omega * H_M / S_M
        else:
            omega_new = p * S_M / H_M
    elif S_S < S_D:
        if pi >= 0:
            omega_new = p * S_M / H_M
        else:
            p = omega * H_M / S_M
    # sticky wage
    #omega_new = omega
    return omega_new, p

def update_expectation(value, memory, mu):
    #memory = np.append(memory, value)
    #hat = np.average(memory, weights = np.arange(1, mu + 1))
    # only use last observed value
    hat = value
    return hat, memory[1:]