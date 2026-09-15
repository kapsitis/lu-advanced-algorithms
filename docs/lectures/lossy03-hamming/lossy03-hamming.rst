Kļūdu korekcija: Heminga kodi
==========================================


**Mērķi**

* Ieviest dažus populārus kļūdu detekcijas algoritmus. 
* Pamatot apgalvojumu par divu kļūdu korekcijas kodu attālumu.
* Lietot un pamatot Heminga kodus. 



**Kļūdu detekcija:**

  .. figure:: figs/error-detection.png
     :width: 4in

**Kļūdu korekcija:** 
  Ideja visās metodēs - papildināt pārraidāmos datus ar 
  papildinformāciju, cerot, ka papildinformācija ļaus pamanīt kļūdas. 

  .. figure:: figs/error-correction.png
     :width: 2in





Kļūdu detekcijas algoritmi
----------------------------




**Bitu paritātes metode**
  Pārraida :math:`n` bitu virkni 
  :math:`x_1,x_2,\ldots,x_n \in \{ 0; 1\}`. 
  Lai konstatētu iespējamu kļūdu 1 bitā (kas var gan 
  iestāties, gan neiestāties), pārraida :math:`n+1` bitus:  
  Visus :math:`x_1,x_2,\ldots,x_n` un arī pēdējo bitu

  .. math::

     \left( x_1 + x_2 + \ldots + x_n \right)\,\text{mod}\,2.


  Pēdējais bits glabā visu iepriekšējo bitu paritāti. 
  Tāpēc visu :math:`n+1` bitu paritāte ir :math:`0`. Ja pārraidē rodas viena
  kļūda, tad paritāte būs :math:`1`, un kļūdu varēs konstatēt. 

**CRC kontrolsumma**

  .. figure:: figs/ethernet-frame.png
     :width: 4in

  "Frame Check Sequence" (FCS) izmanto 
  32-bitu CRC (cyclical redundancy check). 
  Tajā veic bitveida "XOR-ošanu stabiņā" ar maģisko 
  skaitli `0xC704DD7B`. 

  FCS 4 baitos ieraksta CRC doto atlikumu. Viena bita 
  pārbaudīšana nav pietiekami droša; CRC32 ir noturīgāks
  pret pārraides kļūdām, kas var pārmainīt vairākus blakusesošus
  bitus. 

  "Data link layer" (OSI Layer2) izmet tos freimus, 
  kuri ir kļūdaini. Augstāka līmeņa transporta protokoli (TCP) 
  palūdz kļūdainos freimus sūtīt atkārtoti. 

**MD5 hešfunkcija**
  Garākiem failiem (kuri varbūt tikuši bojāti apzināti) var 
  izmantot hešfunkcijas. Piemēram MD5 izveido 128 bitu virknīti 
  (pieraksta kā 32 hex ciparus). 

  .. figure:: figs/hashtools-1.png
     :width: 4in

  MD5 hešfunkcijas kolīzijas ir zināmas.



Kļūdu korekcijas algoritmu jēdzieni
-------------------------------------

**Piemērs: Trīskāršā atkārtošana**

  .. figure:: figs/repetition-code.png
     :width: 4in

  Katru pārraidāmo bitu atkārto trīs reizes. Saņēmējs 
  atrod, kādu bitu ir vairāk -- nuļļu vai vieninieku.
  Šāds kods var izlabot kļūdu vienā bitā.



**Definīcija:** 
  Par :math:`[n,k,d]`-kodu sauc *kļūdu korekcijas kodu*, kurā  

  * `n` - bitu skaits, kurus kodējums faktiski pārraida,  
  * `k` - kodējamo bitu skaits,  
  * `d` - kļūdu skaits, ko iespējams koriģēt.

**Piemērs:** 
  Trīskāršās atkārtošanas metodei `n=3`, `k=1`, `d=1`, tāpēc tas ir
  :math:`[3,1,1]`-kods.


