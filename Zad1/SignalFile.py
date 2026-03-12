import struct
import numpy as np

from SignalGenerator import *

class SignalFile:
    # Format nagłówka: t1(double), fs(double), is_complex(int64), n_samples(int64)
    HEADER_FORMAT = 'ddqq'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    @staticmethod
    def save_to_binary(filename, signal_generator, n_samples):
        # Zapisuje sygnał wraz z nagłówkiem do pliku binarnego
        signal_generator.reset()

        # Pobieramy metadane
        t1 = float(signal_generator.params.get('t1', 0.0))
        fs = float(signal_generator.fs)

        # Pobieramy próbki
        samples = []
        for _ in range(n_samples):
            samples.append(next(signal_generator))

        samples_array = np.array(samples, dtype=np.complex128 if np.iscomplexobj(samples) else np.float64)
        is_complex = 1 if np.iscomplexobj(samples_array) else 0

        with open(filename, 'wb') as f:
            # Zapis nagłówka
            header = struct.pack(SignalFile.HEADER_FORMAT, t1, fs, is_complex, n_samples)
            f.write(header)

            # Zapis danych
            if is_complex:
                # Zespolone zapisujemy jako pary (real, imag)
                flat_data = np.empty(n_samples * 2, dtype=np.float64)
                flat_data[0::2] = samples_array.real
                flat_data[1::2] = samples_array.imag
                flat_data.tofile(f)
            else:
                samples_array.astype(np.float64).tofile(f)

        print(f"Zapisano sygnał do {filename} (N={n_samples}, fs={fs}Hz, t1={t1}s)")

    @staticmethod
    def load_from_binary(filename):
        # Odczytuje sygnał i zwraca obiekt SignalGenerator
        try:
            with open(filename, 'rb') as f:
                header_data = f.read(SignalFile.HEADER_SIZE)
                if not header_data: return None

                t1, fs, is_complex, n_samples = struct.unpack(SignalFile.HEADER_FORMAT, header_data)

                if is_complex:
                    raw_data = np.fromfile(f, dtype=np.float64)
                    samples = raw_data[0::2] + 1j * raw_data[1::2]
                else:
                    samples = np.fromfile(f, dtype=np.float64)

            # Tworzymy fabrykę, która pozwoli na resetowanie załadowanego sygnału
            def loaded_gen_factory():
                for s in samples:
                    yield s

            return SignalGenerator(gen_factory=loaded_gen_factory, fs=fs, t1=t1)
        except Exception as e:
            print(f"Błąd odczytu: {e}")
            return None

    @staticmethod
    def print_text_info(filename):
        # Prezentacja danych z pliku w postaci tekstowej
        with open(filename, 'rb') as f:
            header_data = f.read(SignalFile.HEADER_SIZE)
            t1, fs, is_complex, n_samples = struct.unpack(SignalFile.HEADER_FORMAT, header_data)

            print(f"\n--- INFORMACJE O PLIKU: {filename} ---")
            print(f"Czas początkowy (t1):    {t1} s")
            print(f"Częstotliwość (fs):     {fs} Hz")
            print(f"Typ wartości:           {'Zespolone' if is_complex else 'Rzeczywiste'}")
            print(f"Liczba próbek:          {n_samples}")

            # Wczytanie surowych danych
            raw_data = np.fromfile(f, dtype=np.float64)

            if is_complex:
                # Rekonstrukcja liczb zespolonych
                samples = raw_data[0::2] + 1j * raw_data[1::2]
                print("Początkowe wartości (część zespolona):")
            else:
                samples = raw_data
                print("Początkowe wartości (część rzeczywista):")

            # Wyświetlanie pierwszych 10 próbek
            limit = min(len(samples), 10)
            for i, val in enumerate(samples[:limit]):
                if is_complex:
                    # Ładne formatowanie liczb zespolonych
                    print(f"[{i}]: {val.real:+.4f} {val.imag:+.4f}j")
                else:
                    print(f"[{i}]: {val:+.4f}")

            if len(samples) > limit:
                print("...")
