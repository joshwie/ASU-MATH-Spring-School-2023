import numpy as np
import pandas as pd

from numpy.random import default_rng
from math import floor
from operator import itemgetter

import warnings
warnings.filterwarnings('ignore')

# series setup
from series_parameters import series_params
directory, series_name, verbose, seed, n_sets, sim_params_list, reps = series_params()
rng = default_rng(seed)

from initialisation_functions import *
from firm_functions import *
from household_functions import *
from market_functions import *

sim_labels = ['set', 'run', 'step', 'n', 'H_max', 'A', 'gamma', 'mu', 'pct', 'S_N', 'omega_0', 'p_0',
                    'I', 'pi', 'total_pi', 'omega', 'p', 'H_D', 'S_S', 'S_P', 'S_hat', 'N', 'H_S', 'H_M', 'S_D', 'S_M',
                    'total_H_N', 'total_H_O','total_m', 'med_m', 'mean_m', 'max_m', 'min_m']

# micro_sim_labels = ['set', 'run', 'step', 'n', 'omega_max', 'H_max', 'A', 'gamma', 'mu', 'pct', 'S_N', 'omega_0', 'p_0',
#                     'I', 'pi', 'total_pi', 'omega', 'p', 'H_D', 'S_S', 'S_P', 'S_hat', 'N', 'H_S', 'H_M', 'S_D', 'S_M',
#                     'household', 'alpha', 'beta', 'H_N', 'H_O', 'H', 'H_W', 'm', 'S', 'S_C', 'income', 'U', 'expenditure']

sim_results = []

print('This experiment consists of {} simulations'.format(n_sets * reps))
print('consisting of {} parameter sets.'.format(n_sets))

#### main body of multi parameter set code
for s in range(n_sets):
    print('\nparameter set', s + 1)
    sim_params = sim_params_list[s]

    #unpack parameters
    t_max, n, H_max, mu, pct, omega_0, p_0, A, gamma, S_N = itemgetter('t_max', 'n', 'H_max', 'mu', 'pct', 'omega_0',
                                                                                  'p_0', 'A', 'gamma', 'S_N')(sim_params)

    for r in range(reps):

        t = 0

        households = np.arange(0, n)

        # intitialise firm and household
        I, pi, total_pi, omega, p, H_D, S_P, S_S = create_firm(omega_0, p_0)
        alpha, beta, H_N, H_O, H, H_W, income, m, S, S_C, U, expenditure = create_households(n, H_max, rng)
        N, S_D, H_M, S_M, H_S = 0, 0, 0, 0, 0

        # initialise firm effort and demand expectations
        idxs = rng.integers(0, n, size = mu)

        # household sample S_hat
        S_hat, demand_memory = initialise_demand_expectation(n, alpha[idxs], beta[idxs], omega, p, H_max, S_N)
        #H_hat, hours_memory = initialise_hours_expectation(n, beta[idxs], alpha[idxs], H_max, omega, S_N)

        #save initial results
        #macro results
        step_results = [s, r, t, n, H_max, A, gamma, mu, pct, S_N, omega_0, p_0,
                        I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
                        np.sum(H_N), np.sum(H_O), np.sum(m), np.median(m), np.mean(m), np.max(m), np.min(m)]

        #micro results
        # step_results = [s, r, t, n, omega_max, H_max, A, gamma, mu, pct, S_N, omega_0, p_0,
        #                 I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
        #                 households, alpha, beta, H_N.copy(), H_O.copy(), H.copy(), H_W.copy(), m.copy(), S.copy(),
        #                 S_C, income.copy(), U.copy(), expenditure.copy()]

        sim_results.append(step_results)

        # the simulation steps
        for t in range(1, t_max + 1):

            #firm(s) determines hours
            H_D, S_P = determine_hours(S_hat, A, gamma, S_N, n, I)

            #households determine effort and hours supplied
            for i in households:
                H_N[i] = tribute_hours(p, S_N, omega, m[i], H_max)
                H_O[i] = optimal_hours(beta[i], alpha[i], H_max, omega, m[i], p, S_N)
                H[i] = min(H_N[i] + H_O[i], H_max)

            #market aggregates hours supplied, determines market hours and effective effort
            H_S = np.sum(H)
            H_M = min(H_D, H_S)
            N, H_W = aggregate_effort(H_S, H_D, H)

            #firm produces sugar with effective labour
            S_S = produce_supply(A, N, gamma, I)

            #households plan sugar consumption
            for i in households:
                S[i], income[i] = plan_consumption(S_N, omega, p, H_W[i], m[i])

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
            for i in households:
                m[i], expenditure[i] = update_ledger(income[i], p, S_C[i], m[i])

            #firm adjusts inventory
            #I = adjust_inventory(S_S, S_M, I)

            #firm updates demand expectations
            S_hat, demand_memory = update_expectation(S_D, demand_memory, mu)

            # firm raises or lowers wage
            omega, p = update_wage_price(omega, pct, p, pi, H_S, H_D, S_S, S_D)

            #write step state to frame
            step_results = [s, r, t, n, H_max, A, gamma, mu, pct, S_N, omega_0, p_0,
                            I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
                            np.sum(H_N), np.sum(H_O), np.sum(m), np.median(m), np.mean(m), np.max(m), np.min(m)]
            sim_results.append(step_results)

print('\nFinished series.')

#transform list of lists into dataframes and expand subarrays
sim_results_frame = pd.DataFrame(sim_results, columns = sim_labels)
#sim_results_long = sim_results_frame.explode(['household', 'alpha', 'beta', 'H_N', 'H_O', 'H', 'H_W', 'm', 'S', 'S_C', 'income', 'U', 'expenditure'])

#### Save expanded dataframes to directory as csv files.
print('Writing to files.')
prefix = directory + 'series_' + series_name

#sim_results_long.to_csv(prefix + '.csv', index = False)
#print('Series results written to', prefix + '_micro.csv')

sim_results_frame.to_csv(prefix + '.csv', index = False)
print('Series results written to', prefix + '.csv')