**Negatīvs piemērs**
  Vēlamies veidot kļūdu korekcijas kodu alfabētam, kurā ir 
  `3` ziņojumi: `A = { a,b,c }`. 
  Piedāvājam kodēt ziņojumus `a,b,c` attiecīgi ar kodiem 
  `S = { 1000,0101,1101 }`.  

  Šis kods nespēj koriģēt vienu kļūdu, jo,
  saņemot virkni `0101`, nav skaidrs, vai tika pārraidīta virkne `0101`
  (bez kļūdām) vai arī virkne `1101`
  (ar vienu kļūdu -- pirmajā bitā). Divdomīgs ir arī `1001` u.c.



Kļūdu korekcijas kodu īpašības
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


**Teorēma:** 
  Kopa :math:`S`, kas satur ziņojumu kodus ir :math:`[n,k,d]`-kods tad un tikai tad, ja  

  1. :math:`S` sastāv no virknēm garumā `n`,  
  2. :math:`|S| >= 2^k`, lai visām :math:`k`-bitu virknēm pietiktu kodu.  
  3. katras divas virknes no :math:`S` atšķiras vismaz :math:`2d+1` vietās.

**Pierādījums:** 
  Kods nespēj koriģēt :math:`d` kļūdas, ja eksistē virkne `z = z_1z_2\ldots{}z_n`
  un divas kopas virknes :math:`x=x_1x_2\ldots{}x_n` un :math:`y=y_1y_2\ldots{}y_n`, 
  kas katra atšķiras no :math:`z` ne vairāk kā :math:`d` vietās.
  Līdz ar to virknes :math:`x` un :math:`y` atšķiras ne vairāk kā :math:`2d`
  vietās. Tāpēc, lai kods spētu koriģēt kļūdas, katrām divām kopas :math:`S` virknēm ir
  jāatšķiras vismaz :math:`2d+1` vietās.






**Piemērs n=3:**
  Ja pārraidāmo bitu skaits ir :math:`n=3`, 
  bet maksimāli pieļaujamo kļūdu skaits :math:`d=1`, 
  tad vairāk par divām virknēm kopai :math:`S` nevar
  piederēt. Ja :math:`x_1x_2x_3 \in S`, tad 
  otra var būt vienīgi tāda :math:`y_1y_2y_3`, ka 
  :math:`y_1 \neq x_1`, :math:`y_2 \neq x_2`, :math:`y_3 \neq x_3`. 

**Secinājums:** 
  Eksistē :math:`[n,k,d]` kods :math:`[3,1,1]`, kas 
  :math:`n=3` bitos pārraida :math:`k=1` satura bitu un 
  var izlabot kļūdas, kuru skaits nepārsniedz :math:`d = 1`.  
  Lielāku bitu skaitu nekā :math:`k=1` (jeb divas 
  atšķiramas virknes) pārraidīt nevar.


**Apgalvojums:** 
  Ja pārraida :math:`n=4` bitus, arī tad nevar 
  iekodēt vairāk par divām virknēm (kuras 
  atšķiramas, ja kļūdu skaits nepārsniedz :math:`d=1`). 

**Pierādījums:** 
  Pieņemsim pretējo un aplūkosim trīs virknes, 
  ko satur kopa :math:`S`: :math:`x_1x_2x_3x_4`,  
  :math:`y_1y_2y_3y_4` un :math:`z_1z_2z_3z_4`. 
  Nekādas divas virknes nevar sakrist 
  vairāk kā vienā vietā. 
  Līdz ar to kopējais sakritību skaits 
  nevar būt lielāks par :math:`3`.

  Ja kādā pozīcijā :math:`i` 
  visi trīs biti sakristu (:math:`x_i = y_i = z_i`), tad 
  būtu iegūta pretruna: visas trīs sakritības 
  jau izlietotas, bet kaut kādām sakritībām 
  jābūt arī citās pozīcijās :math:`j \neq i`, 
  jo ir trīs skaitļi :math:`x_j`, :math:`y_j`, :math:`z_j` un 
  tikai divas vērtības. 

  Ja divi biti sakrīt, bet trešais – atšķiras,
  tad sakritību skaits šajā bitā ir 1.
  Tā kā mums ir 4 biti, tad varam secināt, 
  ka kopējais sakritību skaits būs vismaz 4, kas ir pretrunā ar to, ka šis skaits nevar būt lielāks par 3. 

  Tātad kopa :math:`S` nevar saturēt vairāk par divām virknēm. 
  :math:`\blacksquare`




