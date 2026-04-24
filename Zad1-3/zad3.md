**Cyfrowe przetwarzanie sygnałów**


**Zadanie 3**


**Splot, filtracja i korelacja sygnałów**


_**Operacja splotu**_

Splot dyskretny jest jedn˛a z najwa˙zniejszych operacji stosowanych podczas filtracji sygnałów dys
kretnych. Jest on operacj˛a przetwarzania dwóch sygnałów dyskretnych daj˛ac˛a w wyniku pojedyn
czy sygnał dyskretny. W ogólnym przypadku splot dwóch sygnałów dyskretnych h oraz x, ozna
czany dalej symbolem (h _∗_ x)(n) zdefiniowany jest nast˛epuj˛acym wzorem:



(h _∗_ x)(n) =



+ _∞_


h( _k_ )x( _n_   - _k_ ) _._ ( 1)

_k_ = _−∞_



W praktyce, w przypadku sygnałów dyskretnych o (niekoniecznie identycznych) sko´nczonych ilo
´sciach próbek rozmieszczonych równomiernie w dowolnych miejscach osi czasowej zakres zmien
no´sci indeksu próbek n jest równie˙z sko´nczony oraz dla ka˙zdego n zakresy sumowa´n zmieniaj˛a

si˛e odpowiednio zgodnie z poło˙zeniami na osi czasu i ilo´sciami próbek ka˙zdego z wej´sciowych sy
gnałów dyskretnych h oraz x. W praktyce filtracji sygnałów dyskretnych najcz˛e´sciej przyjmuje si˛e

konwencj˛e indeksacyjn˛a wg której obydwa sygnały wej´sciowe rozpoczynaj˛a si˛e na osi czasowej

dla próbki - indeksie zero i poza przedziałami próbkowania s˛a oczywi´scie sygnałami zerowymi.

Przykładowo, dla dwóch sygnałów dyskretnych, M - elementowego sygnału h oraz N - elemen
towego sygnału x rozpi˛etych na osi czasu pocz˛awszy od próbki - indeksie zero ich splot tworzy

pojedynczy dyskretny sygnał wyj´sciowy równie˙z rozpi˛ety na osi czasu pocz˛awszy od próbki 
indeksie zero, który mo˙zna przedstawi´c zale˙zno´sci˛a uproszczon˛a, wynikaj˛ac˛a bezpo´srednio ze

wzoru (1) w nast˛epuj˛acy sposób:



(h _∗_ x)(n) =



_M_ -1


h( _k_ )x( _n_   - _k_ ) _._ ( 2)

_k_ =0



Krótka refleksja nad postaci˛a wzoru (2) skłania do wniosku, ˙ze sygnał wyj´sciowy b˛edzie sygnałem

dyskretnym - długo´sci M + N _−_ 1 próbek rozpi˛etym na osi czasu pocz˛awszy od próbki wyj´scio
wej - indeksie zero. Obrazowo operacj˛e splotu opisan˛a wzorem (2) przedstawia rysunek 1. Ze

wzoru (2) oraz z rysunku 1 wynika, ˙ze poszczególne współrz˛edne splotu dyskretnego h _∗_ x tam

przedstawione b˛ed˛a miały nast˛epuj˛ace warto´sci:


(h _∗_ x)(0) =h(0) _·_ x(0)


(h _∗_ x)(1) =h(0) _·_ x(1) + h(1) _·_ x(0)


(h _∗_ x)(2) =h(0) _·_ x(2) + h(1) _·_ x(1) + h(2) _·_ x(0)


(h _∗_ x)(3) =h(1) _·_ x(2) + h(2) _·_ x(1) + h(3) _·_ x(0)


(h _∗_ x)(4) =h(2) _·_ x(2) + h(3) _·_ x(1)


(h _∗_ x)(5) =h(3) _·_ x(2)


1


Rysunek 1: Na rysunku przedstawiono pogl˛adowo operacj˛e splotu dla dwóch sygnałów: 4 - ele
mentowego h oraz 3 - elementowego x daj˛acych w wyniku 6 - elementowy sygnał h _∗_ x.


W ramach tej cz˛e´sci ´cwiczenia trzeciego nale˙zy zaimplementowa´c operacj˛e splotu dyskretnego

dla dowolnych dwóch sygnałów dyskretnych o arbitralnie podanych (mog˛acych si˛e ró˙zni´c mi˛edzy

sob˛a) ilo´sciach próbek z wykorzystaniem wzoru (2).


