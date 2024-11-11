11. Lineārā programmēšana un dualitāte
===============================================

Simpleksa algoritms praksē strādā labi, bet tam ir vairākas problēmas: 

  * Tam ir dažādi varianti -- pirmā stūra izvēle, pārejas izvēle (dažreiz randomizācija), 
  * Tas var nestrādāt polinomiālā laikā, ja izveido īpašus piemērus. 
    Polinomiāla laika algoritms ir industrijas standarts visam, ko izmanto praksē. 



Divu spēlētāju matricu spēles 
--------------------------------

Divi spēlētāji :math:`X` un :math:`Y` 
vienlaikus izvēlas vienu no 
galīga skaita gājienu. 
Piemēram, spēlētājs :math:`X` izvēlas rindu :math:`x_i` 
un spēlētājs :math:`Y` izvēlas kolonnu :math:`y_j`. 

Matricas :math:`A = (a_{ij})` elements :math:`a_{ij}` 
parāda, cik spēlētājs :math:`X`
maksā spēlētājam :math:`Y`. 
Spēlētājs :math:`X` vēlas šo samaksu minimizēt, 
bet spēlētājs :math:`Y` vēlas to maksimizēt.

*Piezīme:* Šīs ir nulles summas spēles (atšķiras no 
cietumnieku dilemmas); viss, ko samaksā spēlētājs 
:math:`X` nonāk pie spēlētāja :math:`Y`. 
(Ja :math:`Y` zaudē un maksā spēlētājam :math:`X`, tad 
matricā :math:`A` raksta negatīvus skaitļus.)



**Piemērs:** 
  Aplūkojam :math:`2 \times 2` matricu: 

  .. math:: 

    A = \left( \begin{array}{cc}
    1 & 2 \\ 
    4 & 8 \\
    \end{array} \right)

  Šajā matricā spēlētājs :math:`Y` vienmēr izvēlēsies 
  otro kolonnu :math:`y_2`, jo :math:`2 > 1` un 
  :math:`8 > 4`. Pie jebkura :math:`X` gājiena (jeb rindas) ir 
  labāk izvēlēties otro kolonnu. 

  Savukārt spēlētājs :math:`X` vienmēr izvēlēsies 
  pirmo rindu :math:`x_1`, jo skaitlis :math:`a_{12} = 2`
  ir mazāks nekā :math:`a_{22} = 8` un spēlētājs :math:`X`
  vēlas minimizēt to, kas jāmaksā otram spēlētājam. 

*Piezīme:* Skaitli :math:`a_{12}`, kas ir mazākais 
par jebko citu savā kolonnā, bet lielāks par 
jebko citu savā rindiņā, saucas *sedlu punkts*. 
Ja spēlei eksistē sedlu punkts, tad abu 
spēlētāju optimālās stratēģijas ir deterministiskas
(*pure strategies*). 

**Piemērs:** 
  Aplūkojam spēli, kurā abi spēlētāji :math:`X,Y` 
  izvēlas vienu no trim gājieniem: 
  "akmens" (R), "papīrs" (P), "šķēres" (S). 
  Maksājumu matrica ir sekojoša: 

  .. math:: 

    A = \left( \begin{array}{ccc}
    0 & 1 & -1 \\
    -1 & 0 & 1 \\
    1 & -1 & 0 \\
    \end{array} \right)

*Piezīme:* Šādai spēles matricai neeksistē 
sedlu punkts, tāpēc stratēģija nevienam spēlētājam 
nevar stabilizēties uz kādu vienu gājienu. 
Ja otrs spēlētājs zinās otra spēlētāja stratēģiju 
(viņa deterministisko nākamo gājienu), tad 
otram spēlētājam ir optimāli izvēlēties savu gājienu 
atkarībā no tā. Šādās situācijās arī eksistē 
optimāla stratēģija, bet tā ir *jaukta stratēģija* 
(*mixed strategy*) -- tā izvēlas gājienus ar noteiktām 
varbūtībām. 


Jauktās stratēģijas
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jauktās stratēģijas apraksta *stohastiski vektori*. 
Ja spēlētājam :math:`X` ir :math:`n` iespējami 
gājieni, bet spēlētājam :math:`Y` ir :math:`m` 
iespējami gājieni, tad tos var 

.. math:: 

  \mathbf{x} = \left(
    \begin{array}{c}
    x_1\\
    x_2\\
    \ldots\\
    x_n
    \end{array} \right),\;\;\;
  \mathbf{y} = \left(
    \begin{array}{c}
    y_1\\
    x_2\\
    \ldots\\
    y_m
    \end{array} \right).

