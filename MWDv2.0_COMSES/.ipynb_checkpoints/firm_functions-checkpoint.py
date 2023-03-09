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

def update_wage_price(omega, pct, p, pi, H_S, H_D, S_S, S_D):
    omega_new = omega
    if  S_S < S_D:
        if pi > 0:
            omega_new = omega * (1 + pct)
        else:
            p = p * (1 + pct)
    elif S_S > S_D:
        if pi > 0:
            p = p * (1 - pct)
        else:
            omega_new = omega * (1 - pct)
    # sticky wage
    #omega_new = omega
    return omega_new, p

def update_expectation(value, memory, mu):
    memory = np.append(memory, value)
    hat = np.average(memory, weights = np.arange(1, mu + 1))
    return hat, memory[1:]