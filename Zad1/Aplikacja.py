import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from GeneratorSygnalu import GeneratorSygnalu
from PlikSygnalu import PlikSygnalu
from WizualizatorSygnalu import WizualizatorSygnalu


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

        ramka_generacji_1 = ttk.LabelFrame(lewa_ramka, text="1. Generacja Sygnału Głównego", padding="10")
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

        ramka_operacji = ttk.LabelFrame(lewa_ramka, text="2. Operacje Matematyczne (Opcjonalne)", padding="10")
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

        ramka_akcji = ttk.LabelFrame(lewa_ramka, text="3. Akcje na Głównym Sygnale", padding="10")
        ramka_akcji.pack(fill=tk.BOTH, expand=True, pady=5)

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

        self.pole_tekstowe_logow = tk.Text(ramka_akcji, height=15, state=tk.DISABLED, bg="#3c3f41", fg="#e0e0e0",
                                           insertbackground="#ffffff")
        self.pole_tekstowe_logow.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Button(ramka_akcji, text="Oblicz i Wyświetl Statystyki", command=self.pokaz_statystyki).pack(pady=5)

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
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
