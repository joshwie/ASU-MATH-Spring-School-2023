#!/usr/bin/env python
# coding: utf-8

# for use with Modern Wage Dynamics Model
# version 2.0
#
# March 2023
# J M Applegate
#
# use with python3 main.py
# 7 of 7

import numpy as np

from initialisation_functions import *
from firm_functions import *
from household_functions import *
from market_functions import *

def simulation(s, r, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0, rng):
    
    sim_results = []
    t = 0

    households = np.arange(0, n)

    # intitialise firm and household
    I, pi, total_pi, omega, p, H_D, S_P, S_S = create_firm(omega_0, p_0)
    alpha, beta, H_N, H_O, H, H_W, income, m, S, S_C, U, expenditure = create_households(n, H_max, rng)
    N, S_D, H_M, S_M, H_S = 0, 0, 0, 0, 0
    S_D = 1 # these can be any two different inital values that satisfy abs(S_D - S_S) > 1.
    S_S = 2

    # initialise firm effort and demand expectations
    idxs = rng.integers(0, n, size = mu)

    # household sample S_hat
    S_hat, demand_memory = initialise_demand_expectation(n, alpha[idxs], beta[idxs], omega, p, H_max, S_N)

    #save initial results
    #macro results
    step_results = [s, r, t, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0,
                    I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
                    np.sum(H_N), np.sum(H_O), np.sum(m), np.median(m), np.mean(m), np.max(m), np.min(m)]

    #micro results
    # step_results = [s, r, t, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0,
    #                 I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
    #                 households, alpha, beta, H_N.copy(), H_O.copy(), H.copy(), H_W.copy(), m.copy(), S.copy(),
    #                 S_C.copy(), income.copy(), U.copy(), expenditure.copy()]

    sim_results.append(step_results)

    # the simulation steps can be run for a fixed number, t_max, 
    # or with the stopping condition that S_S is within 1 unit of S_D.

    # conditional steps
    while abs(S_D - S_S)>= 1 and t < t_max:
        t = t + 1

    # t_max simulation steps
    #for t in range(1, t_max + 1):

        #firm(s) determines hours
        H_D, S_P = determine_hours(S_hat, A, gamma, S_N, n, I)

        #households determine effort and hours supplied
        m_pos = m.copy()
        m_pos = np.maximum(m_pos, 0)
        H_N = tribute_hours(p, S_N, omega, m_pos, H_max)
        H_O = optimal_hours(beta, alpha, H_max, omega, m_pos, p, S_N)
        H = np.minimum(H_N + H_O, H_max)

        #market aggregates hours supplied, determines market hours and effective effort
        H_S = np.sum(H)
        H_M = min(H_D, H_S)
        N, H_W = aggregate_effort(H_S, H_D, H)

        #firm produces sugar with effective labour
        S_S = produce_supply(A, N, gamma, I)

        #households plan sugar consumption
        S, income = plan_consumption(S_N, omega, p, H_W, m_pos)

        #market aggregates sugar demand and determines sugar sold
        S_D = np.sum(S)
        S_M = min(S_S, S_D)
        S_C = sell_sugar(S_S, S_D, S)

        #calculate firm profit
        pi = profit(omega, p, S_M, H_M)
        total_pi += pi

        #calculate household utility
        U = calculate_utility(H_max, H_W, S_C, S_N, alpha, beta)

        #households adjust ledgers
        m, expenditure = update_ledger(income, p, S_C, m)

        #firm adjusts inventory
        #I = adjust_inventory(S_S, S_M, I)

        #firm updates demand expectations
        S_hat, demand_memory = update_expectation(S_D, demand_memory, mu)

        # firm raises or lowers wage
        omega, p = update_wage_price(omega, p, pi, S_S, S_D, S_M, H_M)

        #write step state to frame
        #macro results
        step_results = [s, r, t, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0,
                        I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
                        np.sum(H_N), np.sum(H_O), np.sum(m), np.median(m), np.mean(m), np.max(m), np.min(m)]
        #micro results
        # step_results = [s, r, t, t_max, n, omega_max, H_max, A, gamma, mu, S_N, omega_0, p_0,
        #                 I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
        #                 households, alpha, beta, H_N.copy(), H_O.copy(), H.copy(), H_W.copy(), m.copy(), S.copy(),
        #                 S_C.copy(), income.copy(), U.copy(), expenditure.copy()]
        
        sim_results.append(step_results)

    return sim_results


# if __name__ == "__main__":
#     import sys
#     lineno = sys.argv[1]
#     with open(r"E:\demos\files\read_demo.txt", 'r') as fp:
#     # read line 8
#     params = fp.readlines()[7]
#     #split tupple into string, then a = float(a)
#     r, s, t_max, n, H_max, omega_0, p_0, A, gamma, mu, pct, S_N = params
#     sim_result = simulation(r, s, t_max, n, H_max, omega_0, p_0, A, gamma, mu, pct, S_N)
#     #save_to_scratch results_s_r.csv

