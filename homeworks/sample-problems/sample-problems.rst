DatZ 4020: Kontroldarbu uzdevumu piemēri
====================================================

Šajā dokumentā iekļautie uzdevumi iecerēti kā paraugi, lai gatavotos 
kontroldarbiem semestra vidū vai beigās. 

Daži uzdevumi var prasīt skaitļošanas ierīces vai arī ir 
nedaudz grūtāki kā citi -- tie zemāk atzīmēti kā 
paraugi kontroldarbu neklātienes daļai. 

Entropija un entropijas saspiešana (1. un 2. tēmas)
-----------------------------------------------------

Uzdevumi par entropiju, Hafmana kods, aritmētiskais kods. 

**1.uzdevums (Aritmētiskā saspiešana):**
  Pieņemsim, ka burtu biežumi ir `a` -- 50%, `b` -- 20%, `c` -- 10%, `d` -- 20%.

  **(A)** 
    Nokodēt vārdu :math:`\mathtt{abcd}`;

  **(B)** 
    Noteikt, kādu vārdu garumā :math:`4` kodē skaitlis :math:`0.784`.


**2.uzdevums (Entropija):**
  Spēlētājs :math:`X` vienā gājienā izņem no urnas trīs kartiņas. 
  Pieņemsim, ka urna ir ļoti liela, kartiņas tajā nekad nebeidzas un ir vienādas varbūtības
  izķeksēt jebkuru no burtiem `A`, `B` vai `C`; citu burtu urnā nav.

  Pēc tam :math:`X` sakārto trīs kartiņas alfabētiskā secībā un nosūta 
  spēlētājam :math:`Y` ziņojumu -- to burtu, kurš 
  pēc sakārtošanas bija pirmais. (Piemēram, ja izķeksētie burti ir `CBC`, 
  tad pēc sakārtošanas tie būs `BCC` un 
  :math:`X` nosūta ziņojumā pirmo burtu `B`.) 

  **(A)**
    Kāds ir informācijas saturs ziņojumiem `A`, `B`, `C`?

  **(B)**
    Kāda ir entropija jebkuram vienam ziņojumam, ko :math:`X` nosūta 
    :math:`Y` saskaņā ar augšminēto procedūru?


**3.uzdevums (Hafmana koks):** 
  Hafmana koku sauksim par *kanonisku*, ja izpildās sekojošas īpašības: 

  * Visi kanoniskā koka zari (ceļi no saknes līdz lapām/ziņojumiem) veido garumus, kuri ir nedilstošā secībā, skaitot no augšas uz leju.
  * Vienāda garuma zariem ziņojumi izkārtoti ziņojumu alfabētiskā secībā. 

  Sk. attēlu.  1.piemērā zaru garumi nav nedilstošā secībā
  (zars :math:`\mathtt{11}` uz lapu :math:`\mathtt{A}` ir garumā :math:`2`, 
  virs tā divi zari garumā :math:`3`). 
  
  2.piemērā :math:`\mathtt{C}`, :math:`\mathtt{D}` ir ar vienādi gariem kodavārdiem,
  bet nav alfabētiskā secībā. 
  
  Vienīgi 3.piemērā Hafmana koks ir kanonisks.

  .. figure:: figs/huffman-examples.png
     :width: 4in


  **(A)**
    :math:`5` ziņojumu kopai :math:`\{ \mathtt{A},\mathtt{B},\mathtt{C},\mathtt{D},\mathtt{E} \}`, 
    kuru varbūtības ir attiecīgi 
    :math:`{\displaystyle \left\{ \frac{1}{15}, \frac{2}{15},\frac{3}{15},\frac{4}{15},\frac{5}{15} \right\}}`,
    izveidot Hafmana koku.

  **(B)** 
    Pārveidot Hafmana koku kanoniskā formā.


