#!/usr/bin/env python
# coding: utf-8

# for use with Modern Wage Dynamics Model
# version 2.0
#
# March 2023
# J M Applegate
#
# houses initialisation functions, called by main.py
# 3 of 7

import numpy as np

def create_firm(omega_0, p_0):
    I = 0
    pi = 0
    total_pi = 0
    omega = omega_0
    p = p_0
    H_D = 0
    S_P = 0
    S_S = 0
    return I, pi, total_pi, omega, p, H_D, S_P, S_S

def create_households(n, H_max, rng):
    #alpha = rng.uniform(0, 1, n)
    #Bimodal distribution (workaholic households and relax households)
    alpha = np.concatenate([rng.normal(0.3, 0.05, int(0.5*n)), rng.normal(0.7, 0.05, int(0.5*n))])
    #print(alpha)
    beta = 1 - alpha
    H_N = np.zeros(n)
    H_O = np.zeros(n)
    H = np.repeat(H_max / 2, n) #set intial household hours to half of H_max
    H_W = np.empty(n)
    income = np.empty(n)
    m = np.zeros(n)
    S = np.empty(n)
    S_C = np.empty(n)
    U = np.zeros(n)
    expenditure = np.zeros(n)
    return alpha, beta, H_N, H_O, H, H_W, income, m, S, S_C, U, expenditure

#vectorised implementation for intialisation
def optimal_demand(alpha, beta, omega, p, H_max, S_N):
    demand = beta * omega / p * H_max + alpha * S_N
    return demand

def initialise_demand_expectation(n, alpha, beta, omega, p, H_max, S_N):
    demands = optimal_demand(alpha, beta, omega, p, H_max, S_N)
    S_hat = n * np.average(demands)
    return S_hat, demands[1:]