_**Filtracja sygnałów**_

Filtracja stanowi jedn˛a z podstawowych operacji cyfrowego przetwarzania sygnałów. W procesie

filtracji widmo sygnału podlega pewnej modyfikacji. Zmiana ta polega na odfiltrowaniu składowych

sygnału - cz˛estotliwo´sciach le˙z˛acych w przedziale zwanym pasmem zaporowym podczas, gdy

pozostała cz˛e´s´c widma, le˙z˛aca w tzw. pa´smie przepustowym, nie jest zmieniana lub podlega

niewielkiemu tłumieniu. Ze wzgl˛edu na umiejscowienie pasma przepustowego i zaporowego filtry

dzielimy na:


_◦_ **filtry** **dolnoprzepustowe**  - pasmo przepustowe obejmuje przedział cz˛estotliwo´sci od 0 do

fo, gdzie fo nazywamy cz˛estotliwo´sci˛a odci˛ecia filtru,


2


_◦_ **filtry górnoprzepustowe**  - pasmo przepustowe le˙zy z zakresie od fo do fp/2 (fp to cz˛estotliwo´s´c próbkowania sygnału),


_◦_ **filtry pasmowe**  - pasmo przepustowe znajduje si˛e w zakresie od fd do fg, przy czym fd, fg>0,
fd<fg oraz fd, fg<fp/2.


W ramach niniejszego ´cwiczenia laboratoryjnego do filtracji sygnałów cyfrowych wykorzystamy

filtry - sko´nczonej odpowiedzi impulsowej SOI (ang. FIR - _Finite_ _Impulse_ _Response_ ). Filtry te

