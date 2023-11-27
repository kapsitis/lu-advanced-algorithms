Kontroldarbs, 2023-10-24
==========================

Klātienē pildāmās daļas maksimālais vērtējums ir 15 procentpunkti.


**1. uzdevums:** 

Aplūkojam ziņojumu alfabētu ar četriem ziņojumiem: :math:`S = \{\mathtt{a}, \mathtt{b}, \mathtt{c}, \mathtt{d}\}`,
kuru varbūtības ir attiecīgi :math:`\{1/3, 1/3, 2/9, 1/9\}`. Hafmana algoritma pseidokods ir sekojošs:

| :math:`\text{\sc Huffman}(S)`
| 1. :math:`n = |S|` :math:`\;\;\;\;` *(elementu skaits)*
| 2. :math:`Q = \text{\sc MinimumPriorityQueue}(S)`
| 3. **for** :math:`i = 1` **to** :math:`n-1`: 
| 4. :math:`\;\;\;\;` izveido jaunu mezglu :math:`z`
| 5. :math:`\;\;\;\;` :math:`z.\mathit{left} = x = Q.\text{\sc ExtractMin}()`
| 6. :math:`\;\;\;\;` :math:`z.\mathit{right} = Y = Q.\text{\sc ExtractMin}()`
| 7. :math:`\;\;\;\;` :math:`z.\mathit{freq} = x.\mathit{freq} + y.\mathit{freq}`
| 8. :math:`\;\;\;\;` :math:`Q.\text{\sc insert}(z)`
| 9. **return** :math:`Q.\text{\sc ExtractMin}()`

.. note:: 
  Šis algoritms savā prioritāšu rindā glabā bināros kokus. Sākumā šajā rindā ir atsevišķie ziņojumi -- 
  katrs no tiem ir koks ar vienu mezglu.  
  Par minimālo elementu prioritāšu rindā :math:`Q` uzskatām to mezglu, kuram ir mazākā varbūtība (t.i. varbūtību summa 
  visiem ziņojumiem pie šī mezgla). 
  Ja diviem mezgliem ir vienādas varbūtības, tad to, kurš būs minimālais, var izvēlēties Jūsu implementācija.

**(A)** 
  Uzzīmēt prioritāšu rindā esošos kokus pirms katras cikla **for** iterācijas (4.rindiņa). 

**(B)** 
  Parādīt, kāds izskatīsies prefiksu koks, ko izveido Hafmana algoritms. (Koks nav jāpārveido par kanonisku koku.)

**(C)**
  Kods :math:`C` ir funkcija, kas četrus ziņojumus attēlo par bitu virknītēm (iespējams, atšķirīga garuma). 
  Atrast :math:`\ell(C)` (*expected length of a code*)-- vidējo vērtību bitu skaitam, lai iekodētu vienu 
  nejauši izvēlētu ziņojumu ar šo koku atbilstoši varbūtību sadalījumam.

**(D)**
  Vai var uzzīmēt citu prefiksu koku, kurš rada citu kodējumu :math:`C'`, kurš ir tikpat optimāls kā Hafmana koks 
  (t.i. :math:`\ell(C) = \ell(C')`), bet tas nevar izveidoties Hafmana algoritma rezultātā.


**2. uzdevums:** 
  Alfabēta burti sakārtoti šādi: 
  :math:`\mathcal{A}=\{\textcolor{blue}{\mathtt{\$}},\textcolor{blue}{\mathtt{A}},\textcolor{blue}{\mathtt{C}}, \textcolor{blue}{\mathtt{L}},\textcolor{blue}{\mathtt{M}},\textcolor{blue}{\mathtt{N}},\textcolor{blue}{\mathtt{P}} \}`. 

  **(A)** 
    Izpildīt Berouza-Vīlera transformāciju ievades virknei jeb stringam
    :math:`\textcolor{blue}{\mathtt{PANAMACANAL\$}}`. 

  **(B)** 
    Veikt transformācijas rezultātam "move to front" kodējumu. 
      


