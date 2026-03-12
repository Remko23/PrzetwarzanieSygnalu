# Generacja sygnału i szumu

import numpy as np
import json

from SignalGenerator import *
from SignalFile import *
from SignalVisualizer import *

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from SignalGenerator import SignalGenerator
from SignalFile import SignalFile
from SignalVisualizer import SignalVisualizer


class SignalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generator i Analizator Sygnałów")
        self.geometry("1800x800")

        self.apply_dark_theme()

        self.signal1 = None
        self.is_discrete = False
        
        # Słownik z nazwami sygnałów
        self.signal_types = {
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
        
        # Odwrotne mapowanie (Nazwa -> Kod)
        self.signal_codes = {v: k for k, v in self.signal_types.items()}

        self.create_widgets()

    def apply_dark_theme(self):
        # Konfiguracja tła standardowego okna
        self.configure(bg="#2b2b2b")
        
        style = ttk.Style(self)
        try:
            # W miarę możliwości startujemy z clam, który dobrze się poddaje stylowaniu
            style.theme_use("clam")
        except:
            pass

        # Główne kolory
        bg_col = "#2b2b2b"
        fg_col = "#e0e0e0"
        btn_bg = "#3c3f41"
        btn_active = "#4b4e50"
        entry_bg = "#3c3f41"
        entry_fg = "#ffffff"

        # Tła ramek i etykiet
        style.configure("TFrame", background=bg_col)
        style.configure("TLabel", background=bg_col, foreground=fg_col)
        style.configure("TLabelframe", background=bg_col, foreground=fg_col)
        style.configure("TLabelframe.Label", background=bg_col, foreground=fg_col, font=("Arial", 10, "bold"))

        # Przycisk (Button)
        style.configure("TButton", 
                        background=btn_bg, foreground=fg_col, 
                        borderwidth=1, focusthickness=3, focuscolor='none')
        style.map("TButton",
                  background=[("active", btn_active), ("pressed", "#5a5d5f")])

        # Pola wyboru i wejścia textowego
        style.configure("TCombobox", 
                        fieldbackground=entry_bg, background=btn_bg, foreground=entry_fg, 
                        arrowcolor=fg_col)
        style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)

        # PanedWindow & Notebook
        style.configure("TPanedwindow", background=bg_col)
        style.configure("TNotebook", background=bg_col, borderwidth=0)
        style.configure("TNotebook.Tab", background=btn_bg, foreground=fg_col, padding=[5, 2])
        style.map("TNotebook.Tab",
                  background=[("selected", "#505050")], 
                  expand=[("selected", [1, 1, 1, 0])])

    def create_widgets(self):
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=6)
        
        # Notebook na wykresy po prawej
        self.viz_notebook = ttk.Notebook(right_frame)
        self.viz_notebook.pack(fill=tk.BOTH, expand=True)

        # --- SEKCJA: GENERACJA SYGNAŁU GŁÓWNEGO ---
        lf_gen1 = ttk.LabelFrame(left_frame, text="1. Generacja Sygnału Głównego", padding="10")
        lf_gen1.pack(fill=tk.X, pady=5)

        ttk.Label(lf_gen1, text="Wybierz sygnał:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_sig1 = ttk.Combobox(lf_gen1, values=list(self.signal_types.values()), state="readonly", width=38)
        self.combo_sig1.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.combo_sig1.bind("<<ComboboxSelected>>", self.on_sig1_selected)

        # Ramka na parametry dla wybranego sygnału
        self.frame_params1 = ttk.Frame(lf_gen1)
        self.frame_params1.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.param_entries1 = {}

        self.btn_gen1 = ttk.Button(lf_gen1, text="Generuj Sygnał Głównego", command=self.generate_signal1)
        self.btn_gen1.grid(row=2, column=0, columnspan=2, pady=10)

        # --- SEKCJA: OPERACJE MATEMATYCZNE ---
        lf_op = ttk.LabelFrame(left_frame, text="2. Operacje Matematyczne (Opcjonalne)", padding="10")
        lf_op.pack(fill=tk.X, pady=5)

        ttk.Label(lf_op, text="Wybierz operację:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_op = ttk.Combobox(lf_op, values=["Dodawanie (add)", "Odejmowanie (sub)", "Mnożenie (mul)", "Dzielenie (div)"], state="readonly", width=20)
        self.combo_op.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(lf_op, text="Wybierz sygnał 2:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_sig2 = ttk.Combobox(lf_op, values=list(self.signal_types.values()), state="readonly", width=38)
        self.combo_sig2.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.combo_sig2.bind("<<ComboboxSelected>>", self.on_sig2_selected)

        # Ramka na parametry dla drugiego sygnału
        self.frame_params2 = ttk.Frame(lf_op)
        self.frame_params2.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.param_entries2 = {}

        self.btn_op = ttk.Button(lf_op, text="Wykonaj Operację na Głównym Sygnale", command=self.execute_operation)
        self.btn_op.grid(row=3, column=0, columnspan=2, pady=10)

        # --- SEKCJA: AKCJE I WIZUALIZACJA ---
        lf_actions = ttk.LabelFrame(left_frame, text="3. Akcje na Głównym Sygnale", padding="10")
        lf_actions.pack(fill=tk.BOTH, expand=True, pady=5)

        # Przyciski akcji
        action_btns_frame = ttk.Frame(lf_actions)
        action_btns_frame.pack(fill=tk.X, pady=5)

        ttk.Button(action_btns_frame, text="Zapisz do pliku", command=self.save_signal).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_btns_frame, text="Wczytaj z pliku", command=self.load_signal).pack(side=tk.LEFT, padx=5)

        # Parametry globalne (wizualizacja/zapis)
        global_params_frame = ttk.Frame(lf_actions)
        global_params_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(global_params_frame, text="Liczba próbek w oknie (n_samples):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.entry_samples = ttk.Entry(global_params_frame, width=10)
        self.entry_samples.insert(0, "1000")
        self.entry_samples.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(global_params_frame, text="Przedziały histogramu (n_bins):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_bins = ttk.Entry(global_params_frame, width=10)
        self.entry_bins.insert(0, "20")
        self.entry_bins.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Button(global_params_frame, text="Wizualizuj (Wykres + Histogram)", command=self.visualize_signal).grid(row=2, column=0, columnspan=2, pady=10)

        # Obszar tekstowy na logi i statystyki. Tu sterujemy kolorami z obiektu bazowego tk (Text nie jest użyteczne via ttk)
        self.txt_output = tk.Text(lf_actions, height=15, state=tk.DISABLED, bg="#3c3f41", fg="#e0e0e0", insertbackground="#ffffff")
        self.txt_output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(lf_actions, text="Oblicz i Wyświetl Statystyki", command=self.show_statistics).pack(pady=5)

    def log_message(self, message):
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.insert(tk.END, message + "\n")
        self.txt_output.see(tk.END)
        self.txt_output.config(state=tk.DISABLED)

    def _build_params_ui(self, parent_frame, param_dict, signal_code):
        # Czyścimy starą zawartość
        for widget in parent_frame.winfo_children():
            widget.destroy()
        param_dict.clear()

        if not signal_code: return

        # Definicja parametrów wymaganych dla danego sygnału
        required_params = [('A', 'Amplituda', '1.0')]
        
        if signal_code not in ["s10", "s11"]:
            required_params.extend([
                ('t1', 'Czas początkowy (t1)', '0.0'),
                ('d', 'Czas trwania (d)', '1.0')
            ])
            if signal_code in ["s3", "s4", "s5", "s6", "s7", "s8", "s12"]:
                required_params.append(('T', 'Okres (T)', '1.0'))
            if signal_code in ["s6", "s7", "s8"]:
                required_params.append(('kw', 'Wsp. wypełnienia (kw)', '0.5'))
            if signal_code == "s9":
                required_params.append(('ts', 'Czas skoku (ts)', '0.5'))
        else:
            if signal_code == "s10":
                required_params.append(('ns', 'Próbka skoku (ns)', '100'))
            if signal_code == "s11":
                required_params.append(('p', 'Prawd. skoku (p)', '0.1'))

        for i, (p_key, p_label, default_val) in enumerate(required_params):
            ttk.Label(parent_frame, text=p_label+":").grid(row=i//4, column=(i%4)*2, padx=2, pady=2, sticky=tk.E)
            entry = ttk.Entry(parent_frame, width=8)
            entry.insert(0, default_val)
            entry.grid(row=i//4, column=(i%4)*2+1, padx=2, pady=2, sticky=tk.W)
            param_dict[p_key] = entry

    def on_sig1_selected(self, event):
        sig_name = self.combo_sig1.get()
        sig_code = self.signal_codes.get(sig_name)
        self._build_params_ui(self.frame_params1, self.param_entries1, sig_code)

    def on_sig2_selected(self, event):
        sig_name = self.combo_sig2.get()
        sig_code = self.signal_codes.get(sig_name)
        self._build_params_ui(self.frame_params2, self.param_entries2, sig_code)

    def _get_parsed_params(self, param_dict):
        parsed = {}
        for key, entry in param_dict.items():
            val_str = entry.get()
            try:
                # Ograniczenie - ns jest intem
                if key == 'ns':
                    parsed[key] = int(val_str)
                else:
                    parsed[key] = float(val_str)
            except ValueError:
                raise ValueError(f"Nieprawidłowa wartość dla parametru '{key}': {val_str}")
        return parsed

    def generate_signal1(self):
        sig_name = self.combo_sig1.get()
        if not sig_name:
            messagebox.showwarning("Uwaga", "Wybierz typ sygnału głównego!")
            return

        sig_code = self.signal_codes[sig_name]
        try:
            params = self._get_parsed_params(self.param_entries1)
            self.signal1 = SignalGenerator(signal_source=sig_code, **params)
            self.is_discrete = sig_code in ["s10", "s11"]
            self.log_message(f"Wygenerowano sygnał główny: {sig_name} z parametrami {params}")
            messagebox.showinfo("Sukces", "Sygnał główny został utworzony.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def execute_operation(self):
        if not self.signal1:
            messagebox.showerror("Błąd", "Najpierw wygeneruj sygnał główny!")
            return

        op_str = self.combo_op.get()
        sig2_name = self.combo_sig2.get()

        if not op_str or not sig2_name:
            messagebox.showwarning("Uwaga", "Wybierz operację oraz drugi sygnał!")
            return

        sig2_code = self.signal_codes[sig2_name]
        try:
            params2 = self._get_parsed_params(self.param_entries2)
            signal2 = SignalGenerator(signal_source=sig2_code, **params2)

            if "add" in op_str:
                self.signal1 = self.signal1 + signal2
            elif "sub" in op_str:
                self.signal1 = self.signal1 - signal2
            elif "mul" in op_str:
                self.signal1 = self.signal1 * signal2
            elif "div" in op_str:
                self.signal1 = self.signal1 / signal2

            # Jeżeli operacja dotyczy sygnałów dyskretnych
            self.is_discrete = self.is_discrete or (sig2_code in ["s10", "s11"])

            self.log_message(f"Wykonano operację '{op_str}' z sygnałem {sig2_name}.")
            messagebox.showinfo("Sukces", "Zaktualizowano sygnał główny operatorem.")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def save_signal(self):
        if not self.signal1:
            messagebox.showerror("Błąd", "Brak wygenerowanego sygnału do zapisu!")
            return
        
        try:
            n_samples = int(self.entry_samples.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek (n_samples).")
            return

        fname = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Pliki Binarne", "*.bin"), ("Wszystkie pliki", "*.*")])
        if fname:
            try:
                SignalFile.save_to_binary(fname, self.signal1, n_samples)
                self.log_message(f"Zapisano sygnał do pliku: {fname} (N={n_samples})")
                messagebox.showinfo("Sukces", f"Zapisano pomyślnie do {fname}")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def load_signal(self):
        fname = filedialog.askopenfilename(filetypes=[("Pliki Binarne", "*.bin"), ("Wszystkie pliki", "*.*")])
        if fname:
            try:
                loaded_sig = SignalFile.load_from_binary(fname)
                if loaded_sig:
                    self.signal1 = loaded_sig
                    self.log_message(f"Wczytano sygnał z pliku: {fname}")
                    # Wywołuje logowanie nagłówka też na UI
                    self.log_message(f"(Zobacz konsolę / odczytywanie binarne)")
                    SignalFile.print_text_info(fname)
                    messagebox.showinfo("Sukces", "Sygnał został pomyślnie wczytany.")
                else:
                    messagebox.showerror("Błąd", "Plik błęny lub pusty.")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def visualize_signal(self):
        if not self.signal1:
            messagebox.showerror("Błąd", "Najpierw wygeneruj lub wczytaj sygnał główny!")
            return
        
        try:
            samples = int(self.entry_samples.get())
            bins = int(self.entry_bins.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek lub binów.")
            return

        try:
            # Czyszczenie starych zakładek
            for tab in self.viz_notebook.tabs():
                self.viz_notebook.forget(tab)

            # Pobranie objętków wykresów Figure z SignalVisualizer
            figs = SignalVisualizer.plot_all(self.signal1, n_samples=samples, n_bins=bins, is_discrete=self.is_discrete)
            self.signal1.reset()

            for title, fig in figs:
                frame = ttk.Frame(self.viz_notebook)
                self.viz_notebook.add(frame, text=title)

                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                toolbar = NavigationToolbar2Tk(canvas, frame)
                toolbar.update()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            self.log_message(f"Wyświetlono wizualizację na {samples} próbkach i {bins} przedziałach.")
        except Exception as e:
            messagebox.showerror("Błąd wizualizacji", str(e))

    def show_statistics(self):
        if not self.signal1:
            messagebox.showerror("Błąd", "Najpierw wygeneruj lub wczytaj sygnał główny!")
            return

        try:
            samples = int(self.entry_samples.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa liczba próbek.")
            return

        try:
            stats = self.signal1.get_stats(n_samples=samples)
            if not stats:
                self.log_message("Sygnał jest pusty lub niemożliwy do przeanalizowania.")
                return

            self.log_message(f"--- Statystyki sygnału ({samples} próbek) ---")
            for k, v in stats.items():
                if isinstance(v, (complex, np.complex128)):
                    val_str = f"{v.real:.4f} + {v.imag:.4f}j"
                else:
                    val_str = f"{v:.4f}"
                self.log_message(f" {k:<15}: {val_str}")
            self.log_message("-" * 35)
        except Exception as e:
            messagebox.showerror("Błąd", str(e))


if __name__ == "__main__":
    app = SignalApp()
    app.mainloop()

