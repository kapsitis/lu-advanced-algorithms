2. Bezzudumu saspiešana: Aritmētiskais kods
============================================

Hafmana kodi ir optimāli gadījumā, ja katru ziņojumu jākodē ar 
vienu un to pašu bitu virknīti un neviena kodējumu virknīte nav 
citas virknītes prefikss. Vidējais bitu skaits uz ziņojumu, ko izmanto Hafmana 
kodējums (tāpat kā citi optimāli kodējumi) nepārsniedz 
:math:`H(S)+1`. 

Dažos gadījumos tas ir neefektīvi: Ja ir ziņojumu kopa :math:`S=\{ \mathtt{0}, \mathtt{1} \}` 
ar varbūtībām attiecīgi :math:`1023/1024` un :math:`1/1024`, tad Hafmana kods 
joprojām tērētu vienu bitu katram ziņojumam kaut arī entropija ir 

.. code-block:: python

  >>> import math
  >>> pp = [1023/1024, 1/1024]
  >>> H = sum([-p*math.log2(p) for p in pp])
  >>> H
  0.011173818721219527

Lai iekodētu 1000 šādi sadalītus ziņojumus, vajadzīgi vidēji :math:`11.17` biti, 
nevis :math:`1000` biti. 

Ir divas populāras pieejas, kas šo atrisina:

* `Aritmētiskie kodi <https://web.mat.upc.edu/sebastia.xambo/CDI15/CDI15-04-ArithmeticCoding.pdf>`_
* `Asimetriskas skaitīšanas sistēmas <https://en.wikipedia.org/wiki/Asymmetric_numeral_systems>`_ - 
  kopš publicēšanas 2014.gadā izmantots Zstandard (``Zstd`` implementācija) 

.. code-block:: bash

  sudo apt-get install zstd
  # brew install zstd    ## (Mac OS X users)
  echo "A quick brown fox jumped over a lazy dog" > input.txt
  zstd input.txt -o output.zst
  zstd -d output.zst -o input2.txt
  diff input.txt input2.txt

**Aritmētiskie kodi**
  Ir labāki adaptīviem varbūtiskiem modeļiem, kur ziņojumu varbūtības var 
  mainīties atkarībā no līdz šim saņemtās ievades. Aritmētiskās darbības 
  sākotnējā algoritmā ir paredzēts veikt ar reāliem skaitļiem; tāpēc šī 
  algoritma (veselās aritmētikas) implementācija nav ļoti vienkārša. Tas arī 
  var zaudēt ātrdarbību, jo regulāri nodarbojas ar reizināšanu un dalīšanu. 

**Asimetriskās skaitīšanas sistēmas:** 
  Parasti nav adaptīvas (visas varbūtības ir izrēķināmas jau iepriekš). 
  Saspiešana un atspiešana ir ļoti ātra, maksimāli izmanto bitu operācijas.



Aritmētiskās saspiešanas pamatideja
----------------------------------------


Piemērs: Metamais kauliņš
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. figure:: figs/dice-rolling-example.png
   :width: 3in

   Metamā kauliņa piemērs. 

Alise grib nosūtīt Bobam :math:`1000` (godīga) metamā kauliņa rezultātus.
Prefiksu kodējumam reizēm vajag :math:`2`, reizēm :math:`3` bitus.
Piemēram, var izmantot šādu kodējumu: 

.. math:: 

  C = \{ (1,\texttt{00}), (2,\texttt{010}), (3,\texttt{011}), 
  (4,\texttt{100}), (5,\texttt{101}), (6,\texttt{11}) \}.

.. math:: 

  \ell_a(C) = \frac{2 + 3 + 3 + 3 + 3 + 2}{6} = 2.666\ldots


.. note::
  Lai nosūtītu :math:`1000` metamā kauliņa rezultātus ar Hafmana kodu, 
  Alise izlietos vidēji :math:`2666.67` bitus. 
  Nedaudz mazāk, ja starp rezultātiem ir vairāk "1" un "6", bet 
  nedaudz vairāk, ja vairāk nekā vidēji tiek uzmesti "2", "3", "4", "5". 



**Cerība uz samazinājumu no 2667 uz 2585**

