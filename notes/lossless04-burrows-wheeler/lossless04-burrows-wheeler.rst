4. Berouza-Vīlera transformācija
=======================================================

Berouza-Vīlera transformācijas (BWT) ideja: Ievades tekstā samaina burtu secību tā, 
ka tie burti, kuri atrodas tūlīt aiz (vai arī - tieši pirms) 
līdzīgiem kontekstiem, nonāk blakus.

Citiem vārdiem - teksta burtus ar īpašu pārveidojumu pārkārto tā, 
ka pārkārtojumā atspoguļojas teksta "iekšējās simetrijas"; nereti 
blakus nonāk atkārtoti burti.  


Kodēšana ar pārvietošanu uz priekšu
--------------------------------------

Pirms BWT aplūkojam citu kodējumu, ko sauc par *Move-to-front*. 
To bieži lieto tūlīt pēc Berouza-Vīlera transformācijas, 
bet to var izmantot arī neatkarīgi -- 
jebkuras ziņojumu virknes iekodēšanai.  

Ja ievadē ir teksts, kurā mēdz bieži nonākt blakus vienādi burti
(vai arī burti no nelielas kopas, kas mazāka par pilno alfabētu). 
to var efektīvi saspiest, ar *Move-to-front* kodējumu:

1. Alfabēta burtus sakārto sarakstā, kura pozīcijas numurē, sākot ar :math:`0`.
2. Katru burtu kodē ar tā pozīciju šajā sarakstā, tad pārvieto šo 
   burtu uz saraksta pašu sākumu. 

Vajadzīga datu struktūra -- saraksts :math:`L`, kas ļauj atrast burta kārtas 
numuru sarakstā :math:`L.\text{\sc index}(c)`, ļauj izmest 
elementu dotajā pozīcijā :math:`L.\text{\sc delete}(\text{\it pos})`
un ļauj iespraust izmesto elementu saraksta sākumā 
:math:`L.\text{\sc insert}(\text{\it pos},c)`. 
Biežāk lietotie burti atradīsies saraksta priekšā, 
izejā būs galvenokārt mazi skaitļi. 
(Ja ievadē biežāk lietotie burti lēnām mainās, attiecīgi adaptējas arī 
saraksts.)


**Piemērs:** 
  Ar :math:`\text{\sc MoveToFrontEncode()}` iekodēt šādu virkni: 
  :math:`\mathtt{abaccab}` alfabētā :math:`S=\{ \mathtt{a}, \mathtt{b}, \mathtt{c} \}`. 

  Tabulā attēlojam katra ievades burta apstrādi - katra soļa beigās 
  izvadei pievieno jaunu skaitli. Alfabēta permutācija parādīta
  *pirms* attiecīgā ievades burta apstrādes. Pēc kārtējā burta 
  apstrādes alfabētu pārkārto, pārvietojot iekodēto burtu uz pašu sākumu.

  =======================  ====================  ====================  
  Ievade                   Izvade                Alfabēts pirms soļa
  =======================  ====================  ====================
  **a**,b,a,c,c,a,b        0                     ``[a,b,c]``
  a,**b**,a,c,c,a,b        0,1                   ``[a,b,c]``
  a,b,**a**,c,c,a,b        0,1,1                 ``[b,a,c]``
  a,b,a,**c**,c,a,b        0,1,1,2               ``[a,b,c]``
  a,b,a,c,**c**,a,b        0,1,1,2,0             ``[c,a,b]``
  a,b,a,c,c,**a**,b        0,1,1,2,0,1           ``[c,a,b]``
  a,b,a,c,c,a,**b**        0,1,1,2,0,1,2         ``[a,c,b]``
                                                 ``[b,a,c]``
  =======================  ====================  ====================

**Piemērs:** 
  Ar :math:`\text{\sc MoveToFrontEncode()}` iekodēt šādu virkni: 
  :math:`\mathtt{abababca}` alfabētā :math:`S=\{ \mathtt{a}, \mathtt{b}, \mathtt{c} \}`. 

  ============================  ====================  ====================  
  Ievade                        Izvade                Alfabēts pirms soļa
  ============================  ====================  ====================
  **a**, b, a, b, a, b, c, a    0                     ``[a,b,c]``
  a, **b**, a, b, a, b, c, a    0,1                   ``[a,b,c]``
  a, b, **a**, b, a, b, c, a    0,1,1                 ``[b,a,c]``
  a, b, a, **b**, a, b, c, a    0,1,1,1               ``[a,b,c]``
  a, b, a, b, **a** ,b, c, a    0,1,1,1,1             ``[b,a,c]``
  a, b, a, b, a, **b**, c, a    0,1,1,1,1,1           ``[a,b,c]``
  a, b, a, b, a, b, **c**, a    0,1,1,1,1,1,2         ``[b,a,c]``
  a, b, a, b, a, b, c, **a**    0,1,1,1,1,1,2,2       ``[c,b,a]``
  &nbsp;                        &nbsp;                ``[a,c,b]``
  ============================  ====================  ====================