Stohastiskie vektori apmierina sakarības: :math:`x_1 + x_2 + \ldots + x_n = 1`, 
:math:`y_1 + \ldots + y_m = 1` un visi :math:`x_i` un :math:`y_j`  
ir nenegatīvi. 

Spēles rezultātu apraksta vektoru/matricu 
reizinājums :math:`\mathbf{x}^T A \mathbf{y}`. 

**Piemērs:** 
  Akmens, papīra, šķēru spēlē var izvēlēties 
  spēlētājam :math:`X` jauktu stratēģiju 
  :math:`\mathbf{x}^T = (1/2, 0, 1/2)` un 
  spēlētājam :math:`Y` jauktu stratēģiju 
  :math:`\mathbf{y}^T = (1/2, 1/3, 1/6)`.
  Tad atkārtoti spēlējot, vidējā vērtība, ko 
  iegūst spēlētājs :math:`Y` ir šāda: 

  .. math::

    \mathbf{x}^T A \mathbf{y} = 
    \left( \begin{array}{ccc}
    \frac{1}{2} & 0 & \frac{1}{2} \end{array} \right) \cdot 
    \left( \begin{array}{ccc}
    0 & 1 & -1 \\
    -1 & 0 & 1 \\
    1 & -1 & 0 \\
    \end{array} \right) \cdot 
    \left(
    \begin{array}{c}
    \frac{1}{2}\\
    \frac{1}{3}\\
    \frac{1}{6}
    \end{array} \right) = 
    \left( \begin{array}{ccc}
    \frac{1}{2} & 0 & -\frac{1}{2} \end{array} \right) \cdot 
    \left(
    \begin{array}{c}
    \frac{1}{2}\\
    \frac{1}{3}\\
    \frac{1}{6}
    \end{array} \right) = \frac{1}{4} - \frac{1}{12} = \frac{1}{6}. 

  Esam ieguvuši, ka spēlētājs :math:`X` katrā gājienā 
  zaudē vidēji :math:`\frac{1}{6}`, lai gan spēles matrica 
  ir simetriska (:math:`a_{ij} = -a_{ji}`), t.i. spēle pret abiem 
  spēlētājiem ir ar vienādiem noteikumiem (vajadzētu varēt panākt vērtību :math:`0`). 
  Tāpēc jauktā stratēģija :math:`\mathbf{x}` nav optimāla. 


**Definīcija:** 
  Par matricu spēles *vērtību* sauc mazāko zaudējumu, 
  ko var sev garantēt spēlētājs :math:`X`, izvēloties optimālo no 
  visām stohastiskajām stratēģijām: 

  .. math:: 

    v(A) = \min_{\text{visiem}\;\mathbf{x}} \left( 
    \max_{\text{visiem}\;\mathbf{y}} \mathbf{x}^T A \mathbf{y}
    \right).



Pagaidām uzdevums neizskatās pēc lineāras programmas -- izteiksmē, 
kura jāminimizē ietilpst nezināms vektors :math:`\mathbf{y}`, 
kas apraksta otra spēlētāja jaukto stratēģiju, ko mēs nevaram kontrolēt. 

Var izmantot sekojošu triku: Fiksējam savu stratēģiju :math:`\mathbf{x}`. 
Ja pretinieks :math:`Y` šo :math:`\mathbf{x}` jau zina, tad viņam 
eksistē optimāla atbildes stratēģija :math:`\mathbf{y}`, kas ir 
deterministiska -- tā vienkārši izvēlas reizinājumā :math:`\mathbf{x}^T \cdot A`
lielāko koordināti un liek tur vērtību :math:`1`. 

**Piemērs:** 
  Ja akmens-papīra-šķēru spēlē Spēlētājs :math:`X` izvēlas jauktu stratēģiju 
  :math:`\mathbf{x}^T = (0.7, 0.2, 0.1)` (t.i. :math:`X` apsola 
  izvēlēties "akmeni" ar :math:`70\%` varbūtību, 
  "papīru" ar :math:`20\%` varbūtību, bet "šķēres" ar :math:`10\%` varbūtību), 
  tad spēlētājam :math:`Y` ir optimāli atbildēt ar stratēģiju 
  :math:`\mathbf{y}^T = (0, 1, 0)` jeb :math:`100\%` gadījumos izvēlēties 
  "papīru". 



Optimālā stratēģija ar lineāru programmu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. https://www.matem.unam.mx/~omar/math340/matrix-games.html

