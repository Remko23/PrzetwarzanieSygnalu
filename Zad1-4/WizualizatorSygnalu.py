from GeneratorSygnalu import *
import matplotlib.pyplot as plt

class WizualizatorSygnalu:
    @staticmethod
    def _rysuj_wspolne(os_czasu, dane, os_czasowa, os_histogramu, liczba_przedzialow, etykieta, kolor, czy_dyskretny, etykieta_x="", czy_widmo=False):
        if czy_widmo:
            markerline, stemlines, baseline = os_czasowa.stem(os_czasu, dane, basefmt=" ", markerfmt='o', linefmt=kolor)
            plt.setp(markerline, color=kolor, markersize=3)
            plt.setp(stemlines, color=kolor, linewidth=1, alpha=0.5)
        elif czy_dyskretny:
            os_czasowa.scatter(os_czasu, dane, s=2, color=kolor)
        else:
            os_czasowa.plot(os_czasu, dane, color=kolor, linewidth=1)
        os_czasowa.set_ylabel(etykieta)
        if etykieta_x:
            os_czasowa.set_xlabel(etykieta_x)
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
    def rysuj_wszystko(generator_sygnalu, liczba_probek, liczba_przedzialow, czy_dyskretny=False, czy_widmo=False, tytul="Analiza Sygnału"):
        plt.style.use('dark_background')
        generator_sygnalu.resetuj()
        probki = np.array([next(generator_sygnalu) for _ in range(liczba_probek)])
        generator_sygnalu.resetuj()

        if czy_widmo:
            os_x = np.arange(liczba_probek) * generator_sygnalu.czestotliwosc_probkowania / liczba_probek
            etykieta_x = "Częstotliwość (Hz)"
        else:
            os_x = np.arange(liczba_probek) / generator_sygnalu.czestotliwosc_probkowania
            etykieta_x = "Czas (s)"
        
        wykresy = []

        if not np.iscomplexobj(probki):
            # Sygnal Rzeczywisty
            wykres, (os_czasowa, os_histogramu) = plt.subplots(2, 1, figsize=(10, 8))
            wykres.patch.set_facecolor('#2b2b2b')
            wykres.suptitle(tytul)
            WizualizatorSygnalu._rysuj_wspolne(os_x, probki.real, os_czasowa, os_histogramu, liczba_przedzialow, "Amplituda", "cyan", czy_dyskretny, etykieta_x, czy_widmo)
            os_czasowa.set_title("Przebieg sygnału")
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
                    WizualizatorSygnalu._rysuj_wspolne(os_x, probki.real, osie[0, 0], osie[0, 1], liczba_przedzialow, "Część Rzeczywista", "cyan", czy_dyskretny, etykieta_x, czy_widmo)
                    WizualizatorSygnalu._rysuj_wspolne(os_x, probki.imag, osie[1, 0], osie[1, 1], liczba_przedzialow, "Część Urojona", "magenta", czy_dyskretny, etykieta_x, czy_widmo)
                    osie[0, 0].set_title("Część Rzeczywista (Real)")
                    osie[1, 0].set_title("Część Urojona (Imag)")
                    wykresy.append(("Rzeczywista/Urojona", wykres))
                else:
                    WizualizatorSygnalu._rysuj_wspolne(os_x, np.abs(probki), osie[0, 0], osie[0, 1], liczba_przedzialow, "Moduł", "lime", czy_dyskretny, etykieta_x, czy_widmo)
                    WizualizatorSygnalu._rysuj_wspolne(os_x, np.angle(probki), osie[1, 0], osie[1, 1], liczba_przedzialow, "Faza", "yellow", czy_dyskretny, etykieta_x, czy_widmo)
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

        os_czasowa.plot(czas_high, sygnal_oryg, color='red', alpha=0.8, label='Oryginał', linewidth=1.5)
        os_czasowa.plot(czas_high, sygnal_nowy, color='cyan', label='Wynik Konwersji', linewidth=1.5)
        
        if f_sample and t_sample is not None and x_sample is not None:
            os_czasowa.scatter(t_sample, x_sample, color='red', s=15, label='Próbki', zorder=5)

        os_czasowa.set_title("Przebieg czasowy")
        os_czasowa.set_ylabel("Amplituda")
        os_czasowa.grid(True, linestyle='--', color='gray', alpha=0.5)
        os_czasowa.legend()

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

    @staticmethod
    def rysuj_korelacje(t_a, sig_a, t_b, sig_b, lags, korelacja, metoda_opis):
        plt.style.use('dark_background')
        
        wykres, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
        wykres.patch.set_facecolor('#2b2b2b')
        wykres.suptitle(f"Wynik korelacji wzajemnej ({metoda_opis})")
        
        if np.iscomplexobj(sig_a):
            ax1.plot(t_a, sig_a.real, color='cyan', label='Real(A)', linewidth=1.5)
            ax1.plot(t_a, sig_a.imag, color='magenta', label='Imag(A)', linewidth=1.5, alpha=0.7)
            ax1.legend(loc='upper right', facecolor='#2b2b2b', labelcolor='white')
        else:
            ax1.plot(t_a, sig_a, color='cyan', linewidth=1.5)
        ax1.set_title("Sygnał A")
        ax1.set_ylabel("Amplituda")
        
        if np.iscomplexobj(sig_b):
            ax2.plot(t_b, sig_b.real, color='yellow', label='Real(B)', linewidth=1.5)
            ax2.plot(t_b, sig_b.imag, color='orange', label='Imag(B)', linewidth=1.5, alpha=0.7)
            ax2.legend(loc='upper right', facecolor='#2b2b2b', labelcolor='white')
        else:
            ax2.plot(t_b, sig_b, color='yellow', linewidth=1.5)
        ax2.set_title("Sygnał B")
        ax2.set_ylabel("Amplituda")
        
        if np.iscomplexobj(korelacja):
            ax3.plot(lags, korelacja.real, color='lime', marker='o', markersize=2, label='Real(R_AB)', linewidth=1)
            ax3.plot(lags, korelacja.imag, color='magenta', marker='x', markersize=2, label='Imag(R_AB)', linewidth=1, alpha=0.7)
            ax3.legend(loc='upper right', facecolor='#2b2b2b', labelcolor='white')
        else:
            ax3.plot(lags, korelacja, color='lime', marker='o', markersize=2, linewidth=1)
            
        ax3.set_title("Korelacja wzajemna R_AB(n)")
        ax3.set_xlabel("Przesunięcie n (próbki)")
        ax3.set_ylabel("Wartość")
        
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor('#2b2b2b')
            ax.tick_params(colors='white')
            ax.grid(True, linestyle='--', color='gray', alpha=0.5)
            for spine in ax.spines.values():
                spine.set_color('gray')
                
        wykres.tight_layout(rect=(0, 0.03, 1, 0.95))
        return [("Wyniki Korelacji", wykres)]