posiadaj˛a dwie bardzo istotne zalety: łatwo´s´c implementacji (obliczenia prowadzone w oparciu 
równanie splotu (2) oraz łatwo´s´c projektowania postaci filtru.

Jak ju˙z wspomniano, w przypadku filtrów SOI proces filtracji sygnału jest realizowany w opar
ciu - równanie splotu. Oznacza to, i˙z ka˙zdorazowo dla obliczenia pojedynczej próbki sygnału

wyj´sciowego, tj. odfiltrowanego (y( _n_ )), wykorzystuje si˛e próbk˛e bie˙z˛ac˛a i pewn˛a liczb˛e _M_ prze
szłych próbek sygnału wej´sciowego (x( _n_ )). Kolejne warto´sci y( _n_ ) obliczane s˛a wówczas jako sumy

wa˙zone x( _n_ ) wzgl˛edem współczynników filtru h( _n_ ), tj.



y( _n_ )=



_M_ -1


h( _k_ )x( _n_   - _k_ ) _._ ( 3)

_k_ =0



Warto´s´c _M_ nazywamy rz˛edem filtru, natomiast zbiór współczynników h( _k_ ) filtru nazywamy od
powiedzi˛a impulsow ˛a ze wzgl˛edu na fakt, i˙z mo˙zna go łatwo uzyska´c poddaj˛ac filtracji sygnał

wej´sciowy x( _n_ ) w postaci impulsu Kroneckera. Nale˙zy jeszcze zwróci´c uwag˛e na to, ˙ze je´sli ci˛ag

próbek sygnału wej´sciowego stanie si˛e ci˛agiem warto´sci zerowych, to filtr SOI wygeneruje na

wyj´sciu zawsze sko´nczony ci˛ag warto´sci niezerowych. St˛ad wła´snie pochodzi nazwa filtrów SOI.

Posługuj˛ac si˛e znanym twierdzeniem o splocie w łatwy sposób mo˙zna wyja´sni´c istot˛e działania

filtru SOI. Widmo sygnału wyj´sciowego Y( _m_ ) b˛edzie wówczas iloczynem widma sygnału wej´scio
wego X( _m_ ) oraz widma H( _m_ ) odpowiedzi impulsowej, zwanego równie˙z transmitancj˛a filtru. Zatem

transmitancja filtru jest definiowana jako widmo Fouriera odpowiedzi impulsowej h( _n_ ). W oparciu

- wspomniane twierdzenie mo˙zna łatwo zaprojektowa´c posta´c odpowiedzi impulsowej filtru SOI.

W ramach ´cwiczenia do projektowania filtrów SOI wykorzystamy jedn˛a z najpopularniejszych

metod zwan˛a metod˛a okna. Jako pierwszy rozwa˙zymy przypadek filtrów dolnoprzepustowych. W

metodzie tej zakłada si˛e idealny filtr dolnoprzepustowy, tzn. taki, który w pa´smie przepustowym

nie zmienia widma sygnału wej´sciowego, tj. transmitancja filtru przyjmuje tutaj warto´sci 1, nato
miast w pa´smie zaporowym składowe cz˛estotliwo´sciowe s˛a całkowicie tłumione, tj. transmitancja

filtru przyjmuje warto´sci 0. Obliczaj˛ac odwrotne przekształcenie Fouriera dla tak zdefiniowanej

transmitancji otrzymujemy odpowied´z impulsow ˛a filtru postaci:



w pozostałych przypadkach _,_
_πn_



_2_ dla _n_ =0 _,_
_K_



h( _n_ )=















sin� 2 _πn_



_n_ 
_K_



gdzie _n_ _∈Z_, natomiast jako cz˛estotliwo´s´c odci˛ecia filtru przyjmuje si˛e fo=fp _/_ K. Oczywi´scie filtr


3


Rysunek 2: Na rysunku przedstawiono kolejno: odpowied´z impulsow ˛a filtru dolnoprzepustowego

dla _K_ =8 i _M_ =7 przy _N_ =256, moduł transmitancji filtru oraz moduł transmitancji wyra˙zony w skali

logarytmicznej


- takiej odpowiedzi impulsowej nie nadaje si˛e do realizacji praktycznej ze wzgl˛edu na niesko´nczo
n˛a liczb˛e współczynników h( _n_ ). W praktyce musimy przyj˛a´c ich sko´nczon˛a liczb˛e _M_, przy czym _M_

dobieramy stosunkowo niewielkie ze wzgl˛edu na zło˙zono´s´c obliczeniow ˛a rz˛edu _O_ ( _NM_ ). Załó˙zmy

dodatkowo _M_ nieparzyste. Zatem ci˛ag współczynników h( _n_ ) musi zosta´c zaw˛e˙zony poprzez od
powiednie obci˛ecie do długo´sci _M_ wzgl˛edem punktu _n_ =0. W najprostszym wydaniu współczynniki

h( _n_ ) dla _n_ powy˙zej ( _M_ -1)/2 i poni˙zej -( _M_ -1)/2 s˛a zerowane. Odpowiada to operacji wymno˙zenia

odpowiedzi impulsowej filtru przez tzw. funkcj˛a okna w( _n_ ), która w danym przypadku jest funkcj˛a

prostok˛atn˛a. Odpowiednikiem tej operacji w dziedzinie cz˛estotliwo´sci b˛edzie splot widma ideal
nego filtru dolnoprzepustowego z widmem funkcji okna, tutaj z funkcj˛a sinc, co w konsekwencji

sprowadza si˛e do zniekształcenia transmitancji tak zaprojektowanego filtru (patrz Rysunek 2 do

4). Poni˙zej prezentujemy wzór na odpowied´z impulsow ˛a filtru - liczbie M współczynników z od
powiednim przesuni˛eciem w celu uzyskania nieujemnych indeksów.



w pozostałych przypadkach _,_
_π_ ( _n_ -( _M_ -1)/2)



_2_ dla _n_ =( _M_ -1)/2 _,_
_K_



h( _n_ )=























( 4)



sin




2 _π_ ( _n_ -( _M_ -1)/2)

_K_



gdzie _n_ =0,1, ..., _M_ -1. Podczas analizy Rysunków 2 do 4 zauwa˙zymy nieliniowo´s´c w pa´smie prze
wodzenia, co jest wynikiem splotu funkcji prostok˛atnej z funkcj˛a sinc, a tak˙ze stosunkowo nie
wielkie wygaszenie pewnych składowych cz˛estotliwo´sciowych w pa´smie zaporowym. Polepsze

4


Rysunek 3: Na rysunku przedstawiono kolejno: odpowied´z impulsow ˛a filtru dolnoprzepustowego

dla _K_ =8 i _M_ =25 przy _N_ =256, moduł transmitancji filtru oraz moduł transmitancji wyra˙zony w skali

logarytmicznej


Rysunek 4: Na rysunku przedstawiono kolejno: odpowied´z impulsow ˛a filtru dolnoprzepustowego

dla _K_ =8 i _M_ =63 przy _N_ =256, moduł transmitancji filtru oraz moduł transmitancji wyra˙zony w skali

logarytmicznej


5


nie tych dwóch parametrów jest mo˙zliwe, je´sli podczas zaw˛e˙zania liczby elementów ci˛agu h( _n_ ),

współczynniki te zostan˛a wyodr˛ebnione przez inn˛a funkcj˛e okna, ni˙z funkcja prostok˛atna. Ponadto

mo˙zna zaobserwowa´c, i˙z wraz ze wzrostem liczby współczynników filtru jego transmitancja b˛edzie

coraz bli˙zsza transmitancji filtru idealnego.

Poni˙zej prezentujemy wybrane funkcje okien cz˛esto stosowane w praktyce cyfrowej filtracji

sygnałów (patrz Rysunek 5):


_◦_ _okno Hamminga_




         - 2 _πn_
w( _n_ )=0.53836-0.46164 _·_ cos
_M_




, ( 5)




_◦_ _okno Hanninga_


_◦_ _okno Blackmana_




      - 2 _πn_
w( _n_ )=0.5-0.5 _·_ cos
_M_




, ( 6)




      - 2 _πn_
w( _n_ )=0.42-0.5 _·_ cos
_M_




- - 4 _πn_
+0.08 _·_ cos
_M_




. ( 7)



Rysunek 5: Funkcje okien: okno Hanninga (linia ci˛agła), okno Hamminga (linia przerywana) i okno

Blackmana (linia wykropkowana)


Wpływ innych funkcji okien na widmo amplitudowe transmitancji filtru dolnoprzepustowego za
demonstrowano na Rysunku 6. Na podstawie analizy rysunku mo˙zna stwierdzi´c w sposób jed
noznaczny, i˙z pozostałe okna, tj. okno Hanninga, Hamminga i Blackmana w znacznym stopniu

redukuj˛a nieliniowo´s´c transmitancji w pa´smie przepustowym oraz istotnie polepszaj˛a tłumienie

składowych w pa´smie zaporowym w odniesieniu do okna prostok˛atnego. Jednak˙ze polepszenie

tych parametrów uzyskuje si˛e kosztem szerszego przedziału przej´sciowego, tzn. wolniejszego

przej´scia pomi˛edzy pasmem przepustowym i zaporowym.


6


Rysunek 6: Widma amplitudowe transmitancji filtru dolnoprzepustowego przy _M_ =25 i _N_ =256 uzy
skane dla ró˙znych okien: okno Hanninga (linia ci˛agła), okno Hamminga (linia przerywana) i okno

Blackmana (linia kropkowana)


Do tego momentu rozwa˙zali´smy przypadek filtru dolnoprzepustowego. Korzystaj˛ac ze zna
nego twierdzenia - modulacji mo˙zna w łatwy sposób przekształci´c odpowied´z impulsow ˛a filtru

dolnoprzepustowego do postaci b˛ed˛acej odpowiedzi˛a filtru:


_◦_ ´srodkowoprzepustowego: w tym celu nale˙zy wymno˙zy´c współczynniki h( _n_ ) przez sygnał si
nusoidalny o cz˛estotliwo´sci f=fp/4, tj. sygnał s( _n_ )=2sin( _πn_ /2). Wówczas fd=fp/4-fo oraz
fg=fp/4+fo,


_◦_ górnoprzepustowego: w tym celu nale˙zy wymno˙zy´c współczynniki h( _n_ ) przez sygnał sinusoidalny   - cz˛estotliwo´sci f=fp/2, tj. przez sygnał postaci s( _n_ ) = ( _−_ 1) _[n]_ . Wówczas fo=fp/2-fo,
gdzie fo to nowa warto´s´c cz˛estotliwo´sci odci˛ecia.


Na Rysunkach 7 i 8 pokazano przykłady odpowiedzi impulsowych i transmitancji filtrów: ´srodko
woprzepustowego i górnoprzepustowego.

Dotychczas nie rozwa˙zali´smy widma fazowego tak projektowanych filtrów. Nale˙zy zwróci´c uwa
g˛e na to, i˙z filtry te w pa´smie przewodzenia posiadaj˛a liniowe widma fazowe (patrz Rysunek 9), co

sprawia, ˙ze filtracja nie zmienia postaci sygnału. Taka zmiana mogłaby mie´c katastrofalne skutki

w przypadku sygnałów modulowanych amplitudowo.

Podsumowuj˛ac, proces projektowania filtru rozpoczynamy od obliczenia współczynników filtru

dolnoprzepustowego zgodnie ze wzorem (4), ustalaj˛ac wcze´sniej rz˛ad filtru i cz˛estotliwo´s´c odci˛e
cia. Je˙zeli chcemy zastosowa´c inne okno ni˙z okno prostok˛atne, to współczynniki filtru wymna˙za
my przez wybran˛a funkcj˛e okna (patrz wzory (5)-(7)). W celu uzyskania filtru - charakterystyce

´srodkowoprzepustowej lub górnoprzepustowej współczynniki filtru nale˙zy dodatkowo przemno˙zy´c


7


Rysunek 7: Odpowied´z impulsowa i transmitancja filtru ´srodkowoprzepustowego ( _M_ =63, _N_ =256,

okno prostok˛atne)


przez funkcj˛e s( _n_ )=2sin( _πn_ /2) lub s( _n_ ) = ( _−_ 1) _[n]_ . Operacj˛e filtracji sygnału realizujemy w oparciu o

równanie splotu (3).

W ramach tej cz˛e´sci ´cwiczenia trzeciego nale˙zy:


_◦_ zaimplementowa´c algorytm, który umo˙zliwi projektowanie filtrów dolnoprzepustowych  - za
danej liczbie współczynników i zadanej cz˛estotliwo´sci obci˛ecia z wykorzystaniem okna pro
stok˛atnego,


_◦_ w zale˙zno´sci od przydzielonego wariantu zadania zastosowa´c dodatkowo jedno z poni˙z
szych okien:


_•_ (O1) okno Hamminga,


_•_ (O2) okno Hanninga,


_•_ (O3) okno Blackmana,


_◦_ w zale˙zno´sci od przydzielonego wariantu zadania umo˙zliwi´c dodatkowo zaprojektowanie

filtru:


_•_ (F1) ´srodkowoprzepustowego,


_•_ (F2) górnoprzepustowego


z mo˙zliwo´sci˛a wyboru funkcji okna i parametrów filtru jak wy˙zej,


_◦_ zaimplementowa´c operacj˛e filtracji podstawiaj˛ac odpowied´z impulsow ˛a filtru do wzoru na

splot,


8


Rysunek 8: Odpowied´z impulsowa i transmitancja filtru górnoprzepustowego ( _M_ =63, _N_ =256, okno

prostok˛atne)


Rysunek 9: Widma fazowe dla filtrów dolno-, ´srodkowo- i górnoprzepustowego przy _M_ =63 i _N_ =256

(okno prostok˛atne)


_◦_ zademonstrowa´c efekt filtracji na arbitralnie wybranych sygnałach testowych.


9


_**Korelacja sygnałów dyskretnych**_

Analiza korelacyjna sygnałów dyskretnych stanowi bardzo wa˙zn˛a cz˛e´s´c praktyki przetwarzania

sygnałów. Zastosowanie znajduje wsz˛edzie tam gdzie zachodzi konieczno´s´c porównywania anali
zowanego sygnału z innym sygnałem, w szczególno´sci ze swoja własna, przesuni˛et˛a na osi czasu

kopi˛a. Podobnie jak operacja splotu korelacja wzajemna sygnałów dyskretnych jest operacj˛a prze
twarzania dwóch sygnałów dyskretnych daj˛ac˛a w wyniku pojedynczy sygnał dyskretny. W ogólnym

przypadku korelacja wzajemna dwóch sygnałów dyskretnych h oraz x, oznaczana dalej symbolem

R _hx_ zdefiniowana jest nast˛epuj˛acym wzorem:



R _hx_ =



+ _∞_


h( _k_ )x( _k_   - _n_ ) _._ ( 8)

_k_ = _−∞_



Tutaj równie˙z, tak jak w przypadku operacji splotu, dla sygnałów dyskretnych - (niekoniecznie

identycznych) sko´nczonych ilo´sciach próbek rozmieszczonych równomiernie w dowolnych miej
scach osi czasowej zakres zmienno´sci indeksu próbek n jest równie˙z sko´nczony oraz dla ka˙zdego

n zakresy sumowa´n zmieniaj˛a si˛e odpowiednio zgodnie z poło˙zeniami na osi czasu i ilo´sciami pró
bek ka˙zdego z wej´sciowych sygnałów dyskretnych h oraz x. Tutaj tak˙ze przyjmuje si˛e konwencj˛e

indeksacyjn˛a wg której obydwa sygnały wej´sciowe rozpoczynaj˛a si˛e na osi czasowej dla próbki o

indeksie zero i poza przedziałami próbkowania s˛a sygnałami zerowymi. Przykładowo, dla dwóch

sygnałów dyskretnych, M - elementowego sygnału h oraz N - elementowego sygnału x rozpi˛etych

na osi czasu pocz˛awszy od próbki - indeksie zero ich funkcja korelacji wzajemnej tworzy poje
dynczy dyskretny sygnał wyj´sciowy równie˙z rozpi˛ety na osi czasu pocz˛awszy od próbki o indeksie

-2, który mo˙zna przedstawi´c zale˙zno´sci˛a uproszczon˛a, wynikaj˛ac˛a bezpo´srednio ze wzoru (8) w

nast˛epuj˛acy sposób:



R _hx_ =



_M_ -1


h( _k_ )x( _n_   - _k_ ) _._ ( 9)

_k_ =0



Krótka refleksja nad postaci˛a wzoru (9) skłania do wniosku, ˙ze sygnał wyj´sciowy b˛edzie sygnałem

dyskretnym o długo´sci M + N _−_ 1 próbek rozpi˛etym na osi czasu pocz˛awszy od próbki wyj´sciowej o

indeksie -2. Obrazowo operacj˛e korelacji wzajemnej opisan˛a wzorem (9) przedstawia rysunek 10.

Ze wzoru (9) oraz z rysunku 10 wynika, ˙ze poszczególne współrz˛edne funkcji korelacji wzajemnej

R _hx_ tam przedstawione b˛ed˛a miały nast˛epuj˛ace warto´sci:


R _hx_ (-2) = h(0) _·_ x(2)


R _hx_ (-1) = h(0) _·_ x(1) + h(1) _·_ x(2)


R _hx_ (0) = h(0) _·_ x(0) + h(1) _·_ x(1) + h(2) _·_ x(2)


R _hx_ (1) = h(1) _·_ x(0) + h(2) _·_ x(1) + h(3) _·_ x(2)


R _hx_ (2) = h(2) _·_ x(0) + h(3) _·_ x(1)


R _hx_ (3) = h(3) _·_ x(0)


10


Rysunek 10: Na rysunku przedstawiono pogl˛adowo operacj˛e korelacji wzajemnej dla dwóch sy
gnałów: 4 - elementowego h oraz 3 - elementowego x daj˛acych w wyniku 6 - elementowy sygnał

R _hx_ .


W ramach tej cz˛e´sci ´cwiczenia trzeciego nale˙zy zaimplementowa´c operacj˛e korelacji wzajemnej

dla dowolnych dwóch sygnałów dyskretnych o arbitralnie podanych (mog˛acych si˛e ró˙zni´c mi˛edzy

sob˛a) ilo´sciach próbek. Oczywi´scie w przypadku implementacji ´cwiczenia nale˙zy przeindekso
wa´c elementy wektora wyj´sciowego R _hx_, tak aby kolejne jego próbki wyj´sciowe znajdowały si˛e w
elementach odpowiedniej tablicy wyj´sciowej - indeksach rozpoczynaj˛aych si˛e od zera. Ponadto

implementacja powinna zawiera´c dwa obligatoryjne, nast˛epuj˛ace warianty:


_◦_ **implementacj˛e bezpo´sredni˛a**  - to znaczy algorytm wykonuj˛acy operacj˛e korelacji wzajem
nej dwóch dowolnych sygnałów dyskretnych bezpo´srednio w oparciu    - wzór (9) (i rysunek

pomocniczy 10).


_◦_ **implementacj˛e z u˙zyciem splotu**  - to znaczy algorytm wykonuj˛acy operacj˛e korelacji wza
jemnej dwóch dowolnych sygnałów dyskretnych w oparciu o wzór (2) (i rysunek pomocniczy

1) z u˙zyciem zaimplementowanej w pierwszej cz˛e´sci ´cwiczenia operacji splotu dyskretnego.


11


_**Zastosowania analizy korelacyjnej - pomiar odległo´sci**_

Jednym z przykładów zastosowa´n, w których wykorzystuje si˛e rezultaty porównywania sygna
łów przesuni˛etych w czasie jest pomiar odległo´sci od celu za pomoc˛a radaru np. impulsowego.

Radar wysyła sygnał sonduj˛acy, który w jednym z mo˙zliwych przypadków mo˙ze stanowi´c (od
powiednio zmodulowany) sygnał okresowy. Sygnał po odbiciu si˛e od celu powraca do anteny

nadawczo-odbiorczej z pewnym opó´znieniem (pomijamy tu fakt potencjalnego zniekształcenia sy
gnału powracaj˛acego). Pomiar odległo´sci jest dokonywany na podstawie pomiaru tego opó´znienia

za pomoc˛a analizy korelacyjnej sygnału wysłanego i zwrotnego. Je´sli tylko cz˛estotliwo´s´c próbko
wania - identyczna dla obydwu sygnałów - jest dostatecznie du˙za, mo˙zna w okre´slonych odst˛e
pach czasu dokonywa´c analizy korelacyjnej spróbkowanej i zbuforowanej (przy u˙zyciu tej samej

ilo´sci próbek dyskretnych) pary sygnałów sonduj˛acego i zwrotnego poprzez obliczenie korelacji

wzajemnej wybranej pary odpowiadaj˛acych sobie sygnałów, aby uaktualni´c odczyt odległo´sci od

zadanego celu. Poniewa˙z korelacja jest najwi˛eksza gdy nało˙zone na siebie sygnały pokrywaj˛a

si˛e wzajemnie w najwi˛ekszym stopniu, a wzór (9) dokonuje wła´snie takiego nało˙zenia obydwu

sygnałów dla ka˙zdego odst˛epu czasowego próbkowania, przesuwaj˛ac odpowiednio sygnały son
duj˛acy i zwrotny wzgl˛edem siebie i obliczaj˛ac pojedyncz˛a warto´s´c korelacji dla ka˙zdego z takich

odst˛epów, to mo˙zna odnale´z´c maksimum funkcji korelacji (na prawo od ´srodkowego argumentu

funkcji korelacji wzajemnej) i na podstawie znajomo´sci cz˛estotliwo´sci (a zatem i okresu) próbko
wania funkcji korelacji (której próbki wyj´sciowe reprezentuj˛a t˛e sam˛a cz˛estotliwo´s´c próbkowania,

co sygnały sonduj˛acy i zwrotny) okre´sli´c opó´znienie czasowe z jakim sygnał zwrotny powraca do

anteny odbiorczej. Sytuacj˛e tak˛a obrazuje poni˙zszy rysunek:


Rysunek 11: Zasada działania korelacyjnego czujnika odległo´sci.


12


Wykorzystuj˛ac znany wzór fizyczny S = V _·_ t i znaj˛ac cz˛estotliwo´s´c (a co za tym idzie i okres ∆t)

próbkowania mo˙zna ju˙z w prosty sposób na podstawie wspomnianej wcze´sniej odległo´sci mak
simum funkcji korelacji wzajemnej okre´sli´c czas w jakim sygnał powraca do anteny, a co za tym

idzie równie˙z i (dwukrotn˛a) drog˛e S jak˛a pokonał od anteny do obiektu i z powrotem (przy dodat
kowym zało˙zeniu, ˙ze pr˛edko´s´c V jest pr˛edko´sci˛a ´swiatła, gdy˙z mamy do czynienia z sygnałem

radarowym). Znaj˛ac t˛e drog˛e i dziel˛ac j˛a przez dwa uzyskujemy chwilow ˛a odległo´s´c pomi˛edzy

czujnikiem a rozwa˙zanym obiektem.


Podsumowuj˛ac, aby wyznaczy´c szukan˛a odległo´s´c, odopwiedni czujnik musi wykona´c nast˛epuj˛a
ce operacje:


_◦_ **Krok 1**  - Wygenerowa´c i wysła´c anten˛a nadawczo - odbiorcz˛a okresowy, ci˛agły sygnał son
duj˛acy    - odpowiednim okresie (w opisie pomijamy konieczno´s´c modulacji tego sygnału)

oczekuj˛ac odbicia sygnału od najbli˙zszego obiektu.


_◦_ **Krok 2**  - nieprzerwanie próbkowa´c z odpowiednio du˙z˛a cz˛estotliwo´sci˛a i buforowa´c obydwa

sygnały do postaci dyskretnej (najpro´sciej aby obydwa bufory zawierały t˛e sam˛a liczb˛e pró
bek)


_◦_ **Krok** **3**  - co pewien okres, zale˙zny od wymaga´n konstrukcyjnych czujnika, dokona´c analizy

korelacyjnej obydwu zbuforowanych w ten sposób sygnałów dyskretnych, aby uaktualni´c

odległo´s´c od zadanego obiektu


_◦_ **Krok** **4**  - podczas takiej analizy wyznaczy´c dyskretn˛a funkcj˛e korelacji wzajemnej spróbko
wanych sygnałów dysktretnych R _yx_ według wzoru (9) i przejrze´c praw ˛a połow˛e wykresu tej

funkcji w poszukiwaniu próbki maksymalnej


_◦_ **Krok** **5**  - po znalezienu próbki maksymalnej, korzystaj˛ac z faktu znanej warto´sci okresu

próbkownia ∆t sygnałów sonduj˛acego i zwrotnego, a co za tym idzie równie˙z znanemu

i identycznemu co do warto´sci (te˙z ∆t) odst˛epu mi˛edzy dyskretnymi próbkami funkcji ko
relacji wzajemnej, okre´sli´c czas t odpowiadaj˛acy odległo´sci próbki maksymalnej od próbki

´srodkowej w buforze dyskretnej funkcji korelacji wzajemnej


_◦_ **Krok** **6**  - na podstawie znanego czasu t opó´znienia okre´sli´c ze wzoru S = V _·_ t (gdzie V = c

jest pr˛edko´sci˛a ´swiatła) drog˛e jak˛a pokonał sygnał od radaru do obiektu i z powrotem


_◦_ **Krok** **7**  - podzieli´c t˛e drog˛e przez 2 otrzymuj˛ac chwilow ˛a odległo´s´c d czujnika od monitoro
wanego obiektu.


Celem tej cz˛e´sci ´cwiczenia jest symulacja działania korelacyjnego czujnika odległo´sci. Nale˙zy

napisa´c program, który b˛edzie symulował taki czujnik i dokonywał porównania rzeczywistej chwi
lowej odległo´sci od ´sledzonego obiektu z pomiarem raportowanym przez symulowany czujnik.

W parametrach programu nale˙zy uwzgl˛edni´c mo˙zliwo´s´c regulacji takich warto´sci jak - od strony

´sledzonego obiektu i (abstrakcyjnego) o´srodka rozchodzenia si˛e sygnału:


13


_•_ podstawow ˛a, dostatecznie mał˛a jednostk˛e czasow ˛a symulatora


_•_ rzeczywist˛a pr˛edko´s´c ´sledzonego obiektu (mo˙ze by´c stała)


_•_ pr˛edko´s´c rozchodzenia si˛e sygnału w abstrakcyjnym o´srodku (dla uogólnionego, abstrak
cyjnego o´srodka nie musi by´c to pr˛edko´s´c swiatła   - unikamy w ten sposób operacji na b.

du˙zych/ b. małych liczbach),


za´s os strony czujnika nale˙zy uwzgl˛edni´c mo˙zliwo´s´c regulacji nast˛epuj˛acych parametrów:


_•_ okres ci˛agłego sygnału sonduj˛acego  - sygnał sonduj˛acy powinien by´c ci˛agły i okresowy

z mo˙zliwo´sci˛a regulowania okresu, a tak˙ze powinien by´c skonstruowany z kilku (najmniej

dwóch) podstawowych, ci˛agłych sygnałów okresowych (patrz instrukcja do ´cwiczenia nr. 1)


_•_ cz˛estotliwo´s´c próbkowania sygnałów sonduj˛acego i zwrotnego


_•_ długo´sci (identyczne) buforów dyskretnych sygnałów sonduj˛acego i zwrotnego


_•_ okres raportowania przez symulowany czujnik przybli˙zonej, chwilowej warto´sci odległo´sci

´sledzonego obiektu


Nale˙zy przeprowadzi´c eksperymenty z tak symulowanym czujnikiem dla róznych warto´sci pa
rametrów podanych wy˙zej i w sprawozdaniu umie´sci´c najciekawsze spostrze˙zenia i obserwacje

dokonane na podstawie przeprowadzonych ekspoerymentów. Ciekawa, cho´c oczywi´scie nie obo
wi˛azkowa, byłaby tak˙ze graficzna prezentacja działania czujnika, np. w formie wykresów, takich

jak te przedstawione na rysunku 11.


14