**4.uzdevums (Aritmētiskais kods; neklātienes daļai):** 
  Dota ziņojumu kopa :math:`S = \{ A,B,C,D \}` ar attiecīgajām varbūtībām 
  :math:`\{ 0.2, 0.5, 0.2, 0.1 \}`.

  **(A)** 
    Parādīt, kā iegūt aritmētisko kodu :math:`6` 
    ziņojumu virknei :math:`\mathtt{CBAABD}` -- uzkonstruēt
    atbilstošo intervālu :math:`[l_6;l_6+s_6) \in [0;1]` 
    un atrast īsāko bitu virkni :math:`d_1d_2\ldots{}d_{\ell}` 
    (visi :math:`d_k \in \{ 0,1 \}`), kur pierakstot binārā 
    pieraksta daļskaitlim :math:`D = 0.d_1d_2\ldots{}d_{\ell}\ldots` 
    galā jebkuru turpinājumu ar cipariem :math:`0` vai :math:`1`, 
    iegūtais skaitlis :math:`d+\varepsilon` pieder
    intervālam :math:`[l_6;l_6+s_6)`.

  **(B)**
    Noteikt, kādu ziņojumu virkni alfabētā :math:`S` kodē skaitlis 
    :math:`D'' = 0.0011101011_2`.
    



**5.uzdevums (nav piemērots kontroldarbiem):**
  Mums ir teksts, kurā sastopami 
  :math:`n = 2^k` dažādi simboli (:math:`k \geq 2`)
  ar biežumiem :math:`p1,p2,\ldots,pn` (:math:`p_1 + p_2 + \ldots + p_n =1`).
  Šim tekstam Hofmana kodējumā katrs no simboliem tika iekodēts 
  par virkni garumā tieši k biti. Pierādīt, ka katram :math:`i` no 
  :math:`1` līdz :math:`n` ir spēkā:

  **(A)**  
    :math:`{\displaystyle p_i \leq \frac{2}{5}}` , ja :math:`k = 2`.

  **(B)**
    :math:`{\displaystyle p \leq \frac{2}{2^k+1}}` ,ja :math:`k` ir patvaļīgs.


**6. uzdevums (nav piemērots kontroldarbiem):**
  Pieņemsim, ka ziņojumu kopai :math:`S = \{ x_1, x_2, \ldots, x_n \}` 
  ir izveidots optimāls prefiksu kodējums. Šis kodējums jāpārraida,
  izmantojot minimālu bitu skaitu.

  Pierādīt vai apgāzt šādu apgalvojumu: 
  
    Jebkuru optimālu prefiksu 
    kodējumu šai :math:`n` ziņojumu kopai var nosūtīt, izmantojot ne vairāk kā 
    :math:`{\displaystyle 2n - 1 + n \left\lceil log_2 n \right\rceil}` bitus. 
    
    Šeit :math:`\lceil x \rceil` apzīmē noapaļošanu uz augšu jeb 
    mazāko veselo skaitli, kas nav mazāks par :math:`x`. 
    Piemēram, :math:`\lceil 17 \rceil = 17` un 
    :math:`\lceil 3.14 \rceil = 4`.

  (*Ieteikums:* Izmantojot :math:`2n-1` bitus, var attēlot kodējumu koka 
  virsotņu apstaigāšanas secību.)




Vārdnīcu un konteksta saspiešana (3. un 4. tēma)
---------------------------------------------------

Lempela-Ziva saimes saspiešanas algoritmi, Berouza-Vīlera transformācija. 

**7.uzdevums (Lempela-Ziva metode)**

  **(A)** 
    Ar LZ78 metodi nokodēt tekstu:   
    :math:`\mathtt{abracadabra, abracadabra}`

  **(B)** 
    Atkodēt ar LZ78 metodi nokodētu tekstu :math:`\mathtt{a, b, c, d, 2, 5, a, 6}`, 
    kur :math:`\mathtt{a}`, :math:`\mathtt{b}` un :math:`\mathtt{c}` apzīmē atbilstošos burtus, bet skaitļi -- vārdnīcas virkņu numurus.

  **(C)** 
    Nokodēt (A) punkta tekstu :math:`\mathtt{abracadabra, abracadabra}` ar 
    LZ77 metodi, kā logu lietojot visu nokodēto/atkodēto tekstu.


