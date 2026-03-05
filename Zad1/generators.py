import random
import math

def szum_jednostajny(A, t):
    return [random.uniform(-A, A) for _ in range(len(t))]


def szum_gaussa(A, t):
    samples = []
    for _ in range(len(t)):
        u1 = random.random()
        u2 = random.random()

        z0 = math.sqrt(-2.0 * math.log(max(u1, 1e-10))) * math.cos(2.0 * math.pi * u2)

        samples.append(z0 * A)
    return samples