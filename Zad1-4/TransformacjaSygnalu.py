import numpy as np

class TransformacjaSygnalu:

    @staticmethod
    def dft(x):
        N = len(x)
        m = np.arange(N)
        n = np.arange(N)
        # Tworzenie macierzy NxN gdzie kazdy element to m*n
        mn = m.reshape((N, 1)) * n
        # Exponenta, macierz bazowa Fouriera
        e = np.exp(-1j * 2 * np.pi * mn / N)
        # Obliczenie transformaty Fouriera przez mnożenie macierzy i dzielenie przez N (wg wzoru z instrukcji)
        X = np.dot(e, x) / N
        return X

    @staticmethod
    def fft_dit(x):
        # Szybka transformacja Fouriera z decymacją w czasie (DIT)
        x = np.asarray(x, dtype=complex)
        N = len(x)
        
        if N <= 1:
            return x
        
        # Sprawdzanie czy N to potęga 2
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
                            
        # Ostateczne skalowanie 1/N ze względu na wzór definicyjny z instrukcji
        return _fft_dit_rekurencyjnie(x) / N

    @staticmethod
    def fft_dif(x):
        # Szybka transformacja Fouriera z decymacją w częstotliwości (DIF)
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
    def dct_2(x):
        # Dyskretna Transformacja Kosinusowa typu II - z definicji
        N = len(x)
        X = np.zeros(N)
        for m in range(N):
            suma = 0
            for n in range(N):
                suma += x[n] * np.cos(np.pi * m * (2 * n + 1) / (2 * N))
            
            # Normalizacja
            c = np.sqrt(1 / N) if m == 0 else np.sqrt(2 / N)
            X[m] = c * suma
        return X

    @staticmethod
    def fct_2(x):
        # Szybka Transformacja Kosinusowa typu II przy użyciu FFT
        N = len(x)
        
        # 1. Przekształcenie wektora wejściowego w długość N
        v = np.zeros(N, dtype=x.dtype)
        for i in range(N // 2):
            v[i] = x[2 * i]
            v[N - 1 - i] = x[2 * i + 1]
            
        # Jesli N nieparzyste
        if N % 2 != 0:
            v[N // 2] = x[N - 1]
            
        # 2. Wykonanie FFT unscaled na przekształconym wektorze
        # Korzystamy z np.fft.fft, które jest unscaled
        V = np.fft.fft(v)
        
        # 3. Przemnożenie przez współczynniki i skalowanie
        X = np.zeros(N)
        for m in range(N):
            c = np.sqrt(1 / N) if m == 0 else np.sqrt(2 / N)
            # Re{ V(m) * e^{-j pi m / (2N)} }
            X[m] = c * np.real(V[m] * np.exp(-1j * np.pi * m / (2 * N)))
            
        return X

    @staticmethod
    def wht(x):
        # Transformacja Walsha-Hadamarda (rekurencyjna budowa macierzy i mnożenie)
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
        # Zwyczajowo niektórzy dzielą przez N lub sqrt(N). Przyjmijmy 1/N.
        return np.dot(H_N, x) / N

    @staticmethod
    def fwht(x):
        # Szybka transformacja Walsha-Hadamarda (w miejscu)
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
