import numpy as np

def noise_uniform(A, t):
    return np.random.uniform(-A, A, len(t))


def noise_gauss(A, t):
    return np.random.normal(0, 1, len(t)) * A