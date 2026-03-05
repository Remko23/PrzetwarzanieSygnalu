import numpy as np
import generators


def generate_time(t1, duration, sampling_freq):
    n = np.arange(0, int(duration * sampling_freq))
    t = n / sampling_freq + t1
    return t

# to bedzie podawal user
A = 10.0
t1 = 0.0
d = 5.0
f = 100.0

t = generate_time(t1, d, f)

noise_uniform = generators.noise_uniform(A, t) #S1

noise_gauss = generators.noise_gauss(A, t) #S2

print("--------------- S1: ---------------")
print(noise_uniform)

print("--------------- S2: ---------------")
print(noise_gauss)