**Piemērs, ja n=5, k=2**

=============  =============  ====================================================
:math:`x_1`    :math:`x_2`    :math:`x_1,x_1,x_2,x_2,(x_1 + x_2)\,\text{mod}\,2`
=============  =============  ====================================================
0              0              00000
0              1              00111
1              0              11001
1              1              11110
=============  =============  ====================================================

Tabula parāda, kā kodēt divu bitu virknītes par piecu bitu 
virknītēm: divreiz pārraida pirmo bitu, divreiz - otro, 
bet pēdējais baits ir abu satura bitu paritāte. 

*Piezīme:* Tabulā redzams :math:`[5,2,1]`-kods. 


**Vai pie n=5 būt vairāk par 4 virknēm?**

**Apgalvojums:** 
Kopa :math:`S` pie :math:`n=5` un :math:`d=1` nevar saturēt vairāk par četrām virknēm. 


Pieņemsim pretējo un aplūkosim piecas virknes, ko satur kopa :math:`S`. 
Vismaz trim no tām pirmais bits būs vienāds, t.i., vai nu būs 
vismaz :math:`3` virknes, kurām pirmais bits vienāds ar :math:`0`, 
vai arī vismaz :math:`3` virknes, kurām pirmais bits vienāds ar :math:`1`. 

Šīm trim virknēm atšķirības var būt tikai pēdējos četros bitos. 
Bet četru bitu gadījumā jau tika pierādīts, ka lielākais 
atšķiramo virkņu skaits ir :math:`2`. Tāpēc kādas divas no 
šīm trim virknēm atšķirsies mazāk nekā trijās vietās.
Pretruna. :math:`\blacksquare`


Heminga kodi
--------------


**Ja pārraida n=7 bitus**

  No :math:`n=7` iespējams izveidot :math:`2^4 = 16` atšķiramas virknes:

  .. code-block:: text

    0000000
    0000111
    0011001
    0011110
    0101010
    0101101
    0110011
    0110100
    1100001
    1100110

**Heminga koda konstruēšana**
  Virkni :math:`x_1x_2x_3x_4` pārraida 
  kā :math:`x_1x_2x_3y_1x_4y_2y_3`, kur 

  .. math:: 

    \begin{array}{l}
    y_1 = \left( x_1 + x_2 + x_3 \right)\,\text{mod}\,2\\
    y_2 = \left( x_1 + x_2 + x_4 \right)\,\text{mod}\,2\\
    y_3 = \left( x_1 + x_3 + x_4 \right)\,\text{mod}\,2\\
    \end{array}

  Šis ir :math:`[7,4,1]`-kods, ko sauc arī par *Heminga kodu* (*Haming code*).



**Apgalvojums par Heminga kodu [7,4,1]**
  Katras divas Heminga koda
  7-bitu virknes atšķirsies vismaz :math:`3` vietās
  (tātad varēs izlabot vienu kļūdu). 

