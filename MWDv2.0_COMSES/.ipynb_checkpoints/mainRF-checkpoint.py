# coding: utf-8

# for use with Modern Wage Dynamics Model
# version 2.0
#
# March 2023
# J M Applegate
#
# use with python3 main.py
# 1 of 6

import numpy as np
import pandas as pd

from numpy.random import default_rng
from operator import itemgetter
import copy

import warnings
warnings.filterwarnings('ignore')

#### series setup
from series_parametersRF import series_params
directory, series_name, seed, reps, n_sets, sim_params_list = series_params()

#### initialise rng to be used by simulation series
rng = default_rng(seed)

from initialisation_functions import *
from firm_functions import *
from household_functions import *
from market_functions import *
from simulationRF import simulation

macro_labels = ['set', 'run', 'step', 'n', 'H_max', 'A', 'gamma', 'mu', 'S_N', 'omega_0', 'p_0',
                    'I', 'pi', 'total_pi', 'omega', 'p', 'H_D', 'S_S', 'S_P', 'S_hat', 'N', 'H_S', 'H_M', 'S_D', 'S_M',
                    'total_H_N', 'total_H_O','total_m', 'med_m', 'mean_m', 'max_m', 'min_m']

# micro_labels = ['set', 'run', 'step', 'n', 'omega_max', 'H_max', 'A', 'gamma', 'mu', 'S_N', 'omega_0', 'p_0',
#                     'I', 'pi', 'total_pi', 'omega', 'p', 'H_D', 'S_S', 'S_P', 'S_hat', 'N', 'H_S', 'H_M', 'S_D', 'S_M',
#                     'household', 'alpha', 'beta', 'H_N', 'H_O', 'H', 'H_W', 'm', 'S', 'S_C', 'income', 'U', 'expenditure']

print('This experiment consists of {} simulations'.format(n_sets * reps))
print('consisting of {} parameter sets.'.format(n_sets))

# intitialise storage vehicle for series results
series_results = []

#### main body of multi parameter set code
for params in sim_params_list:
    # unpack parameters
    r, s, t_max, n, H_max, omega_0, p_0, A, gamma, mu, S_N = params
    r_, s_ = copy.deepcopy(r), copy.deepcopy(s)
    sim_results = simulation(s_, r_, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0, rng)
    series_results.append(sim_results)

print('\nFinished series.')

# For troubleshooting
#print(series_results)

# Transform list of lists into dataframes
sim_results_frame = pd.DataFrame(sim_results, columns = macro_labels) #use micro_labels with micro results
print(sim_results_frame)
# Expand subarrays for micro results
#sim_results_long = sim_results_frame.explode(['household', 'alpha', 'beta', 'H_N', 'H_O', 'H', 'H_W', 'm', 'S', 'S_C', 'income', 'U', 'expenditure'])

#### Save expanded dataframes to directory as csv files.
# print('Writing to files.')
# prefix = directory + 'series_' + series_name

# # For micro results
# #sim_results_long.to_csv(prefix + '.csv', index = False)
# #print('Series results written to', prefix + '_micro.csv')

# # For macro results
# sim_results_frame.to_csv(prefix + '.csv', index = False)
# print('Series results written to', prefix + '.csv')
