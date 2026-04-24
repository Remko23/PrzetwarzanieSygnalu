import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from GeneratorSygnalu import GeneratorSygnalu
from PlikSygnalu import PlikSygnalu
from WizualizatorSygnalu import WizualizatorSygnalu
from KonwerterSygnalu import KonwerterSygnalu
from FiltrSygnalu import FiltrSygnalu

class Aplikacja(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generator i Analizator Sygnałów")
        self.geometry("1800x800")

        self.zastosuj_ciemny_motyw()

        self.sygnal_glowny = None
        self.czy_dyskretny = False

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
            "s12": "Testowy sygnał zespolony (s12)"
        }

        self.kody_sygnalow = {v: k for k, v in self.typy_sygnalow.items()}

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
        self.wybor_filtru = ttk.Combobox(ramka_filtracji, values=["Dolnoprzepustowy", "Górnoprzepustowy", "Środkowoprzepustowy"], state="readonly", width=20)
        self.wybor_filtru.current(0)
        self.wybor_filtru.grid(row=0, column=1, sticky=tk.W, pady=2, columnspan=3)

        ttk.Label(ramka_filtracji, text="Okno:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.wybor_okna = ttk.Combobox(ramka_filtracji, values=["prostokatne", "hamming", "hanning", "blackman"], state="readonly", width=20)
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
        self.pole_liczba_probek.insert(0, "1000")
        self.pole_liczba_probek.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(ramka_parametrow_globalnych, text="Przedziały histogramu:").grid(row=1, column=0, sticky=tk.W, padx=5,
                                                                                   pady=5)
        self.pole_liczba_przedzialow = ttk.Entry(ramka_parametrow_globalnych, width=10)
        self.pole_liczba_przedzialow.insert(0, "20")
        self.pole_liczba_przedzialow.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Button(ramka_parametrow_globalnych, text="Wizualizuj (Wykres + Histogram)",
                   command=self.wizualizuj_sygnal).grid(row=2, column=0, columnspan=2, pady=10)

        self.pole_tekstowe_logow = tk.Text(ramka_akcji, height=10, state=tk.DISABLED, bg="#3c3f41", fg="#e0e0e0",
                                           insertbackground="#ffffff")
        self.pole_tekstowe_logow.pack(fill=tk.BOTH, expand=True, pady=5)

    def loguj_wiadomosc(self, wiadomosc):
        self.pole_tekstowe_logow.config(state=tk.NORMAL)
        self.pole_tekstowe_logow.insert(tk.END, wiadomosc + "\n")
        self.pole_tekstowe_logow.see(tk.END)
        self.pole_tekstowe_logow.config(state=tk.DISABLED)

    def _zbuduj_interfejs_parametrow(self, ramka_rodzica, slownik_parametrow, kod_sygnalu):
        for widzet in ramka_rodzica.winfo_children():
            widzet.destroy()
        slownik_parametrow.clear()

        if not kod_sygnalu: return

        wymagane_parametry = [('amplituda', 'Amplituda', '1.0')]

        if kod_sygnalu not in ["s10", "s11"]:
            wymagane_parametry.extend([
                ('czas_poczatkowy', 'Czas początkowy', '0.0'),
                ('czas_trwania', 'Czas trwania', '1.0')
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

    def _pobierz_przetworzone_parametry(self, slownik_parametrow):
        przetworzone = {}
        for klucz, pole_wprowadzania in slownik_parametrow.items():
            wartosc_tekstowa = pole_wprowadzania.get()
            try:
                if klucz == 'numer_probki_skoku':
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
            self.sygnal_glowny = GeneratorSygnalu(zrodlo_sygnalu=kod_sygnalu, **parametry)
            self.czy_dyskretny = kod_sygnalu in ["s10", "s11"]
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
            sygnal_2 = GeneratorSygnalu(zrodlo_sygnalu=kod_sygnalu_2, **parametry_2)

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
                                                         czy_dyskretny=self.czy_dyskretny)
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
            
            # Ustawienie początkowej widoczności
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
            K = fp / fo
            
            if rodzaj_filtru == "Dolnoprzepustowy":
                h = FiltrSygnalu.generuj_filtr_dolnoprzepustowy(M, K, okno)
            elif rodzaj_filtru == "Górnoprzepustowy":
                h = FiltrSygnalu.generuj_filtr_gornoprzepustowy(M, K, okno)
            elif rodzaj_filtru == "Środkowoprzepustowy":
                h = FiltrSygnalu.generuj_filtr_srodkowoprzepustowy(M, K, okno)
                
            liczba_probek = int(self.pole_liczba_probek.get())
            self.sygnal_glowny.resetuj()
            probki_x = np.array([next(self.sygnal_glowny) for _ in range(liczba_probek)])
            
            probki_y = FiltrSygnalu.splot(h, probki_x)
            
            self.sygnal_glowny = GeneratorSygnalu.z_tablicy(probki_y, fp)
            self.loguj_wiadomosc(f"Wykonano filtrację: {rodzaj_filtru}, M={M}, fo={fo}, okno={okno}.")
            messagebox.showinfo("Sukces", "Sygnał główny został przefiltrowany. Wykres wizualizacji można odświeżyć.")
            
        except Exception as e:
            messagebox.showerror("Błąd filtracji", str(e))