**Pierādījums:** 
  Apskatīsim jebkuras divas
  pareizi izrēķinātas (bez kļūdām saņemtas)
  virknes :math:`x_1x_2x_3y_1x_4y_2y_3` un 
  :math:`x'_1x'_2x'_3y'_1x'_4y'_2y'_3`.

  **1.gadījums:** 
    Atšķiras viens :math:`x_i`.  
    Katrs :math:`x_i` ietilpst vismaz :math:`2` no formulām 
    priekš :math:`y_1`, :math:`y_2`, :math:`y_3` un, mainoties :math:`x_i` vērtībai,
    mainīsies šo formulu vērtības. 
    Tāpēc virknes atšķiras vismaz :math:`3` vietās: vienā :math:`x_i` un
    vismaz divos :math:`y_i`.

    .. math:: 

      \begin{array}{l}
      y_1 = \left( x_1 + x_2 + x_3 \right)\,\text{mod}\,2\\
      y_2 = \left( x_1 + x_2 + x_4 \right)\,\text{mod}\,2\\
      y_3 = \left( x_1 + x_3 + x_4 \right)\,\text{mod}\,2\\
      \end{array}


  **2.gadījums:** 
    Atšķiras divi :math:`x_i`.  
    Apzīmējam atšķirīgos bitus ar :math:`x_i` un :math:`x_j`. 
    Lai kādi būtu :math:`i` un :math:`j`, mēs vienmēr varam atrast
    vienu no :math:`y_i` formulām, kurā ietilpst viens no 
    :math:`x_i` un :math:`x_j`, bet ne otrs. Virknes atšķirsies
    vismaz :math:`3` vietās: divos :math:`x_i` un šajā vienā :math:`y_i`.

  **3.gadījums:** 
    Atšķiras trīs :math:`x_i`.  
    Tad uzreiz ir :math:`3` atšķirības attiecīgajos :math:`x_i` (jo tos 
    pārraida arī pašus).



**Heminga kods: Vispārīgais gadījums**
  Heminga kods sastāv no :math:`2^n-1` bitu virknēm, 
  kurās :math:`2^n-n-1` biti tiek izmantoti ziņojumam, bet :math:`n` 
  ir kontrolbiti, kas tiek izrēķināti no ziņojuma bitiem.

  Lai aprakstītu šo kodu, sanumurējam :math:`2^n-1` bitu pozīcijas 
  ar skaitļiem :math:`1, 2, \ldots, 2^n-1`, 
  šos skaitļus pierakstot binārajā skaitīšanas sistēmā 
  (:math:`000001`, :math:`000010`, :math:`\ldots`, :math:`111111`). 
  Ir :math:`n` skaitļi, kuru binārajā pierakstā ir tieši 
  viens :math:`1` (:math:`000001`, :math:`000010`, :math:`\ldots`, :math:`100000`). 
  Šajās pozīcijās būs kontrolbiti. 

  Pārējās pozīcijas ir ziņojuma biti, kas var būt patvaļīgi.

**Piemēri**
  Vispārinātais Heminga kods ir aprakstāms kā
  :math:`\left[ 2^n - 1, 2^n - n - 1,1 \right]`. 
  Visām :math:`n` vērtībām tas koriģē tikai :math:`1` bitu.

  * :math:`n = 2`, tad Heminga kods :math:`[3,1,1]` (trīskāršā atkārtošana). 
  * :math:`n = 3`, tad Heminga kods :math:`[7,4,1]`. 
  * :math:`n = 4`, tad Hemings :math:`[15,11,1]`. 
  * :math:`n = 5`, tad Hemings :math:`[31,26,1]`. 
  * :math:`n = 6`, tad Hemings :math:`[63,57,1]`.

**Kontrolbitu izrēķināšana**

  .. math:: 

    x_{0\ldots{}010\ldots{}0} = \left( 
    \sum\limits_{i_1,\ldots,i_{k-1},i_{k+1},\ldots,i_{n}}
    x_{i_1\ldots{}i_{k-1}1i_{k+1}\ldots{}i_n} \right)\;\text{mod}\;2

  Lai atrastu, vai ir kļūda, rīkojās šādi. Ja kontrolbits pozīcijā 
  :math:`0\ldots{}010\ldots{}0` (ar 1-nieku :math:`k`-tajā ciparā) 
  **nesakrīt** ar to, kas izrēķināts pēc formulas, 
  tad mēs zinām, ka kādā no bitiem, 
  kuru numuriem :math:`k`-tā pozīcija :math:`=1` ir kļūda. 

  Ja kontrolbits pozīcijā :math:`0\ldots{}010\ldots{}0` (ar 1-nieku :math:`k`-tajā ciparā) 
  **sakrīt** ar to, kas izrēķināts pēc formulas, 
  tad kļūda var būt tikai tajos bitos, kuru numuriem 
  :math:`k`-tajā pozīcijā ir :math:`0` 
  (jo visi biti ar 1 k-tajā pozīcijā ietilpst formulā).

