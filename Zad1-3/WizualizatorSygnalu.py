from GeneratorSygnalu import *
import matplotlib.pyplot as plt

class WizualizatorSygnalu:
    @staticmethod
    def _rysuj_wspolne(os_czasu, dane, os_czasowa, os_histogramu, liczba_przedzialow, etykieta, kolor, czy_dyskretny):
        if czy_dyskretny:
            os_czasowa.scatter(os_czasu, dane, s=2, color=kolor)
        else:
            os_czasowa.plot(os_czasu, dane, color=kolor, linewidth=1)
        os_czasowa.set_ylabel(etykieta)
        os_czasowa.grid(True, linestyle='--', color='gray', alpha=0.5)

        minimum_danych = np.min(dane)
        maksimum_danych = np.max(dane)

        if np.isclose(minimum_danych, maksimum_danych):
            os_histogramu.hist(dane, bins=1, color=kolor, edgecolor='white', alpha=0.7)
            os_histogramu.set_title(f"Histogram (wartość stała: {minimum_danych:.2f})")
        else:
            os_histogramu.hist(dane, bins=liczba_przedzialow, color=kolor, edgecolor='white', alpha=0.7)

        os_histogramu.set_ylabel("Częstość")

    @staticmethod
    def rysuj_wszystko(generator_sygnalu, liczba_probek, liczba_przedzialow, czy_dyskretny=False, tytul="Analiza Sygnału"):
        plt.style.use('dark_background')
        generator_sygnalu.resetuj()
        probki = np.array([next(generator_sygnalu) for _ in range(liczba_probek)])
        generator_sygnalu.resetuj()

        os_czasu = np.arange(liczba_probek) / generator_sygnalu.czestotliwosc_probkowania
        
        wykresy = []

        if not np.iscomplexobj(probki):
            # Sygnal Rzeczywisty
            wykres, (os_czasowa, os_histogramu) = plt.subplots(2, 1, figsize=(10, 8))
            wykres.patch.set_facecolor('#2b2b2b')
            wykres.suptitle(tytul)
            WizualizatorSygnalu._rysuj_wspolne(os_czasu, probki.real, os_czasowa, os_histogramu, liczba_przedzialow, "Amplituda", "cyan", czy_dyskretny)
            os_czasowa.set_title("Przebieg czasowy")
            os_histogramu.set_title("Histogram")
            wykres.tight_layout(rect=(0, 0.03, 1, 0.95))
            wykresy.append(("Sygnał Rzeczywisty", wykres))
        else:
            # Sygnal zespolony
            for typ_wykresu in ['rzecz_uroj', 'modul_faza']:
                wykres, osie = plt.subplots(2, 2, figsize=(12, 10))
                wykres.patch.set_facecolor('#2b2b2b')
                wykres.suptitle(f"{tytul} - {typ_wykresu.upper()}")

                if typ_wykresu == 'rzecz_uroj':
                    WizualizatorSygnalu._rysuj_wspolne(os_czasu, probki.real, osie[0, 0], osie[0, 1], liczba_przedzialow, "Część Rzeczywista", "cyan", czy_dyskretny)
                    WizualizatorSygnalu._rysuj_wspolne(os_czasu, probki.imag, osie[1, 0], osie[1, 1], liczba_przedzialow, "Część Urojona", "magenta", czy_dyskretny)
                    osie[0, 0].set_title("Część Rzeczywista (Real)")
                    osie[1, 0].set_title("Część Urojona (Imag)")
                    wykresy.append(("Rzeczywista/Urojona", wykres))
                else:
                    WizualizatorSygnalu._rysuj_wspolne(os_czasu, np.abs(probki), osie[0, 0], osie[0, 1], liczba_przedzialow, "Moduł", "lime", czy_dyskretny)
                    WizualizatorSygnalu._rysuj_wspolne(os_czasu, np.angle(probki), osie[1, 0], osie[1, 1], liczba_przedzialow, "Faza", "yellow", czy_dyskretny)
                    osie[0, 0].set_title("Moduł (Abs)")
                    osie[1, 0].set_title("Faza (Angle)")
                    wykresy.append(("Moduł/Faza", wykres))
                
                wykres.tight_layout(rect=(0, 0.03, 1, 0.95))

        return wykresy

    @staticmethod
    def rysuj_konwersje(czas_high, sygnal_oryg, sygnal_nowy, tryb, parametry_opis, liczba_przedzialow, f_sample=None, t_sample=None, x_sample=None):
        plt.style.use('dark_background')
        wykres, (os_czasowa, os_histogramu) = plt.subplots(2, 1, figsize=(10, 8))
        wykres.patch.set_facecolor('#2b2b2b')
        wykres.suptitle(f"{tryb} - {parametry_opis}")

        # Przebieg czasowy
        os_czasowa.plot(czas_high, sygnal_oryg, color='green', alpha=0.6, label='Oryginał', linewidth=1)
        os_czasowa.plot(czas_high, sygnal_nowy, color='cyan', label='Wynik Konwersji', linewidth=1.5)
        
        if f_sample and t_sample is not None and x_sample is not None:
            os_czasowa.scatter(t_sample, x_sample, color='red', s=15, label='Próbki', zorder=5)

        os_czasowa.set_title("Przebieg czasowy")
        os_czasowa.set_ylabel("Amplituda")
        os_czasowa.grid(True, linestyle='--', color='gray', alpha=0.5)
        os_czasowa.legend()

        # Histogram (korzystamy z wyniku konwersji jako glownego)
        dane = sygnal_nowy
        minimum_danych = np.min(dane)
        maksimum_danych = np.max(dane)

        if np.isclose(minimum_danych, maksimum_danych):
            os_histogramu.hist(dane, bins=1, color='cyan', edgecolor='white', alpha=0.7)
            os_histogramu.set_title(f"Histogram (wartość stała: {minimum_danych:.2f})")
        else:
            os_histogramu.hist(dane, bins=liczba_przedzialow, color='cyan', edgecolor='white', alpha=0.7)

        os_histogramu.set_ylabel("Częstość")
        os_histogramu.set_title("Histogram wyniku konwersji")
        
        wykres.tight_layout(rect=(0, 0.03, 1, 0.95))
        return [("Wyniki Konwersji", wykres)]
