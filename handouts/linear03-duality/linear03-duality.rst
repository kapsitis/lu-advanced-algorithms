15. Lineārā programmēšana un dualitāte
===============================================

Simpleksa algoritms praksē strādā labi, bet tam ir vairākas problēmas: 

  * Tam ir dažādi varianti -- pirmā stūra izvēle, pārejas izvēle (dažreiz randomizācija), 
  * Tas var nestrādāt polinomiālā laikā, ja izveido īpašus piemērus. 
    Polinomiāla laika algoritms ir industrijas standarts visam, ko izmanto praksē. 





Duālais uzdevums standartformas LP
----------------------------------------------

Aprakstām vispirms standarta gadījumu, kur visas nevienādības sistēmā ir :math:`\leq`, 
bet visi mainīgie :math:`x_i` -- nenegatīvi skaitļi.

  **Primārā LP:** 
    Jeb *Primal LP* apzīmēta ar :math:`P`. 
    Atrast :math:`\min \mathbf{c}^T \cdot \mathbf{x}`,
    kur :math:`A \mathbf{x} \leq \mathbf{b}`, :math:`\mathbf{x} \geq 0`.

  **Duālā LP:** 
    Jeb *Dual LP* apzīmēta ar :math:`D`. 
    Atrast :math:`\max \mathbf{b}^T \cdot \mathbf{y}`,
    kur :math:`A^T \mathbf{y} \leq \mathbf{c}`.


