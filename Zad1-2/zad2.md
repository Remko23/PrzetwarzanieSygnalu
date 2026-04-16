# Cyfrowe przetwarzanie sygnału - Zadanie 2

## Próbkowanie i kwantyzacja

Celem ćwiczenia jest zapoznanie się z praktycznymi aspektami procesu konwersji analogowo-cyfrowej (A/C) i cyfrowo-analogowej (C/A) sygnałów. Zadanie polega na zaimplementowaniu procesu przetwarzania analogowo-cyfrowego z uwzględnieniem operacji próbkowania i kwantyzacji oraz konwersji odwrotnej, tj. cyfrowo-analogowej.

### Dostępne warianty:
* **Konwersja A/C - próbkowanie**
  * (S1) Próbkowanie równomierne
* **Konwersja A/C - kwantyzacja**
  * (Q1) Kwantyzacja równomierna z obcięciem
  * (Q2) Kwantyzacja równomierna z zaokrąglaniem
* **Konwersja C/A - rekonstrukcja sygnału**
  * (R1) Ekstrapolacja zerowego rzędu
  * (R2) Interpolacja pierwszego rzędu
  * (R3) Rekonstrukcja w oparciu o funkcję sinc

Istotność zasadniczych parametrów konwersji A/C, czyli częstotliwości próbkowania i progu kwantyzacji oraz wyboru metody interpolacji sygnału podczas konwersji C/A należy ocenić porównując sygnał zrekonstruowany z sygnałem oryginalnym. Możliwość obiektywnej oceny skutków konwersji wymaga zdefiniowania odpowiednich miar podobieństwa sygnałów. W ramach realizacji ćwiczenia należy zaimplementować wszystkie poniższe miary:
* (C1) Błąd średniokwadratowy (MSE)
* (C2) Stosunek sygnał szum (SNR)
* (C3) Szczytowy stosunek sygnał - szum (PSNR)
* (C4) Maksymalna różnica (MD)

> **Uwaga:** Porównania powinny być realizowane osobno dla procesu próbkowania i kwantyzacji. W przypadku próbkowania sygnał zrekonstruowany na podstawie ciągu próbek porównywany jest z sygnałem oryginalnym ¹. Należy przedstawić wyniki dla różnych sygnałów zwracając szczególną uwagę na zależność między częstotliwością sygnału, a częstotliwością jego próbkowania. W przypadku kwantyzacji, skwantowany ciąg próbek sygnału porównujemy z tym samym ciągiem w postaci oryginalnej (sprzed kwantyzacji). Należy przedstawić wyniki dla różnych sygnałów i różnej liczby poziomów kwantyzacji.

¹ Z uwagi na możliwość praktycznej implementacji miar podobieństwa oba sygnały muszą być również reprezentowane w postaci dyskretnej (oczywiście, ich dyskretyzacja powinna być "dokładniejsza", tzn. powinna wykorzystywać krótszy okres próbkowania niż miało to miejsce podczas określania ciągu próbek do rekonstrukcji).

Uzyskane wartości SNR porównać z wartościami teoretycznymi dla określonej liczby bitów reprezentacji stałoprzecinkowej, obliczyć wartość ENOB.

Rozważając kwestię próbkowania sygnału (dolnopasmowego) z częstotliwością próbkowania $f_{s}$ zakładamy, że użyteczne pasmo sygnału jest ograniczone do przedziału $(-\frac{f_{x}}{2},\frac{f_{x}}{2})$. Częstotliwość $\frac{f_{z}}{2}$ nosi nazwę częstotliwości Nyquista.

W przeciwnym wypadku, tj. jeśli sygnał będzie zawierał składową $f_{d}$ o częstotliwości większej od połowy częstotliwości próbkowania, będzie to powodować zniekształcenie (osłabienie, bądź wzmocnienie) pewnej składowej o częstotliwości $f_{0}$ leżącej w paśmie użytecznym. Zjawisko to nazywamy aliasingiem ², ponieważ wyraża się ono faktycznym utożsamieniem ze sobą składowych $f_{0}$ i $f_{d}$. Należy zademonstrować to zjawisko określając odpowiednią wartość $f_{d}$ dla zadanej częstotliwości $f_{0}$ sygnału sinusoidalnego i częstotliwości próbkowania $f_{s}$:
* (A1) $f_{0}=100Hz$, $f_{s}=1000Hz$
* (A2) $f_{0}=440Hz$, $f_{s}=22050Hz$
* (A3) $f_{0}=220Hz$, $f_{s}=44100Hz$

² W praktyce, w celu uniknięcia skutków aliasingu składowe leżące poza pasmem użytecznym filtruje się za pomocą analogowego filtru dolnoprzepustowego przed próbkowaniem.

> **Uwaga:** Uzyskane wyniki należy przedstawić na wykresach, z uwzględnieniem kilku różnych wartości amplitudy sygnału o częstotliwości $f_{d}$ przy ustalonej amplitudzie sygnału użytecznego $f_{0}$.

---

## Uwagi ogólne

Proces próbkowania pozwala na zamianę wejściowego sygnału analogowego $f(t)$ na sygnał dyskretny:
$$x(n)=f(nT_{s})$$
reprezentowany jako ciąg próbek rozmieszczonych równomiernie w czasie w odstępach $T_{s}$. Twierdzenie o próbkowaniu określa możliwość odtworzenia oryginalnego sygnału analogowego przy założeniu, że częstotliwość próbkowania:
$$f_{s}=\frac{1}{T_{s}}$$
jest przynajmniej dwukrotnie wyższa niż najwyższa częstotliwość jakiejkolwiek składowej sygnału.