Entropija (vidējais informācijas saturs) vienā kauliņa metienā ir ap 
:math:`\log_2 6 \approx 2.585`.

.. math::

    H = \sum\limits_{s \in S} p(s) \cdot \left( - \log_2 p(s) \right) = 
    6 \cdot \left( \frac{1}{6} \cdot \left( - \log_2\,\frac{1}{6} \right) \right) \approx 2.584963.

Prefiksu kodi to nevar atrisināt, jo katram ziņojumam sūta divus vai trīs bitus
(nevar sūtīt daļveida bitus). 
Aritmētiskais kods rīkojas citādi: Katram metamā kauliņa rezultātam 
var izveidot sešas reizes īsāku intervālu (kā aprakstīts aritmētiskajā kodējumā). 
Un tikai pašās beigās iekodē iegūto ļoti īso intervālu ar bitu virknīti. 
  

Piemērs: Angļu burtu biežumi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: figs/english-letter-frequencies.png
   :width: 8in

Dabīgo valodu burtu sadalījums parasti nav labākais piemērs, jo tie mēdz parādīties
prognozējamās virknītēs, atsevišķa simbolu kodēšana (gan ar Hafmana, gan aritmētisko kodējumu)
parasti ir neoptimāla.
`Burtu biežumi <http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html>`



**Aritmētiskā saspiešana**

**Kāpēc lietot aritmētisko kodēšanu?**
  Ja ziņojumu telpā ir jocīgas varbūtības, tad Hafmana kodi (kas dala
  kodu telpas "nekustamo īpašumu" gabalos pa :math:`1/2`, :math:`1/4` utt.)
  iznieko daudz vietas un neizmanto to, ka dažu ziņojumu informācijas saturs 
  ir daudz mazāks par :math:`1`. 

**Kā nosūtīt ziņojumu, kura informācijas saturs ir nepilns bits?**
  Piemēram, ziņojumam ar varbūtību :math:`1023/1024` informācijas saturs 
  ir :math:`\log_2 (1023/1024) \approx 0.0014`. 
  Griežam kodu telpu cita veida gabalos,
  un bitos iekodējam tikai pašās beigās.



Aritmētiskās saspiešanas algoritms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ievade:** Dots ziņojumu alfabēts un tā varbūtību sadalījums. Dota arī ziņojumu virkne šajā alfabētā.   
**Izvade:** Intervāls :math:`I \subseteq [0;1]` (pietiek nosūtīt skaitli no šī 
intervāla). 

* Ir :math:`m` ziņojumi :math:`\{ 1,\ldots,m \}`. To varbūtības
  ir :math:`\{p(1),\ldots , p(m)\}`, kuru summa ir :math:`1`. 
* Definējam *kumulatīvās varbūtības*: 

  .. math::
      f(j) = \sum\limits_{i=1}^{j-1} p(i),\;\;j=1,\ldots,m.


**Intervālu konstruēšana**

Dota ziņojumu virkne :math:`x_1,x_2,\ldots,x_k \in \{ 1,\ldots,m \}`.  
Veidojam intervālu virkni, kur katram intervālam zināms kreisais galapunkts :math:`\ell_i`
un garums :math:`s_i`.  

.. math::
    [0;1] \supset [l_1;l_1+s_1) \supset [l_2;l_2+s_2) \supset \ldots \supset [l_k; l_k+s_k).

1.intervāls: :math:`[l_1;l_1 + s_1) = \left[ f(x_1);p(x_1) \right)`.  
Intervāliem :math:`2,\ldots,k` apzīmējam:

