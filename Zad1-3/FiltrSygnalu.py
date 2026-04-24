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
    def generuj_filtr_dolnoprzepustowy(M, K, okno='prostokatne'):
        h = np.zeros(M)
        srodek = (M - 1) / 2.0
        
        for i in range(M):
            if i == srodek:
                h[i] = 2.0 / K
            else:
                h[i] = np.sin(2 * np.pi * (i - srodek) / K) / (np.pi * (i - srodek))
                
        if okno == 'hamming':
            w = FiltrSygnalu.okno_hamminga(M)
        elif okno == 'hanning':
            w = FiltrSygnalu.okno_hanninga(M)
        elif okno == 'blackman':
            w = FiltrSygnalu.okno_blackmana(M)
        else:
            w = FiltrSygnalu.okno_prostokatne(M)
            
        return h * w

    @staticmethod
    def generuj_filtr_gornoprzepustowy(M, K, okno='prostokatne'):
        h_lp = FiltrSygnalu.generuj_filtr_dolnoprzepustowy(M, K, okno)
        n = np.arange(M)
        return h_lp * ((-1) ** n)

    @staticmethod
    def generuj_filtr_srodkowoprzepustowy(M, K, okno='prostokatne'):
        h_lp = FiltrSygnalu.generuj_filtr_dolnoprzepustowy(M, K, okno)
        n = np.arange(M)
        return h_lp * 2.0 * np.sin(np.pi * n / 2.0)

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
