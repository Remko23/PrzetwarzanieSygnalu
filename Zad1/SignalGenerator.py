import numpy as np


class SignalGenerator:
    def __init__(self, signal_source=None, gen_factory=None, fs=1000.0, **kwargs):
        self.fs = fs
        self.params = kwargs
        # licznik próbek
        self.n = 0

        self.methods = {
            # sygnały ciągłe
            "s1": self._s1_uniform_noise,
            "s2": self._s2_gaussian_noise,
            "s3": self._s3_sine,
            "s4": self._s4_half_rectified_sine,
            "s5": self._s5_full_rectified_sine,
            "s6": self._s6_rectangular,
            "s7": self._s7_symmetrical_rectangular,
            "s8": self._s8_triangular,
            "s9": self._s9_unit_step,
            # sygnały dyskretne
            "s10": self._s10_unit_impulse,
            "s11": self._s11_impulse_noise,
            # sygnały zespolone
            "s12": self._s12_complex_sine,
        }

        if gen_factory is None:
            stype = signal_source.lower()
            self._gen_factory = lambda: self.methods[stype](**self.params)
        else:
            self._gen_factory = gen_factory

        self.active_gen = self._gen_factory()

    def __iter__(self):
        return self

    def __next__(self):
        val = next(self.active_gen)
        self.n += 1
        return val

    def __add__(self, other):
        return self._combine(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self._combine(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self._combine(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self._combine(other, lambda a, b: a / b if b != 0 else 0)

    def reset(self):
        self.n = 0
        self.active_gen = self._gen_factory()
        return self

    def _combine(self, other, op):
        if isinstance(other, SignalGenerator) and self.fs != other.fs:
            raise ValueError(f"Niezgodność fs: {self.fs} != {other.fs}. "
                            "Operacje na sygnałach o różnym próbkowaniu są niedozwolone.")

        def combined_factory():
            if isinstance(other, SignalGenerator):
                g1 = self._gen_factory()
                g2 = other._gen_factory()
                return (op(v1, v2) for v1, v2 in zip(g1, g2))
            else:
                g1 = self._gen_factory()
                return (op(v1, other) for v1 in g1)

        return SignalGenerator(gen_factory=combined_factory, fs=self.fs)

    # --- Obliczanie statystyk ---
    def get_stats(self, n_samples=None):
        self.reset()

        # Pobieramy okres T z parametrów, jeśli istnieje
        T = self.params.get('T')

        if T is not None:
            # Obliczamy ile próbek przypada na jeden pełny okres
            samples_per_period = T * self.fs

            # Wyznaczamy liczbę pełnych okresów, które zmieszczą się w zadanej liczbie próbek
            # Jeśli użytkownik nie podał n_samples, weźmiemy domyślnie np. 1000
            target_n = n_samples if n_samples else 1000
            num_periods = max(1, int(target_n / samples_per_period))

            # Ostateczna liczba próbek będąca całkowitą wielokrotnością okresu
            actual_n = int(num_periods * samples_per_period)

            print(f"> Analiza okresowa: Pobieram {num_periods} pełnych okresów ({actual_n} próbek).")
        else:
            # Dla sygnałów nieokresowych (szumy, skoki) bierzemy n_samples
            actual_n = n_samples if n_samples else 1000
            print(f"> Analiza standardowa: Pobieram {actual_n} próbek.")

        # Pobieranie próbek
        samples = np.array([next(self) for _ in range(actual_n)])
        self.reset()

        if len(samples) == 0:
            return None

        mean = np.mean(samples)
        abs_mean = np.mean(np.abs(samples))
        power = np.mean(samples ** 2)
        variance = np.var(samples)
        rms = np.sqrt(power)

        return {
            "mean": mean,
            "abs_mean": abs_mean,
            "power": power,
            "variance": variance,
            "rms": rms,
            "n": actual_n,
            "duration": actual_n / self.fs
        }

    # --- Implementacja Sygnałów (S1-S11) ---

    def _get_time(self):
        t = 0.0
        dt = 1.0 / self.fs
        while True:
            yield t
            t += dt

    def _s1_uniform_noise(self, A=1.0, t1=0.0, d=1.0, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                yield np.random.uniform(-A, A)
            else:
                yield 0.0

    def _s2_gaussian_noise(self, A=1.0, t1=0.0, d=1.0, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                yield A * np.random.normal(0, 1)
            else:
                yield 0.0

    def _s3_sine(self, A=1.0, T=1.0, t1=0.0, d=1.0, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                yield A * np.sin((2 * np.pi / T) * (t - t1))
            else:
                yield 0.0

    def _s4_half_rectified_sine(self, A=1.0, T=1.0, t1=0.0, d=1.0, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                sine = np.sin((2 * np.pi / T) * (t - t1))
                yield 0.5 * A * ( sine + np.abs(sine) )
            else:
                yield 0.0

    def _s5_full_rectified_sine(self, A=1.0, T=1.0, t1=0.0, d=1.0, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                yield A * np.abs(np.sin((2 * np.pi / T) * (t - t1)))
            else:
                yield 0.0

    def _s6_rectangular(self, A=1.0, T=1.0, t1=0.0, d=1.0, kw=0.5, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                t_rel = (t - t1) % T
                yield A if t_rel < kw * T else 0.0
            else:
                yield 0.0

    def _s7_symmetrical_rectangular(self, A=1.0, T=1.0, t1=0.0, d=1.0, kw=0.5, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                t_rel = (t - t1) % T
                yield A if t_rel < kw * T else -A
            else:
                yield 0.0

    def _s8_triangular(self, A=1.0, T=1.0, t1=0.0, d=1.0, kw=0.5, **_):
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                t_rel = (t - t1) % T
                if t_rel < kw * T:
                    yield (A / (kw * T)) * t_rel
                else:
                    yield (-A / (T * (1 - kw))) * (t_rel - kw * T) + A
            else:
                yield 0.0

    def _s9_unit_step(self, A=1.0, t1=0.0, d=1.0, ts=0.5, **_):
        for t in self._get_time():
            if t > ts:
                yield A
            elif t == ts:
                yield 0.5 * A
            else:
                yield 0.0

    def _s10_unit_impulse(self, A=1.0, ns=100, **_):
        n = 0
        while True:
            yield A if n == ns else 0.0
            n += 1

    def _s11_impulse_noise(self, A=1.0, p=0.1, **_):
        while True:
            yield A if np.random.random() < p else 0.0

    def _s12_complex_sine(self, A=1.0, T=1.0, t1=0.0, d=1.0, **_):
        # test - sygnał zespolony
        for t in self._get_time():
            if t1 <= t <= t1 + d:
                yield A * np.exp(1j * 2 * np.pi * (t - t1) / T)
            else:
                yield 0.0 + 0.0j
