import numpy as np

class FiltrSygnalu:
    @staticmethod
    def okno_prostokatne(M):
        return np.ones(M)

    @staticmethod
    def okno_hamminga(M):
        n = np.arange(M)
        return 0.53836 - 0.46164 * np.cos(2 * np.pi * n / M)

    @staticmethod
    def okno_hanninga(M):
        n = np.arange(M)
        return 0.5 - 0.5 * np.cos(2 * np.pi * n / M)

    @staticmethod
    def okno_blackmana(M):
        n = np.arange(M)
        return 0.42 - 0.5 * np.cos(2 * np.pi * n / M) + 0.08 * np.cos(4 * np.pi * n / M)

    @staticmethod
    def generuj_filtr_dolnoprzepustowy(M, K, okno='Hamming'):
        h = np.zeros(M)
        srodek = (M - 1) / 2.0
        
        for i in range(M):
            if i == srodek:
                h[i] = 2.0 / K
            else:
                h[i] = np.sin(2 * np.pi * (i - srodek) / K) / (np.pi * (i - srodek))
                
        if okno == 'Prostokątne':
            w = FiltrSygnalu.okno_prostokatne(M)
        elif okno == 'Hamming':
            w = FiltrSygnalu.okno_hamminga(M)
        elif okno == 'Hanning':
            w = FiltrSygnalu.okno_hanninga(M)
        elif okno == 'Blackman':
            w = FiltrSygnalu.okno_blackmana(M)
        else:
            w = FiltrSygnalu.okno_hamminga(M)
            
        return h * w

    @staticmethod
    def generuj_filtr_gornoprzepustowy(M, K, okno='Hamming'):
        h_lp = FiltrSygnalu.generuj_filtr_dolnoprzepustowy(M, K, okno)
        n = np.arange(M)
        return h_lp * ((-1) ** n)

    @staticmethod
    def splot(h, x):
        M = len(h)
        N = len(x)
        L = M + N - 1
        y = np.zeros(L)
        
        for n in range(L):
            suma = 0.0
            for k in range(M):
                if 0 <= n - k < N:
                    suma += h[k] * x[n - k]
            y[n] = suma
            
        return y

    @staticmethod
    def korelacja_bezposrednia(h, x):
        M = len(h)
        N = len(x)
        L = M + N - 1
        y = np.zeros(L)
        
        for n in range(L):
            # n to indeks w tablicy wyjsciowej (od 0 do L-1)
            # Przesuniecie 'm' odpowiada za relacje h(k) * x(k - m) lub podobne
            # Zgodnie z instrukcja R_hx = sum h(k) * x(n - k) gdzie R wyjsciowe przesuniete
            # Opracujmy wzor korelacji R_hx(m) = sum_k h(k)*x(k-m).
            # Jeśli R_hx(m) chcemy mieć w tablicy od indeksu 0.
            # R_hx(n) = sum_{k=0}^{M-1} h(k) * x(k + (N-1) - n) - żeby uzyskać poprawny splot z odwróconym x.
            suma = 0.0
            for k in range(M):
                idx_x = k + (N - 1) - n
                if 0 <= idx_x < N:
                    suma += h[k] * x[idx_x]
            y[n] = suma
            
        return y

    @staticmethod
    def korelacja_z_uzyciem_splotu(h, x):
        # Korelacja to splot h z odwróconym x
        x_odwr = x[::-1]
        return FiltrSygnalu.splot(h, x_odwr)