**Piemērs:**
  Atkodēt :math:`\mathtt{010010}` alfabētā :math:`S=\{ \mathtt{a}, \mathtt{b} \}`

  =======================  ====================  ====================  
  Ievade                   Izvade                Alfabēts pirms soļa
  =======================  ====================  ====================
  **0**,1,0,0,1,0          a                     ``[a,b]``
  0,**1**,0,0,1,0          a,b                   ``[a,b]``
  0,1,**0**,0,1,0          a,b,b                 ``[b,a]``
  0,1,0,**0**,1,0          a,b,b,b               ``[b,a]``
  0,1,0,0,**1**,0          0,b,b,b,a             ``[b,a]``
  0,1,0,0,1,**0**          a,b,b,b,a,a           ``[a,b]``
                                                 ``[a,b]``
  =======================  ====================  ====================




Berouza-Vīlera transformācija
-------------------------------

**Definīcija:** 
  Par :math:`n` elementu saraksta *permutāciju* (*permutation*) sauc jebkuru
  citu sarakstu, kurā izmainīta šo elementu secība.
  Par *ciklisku permutāciju* sauc tādu permutāciju, kurā elementiem saglabājas 
  abi kaimiņi -- t.i. vienu vai vairākus 
  elementus no saraksta beigām pārliek uz saraksta sākumu, nemainot 
  pārvietoto elementu savstarpējo secību.

Ja visi burti ir atšķirami, tad :math:`n` elementu sarakstam 
ir ir :math:`n!` permutāciju (bet tikai :math:`n` cikliskas permutācijas). 

**Piemērs:** 
  Izrakstīt visas cikliskās permutācijas vārdiem :math:`\mathtt{BONBON\$}`, 
  un :math:`\mathtt{BANANA\$}`, tad sakārtot tās alfabētiski.

  .. code-block:: text

    B O N B O N $              $ B O N B O N
    $ B O N B O N              B O N $ B O N
    N $ B O N B O              B O N B O N $
    O N $ B O N B     --->     N $ B O N B O  
    B O N $ B O N              N B O N $ B O
    N B O N $ B O              O N $ B O N B 
    O N B O N $ B              O N B O N $ B 


  .. code-block:: 

    B A N A N A $              $ B A N A N A
    $ B A N A N A              A $ B A N A N
    A $ B A N A N              A N A $ B A N
    N A $ B A N A     --->     A N A N A $ B
    A N A $ B A N              B A N A N A $
    N A N A $ B A              N A $ B A N A
    A N A N A $ B              N A N A $ B A

  Berouza-Vīlera transformācija ir šajā sakārtojumā iegūtā pēdējā kolonna -- 
  :math:`BWT(\mathtt{BONBON\$}) = \mathtt{NN\$OOBB}` un 
  :math:`BWT(\mathtt{BANANA\$}) = \mathtt{ANNB\$AA}`. 
  

**Definīcija:** 
  Par alfabēta burta :math:`x \in S` *labo kontekstu* 
  dotajā tekstā :math:`T` sauc jebkuru stringu fiksētā garumā :math:`k`, 
  kas tieši seko aiz šī burta :math:`x` (ja burts :math:`x` ir tuvu vārda beigām, tad 
  kontekstu iegūst cikliski pārvietojoties uz teksta sākumu). 

Berouza-Vīlera transformācija sakārto visus labos kontekstus leksikogrāfiski 
un izraksta teksta burtus secībā, kuru nosaka šie labie konteksti. 

.. figure:: figs/burrows-wheeler-fragment.png
   :width: 5in


.. note:: 
  Varētu kārtot arī inversi leksikogrāfiski (t.i. alfabētiski, bet skatoties 
  vārdam no otra gala). Šādā gadījumā pirmā kolonna kļūtu par Berouza-Vīlera 
  transformāciju. T.i. var izmantot arī sakārtošanu pēc "kreisajiem kontekstiem". 
  Šādi to apraksta Guy Blelloch *Introduction to Data Compression* grāmatā.




Apgrieztā Berouza-Vīlera transformācija
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No Berouza-Vīlera transformācijas (pēdējās kolonnas) var izsecināt, kāda 
būs pirmā kolonna (tie paši burti, bet alfabētiskā secībā). 
Var pamatot, ka vienādo burtu secība Berouza-Vīlera transformācijas rezultātā 
nemainās. Tāpēc pietiek zināt šīs divas kolonnas un izmantot L2F (Last-to-First)
kodējuma tabulu.



Ir arī iespējams atjaunot visu matricu: 