Najprostsza metoda rekonstrukcji sygnału oparta jest na ekstrapolacji zerowego rzędu (ZOH, ang. *zero-order hold*), w której wartość próbki jest pamiętana i definiuje stałą wartość sygnału wyjściowego aż do nadejścia próbki następnej. Zastosowanie tej metody wymaga zwykle użycia znacznie wyższej częstotliwości próbkowania niż wynikałoby to z twierdzenia o próbkowaniu. Redukcję widocznego na Rysunku 1 efektu „schodków" uzyskuje się w praktyce za pomocą odpowiednich filtrów wygładzających. Lepsze efekty można osiągnąć stosując interpolację pierwszego rzędu (FOH, ang. *first-order hold*), w której wartości sygnału pomiędzy sąsiednimi próbkami interpoluje się za pomocą odcinków prostej (Rysunek 2).

* **Rysunek 1:** Metoda zero-order hold. Kolorem zielonym zaznaczono sygnał oryginalny, kolorem niebieskim jego rekonstrukcję.
* **Rysunek 2:** Metoda first-order hold. Kolorem zielonym zaznaczono sygnał oryginalny, kolorem niebieskim jego rekonstrukcję.

Metodą umożliwiającą teoretycznie dowolnie dokładne odtworzenie sygnału analogowego jest zastosowanie wzoru interpolacyjnego:
$$x(t)=\sum_{n=-\infty}^{\infty}x(nT_{s})sinc(t/T_{s}-n)$$
gdzie znormalizowana funkcja sinc (od łac. sinus cardinalis) zdefiniowana jest jako:
$$sinc(t)=\begin{matrix}\frac{\sin(\pi t)}{\pi t}&;\text{dla }x\ne0\\ 1&;\text{dla }x=0\end{matrix}$$
W praktycznej realizacji granice sumowania są ograniczone, przy czym liczba uwzględnianych próbek jest parametrem metody (należy przeprowadzić testy dla kilku różnych wartości).

Zjawisko aliasingu występuje w przypadku każdej częstotliwości sygnału $f_{0}$ i każdej częstotliwości próbkowania $f_{s}$. Wyraża się ono tym, że niemożliwe jest odróżnienie spróbkowanego sygnału o częstotliwości $f_{0}$ od sygnału o częstotliwości $f_{d}=f_{0}+kf_{s}$, gdzie $k$ jest dowolną liczbą całkowitą. Warto zauważyć, że dla $k<0$ możemy otrzymać sygnał o częstotliwości ujemnej $f_{d}$, interpretowany jako sygnał o częstotliwości $f_{d}$ przesunięty w fazie o 180°.

Kwantyzacja jest procesem, w którym amplituda sygnału zostaje odwzorowana w skończony zbiór wartości (poziomów kwantyzacji). Różnicę sąsiednich wartości w tym zbiorze nazywamy progiem kwantyzacji. Jeśli jest on stały, mówimy wówczas o kwantyzacji równomiernej. Stosując b-bitową stałoprzecinkową reprezentację danych, liczba poziomów kwantyzacji wynosi zwykle $2^{b}$. Kwantyzacja może być rozumiana jako operacja obcinania, bądź zaokrąglania danych (rys. 3 i 4, odpowiednio).

* **Rysunek 3:** Kwantyzacja z obcięciem. Kolorem zielonym zaznaczono sygnał oryginalny, kolorem niebieskim wynik kwantyzacji.
* **Rysunek 4:** Kwantyzacja z zaokrąglaniem. Kolorem zielonym zaznaczono sygnał oryginalny, kolorem niebieskim wynik kwantyzacji.

W obu przypadkach jej efektem jest powstawanie błędu kwantyzacji, który może być interpretowany jako addytywny szum o mocy zależnej bezpośrednio od liczby bitów kwantyzera. Przykładowo, dla sygnału sinusoidalnego idealny przetwornik A/C o $b$ bitach charakteryzuje się maksymalnym wyjściowym stosunkiem sygnał szum danym jako:
$$SNR_{A/C}\approx6.02b+1.76dB$$
Przekształcając to wyrażenie otrzymujemy wzór na efektywną liczbę bitów (ENOB, ang. *Effective Number Of Bits*) rzeczywistego przetwornika:
$$ENOB=\frac{SNR-1.76}{6.02}$$

---

### Miary podobieństwa

Miary podobieństwa przydatne do obiektywnej oceny skutków próbkowania i kwantyzacji definiujemy jako:

* **Błąd średniokwadratowy (MSE, ang. Mean Squared Error)**
  $$MSE=\frac{1}{N}\sum_{i=0}^{N-1}[x(i)-\hat{x}(i)]^{2}$$
* **Stosunek sygnał szum (SNR, ang. Signal to Noise Ratio)**
  $$SNR_{dB}=10\log_{10}\left(\frac{\sum_{i=0}^{N-1}x^{2}(i)}{\sum_{i=0}^{N-1}[x(i)-\overline{x}(i)]^{2}}\right)$$
* **Szczytowy stosunek sygnał szum (PSNR, ang. Peak Signal to Noise Ratio)**
  $$PSNR_{dB}=10\log_{10}\left(\frac{\max_{i=0,...,N}x(i)}{MSE}\right)$$
* **Maksymalna różnica (MD, ang. Maximum Difference)**
  $$MD=\max_{i=0,1,...,N}|x(i)-\hat{x}(i)|$$

Zauważmy tu, że błąd średniokwadratowy MSE wyraża w istocie moc średnią sygnału różnicowego $n=x-\hat{x}$, rozumianego jako szum powstały w wyniku konwersji sygnału.