import struct
import numpy as np

from GeneratorSygnalu import *

class PlikSygnalu:
    # Format nagłówka: czas_poczatkowy(double), czestotliwosc_probkowania(double), czy_zespolony(int64), liczba_probek(int64)
    FORMAT_NAGLOWKA = 'ddqq'
    ROZMIAR_NAGLOWKA = struct.calcsize(FORMAT_NAGLOWKA)

    @staticmethod
    def zapisz_do_binarnego(nazwa_pliku, generator_sygnalu, liczba_probek):
        generator_sygnalu.resetuj()

        czas_poczatkowy = float(generator_sygnalu.parametry.get('czas_poczatkowy', 0.0))
        czestotliwosc_probkowania = float(generator_sygnalu.czestotliwosc_probkowania)

        probki = []
        for _ in range(liczba_probek):
            probki.append(next(generator_sygnalu))

        tablica_probek = np.array(probki, dtype=np.complex128 if np.iscomplexobj(probki) else np.float64)
        czy_zespolony = 1 if np.iscomplexobj(tablica_probek) else 0

        with open(nazwa_pliku, 'wb') as plik:
            naglowek = struct.pack(PlikSygnalu.FORMAT_NAGLOWKA, czas_poczatkowy, czestotliwosc_probkowania, czy_zespolony, liczba_probek)
            plik.write(naglowek)

            if czy_zespolony:
                plaskie_dane = np.empty(liczba_probek * 2, dtype=np.float64)
                plaskie_dane[0::2] = tablica_probek.real
                plaskie_dane[1::2] = tablica_probek.imag
                plaskie_dane.tofile(plik)
            else:
                tablica_probek.astype(np.float64).tofile(plik)

        print(f"Zapisano sygnał do {nazwa_pliku} (N={liczba_probek}, fs={czestotliwosc_probkowania}Hz, t1={czas_poczatkowy}s)")

    @staticmethod
    def wczytaj_z_binarnego(nazwa_pliku):
        try:
            with open(nazwa_pliku, 'rb') as plik:
                dane_naglowka = plik.read(PlikSygnalu.ROZMIAR_NAGLOWKA)
                if not dane_naglowka: return None

                czas_poczatkowy, czestotliwosc_probkowania, czy_zespolony, liczba_probek = struct.unpack(PlikSygnalu.FORMAT_NAGLOWKA, dane_naglowka)

                if czy_zespolony:
                    surowe_dane = np.fromfile(plik, dtype=np.float64)
                    probki = surowe_dane[0::2] + 1j * surowe_dane[1::2]
                else:
                    probki = np.fromfile(plik, dtype=np.float64)

            def wczytana_fabryka_generatorow():
                for probka in probki:
                    yield probka

            return GeneratorSygnalu(fabryka_generatorow=wczytana_fabryka_generatorow, czestotliwosc_probkowania=czestotliwosc_probkowania, czas_poczatkowy=czas_poczatkowy)
        except Exception as e:
            print(f"Błąd odczytu: {e}")
            return None

    @staticmethod
    def wyswietl_informacje_tekstowe(nazwa_pliku):
        with open(nazwa_pliku, 'rb') as plik:
            dane_naglowka = plik.read(PlikSygnalu.ROZMIAR_NAGLOWKA)
            czas_poczatkowy, czestotliwosc_probkowania, czy_zespolony, liczba_probek = struct.unpack(PlikSygnalu.FORMAT_NAGLOWKA, dane_naglowka)

            print(f"\n--- INFORMACJE O PLIKU: {nazwa_pliku} ---")
            print(f"Czas początkowy:         {czas_poczatkowy} s")
            print(f"Częstotliwość próbk:     {czestotliwosc_probkowania} Hz")
            print(f"Typ wartości:            {'Zespolone' if czy_zespolony else 'Rzeczywiste'}")
            print(f"Liczba próbek:           {liczba_probek}")

            surowe_dane = np.fromfile(plik, dtype=np.float64)

            if czy_zespolony:
                probki = surowe_dane[0::2] + 1j * surowe_dane[1::2]
                print("Początkowe wartości (wymiar zespolony):")
            else:
                probki = surowe_dane
                print("Początkowe wartości (wymiar rzeczywisty):")

            limit = min(len(probki), 10)
            for i, wartosc in enumerate(probki[:limit]):
                if czy_zespolony:
                    print(f"[{i}]: {wartosc.real:+.4f} {wartosc.imag:+.4f}j")
                else:
                    print(f"[{i}]: {wartosc:+.4f}")

            if len(probki) > limit:
                print("...")