.. figure:: figs/burrows-decode.png
   :width: 7in

   Decode

**Algoritma apraksts**

1. Ciklā katru kolonnu pabīda vienu soli pa labi un 
   tad pārkārto. Permutāciju nosaka pēdējā kolonna matricā. 
2. Šādi, ja mēs varam atrast kolonnu :math:`j`, varam iegūt
   kolonnu :math:`j+1` no kolonnas :math:`j`. Šo atkārtojot, varam 
   atjaunot visu matricu :math:`M`.
3. Lai rekonstruētu sākotnējo tekstu :math:`T`, mums pietiek atrast tikai vienu 
   rindiņu matricā.

.. note::
  Sk. 177 lapu no `<https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf>`_




Efektīva BWT ar sufiksu kokiem 
-------------------------------

**Apgalvojums:** 
  BWT naivā implementācija prasa laiku :math:`O(n^2 \log n)`. 

**Pierādījums:** 
  Ciklisko permutāciju izrakstīšana prasa aizpildīt :math:`n \times n`
  matricu ar burtiem; tas prasa :math:`n^2` laiku. 

Praksē garus tekstus saspiež veicot Berouza-Vīlera transformāciju 
atsevišķiem blokiem. Tipisks bloku garums ir daži simti kilobaitu. 
Blokiem nav labi būt pārāk gariem, lai tos būtu praktiski apstrādāt.  
Tiem nevajadzētu arī būt pārāk īsiem, lai atrastu un optimāli 
izmantotu atkārtotos kontekstus.

Berouza-Vīlera transformāciju var veikt lineārā laikā no vārda garuma
:math:`O(n)`, izmantojot  
*sufiksu masīvus* (*suffix arrays*). 







Uzdevumi
------------

**4.1. uzdevums**
  Ierakstīt Berouza-Vīlera transformāciju vārdam :math:`\textcolor{blue}{\mathtt{ABBA\$}}`. 
  Aiz tās norādīt, kurā vietā šajā transformācijā ir strings :math:`\textcolor{blue}{\mathtt{ABBA\$}}`.   
  *Piezīme.* Sakārtotajā matricā virkņu numerācija sākas no :math:`1`.

.. only:: Internal 

  **Atbilde:** 

    Iegūst cikliskas `ABBA$` permutācijas, sakārto leksikogrāfiski:

    .. math::

      \left( \begin{array}{ccccc}
      \text{A} & B & B & A & \$ \\
      \$ & A & B & B & A \\
      A & \$ & A & B & B \\
      B & A & \$ & A & B \\
      B & B & A & \$ & A
      \end{array} \right) \rightarrow
      \left( \begin{array}{ccccc}
      \text{\$} & A & B & B & A \\
      A & \$ & A & B & B \\
      A & B & B & A & \$ \\
      B & A & \$ & A & B \\
      B & B & A & \$ & A
      \end{array} \right).

    Transformācijas rezultāts ir labējā kolonna: *AB$BA*.
    Sākotnējā virkne ir 3.rindiņa.

  :math:`\square`


**4.2. uzdevums**
  Iepriekšējā jautājumā iegūtajai `ABBA$` Berouza-Vīlera transformācijas 
  virknei uzrakstīt **Move-to-Front** kodu, ja
  sākotnējā burtu secība alfabētā ir 
  :math:`\textcolor{blue}{\mathtt{\$}} < \textcolor{blue}{\mathtt{A}} < \textcolor{blue}{\mathtt{B}}`.  
  *Piezīme.* **Move-to-Front** algoritmos alfabēta numerācija sākas no :math:`0`.

  * Uzrakstīt virkni, kas iegūta ar Berouza-Vīlera transformāciju.   
  * Uzrakstīt šīs virknes move-to-front kodu. 

.. only:: Internal 

  **Atbilde:** 

    Katrā **Move-to-Front** kodēšanas solī pārliekam
    tekošo simbolu uz alfabēta sākumu. 

    =================  ==================  ==================
    Virkne             Kods                Alfabēts
    =================  ==================  ==================
    `*A*B$BA`            1                   ($,A,B)
    `A*B*$BA`            2                   (A,$,B)
    `AB*$*BA`            2                   (B,A,$)
    `AB$*B*A`            2                   ($,B,A)
    `AB$B*A*`            2                   (B,$,A)
    =================  ==================  ==================

    Iegūtais kods ir `12222`.

  :math:`\square`


Izmantotā literatūra 
-----------------------

* `https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf <https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf>`_
* `https://docs.python.org/3/library/bz2.html <https://docs.python.org/3/library/bz2.html>`_
* `https://serverfault.com/questions/2600/how-do-you-set-bzip2-block-size-when-using-tar <https://serverfault.com/questions/2600/how-do-you-set-bzip2-block-size-when-using-tar>`_
