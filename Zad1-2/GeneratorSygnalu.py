import numpy as np


class GeneratorSygnalu:
    def __init__(self, zrodlo_sygnalu=None, fabryka_generatorow=None, czestotliwosc_probkowania=1000.0, **kwargs):
        self.czestotliwosc_probkowania = czestotliwosc_probkowania
        self.parametry = kwargs
        self.nr_probki = 0

        self.metody = {
            "s1": self._s1_szum_jednostajny,
            "s2": self._s2_szum_gaussowski,
            "s3": self._s3_sinusoidalny,
            "s4": self._s4_sinus_wyprostowany_jednopolowkowo,
            "s5": self._s5_sinus_wyprostowany_dwupolowkowo,
            "s6": self._s6_prostokatny,
            "s7": self._s7_prostokatny_symetryczny,
            "s8": self._s8_trojkatny,
            "s9": self._s9_skok_jednostkowy,
            "s10": self._s10_impuls_jednostkowy,
            "s11": self._s11_szum_impulsowy,
            "s12": self._s12_sygnal_zespolony,
        }

        if fabryka_generatorow is None:
            typ_sygnalu = zrodlo_sygnalu.lower()
            self._fabryka_generatorow = lambda: self.metody[typ_sygnalu](**self.parametry)
        else:
            self._fabryka_generatorow = fabryka_generatorow

        self.aktywny_generator = self._fabryka_generatorow()

    def __iter__(self):
        return self

    def __next__(self):
        wartosc = next(self.aktywny_generator)
        self.nr_probki += 1
        return wartosc

    def dodaj_sygnal(self, inny_sygnal):
        return self._polacz_sygnaly(inny_sygnal, lambda a, b: a + b)

    def odejmij_sygnal(self, inny_sygnal):
        return self._polacz_sygnaly(inny_sygnal, lambda a, b: a - b)

    def pomnoz_sygnal(self, inny_sygnal):
        return self._polacz_sygnaly(inny_sygnal, lambda a, b: a * b)

    def podziel_sygnal(self, inny_sygnal):
        return self._polacz_sygnaly(inny_sygnal, lambda a, b: a / b if b != 0 else 0)

    def resetuj(self):
        self.nr_probki = 0
        self.aktywny_generator = self._fabryka_generatorow()
        return self

    def _polacz_sygnaly(self, inny_sygnal, operacja):
        if isinstance(inny_sygnal, GeneratorSygnalu) and self.czestotliwosc_probkowania != inny_sygnal.czestotliwosc_probkowania:
            raise ValueError(f"Niezgodność czestotliwosci probkowania: {self.czestotliwosc_probkowania} != {inny_sygnal.czestotliwosc_probkowania}. "
                            "Operacje na sygnałach o różnym próbkowaniu są niedozwolone.")

        def fabryka_polaczona():
            if isinstance(inny_sygnal, GeneratorSygnalu):
                g1 = self._fabryka_generatorow()
                g2 = inny_sygnal._fabryka_generatorow()
                return (operacja(v1, v2) for v1, v2 in zip(g1, g2))
            else:
                g1 = self._fabryka_generatorow()
                return (operacja(v1, inny_sygnal) for v1 in g1)

        return GeneratorSygnalu(fabryka_generatorow=fabryka_polaczona, czestotliwosc_probkowania=self.czestotliwosc_probkowania)

    def pobierz_statystyki(self, liczba_probek=None):
        self.resetuj()
        okres = self.parametry.get('okres')

        if okres is not None:
            probki_na_okres = okres * self.czestotliwosc_probkowania
            docelowe_n = liczba_probek if liczba_probek else 1000
            liczba_okresow = max(1, int(docelowe_n / probki_na_okres))

            rzeczywiste_n = int(liczba_okresow * probki_na_okres)

            print(f"> Analiza okresowa: Pobieram {liczba_okresow} pełnych okresów ({rzeczywiste_n} próbek).")
        else:
            rzeczywiste_n = liczba_probek if liczba_probek else 1000
            print(f"> Analiza standardowa: Pobieram {rzeczywiste_n} próbek.")

        probki = np.array([next(self) for _ in range(rzeczywiste_n)])
        self.resetuj()

        if len(probki) == 0:
            return None

        srednia = np.mean(probki)
        srednia_bezwzgledna = np.mean(np.abs(probki))
        moc = np.mean(probki ** 2)
        wariancja = np.var(probki)
        wartosc_skuteczna = np.sqrt(moc)

        return {
            "srednia": srednia,
            "srednia_bezwzgledna": srednia_bezwzgledna,
            "moc": moc,
            "wariancja": wariancja,
            "wartosc_skuteczna": wartosc_skuteczna,
            "liczba_probek": rzeczywiste_n,
            "czas_trwania_sygnalu": rzeczywiste_n / self.czestotliwosc_probkowania
        }

    def _pobierz_czas(self):
        t = 0.0
        dt = 1.0 / self.czestotliwosc_probkowania
        while True:
            yield t
            t += dt

    def _s1_szum_jednostajny(self, amplituda=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                yield np.random.uniform(-amplituda, amplituda)
            else:
                yield 0.0

    def _s2_szum_gaussowski(self, amplituda=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                yield amplituda * np.random.normal(0, 1)
            else:
                yield 0.0

    def _s3_sinusoidalny(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                yield amplituda * np.sin((2 * np.pi / okres) * (t - czas_poczatkowy))
            else:
                yield 0.0

    def _s4_sinus_wyprostowany_jednopolowkowo(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                sinus = np.sin((2 * np.pi / okres) * (t - czas_poczatkowy))
                yield 0.5 * amplituda * ( sinus + np.abs(sinus) )
            else:
                yield 0.0

    def _s5_sinus_wyprostowany_dwupolowkowo(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                yield amplituda * np.abs(np.sin((2 * np.pi / okres) * (t - czas_poczatkowy)))
            else:
                yield 0.0

    def _s6_prostokatny(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, wspolczynnik_wypelnienia=0.5, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                t_wzgledne = (t - czas_poczatkowy) % okres
                yield amplituda if t_wzgledne < wspolczynnik_wypelnienia * okres else 0.0
            else:
                yield 0.0

    def _s7_prostokatny_symetryczny(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, wspolczynnik_wypelnienia=0.5, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                t_wzgledne = (t - czas_poczatkowy) % okres
                yield amplituda if t_wzgledne < wspolczynnik_wypelnienia * okres else -amplituda
            else:
                yield 0.0

    def _s8_trojkatny(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, wspolczynnik_wypelnienia=0.5, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                t_wzgledne = (t - czas_poczatkowy) % okres
                if t_wzgledne < wspolczynnik_wypelnienia * okres:
                    yield (amplituda / (wspolczynnik_wypelnienia * okres)) * t_wzgledne
                else:
                    yield (-amplituda / (okres * (1 - wspolczynnik_wypelnienia))) * (t_wzgledne - wspolczynnik_wypelnienia * okres) + amplituda
            else:
                yield 0.0

    def _s9_skok_jednostkowy(self, amplituda=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, czas_skoku=0.5, **_):
        for t in self._pobierz_czas():
            if t > czas_skoku:
                yield amplituda
            elif t == czas_skoku:
                yield 0.5 * amplituda
            else:
                yield 0.0

    def _s10_impuls_jednostkowy(self, amplituda=1.0, numer_probki_skoku=100, **_):
        n = 0
        while True:
            yield amplituda if n == numer_probki_skoku else 0.0
            n += 1

    def _s11_szum_impulsowy(self, amplituda=1.0, prawdopodobienstwo=0.1, **_):
        while True:
            yield amplituda if np.random.random() < prawdopodobienstwo else 0.0

    def _s12_sygnal_zespolony(self, amplituda=1.0, okres=1.0, czas_poczatkowy=0.0, czas_trwania=1.0, **_):
        for t in self._pobierz_czas():
            if czas_poczatkowy <= t <= czas_poczatkowy + czas_trwania:
                yield amplituda * np.exp(1j * 2 * np.pi * (t - czas_poczatkowy) / okres)
            else:
                yield 0.0 + 0.0j