.. math::
    \left\{
    \begin{array}{l}
    l_i = l_{i-1} + f(x_i) \cdot s_{i-1}\\
    s_i = s_{i-1} \cdot p(x_i)
    \end{array} \right.


**Piemērs**

  .. figure:: figs/arithmetic-babc.png
     :width: 4in

     Intervālu virkne.

  * Alfabētā ir 3 burti *a,b,c*. Varbūtības ir attiecīgi 0.2, 0.5, 0.3
    (entropija viena burta nosūtīšanai būs 1.485475)
  * Piemērā parādīts, ka *`babc`* atbilst intervāls [.255, .27).
  * Galīga bināra daļa šajā intervālā: 
    `.0100001` jeb [33/128,34/128) \subseteq [.255, .27).
  * 4 ziņojumu virknītes nosūtīšanai iztērējām 7 bitus
    (vidēji 1.75 biti uz vienu ziņojumu).

**Jautājums:** Vai robežā nosūtīto bitu daudzums pret ziņojuma garumu tieksies uz 
entropiju 1.485475. Kāpēc?


**Intervālu nosūtīšana**

  * Ja dots intervāls ar garumu :math:`s`, tad tā iekšienē 
    var atrast skaitli, kura binārajā pierakstā ir 
    ne vairāk kā :math:`-\left\lceil \log_2 s \right\rceil` biti.
  * Gribam sūtīt tikai vienu skaitli. Lai saprastu, cik garš ir 
    tā intervāls, interpretējam, teiksim :math:`0.010` nevis vienkārši 
    kā :math:`1/4`, bet kā intervālu :math:`[1/4, 3/8)`. 
  * Nepazaudējot vairāk kā 1-2 bitus, varam izveidot šādu 
    intervālu :math:`[k/2^n,(k+1)/2^n)`, kurš atradīsies stingri iekšpusē 
    tam :math:`I`, ko dod aritmētiskais kods.


**Aritmētiskā koda īpatnības**

  * Aritmētiskā koda algoritmus jābūvē vai nu relatīvi nelielām ziņojumu 
    kopām (kur mums pietiek ar floating aritmētiku), vai arī
    jāizveido tuvinājums, kur reālos skaitļus tuvina ar veseliem skaitļiem. 

Sk arī 21.lpp. no teksta
`G.Blelloch. Introduction to Data Compression <https://www.cs.cmu.edu/~guyb/realworld/compression.pdf>`_ 
- ar veseliem skaitļiem tuvināts aritmētiskās kodēšanas algoritms.



**Iekodēšanas piemērs**

Sūtām stringu :math:`\textcolor{blue}{\mathtt{GACGU\$}}`, kur simboli 
:math:`\textcolor{blue}{\mathtt{A}}`, :math:`\textcolor{blue}{\mathtt{C}}`, 
:math:`\textcolor{blue}{\mathtt{G}}`, :math:`\textcolor{blue}{\mathtt{U}}` 
ir RNS-virknes nukleobāzes, 
bet :math:`\textcolor{blue}{\mathtt{\$}}` apzīmē stringa beigas.  Simbolu apriorās varbūtības ir šādas:



.. figure:: figs/arithmetic-coding.png
   :width: 6in


===================  ===================  ===================  ===================  ===================
:math:`\mathtt{A}`   :math:`\mathtt{C}`   :math:`\mathtt{G}`   :math:`\mathtt{U}`   :math:`\mathtt{\$}`
===================  ===================  ===================  ===================  ===================
30%                  10%                  30%                  20%                  10%
===================  ===================  ===================  ===================  ===================

**Intervālu aprēķini**

  * :math:`S_0 = [0.000000; 1.000000]` atbilst :math:`\textcolor{blue}{\mathtt{""}}` (tukšais strings),
  * :math:`S_1 = [0.400000; 0.700000]` atbilst :math:`\textcolor{blue}{\mathtt{G}}`,
  * :math:`S_2 = [0.400000; 0.490000]` atbilst :math:`\textcolor{blue}{\mathtt{GA}}`,
  * :math:`S_3 = [0.427000; 0.436000]` atbilst :math:`\textcolor{blue}{\mathtt{GAC}}`,
  * :math:`S_4 = [0.430600; 0.433300]` atbilst :math:`\textcolor{blue}{\mathtt{GACG}}`,
  * :math:`S_5 = [0.432490; 0.433030]` atbilst :math:`\textcolor{blue}{\mathtt{GACGU}}`,
  * :math:`S_6 = [0.432976; 0.433030]` atbilst :math:`\textcolor{blue}{\mathtt{GACGU\$}}`.

Bināri pierakstītais skaitlis 

.. math::
    \beta = 0.011011101101100_2 \approx 0.4329834_{10}

pieder intervālam :math:`S_6 = [0.432976; 0.433030]`. 

Kāpēc :math:`\beta` binārais pieraksts beidzas ar divām nullēm?  
Tieši 15 cipari aiz komata un :math:`\left[\beta;\,\beta + \frac{1}{2^{15}}\right] \subseteq S_6`. 

.. note::
  Katrai galīgai binārai daļai atbilst :math:`[0;1]` apakšintervāls.



Aritmētiskais kods veselos skaitļos
---------------------------------------

Reālo skaitļu aritmētika, darbojoties ar 4 baitu vai 8 baitu 
peldošā punkta skaitļiem var saskarties ar reģistra pārpildīšanos 
(*overflow* vai *underflow*) -- vienā skaitlī var iekodēt tikai nedaudz informācijas.
Ir arī noapaļošanas kļūdas; ir kaut kā jānodrošina, lai iekodējot un atkodējot 
noapaļošanas kļūdas vienmēr notiktu vienādi. 
  
Parastais risinājums ir pāriet uz veselo skaitļu aritmētiku
un noapaļot varbūtības līdz skaitļiem formā :math:`i/2^k`. 

Definējam, cik reižu parādās katrs ziņojums (aptuveni proporcionāli varbūtībām)
un arī kumulatīvās summas: 

.. math:: 

  c(1), c(2), \ldots, c(m)

.. math:: 

  f(i) = c(1) + \ldots + c(i-1),\;\; \mbox{katram $i \in [1;m]$}

Visu skaitu summa :math:`T = c(1) + \ldots + c(m)`. 


| :math:`\text{\sc IntArithmeticCode}(\text{file}, k, n)`
| 1. :math:`R = 2^k`
| 2. :math:`l = 0`
| 3. :math:`u = R - 1`
| 4. :math:`m = 0`
| 5. **for** :math:`i = 1` **to** :math:`n`:
| 6. :math:`\quad` :math:`s = u - l + 1`
| 7. :math:`\quad` :math:`u = l + \left\lfloor \left(s \cdot f_i(v_i + 1) \right)/T \right\rfloor - 1`
| 8. :math:`\quad` :math:`l = l + \left\lfloor \left(s \cdot f_i(v_i) \right)/T \right\rfloor`
| 9. :math:`\quad` **while** :math:`\text{\sc True}`:
| 10. :math:`\quad\quad` **if** :math:`(l \geq \frac{R}{2})` :math:`\quad` *// intervāls augšējā pusē*
| 11. :math:`\quad\quad\quad` :math:`\text{\sc WriteBit}(1)`
| 12. :math:`\quad\quad\quad` :math:`u = 2u - R + 1 \;\;\; l = 2l - R`
| 13. :math:`\quad\quad\quad` **for** :math:`j = 1` **to** :math:`m`: :math:`\text{\sc WriteBit}(0)`
| 14. :math:`\quad\quad\quad` :math:`m = 0`
| 15. :math:`\quad\quad` **else if** :math:`(u < \frac{R}{2})` :math:`\quad` *// intervāls apakšējā pusē*
| 16. :math:`\quad\quad\quad` :math:`\text{\sc WriteBit}(0)`
| 17. :math:`\quad\quad\quad` :math:`u = 2u + 1 \;\;\; l = 2l`
| 18. :math:`\quad\quad\quad` **for** :math:`j = 1` **to** :math:`m`: :math:`\text{\sc WriteBit}(1)`
| 19. :math:`\quad\quad\quad` :math:`m = 0`
| 20. :math:`\quad\quad` **else if** :math:`(l \geq \frac{R}{4} \;\;\text{and}\;\; u < \frac{3R}{4})` :math:`\;\;\;\;\;` *// intervāls pa vidu*
| 21. :math:`\quad\quad\quad` :math:`u = 2u - \frac{R}{2} + 1 \;\;\; l = 2l - \frac{R}{2}`
| 22. :math:`\quad\quad\quad` :math:`m = m + 1`
| 23. :math:`\quad\quad` **else** **continue** 
| 24. :math:`\quad` **end while**
| 25. **end for**
| 26. **if** :math:`(l \geq \frac{R}{4})` :math:`\quad`  *// izvada pēdējos bitus*
| 27. :math:`\quad` :math:`\text{\sc WriteBit}(1)`
| 28. :math:`\quad` **for** :math:`j = 1` **to** :math:`m`: :math:`\text{\sc WriteBit}(0)`
| 29. :math:`\quad` :math:`\text{\sc WriteBit}(0)`
| 30. **else**
| 31. :math:`\quad` :math:`\text{\sc WriteBit(0)}`
| 32. :math:`\quad` **for** :math:`j = 1` **to** :math:`m`: :math:`\text{\sc WriteBit}(1)`
| 33. :math:`\quad` :math:`\text{\sc WriteBit}(1)`


Atspiešanas algoritms
~~~~~~~~~~~~~~~~~~~~~~~



| :math:`\text{\sc IntArithmeticDecode}(\text{file}, k, n)`
| 1. :math:`R = 2^k`
| 2. :math:`l = 0 \quad \text{// sequence interval}`
| 3. :math:`u = R - 1 \quad \text{// sequence interval}`
| 4. :math:`l_b = 0 \quad \text{// code interval}`
| 5. :math:`u_b = R - 1 \quad \text{// code interval}`
| 6. :math:`j = 1 \quad \text{// message number}`
| 7. **while** :math:`j \leq n` **do**:
| 8. :math:`\quad s = u - l + 1`
| 9. :math:`\quad i = 0`
| 10. :math:`\quad \text{do} \quad \text{// find if the code interval is within one of the message intervals}`
| 11. :math:`\quad \quad i = i + 1`
| 12. :math:`\quad \quad u' = l + \left\lfloor \left( s \cdot f_j(i + 1) \right) / T_j \right\rfloor - 1`
| 13. :math:`\quad \quad l' = l + \left\lfloor \left( s \cdot f_j(i) \right) / T_j \right\rfloor`
| 14. :math:`\quad \text{while} \ i \leq m_j \ \text{and not} \left( (l_b \geq l') \ \text{and} \ (u_b \leq u') \right):`
| 15. :math:`\quad \quad i = i + 1`
| 16. :math:`\quad \text{if} \ i \gt m_j\ \text{then}\ \quad \text{// halve the size of the code interval by reading a bit}`
| 17. :math:`\quad \quad b = \text{\sc ReadBit}(\text{file})`
| 18. :math:`\quad \quad s_b = u_b - l_b + 1`
| 19. :math:`\quad \quad l_b = l_b + b \frac{s_b}{2}`
| 20. :math:`\quad \quad u_b = l_b + s_b / 2 - 1`
| 21. :math:`\quad \text{else}:`
| 22. :math:`\quad \quad \text{\sc Output}(i) \quad \text{// output the message in which the code interval fits}`
| 23. :math:`\quad \quad u = u' \ \quad l = l' \quad \text{// adjust the sequence interval}`
| 24. :math:`\quad \quad j = j + 1`
| 25. :math:`\quad \text{while true}:`
| 26. :math:`\quad \quad \text{if} \ (l \geq \frac{R}{2}): \quad \text{// sequence interval in top half}`
| 27. :math:`\quad \quad \quad u = 2u - R + 1 \quad l = 2l - R`
| 28. :math:`\quad \quad \quad u_b = 2u_b - R + 1 \ \quad l_b = 2l_b - R`
| 29. :math:`\quad \quad \text{else if} \ (u < \frac{R}{2}): \quad \text{// sequence interval in bottom half}`
| 30. :math:`\quad \quad \quad u = 2u + 1 \quad l = 2l`
| 31. :math:`\quad \quad \quad u_b = 2u_b + 1 \quad l_b = 2l_b`
| 32. :math:`\quad \quad \text{else if} \ (l \geq \frac{R}{4} \ \text{and} \ u < \frac{3R}{4}): \quad \text{// sequence interval in middle half}`
| 33. :math:`\quad \quad \quad u = 2u - R / 2 + 1 \quad l = 2l - R / 2`
| 34. :math:`\quad \quad \quad u_b = 2u_b - R / 2 + 1 \quad l_b = 2l_b - R / 2`
| 35. :math:`\quad \quad \text{else continue} \quad \text{// exit inner while loop}`
| 36. :math:`\quad \text{end if}`
| 37. :math:`\text{end while}`



Beigu marķieris
~~~~~~~~~~~~~~~~~~~

Aritmētiskā koda atspiešana veic pārveidojumus ar nosūtīto skaitli jeb intervālu un 
atkodē arvien jaunus ziņojumus. 
Var noteikt brīdi, kad atspiežamais intervāls jau izgājis ārpus :math:`[0;1]` un 
tad atspiešana ir jābeidz. 

Ir cits populārs risinājums: ``PSEUDO_EOF`` - kods var beigties baita vidū. 
Parasti pievieno īpašu simbolu (teksta beigu marķieri), 
lai saprastu, kad atkodēšana jāpārtrauc. 

Beigu marķieris nodrošina arī to, ka viena saspiesta ziņojumu virkne 
nevar būt citas ziņojumu virknes prefikss (jo beigu marķieris nedrīst atrasties kodējuma vidū). 
Sk. arī detalizētu `Hafmana aprakstu <https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1172/assn/huffman.html>`_, 
kurā aprakstīta līdzīga problēma.








Citi entropijas kodi 
-----------------------

**Nosacītās varbūtības modelis**

Aritmētisko kodu var uzlabot, ja ņem vērā simbolu parādīšanās
varbūtību atkarību no konteksta (1.kārtas modelis - tikai viens iepriekšējais
simbols). Tad nākamo intervālu dala gabalos atkarībā 
no iepriekšējā simbola.

.. figure:: figs/conditional-probability-model.png
   :width: 7in 

   Nosacītās varbūtības modelis.



.. note::
  `Bildes par aritmētisko kodēšanu 
  <http://www.ws.binghamton.edu/fowler/fowler%20personal%20page/EE523_files/Ch_04%20Arithmetic%20Coding%20(PPT).pdf>`_



**Asimetriskās skaitīšanas sistēmas**

*Asymmetric numeral systems (ASN)* -- Jaroslaw Duda (2014) pētījumi.
Kalpo līdzīgam mērķim kā aritmētiskie kodi (saspiež ievades datu plūsmu līdz 
entropijas noteiktajai robežai). Ar ko atšķiras no aritmētiskajiem kodiem:
Lietojumi dažos jaunos standartos. 

1. Facebook Zstandard.
2. Apple LZFSE.
3. Google Draco 3D compressor.

Jaunie algoritmi var labāk saspiest vai pārraidīt vairāk datu pa to pašu sakaru kanālu; 
tiem reizēm vajadzīgas lielākas skaitļošanas jaudas (vai tie labākai efektivitātei 
jāprogrammē paralēli), tāpēc tos visas platformas neatbalsta. 

Būtiski, uz kādas ierīces un kādā situācijā notiek saspiešana/atspiešana. 
(Kešošana, retāka un mazāka tīkla izmantošana. CPU var izmantot drošāk.)


**Entropijas kodēšana kā paralēli algoritmi?**

  Visos šajos algoritmos nākamais iekodējamais/atkodējamais simbols atkarīgs no 
  iepriekšējiem simboliem (un algoritma iekšējā stāvokļa). Parasti paralelizēt nevar. 

  * Ar Hafmana kodiem var mēģināt paralelizēt dažādu datu bloku iekodēšanu un atkodēšanu
    vairākos pavedienos.
  * GPU izmantot nevar, jo aprēķini katrā pavedienā izskatās citādi. 

  Varbūt iespējamas saspiešanas/atspiešanas instrukcijas uz garākiem vektoriem, 
  ja ievades dati iegūti kādā īpašā veidā.  
  Bet pagaidām rezultātu par to nav.

  

Uzdevumi
---------

**2.1. uzdevums:**
  Aritmētisko kodu definē garai virknei, ko veido 
  no diviem ziņojumiem :math:`(A,B)` ar varbūtībām :math:`p(A) = 0.9`, :math:`p(B) = 0.1`.  
  Šajā aritmētiskajā kodā nosūta :math:`1/3` (binārajā pierakstā :math:`0.010101\ldots_2`). 
  Ja :math:`1/3` atkodē, ar cik ziņojumiem "A" sākas virkne, pirms 
  tajā parādās pirmais "B".


.. only:: Internal  

  **Atbilde:** 

    * Ja :math:`x \geq 0.9`, tad :math:`x` atkodējums sākas ar `B`.
    * Ja :math:`x < 0.9` un :math:`x \geq (0.9)^2`, tad atkodējums sākas ar `AB`.
    * Ja :math:`x < (0.9)^2` un :math:`x \geq (0.9)^3`, tad atkodējums sākas ar `AAB`.
    * Ja :math:`x < (0.9)^3` un :math:`x \geq (0.9)^4`, tad atkodējums sākas ar `AAAB`.

    Šeit :math:`x = \frac{1}{3}`. Jāatrod mazākais :math:`k-1`, kuram 

    .. math::

      1/3 \geq (0.9)^k\;\;\text{jeb}\;\;-\ln 3 \geq k \cdot \ln 0.9 

    Tā kā :math:`\ln 0.9 < 0`, tad :math:`k \geq \frac{-\ln 3}{\ln 0.9} \approx 10.43`. 
    Mazākā veselā $k$ vērtība ir :math:`11`, tātad :math:`x = 1/3` atkodējumā 
    vispirms būs :math:`k-1 = 10` ziņojumi `A`, pēc tam sekos ziņojums `B`.


    .. note::
      :math:`{\displaystyle \frac{1}{3}}` 
      binārais pieraksts: 
      Summējot :math:`0.010101\ldots` nenulles ciparus, iegūstam:

    .. math::

      \frac{1}{4} + \frac{1}{16} + \frac{1}{64} + \ldots = \frac{1/4}{1 - 1/4}.

    *Bezgalīgas ģeometriskas progresijas summas formula:*

      .. math::

        b_1 + b_1q + b_1q^2 + b_2q^3 + \ldots = \frac{b_1}{1 - q}.


  :math:`\square`


**Kopsavilkums** 

1. Ar Hafmana algoritmu uzbūvēts prefiksu koks ir savā ziņā optimāls kodējums, 
   bet tas katru ziņojumu iekodē ar veselu skaitu bitu. Var nevajadzīgi iztērēt 
   līdz pat :math:`1` bitam uz katru nosūtāmo ziņojumu. 
2. Aritmētiskais kods var nedaudz aizturēt bitu plūsmas izvadi 
   (lai pareizi iekodētu iepriekšējo ziņojumu reizēm ir jāzina nākamais ziņojums), 
   toties nezaudē bitus. 
3. Aritmētiskās saspiešanas pamatalgoritms izmanto reālos skaitļus - to ir grūti 
   implementēt korekti, tas arī ir lēnāks un var prasīt vairāk atmiņas. 
   Tāpēc praksē izmantot veselo skaitļu variantu. 
4. Kopš 1986.g. pazīstams arī aritmētiskā koda variants, kurā nevajag reizināt 
   (pietiek ar bitu nobīdēm). 
5. Aritmētiskā koda idejas var pielāgot arī adaptīviem modeļiem, kuri ņem vērā 
   ziņojumu sadalījuma nosacītās varbūtības. 
6. 1980-tajos un 1990-tajos gados vairumu saprātīgo aritmētiskā kodējuma lietojumu 
   ierobežoja patenti. Tādēļ `bzip2` arhivators un JPEG failu formāts 
   izmantoja Hafmana kodējumu (mazāk optimāls viņu vajadzībām, bet bez patentu 
   ierobežojumiem). Patenti, kuru pieteikumi tika iesūtīti jau 
   1976.g. (Jorma Rissanen, IBM) joprojām iespaido tehnoloģiju standartus. 
7. 2004.g. publicētais video kodeka standarts H.264/AVC izmanto aritmētiskā kodējuma 
   variantu CABAC - `Context-adaptive binary arithmetic coding 
   <https://en.wikipedia.org/wiki/Context-adaptive_binary_arithmetic_coding>`_. 



**Bibliogrāfija:** 

**(Wiki:ANS)** 
  `Pārskats par asimetriskām skaitīšanas sistēmām <https://en.wikipedia.org/wiki/Asymmetric_numeral_systems>`_
