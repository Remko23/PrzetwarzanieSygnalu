import numpy as np

class TransformacjaSygnalu:

    @staticmethod
    def dyskretna_transformacja_fouriera(x):
        N = len(x)
        m = np.arange(N)
        n = np.arange(N)
        mn = m.reshape((N, 1)) * n
        e = np.exp(-1j * 2 * np.pi * mn / N)
        X = np.dot(e, x) / N
        return X

    @staticmethod
    def odwrotna_dyskretna_transformacja_fouriera(X):
        N = len(X)
        m = np.arange(N)
        n = np.arange(N)
        mn = m.reshape((N, 1)) * n
        e = np.exp(1j * 2 * np.pi * mn / N)
        x = np.dot(e, X)
        return x

    @staticmethod
    def szybka_transformacja_fouriera_z_decymacja_w_czasie(x):
        x = np.asarray(x, dtype=complex)
        N = len(x)
        
        if N <= 1:
            return x
        
        if (N & (N - 1)) != 0:
            raise ValueError("Długość wektora musi być potęgą liczby 2")
            
        def _fft_dit_rekurencyjnie(x):
            N = len(x)
            if N <= 1:
                return x
            even = _fft_dit_rekurencyjnie(x[0::2])
            odd = _fft_dit_rekurencyjnie(x[1::2])
            
            T = [np.exp(-1j * 2 * np.pi * k / N) * odd[k] for k in range(N // 2)]
            return np.array([even[k] + T[k] for k in range(N // 2)] +
                            [even[k] - T[k] for k in range(N // 2)])
                            
        return _fft_dit_rekurencyjnie(x) / N

    @staticmethod
    def szybka_transformacja_fouriera_z_decymacja_w_czestotliwosci(x):
        x = np.asarray(x, dtype=complex)
        N = len(x)
        
        if N <= 1:
            return x
            
        if (N & (N - 1)) != 0:
            raise ValueError("Długość wektora musi być potęgą liczby 2")
            
        def _fft_dif_rekurencyjnie(x):
            N = len(x)
            if N <= 1:
                return x
            polowa = N // 2
            x_sum = x[:polowa] + x[polowa:]
            x_diff = (x[:polowa] - x[polowa:]) * np.exp(-1j * 2 * np.pi * np.arange(polowa) / N)
            
            X_even = _fft_dif_rekurencyjnie(x_sum)
            X_odd = _fft_dif_rekurencyjnie(x_diff)
            
            X = np.zeros(N, dtype=complex)
            X[0::2] = X_even
            X[1::2] = X_odd
            return X
            
        return _fft_dif_rekurencyjnie(x) / N

    @staticmethod
    def odwrotna_szybka_transformacja_fouriera(X):
        N = len(X)
        if N <= 1:
            return X
        X = np.asarray(X, dtype=complex)
        
        wynik = np.conjugate(TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czasie(np.conjugate(X))) * N
        return wynik

    @staticmethod
    def dyskretna_transformacja_kosinusowa(x):
        N = len(x)
        X = np.zeros(N)
        for m in range(N):
            suma = 0
            for n in range(N):
                suma += x[n] * np.cos(np.pi * m * (2 * n + 1) / (2 * N))
            
            c = np.sqrt(1 / N) if m == 0 else np.sqrt(2 / N)
            X[m] = c * suma
        return X

    @staticmethod
    def szybka_transformacja_kosinusowa(x):
        N = len(x)
        v = np.zeros(N, dtype=x.dtype)
        for i in range(N // 2):
            v[i] = x[2 * i]
            v[N - 1 - i] = x[2 * i + 1]
            
        if N % 2 != 0:
            v[N // 2] = x[N - 1]
            
        V = np.fft.fft(v)
        X = np.zeros(N)
        for m in range(N):
            c = np.sqrt(1 / N) if m == 0 else np.sqrt(2 / N)
            X[m] = c * np.real(V[m] * np.exp(-1j * np.pi * m / (2 * N)))
            
        return X

    @staticmethod
    def transformacja_walsha_hadamarda(x):
        N = len(x)
        
        if (N & (N - 1)) != 0:
            raise ValueError("Długość wektora musi być potęgą liczby 2")
            
        def create_hadamard_matrix(n):
            if n == 1:
                return np.array([[1]])
            else:
                H = create_hadamard_matrix(n // 2)
                top = np.hstack((H, H))
                bottom = np.hstack((H, -H))
                return np.vstack((top, bottom))
                
        H_N = create_hadamard_matrix(N)
        return np.dot(H_N, x) / N

    @staticmethod
    def szybka_transformacja_walsha_hadamarda(x):
        N = len(x)
        if (N & (N - 1)) != 0:
            raise ValueError("Długość wektora musi być potęgą liczby 2")
            
        a = np.array(x, dtype=float)
        h = 1
        while h < N:
            for i in range(0, N, h * 2):
                for j in range(i, i + h):
                    x_j = a[j]
                    x_jh = a[j + h]
                    a[j] = x_j + x_jh
                    a[j + h] = x_j - x_jh
            h *= 2
            
        return a / N