**Kļūdas atrašana**
  Šādā veidā pēc katra kontrolbita var noteikt vienu bitu 
  pozīcijai, kurā ir kļūda, numura. 
  Kontrolbiti tad pilnībā nosaka šīs pozīcijas numuru. 
  Ja iegūtais numurs ir :math:`000\ldots{}000` 
  (t.i., visi kontrolbiti sakrita), tad kļūdas nav vispār. 
  Citādi, mēs zinām, kurā vietā tā ir.

  Kas notiek, ja kļūda ir pašā kontrolbitā?



**Teorēma (Heminga koda optimalitāte):** 
  Ja :math:`S \subseteq \{ 0, 1\}^{2^n-1}` ir kods, kas spēj 
  koriģēt vienu kļūdu, tad 
  :math:`|S| \leq 2^{2^n-n-1}`.

  Šī teorēma nozīmē, ka virkņu skaitu Heminga kodā 
  nevar uzlabot pat par :math:`1` virkni!

**Optimalitātes pierādījums**
  Apzīmējam koda virknes ar :math:`v_1,\ldots,v_m`. 
  Ar :math:`V_i` apzīmējam kopu, kur ietilpst :math:`v_i` un 
  visas virknes, kas atšķiras no :math:`v_i` tieši vienā vietā
  (koda :math:`v_i` ":math:`\varepsilon`-apkārtne"). 

  1. Apkārtnēm :math:`V_i` un :math:`V_j` (:math:`i \neq j`) nav kopīgu elementu, 
     citādi nevarētu veikt kļūdu korekciju. 
  2. Katrā :math:`V_i` ietilpst tieši :math:`2^n` virknes: :math:`v_i` un 
     :math:`2^n - 1` virknes, kas atšķiras no tās kādā :math:`1` pozīcijā. 

  Tāpēc kopās :math:`V_1,V_2,\ldots,V_m` kopā ir :math:`2^n \cdot m` elementi. 
  Tā kā ir pavisam :math:`2^{2^n - 1}` virkņu garumā :math:`2^n-1`, tad

  .. math:: 

    2^n \cdot m \leq 2^{2^n - 1} \Rightarrow m \leq 2^{2^n - n-1}.
 


Citi lineāri kodi
---------------------

**Definīcija**
  Jebkuru kodu, kurā katrs nokodētās virknes bits ir aprakstāms ar formulu

  .. math::

     \left( x_{i_1} + \dots + x_{i_k} \right)\,\text{mod}\,2

  sauc par lineāru kodu. Heminga kods ir lineārs kods un gandrīz visi citi praksē lietotie
  kodi arī ir lineāri.

Lineāru kodu var aprakstīt ar tā ģeneratormatricu. 
Ja :math:`n` ir kodētā ziņojuma garums, bet
:math:`k` -- nokodēto bitu skaits, tad ģeneratormatrica ir :math:`n \times k` matrica. 
Ja bits :math:`x_i` ietilpst formulā pēc kuras rēķina :math:`j`-to nokodētā ziņojuma bitu, 
tad šīs matricas :math:`(i,j)`-ajā vietā ir :math:`1`.
Citādi tur ir :math:`0`. 


**Lineāra koda piemērs**
  Heminga :math:`[7,4,1]` ģeneratormatrica izskatās šādi:

  .. math::

     G = \left(
     \begin{array}{cccc}
     1 & 0 & 0 & 0 \\
     0 & 1 & 0 & 0 \\
     0 & 0 & 1 & 0 \\
     1 & 1 & 1 & 0 \\
     0 & 0 & 0 & 1 \\
     1 & 1 & 0 & 1 \\
     1 & 0 & 1 & 1 
     \end{array} \right)

  1.,2.,3. un 5. rinda apraksta kodētā ziņojuma 
  bitu sakrišanu ar sākotnējā ziņojuma bitiem.  
  Pārējās rindas apraksta formulas kontrolbitiem. 