**8.uzdevums:**
  Izmantojot LZ78 algoritmu 6 simbolu alfabētam 
  :math:`\{\mathtt{C}, \mathtt{E}, \mathtt{L}, \mathtt{N},\mathtt{S}, \mathtt{U}\}`,
  izveidot tabulu un nokodēt sekojošu :math:`15` simbolu ziņojumu: :math:`\mathtt{SUCCESSLESSNESS}`. 
  Tabulā attēlot soļa numuru, :math:`w` - garāko vārdnīcā jau atrodamo simbolu virkni, 
  :math:`k` - virknei :math:`w` sekojošo simbolu, algoritma izvadi un 
  vārdnīcai attiecīgajā solī pievienojamo vārdu. 


  ==========  ==========  ==========  ==========  ===================
  Solis       :math:`w`   :math:`k`   Izvade      Pievieno vārdnīcai
  ...         ...         ...         ...         ...
  ==========  ==========  ==========  ==========  ===================




    
**9.uzdevums (Burrows-Wheeler kodēšana un atkodēšana):** 

  **(A)** 
    Kāds ir rezultāts, lietojot Burrows-Wheeler transformāciju un
    Move-to-Front kodēšanu simbolu virknei :math:`\mathtt{abcabdabc}`?

  **(B)** 
    Pēc BW transformācijas pielietošanas tika iegūta simbolu virkne :math:`dbbacaa`. 
    Kāda bija simbolu virkne pirms transformācijas (ņemot 5. virkni no atjaunotās tabulas)?



**10.uzdevums (neklātienes daļai):** 

  **(A)**
    Kāds ir rezultāts (transformētā simbolu virkne un sākotnējās virknes pozīcija), 
    lietojot Berouza-Vīlera transformāciju 
    :math:`14` simbolu virknei :math:`alusariirasula`?

  **(B)**
    Kāds ir iepriekšējā piemērā iegūtās transformētās simbolu virknes pieraksts,
    izmantojot Move-to-Front kodēšanu?

  **(C)** 
    Pēc BW transformācijas pielietošanas tika iegūta simbolu virkne 
    :math:`\mathtt{mmmrvvauuuiibbbri}`. 
    Kāda bija simbolu virkne pirms 
    transformācijas (ņemot 4. virkni
    no atjaunotās tabulas)?






Mediju saspiešana (5. un 6. tēma)
------------------------------------


**11.uzdevums (Diskrētā krāsu plakne YCbCr):** 
  Koordinātes :math:`(Y,Cb,Cr)` 
  aprēķina no koordinātēm :math:`(R,G,B)` atbilstoši šādai vektoru algebras sakarībai:

  .. math::

    \left( \begin{array}{c}
    Y\\
    Cb\\
    Cr
    \end{array} \right) = 
    \left( \begin{array}{ccc}
    65.48 & 128.55 & 24.97\\
    -37.78 & -74.16 & 111.93\\
    111.96 & -93.75 & -18.21
    \end{array} \right) \left( \begin{array}{ccc}
    \frac{1}{255} & 0 & 0\\
    0 & \frac{1}{255} & 0\\
    0 & 0 & \frac{1}{255}
    \end{array} \right) 
    \left( \begin{array}{c}
    R\\
    G\\
    B
    \end{array} \right) + \left( \begin{array}{c}
    16\\
    128\\
    128
    \end{array} \right).

  Sk. `<https://onlinelibrary.wiley.com/doi/full/10.1002/col.22291>`_. 
  Atrast YCbCr koordinātes zemāk minētajām krāsām, kas uzdotas :math:`(R,G,B)` krāsu plaknē
  (un noapaļot visas :math:`(Y,Cb,Cr)` koordinātes līdz tuvākajam veselajam skaitlim). 

  **(A)** 
    Baltai krāsai :math:`\mathtt{\#FFFFFF}` jeb :math:`(R,G,B) = (255,255,255)`. 

  **(B)**
    Ciāna krāsai  :math:`\mathtt{\#00FFFF}` jeb :math:`(R,G,B) = (0,255,255)`.

  **(C)**
    Magentas krāsai :math:`\mathtt{\#FF00FF}` jeb :math:`(R,G,B) = (255,0,255)`. 

  **(D)** 
    Dzeltenai krāsai :math:`\mathtt{\#FFFF00}` jeb :math:`(R,G,B) = (255,255,0)`.

  **(E)**
    Melnai krāsai  :math:`\mathtt{\#000000}` jeb :math:`(R,G,B) = (0,0,0)`.




