import numpy as np
import scipy.fft as sp_fft
import scipy.linalg as sp_linalg
from TransformacjaSygnalu import TransformacjaSygnalu
import time

def test_transformations():
    N = 256
    print(f"Testy transformacji \n")
    x_real = np.random.rand(N)

    x_complex = np.random.rand(N) + 1j * np.random.rand(N)
    
    tests = []

    t0 = time.time()
    res_custom = TransformacjaSygnalu.dyskretna_transformacja_fouriera(x_real)
    t1 = time.time()
    res_scipy = sp_fft.fft(x_real) / N
    t2 = time.time()
    tests.append(("DFT (rzeczywisty)", res_custom, res_scipy, t1-t0, t2-t1))


    t0 = time.time()
    res_custom = TransformacjaSygnalu.dyskretna_transformacja_fouriera(x_complex)
    t1 = time.time()
    res_scipy = sp_fft.fft(x_complex) / N
    t2 = time.time()
    tests.append(("DFT (zespolony)", res_custom, res_scipy, t1-t0, t2-t1))


    t0 = time.time()
    res_custom = TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czasie(x_complex)
    t1 = time.time()
    res_scipy = sp_fft.fft(x_complex) / N
    t2 = time.time()
    tests.append(("FFT DIT", res_custom, res_scipy, t1-t0, t2-t1))


    t0 = time.time()
    res_custom = TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czestotliwosci(x_complex)
    t1 = time.time()
    res_scipy = sp_fft.fft(x_complex) / N
    t2 = time.time()
    tests.append(("FFT DIF", res_custom, res_scipy, t1-t0, t2-t1))


    X_complex = TransformacjaSygnalu.dyskretna_transformacja_fouriera(x_complex)
    t0 = time.time()
    res_custom = TransformacjaSygnalu.odwrotna_dyskretna_transformacja_fouriera(X_complex)
    t1 = time.time()
    res_scipy = sp_fft.ifft(X_complex * N)
    t2 = time.time()
    tests.append(("IDFT", res_custom, res_scipy, t1-t0, t2-t1))
    

    t0 = time.time()
    res_custom = TransformacjaSygnalu.odwrotna_szybka_transformacja_fouriera(X_complex)
    t1 = time.time()
    res_scipy = sp_fft.ifft(X_complex * N)
    t2 = time.time()
    tests.append(("IFFT", res_custom, res_scipy, t1-t0, t2-t1))


    t0 = time.time()
    res_custom = TransformacjaSygnalu.dyskretna_transformacja_kosinusowa(x_real)
    t1 = time.time()
    res_scipy = sp_fft.dct(x_real, type=2, norm='ortho')
    t2 = time.time()
    tests.append(("DCT", res_custom, res_scipy, t1-t0, t2-t1))


    t0 = time.time()
    res_custom = TransformacjaSygnalu.szybka_transformacja_kosinusowa(x_real)
    t1 = time.time()
    res_scipy = sp_fft.dct(x_real, type=2, norm='ortho')
    t2 = time.time()
    tests.append(("FCT (Szybka Kosinusowa)", res_custom, res_scipy, t1-t0, t2-t1))


    H = sp_linalg.hadamard(N)
    t0_scipy = time.time()
    scipy_wht = np.dot(H, x_real) / N
    t1_scipy = time.time()
    
    t0 = time.time()
    res_custom = TransformacjaSygnalu.transformacja_walsha_hadamarda(x_real)
    t1 = time.time()
    tests.append(("WHT (Walsh-Hadamard)", res_custom, scipy_wht, t1-t0, t1_scipy-t0_scipy))


    t0 = time.time()
    res_custom = TransformacjaSygnalu.szybka_transformacja_walsha_hadamarda(x_real)
    t1 = time.time()
    tests.append(("FWHT (Szybki WHT)", res_custom, scipy_wht, t1-t0, t1_scipy-t0_scipy))

    print(f"{'Transformata':<25} | {'MSE względem Scipy':<12} | {'Czas [s] (Nasza)':<15} | {'Czas [s] (Scipy)':<15}")
    print("-" * 85)
    
    for name, c_res, s_res, t_c, t_s in tests:
        mse = np.mean(np.abs(c_res - s_res)**2)
        print(f"{name:<25} | {mse:<18.2e} | {t_c:<16.6f} | {t_s:<16.6f} ")

if __name__ == '__main__':
    test_transformations()
