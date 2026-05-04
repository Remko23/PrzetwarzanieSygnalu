import numpy as np
from FiltrSygnalu import FiltrSygnalu

class CzujnikOdleglosci:
    def __init__(self, dt_sim, v_ob, d0, c_osr, T_syg, fp, N_buf, T_rep, korelacja_typ="splot"):
        self.dt = dt_sim
        self.v_ob = v_ob
        self.d0 = d0
        self.c = c_osr
        self.T_syg = T_syg
        self.fp = fp
        self.N_buf = int(N_buf)
        self.T_rep = T_rep
        self.korelacja_typ = korelacja_typ
        
    def _sygnal_sondujacy(self, t):
        # Konfiguracja sygnału: suma trzech sinusów o różnych częstotliwościach
        # f1: częstotliwość podstawowa (1/T_syg)
        # f2: trzecia harmoniczna (3/T_syg) z amplitudą 0.4
        # f3: piąta harmoniczna (5/T_syg) z amplitudą 0.2
        f1 = 1.0 / self.T_syg
        f2 = 3.0 / self.T_syg
        f3 = 5.0 / self.T_syg
        return np.sin(2 * np.pi * f1 * t) + 0.4 * np.sin(2 * np.pi * f2 * t) + 0.2 * np.sin(2 * np.pi * f3 * t)

    def symuluj(self, czas_calkowity):
        czasy_raportu = []
        rzeczywiste_d = []
        zmierzone_d = []

        # Buforowanie
        buf_wyslany = np.zeros(self.N_buf)
        buf_odebrany = np.zeros(self.N_buf)

        liczba_krokow_sym = int(czas_calkowity / self.dt)
        dt_probk = 1.0 / self.fp
        
        czas_nastepnego_probkowania = 0.0
        czas_nastepnego_raportu = self.T_rep

        for k in range(liczba_krokow_sym):
            t = k * self.dt
            
            # Prawdziwa odległość w danym momencie (S = V * t + d0)
            d_t = self.d0 + self.v_ob * t
            
            # Sprawdzenie czy nadszedł czas próbkowania
            if t >= czas_nastepnego_probkowania:
                val_wys = self._sygnal_sondujacy(t)
                
                # Sygnał powracający jest opóźniony o czas lotu w obie strony: t_op = 2 * d(t) / c
                t_opoznienia = 2.0 * d_t / self.c
                t_wyslania = t - t_opoznienia
                
                if t_wyslania < 0:
                    val_od = 0.0
                else:
                    val_od = self._sygnal_sondujacy(t_wyslania)
                    
                buf_wyslany = np.roll(buf_wyslany, -1)
                buf_wyslany[-1] = val_wys
                
                buf_odebrany = np.roll(buf_odebrany, -1)
                buf_odebrany[-1] = val_od
                
                czas_nastepnego_probkowania += dt_probk
                
            # Sprawdzenie czy nadszedł czas analizy i raportowania odległości
            if t >= czas_nastepnego_raportu:
                # Korelacja dwóch zbuforowanych sygnałów.
                # Używamy zaimplementowanej metody korelacji.
                # Aby pik korelacji był po prawej stronie dla opóźnionego sygnału odebranego,
                # wywołujemy korelację z parametrami (sygnał_odebrany, sygnał_wysłany)
                if self.korelacja_typ == "bezposrednia":
                    korelacja = FiltrSygnalu.korelacja_bezposrednia(buf_odebrany, buf_wyslany)
                else:
                    korelacja = FiltrSygnalu.korelacja_z_uzyciem_splotu(buf_odebrany, buf_wyslany)
                
                # Wykres korelacji wzajemnej ma rozmiar 2*N_buf - 1
                # Środkowy indeks (odpowiadający opóźnieniu zerowemu) to N_buf - 1
                srodek = self.N_buf - 1
                
                # Bierzemy pod uwagę tylko prawa połówkę wykresu (t >= 0)
                prawa_polowa = korelacja[srodek:]
                
                # Znalezienie maksimum
                max_idx = np.argmax(prawa_polowa)
                
                # Przeliczenie indeksu na czas opóźnienia
                t_opoznienia_zmierzone = max_idx * dt_probk
                
                # Wyliczenie odległości na podstawie opóźnienia
                d_zmierzone = self.c * t_opoznienia_zmierzone / 2.0
                
                czasy_raportu.append(t)
                rzeczywiste_d.append(d_t)
                zmierzone_d.append(d_zmierzone)
                
                czas_nastepnego_raportu += self.T_rep
                
        return czasy_raportu, rzeczywiste_d, zmierzone_d, buf_wyslany, buf_odebrany, korelacja, t
