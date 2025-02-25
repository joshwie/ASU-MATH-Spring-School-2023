#!/usr/bin/env python
# coding: utf-8

# for use with Modern Wage Dynamics Model
# version 2.0
#
# March 2023
# J M Applegate
#
# used to specify all parameter values, called by main.py
# 2 of 6

def series_params():
    series_name = 'Mar2_SN300_r500_mu1_n10000_w10_p1'
    directory = '~/Dropbox (ASU)/MWDv2.0/' #./results/'

    # series variables
    seed = None
    t_max = 2000 #number of simulation steps
    reps = 5 #repetitions of each parameter set

    # simulation variables
    n_list = [10] #number of households
    omega_0_list = [10] #inital wage
    p_0_list = [1] #intial price
    H_max = 400 #max household hours per month

    # firm parameters
    A_list = [3] #firm production function coefficient
    gamma_list = [1.2] #firm production function exponent
    mu_list = [1] #memory for firm expectation updates

    #base consumption requirement
    S_N_list = [300] #[1200] #minimum household consumption

    param_sets = [[n, omega_0, p_0, A, gamma, mu, S_N] for n in n_list for omega_0 in omega_0_list for p_0 in p_0_list 
    for A in A_list for gamma in gamma_list for mu in mu_list for S_N in S_N_list]

    # determine number of distinct parameter sets
    n_sets = len(param_sets)
    
    # add fixed parameters
    for s in range(n_sets):
        (param_sets[s]).insert(0, t_max)
        (param_sets[s]).insert(2, H_max)
        (param_sets[s]).insert(0, s)
        
    expanded_sets = [item.copy() for item in param_sets for i in range(reps)]
    
    run_list = list(range(reps)) * n_sets
    
    for i in range(n_sets * reps):
        (expanded_sets[i]).insert(0, run_list[i])

    return directory, series_name, seed, reps, n_sets, expanded_sets