Matricu spēles ir risināmas ar lineārās programmēšanas līdzekļiem -- 
sk. *Matrix Games* :ref:`[Cam16] <Cam16>`.
Tā kā spēlētājs :math:`X` zina, ka otrs spēlētājs (iespējams, pēc ilgākiem 
novērojumiem) uzzinās viņa jaukto stratēģiju un izvēlēsies optimālo 
atbildi :math:`y_j` (maksimālo elementu no 
matricu reizinājuma :math:`\mathbf{x}^T A`), tad 
spēlētājs :math:`X` "minimizē maksimumu" jeb atrod savu gājienu varbūtības 
:math:`x_1, \ldots, x_n`, izmantojot lineāru programmu: 

.. math:: 

  \textcolor{blue}{\min(z)},\;\text{kur}
  \left\{ \begin{array}{l}
  (z, z, \ldots, z) \geq \mathbf{x}^T A, \\
  x_1 + x_2 + \ldots + x_n  = 1,\\
  x_1, x_2, \ldots, x_n \geq 0.
  \end{array} \right. 


Otrs spēlētājs :math:`Y` zina, ka pirmais spēlētājs :math:`X` 
izvēlēsies optimālo (minimālo) atbildi :math:`x_i` uz 
katru viņa jaukto stratēģiju :math:`\mathbf{y}`, tad arī 
spēlētājs :math:`Y` var atrast savu gājienu varbūtības 
:math:`y_1,\ldots, y_m`, izmantojot lineāru programmu: 

.. math:: 

  \textcolor{blue}{\max(w)},\;\text{kur}
  \left\{ \begin{array}{l}
  (w, w, \ldots, w) \leq A \mathbf{y}, \\
  y_1 + y_2 + \ldots + y_m  = 1,\\
  y_1, y_2, \ldots, y_m \geq 0.
  \end{array} \right. 


Spēles vērtība (ko pie abu spēlētāju optimālām stratēģijām 
spēlētājs :math:`X` maksā spēlētājam :math:`Y`) ir viena un 
tā pati abos gadījumos. 

**Teorēma (Minimaksa teorēma):** 
  Katrai matricai :math:`A` *spēles vērtību* var izteikt divos līdzvērtīgos veidos: 

  .. math:: 

    v(A) = \min_{\text{visiem}\;\mathbf{x}} \left( 
    \max_{\text{visiem}\;\mathbf{y}} \mathbf{x}^T A \mathbf{y}
    \right) = 
    \max_{\text{visiem}\;\mathbf{y}} \left( 
    \max_{\text{visiem}\;\mathbf{x}} \mathbf{x}^T A \mathbf{y}
    \right). 

**Secinājums:** 
  Ja esam uzminējuši kaut kādas stratēģijas :math:`\mathbf{x}^{\ast}` 
  un :math:`\mathbf{y}^{\ast}` attiecīgi spēlētājiem :math:`X` un :math:`Y`, 
  tad tās abas ir optimālas tad un tikai tad, ja izpildās vienādība: 

  .. math:: 

    \min ((\mathbf{x}^{\ast})^T A) = \max (A \mathbf{y}). 


Stohastiskie vektori apraksta slēgtu ierobežotu kopu 
(tādas kopas sauc par kompaktām). 

Veierštrāsa teorēma par ekstremālo vērtību kompaktā kopā 
nozīmē to, ka abām lineārajām programmām eksistē 
atrisinājumi un tātad 
katrai matricu spēlei eksistē optimālā jauktā stratēģija
katram no spēlētājiem. 
Sk. `<https://en.wikipedia.org/wiki/Extreme_value_theorem>`_. 


Skaitlisks spēles piemērs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. https://youtu.be/feb9j65Iz4w?si=tGIUByy4Hc5fwr_b

Aplūkosim spēli ar sekojošu matricu (sk. :ref:`[Str18] <Str18>`): 

.. math:: 

  A = \left( \begin{array}{cc}
  1 & 8 \\
  4 & 2 \\
  \end{array} \right). 

Kā parasti, spēlētājs :math:`X` izvēlas rindiņu šajā matricā, bet 
spēlētājs :math:`Y` izvēlas kolonnu. 
Izveidojam lineāras programmas, lietojot Python bibliotēku ``pulp``.
Primārā problēma (spēlētāja :math:`X` jauktā stratēģija):

.. code-block:: python 

  from pulp import *

  model = LpProblem(sense=LpMinimize)

  x1 = LpVariable(name="x1", lowBound=0)
  x2 = LpVariable(name="x2", lowBound=0)
  z = LpVariable(name="z")

  model += z - 1*x1 - 4*x2 >= 0
  model += z - 8*x1 - 2*x2 >= 0
  model += x1 + x2 == 1 
  model += z  # Mērķa funkcija

  status = model.solve(PULP_CBC_CMD(msg=False))
  print(f"(x1,x2) = {x1.value(), x2.value()}")
  print(f"Value of the game = {model.objective.value()}")

Stratēģija ir :math:`(\mathbf{x}^{\ast})^T = (x_1,x_2) = (2/9, 7/9)` un spēles vērtība :math:`z = 3\frac{1}{3}`. 


Duālā problēma (spēlētāja :math:`Y` jauktā stratēģija):

.. code-block:: python 

  from pulp import *

  model = LpProblem(sense=LpMaximize)

  y1 = LpVariable(name="y1", lowBound=0)
  y2 = LpVariable(name="y2", lowBound=0)
  w = LpVariable(name="w")

  model += 1*y1 + 8*y2 - w >= 0
  model += 4*x1 + 2*x2 - w >= 0
  model += y1 + y2 == 1 
  model += w  # Mērķa funkcija

  status = model.solve(PULP_CBC_CMD(msg=False))
  print(f"(y1,y2) = {y1.value(), y2.value()}")
  print(f"Value of the game = {model.objective.value()}")

Stratēģija ir :math:`(\mathbf{y}^{\ast})^T = (y_1,y_2) = (2/3, 1/3)` 
un spēles vērtība :math:`w = 3\frac{1}{3}`. 

Pēc minimaksa teorēmas abām spēles vērtībām :math:`z` un 
:math:`w` ir jāsakrīt. 

Optimālās stratēģijas var piereizināt ar matricu :math:`A` (vienu no kreisās puses, 
otru -- no labās puses): 

.. math:: 

  (\mathbf{x}^{\ast})^T A = (2/9, 7/9) \cdot \left( \begin{array}{cc} 
  1 & 8 \\
  4 & 2 \\
  \end{array} \right) = 
  \left( \frac{2}{9} \cdot 1 + \frac{7}{9} \cdot 4, \frac{2}{9} \cdot 8  + \frac{7}{9} \cdot 2 \right) =
  \left( \frac{30}{9}, \frac{30}{9} \right) =  \left( 3\frac{1}{3}, 3\frac{1}{3} \right).

.. math:: 

  A \cdot \mathbf{y} = \left( \begin{array}{cc}
  1 & 8 \\
  4 & 2 \\
  \end{array} \right) \cdot \left( \begin{array}{c}
  2/3\\ 
  1/3\\
  \end{array} \right) = \left( \begin{array}{c}
  10/3\\ 
  10/3\\
  \end{array} \right) = \left( \begin{array}{c}
  3\frac{1}{3}\\ 
  3\frac{1}{3}\\
  \end{array} \right).


Abos gadījumos iegūstam vektorus ar vairākām identiskām vērtībām :math:`3\frac{1}{3}`. 
Šī sakarība izpildās jauktām stratēģijām; to var izmantot optimālo vērtību 
atrašanai. To, ka visām derīgajām izvēlēm atbildīs vienādas varbūtības 
spēļu teorijā sauc par *vienaldzības principu* 
(*Indifference Principle*).





Kāpostu-burkānu uzdevums un tā duālais
---------------------------------------

**Piemērs:** 
  Aplūkojam LP uzdevumu sējumu platībai, kas ierobežota ar :math:`5` hektāriem:

  .. math:: 

    \textcolor{blue}{\max \left( 1200x_k + 1700x_b \right)},\;\;\text{kur}\;\;
    \left\{ \begin{array}{l} 
    x_k \leq 3,\\
    x_b \leq 4\\
    x_k + k_b \leq 5,\\
    x_k,x_b \geq 0. 
    \end{array} \right.


.. code-block:: python 

  from pulp import *

  model = LpProblem(sense=LpMaximize)
  x_k = LpVariable(name="kaposti", lowBound=0)
  x_b = LpVariable(name="burkani", lowBound=0)

  model += x_k <= 3        # kāpostu ierobežojums
  model += x_b <= 4        # burkānu ierobežojums
  model += x_k + x_b <= 5  # platības ierobežojums (5 ha)
  model += 1200 * x_k + 1700 * x_b

  status = model.solve(PULP_CBC_CMD(msg=False))
  print(f'Kāposti: {x_k.value()}')
  print(f'Burkāni: {x_b.value()}')
  print(f'Peļņa: {model.objective.value()}')


Atrisinājums: :math:`(x_k, x_b) = (1,4)`. Mērķa funkcija: :math:`8000`. 


**Duālais uzdevums**
  Kā pārliecināties, vai tas, ko atrada programma, ir īstais atrisinājums (un nevar labāk)?
  Visas trīs nevienādības var piereizināt ar nenegatīviem skaitļiem :math:`y_1, y_2, y_3` 
  un saskaitīt. 

  .. math:: 

    \textcolor{blue}{\min \left( 3y_1 + 4y_2 + 5y_3 \right)},\;\;\text{kur}\;\;
    \left\{ \begin{array}{l} 
    y_1 + y_3 \geq 1200,\\
    y_2 + y_3 \geq 1700,\\
    y_1,y_2,y_3 \geq 0. 
    \end{array} \right.

.. code-block:: python 

  from pulp import *

  model = LpProblem(sense=LpMinimize)
  y1 = LpVariable(name="y1", lowBound=0)
  y2 = LpVariable(name="y2", lowBound=0)
  y3 = LpVariable(name="y3", lowBound=0)

  model += y1 + y3 >= 1200
  model += y2 + y3 >= 1700
  model += 3*y1 + 4*y2 + 5*y3

  status = model.solve(PULP_CBC_CMD(msg=False))
  print(f'(y1, y2, y3)= ({y1.value()}, {y2.value()}, {y3.value()})')
  print(f'Peļņas augšējais novērtējums: {model.objective.value()}')
 
Atrisinājums: :math:`(y_1, y_2, y_3)= (0.0, 500.0, 1200.0)`. Mērķa funkcija: :math:`8000`. 



**Primārais un duālais LP uzdevumi matricu pierakstā:**

  .. math:: 

    (P): \textcolor{blue}{\max \left( 1200x_k + 1700x_b \right)},\;\;\text{kur}\;\;
    A = \left( \begin{array}{cc}
    1 & 0 \\
    0 & 1 \\
    1 & 1 \\
    \end{array} \right) \cdot \left( \begin{array}{c}
    x_k \\
    x_b \\
    \end{array} \right) \leq \left( \begin{array}{c} 
    3 \\
    4 \\
    5 \\
    \end{array} \right),\;\; x_k,x_b \geq 0. 

  .. math:: 

    (D):  \textcolor{blue}{\min \left( 3y_1 + 4y_2 + 5y_3 \right)},\;\;\text{kur}\;\;
    A = \left( \begin{array}{ccc}
    1 & 0 & 1 \\
    0 & 1 & 1 \\
    \end{array} \right) \cdot \left( \begin{array}{c}
    y_1 \\
    y_2 \\
    y_3 \\
    \end{array} \right) \geq \left( \begin{array}{c} 
    1200 \\
    1700 \\
    \end{array} \right),\;\; y_1, y_2, y_3 \geq 0. 


Duālās problēmas interpretācijas 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ēnu cenas (Shadow prices):**
  Peļņas maksimizēšanas uzdevumos
  duālais atrisinājums :math:`(y_1, y_2, y_3)= (0.0, 500.0, 1200.0)` parāda, 
  kādā ātrumā pieaugtu peļņa, ja (kādā īsā intervālā) nedaudz atvieglotu kādu 
  ierobežojumu. Ir pavisam trīs ierobežojumi jeb trīs *ēnu cenas*: kāpostiem, 
  burkāniem un zemes hektāram (gada nomas maksa).
  
  * :math:`y_1 = 0`. Atvieglojot ierobežojumu uz kāpostu sējas platību 
    nav ietekmes uz peļņu, jo arī pašlaik visas kāpostu sēklas netiek izmantotas.  
  * :math:`y_2 = 500`. Ja burkānu sēklu būtu nedaudz vairāk, peļņa pieaugtu 
    ar ātrumu :math:`500` par burkānu sēklu vienību. 
    Ievērosim, ka :math:`1700 - 1200` ir peļņas starpība starp burkāniem un kāpostiem: 
    varētu kāpostus aizstāt ar burkāniem. 
  * :math:`y_3 = 1200`. Papildus zemes hektārs atnestu :math:`1200` papildus peļņu, 
    jo mums ir neizmantotas kāpostu sēklas.

  *Ēnu cenas* ir augšējais novērtējums tam, par cik būtu ekonomiski pamatoti 
  iegādāties vienu vai otru resursu. Turklāt ēnu cenas paliek spēkā, 
  vienīgi runājot par nelieliem iepirkšanas apjomiem,  
  lai neizmainītos LP uzdevuma pieļaujamā apgabala forma, kad optimālais risinājums 
  pārvietojas uz kādu citu stūri ar citiem būtiskajiem ierobežojumiem. Piemēram, 
  būtiski palielinot pieejamo zemes platību virs 5 ha, varētu panākt, 
  lai zemei ēnu cena kļūtu 0, bet parādītos pozitīva ēnu cena kāpostu sēklām. 
  Ēnu cenām nav sakara ar faktiskajām cenām, ja tādas arī parādās LP uzdevumā.


**Gravitācijas un normālās reakcijas modelis:** 
  Var uzzīmēt pieļaujamo apgabalu primārajam uzdevumam un primārā uzdevuma atrisinājums 
  ir neliela lodīte, kas nonākusi (sekojot gravitācijas gradientam) vietā ar viszemāko potenciālu. 
  Tad duālā uzdevuma atrisinājums ir normālās reakcijas, ko dod tie balsti, uz kuriem 
  balstās lodīte, kas līdzsvaro gravitācijas spēku. 


**Interpretācija ar nevienādību novērtējumiem:** 
  Duālo uzdevumu var interpretēt šādi: katrs pieļaujams punkts 
  :math:`(y_1, y_2, y_3)`, kas apmierina visus ierobežojumus (bet varbūt 
  neoptimizē mērķa funkciju), 
  dod novērtējumu no augšas primārās programmas atrisinājumam. 

  Kāpostu-burkānu uzdevumam ir vairāki pieļaujami atrisinājumi, 
  arī iegūtie novērtējumi no augšas būs dažādi: 

  * :math:`(y_1, y_2, y_3) = (1200, 1700, 0)`. 
    Tad ir spēkā novērtējums: 

    .. math:: 

      1200 x_k + 1700 x_b \leq 1200 \cdot (x_k) + 1700 \cdot (x_b) \leq 1200 \cdot 3 + 1700 \cdot 4 = 10400.

  * :math:`(y_1, y_2, y_3) = (200, 700, 1000)`.
    Tad ir spēkā novērtējums: 

    .. math:: 

      1200 x_k + 1700 x_b \leq 200 \cdot (x_k) + 700 \cdot (x_b) + 1000 \cdot (x_k + x_b) 
      \leq 200 \cdot 3 + 700 \cdot 4 + 1000 \cdot 5 = 8400.

  * :math:`(\mathbf{y}^{\ast})^T = (y_1, y_2, y_3) = (0, 500, 1200)`.
    Tad ir spēkā novērtējums: 

    .. math:: 

      1200 x_k + 1700 x_b \leq 0 \cdot (x_k) + 500 \cdot (x_b) + 1200 \cdot (x_k + x_b)
      \leq 0 + 500 \cdot 4 + 1200 \cdot 5 = 8000. 

Pēdējais no novērtējumiem, ko rada duālā uzdevuma optimālais atrisinājums 
:math:`(\mathbf{y}^{\ast})^T` ir :math:`8000`, kuru tālāk uzlabot nevar. 

Ja primārais LP uzdevums prasīja maksimizēt kaut ko, tad 
duālais LP uzdevums prasa minimizēt. Un katrs duālā uzdevuma pieļaujamais 
punkts (ja vien tas nav pats minimums) dos duālajai
mērķfunkcijai :math:`3y_1 + 4y_2 + 5y_3` lielāku vērtību 
nekā ir primārās problēmas mērķfunkcija :math:`1200x_k + 1700x_b`
katrā pieļaujamā punktā :math:`(x_k,x_b)`.
   




**Piemērs:**
  Aplūkojam standartformas LP uzdevumu, kur jāmeklē minimums, 
  visas nevienādības sistēmā ir :math:`\leq`, 
  bet visi mainīgie :math:`x_i` -- nenegatīvi skaitļi. 
  Primārais (P) un duālais (D) doti ar matricu izteiksmēm: 

    .. math:: 
    
      (P): \textcolor{blue}{\min\left( \mathbf{c}^T \cdot \mathbf{x} \right)},\;\;\text{kur}
      A \mathbf{x} \leq \mathbf{b},\;\; \mathbf{x} \geq 0.

    .. math:: 

       (D): \textcolor{blue}{\max\left( \mathbf{b}^T \cdot \mathbf{y} \right)},\;\;\text{kur}
       A^T \mathbf{y} \leq \mathbf{c},\;\; \mathbf{y} \geq 0.





Vispārīga LP uzdevuma duālais 
---------------------------------

Duālos mēdz pierakstīt arī tādiem LP uzdevumiem, kuri nav 
standartformā. Mērķa funkcija primārajā uzdevumā var būt gan 
jāminimizē, gan jāmaksimizē, nevienādības vai vienādības ierobežojumos 
var būt uz jebkuru pusi, dažreiz mainīgie :math:`x_i` nevar būt negatīvi, citreiz 
tie netiek ierobežoti. Visi šādi uzdevumi pārveidojas par duālajiem. 


**Primārā lineārā programma:**
  Definēsim lineāru programmu :math:`(P)`, ko sauksim par *primāro LP*:

  .. math::

    (P): \textcolor{blue}{\min \left( c_1 x_1 + c_2 x_2 + \ldots + c_n x_n \right)},\;\;\text{kur}\;\;
    \left\{ \begin{array}{l}
    a_{11} x_1 + a_{12} x_2 + \ldots + a_{1n} x_n  \;\;\textcolor{red}{?}\;\; b_1,\\
    \ldots\\
    a_{k1} x_1 + a_{k2} x_2 + \ldots + a_{kn} x_n \;\;\textcolor{red}{?}\;\; b_k,\\
    x_1 \geq 0,\; x_2 \geq 0,\;\ldots \\
    \end{array} \right.

  Šeit LP var nebūt standartformā: 

  * Nosacījumiem :math:`a_{i1} x_1 + a_{i2} x_2 + \ldots + a_{in} x_n \;\;\textcolor{red}{?}\;\; b_i`,
    jautājuma zīmes vietā var būt jebkura zīme (:math:`\geq`, :math:`\leq`, :math:`=`). 
  * Mainīgajiem :math:`x_i` var būt nosacījumi :math:`x_i \geq 0`, :math:`x_i \leq 0`, 
    vai arī var nebūt nosacījuma uz :math:`x_i`.


**Definīcija:**
   Par *duālo programmu* sauc lineāro programmu:

   .. math:: 

     (D): \textcolor{blue}{\max \left( b_1 y_1 + b_2 y_2 + \ldots + b_k y_k \right)},\;\;\text{kur}\;\;
     a_{11} y_1 + a_{21} y_2 + \ldots + a_{k1} y_k \;\;\textcolor{red}{?} \;\; c_k\;\;\mbox{pie $k = 1,\ldots,n$}.

   Simbolu jautājuma zīmes vietā nosaka šādi:

   * Ja primārajā LP bija nosacījums :math:`x_i \geq 0`, tad jautājuma zīmes vietā ir :math:`\geq`.
   * Ja primārajā LP bija nosacījums :math:`x_i \leq 0`, tad jautājuma zīmes vietā ir :math:`\leq`.
   * Ja primārajā LP nebija nosacījuma attiecībā uz :math:`x_i`, tad jautājuma zīmes vietā ir :math:`=`.

   Attiecībā uz mainīgajiem :math:`y_1, y_2, \ldots, y_k`, nosacījumi ir atkarīgi no tā, 
   kāda zīme bija primārās LP nosacījumā 
   :math:`a_{i1} x_1 + a_{i2} x_2 + \ldots + a_{in} x_n \;\;\textcolor{red}{?} \;\; b_i`:

   * Ja :math:`?` vietā bija :math:`\geq`, tad mums tagad ir nosacījums :math:`y_i \leq 0`.
   * Ja :math:`?` vietā bija :math:`\leq`, tad mums tagad ir nosacījums :math:`y_i \geq 0`.
   * Ja :math:`?` vietā bija :math:`=`, tad mums tagad nav nosacījuma attiecībā uz :math:`y_i`.


**Piemērs**
  Aplūkojam primāro LP uzdevumu, kura ierobežojumos saliktas visādu veidu nevienādības:

  .. math:: 
    
    \textcolor{blue}{\max \left( 4x_1 + 2x_2 - x_3 \right)},\;\; \text{kur}\;\; 
    \left\{
    \begin{array}{l}
    x_1 + x_2 + x_3 = 20\\
    2x_1 - x_2 \geq 6\\
    3x_1 + 2x_2 + x_3 \leq 40\\
    x_1,x_2 \geq 0
    \end{array} \right.

  Tas pats matricu pierakstā, kur :math:`\mathbf{x}` ir kolonnas vektors ar 3 koordinātēm :math:`x_1,x_2,x_3`:  

  .. math::

    (P): \textcolor{blue}{\max \left( (4, 2, -1) \cdot \mathbf{x} \right)},\;\;\text{kur}\;\;
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
    \end{array} \right)\;\;\text{un}

    x_1 \geq^{\textcolor{blue}{(d)}} 0,\; x_2 \geq^{\textcolor{blue}{(e)}} 0, 
    x_3\;\text{bez nosac.}^{\textcolor{blue}{(f)}}

**Atbilstošais duālais LP uzdevums:**
  Apzīmējam :math:`\mathbf{y}` kolonnas vektoru ar 3 koordinātēm: :math:`y_1, y_2, y_3`. Tad

  .. math:: 

    (D): \textcolor{blue}{ \min \left(  (20,6,-40) \cdot \mathbf{y}  \right) },\;\;\text{kur}\;\;
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
    \end{array} \right)\;\;\text{un}

    y_1\;\text{bez nosac.}^{\textcolor{blue}{(a)}},\; 
    y_2 \leq^{\textcolor{blue}{(b)}} 0,\; 
    y_3 \geq^{\textcolor{blue}{(c)}} 0.

  Duālajā uzdevumā koeficientus iegūst, transponējot matricu :math:`A`. 
  ienādību un nevienādību tipus nosaka atbilstoši 
  augšminētajiem noteikumiem: Piemēram, ja :math:`x_1 \geq 0` primārajā 
  problēmā, tad :math:`x_1` mainīgajam atbilstošais duālais vienādojums 
  :math:`y_1 + 2y_2 + 3y_3 \geq 4` (arī nevienādība :math:`\geq`). 




Dualitātes teorēmas 
----------------------


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





**Primārās un duālās LP apvienošana**
  Ja dotas primārā LP un duālā LP, varam uzrakstīt jaunu LP, 
  kas satur visus mainīgos (gan :math:`x_1, x_2, \ldots, x_n`, 
  gan :math:`y_1, y_2, \ldots, y_k`), 
  gan visus nosacījumus no abām programmām un pievienot tai vēl vienu nosacījumu:

  .. math:: 
    c_1 x_1 + c_2 x_2 + \ldots + c_n x_n = b_1 y_1 + b_2 y_2 + \ldots + b_k y_k.


Vienīgais gadījums, kad izpildās visi nosacījumi ir, ja 
:math:`x_1, x_2, \ldots, x_n` sasniedz primārās LP maksimums, bet 
:math:`y_1, y_2, \ldots, y_k` sasniedz duālās LP minimumu.

**Secinājums:** 
  Ja mums ir algoritms, kas prot patvaļīgai LP atrast 
  vienu punktu, kas apmierina visus nosacījumus, tad šo algoritmu 
  var izmantot arī maksimuma atrašanai.





Vājā dualitāte
~~~~~~~~~~~~~~~~~~~~~

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
  :math:`\square`




Stiprā dualitāte 
~~~~~~~~~~~~~~~~~~~~~

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





Dualitāte grafu uzdevumos
-----------------------------------

**Maksimālās plūsmas atrašana grafā**

  .. figure:: figs/max-flow-graph.png
     :width: 4.5in

     Max Flow Graph

  Aplūkotajā grafā katrai šķautnei ir pierakstīta skaitliska vērtība - maksimālā 
  atļautā plūsma, kuru pa šo šķautni var sūtīt (vai nu vienā, vai otrā virzienā). 
  Var sūtīt arī mazāku plūsmu.   


**Lineārā programma plūsmai**
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
  Var maksimizēt plūsmu summu visām no "IN" izejošajām virsotnēm.
  Biežāk izmanto triku: pievieno fiktīvu šķautni no "OUT" atpakaļ uz "IN" 
  un maksimizē plūsmu uz šīs vienas šķautnes.








Izmantotā literatūra
---------------------

.. _Cam16:
  
**[Cam16]**
  O.A.Camarena, *Math 340: Linear Programming*, National Autonomous University of Mexico, 
  Fall 2016. Available at `<https://bit.ly/4fmrfzp>`_, 
  `Archived:Cam16 <https://web.archive.org/web/20201022041337/https://www.matem.unam.mx/~omar/math340/index.html>`_.


.. _Goe08:

**[Goe08]**
  M. Goemans, *Advanced Algorithms*, MIT OpenCourseWare, 
  Massachusetts Institute of Technology, Spring 2008. 
  Available at `<https://bit.ly/40IoKmh>`_, 
  `Archived:Goe08 <https://web.archive.org/web/20220531183759/https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2008/>`_.

.. _Str18:

**[Str18]**
  G.Strang, *MIT 18.065 Matrix Methods in Data Analysis*, MIT OpenCourseWare, 
  Massachusetts Institute of Technology, Spring 2018. 
  Available at `<https://bit.ly/40H8H8z>`_, 
  `YouTube <https://youtu.be/feb9j65Iz4w?si=mtQZZxM6jex8zCAp>`_.



.. `<https://ocw.mit.edu/courses/mathematics/18-086-mathematical-methods-for-engineers-ii-spring-2006/video-lectures/lecture-28-linear-programming-and-duality/>`_ -- 
.. MIT lekcija 
.. `Max Flow to Linear Programming <http://www.cs.cmu.edu/~odonnell/toolkit13/lecture14.pdf>`_ -- 
.. Dualitāte grafu uzdevumos, tsk. maksimālajai plūsmai. 
.. `Shadow Price <https://economics.stackexchange.com/questions/21796/linear-programming-shadow-price-range>`_ -- 
.. Skaidrojums par to, kas ir "shadow price". 

