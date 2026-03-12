# Generacja sygnału i szumu

import numpy as np
import json

from SignalGenerator import *
from SignalFile import *
from SignalVisualizer import *

def print_menu():
    print("\n--- GENERATOR SYGNAŁÓW (MENU) ---")
    print("1. Wybierz sygnał podstawowy (S1-S11)")
    print("2. Wykonaj operację (D1-D4) na dwóch sygnałach")
    print("3. Zapisz sygnał do pliku binarnego")
    print("4. Odczytaj sygnał z pliku binarnego")
    print("5. Wizualizacja (Wykres + Histogram)")
    print("6. Statystyki wybranego sygnału podstawowego")
    print("7. Wyjdź")


def get_params(signal_type):
    print("Podaj par1ametry (pozostaw puste dla domyślnych):")
    params = {}

    # if signal_type in ["s1", "s2", "s3", "s4", "s5"]:
    params['A'] = float(input("Amplituda (A) [1.0]: ") or 1.0)

    if signal_type not in ["s10", "s11"]:
        params['t1'] = float(input("Czas początkowy (t1) [0.0]: ") or 0.0)
        params['d'] = float(input("Czas trwania (d) [1.0]: ") or 1.0)

        if signal_type in ["s3", "s4", "s5", "s6", "s7", "s8", "s12"]:
            params['T'] = float(input("Okres (T) [1.0]: ") or 1.0)

        if signal_type in ["s6", "s7", "s8"]:
            params['kw'] = float(input("Współczynnik wypełnienia (kw) [0.5]: ") or 0.5)

        if signal_type in ["s9"]:
            params['ts'] = float(input("ts [0.5]: ") or 0.5)
    else:
        if signal_type in ["s10"]:
            params['ns'] = int(input("Numer próbki skoku amplitudy [100]: ") or 100)
        if signal_type in ["s11"]:
            params['p'] = float(input("Prawdopodobieństwo wystąpienia skoku [0.1]: ") or 0.1)

    return params


def print_stats(stats):
    print(f"\n{'PARAMETR':<25} | {'WARTOŚĆ'}")
    print("-" * 45)
    for k, v in stats.items():
        if isinstance(v, (complex, np.complex128)):
            val_str = f"{v.real:.4f} + {v.imag:.4f}j"
        else:
            val_str = f"{v:.4f}"
        print(f"{k:<25} | {val_str}")


def main():
    signal1 = None
    is_discrete = False

    while True:
        print_menu()
        choice = input("Wybierz opcję: ")

        if choice == '1':
            print("Dostępne: s1(szum uni), s2(szum gauss), s3(sin), s6(prostokat), s8(trojkat), s9(skok)...")
            stype1 = input("Wpisz kod sygnału (np. s3): ")

            is_discrete = stype1 in ["s10", "s11"]

            params = get_params(stype1)
            signal1 = SignalGenerator(signal_source=stype1, **params)
            print("Sygnał utworzony.")

        elif choice == '2':
            if not signal1:
                print("Najpierw utwórz sygnał główny!")
                continue
            print("Dostępne operacje: add, sub, mul, div")
            op = input("Typ operacji: ")
            stype2 = input("Wpisz kod drugiego sygnału (np. s2): ")

            is_discrete = stype2 in ["s10", "s11"]

            signal2 = SignalGenerator(signal_source=stype2, **get_params(stype2))

            if op == 'add':
                signal1 = signal1 + signal2
            elif op == 'sub':
                signal1 = signal1 - signal2
            elif op == 'mul':
                signal1 = signal1 * signal2
            elif op == 'div':
                signal1 = signal1 / signal2
            print("Operacja wykonana.")

        elif choice == '3':
            if not signal1:
                print("Brak sygnału!")
                continue
            fname = input("Nazwa pliku (np. wynik.bin): ")
            n = int(input("Liczba próbek [1000]: ") or 1000)
            SignalFile.save_to_binary(fname, signal1, n)

        elif choice == '4':
            fname = input("Nazwa pliku do odczytu: ")
            signal1 = SignalFile.load_from_binary(fname)
            SignalFile.print_text_info(fname)

        elif choice == '5':
            if not signal1:
                print("Brak sygnału!")
                continue
            samples = int(input("Ile próbek wizualizować? [1000]: ") or 1000)
            bins = int(input("Podaj ilość przedziałów histogramu (binów) (np. 5, 10, 20) [20]: ") or 20)
            SignalVisualizer.plot_all(signal1, n_samples = samples, n_bins = bins, is_discrete = is_discrete)
            signal1.reset()

        elif choice == '6':
            if not signal1:
                print("Brak sygnału")
                continue
            samples = int(input("Ile próbek analizować? [1000]: ") or 1000)
            stats = signal1.get_stats(n_samples = samples)
            print_stats(stats)

        elif choice == '7':
            break


if __name__ == "__main__":
    main()