**3. uzdevums:** 
  Kosmisko azartspēļu serverim jāsūta 
  :math:`6` dažādi ziņojumi (metamā kauliņa rezultāti). Sakaru kanālā vienam metienam var atvēlēt 
  :math:`n = 6` bitus -- visiem metieniem sūtāmo bitu skaits ir vienāds. 
  Pa ceļam pie saņēmēja ne vairāk kā viens no šiem bitiem var 
  sabojāties (:math:`0` vietā aizsūta :math:`1` vai otrādi).
  Saņēmējam jāvar saprast, kurš metiena rezultāts tika nosūtīts arī tad, ja ir kļūda. 

  **(A)** 
    Piedāvāt kodu tabuliņu, kas katram metiena rezultātam (no :math:`\mathtt{"1"}` 
    līdz :math:`\mathtt{"6"}`) parāda sūtāmos :math:`n` bitus. 
    Pamatot, kāpēc kļūdu vienmēr varēs izlabot. 

  **(B)** 
    Ieviešam gadījumlielumu :math:`X`, kas satur visas :math:`n`-bitu virknītes, kuras 
    var nonākt pie saņēmēja (to ir vairāk nekā :math:`6`, jo jāapskata arī virknītes ar kļūdām). 
    Pieņemam, ka visi metamā kauliņa rezultāti ir ar vienādu varbūtību; un katrs bits var 
    sabojāties ar vienādu varbūtību :math:`\frac{1}{n+1}`. 
    Atrast entropiju gadījumlielumam :math:`H(X)`.

  **(C)** 
    Kā zināms, Heminga (*Hamming*) kods ir :math:`[7,4,1]` kļūdu korekcijas kods. 
    Definēt, ko nozīmē :math:`[6,6,1]` kļūdu korekcijas kods. Vai punktā (A) aprakstītā 
    tabuliņa ir :math:`[6,6,1]` kļūdu korekcijas kods?




**Mājās pildāmā daļa (iesūtāma līdz 2023-10-26):** 

Neklātienē pildāmās daļas maksimālais vērtējums ir 15 procentpunkti. 
Atrisinājumi jāiesūta PDF formā E-studijas vidē līdz 26.oktobra dienas beigām. 
(Par katru nokavēto dienu, šīs daļas vērtējums tiks samazināts par 3 procentpunktiem.)


**4. uzdevums:** 

Pārveidot savas studenta apliecības 5 ciparus par vārdu, izmantojot šādu tabulu: 

========  =========
Cipars    Teksts 
========  =========
0         AB
1         RA 
2         CA 
3         DA 
4         BRA 
5         ABR 
6         AC 
7         AD 
8         AB  
9         RA 
========  =========

Teiksim, studenta apliecības numurs `xx12014` pārveidosies par tekstu "RACAABRABRA".
Iekodēt iegūto tekstu, izmantojot LZ78 algoritmu. 

.. note:: 
  Algoritms numurē vārdnīcas elementus sākot ar numuru "1". 
  Kamēr vārdnīcā nav atrodams garāks savienojums ar attiecīgo burtu, katrs burts kodē pats sevi
  (var uzskatīt, ka visi burti A,B,C,D,R vārdnīcā ir jau pašā sākumā). 



**5. uzdevums:** 
  Sk. `<https://github.com/kapsitis/lu-datastructures-workspace/tree/main/JPEG>`_. 
  Sadalīt attēlu `kuldiga.png` 3 attēlos YCbCr krāsu telpā (līdzīgi kā to dara H.264 algoritms). 
  Visus trīs attēlus kā PNG attēlus iekopēt savā darbā (PDF dokumentā). 
  Piemērs, kā izskatās YCbCr krāsu modelī sadalīts attēls ir atrodams Vikipēdijā:
  `<https://en.wikipedia.org/wiki/YCbCr>`_. 





**6. uzdevums:** 

Kā ieejas datus izmantot Kuldīgas tilta melnbalto attēlu `kuldiga1.png`.
Pielietot DCT blokiem :math:`16 \times 16`. No visiem :math:`16 \times 16` koeficientiem paturēt 
tikai matricas "kreiso augšējo stūri" -- koeficientus, kuriem gan rindiņas, gan kolonnas
numurs ir skaitlis no kopas :math:`\{ 0,1,2,3 \}`.  Pārējos koeficientus pārvērst par nullēm. 
Pārveidot no iegūtajiem koeficientiem atpakaļ par pikseļu vērtībām, izvadīt visu attēlu PNG formā un 
iekopēt to savā darbā (PDF dokumentā). 



 
