import numpy as np

def series_params():
    series_name = 'Feb3_t1000_SN300_r500_mu1to20_n100_w10_p1_pctp1_v3'
    directory = '../results/'

    # series variables
    #seed = 71205
    seed = None
    #verbose = True
    verbose = False
    t_max = 1000 #number of simulation steps
    reps = 500 #repetitions of each parameter set

    # simulation variables
    n_list = [100] #number of households
    omega_0_list = [10] #inital wage
    p_0_list = [1] #intial price
    H_max = 400 #max household hours per month

    # firm parameters
    A_list = [3]
    gamma_list = [1.2] #firm production function
    mu_list = [1, 2, 10, 15, 20] #memory for firm expectation updates
    pct_list = [.1] #percentage of wage adjustment

    #base consumption requirement, per month
    S_N_list = [300] #[1200] #minimum household consumption

    #combine multi-value parameters
    # added efficiency variable for v1.1.0
    param_names = ['n', 'omega_0', 'p_0', 'A', 'gamma', 'mu', 'pct', 'S_N']

    param_sets = [[n, omega_0, p_0, A, gamma, mu, pct, S_N] for n in n_list for omega_0 in omega_0_list for p_0 in p_0_list for
                  A in A_list for gamma in gamma_list for mu in mu_list for pct in pct_list for S_N in S_N_list]

    n_sets = len(param_sets)

    # make parameter dictionary (variable and fixed parameters
    fixed_params = {'t_max': t_max,
                    'H_max': H_max,
                   }

    sim_params_list = [{**dict(zip(param_names, ps)), **fixed_params} for ps in param_sets]

    return directory, series_name, verbose, seed, n_sets, sim_params_list, reps
