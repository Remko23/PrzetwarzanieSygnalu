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
        # suma trzech sygnalow sinusowych
        f1 = 1.0 / self.T_syg
        f2 = 3.0 / self.T_syg
        f3 = 5.0 / self.T_syg
        return np.sin(2 * np.pi * f1 * t) + 0.4 * np.sin(2 * np.pi * f2 * t) + 0.2 * np.sin(2 * np.pi * f3 * t)

    def symuluj(self, czas_calkowity):
        czasy_raportu = []
        rzeczywiste_d = []
        zmierzone_d = []

        buf_wyslany = np.zeros(self.N_buf)
        buf_odebrany = np.zeros(self.N_buf)

        liczba_krokow_sym = int(czas_calkowity / self.dt)
        dt_probk = 1.0 / self.fp
        
        czas_nastepnego_probkowania = 0.0
        czas_nastepnego_raportu = self.T_rep

        for k in range(liczba_krokow_sym):
            t = k * self.dt
            d_t = self.d0 + self.v_ob * t

            if t >= czas_nastepnego_probkowania:
                val_wys = self._sygnal_sondujacy(t)
                t_opoznienia = 2.0 * d_t / self.c
                t_wyslania = t - t_opoznienia
                
                if t_wyslania < 0:
                    val_od = np.random.normal(0, 0.5)
                else:
                    val_od = self._sygnal_sondujacy(t_wyslania) + np.random.normal(0, 0.5)
                    
                buf_wyslany = np.roll(buf_wyslany, -1)
                buf_wyslany[-1] = val_wys
                
                buf_odebrany = np.roll(buf_odebrany, -1)
                buf_odebrany[-1] = val_od
                
                czas_nastepnego_probkowania += dt_probk

            if t >= czas_nastepnego_raportu:
                if self.korelacja_typ == "bezposrednia":
                    korelacja = FiltrSygnalu.korelacja_bezposrednia(buf_odebrany, buf_wyslany)
                else:
                    korelacja = FiltrSygnalu.korelacja_z_uzyciem_splotu(buf_odebrany, buf_wyslany)

                srodek = self.N_buf - 1
                prawa_polowa = korelacja[srodek:]
                
                import scipy.signal
                peaks, _ = scipy.signal.find_peaks(prawa_polowa)
                if len(peaks) > 0:
                    najwyzszy_pik_idx = np.argmax(prawa_polowa[peaks])
                    max_idx = peaks[najwyzszy_pik_idx]
                else:
                    max_idx = np.argmax(prawa_polowa)

                t_opoznienia_zmierzone = max_idx * dt_probk
                d_zmierzone = self.c * t_opoznienia_zmierzone / 2.0
                
                czasy_raportu.append(t)
                rzeczywiste_d.append(d_t)
                zmierzone_d.append(d_zmierzone)
                
                czas_nastepnego_raportu += self.T_rep
                
        return czasy_raportu, rzeczywiste_d, zmierzone_d, buf_wyslany, buf_odebrany, korelacja, t