**Ziņojuma kodēšana**
  Lai nokodētu ziņojumu, mēs aprakstām to ar vektoru:

  .. math::

     \mathbf{x} = \left( \begin{array}{l}
     x_1\\
     x_2\\
     x_3\\
     x_4
     \end{array} \right)

  un tad reizinām šo vektoru ar ģeneratormatricu :math:`M`.  
  Nokodētais ziņojums būs :math:`M\mathbf{x}`, 
  visus tā elementus rēķinot pēc moduļa :math:`2`.


**Lineāra koda atkodēšana**
  Atkodēšanai var izmantot
  paritātes pārbaudes matricu. Hemingam :math:`[7,4,1]` tā ir šāda:

  .. math::

     P = \left( \begin{array}{ccccccc}
     1 & 1 & 1 & 1 & 0 & 0 & 0\\
     1 & 1 & 0 & 0 & 1 & 1 & 0\\
     1 & 0 & 1 & 0 & 1 & 0 & 1
     \end{array} \right)

  Katra tabulas rinda apraksta vienu no Heminga koda pārbaudēm 
  (vai kontrolbits sakrīt ar noteiktu bitu summu pēc mod :math:`2`). 
  
  Ja :math:`\mathbf{y}` -- nokodētais ziņojums, :math:`P` -- paritātes 
  pārbaudes matrica un kļūdu nav, tad, rēķinot pēc mod :math:`2`, jāizpildās

  .. math::

     P\mathbf{y} = \left( \begin{array}{c}
     0 \\ 
     0 \\
     0 
     \end{array} \right)

  Paritātes pārbaudes matricu var izmantot arī, 
  lai noteiktu, kur ir kļūdas, ja tādas ir, 
  bet tas ir sarežģītāk un šajā kursā netiks aplūkots.


Heminga kodu piemēri
-----------------------

**7-bitu Heminga kods**

  ==================================  ===================================  ===================================  ===================================  ===================================  ===================================  ===================================  ===================================
  :math:`x,y` apzīmējumi              :math:`x_1`                          :math:`x_2`                          :math:`x_3`                          :math:`\textcolor{red}{y_1}`         :math:`x_4`                          :math:`\textcolor{red}{y_2}`         :math:`\textcolor{red}{y_3}`
  Apzīmējumi ar bināriem indeksiem    :math:`\textcolor{blue}{x_{111}}`    :math:`\textcolor{blue}{x_{110}}`    :math:`\textcolor{blue}{x_{101}}`    :math:`\textcolor{blue}{x_{100}}`    :math:`\textcolor{blue}{x_{011}}`    :math:`\textcolor{blue}{x_{010}}`    :math:`\textcolor{blue}{x_{001}}`
  ==================================  ===================================  ===================================  ===================================  ===================================  ===================================  ===================================  ===================================




Kodi :math:`x_{111},\ldots,x_{001}` 
izkārtoti *apgrieztā leksikogrāfiskā secībā* 
(*reverse lexicographic order*) -- 
`Wikipedia <https://oeis.org/wiki/Orderings#Reverse_lexicographic_order>`_). 

Kāpēc virknītē :math:`x_1,x_2,x_3,y_1,x_4,y_2,y_3` 
ziņojuma biti :math:`x_i` nedaudz sajaukti ar kontrolbitiem :math:`y_j`?