**12.uzdevums (Diskrētais kosinusu pārveidojums, neklātienes daļai):**
  Dota funkcija :math:`f(x)`, kas definēta argumentiem :math:`x=0,1,\ldots,N-1`. 
  Par 1-dimensionālu DCT (diskrēto kosinusu pārveidojumu, *discrete cosine transform*) 
  sauksim funkciju :math:`F(u)`, kas definēta tām pašām argumenta vērtībām :math:`u=0,1,\ldots,N-1` 
  ar šādām vienādībām: 

  .. math::

    F(u) = \sqrt{\frac{2}{N}} \sum\limits_{x=0}^{N-1} \lambda_u \cdot 
    \cos \left( \frac{\pi u}{N}\left(  x+\frac{1}{2} \right) \right) \cdot f(x),


  kur :math:`u=0,1,\ldots,N-1` un :math:`\lambda_u = \frac{1}{\sqrt{2}}` 
  (pie :math:`u=0`) un :math:`\lambda_u = 1` (pie :math:`u>0`).
  Sk. `<https://bit.ly/3fcbrC2>`_. 

  Par *inverso diskrēto kosinusu pārveidojumu* sauksim atgriešanos no funkcijas 
  :math:`F(u)` atpakaļ pie funkcijas $f(x)$, ko definē ar šādām vienādībām:

  .. math:: 

    f(x) = \sqrt{\frac{2}{N}} \sum\limits_{u=0}^{N-1} \lambda_u \cdot 
    \cos \left( \frac{\pi u}{N}\left(  x+\frac{1}{2} \right) \right) \cdot F(u),

  kur :math:`x=0,1,\ldots,N-1` un :math:`\lambda_u` definēti tāpat kā agrāk.

  **(A)**
    Aprēķināt diskrēto kosinusu pārveidojumu :math:`F(u)` punktā :math:`u=3`
    funkcijai :math:`f(x) = (N-1)-x`, kur :math:`N=8`. 
    Atbildi noapaļot līdz 4 cipariem aiz komata.


  **(B)**
    Aprēķināt inverso diskrēto kosinusu pārveidojumu :math:`f(x)` visiem 
    punktiem :math:`x=0,1,2,3,4,5,6,7` no funkcijas :math:`F(u)`, kas uzdota ar
    sekojošām :math:`N=8` vērtībām:

    .. math::

      (F(0),F(1),F(2),F(3),F(4),F(5),F(6),F(7)) = (57.9828,-6.4423,0,-0.6735,0,-0.2009,0,-0.0507).

    Atbildi noapaļot līdz 4 cipariem aiz komata.



Kļūdu korekcija (7. un 8. tēma)
---------------------------------