**Piemērs:**

  **Primārais LP uzdevums (:math:`P`):**  
    *Maksimizēt* :math:`5x_1 + 7x_2 + 6x_3` pie nosacījumiem

    .. math::

        \left\{ \begin{array}{l}
        6x_1 + 5x_2 + 8x_3 \leq 16,\\
        10x_1 + 20x_2 + 10x_3 \leq 35,\\
        x_1 \geq 0,\;\; x_2 \geq 0,\;\; x_3 \geq 0,\\
        \end{array} \right.

  **Duālais LP uzdevums (:math:`D`):**  
    *Minimizēt* :math:`16y_1+ 35y_2` pie nosacījumiem:

    .. math::

        \left\{ \begin{array}{l}
        6y_1 + 10y_2 \geq 5,\\
        5y_1 + 20y_2 \geq 7,\\
        8y_1 + 10y_2 \geq 6,\\
        y_1 \geq 0,\;\; y_2 \geq 0.
        \end{array} \right.

  .. figure:: figs/dual-charts.png
     :width: 5in

     Duālās problēmas atrisinājums. 


**Duālā uzdevuma nozīme**

  Duālo uzdevumu var interpretēt šādi: katrs tā atrisinājums 
  dod novērtējumu no augšas primārās programmas atrisinājumam. 
  Piemēram, ja ir duālās programmas atrisinājums :math:`y_1 = 0.5` un :math:`y_2 = 0.2`, 
  tad no duālās programmas nosacījumiem seko: 
   
  .. math:: 
    
    5x_1 + 7x_2 + 6x_3 \leq  0.5(6x_1 + 5x_2 + 8x_3) + 0.2(10x_1 + 20x_2 + 10x_3).
  
  Var pārliecināties, ka ikvienam koeficientam (pie :math:`x_1,x_2,x_3`) izpildās 
  nevienādības: :math:`0.5 \cdot 6 + 0.2 \cot 10 = y_1 \cdot 6 + y_2 \cdot 10 \geq 5` utt., 
  jo :math:`(y_1,y_2)` ir derīgs punkts duālajai programmai. 

  Apvienojot ar primārās programmas nosacījumiem:

  .. math:: 
    
    5x_1 + 7x_2 + 6x_3  \leq  0.5 \cdot 16 + 0.2 \cdot 35 = 15.
   
   
  Primārās LP mērķfunkcija jebkurā punktā :math:`(x_1,x_2,x_3)` ir mazāka 
  par duālās programmas mērķfunkciju. 
   



Duālais uzdevums vispārīgās formas LP
----------------------------------------

**Primārā lineārā programma:**
  Definēsim lineāru programmu :math:`P` (ko sauksim par *primāro LP*):

  Izvēlamies *minimizēt* :math:`c_1 x_1 + c_2 x_2 + \ldots + c_n x_n` pie šādiem nosacījumiem:
  
  .. math::

    \left\{ \begin{array}{l}
    a_{11} x_1 + a_{12} x_2 + \ldots + a_{1n} x_n  \;\;\textcolor{red}{?}\;\; b_1,\\
    \ldots\\
    a_{k1} x_1 + a_{k2} x_2 + \ldots + a_{kn} x_n \;\;\textcolor{red}{?}\;\; b_k,\\
    x_1 \geq 0,\; x_2 \geq 0,\;\ldots \\
    \end{array} \right.

  LP var nebūt standartformā: 

  * Nosacījumiem :math:`a_{i1} x_1 + a_{i2} x_2 + \ldots + a_{in} x_n \;\;\textcolor{red}{?}\;\; b_i`,
    jautājuma zīmes vietā var būt jebkura zīme (:math:`\geq`, :math:`\leq`, :math:`=`). 
  * Attiecībā uz mainīgajiem :math:`x_i` var būt nosacījumi :math:`x_i \geq 0`, :math:`x_i \leq 0`, 
    vai vispār nebūt nosacījuma attiecībā uz :math:`x_i`.

**Definīcija:** 
  Vektoru :math:`\mathbf{x}` sauc par *iespējamu* (*feasible*)
  (arī (neoptimālu) LP uzdevuma *risinājumu*),
  ja tas apmierina visus ierobežojumus (vienādības, nevienādības). 

**Definīcija:** 
  LP uzdevumu sauc par *iespējamu* (*feasible*),
  ja tam ir iespējams risinājums :math:`\mathbf{x}`.

**Definīcija:** 
  LP uzdevums ir *neiespējams* (*infeasible*),
  ja tam šāds :math:`\mathbf{x}` neeksistē. 

**Definīcija:** 
  LP minimuma uzdevums
  (:math:`\min\{ \mathbf{c}^T \mathbf{x}\;:\;A\mathbf{x}=\mathbf{b},\mathbf{x}\geq\mathbf{0}\}`)
  ir *neierobežots* (*unbounded*), ja katram :math:`\lambda \in \mathbb{R}`
  eksistē :math:`\mathbf{x} \in \mathbb{R}^n`,
  ka visi LP ierobežojumi izpildās un :math:`\mathbf{c}^T \mathbf{x} \leq \lambda`.



Lineāru programmu var pārveidot, ieviešot *nokares mainīgos* (*slack variables*). 
Šajā gadījumā visas nevienādības var pārrakstīt par vienādībām, papildus prasot, 
lai mainīgie (ieskaitot nokares mainīgos) būtu nenegatīvi skaitļi. 

  .. math::

    \begin{array}{ccc}
    \max\{ \mathbf{c}^T \mathbf{x}\} & \rightarrow  & \min\{ -\mathbf{c}^T \mathbf{x}\}\\
    \mathbf{a}_i^T \mathbf{x} = b_i & \rightarrow  &  (\mathbf{a}_i^T \mathbf{x} \leq b_i) 
    \wedge (\mathbf{a}_i^T \mathbf{x} \geq b_i)  \\
    \mathbf{a}_i^T \mathbf{x} \leq b_i & \rightarrow  &  (\mathbf{a}_i^T \mathbf{x} + s_i = b_i) 
    \wedge (s_i \geq 0)  \\
    \end{array} 






**Definīcija:**
   Par *duālo programmu* sauc tādu lineāro programmu, kur jāminimizē izteiksme:
   :math:`b_1 y_1 + b_2 y_2 + \ldots + b_k y_k`,
   pie nosacījumiem
   :math: `a_{11} y_1 + a_{21} y_2 + \ldots + a_{k1} y_k \;\;? \;\; c_k`,
   kur simbols jautājuma zīmes vietā tiek noteikts šādi:

   * Ja primārajā LP bija nosacījums :math:`x_i \geq 0`, tad jautājuma zīmes vietā ir :math:`\geq`.
   * Ja primārajā LP bija nosacījums :math:`x_i \leq 0`, tad jautājuma zīmes vietā ir :math:`\leq`.
   * Ja primārajā LP nebija nosacījuma attiecībā uz :math:`x_i`, tad jautājuma zīmes vietā ir :math:`=`.

   Attiecībā uz mainīgajiem :math:`y_1, y_2, \ldots, y_k`, nosacījumi ir atkarīgi no tā, 
   kāda zīme bija primārās LP nosacījumā :math:`a_{i1} x_1 + a_{i2} x_2 + \ldots + a_{in} x_n \;\;? \;\; b_i`:

   * Ja :math:`?` vietā bija :math:`\geq`, tad mums tagad ir nosacījums :math:`y_i \leq 0`.
   * Ja :math:`?` vietā bija :math:`\leq`, tad mums tagad ir nosacījums :math:`y_i \geq 0`.
   * Ja :math:`?` vietā bija :math:`=`, tad mums tagad nav nosacījuma attiecībā uz :math:`y_i`.


**Piemērs**
  *Maksimizēt:* :math:`\textcolor{blue}{4x_1 + 2x_2 - x_3}`, kur 

  .. math::

     \left\{
     \begin{array}{l}
     x_1 + x_2 + x_3 = 20\\
     2x_1 - x_2 \geq 6\\
     3x_1 + 2x_2 + x_3 \leq 40\\
     x_1,x_2 \geq 0
     \end{array} \right.

  **Matricu pieraksts**
    *Maksimizēt skalāro reizinājumu:* :math:`(4, 2, -1) \cdot (x_1,x_2,x_3)`, kur 

    .. math::

      A = \left(
      \begin{array}{ccc}
      1 & 1 & 1\\
      2 & -1 & 0\\
      3 & 2 & 1
      \end{array} \right) \left(
      \begin{array}{c}
      x_1\\
      x_2\\
      x_3 \end{array} \right) 
      \begin{array}{c}
      =\\
      \geq \\
      \leq
      \end{array}
      \left(
      \begin{array}{c}
      20\\
      6 \\
      40
      \end{array} \right).

    un 

    .. math::
    
      x_1 \geq 0,\;\;x_2 \geq 0,\;\;x_3\;\text{bez nosac.}


**Piemērs:**
  *Maksimizēt skalāro reizinājumu:* :math:`(4, 2, -1) \cdot (x_1,x_2,x_3)`, kur 

  .. math::

      \left(
      \begin{array}{ccc}
      1 & 1 & 1\\
      2 & -1 & 0\\
      3 & 2 & 1
      \end{array} \right) \left(
      \begin{array}{c}
      x_1\\
      x_2\\
      x_3 \end{array} \right) 
      \begin{array}{c}
      =^{\textcolor{blue}{(a)}}\\
      \geq^{\textcolor{blue}{(b)}} \\
      \leq^{\textcolor{blue}{(c)}}
      \end{array}
      \left(
      \begin{array}{c}
      20\\
      6 \\
      40
      \end{array} \right).

    un :math:`x_1 \geq^{\textcolor{blue}{(d)}} 0`, :math:`x_2 \geq^{\textcolor{blue}{(e)}} 0`, 
    :math:`x_3\;\text{bez nosac.}^{\textcolor{blue}{(f)}}`

**Duālais LP uzdevums:**  
  *Minimizēt skalāro reizinājumu:* :math:`(20,6,-40) \cdot \left( y_1, y_2, y_3 \right)`, kur 

  .. math::

      \left(
      \begin{array}{ccc}
      1 & 2 & 3\\
      1 & -1 & 2\\
      1 & 0 & 1
      \end{array} \right) \left(
      \begin{array}{c}
      y_1\\
      y_2\\
      y_3 \end{array} \right) 
      \begin{array}{c}
      \geq^{\textcolor{blue}{(d)}}\\
      \geq^{\textcolor{blue}{(e)}} \\
      =^{\textcolor{blue}{(f)}}
      \end{array}
      \left(
      \begin{array}{c}
      4\\
      2 \\
      -1
      \end{array} \right).

  un  :math:`y_1\;\text{bez nosac.}^{\textcolor{blue}{(a)}}`, 
  :math:`y_2 \leq^{\textcolor{blue}{(b)}} 0`, 
  :math:`y_3 \geq^{\textcolor{blue}{(c)}} 0.`

  * Koeficientus iegūst, transponējot :math:`A`. 
  * Vienādību un nevienādību tipus nosaka atbilstoši 
    augšminētajiem noteikumiem: Piemēram, ja :math:`x_1 \geq 0` primārajā 
    problēmā, tad :math:`x_1` mainīgajam atbilstošais duālais vienādojums 
    :math:`y_1 + 2y_2 + 3y_3 \geq 4`.


**Primārās un duālās LP apvienošana**

Ja dotas primārā LP un duālā LP, varam uzrakstīt jaunu LP, 
kas satur visus mainīgos (gan :math:`x_1, x_2, \ldots, x_n`, 
gan :math:`y_1, y_2, \ldots, y_k`), 
gan visus nosacījumus no abām programmām un pievienot tai vēl vienu nosacījumu:

.. math:: c_1 x_1 + c_2 x_2 + \ldots + c_n x_n = b_1 y_1 + b_2 y_2 + \ldots + b_k y_k.

Tad vienīgais gadījums, kad izpildās visi nosacījumi ir, ja 
:math:`x_1, x_2, \ldots, x_n` sasniedz primārās LP maksimums, bet 
:math:`y_1, y_2, \ldots, y_k` sasniedz duālās LP minimumu.

**Secinājums:** 
  Ja mums ir algoritms, kas prot patvaļīgai LP atrast 
  vienu punktu, kas apmierina visus nosacījumus, tad šo algoritmu 
  var izmantot arī maksimuma atrašanai.




Vājās dualitātes teorēma
-------------------------



**Farkaša lemma**
  Ja :math:`A` ir :math:`m \times n` matrica,
  tad izpildās tieši viens no apgalvojumiem:  
  **(1)** :math:`\exists\mathbf{x} \in \mathbb{R}^n\;:\;A\mathbf{x}=\mathbf{b}`, kur :math:`\mathbf{x} \geq \mathbf{0}`,
  **(2)** :math:`\exists\mathbf{y} \in \mathbb{R}^m\;:\;A^T \mathbf{y} \geq \mathbf{0}`, kur :math:`\mathbf{b}^T \mathbf{y} < 0`. 

  Atsevišķs gadījums ir lineārajā algebrā,
  kur vai nu :math:`A\mathbf{x} = \mathbf{b}` eksistē atrisinājums,
  vai arī sistēmai :math:`A^T \mathbf{y} = 0`
  (kur :math:`\mathbf{b}^T \mathbf{y} \neq 0`) eksistē atrisinājums.


**Pierādījums:**
  Abi nosacījumi nevar vienlaicīgi izpildīties, jo šādu :math:`\mathbf{x}` un :math:`\mathbf{y}` pastāvēšana nozīmētu 

  .. math::

    \begin{array}{l}
    \mathbf{y}^T A \mathbf{x} = \mathbf{y}^T (A \mathbf{x}) = \mathbf{y} \mathbf{b} < 0 \\
    \mathbf{y}^T A \mathbf{x} = (A^T \mathbf{y})^T \mathbf{x} \geq 0 \\
    \end{array}

  jo divu nenegatīvu vektoru skalārais reizinājums ir nenegatīvs.  




**Vājās dualitātes teorēma**
  Primārā :math:`P`: :math:`\min \mathbf{c}^T \cdot \mathbf{x}`,  
  kur :math:`A\mathbf{x} = \mathbf{b}`, :math:`\mathbf{x} \geq 0`. 

  Duālā :math:`D`: :math:`\max \mathbf{b}^T \cdot \mathbf{y}`,  
  kur :math:`A^T\mathbf{y} \leq \mathbf{c}`. 


**Teorēma:** 
  Zināms, ka :math:`P` atrisinājums ir 
  :math:`\mathbf{x} = \mathbf{x}_{\text{opt}}` un 
  :math:`D` atrisinājums ir :math:`\mathbf{y} = \mathbf{y}_{\text{opt}}`. 
  Apzīmējam optimālās vērtības ar 
  :math:`z_{\text{opt}} = \mathbf{c}^T \cdot \mathbf{x}_{\text{opt}}`
  un :math:`w_{\text{opt}} = \mathbf{b}^T \cdot \mathbf{y}_{\text{opt}}`. 

  Tad :math:`z_{\text{opt}} \geq w_{\text{opt}}`. 



**Pretrunīgi/neierobežoti nosacījumi**
  Vājās dualitātes teorēma spēkā pat tad, ja primārā :math:`P` vai 
  duālā :math:`D` ir pretrunīgas vai neierobežotas. Apzīmējam:

  * Ja primārais/minimuma uzdevums :math:`P` ir pretrunīgs, tad optimums :math:`z_{\text{opt}} = +\infty`.
  * Ja primārais/minimuma uzdevums :math:`P` ir neierobežots, tad optimums :math:`z_{\text{opt}} = -\infty`.
  * Ja duālais/maksimuma uzdevums :math:`D` ir pretrunīgs, tad optimums :math:`w_{\text{opt}} = -\infty`.
  * Ja duālais/maksimuma uzdevums :math:`D` ir neierobežots, tad optimums :math:`w_{\text{opt}} = +\infty`.

**Vājās dualitātes teorēmas pierādījums**
  Duālā LP veidota tā, lai vājā dualitāte būtu spēkā.  
  Iedomāsimies, ka ir kaut kāds vektors :math:`\mathbf{y}`, kam :math:`A^T\mathbf{y} \leq \mathbf{c}`. 
  Pārrakstām:

  .. math::

    \mathbf{y}^T \mathbf{b} = \mathbf{y}^T A \mathbf{x} \leq \mathbf{c}^T \mathbf{x},

  kur :math:`\mathbf{x}` ir jebkurš (arī neoptimāls) risinājums, kas apmierina :math:`P` nosacījumus. 
  Tādēļ :math:`\mathbf{y}^T \mathbf{b}` ir apakšējais novērtējums optimālajam risinājumam. 
  Tas ir spēkā visiem :math:`\mathbf{y}`, kas apmierina :math:`A^T \mathbf{y} \leq \mathbf{c}`, 
  tādēļ vislabāko apakšējo novērtējumu iegūsim, maksimizējot 
  :math:`\mathbf{y}^T \mathbf{b}`  pie nosacījuma :math:`A^T \mathbf{y} \leq \mathbf{c}`.
  :math:`\blacksquare`




Stiprās dualitātes teorēma
-----------------------------

**Duālais uzdevums, tikai nevienādības**

  **Primārais LP uzdevums:**  
    Maksimizēt skalāro reizinājumu :math:`z = \mathbf{c} \cdot \mathbf{x}`, kur 

    .. math::

      \left\{ 
      \begin{array}{l}
      A\mathbf{x} \leq \mathbf{b}\\
      \mathbf{x} \geq \mathbf{0} 
      \end{array} 
      \right.

  **Duālais LP uzdevums:**  
    Minimizēt skalāro reizinājumu :math:`Z = \mathbf{y} \cdot \mathbf{b}`, kur

    .. math::

      \left\{ 
      \begin{array}{l}
      A^{T}\mathbf{y} \geq \mathbf{c}\\
      \mathbf{y} \geq \mathbf{0} 
      \end{array} 
      \right.

**Dualitātes teorēma:** 

  **(1)** 
    Ja :math:`\mathbf{x}^{\ast}` ir pieļaujams vektors primārajai problēmai 
    (apmierina nevienādības :math:`A\mathbf{x}^{\ast} \leq \mathbf{b}` un 
    :math:`\mathbf{x}^{\ast} \geq \mathbf{0}`),  

  **(2)** 
    Un ja :math:`\mathbf{y}^{\ast}` ir 
    pieļaujams risinājums duālajai problēmai 
    (apmierina nevienādības 
    :math:`A^{T}\mathbf{y} \geq \mathbf{c}` un :math:`\mathbf{y} \geq \mathbf{0}`),  
    TAD  
    :math:`\mathbf{c}\cdot \mathbf{x}^{\ast} \leq \mathbf{b} \cdot \mathbf{y}^{\ast}`.


  Ja turklāt :math:`\mathbf{x}^{\ast}` un :math:`\mathbf{y}^{\ast}` ir optimālie 
  atrisinājumi attiecīgi primārajai un duālajai lineārajām programmām, tad 

  .. math::

    \mathbf{c}\cdot \mathbf{x}^{\ast} = \mathbf{b} \cdot \mathbf{y}^{\ast}

**Definīcija:** 
  Atšķirību :math:`\mathbf{b} \cdot \mathbf{y}^{\ast} - \mathbf{c} \cdot \mathbf{x}^{\ast}`
  sauc par *dualitātes atstarpi* (*duality gap*). Šīs atstarpes lielums palīdz noteikt, cik tālu 
  pašreizējais atrisinājums (neoptimāls, bet pieļaujams vektors :math:`\mathbf{x}` 
  vai attiecīgi :math:`\mathbf{y}`) ir no optimālā.







Sākumtuvinājuma izvēle
------------------------

Aprakstām mākslīgu mainīgo pievienošanas dažādus gadījumus. 

**Gadījums Nr.1:** 
  Dots LP uzdevums šādā formā:

  .. math::

    A\mathbf{x} \textcolor{red}{\leq} \mathbf{b},\;\;\mathbf{x} \geq 0,\;\; \mathbf{b} \geq 0.

  Var pievinināt *nokares mainīgos* (*slack variables*), 
  kas nosaka sākumstāvokli: visi vektora :math:`\mathbf{x}` mainīgie ir 0, 
  bet visi nokares mainīgie :math:`\mathbf{y}` vienādi ar attiecīgajām 
  vērtībām :math:`\mathbf{b}`.


**Gadījums Nr.2:** 
  Dots LP uzdevums, kur nevienādības vietā ir vienādība:

  .. math::

    A\mathbf{x} \textcolor{red}{\leq} \mathbf{b},\;\;\mathbf{x} \geq 0,\;\; \mathbf{b} \geq 0,

  tad pirmo tuvinājumu vispirms ir jāatrod.
  Viens no veidiem - sākt risināt nedaudz izmainītu uzdevumu.

  .. figure:: figs/adding-artificial-variables.png
     :width: 5in

     Adding Artificial Variables

  Katram mākslīgajam mainīgajam piekārtojam ļoti negatīvu :math:`c_i`, 
  lai noteikti nebūtu izdevīgi tam piešķirt nekādu pozitīvu vērtību.


**Gadījums Nr.2:** 
  Sākotnēji visi mākslīgie mainīgie ir "pamata mainīgie" (ja izmaksu 
  vektora vērtības :math:`c_i` zem tiem var pataisīt par 0, izmantojot 
  Gausa izslēgšanas metodi). Pēc tam simpleksa algoritms tos citu 
  pēc cita padara par brīvajiem mainīgajiem.

  1. Ja visi mākslīgie mainīgie kļūst brīvi, tad tiem atbilstošās kolonnas 
     var turpmāk ignorēt (aprēķini šajās kolonnās vairs neiespaidos LP atrisinājumu), 
     jo neviens no tiem nebūs pozitīvs.
  2. Ja mākslīgie mainīgie saglabājas pie pamatmainīgajiem un tos izslēgt 
     gājienu skaitā, kas sakristu ar šo mainīgo skaitu, neizdodas, tad nosacījumi ir 
     pretrunīgi.








Dualitāte grafu uzdevumos un citur
-----------------------------------

**Maksimālās plūsmas atrašana grafā**

  .. figure:: figs/max-flow-graph.png
     :width: 4.5in

     Max Flow Graph

  Aplūkotajā grafā katrai šķautnei ir pierakstīta skaitliska vērtība - maksimālā 
  atļautā plūsma, kuru pa šo šķautni var sūtīt (vai nu vienā, vai otrā virzienā). 
  Var sūtīt arī mazāku plūsmu.   


**Uzdevums:** 
  Atrast lielāko plūsmu no virsotnes "IN" uz virsotni "OUT". 
  Šim uzdevumam 1956.g. tika izveidots 
  `Forda-Falkersona algoritms <https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm>`_ 
  (*Ford-Fulkerson algorithm*), ko kursā neaplūkojam. 
  Uzdevumu var arī reducēt uz Lineāro programmēšanu.

**Lineārā programma plūsmai**

  .. figure:: figs/flow-preservation.png
     :width: 300px

     Flow Preservation

  Katrai (neorientētai) šķautnei ieviešam divus mainīgos, piemēram, :math:`x_1` un 
  :math:`x'_1` (nenegatīvas plūsmas katrā no iespējamajiem virzieniem).

  1. Katrai virsotnei grafā rakstām "plūsmas saglabāšanās" ("flow preservation") 
     vienādojumus. Piemēram,

     .. math::
   
       x_1 + x_2 + x'_3 = x'_1 + x'_2 + x_3.

  2. Katrai šķautnei grafā rakstām divas nevienādības caurlaidībai ("edge capacity"). 
     Piemēram,

     .. math::
   
       x_1 \leq 3,\;\;x'_1 \leq 3.

     (Ja šķautne, kas atbilst :math:`x_1` un :math:`x'_1` ir ar caurlaidību :math:`3`.)

  3. Visas plūsmas ir nenegatīvas. Piemēram,

     .. math::
   
       x_1 \geq 0,\;\;x'_1 \geq 0.

**Maksimizējamā funkcija**

  .. figure:: figs/max-flow-graph.png
     :width: 4in

     Max Flow Graph

  1. Var maksimizēt plūsmu summu visām no "IN" izejošajām virsotnēm.
  2. Biežāk izmanto triku: pievieno fiktīvu šķautni no "OUT" atpakaļ uz "IN" - un maksimizē
     plūsmu uz šīs vienas šķautnes.



**Tipiska ideja:** 
  No reālās dzīves nākušam Lineārās Programmēšanas 
  uzdevumam formulējam duālo uzdevumu un mēģinām atrast šī uzdevuma interpretāciju.








Kopsavilkums
--------------

1. Pārveidojām patvaļīgu LP standartformā; izvērstā vai matricu pierakstā.
2. Formulējām un pierādījām Farkaša lemmu.
3. Veidojām dotajam LP uzdevumam duālo uzdevumu. 
4. Formulējām vājo un stipro dualitātes teorēmu.
5. Minējām metodi sākotnējā tuvinājuma izvēlei (vai LP uzdevums
   ir atrisināms un nav pretrunīgs).
6. Aprakstījām, kā dualitāte izpaužas īsāko ceļu meklēšanā, 
   maksimālajām plūsmām vai "shadow pricing" uzdevumam.


**Bibliogrāija**

* `<https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2008/pages/lecture-notes/>`_ -- 
  Algoritmu kurss, kas satur arī lineāro programmēšanu un dualitāti. 
* `<https://ocw.mit.edu/courses/mathematics/18-086-mathematical-methods-for-engineers-ii-spring-2006/video-lectures/lecture-28-linear-programming-and-duality/>`_ -- 
  MIT lekcija 
* `Max Flow to Linear Programming <http://www.cs.cmu.edu/~odonnell/toolkit13/lecture14.pdf>`_ -- 
  Dualitāte grafu uzdevumos, tsk. maksimālajai plūsmai. 
* `Shadow Price <https://economics.stackexchange.com/questions/21796/linear-programming-shadow-price-range>`_ -- 
  Skaidrojums par to, kas ir "shadow price". 