.. math::

    \left\{
    \begin{array}{l}
    y_{1} = \textcolor{blue}{x_{100}} = \textcolor{blue}{x_{111} \oplus x_{110} \oplus x_{101}} = x_1 \oplus x_2 \oplus x_3\\
    y_{2} = \textcolor{blue}{x_{010}} = \textcolor{blue}{x_{111} \oplus x_{110} \oplus x_{011}} = x_1 \oplus x_2 \oplus x_4\\
    y_{3} = \textcolor{blue}{x_{001}} = \textcolor{blue}{x_{111} \oplus x_{101} \oplus x_{011}} = x_1 \oplus x_3 \oplus x_4
    \end{array} \right.

Ar :math:`x_1 \oplus x_2` apzīmējam 
:math:`\left(x_1+x_2\right)\,\text{mod}\,2`.  
Saskaitīšana pēc moduļa :math:`2` jeb XOR, jeb 
"izslēdzošais VAI".


**Piemērs #1**
  Izmantojot Heminga kodu :math:`[7,4,1]`, nokodēt virkni 0110.


**Atrisinājums**
  Ņemam :math:`x_1 = 0`, :math:`x_2 = 1`, :math:`x_3 = 1`, :math:`x_4 = 0`.  
  Aprēķinot :math:`y_1`, :math:`y_2`, :math:`y_3` saskaņā ar formulām:

  .. math:: 
  
    \left\{
    \begin{array}{l}
    y_1 = x_1 \oplus x_2 \oplus x_3\\
    y_2 = x_1 \oplus x_2 \oplus x_4\\
    y_3 = x_1 \oplus x_3 \oplus x_4
    \end{array} \right.`

  Iegūst :math:`y_1 = 0`, :math:`y_2 = 1`, :math:`y_3 = 1`.  
  Tātad kodētais Ziņojums būs: `0110011`.



**Piemērs #2**
  Izmantojot Heminga kodu :math:`[7,4,1]`, atkodēt virkni `0111101`.



**Atrisinājums**

  .. math:: 

    \left\{
    \begin{array}{l}
    y_1 = x_1 \oplus x_2 \oplus x_3,\\
    y_2 = x_1 \oplus x_2 \oplus x_4,\\
    y_3 = x_1 \oplus x_3 \oplus x_4.
    \end{array} \right.

  * :math:`y_1` nesakrīt :math:`\Rightarrow` kļūda var būt tikai kādā no bitiem, 
    kas ietekmē :math:`y_1` (:math:`y_1, x_1, x_2, x_3`). 
  * :math:`y_2` sakrīt :math:`\Rightarrow` kļūda var būt tikai kādā no bitiem, 
    kas neietekmē :math:`y_2` (:math:`y_1, y_3, x_3`).
  * :math:`y_3` nesakrīt `\Rightarrow` kļūda var būt tikai kādā no bitiem, 
    kas ietekmē :math:`y_3` (:math:`x_1, x_3, x_4, y_3`).
  * Vienīgais bits, kas ir atzīmēts visās rindās ir :math:`x_3`. Tātad tas ir kļūdainais bits. 

  Sākotnējais ziņojums bija :math:`\mathtt{01}\textcolor{red}{\mathtt{0}}\mathtt{1101}` 
  (un :math:`x_1x_2x_3x_4 = \mathtt{0101}`).

  "X" :math:`i`-tajā rindiņā nozīmē, ka kontrolbits :math:`y_i` 
  pieļauj iespēju, ka attiecīgajā bitā ir kļūda.


  .. list-table:: 
     :header-rows: 1 

     * - :math:`x_1 = \mathtt{0}`
       - :math:`x_2 = \mathtt{1}`
       - :math:`x_3 = \mathtt{1}`
       - :math:`y_1 = \mathtt{1}`
       - :math:`x_4 = \mathtt{1}`
       - :math:`y_2 = \mathtt{0}`
       - :math:`y_3 = \mathtt{1}`
     * - X
       - X
       - X
       - X
       - 
       - 
       - 
     * - 
       - 
       - X
       - X
       - 
       - 
       - X
     * - X
       -
       - X
       - 
       - X
       - 
       - X
     * - :math:`\mathtt{0}`
       - :math:`\mathtt{1}`
       - :math:`\textcolor{red}{\mathtt{0}}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{0}`
       - :math:`\mathtt{1}`




**Piemērs #3**
  Izmantojot Heminga kodu :math:`[7,4,1]`, atkodēt virkni `1010010`.



**Piemērs #3**

  .. math::

    \left\{
    \begin{array}{l}
    y_1 = x_1 \oplus x_2 \oplus x_3,\\
    y_2 = x_1 \oplus x_2 \oplus x_4,\\
    y_3 = x_1 \oplus x_3 \oplus x_4.
    \end{array} \right.

  * :math:`y_1` sakrīt :math:`\Rightarrow` kļūda var būt tikai kādā no bitiem, kas neietekmē :math:`y_1` (:math:`y_2, y_3, x_4`). 
  * :math:`y_2` sakrīt :math:`\Rightarrow` kļūda var būt tikai kādā no bitiem, kas neietekmē :math:`y_2` (:math:`y_1, y_3, x_3`).
  * :math:`y_3` sakrīt :math:`\Rightarrow` kļūda var būt tikai kādā no bitiem, kas neietekmē :math:`y_3` (:math:`y_1, y_2, x_2`).
  * Nav neviena bita, kas ir atzīmēts visās rindās. Kļūdainu bitu nav.

  Sākotnējais ziņojums bija :math:`\mathtt{1010010}` 
  (un :math:`x_1x_2x_3x_4 = \mathtt{1010}`).

  "X" :math:`i`-tajā rindiņā nozīmē, ka kontrolbits `y_i` 
  pieļauj iespēju, ka attiecīgajā bitā ir kļūda.


  .. list-table:: 
     :header-rows: 1 

     * - :math:`x_1 = \mathtt{1}`
       - :math:`x_2 = \mathtt{0}`
       - :math:`x_3 = \mathtt{1}`
       - :math:`y_1 = \mathtt{0}`
       - :math:`x_4 = \mathtt{0}`
       - :math:`y_2 = \mathtt{1}`
       - :math:`y_3 = \mathtt{0}`
     * - 
       - 
       - 
       - 
       - X
       - X
       - X
     * - 
       - 
       - X
       - X
       - 
       - 
       - X
     * - 
       - X
       - 
       - X
       - 
       - X
       - 
     * - :math:`\mathtt{1}`
       - :math:`\mathtt{0}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{0}`
       - :math:`\mathtt{0}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{0}`



**Piemērs #4**
  Izmantojot Heminga kodu :math:`[7,4,1]`, atkodēt saņemto virkni `1101110`.


**Atrisinājums**

  .. math::

    \left\{
    \begin{array}{l}
    y_1 = x_1 \oplus x_2 \oplus x_3,\\
    y_2 = x_1 \oplus x_2 \oplus x_4,\\
    y_3 = x_1 \oplus x_3 \oplus x_4.
    \end{array} \right.

  * :math:`y_1` nesakrīt :math:`\Rightarrow` kļūda ir kādā no bitiem, kas ietekmē :math:`y_1` (:math:`y_1, x_1, x_2, x_3`). 
  * :math:`y_2` sakrīt :math:`\Rightarrow` kļūda ir kādā no bitiem, kas neietekmē :math:`y_2` (:math:`y_1, y_3, x_3`).
  * :math:`y_3` sakrīt :math:`\Rightarrow` kļūda ir kādā no bitiem, kas neietekmē :math:`y_3` (:math:`x_2, y_1, y_2`).
  * Vienīgas bits, kas ir atzīmēts visās rindās ir `y_1`. Tātad tas ir kļūdainais bits. 

  Tāpēc nosūtītais ziņojums bija :math:`\mathtt{110}\textcolor{red}{\mathtt{0}}\mathtt{110}`
  (un :math:`x_1x_2x_3x_4 = \mathtt{1101}`).

  "X" :math:`i`-tajā tabulas rindiņā nozīmē, ka kontrolbits :math:`y_i` 
  pieļauj iespēju, ka attiecīgajā bitā ir kļūda.

  .. list-table:: 
     :header-rows: 1 

     * - :math:`x_1 = \mathtt{1}`
       - :math:`x_2 = \mathtt{1}`
       - :math:`x_3 = \mathtt{0}`
       - :math:`y_1 = \mathtt{1}`
       - :math:`x_4 = \mathtt{1}`
       - :math:`y_2 = \mathtt{1}`
       - :math:`y_3 = \mathtt{0}`
     * - X
       - X
       - X
       - X
       - 
       - 
       - 
     * - 
       - 
       - X
       - X
       - 
       - 
       - X
     * - 
       - X
       - 
       - X
       - 
       - X
       - 
     * - :math:`\mathtt{1}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{0}`
       - :math:`\textcolor{red}{\mathtt{0}}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{1}`
       - :math:`\mathtt{0}`

