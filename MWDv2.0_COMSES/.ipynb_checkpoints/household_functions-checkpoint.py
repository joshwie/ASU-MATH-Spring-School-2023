import numpy as np

def tribute_hours(p, S_N, omega, m, H_max):
    return max(0, (p * S_N - (max(0, m))) / omega)

def optimal_hours(beta, alpha, H_max, omega, m, p, S_N):
    hours = beta * H_max + alpha / omega * max(0, (p * S_N - max(0, m)))
    #hours = beta * H_max + alpha * (H_N - max(0, max(0, m) - p * S_N) / omega)
    return hours

def plan_consumption(S_N, omega, p, hours, m):
    income = hours * omega
    if hours > 0:
        S = (income + max(m, 0)) / p
    else:
        S = (max(m, 0)) / p 
    demand = max(S, S_N)
    return demand, income

def calculate_utility(H_max, H_W, S_C, S_N, alpha, beta):
    return (H_max - H_W) ** alpha * np.maximum(0, S_C - S_N) ** beta

def update_ledger(income, p, s, m):
    expenditure = p * s
    # if income >= 0:
    #     m += income - expenditure
    # else:
    #     m -= expenditure
    m += income - expenditure
    return m, expenditure