**13.uzdevums (neklātienes daļai):**
  Ziņojums nokodēts ar grafu kodu, kas atbilst augstāk uzzīmētajam grafam 
  (:math:`x_i` ir ziņojuma biti, :math:`y_i` ir kontrolbiti). 
  Saņemot pazaudēti :math:`3` ziņojuma biti. 
  Rezultātā kā ziņojuma biti :math:`x1,\ldots , x_6` saņemti :math:`\mathtt{*, 1, *, 1, 0, *}`
  (Šeit un citur ar :math:`\ast` apzīmē pazaudētu vērtību). Kā kontrolbiti 
  :math:`y_1, \ldots , y_4` saņemti :math:`0, 1, 0, 0`. Atjaunot trūkstošos bitus.

  .. note:: 
    Grafu kodā virsotnes  :math:`x_1,\ldots , x_{15}` ir savienotas ar kontrolbitu 
    virsotnēm :math:`y_1, \ldots ,y_k` tā, ka kontrolbits :math:`y_j` veidojas, 
    saskaitot (pēc moduļa 2) visus tos datu bitus, kuri grafā ir ar šo kontrolbitu savienoti. 

**14.uzdevums (neklātienes daļai):** 

  **(A)**
    Uzrakstīt grafu kodu ar 9 ziņojuma bitiem :math:`x_1,\ldots , x_{15}` un pēc 
    iespējas mazāku skaitu kontrolbitu :math:`y_1, \ldots ,y_k` tā, 
    lai kods spētu atjaunot jebkurus :math:`2` pazaudētus ziņojuma bitus :math:`x_i`.

  **(B)**
    Pamatot, ka mazāks kontrolbitu skaits nav iespējams.

  **(C)** 
    Uzrakstīt grafu kodu ar :math:`9` ziņojuma bitiem 
    :math:`x_1, \ldots, x_{15}` un pēc iespējas mazāku skaitu kontrolbitu 
    :math:`y_1, \ldots, y_k` tā, lai kods spētu atjaunot jebkurus :math:`3` 
    pazaudētus ziņojuma bitus :math:`x_i`.


**15.uzdevums (Heminga kodi, neklātienes daļai):** 
  
  Pseidonejaušu skaitļu vikrnes iegūšanai 
  uzrakstām skaitļa :math:`\pi = 3.14159\ldots` pierakstu divnieku skaitīšanas sistēmā un 
  grupējam tā ciparus aiz komata -- divas grupas pa :math:`7` un divas grupas pa :math:`15`:

  .. math:: 
    
    \pi = 11.\underbrace{0010010}\underbrace{0001111}\underbrace{110110101010001}\underbrace{000100001011010}\ldots_2.

  Atrast kļūdas (ja tādas ir) atbilstošajos Heminga koda ziņojumos:

  **(A)**
    Heminga koda ziņojums `0010010` (:math:`7`-bitu Heminga kods, bitu secība apgriezti leksikogrāfiska
    -- no :math:`x_{111}` līdz :math:`x_{001}`). 
    Atrast kļūdaino pozīciju, ja tāda ir, un uzrakstīt šo :math:`7`-bitu kodu bez kļūdām.

  **(B)**
    Heminga koda ziņojums `0001111` (:math:`7`-bitu Heminga kods) -- 
    izlabot kļūdas, ja tās ir, un uzrakstīt :math:`4` ziņojuma bitus :math:`x_1x_2x_3x_4`.

  **(C)** 
    Ziņojums `110110101010001` ir :math:`15`-bitu Heminga kods, 
    bitu secība apgriezti leksikogrāfiska -- no :math:`x_{1111}` līdz :math:`x_{0001}`. 
    Atrast kļūdaino pozīciju, ja tāda ir, un uzrakstīt šo kodu bez kļūdām.

  **(D)**
    Heminga koda ziņojums `000100001011010` (:math:`15`-bitu Heminga kods) -- 
    izlabot kļūdas, ja tās ir, un uzrakstīt visus ziņojuma bitus 
    (ziņojumu bitu secība apgriezti leksikogrāfiska :math:`x_{1111}\ldots{}x_{0011}`).



(*Galaeksāmena tēmām uzdevumu paraugu vēl nav.*)