import numpy as np

class KonwerterSygnalu:

    @staticmethod
    def probkowanie_rownomierne(czas_high, sygnal_high, f_sample):
        # (S1) Próbkowanie równomierne.
        T_s = 1.0 / f_sample
        czas_poczatkowy = czas_high[0]
        dt = czas_high[1] - czas_high[0]
        
        czas_koncowy_okna = czas_poczatkowy + len(czas_high) * dt
        
        czas_sample = np.arange(czas_poczatkowy, czas_koncowy_okna + 1e-9, T_s)
        
        dt = czas_high[1] - czas_high[0]
        indices = np.round((czas_sample - czas_poczatkowy) / dt).astype(int)
        
        indices = np.clip(indices, 0, len(sygnal_high) - 1)
        
        sygnal_sample = sygnal_high[indices]
        return czas_sample, sygnal_sample

    @staticmethod
    def kwantyzacja_obcieciem(sygnal, bity):
        # (Q1) Kwantyzacja równomierna z obcięciem.
        L = 2 ** bity
        minimum = np.min(sygnal)
        maksimum = np.max(sygnal)
        
        if minimum == maksimum:
            return sygnal.copy()
            
        skalowany = (sygnal - minimum) / (maksimum - minimum) * (L - 1)
        # Obcięcie (floor) do najbliższej niższej liczby całkowitej
        poziomy = np.floor(skalowany)
        
        zrekonstruowany = (poziomy / (L - 1)) * (maksimum - minimum) + minimum
        return zrekonstruowany

    @staticmethod
    def kwantyzacja_zaokragleniem(sygnal, bity):
        # (Q2) Kwantyzacja równomierna z zaokrąglaniem.
        L = 2 ** bity
        minimum = np.min(sygnal)
        maksimum = np.max(sygnal)
        
        if minimum == maksimum:
            return sygnal.copy()
            
        skalowany = (sygnal - minimum) / (maksimum - minimum) * (L - 1)
        poziomy = np.round(skalowany)
        
        zrekonstruowany = (poziomy / (L - 1)) * (maksimum - minimum) + minimum
        return zrekonstruowany

    @staticmethod
    def rekonstrukcja_zoh(czas_sample, sygnal_sample, czas_high):
        # (R1) Ekstrapolacja zerowego rzędu.
        indices = np.searchsorted(czas_sample, czas_high, side='right') - 1
        indices = np.clip(indices, 0, len(sygnal_sample) - 1)
        return sygnal_sample[indices]

    @staticmethod
    def rekonstrukcja_foh(czas_sample, sygnal_sample, czas_high):
        # (R2) Interpolacja pierwszego rzędu.
        return np.interp(czas_high, czas_sample, sygnal_sample)

    @staticmethod
    def rekonstrukcja_sinc(czas_sample, sygnal_sample, czas_high, liczba_probek=50):
        # (R3) Rekonstrukcja w oparciu o funkcję sinc.
        T_s = czas_sample[1] - czas_sample[0] if len(czas_sample) > 1 else 1.0
        zrekonstruowany = np.zeros_like(czas_high)
        
        for i, t in enumerate(czas_high):
            idx_center = np.searchsorted(czas_sample, t)
            idx_start = max(0, idx_center - liczba_probek)
            idx_end = min(len(sygnal_sample), idx_center + liczba_probek)
            
            t_n = czas_sample[idx_start:idx_end]
            x_n = sygnal_sample[idx_start:idx_end]
            
            zrekonstruowany[i] = np.sum(x_n * np.sinc((t - t_n) / T_s))
            
        return zrekonstruowany

    @staticmethod
    def oblicz_mse(oryginalny, porownywany):
        # (C1) Błąd średniokwadratowy. MSE
        return np.mean((oryginalny - porownywany) ** 2)

    @staticmethod
    def oblicz_snr(oryginalny, porownywany):
        # (C2) Stosunek sygnał-szum. SNR
        mse = np.sum((oryginalny - porownywany) ** 2)
        if mse == 0:
            return float('inf')
        moc_sygnalu = np.sum(oryginalny ** 2)
        return 10 * np.log10(moc_sygnalu / mse)

    @staticmethod
    def oblicz_psnr(oryginalny, porownywany):
        # (C3) Szczytowy stosunek sygnał-szum. PSNR
        mse = KonwerterSygnalu.oblicz_mse(oryginalny, porownywany)
        if mse == 0:
            return float('inf')
        maksimum = np.max(oryginalny)

        if maksimum <= 0:
            maksimum = np.max(np.abs(oryginalny))
        return 10 * np.log10(maksimum / mse)

    @staticmethod
    def oblicz_md(oryginalny, porownywany):
        # (C4) Maksymalna różnica. MD
        return np.max(np.abs(oryginalny - porownywany))

    @staticmethod
    def oblicz_enob(snr):
        return (snr - 1.76) / 6.02
