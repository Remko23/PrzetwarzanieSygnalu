import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from GeneratorSygnalu import GeneratorSygnalu
from PlikSygnalu import PlikSygnalu
from WizualizatorSygnalu import WizualizatorSygnalu
from KonwerterSygnalu import KonwerterSygnalu
from FiltrSygnalu import FiltrSygnalu
from CzujnikOdleglosci import CzujnikOdleglosci
from TransformacjaSygnalu import TransformacjaSygnalu
import time
import scipy.fft as sp_fft
import scipy.linalg as sp_linalg
import matplotlib.pyplot as plt

class Aplikacja(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generator i Analizator Sygnałów")
        self.geometry("1800x800")

        self.zastosuj_ciemny_motyw()

        self.sygnal_glowny = None
        self.ostatnia_transformata = None
        self.czy_dyskretny = False
        self.czy_widmo = False

        self.typy_sygnalow = {
            "s1": "Szum o rozkładzie jednostajnym (s1)",
            "s2": "Szum gaussowski (s2)",
            "s3": "Sygnał sinusoidalny (s3)",
            "s4": "Sygnał sinusoidalny wyprostowany jednopołówkowo (s4)",
            "s5": "Sygnał sinusoidalny wyprostowany dwupołówkowo (s5)",
            "s6": "Sygnał prostokątny (s6)",
            "s7": "Sygnał prostokątny symetryczny (s7)",
            "s8": "Sygnał trójkątny (s8)",
            "s9": "Skok jednostkowy (s9)",
            "s10": "Impuls jednostkowy (s10)",
            "s11": "Szum impulsowy (s11)",
            "s12": "Sygnał zespolony (s12)",
            "s13": "Sygnał złożony S1 (s13)",
            "s14": "Sygnał złożony S2 (s14)",
            "s15": "Sygnał złożony S3 (s15)"
        }

        self.kody_sygnalow = {v: k for k, v in self.typy_sygnalow.items()}
        self.pola_parametrow_a = {}
        self.pola_parametrow_b = {}
        self.uzyj_glownego_jako_a = tk.BooleanVar(value=False)
        self.uzyj_glownego_trans = tk.BooleanVar(value=True)
        self.pola_parametrow_trans = {}

        self.utworz_widzety()

    def zastosuj_ciemny_motyw(self):
        self.configure(bg="#2b2b2b")

        styl = ttk.Style(self)
        try:
            styl.theme_use("clam")
        except:
            pass

        kolor_tla = "#2b2b2b"
        kolor_tekstu = "#e0e0e0"
        tlo_przycisku = "#3c3f41"
        aktywny_przycisk = "#4b4e50"
        tlo_pola_tekstowego = "#3c3f41"
        tekst_pola_tekstowego = "#ffffff"

        styl.configure("TFrame", background=kolor_tla)
        styl.configure("TLabel", background=kolor_tla, foreground=kolor_tekstu)
        styl.configure("TLabelframe", background=kolor_tla, foreground=kolor_tekstu)
        styl.configure("TLabelframe.Label", background=kolor_tla, foreground=kolor_tekstu, font=("Arial", 10, "bold"))

        styl.configure("TButton",
                       background=tlo_przycisku, foreground=kolor_tekstu,
                       borderwidth=1, focusthickness=3, focuscolor='none')
        styl.map("TButton",
                 background=[("active", aktywny_przycisk), ("pressed", "#5a5d5f")])

        styl.configure("TCombobox",
                       fieldbackground=tlo_pola_tekstowego, background=tlo_przycisku, foreground=tekst_pola_tekstowego,
                       arrowcolor=kolor_tekstu)
        styl.configure("TEntry", fieldbackground=tlo_pola_tekstowego, foreground=tekst_pola_tekstowego)

        styl.configure("TPanedwindow", background=kolor_tla)
        styl.configure("TNotebook", background=kolor_tla, borderwidth=0)
        styl.configure("TNotebook.Tab", background=tlo_przycisku, foreground=kolor_tekstu, padding=[5, 2])
        styl.map("TNotebook.Tab",
                 background=[("selected", "#505050")],
                 expand=[("selected", [1, 1, 1, 0])])

        styl.configure("TCheckbutton",
                       background=kolor_tla,
                       foreground=kolor_tekstu,
                       focuscolor="none",
                       font=("Arial", 10))
        styl.map("TCheckbutton",
                 background=[("disabled", kolor_tla), ("active", kolor_tla)],
                 foreground=[("disabled", "#777777"), ("active", "#ffffff")],
                 indicatorcolor=[("selected", "#4fc3f7"), ("!selected", tlo_pola_tekstowego)],
                 indicatorbackground=[("selected", tlo_pola_tekstowego), ("!selected", tlo_pola_tekstowego)],
                 lightcolor=[("selected", "#4fc3f7"), ("!selected", "#555555")],
                 darkcolor=[("selected", "#0091ea"), ("!selected", "#111111")],
                 bordercolor=[("selected", "#4fc3f7"), ("!selected", "#555555")])

    def utworz_widzety(self):
        panel_podzielony = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        panel_podzielony.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        lewa_ramka = ttk.Frame(panel_podzielony)
        panel_podzielony.add(lewa_ramka, weight=1)

        prawa_ramka = ttk.Frame(panel_podzielony)
        panel_podzielony.add(prawa_ramka, weight=6)

        self.notatnik_wizualizacji = ttk.Notebook(prawa_ramka)
        self.notatnik_wizualizacji.pack(fill=tk.BOTH, expand=True)

        self.zakladki_lewe = ttk.Notebook(lewa_ramka)
        self.zakladki_lewe.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        zakladka_generacja = ttk.Frame(self.zakladki_lewe)
        self.zakladki_lewe.add(zakladka_generacja, text="Generowanie sygnału")
        
        zakladka_konwersja = ttk.Frame(self.zakladki_lewe)
        self.zakladki_lewe.add(zakladka_konwersja, text="Kwantyzacja i rekonstrukcja")
        
        zakladka_filtracja = ttk.Frame(self.zakladki_lewe)
        self.zakladki_lewe.add(zakladka_filtracja, text="Filtrowanie")

        zakladka_odleglosc = ttk.Frame(self.zakladki_lewe)
        self.zakladki_lewe.add(zakladka_odleglosc, text="Pomiar odległości")

        zakladka_korelacja = ttk.Frame(self.zakladki_lewe)
        self.zakladki_lewe.add(zakladka_korelacja, text="Korelacja")

        zakladka_transformacje = ttk.Frame(self.zakladki_lewe)
        self.zakladki_lewe.add(zakladka_transformacje, text="Transformacje")

        ramka_trans_sygnal = ttk.LabelFrame(zakladka_transformacje, text="Sygnał wejściowy do transformacji", padding="10")
        ramka_trans_sygnal.pack(fill=tk.X, pady=5)
        
        self.chk_uzyj_glownego_trans = ttk.Checkbutton(ramka_trans_sygnal, text="Użyj Sygnału Głównego z lewego panelu", 
                                                 variable=self.uzyj_glownego_trans, 
                                                 command=self.przelacz_uzycie_glownego_trans)
        self.chk_uzyj_glownego_trans.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(ramka_trans_sygnal, text="Wybierz sygnał:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wybor_sygnalu_trans = ttk.Combobox(ramka_trans_sygnal, values=list(self.typy_sygnalow.values()),
                                            state="disabled", width=38)
        self.wybor_sygnalu_trans.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.wybor_sygnalu_trans.bind("<<ComboboxSelected>>", self.przy_wyborze_sygnalu_trans)

        self.ramka_parametrow_trans = ttk.Frame(ramka_trans_sygnal)
        self.ramka_parametrow_trans.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        ramka_trans = ttk.LabelFrame(zakladka_transformacje, text="Operacje transformacji", padding="10")
        ramka_trans.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_trans, text="Wybierz transformację:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.wybor_transformacji = ttk.Combobox(ramka_trans, values=[
            "Transformacja Fouriera (DFT)",
            "Szybka Transformacja Fouriera (FFT)",
            "Transformacja Kosinusowa (DCT)",
            "Szybka Transformacja Kosinusowa (FCT)",
            "Transformacja Walsha-Hadamarda (WHT)",
            "Szybka Transformacja Walsha-Hadamarda (FWHT)"
        ], state="readonly", width=40)
        self.wybor_transformacji.current(0)
        self.wybor_transformacji.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.wybor_transformacji.bind("<<ComboboxSelected>>", self.aktualizuj_stan_decymacji)

        self.label_dziedzina = ttk.Label(ramka_trans, text="Dziedzina decymacji:")
        self.wybor_dziedziny = ttk.Combobox(ramka_trans, values=[
            "W dziedzinie czasu (DIT)",
            "W dziedzinie częstotliwości (DIF)"
        ], state="readonly", width=40)
        self.wybor_dziedziny.current(0)


        ttk.Label(ramka_trans, text="Wybierz implementację:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.wybor_implementacji = ttk.Combobox(ramka_trans, values=[
            "Własna implementacja",
            "Biblioteka gotowa (Scipy)"
        ], state="readonly", width=40)
        self.wybor_implementacji.current(0)
        self.wybor_implementacji.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.przycisk_transformuj = ttk.Button(ramka_trans, text="Wykonaj transformację i porównaj", command=self.wykonaj_transformacje)
        self.przycisk_transformuj.grid(row=3, column=0, pady=10, sticky=tk.E, padx=5)

        self.przycisk_benchmark = ttk.Button(ramka_trans, text="Benchmark (czas N=512..8192)", command=self.wykonaj_benchmark)
        self.przycisk_benchmark.grid(row=3, column=1, pady=10, sticky=tk.W, padx=5)

        ramka_a = ttk.LabelFrame(zakladka_korelacja, text="Sygnał A", padding="10")
        ramka_a.pack(fill=tk.X, pady=5)

        self.chk_uzyj_glownego = ttk.Checkbutton(ramka_a, text="Użyj Sygnału Głównego jako A", 
                                                 variable=self.uzyj_glownego_jako_a, 
                                                 command=self.przelacz_uzycie_glownego_a)
        self.chk_uzyj_glownego.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        self.label_sygnal_a = ttk.Label(ramka_a, text="Sygnał A:")
        self.label_sygnal_a.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wybor_sygnalu_a = ttk.Combobox(ramka_a, values=list(self.typy_sygnalow.values()),
                                            state="readonly", width=38)
        self.wybor_sygnalu_a.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.wybor_sygnalu_a.bind("<<ComboboxSelected>>", self.przy_wyborze_sygnalu_a)

        self.ramka_parametrow_a = ttk.Frame(ramka_a)
        self.ramka_parametrow_a.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(ramka_a, text="Próbek N_A:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.pole_liczba_probek_a = ttk.Entry(ramka_a, width=10)
        self.pole_liczba_probek_a.insert(0, "1000")
        self.pole_liczba_probek_a.grid(row=3, column=1, sticky=tk.W, pady=2)

        ramka_b = ttk.LabelFrame(zakladka_korelacja, text="Sygnał B", padding="10")
        ramka_b.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_b, text="Sygnał B:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.wybor_sygnalu_b = ttk.Combobox(ramka_b, values=list(self.typy_sygnalow.values()),
                                            state="readonly", width=38)
        self.wybor_sygnalu_b.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.wybor_sygnalu_b.bind("<<ComboboxSelected>>", self.przy_wyborze_sygnalu_b)

        self.ramka_parametrow_b = ttk.Frame(ramka_b)
        self.ramka_parametrow_b.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(ramka_b, text="Próbek N_B:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.pole_liczba_probek_b = ttk.Entry(ramka_b, width=10)
        self.pole_liczba_probek_b.insert(0, "1000")
        self.pole_liczba_probek_b.grid(row=2, column=1, sticky=tk.W, pady=2)

        ramka_param_kor = ttk.LabelFrame(zakladka_korelacja, text="Parametry korelacji", padding="10")
        ramka_param_kor.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_param_kor, text="Częst. próbkowania fp (Hz):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pole_fp_korelacji = ttk.Entry(ramka_param_kor, width=10)
        self.pole_fp_korelacji.insert(0, "1000.0")
        self.pole_fp_korelacji.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(ramka_param_kor, text="Metoda korelacji:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wybor_algorytmu_korelacji = ttk.Combobox(ramka_param_kor, values=["Bezpośrednia", "Z użyciem splotu"],
                                                      state="readonly", width=18)
        self.wybor_algorytmu_korelacji.current(0)
        self.wybor_algorytmu_korelacji.grid(row=1, column=1, sticky=tk.W, pady=2)

        self.przycisk_koreluj = ttk.Button(zakladka_korelacja, text="Oblicz i Wizualizuj Korelację", command=self.oblicz_korelacje)
        self.przycisk_koreluj.pack(pady=10)

        ramka_generacji_1 = ttk.LabelFrame(zakladka_generacja, text="Generacja Sygnału Głównego", padding="10")
        ramka_generacji_1.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_generacji_1, text="Wybierz sygnał:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.wybor_sygnalu_1 = ttk.Combobox(ramka_generacji_1, values=list(self.typy_sygnalow.values()),
                                            state="readonly", width=38)
        self.wybor_sygnalu_1.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.wybor_sygnalu_1.bind("<<ComboboxSelected>>", self.przy_wyborze_sygnalu_1)

        self.ramka_parametrow_1 = ttk.Frame(ramka_generacji_1)
        self.ramka_parametrow_1.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.pola_parametrow_1 = {}

        self.przycisk_generacji_1 = ttk.Button(ramka_generacji_1, text="Generuj Sygnał Główny",
                                               command=self.generuj_sygnal_glowny)
        self.przycisk_generacji_1.grid(row=2, column=0, columnspan=2, pady=10)

        ramka_operacji = ttk.LabelFrame(zakladka_generacja, text="Operacje Matematyczne (Opcjonalne)", padding="10")
        ramka_operacji.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_operacji, text="Wybierz operację:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.wybor_operacji = ttk.Combobox(ramka_operacji, values=["Dodawanie", "Odejmowanie", "Mnożenie", "Dzielenie"],
                                           state="readonly", width=20)
        self.wybor_operacji.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(ramka_operacji, text="Wybierz sygnał 2:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wybor_sygnalu_2 = ttk.Combobox(ramka_operacji, values=list(self.typy_sygnalow.values()), state="readonly",
                                            width=38)
        self.wybor_sygnalu_2.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.wybor_sygnalu_2.bind("<<ComboboxSelected>>", self.przy_wyborze_sygnalu_2)

        self.ramka_parametrow_2 = ttk.Frame(ramka_operacji)
        self.ramka_parametrow_2.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.pola_parametrow_2 = {}

        self.przycisk_operacji = ttk.Button(ramka_operacji, text="Wykonaj Operację na Głównym Sygnale",
                                            command=self.wykonaj_operacje)
        self.przycisk_operacji.grid(row=3, column=0, columnspan=2, pady=10)

        ramka_konwersji = ttk.LabelFrame(zakladka_konwersja, text="Próbkowanie i Kwantyzacja (A/C i C/A)", padding="10")
        ramka_konwersji.pack(fill=tk.X, pady=5)
        
        ttk.Label(ramka_konwersji, text="Tryb:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.wybor_trybu_konwersji = ttk.Combobox(ramka_konwersji, values=["Próbkowanie i Rekonstrukcja", "Kwantyzacja"], state="readonly", width=28)
        self.wybor_trybu_konwersji.current(0)
        self.wybor_trybu_konwersji.grid(row=0, column=1, sticky=tk.W, pady=2, columnspan=3)
        self.wybor_trybu_konwersji.bind("<<ComboboxSelected>>", self.aktualizuj_interfejs_konwersji)
        
        self.ramka_param_konwersji = ttk.Frame(ramka_konwersji)
        self.ramka_param_konwersji.grid(row=1, column=0, columnspan=4, pady=5, sticky=tk.W)
        
        self.przycisk_wykonaj_konwersje = ttk.Button(ramka_konwersji, text="Wykonaj Konwersję", command=self.wykonaj_konwersje)
        self.przycisk_wykonaj_konwersje.grid(row=2, column=0, columnspan=4, pady=5)
        self.aktualizuj_interfejs_konwersji()

        ramka_filtracji = ttk.LabelFrame(zakladka_filtracja, text="Filtracja Sygnału", padding="10")
        ramka_filtracji.pack(fill=tk.X, pady=5)
        
        ttk.Label(ramka_filtracji, text="Rodzaj filtru:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.wybor_filtru = ttk.Combobox(ramka_filtracji, values=["Dolnoprzepustowy", "Górnoprzepustowy"], state="readonly", width=20)
        self.wybor_filtru.current(0)
        self.wybor_filtru.grid(row=0, column=1, sticky=tk.W, pady=2, columnspan=3)

        ttk.Label(ramka_filtracji, text="Okno:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wybor_okna = ttk.Combobox(ramka_filtracji, values=["Prostokątne", "Hamming", "Hanning", "Blackman"], state="readonly", width=20)
        self.wybor_okna.current(0)
        self.wybor_okna.grid(row=1, column=1, sticky=tk.W, pady=2, columnspan=3)

        ttk.Label(ramka_filtracji, text="M (rząd filtru):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.pole_m = ttk.Entry(ramka_filtracji, width=8)
        self.pole_m.insert(0, "63")
        self.pole_m.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(ramka_filtracji, text="fo (częst. odcięcia):").grid(row=2, column=2, sticky=tk.W, pady=2)
        self.pole_fo = ttk.Entry(ramka_filtracji, width=8)
        self.pole_fo.insert(0, "10")
        self.pole_fo.grid(row=2, column=3, sticky=tk.W, pady=2)

        self.przycisk_filtruj = ttk.Button(ramka_filtracji, text="Filtruj Główny Sygnał", command=self.filtruj_sygnal)
        self.przycisk_filtruj.grid(row=3, column=0, columnspan=4, pady=5)

        ramka_srodowisko = ttk.LabelFrame(zakladka_odleglosc, text="Parametry środowiska i obiektu", padding="10")
        ramka_srodowisko.pack(fill=tk.X, pady=5)
        
        ttk.Label(ramka_srodowisko, text="Krok czasu sym. dt:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pole_dt_sim = ttk.Entry(ramka_srodowisko, width=10)
        self.pole_dt_sim.insert(0, "0.001")
        self.pole_dt_sim.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(ramka_srodowisko, text="Prędkość obiektu v:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.pole_v_ob = ttk.Entry(ramka_srodowisko, width=10)
        self.pole_v_ob.insert(0, "0.0")
        self.pole_v_ob.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(ramka_srodowisko, text="Pocz. odległość d0:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.pole_d0 = ttk.Entry(ramka_srodowisko, width=10)
        self.pole_d0.insert(0, "100.0")
        self.pole_d0.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(ramka_srodowisko, text="Prędkość sygnału c:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.pole_c_osr = ttk.Entry(ramka_srodowisko, width=10)
        self.pole_c_osr.insert(0, "300.0")
        self.pole_c_osr.grid(row=3, column=1, sticky=tk.W, pady=2)

        ramka_radar = ttk.LabelFrame(zakladka_odleglosc, text="Parametry radaru (czujnika)", padding="10")
        ramka_radar.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_radar, text="Okres syg. sond. T:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pole_T_syg = ttk.Entry(ramka_radar, width=10)
        self.pole_T_syg.insert(0, "1.0")
        self.pole_T_syg.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(ramka_radar, text="Częst. próbkowania fp:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.pole_fp_rad = ttk.Entry(ramka_radar, width=10)
        self.pole_fp_rad.insert(0, "1000.0")
        self.pole_fp_rad.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(ramka_radar, text="Długość bufora N:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.pole_N_buf = ttk.Entry(ramka_radar, width=10)
        self.pole_N_buf.insert(0, "2000")
        self.pole_N_buf.grid(row=2, column=1, sticky=tk.W, pady=2)

        ttk.Label(ramka_radar, text="Okres raportowania:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.pole_T_rep = ttk.Entry(ramka_radar, width=10)
        self.pole_T_rep.insert(0, "0.5")
        self.pole_T_rep.grid(row=3, column=1, sticky=tk.W, pady=2)

        ttk.Label(ramka_radar, text="Metoda korelacji:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.wybor_korelacji = ttk.Combobox(ramka_radar, values=["splot", "bezposrednia"], state="readonly", width=12)
        self.wybor_korelacji.current(0)
        self.wybor_korelacji.grid(row=4, column=1, sticky=tk.W, pady=2)

        ramka_symulacja = ttk.Frame(zakladka_odleglosc)
        ramka_symulacja.pack(fill=tk.X, pady=10)
        
        ttk.Label(ramka_symulacja, text="Czas całk. symulacji:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pole_czas_calk = ttk.Entry(ramka_symulacja, width=10)
        self.pole_czas_calk.insert(0, "5.0")
        self.pole_czas_calk.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        self.przycisk_symuluj_odleglosc = ttk.Button(ramka_symulacja, text="Symuluj Pomiar", command=self.symuluj_odleglosc)
        self.przycisk_symuluj_odleglosc.grid(row=1, column=0, columnspan=2, pady=10)

        ramka_akcji = ttk.LabelFrame(lewa_ramka, text="Akcje na Głównym Sygnale i Logi", padding="10")
        ramka_akcji.pack(fill=tk.X, pady=5)

        ramka_przyciskow_akcji = ttk.Frame(ramka_akcji)
        ramka_przyciskow_akcji.pack(fill=tk.X, pady=5)

        ttk.Button(ramka_przyciskow_akcji, text="Zapisz do pliku", command=self.zapisz_sygnal).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Button(ramka_przyciskow_akcji, text="Wczytaj z pliku", command=self.wczytaj_sygnal).pack(side=tk.LEFT,
                                                                                                     padx=5)

        ramka_parametrow_globalnych = ttk.Frame(ramka_akcji)
        ramka_parametrow_globalnych.pack(fill=tk.X, pady=5)

        ttk.Label(ramka_parametrow_globalnych, text="Liczba próbek w oknie:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.pole_liczba_probek = ttk.Entry(ramka_parametrow_globalnych, width=10)
        self.pole_liczba_probek.insert(0, "1024")
        self.pole_liczba_probek.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(ramka_parametrow_globalnych, text="Przedziały histogramu:").grid(row=1, column=0, sticky=tk.W, padx=5,
                                                                                   pady=5)
        self.pole_liczba_przedzialow = ttk.Entry(ramka_parametrow_globalnych, width=10)
        self.pole_liczba_przedzialow.insert(0, "20")
        self.pole_liczba_przedzialow.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(ramka_parametrow_globalnych, text="Częstotliwość próbk. (Hz):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.pole_czestotliwosc_probkowania = ttk.Entry(ramka_parametrow_globalnych, width=10)
        self.pole_czestotliwosc_probkowania.insert(0, "1000.0")
        self.pole_czestotliwosc_probkowania.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Button(ramka_parametrow_globalnych, text="Wizualizuj (Wykres + Histogram)",
                   command=self.wizualizuj_sygnal).grid(row=3, column=0, columnspan=2, pady=10)

        self.pole_tekstowe_logow = tk.Text(ramka_akcji, height=10, state=tk.DISABLED, bg="#3c3f41", fg="#e0e0e0",
                                           insertbackground="#ffffff")
        self.pole_tekstowe_logow.pack(fill=tk.BOTH, expand=True, pady=5)

    def loguj_wiadomosc(self, wiadomosc):
        self.pole_tekstowe_logow.config(state=tk.NORMAL)
        self.pole_tekstowe_logow.insert(tk.END, wiadomosc + "\n")
        self.pole_tekstowe_logow.see(tk.END)
        self.pole_tekstowe_logow.config(state=tk.DISABLED)

    def aktualizuj_stan_decymacji(self, event=None):
        if self.wybor_transformacji.get() == "Szybka Transformacja Fouriera (FFT)":
            self.label_dziedzina.grid(row=1, column=0, sticky=tk.W, pady=5)
            self.wybor_dziedziny.grid(row=1, column=1, sticky=tk.W, pady=5)
        else:
            self.label_dziedzina.grid_remove()
            self.wybor_dziedziny.grid_remove()

    def _zbuduj_interfejs_parametrow(self, ramka_rodzica, slownik_parametrow, kod_sygnalu):
        for widzet in ramka_rodzica.winfo_children():
            widzet.destroy()
        slownik_parametrow.clear()

        if not kod_sygnalu: return

        wymagane_parametry = [('amplituda', 'Amplituda', '1.0')]

        if kod_sygnalu not in ["s10", "s11"]:
            wymagane_parametry.extend([
                ('czas_poczatkowy', 'Czas początkowy', '0.0'),
                ('czas_trwania', 'Czas trwania', '1.024')
            ])
            if kod_sygnalu in ["s3", "s4", "s5", "s6", "s7", "s8", "s12"]:
                wymagane_parametry.append(('okres', 'Okres', '1.0'))
            if kod_sygnalu in ["s6", "s7", "s8"]:
                wymagane_parametry.append(('wspolczynnik_wypelnienia', 'Wsp. wypełnienia', '0.5'))
            if kod_sygnalu == "s9":
                wymagane_parametry.append(('czas_skoku', 'Czas skoku', '0.5'))
        else:
            if kod_sygnalu == "s10":
                wymagane_parametry.append(('numer_probki_skoku', 'Numer próbki skoku', '100'))
            if kod_sygnalu == "s11":
                wymagane_parametry.append(('prawdopodobienstwo', 'Prawd. skoku', '0.1'))

        wymagane_parametry.append(('przesuniecie_probek', 'Przesunięcie (próbki)', '0'))

        for i, (klucz_parametru, etykieta_parametru, wartosc_domyslna) in enumerate(wymagane_parametry):
            ttk.Label(ramka_rodzica, text=etykieta_parametru + ":").grid(row=i // 4, column=(i % 4) * 2, padx=2, pady=2,
                                                                         sticky=tk.E)
            pole_wprowadzania = ttk.Entry(ramka_rodzica, width=8)
            pole_wprowadzania.insert(0, wartosc_domyslna)
            pole_wprowadzania.grid(row=i // 4, column=(i % 4) * 2 + 1, padx=2, pady=2, sticky=tk.W)
            slownik_parametrow[klucz_parametru] = pole_wprowadzania

    def przy_wyborze_sygnalu_1(self, zdarzenie):
        nazwa_sygnalu = self.wybor_sygnalu_1.get()
        kod_sygnalu = self.kody_sygnalow.get(nazwa_sygnalu)
        self._zbuduj_interfejs_parametrow(self.ramka_parametrow_1, self.pola_parametrow_1, kod_sygnalu)

    def przy_wyborze_sygnalu_2(self, zdarzenie):
        nazwa_sygnalu = self.wybor_sygnalu_2.get()
        kod_sygnalu = self.kody_sygnalow.get(nazwa_sygnalu)
        self._zbuduj_interfejs_parametrow(self.ramka_parametrow_2, self.pola_parametrow_2, kod_sygnalu)

    def przy_wyborze_sygnalu_a(self, zdarzenie):
        nazwa_sygnalu = self.wybor_sygnalu_a.get()
        kod_sygnalu = self.kody_sygnalow.get(nazwa_sygnalu)
        self._zbuduj_interfejs_parametrow(self.ramka_parametrow_a, self.pola_parametrow_a, kod_sygnalu)

    def przy_wyborze_sygnalu_b(self, zdarzenie):
        nazwa_sygnalu = self.wybor_sygnalu_b.get()
        kod_sygnalu = self.kody_sygnalow.get(nazwa_sygnalu)
        self._zbuduj_interfejs_parametrow(self.ramka_parametrow_b, self.pola_parametrow_b, kod_sygnalu)

    def przelacz_uzycie_glownego_a(self):
        if self.uzyj_glownego_jako_a.get():
            self.wybor_sygnalu_a.config(state="disabled")
            for w in self.ramka_parametrow_a.winfo_children():
                w.destroy()
            self.pola_parametrow_a.clear()
        else:
            self.wybor_sygnalu_a.config(state="readonly")
            self.przy_wyborze_sygnalu_a(None)

    def przy_wyborze_sygnalu_trans(self, zdarzenie):
        nazwa_sygnalu = self.wybor_sygnalu_trans.get()
        kod_sygnalu = self.kody_sygnalow.get(nazwa_sygnalu)
        self._zbuduj_interfejs_parametrow(self.ramka_parametrow_trans, self.pola_parametrow_trans, kod_sygnalu)

    def przelacz_uzycie_glownego_trans(self):
        if self.uzyj_glownego_trans.get():
            self.wybor_sygnalu_trans.config(state="disabled")
            for w in self.ramka_parametrow_trans.winfo_children():
                w.destroy()
            self.pola_parametrow_trans.clear()
        else:
            self.wybor_sygnalu_trans.config(state="readonly")
            self.przy_wyborze_sygnalu_trans(None)

    def _pobierz_przetworzone_parametry(self, slownik_parametrow):
        przetworzone = {}
        for klucz, pole_wprowadzania in slownik_parametrow.items():
            wartosc_tekstowa = pole_wprowadzania.get()
            try:
                if klucz in ['numer_probki_skoku', 'przesuniecie_probek']:
                    przetworzone[klucz] = int(wartosc_tekstowa)
                else:
                    przetworzone[klucz] = float(wartosc_tekstowa)
            except ValueError:
                raise ValueError(f"Nieprawidłowa wartość dla parametru '{klucz}': {wartosc_tekstowa}")
        return przetworzone

    def generuj_sygnal_glowny(self):
        nazwa_sygnalu = self.wybor_sygnalu_1.get()
        if not nazwa_sygnalu:
            messagebox.showwarning("Uwaga", "Wybierz typ sygnału głównego!")
            return

        kod_sygnalu = self.kody_sygnalow[nazwa_sygnalu]
        try:
            parametry = self._pobierz_przetworzone_parametry(self.pola_parametrow_1)
            fs = float(self.pole_czestotliwosc_probkowania.get())
            self.sygnal_glowny = GeneratorSygnalu(zrodlo_sygnalu=kod_sygnalu, czestotliwosc_probkowania=fs, **parametry)
            self.czy_dyskretny = kod_sygnalu in ["s10", "s11"]
            self.czy_widmo = False
            self.loguj_wiadomosc(f"Wygenerowano sygnał główny: {nazwa_sygnalu} z parametrami {parametry}")
            messagebox.showinfo("Sukces", "Sygnał główny został utworzony.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def wykonaj_operacje(self):
        if not self.sygnal_glowny:
            messagebox.showerror("Błąd", "Najpierw wygeneruj sygnał główny!")
            return

        operacja_tekst = self.wybor_operacji.get()
        nazwa_sygnalu_2 = self.wybor_sygnalu_2.get()

        if not operacja_tekst or not nazwa_sygnalu_2:
            messagebox.showwarning("Uwaga", "Wybierz operację oraz drugi sygnał!")
            return

        kod_sygnalu_2 = self.kody_sygnalow[nazwa_sygnalu_2]
        try:
            parametry_2 = self._pobierz_przetworzone_parametry(self.pola_parametrow_2)
            fs = float(self.pole_czestotliwosc_probkowania.get())
            sygnal_2 = GeneratorSygnalu(zrodlo_sygnalu=kod_sygnalu_2, czestotliwosc_probkowania=fs, **parametry_2)

            if operacja_tekst == "Dodawanie":
                self.sygnal_glowny = self.sygnal_glowny.dodaj_sygnal(sygnal_2)
            elif operacja_tekst == "Odejmowanie":
                self.sygnal_glowny = self.sygnal_glowny.odejmij_sygnal(sygnal_2)
            elif operacja_tekst == "Mnożenie":
                self.sygnal_glowny = self.sygnal_glowny.pomnoz_sygnal(sygnal_2)
            elif operacja_tekst == "Dzielenie":
                self.sygnal_glowny = self.sygnal_glowny.podziel_sygnal(sygnal_2)

            self.czy_dyskretny = self.czy_dyskretny or (kod_sygnalu_2 in ["s10", "s11"])

            self.loguj_wiadomosc(f"Wykonano operację '{operacja_tekst}' z sygnałem {nazwa_sygnalu_2}.")
            messagebox.showinfo("Sukces", "Zaktualizowano sygnał główny operatorem.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def wykonaj_transformacje(self):
        try:
            liczba_probek = int(self.pole_liczba_probek.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek w prawym panelu.")
            return

        if self.uzyj_glownego_trans.get():
            if not self.sygnal_glowny:
                messagebox.showerror("Błąd", "Najpierw wygeneruj sygnał główny!")
                return
            self.sygnal_glowny.resetuj()
            probki_x = np.array([next(self.sygnal_glowny) for _ in range(liczba_probek)])
            fp = self.sygnal_glowny.czestotliwosc_probkowania
        else:
            nazwa_syg = self.wybor_sygnalu_trans.get()
            if not nazwa_syg:
                messagebox.showerror("Błąd", "Wybierz sygnał do transformacji!")
                return
            kod_syg = self.kody_sygnalow[nazwa_syg]
            parametry = self._pobierz_przetworzone_parametry(self.pola_parametrow_trans)
            fs = float(self.pole_czestotliwosc_probkowania.get())
            tmp_sygnal = GeneratorSygnalu(zrodlo_sygnalu=kod_syg, czestotliwosc_probkowania=fs, **parametry)
            probki_x = np.array([next(tmp_sygnal) for _ in range(liczba_probek)])
            fp = tmp_sygnal.czestotliwosc_probkowania

        typ_trans = self.wybor_transformacji.get()
        dziedzina = self.wybor_dziedziny.get()
        implementacja = self.wybor_implementacji.get()
        
        info_dec = f" [{dziedzina}]" if typ_trans == "Szybka Transformacja Fouriera (FFT)" else ""
        self.loguj_wiadomosc(f"Rozpoczynanie transformacji: {typ_trans}{info_dec} ({implementacja}) na N={liczba_probek}...")
        
        start_time = time.time()
        wynik = None
        wynik_scipy = None
        scipy_time = 0

        try:
            is_power_of_2 = (liczba_probek & (liczba_probek - 1)) == 0 and liczba_probek > 0
            
            if "Walsha-Hadamarda" in typ_trans and not is_power_of_2:
                raise ValueError("Dla Transformacji Walsha-Hadamarda liczba próbek musi być potęgą liczby 2 (np. 256, 512, 1024). Zmień parametr 'Liczba próbek'.")
                
            if "Szybka" in typ_trans and not is_power_of_2:
                raise ValueError("Dla szybkiej transformacji liczba próbek musi być potęgą liczby 2 (np. 512, 1024). Zmień parametr 'Liczba próbek'.")

            t0_sc = time.time()
            if "Fouriera" in typ_trans:
                wynik_scipy = sp_fft.fft(probki_x) / liczba_probek
            elif "Kosinusowa" in typ_trans:
                wynik_scipy = sp_fft.dct(probki_x, type=2, norm='ortho')
            elif "Walsha-Hadamarda" in typ_trans:
                H = sp_linalg.hadamard(liczba_probek)
                wynik_scipy = np.dot(H, probki_x) / liczba_probek
            scipy_time = time.time() - t0_sc

            czas_wlasny = None
            if implementacja == "Biblioteka gotowa (Scipy)":
                wynik = wynik_scipy
                czas_wlasny = scipy_time
            else:
                t0_own = time.time()
                if typ_trans == "Transformacja Fouriera (DFT)":
                    wynik = TransformacjaSygnalu.dyskretna_transformacja_fouriera(probki_x)
                elif typ_trans == "Szybka Transformacja Fouriera (FFT)":
                    if "czasu" in dziedzina:
                        wynik = TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czasie(probki_x)
                    else:
                        wynik = TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czestotliwosci(probki_x)
                elif typ_trans == "Transformacja Kosinusowa (DCT)":
                    wynik = TransformacjaSygnalu.dyskretna_transformacja_kosinusowa(probki_x)
                elif typ_trans == "Szybka Transformacja Kosinusowa (FCT)":
                    wynik = TransformacjaSygnalu.szybka_transformacja_kosinusowa(probki_x)
                elif typ_trans == "Transformacja Walsha-Hadamarda (WHT)":
                    wynik = TransformacjaSygnalu.transformacja_walsha_hadamarda(probki_x)
                elif typ_trans == "Szybka Transformacja Walsha-Hadamarda (FWHT)":
                    wynik = TransformacjaSygnalu.szybka_transformacja_walsha_hadamarda(probki_x)
                
                czas_wlasny = time.time() - t0_own
                
            if implementacja == "Biblioteka gotowa (Scipy)":
                self.loguj_wiadomosc(f"Zakończono. Czas Scipy: {scipy_time:.6f} s")
            else:
                self.loguj_wiadomosc(f"Zakończono. Czas własny: {czas_wlasny:.6f} s, Czas Scipy: {scipy_time:.6f} s")
                if wynik_scipy is not None:
                    mse = np.mean(np.abs(wynik - wynik_scipy)**2)
                    self.loguj_wiadomosc(f"Błąd średniokwadratowy względem Scipy (MSE): {mse:.2e}")
                
            self.ostatnia_transformata = {
                'wynik': wynik,
                'wynik_scipy': wynik_scipy,
                'fp': fp,
                'typ_trans': typ_trans,
                'implementacja': implementacja,
                'dziedzina': dziedzina,
                'liczba_probek': liczba_probek,
                'probki_x': probki_x,
                'czas_wlasny': czas_wlasny,
                'czas_scipy': scipy_time
            }
            self.wizualizuj_transformacje()
            
        except ValueError as e:
            messagebox.showerror("Błąd danych", str(e))
        except Exception as e:
            messagebox.showerror("Błąd transformacji", str(e))

    def zapisz_sygnal(self):
        if not self.sygnal_glowny:
            messagebox.showerror("Błąd", "Brak wygenerowanego sygnału do zapisu!")
            return

        try:
            liczba_probek = int(self.pole_liczba_probek.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek.")
            return

        nazwa_pliku = filedialog.asksaveasfilename(defaultextension=".bin",
                                                   filetypes=[("Pliki Binarne", "*.bin"), ("Wszystkie pliki", "*.*")])
        if nazwa_pliku:
            try:
                PlikSygnalu.zapisz_do_binarnego(nazwa_pliku, self.sygnal_glowny, liczba_probek)
                self.loguj_wiadomosc(f"Zapisano sygnał do pliku: {nazwa_pliku} (N={liczba_probek})")
                messagebox.showinfo("Sukces", f"Zapisano pomyślnie do {nazwa_pliku}")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def wczytaj_sygnal(self):
        nazwa_pliku = filedialog.askopenfilename(filetypes=[("Pliki Binarne", "*.bin"), ("Wszystkie pliki", "*.*")])
        if nazwa_pliku:
            try:
                wczytany_sygnal = PlikSygnalu.wczytaj_z_binarnego(nazwa_pliku)
                if wczytany_sygnal:
                    self.sygnal_glowny = wczytany_sygnal
                    self.loguj_wiadomosc(f"Wczytano sygnał z pliku: {nazwa_pliku}")
                    self.loguj_wiadomosc(f"(Zobacz konsolę / odczytywanie binarne)")
                    PlikSygnalu.wyswietl_informacje_tekstowe(nazwa_pliku)
                    messagebox.showinfo("Sukces", "Sygnał został pomyślnie wczytany.")
                else:
                    messagebox.showerror("Błąd", "Plik błęny lub pusty.")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def wizualizuj_sygnal(self):
        if not self.sygnal_glowny:
            messagebox.showerror("Błąd", "Najpierw wygeneruj lub wczytaj sygnał główny!")
            return

        try:
            liczba_probek = int(self.pole_liczba_probek.get())
            liczba_przedzialow = int(self.pole_liczba_przedzialow.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek lub przedziałów.")
            return

        try:
            for zakladka in self.notatnik_wizualizacji.tabs():
                self.notatnik_wizualizacji.forget(zakladka)

            wykresy = WizualizatorSygnalu.rysuj_wszystko(self.sygnal_glowny, liczba_probek=liczba_probek,
                                                         liczba_przedzialow=liczba_przedzialow,
                                                         czy_dyskretny=self.czy_dyskretny,
                                                         czy_widmo=self.czy_widmo)
            self.sygnal_glowny.resetuj()

            for tytul, wykres in wykresy:
                ramka = ttk.Frame(self.notatnik_wizualizacji)
                self.notatnik_wizualizacji.add(ramka, text=tytul)

                plotno = FigureCanvasTkAgg(wykres, master=ramka)
                plotno.draw()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                pasek_narzedzi = NavigationToolbar2Tk(plotno, ramka)
                pasek_narzedzi.update()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            self.loguj_wiadomosc(
                f"Wyświetlono wizualizację na {liczba_probek} próbkach i {liczba_przedzialow} przedziałach.")

            self.pokaz_statystyki()

            if self.notatnik_wizualizacji.tabs():
                self.notatnik_wizualizacji.select(0)

        except Exception as e:
            messagebox.showerror("Błąd wizualizacji", str(e))

    def wizualizuj_transformacje(self):
        if not self.ostatnia_transformata:
            messagebox.showerror("Błąd", "Brak danych z transformacji do wizualizacji!")
            return

        try:
            wynik = self.ostatnia_transformata['wynik']
            probki_x = self.ostatnia_transformata['probki_x']
            fp = self.ostatnia_transformata['fp']
            liczba_probek = self.ostatnia_transformata['liczba_probek']
            
            for zakladka in self.notatnik_wizualizacji.tabs():
                self.notatnik_wizualizacji.forget(zakladka)

            sygnal_we = GeneratorSygnalu.z_tablicy(probki_x, fp)
            wykresy_we = WizualizatorSygnalu.rysuj_wszystko(sygnal_we, liczba_probek=liczba_probek,
                                                         liczba_przedzialow=int(self.pole_liczba_przedzialow.get()),
                                                         czy_dyskretny=self.czy_dyskretny,
                                                         czy_widmo=False)
            
            for tytul, wykres in wykresy_we:
                ramka = ttk.Frame(self.notatnik_wizualizacji)
                self.notatnik_wizualizacji.add(ramka, text="Sygnał Wejściowy")
                plotno = FigureCanvasTkAgg(wykres, master=ramka)
                plotno.draw()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                pasek_narzedzi = NavigationToolbar2Tk(plotno, ramka)
                pasek_narzedzi.update()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                break 

            tmp_sygnal = GeneratorSygnalu.z_tablicy(wynik, fp)
            wykresy = WizualizatorSygnalu.rysuj_wszystko(tmp_sygnal, liczba_probek=liczba_probek,
                                                         liczba_przedzialow=10,
                                                         czy_dyskretny=self.czy_dyskretny,
                                                         czy_widmo=True)

            for tytul, wykres in wykresy:
                ramka = ttk.Frame(self.notatnik_wizualizacji)
                self.notatnik_wizualizacji.add(ramka, text=f"Transformata: {tytul}")
                ramka_akcji = ttk.Frame(ramka)
                ramka_akcji.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
                btn_odwroc = ttk.Button(ramka_akcji, text="Wykonaj transformację odwrotną", command=self.wykonaj_transformacje_odwrotna)
                btn_odwroc.pack(side=tk.LEFT)

                plotno = FigureCanvasTkAgg(wykres, master=ramka)
                plotno.draw()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                pasek_narzedzi = NavigationToolbar2Tk(plotno, ramka)
                pasek_narzedzi.update()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            self._pokaz_statystyki_transformacji()

            self.loguj_wiadomosc(f"Wyświetlono wizualizację transformaty.")

            if self.notatnik_wizualizacji.tabs():
                self.notatnik_wizualizacji.select(0)

        except Exception as e:
            messagebox.showerror("Błąd wizualizacji transformaty", str(e))

    def _dodaj_sekcje(self, kontener, tytul, elementy, szerokosc_etykiety=30):
        tk.Label(kontener, text=tytul, font=("Arial", 12, "bold"), bg="#2b2b2b", fg="#4fc3f7").pack(anchor=tk.W, pady=(15, 5))
        for etykieta, wartosc in elementy:
            wiersz = tk.Frame(kontener, bg="#2b2b2b")
            wiersz.pack(fill=tk.X, pady=2)
            tk.Label(wiersz, text=etykieta, font=("Arial", 10), bg="#2b2b2b", fg="#e0e0e0", width=szerokosc_etykiety, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(wiersz, text=str(wartosc), font=("Consolas", 10), bg="#2b2b2b", fg="#ffffff", anchor=tk.W).pack(side=tk.LEFT)
        tk.Frame(kontener, height=1, bg="#555555").pack(fill=tk.X, pady=(10, 0))

    def _pokaz_statystyki_transformacji(self):
        dane = self.ostatnia_transformata
        ramka_stat = ttk.Frame(self.notatnik_wizualizacji)
        self.notatnik_wizualizacji.add(ramka_stat, text="Statystyki")
        
        plotno_scroll = tk.Canvas(ramka_stat, bg="#2b2b2b")
        scrollbar = ttk.Scrollbar(ramka_stat, orient="vertical", command=plotno_scroll.yview)
        kontener = tk.Frame(plotno_scroll, bg="#2b2b2b", padx=20, pady=20)

        kontener.bind("<Configure>", lambda e: plotno_scroll.configure(scrollregion=plotno_scroll.bbox("all")))
        plotno_scroll.create_window((0, 0), window=kontener, anchor="nw")
        plotno_scroll.configure(yscrollcommand=scrollbar.set)
        
        plotno_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def add_element(sekcja, etykieta, wartosc):
            sekcja.append((etykieta, wartosc))

        tk.Label(kontener, text="Wyniki numeryczne i statystyki", font=("Arial", 16, "bold"), bg="#2b2b2b", fg="#ffffff").pack(anchor=tk.W, pady=(0, 10))
        
        parametry = []
        add_element(parametry, "Zastosowana implementacja", dane['implementacja'])
        if dane['dziedzina']: add_element(parametry, "Dziedzina (dla FFT)", dane['dziedzina'])
        add_element(parametry, "Liczba próbek N", dane['liczba_probek'])
        add_element(parametry, "Częstotliwość próbkowania fp", f"{dane['fp']} Hz")
        delta_f = dane['fp'] / dane['liczba_probek']
        add_element(parametry, "Rozdzielczość częstotliwościowa Δf", f"{delta_f:.4f} Hz")
        self._dodaj_sekcje(kontener, "Parametry transformacji", parametry)

        czasy = []
        add_element(czasy, "Czas własny algorytmu", f"{dane['czas_wlasny']:.6f} s" if dane['czas_wlasny'] is not None else "Brak")
        add_element(czasy, "Czas biblioteki Scipy", f"{dane['czas_scipy']:.6f} s")
        if dane['czas_wlasny'] and dane['czas_scipy'] > 0:
            add_element(czasy, "Stosunek czasu (Własny/Scipy)", f"{(dane['czas_wlasny'] / dane['czas_scipy']):.2f}x")
        self._dodaj_sekcje(kontener, "Porównanie czasów", czasy)

        bledy = []
        wynik = dane['wynik']
        wynik_scipy = dane['wynik_scipy']
        if wynik_scipy is not None and dane['implementacja'] != "Biblioteka gotowa (Scipy)":
            mse = np.mean(np.abs(wynik - wynik_scipy)**2)
            max_err = np.max(np.abs(wynik - wynik_scipy))
            add_element(bledy, "Błąd średniokwadratowy (MSE)", f"{mse:.4e}")
            add_element(bledy, "Maksymalny błąd bezwzględny", f"{max_err:.4e}")
        else:
            add_element(bledy, "Weryfikacja", "Nie dotyczy (użyto Scipy)")
        self._dodaj_sekcje(kontener, "Weryfikacja poprawności (vs Scipy)", bledy)

        skok = []
        modul = np.abs(wynik)
        indeksy_sort = np.argsort(modul)[::-1]
        for i in range(min(5, len(indeksy_sort))):
            idx = indeksy_sort[i]
            freq = idx * delta_f
            val = wynik[idx]
            val_str = f"{val.real:.4f} + {val.imag:.4f}j" if np.iscomplexobj(val) else f"{val:.4f}"
            add_element(skok, f"#{i+1}", f"f = {freq:.2f} Hz  |  Wartość: {val_str}  |  Moduł: {modul[idx]:.4f}")
        self._dodaj_sekcje(kontener, "Top 5 Dominujących Składowych", skok, szerokosc_etykiety=5)

    def wykonaj_benchmark(self):
        try:
            if self.uzyj_glownego_trans.get():
                if not self.sygnal_glowny:
                    messagebox.showerror("Błąd", "Najpierw wygeneruj sygnał główny!")
                    return
                def _zbierz_probki(N):
                    self.sygnal_glowny.resetuj()
                    return np.array([next(self.sygnal_glowny) for _ in range(N)])
            else:
                nazwa_syg = self.wybor_sygnalu_trans.get()
                if not nazwa_syg:
                    messagebox.showerror("Błąd", "Wybierz sygnał do transformacji!")
                    return
                kod_syg = self.kody_sygnalow[nazwa_syg]
                parametry = self._pobierz_przetworzone_parametry(self.pola_parametrow_trans)
                fs = float(self.pole_czestotliwosc_probkowania.get())
                
                def _zbierz_probki(N):
                    tmp_sygnal = GeneratorSygnalu(zrodlo_sygnalu=kod_syg, czestotliwosc_probkowania=fs, **parametry)
                    return np.array([next(tmp_sygnal) for _ in range(N)])

        except Exception as e:
            messagebox.showerror("Błąd", str(e))
            return

        zakres_n = [2**i for i in range(9, 14)]
        wyniki = {"N": zakres_n}

        self.loguj_wiadomosc(f"Rozpoczynam benchmark dla N od 512 do 8192...")

        typy = ["DFT", "FFT DIT", "FFT DIF", "DCT", "FCT", "WHT", "FWHT"]
        for k in typy: wyniki[k] = []
        
        for N in zakres_n:
            px = _zbierz_probki(N)
            
            t0 = time.time()
            TransformacjaSygnalu.dyskretna_transformacja_fouriera(px)
            wyniki["DFT"].append(time.time() - t0)

            t0 = time.time()
            TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czasie(px)
            wyniki["FFT DIT"].append(time.time() - t0)

            t0 = time.time()
            TransformacjaSygnalu.szybka_transformacja_fouriera_z_decymacja_w_czestotliwosci(px)
            wyniki["FFT DIF"].append(time.time() - t0)

            t0 = time.time()
            TransformacjaSygnalu.dyskretna_transformacja_kosinusowa(px)
            wyniki["DCT"].append(time.time() - t0)

            t0 = time.time()
            TransformacjaSygnalu.szybka_transformacja_kosinusowa(px)
            wyniki["FCT"].append(time.time() - t0)

            t0 = time.time()
            TransformacjaSygnalu.transformacja_walsha_hadamarda(px)
            wyniki["WHT"].append(time.time() - t0)

            t0 = time.time()
            TransformacjaSygnalu.szybka_transformacja_walsha_hadamarda(px)
            wyniki["FWHT"].append(time.time() - t0)

        self.loguj_wiadomosc("Benchmark zakończony. Wyświetlam wyniki.")
        
        for tab_id in self.notatnik_wizualizacji.tabs():
            if self.notatnik_wizualizacji.tab(tab_id, "text") == "Benchmark":
                self.notatnik_wizualizacji.forget(tab_id)
                break

        ramka_bench = tk.Frame(self.notatnik_wizualizacji, bg="#2b2b2b")
        self.notatnik_wizualizacji.add(ramka_bench, text="Benchmark")
        self.notatnik_wizualizacji.select(ramka_bench)

        fig = plt.Figure(figsize=(10, 6), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)

        kolory = ['cyan', 'magenta', 'lime', 'yellow', 'red', 'orange', 'pink']
        markery = ['o', 's', '^', 'D', 'x']
        
        for i, t in enumerate(typy):
            ax.plot(zakres_n, wyniki[t], color=kolory[i%len(kolory)], marker=markery[i%len(markery)], label=t, linewidth=2)

        ax.set_xscale('log', base=2)
        ax.set_yscale('log')
        ax.set_title("Złożoność czasowa transformat", color='white')
        ax.set_xlabel("Liczba próbek N", color='white')
        ax.set_ylabel("Czas wykonywania [s]", color='white')
        ax.grid(True, which="both", ls="--", color='gray', alpha=0.5)
        ax.set_facecolor('#2b2b2b')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('gray')
        ax.legend(facecolor='#2b2b2b', labelcolor='white')
        fig.tight_layout()

        plotno = FigureCanvasTkAgg(fig, master=ramka_bench)
        plotno.draw()
        plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ramka_tabeli = tk.Frame(ramka_bench, bg="#2b2b2b")
        ramka_tabeli.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        style = ttk.Style()
        style.configure("Dark.Treeview", background="#333333", fieldbackground="#333333", foreground="white", rowheight=25, borderwidth=0)
        style.map("Dark.Treeview", background=[('selected', '#4fc3f7')], foreground=[('selected', 'black')])
        style.configure("Dark.Treeview.Heading", background="#444444", foreground="white", font=("Arial", 10, "bold"), borderwidth=1)
        
        kolumny = ["N"] + typy
        tabela = ttk.Treeview(ramka_tabeli, columns=kolumny, show='headings', height=len(zakres_n), style="Dark.Treeview")
        for col in kolumny:
            tabela.heading(col, text=col)
            tabela.column(col, width=100, anchor=tk.CENTER)
            
        for i, n in enumerate(zakres_n):
            wartosci = [n] + [f"{wyniki[t][i]:.6f}" for t in typy]
            tabela.insert("", "end", values=wartosci)
            
        tabela.pack(fill=tk.BOTH, expand=True)


    def wykonaj_transformacje_odwrotna(self):
        if not self.ostatnia_transformata:
            messagebox.showerror("Błąd", "Brak danych z transformacji!")
            return

        wynik = self.ostatnia_transformata['wynik']
        fp = self.ostatnia_transformata['fp']
        typ_trans = self.ostatnia_transformata['typ_trans']
        implementacja = self.ostatnia_transformata['implementacja']
        dziedzina = self.ostatnia_transformata.get('dziedzina', '')
        liczba_probek = self.ostatnia_transformata['liczba_probek']

        info_dec = f" [{dziedzina}]" if typ_trans == "Szybka Transformacja Fouriera (FFT)" else ""
        self.loguj_wiadomosc(f"Wywoływanie transformacji odwrotnej dla {typ_trans}{info_dec} ({implementacja})...")
        
        start_time = time.time()
        nowy_wynik = None
        
        try:
            if implementacja == "Biblioteka gotowa (Scipy)":
                if "Fouriera" in typ_trans:
                    nowy_wynik = sp_fft.ifft(wynik) * liczba_probek
                elif "Kosinusowa" in typ_trans:
                    nowy_wynik = sp_fft.idct(wynik, type=2, norm='ortho')
                elif "Walsha-Hadamarda" in typ_trans:
                    H = sp_linalg.hadamard(liczba_probek)
                    nowy_wynik = np.dot(H, wynik) / liczba_probek
            else:
                if "Fouriera" in typ_trans:
                    if "Szybka" in typ_trans:
                        nowy_wynik = TransformacjaSygnalu.odwrotna_szybka_transformacja_fouriera(wynik)
                    else:
                        nowy_wynik = TransformacjaSygnalu.odwrotna_dyskretna_transformacja_fouriera(wynik)
                elif "Kosinusowa" in typ_trans:
                    nowy_wynik = sp_fft.idct(wynik, type=2, norm='ortho')
                    self.loguj_wiadomosc("Użyto bibliotecznego IDCT jako odwrotności do DCT.")
                elif "Walsha-Hadamarda" in typ_trans:
                    if "Szybka" in typ_trans:
                        nowy_wynik = TransformacjaSygnalu.szybka_transformacja_walsha_hadamarda(wynik)
                    else:
                        nowy_wynik = TransformacjaSygnalu.transformacja_walsha_hadamarda(wynik)

            moj_czas = time.time() - start_time
            self.loguj_wiadomosc(f"Zakończono transformację odwrotną. Czas: {moj_czas:.6f} s")
            
            self.sygnal_glowny = GeneratorSygnalu.z_tablicy(nowy_wynik, fp)
            self.czy_widmo = False
            self.wizualizuj_sygnal()

        except Exception as e:
            messagebox.showerror("Błąd transformacji odwrotnej", str(e))

    def pokaz_statystyki(self):
        if not self.sygnal_glowny:
            messagebox.showerror("Błąd", "Najpierw wygeneruj lub wczytaj sygnał główny!")
            return

        try:
            liczba_probek = int(self.pole_liczba_probek.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek.")
            return

        try:
            statystyki = self.sygnal_glowny.pobierz_statystyki(liczba_probek=liczba_probek)
            if not statystyki:
                self.loguj_wiadomosc("Sygnał jest pusty lub niemożliwy do przeanalizowania.")
                return

            self.loguj_wiadomosc(f"--- Statystyki sygnału ({liczba_probek} próbek) ---")
            for nazwa, wartosc in statystyki.items():
                if isinstance(wartosc, (complex, np.complex128)):
                    wartosc_tekstowa = f"{wartosc.real:.4f} + {wartosc.imag:.4f}j"
                else:
                    wartosc_tekstowa = f"{wartosc:.4f}"
                self.loguj_wiadomosc(f" {nazwa:<25}: {wartosc_tekstowa}")
            self.loguj_wiadomosc("-" * 35)

            for tab_id in self.notatnik_wizualizacji.tabs():
                if self.notatnik_wizualizacji.tab(tab_id, "text") == "Statystyki":
                    self.notatnik_wizualizacji.forget(tab_id)
                    break

            ramka_stat = ttk.Frame(self.notatnik_wizualizacji)
            self.notatnik_wizualizacji.add(ramka_stat, text="Statystyki")
            self.notatnik_wizualizacji.select(ramka_stat)

            kontener = tk.Frame(ramka_stat, bg="#2b2b2b", padx=40, pady=30)
            kontener.pack(fill=tk.BOTH, expand=True)
            tk.Label(kontener, text="Parametry sygnału", font=("Arial", 16, "bold"),
                     bg="#2b2b2b", fg="#ffffff").pack(anchor=tk.W, pady=(0, 5))

            rzeczywiste_n = statystyki.get("liczba_probek", liczba_probek)
            czas_trwania = statystyki.get("czas_trwania_sygnalu", 0)
            tk.Label(kontener,
                     text=f"Liczba próbek: {rzeczywiste_n}   |   Czas trwania: {czas_trwania:.4f} s",
                     font=("Arial", 10), bg="#2b2b2b", fg="#aaaaaa").pack(anchor=tk.W, pady=(0, 20))

            tk.Frame(kontener, height=1, bg="#555555").pack(fill=tk.X, pady=(0, 15))

            etykiety = {
                "srednia": "Wartość średnia",
                "srednia_bezwzgledna": "Wartość średnia bezwzględna",
                "wartosc_skuteczna": "Wartość skuteczna (RMS)",
                "wariancja": "Wariancja",
                "moc": "Moc średnia",
            }

            for klucz, etykieta in etykiety.items():
                wartosc = statystyki.get(klucz)
                if wartosc is None:
                    continue

                wiersz = tk.Frame(kontener, bg="#2b2b2b")
                wiersz.pack(fill=tk.X, pady=4)

                tk.Label(wiersz, text=etykieta, font=("Arial", 12),
                         bg="#2b2b2b", fg="#e0e0e0", width=30, anchor=tk.W).pack(side=tk.LEFT)

                if isinstance(wartosc, (complex, np.complex128)):
                    tekst_wartosci = f"{wartosc.real:.6f} + {wartosc.imag:.6f}j"
                else:
                    tekst_wartosci = f"{wartosc:.6f}"

                tk.Label(wiersz, text=tekst_wartosci, font=("Consolas", 12, "bold"),
                         bg="#2b2b2b", fg="#4fc3f7", anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))

        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def aktualizuj_interfejs_konwersji(self, event=None):
        for w in self.ramka_param_konwersji.winfo_children():
            w.destroy()
            
        tryb = self.wybor_trybu_konwersji.get()
        self.parametry_konwersji_pola = {}
        
        if tryb == "Próbkowanie i Rekonstrukcja":
            ttk.Label(self.ramka_param_konwersji, text="f próbkowania (Hz):").grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            pol_fs = ttk.Entry(self.ramka_param_konwersji, width=8)
            pol_fs.insert(0, "100")
            pol_fs.grid(row=0, column=1, padx=2, pady=2)
            self.parametry_konwersji_pola['f_sample'] = pol_fs
            
            ttk.Label(self.ramka_param_konwersji, text="Rekonstrukcja:").grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
            pol_rek = ttk.Combobox(self.ramka_param_konwersji, values=["ZOH", "FOH", "Sinc"], state="readonly", width=8)
            pol_rek.current(0)
            pol_rek.grid(row=0, column=3, padx=2, pady=2)
            pol_rek.bind("<<ComboboxSelected>>", self.aktualizuj_widocznosc_sinc)
            self.parametry_konwersji_pola['rekonstrukcja'] = pol_rek

            self.etykieta_sinc = ttk.Label(self.ramka_param_konwersji, text="Sinc próbki:")
            self.etykieta_sinc.grid(row=1, column=2, padx=2, pady=2, sticky=tk.W)
            pol_sinc = ttk.Entry(self.ramka_param_konwersji, width=8)
            pol_sinc.insert(0, "50")
            pol_sinc.grid(row=1, column=3, padx=2, pady=2)
            self.parametry_konwersji_pola['sinc_n'] = pol_sinc
            self.aktualizuj_widocznosc_sinc()
            
        elif tryb == "Kwantyzacja":
            ttk.Label(self.ramka_param_konwersji, text="Liczba bitów:").grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            pol_bit = ttk.Entry(self.ramka_param_konwersji, width=8)
            pol_bit.insert(0, "8")
            pol_bit.grid(row=0, column=1, padx=2, pady=2)
            self.parametry_konwersji_pola['bity'] = pol_bit
            
            ttk.Label(self.ramka_param_konwersji, text="Algorytm:").grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
            pol_alg = ttk.Combobox(self.ramka_param_konwersji, values=["Obcięcie", "Zaokrąglenie"], state="readonly", width=12)
            pol_alg.current(0)
            pol_alg.grid(row=0, column=3, padx=2, pady=2)
            self.parametry_konwersji_pola['algorytm'] = pol_alg

    def aktualizuj_widocznosc_sinc(self, event=None):
        if 'rekonstrukcja' not in self.parametry_konwersji_pola or 'sinc_n' not in self.parametry_konwersji_pola:
            return
            
        if self.parametry_konwersji_pola['rekonstrukcja'].get() == "Sinc":
            self.etykieta_sinc.grid()
            self.parametry_konwersji_pola['sinc_n'].grid()
        else:
            self.etykieta_sinc.grid_remove()
            self.parametry_konwersji_pola['sinc_n'].grid_remove()

    def wykonaj_konwersje(self):
        if not self.sygnal_glowny:
            messagebox.showerror("Błąd", "Najpierw wygeneruj lub wczytaj sygnał główny!")
            return
            
        tryb = self.wybor_trybu_konwersji.get()
        liczba_probek = int(self.pole_liczba_probek.get())
        
        self.sygnal_glowny.resetuj()
        probki_high = np.array([next(self.sygnal_glowny) for _ in range(liczba_probek + 1)])
        if np.iscomplexobj(probki_high):
            messagebox.showerror("Błąd", "Konwersja A/C i C/A obsługuje tylko sygnały rzeczywiste!")
            return
            
        f_high = self.sygnal_glowny.czestotliwosc_probkowania
        czas_poczatkowy = self.sygnal_glowny.parametry.get('czas_poczatkowy', 0.0)
        T_h = 1.0 / f_high
        czas_high = np.arange(liczba_probek + 1) * T_h + czas_poczatkowy
        
        self.sygnal_glowny.resetuj()
        
        try:
            for tab_id in self.notatnik_wizualizacji.tabs():
                if self.notatnik_wizualizacji.tab(tab_id, "text") == "Wyniki Konwersji":
                    self.notatnik_wizualizacji.forget(tab_id)
            
            ramka_wynikow = ttk.Frame(self.notatnik_wizualizacji)
            self.notatnik_wizualizacji.add(ramka_wynikow, text="Wyniki Konwersji")
            self.notatnik_wizualizacji.select(ramka_wynikow)
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            from WizualizatorSygnalu import WizualizatorSygnalu
            konwerter = KonwerterSygnalu()
            liczba_przedzialow = int(self.pole_liczba_przedzialow.get())
            
            if tryb == "Próbkowanie i Rekonstrukcja":
                f_sample = float(self.parametry_konwersji_pola['f_sample'].get())
                rekonstrukcja = self.parametry_konwersji_pola['rekonstrukcja'].get()
                sinc_n = int(self.parametry_konwersji_pola['sinc_n'].get())
                
                t_sample, x_sample = konwerter.probkowanie_rownomierne(czas_high, probki_high, f_sample)
                
                if rekonstrukcja == "ZOH":
                    x_rec = konwerter.rekonstrukcja_zoh(t_sample, x_sample, czas_high)
                elif rekonstrukcja == "FOH":
                    x_rec = konwerter.rekonstrukcja_foh(t_sample, x_sample, czas_high)
                elif rekonstrukcja == "Sinc":
                    x_rec = konwerter.rekonstrukcja_sinc(t_sample, x_sample, czas_high, sinc_n)
                
                sygnal_oryg = probki_high
                sygnal_porown = x_rec
                
                opis = f"Próbkowanie: {f_sample} Hz, Odtwarzanie: {rekonstrukcja}"
                wykresy = WizualizatorSygnalu.rysuj_konwersje(czas_high, sygnal_oryg, sygnal_porown, tryb, opis, liczba_przedzialow, f_sample=f_sample, t_sample=t_sample, x_sample=x_sample)

            else:
                bity = int(self.parametry_konwersji_pola['bity'].get())
                algorytm = self.parametry_konwersji_pola['algorytm'].get()
                
                if algorytm == "Obcięcie":
                    x_quant = konwerter.kwantyzacja_obcieciem(probki_high, bity)
                else:
                    x_quant = konwerter.kwantyzacja_zaokragleniem(probki_high, bity)
                    
                sygnal_oryg = probki_high
                sygnal_porown = x_quant
                
                opis = f"Algorytm: {algorytm}, Bity: {bity}"
                wykresy = WizualizatorSygnalu.rysuj_konwersje(czas_high, sygnal_oryg, sygnal_porown, tryb, opis, liczba_przedzialow)

            for tytul, wykres in wykresy:
                plotno = FigureCanvasTkAgg(wykres, master=ramka_wynikow)
                plotno.draw()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                pasek_narzedzi = NavigationToolbar2Tk(plotno, ramka_wynikow)
                pasek_narzedzi.update()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            mse = konwerter.oblicz_mse(sygnal_oryg, sygnal_porown)
            snr = konwerter.oblicz_snr(sygnal_oryg, sygnal_porown)
            psnr = konwerter.oblicz_psnr(sygnal_oryg, sygnal_porown)
            md = konwerter.oblicz_md(sygnal_oryg, sygnal_porown)
            
            self.loguj_wiadomosc(f"--- Wyniki Konwersji ({tryb}) ---")
            self.loguj_wiadomosc(f" MSE  : {mse:.6f}")
            self.loguj_wiadomosc(f" SNR  : {snr:.6f} dB")
            self.loguj_wiadomosc(f" PSNR : {psnr:.6f} dB")
            self.loguj_wiadomosc(f" MD   : {md:.6f}")
            if tryb == "Kwantyzacja":
                enob = konwerter.oblicz_enob(snr)
                self.loguj_wiadomosc(f" ENOB : {enob:.4f} bitów")
            self.loguj_wiadomosc("-" * 35)

        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def filtruj_sygnal(self):
        if not self.sygnal_glowny:
            messagebox.showerror("Błąd", "Najpierw wygeneruj lub wczytaj sygnał główny!")
            return
            
        try:
            M = int(self.pole_m.get())
            fo = float(self.pole_fo.get())
            rodzaj_filtru = self.wybor_filtru.get()
            okno = self.wybor_okna.get()
            
            fp = self.sygnal_glowny.czestotliwosc_probkowania
            
            if rodzaj_filtru == "Dolnoprzepustowy":
                K = fp / fo
                h = FiltrSygnalu.generuj_filtr_dolnoprzepustowy(M, K, okno)
            elif rodzaj_filtru == "Górnoprzepustowy":
                prawdziwe_fo = (fp / 2.0) - fo
                if prawdziwe_fo <= 0:
                    raise ValueError("Częstotliwość odcięcia filtru górnoprzepustowego musi być ostro mniejsza od częstotliwości Nyquista (fp/2)!")
                if prawdziwe_fo >= (fp / 2.0):
                    raise ValueError("Częstotliwość odcięcia musi być większa od zera!")
                K = fp / prawdziwe_fo
                h = FiltrSygnalu.generuj_filtr_gornoprzepustowy(M, K, okno)
                
            liczba_probek = int(self.pole_liczba_probek.get())
            self.sygnal_glowny.resetuj()
            probki_x = np.array([next(self.sygnal_glowny) for _ in range(liczba_probek)])
            
            probki_y = FiltrSygnalu.splot(h, probki_x)
            
            self.sygnal_glowny = GeneratorSygnalu.z_tablicy(probki_y, fp)
            self.loguj_wiadomosc(f"Wykonano filtrację: {rodzaj_filtru}, M={M}, fo={fo}, okno={okno}.")
            messagebox.showinfo("Sukces", "Sygnał główny został przefiltrowany. Wykres wizualizacji można odświeżyć.")
            
        except Exception as e:
            messagebox.showerror("Błąd filtracji", str(e))

    def symuluj_odleglosc(self):
        try:
            dt_sim = float(self.pole_dt_sim.get())
            v_ob = float(self.pole_v_ob.get())
            d0 = float(self.pole_d0.get())
            c_osr = float(self.pole_c_osr.get())
            
            T_syg = float(self.pole_T_syg.get())
            fp = float(self.pole_fp_rad.get())
            N_buf = int(self.pole_N_buf.get())
            T_rep = float(self.pole_T_rep.get())
            korelacja_typ = self.wybor_korelacji.get()
            
            czas_calkowity = float(self.pole_czas_calk.get())
            
            czujnik = CzujnikOdleglosci(dt_sim, v_ob, d0, c_osr, T_syg, fp, N_buf, T_rep, korelacja_typ)
            
            czasy, rz_d, zm_d, buf_wyslany, buf_odebrany, korelacja, t_koniec = czujnik.symuluj(czas_calkowity)
            self.loguj_wiadomosc("Symulacja zakończona. Wyświetlam wyniki.")
            srodek = int(self.pole_N_buf.get()) - 1
            prawa_polowa = korelacja[srodek:]
            
            import scipy.signal
            peaks, _ = scipy.signal.find_peaks(prawa_polowa)
            if len(peaks) > 0:
                najwyzszy_pik_idx = np.argmax(prawa_polowa[peaks])
                max_idx = peaks[najwyzszy_pik_idx]
            else:
                max_idx = np.argmax(prawa_polowa)
            dt_probk = 1.0 / float(self.pole_fp_rad.get())
            odleglosc = float(self.pole_c_osr.get()) * (max_idx * dt_probk) / 2.0
            
            self.loguj_wiadomosc(f"Odległość policzona dla maksimum korelacji: {odleglosc:.4f} m")
            
            for tab_id in self.notatnik_wizualizacji.tabs():
                if self.notatnik_wizualizacji.tab(tab_id, "text") in ["Wyniki Radaru", "Statystyki Radaru"]:
                    self.notatnik_wizualizacji.forget(tab_id)
                    
            ramka_wynikow = ttk.Frame(self.notatnik_wizualizacji)
            self.notatnik_wizualizacji.add(ramka_wynikow, text="Wyniki Radaru")
            self.notatnik_wizualizacji.select(ramka_wynikow)
            
            fig = plt.Figure(figsize=(8, 8), facecolor='#2b2b2b')
            ax1 = fig.add_subplot(311)
            ax2 = fig.add_subplot(312)
            ax3 = fig.add_subplot(313)
            
            fp = float(self.pole_fp_rad.get())
            N = int(self.pole_N_buf.get())
            t_buf = np.linspace(t_koniec - N/fp, t_koniec, N)
            
            ax1.plot(t_buf, buf_wyslany, color='cyan', linewidth=2)
            ax1.set_title("Sygnał Sondujący", color='white')
            
            ax2.plot(t_buf, buf_odebrany, color='cyan', linewidth=2)
            ax2.set_title("Sygnał Powrotny", color='white')
            
            t_kor = np.linspace(t_koniec - (2*N-1)/fp, t_koniec, 2*N-1)
            ax3.plot(t_kor, korelacja, color='cyan', linewidth=2)
            ax3.set_title("Korelacja Sygnałów Sondującego oraz Powrotnego", color='white')
            
            t_srodek = t_kor[N-1]
            t_pik = t_kor[N-1 + max_idx]
            opoznienie_sek = max_idx * (1.0 / fp)
            
            ax3.axvline(x=t_srodek, color='red', linestyle='--', alpha=0.7, label='Środek (0 opóźnienia)')
            if max_idx > 0:
                ax3.axvline(x=t_pik, color='yellow', linestyle=':', alpha=0.9, label=f'Pik korelacji (+{opoznienie_sek:.5f} s)')
                ax3.axvspan(t_srodek, t_pik, color='yellow', alpha=0.2)
            ax3.legend(loc='upper right', facecolor='#2b2b2b', edgecolor='gray', labelcolor='white', fontsize=8)
            
            self.loguj_wiadomosc(f"Wizualne przesunięcie piku od środka wykresu wynosi: {opoznienie_sek:.6f} sekund")
            
            for ax in [ax1, ax2, ax3]:
                ax.set_facecolor('#2b2b2b')
                ax.tick_params(colors='white')
                ax.grid(True, linestyle='--', color='lightgray', alpha=0.5)
                for spine in ax.spines.values():
                    spine.set_color('gray')
            
            fig.tight_layout()
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            plotno = FigureCanvasTkAgg(fig, master=ramka_wynikow)
            plotno.draw()
            plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


            ramka_stat = ttk.Frame(self.notatnik_wizualizacji)
            self.notatnik_wizualizacji.add(ramka_stat, text="Statystyki Radaru")
            
            kontener = tk.Frame(ramka_stat, bg="#2b2b2b", padx=40, pady=30)
            kontener.pack(fill=tk.BOTH, expand=True)
            tk.Label(kontener, text="Statystyki Pomiaru Odległości", font=("Arial", 16, "bold"),
                     bg="#2b2b2b", fg="#ffffff").pack(anchor=tk.W, pady=(0, 5))

            rz_d_arr = np.array(rz_d)
            zm_d_arr = np.array(zm_d)
            bledy = rz_d_arr - zm_d_arr
            bledy_bezwzgledne = np.abs(bledy)
            
            sredni_blad = np.mean(bledy_bezwzgledne) if len(bledy_bezwzgledne) > 0 else 0
            max_blad = np.max(bledy_bezwzgledne) if len(bledy_bezwzgledne) > 0 else 0
            rms_blad = np.sqrt(np.mean(bledy**2)) if len(bledy) > 0 else 0
            
            c = float(self.pole_c_osr.get())
            rozdzielczosc = c / (2.0 * fp)

            tk.Label(kontener,
                     text=f"Liczba pomiarów: {len(rz_d)}   |   Rozdzielczość teoretyczna: {rozdzielczosc:.4f} m",
                     font=("Arial", 10), bg="#2b2b2b", fg="#aaaaaa").pack(anchor=tk.W, pady=(0, 20))

            tk.Frame(kontener, height=1, bg="#555555").pack(fill=tk.X, pady=(0, 15))

            etykiety = {
                "Średni błąd bezwzględny": sredni_blad,
                "Maksymalny błąd": max_blad,
                "Błąd średniokwadratowy (RMS)": rms_blad,
            }

            for etykieta, wartosc in etykiety.items():
                wiersz = tk.Frame(kontener, bg="#2b2b2b")
                wiersz.pack(fill=tk.X, pady=4)

                tk.Label(wiersz, text=etykieta, font=("Arial", 12),
                         bg="#2b2b2b", fg="#e0e0e0", width=35, anchor=tk.W).pack(side=tk.LEFT)

                tk.Label(wiersz, text=f"{wartosc:.6f} m", font=("Consolas", 12, "bold"),
                         bg="#2b2b2b", fg="#4fc3f7", anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
            
        except Exception as e:
            messagebox.showerror("Błąd symulacji", str(e))

    def oblicz_korelacje(self):
        try:
            fp = float(self.pole_fp_korelacji.get())
            if fp <= 0:
                raise ValueError("Częstotliwość próbkowania musi być większa od 0.")
            
            algorytm = self.wybor_algorytmu_korelacji.get()
            if not algorytm:
                raise ValueError("Wybierz metodę korelacji!")
        except Exception as e:
            messagebox.showerror("Błąd parametrów", f"Błędne parametry korelacji: {str(e)}")
            return

        try:
            if self.uzyj_glownego_jako_a.get():
                if not self.sygnal_glowny:
                    raise ValueError("Brak wygenerowanego sygnału głównego! Najpierw wygeneruj go w pierwszej zakładce.")
                
                N_A = int(self.pole_liczba_probek_a.get())
                if N_A <= 0:
                    raise ValueError("Liczba próbek N_A must be greater than 0.")
                
                self.sygnal_glowny.resetuj()
                probki_a = np.array([next(self.sygnal_glowny) for _ in range(N_A)])
                self.sygnal_glowny.resetuj()
                
                fp_a = self.sygnal_glowny.czestotliwosc_probkowania
                fp = fp_a
                self.pole_fp_korelacji.delete(0, tk.END)
                self.pole_fp_korelacji.insert(0, f"{fp_a}")
                
                typ_a_nazwa = "Sygnał Główny"
            else:
                nazwa_syg_a = self.wybor_sygnalu_a.get()
                if not nazwa_syg_a:
                    raise ValueError("Wybierz typ sygnału A!")
                
                kod_syg_a = self.kody_sygnalow[nazwa_syg_a]
                parametry_a = self._pobierz_przetworzone_parametry(self.pola_parametrow_a)
                N_A = int(self.pole_liczba_probek_a.get())
                if N_A <= 0:
                    raise ValueError("Liczba próbek N_A must be greater than 0.")
                
                sig_a = GeneratorSygnalu(zrodlo_sygnalu=kod_syg_a, czestotliwosc_probkowania=fp, **parametry_a)
                probki_a = np.array([next(sig_a) for _ in range(N_A)])
                typ_a_nazwa = nazwa_syg_a
        except Exception as e:
            messagebox.showerror("Błąd Sygnału A", f"Błąd przy generowaniu Sygnału A: {str(e)}")
            return

        try:
            nazwa_syg_b = self.wybor_sygnalu_b.get()
            if not nazwa_syg_b:
                raise ValueError("Wybierz typ sygnału B!")
            
            kod_syg_b = self.kody_sygnalow[nazwa_syg_b]
            parametry_b = self._pobierz_przetworzone_parametry(self.pola_parametrow_b)
            N_B = int(self.pole_liczba_probek_b.get())
            if N_B <= 0:
                raise ValueError("Liczba próbek N_B must be greater than 0.")
            
            sig_b = GeneratorSygnalu(zrodlo_sygnalu=kod_syg_b, czestotliwosc_probkowania=fp, **parametry_b)
            probki_b = np.array([next(sig_b) for _ in range(N_B)])
        except Exception as e:
            messagebox.showerror("Błąd Sygnału B", f"Błąd przy generowaniu Sygnału B: {str(e)}")
            return

        try:
            if algorytm == "Bezpośrednia":
                korelacja = FiltrSygnalu.korelacja_bezposrednia(probki_a, probki_b)
            else:
                korelacja = FiltrSygnalu.korelacja_z_uzyciem_splotu(probki_a, probki_b)
                
            L = len(korelacja)
            lags = np.arange(L) - (N_B - 1)
            time_lags = lags / fp
            
            self.loguj_wiadomosc(f"--- Obliczono Korelację ({algorytm}) ---")
            self.loguj_wiadomosc(f" Sygnał A: {typ_a_nazwa} (N={N_A})")
            self.loguj_wiadomosc(f" Sygnał B: {nazwa_syg_b} (N={N_B})")
            self.loguj_wiadomosc(f" Krok próbkowania dt: {1.0/fp:.6f} s")
            
            korelacja_abs = np.abs(korelacja)
            max_idx = np.argmax(korelacja_abs)
            max_val = korelacja[max_idx]
            max_lag = lags[max_idx]
            max_time = time_lags[max_idx]
            
            if np.iscomplexobj(max_val):
                max_val_str = f"{max_val.real:.4f} + {max_val.imag:.4f}j"
            else:
                max_val_str = f"{max_val:.4f}"
                
            self.loguj_wiadomosc(f" Długość wyniku: {L}")
            self.loguj_wiadomosc(f" Maksimum korelacji: {max_val_str}")
            self.loguj_wiadomosc(f"   na próbce (lag): {max_lag}")
            self.loguj_wiadomosc(f"   opóźnienie czasowe: {max_time:.6f} s")
            self.loguj_wiadomosc("-" * 35)

            for tab_id in self.notatnik_wizualizacji.tabs():
                if self.notatnik_wizualizacji.tab(tab_id, "text") == "Wyniki Korelacji":
                    self.notatnik_wizualizacji.forget(tab_id)
                    break
                    
            ramka_wynikow = ttk.Frame(self.notatnik_wizualizacji)
            self.notatnik_wizualizacji.add(ramka_wynikow, text="Wyniki Korelacji")
            self.notatnik_wizualizacji.select(ramka_wynikow)
            
            t_a = np.arange(N_A) / fp
            t_b = np.arange(N_B) / fp
            
            wykresy = WizualizatorSygnalu.rysuj_korelacje(t_a, probki_a, t_b, probki_b, lags, korelacja, algorytm)
            
            for tytul, wykres in wykresy:
                plotno = FigureCanvasTkAgg(wykres, master=ramka_wynikow)
                plotno.draw()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                pasek_narzedzi = NavigationToolbar2Tk(plotno, ramka_wynikow)
                pasek_narzedzi.update()
                plotno.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                
            messagebox.showinfo("Sukces", "Korelacja została pomyślnie obliczona i zwizualizowana!")
            
        except Exception as e:
            messagebox.showerror("Błąd korelacji", f"Błąd podczas obliczania korelacji: {str(e)}")
            return
