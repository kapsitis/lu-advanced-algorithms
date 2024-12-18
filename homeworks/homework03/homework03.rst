3. mājasdarbs: Lineārā programmēšana
=======================================================

**1. uzdevums:** 

  Apskatām lineāro programmu: 

  .. math::

    \textcolor{blue}{\max \left( 5x_1 + 3x_2 + 5x_3 \right)}\;\;\text{kur}
    \left\{ \begin{array}{l}
    7x_1 + 4x_2 + 5x_3 \leq 25, \\
    5x_1 + 3x_2 + 6x_3 \leq 19, \\
    x_1 \geq 0,\; x_2 \geq 0,\; x_3 \geq 0.\\
    \end{array} \right.

  **(A)**
    Pārveidot normālformā un atrisināt šo lineāro programmu, izmantojot simpleksa metodes tabulas.
    Sākt ar tuvinājumu :math:`(x_1,x_2,x_3) = (0,0,0)`, katrā solī nākamo palielināmo 
    mainīgo var izvēlēties atbilstoši Danciga nosacījumam (*Dantzig's rule about the most profitable column*) - 
    kolonnu, kurai atbilstošajam mainīgajam ir vislielākais pozitīvais koeficients.
    Ja nepieciešams, pārveidot lineāro programmu nepieciešamajā formātā, 
    pārmainot mainīgo zīmes vai ieviešot nokares (*slack*) mainīgos.

  **(B)** 
    Uzrakstīt šai lineārajai programmai duālo programmu (ar diviem mainīgajiem :math:`y_1,y_2` un trim 
    nevienādībām) un atrisināt to 
    ar kādu bibliotēku (piemēram, Python ``pulp`` vai  ``linprog`` no ``scipy.optimize``). 


**2. uzdevums:** 

  Apskatām uzdevumu par maksimālo sapārojumu (*maximum matching*). 
  Šajā uzdevumā doti :math:`n` cilvēki un :math:`n` uzdevumi ar nosacījumiem, 
  kuri cilvēki drīkst pildīt kurus uzdevumus. 
  
  Jānosaka maksimālais uzdevumu skaits, ko var pildīt vienlaikus, 
  ja viens cilvēks drīkst pildīt ne vairāk kā vienu uzdevumu 
  (un vienu uzdevumu drīkst pildīt ne vairāk kā viens cilvēks). 
  Šo uzdevumu var modelēt ar lineāru programmu ar mainīgajiem :math:`x_{ij}` 
  katram :math:`i,j`, kur :math:`i` ir cilvēks, kas drīkst pildīt uzdevumu :math:`j`. 
  (Ja cilvēks :math:`i` nedrīkst pildīt uzdevumu :math:`j`, tad attiecīgo mainīgo :math:`x_{ij}` neievieš.)
  Lineārā programma izskatīsies šādi: 

  .. math:: 

    \textcolor{blue}{\max \left( \sum x_{ij} \right)},\;\;\text{kur}
    \left\{ \begin{array}{l}
    \sum_{j \in [1;n]} x_{ij} \leq 1,\;\text{katram $i$}\\
    \sum_{i \in [1;n]} x_{ij} \leq 1,\;\text{katram $j$}\\
    x_{ij} \leq 1,\;\text{katriem $i,j$}\\
    x_{ij} \geq 0,\;\text{katriem $i,j$}\\
    \end{array} \right.


  Pierādīt, ka šīs lineārās programmas atrisinājums reālos skaitļos 
  (kas sasniedz, piemēram, summu :math:`S`), 
  ir vienlaikus arī atrisinājums veselos skaitļos -- to pašu maksimumu var sasniegt arī prasot, 
  lai visi :math:`x_{ij}` būtu veseli skaitļi no :math:`\{ 0, 1 \}`. 

**3. uzdevums:**
  Dots grafs, kura 6 virsotnes apzīmētas ar lielajiem burtiem: 
  :math:`V = \{ \mathtt{S}, \mathtt{A}, \mathtt{B}, \mathtt{C}, \mathtt{D}, \mathtt{T} \}` 
  (:math:`\mathtt{S}` ir izteka, :math:`\mathtt{T}` ir ieteka). 
  Grafa šķautnes ir: 

  .. math::
  
    e_1 = \mathtt{SA},\, e_2 = \mathtt{SC},\, e_3 = \mathtt{AB},\, e_4 = \textcolor{red}{\mathtt{BC}},\, e_5 = \mathtt{BT},\, e_6 = \mathtt{CA},\, e_7 = \mathtt{CD},\, e_8 = \mathtt{DB},\, e_9 = \mathtt{DT}
  
  un to kapacitātes ir attiecīgi: 

  .. math::

     c(\mathtt{SA})=15,\, c(\mathtt{SC})=12,\, c(\mathtt{AB})=11,\, c(\mathtt{BC})=8,\, c(\mathtt{BT})=19,\, c(\mathtt{CA})=5,\, c(\mathtt{CD})=15,\, c(\mathtt{DB})=6,\, c(\mathtt{DT})=21    


  .. figure:: figs/problem3.3.png
     :width: 2.4in 

  **(A)** 
    Katrai no grafa šķautnēm :math:`e_i \in E` ar :math:`x_i` apzīmēta plūsma šajā šķautnē. 
    Aprakstīt maksimālās plūsmas uzdevumu kā lineāro programmu ar nevienādībām, vienādojumiem un mainīgajiem :math:`x_i`. 
    Atrisiniet šo lineāro programmu ar "pulp" vai līdzīgu Python bibliotēku. 

  **(B)** 
    Sanumurējiet vienādojumus un nevienādības lineārajā programmā, kas iegūta punktā (A). 
    (Ierobežojumi :math:`x_i \geq 0` nav jānumurē.)
    Uzrakstīt minētajai lineārajai programmai duālo lineāro programmu. 
    Jaunie mainīgie :math:`y_j` atbilst vienādojumu/nevienādību 
    numuriem. Šī lineārā programma nav jārisina, tikai jāuzraksta. 


**4.uzdevums:** 
  Darbnīca var iegādāties hidrauliskās preses un virpas.
  Katra prese palielinātu viņu ikmēneša ienākumus par 100 EUR, bet virpa par 150 EUR. 
  Prese aizņem 3 kvadrātmetrus, bet virpa 6 kvadrātmetrus. 
  Preses cena ir 8000 EUR, bet virpas cena ir 4000 EUR. 
  Darbnīcai ir 40000 EUR un 40 kvadrātmetri brīvas vietas. 
  
  **(A)**
    Sastādīt 
    veselo skaitļu programmēšanas uzdevumu ar kādu Python bibliotēku. 
    Atrast maksimālos ienākumus. 

  **(B)** 
    Relaksēt veselo skaitļu ierobežojumu; pieņemt ka prešu un virpu 
    skaits var būt jebkurš nenegatīvs daļskaitlis. 
    Atrast maksimālos ienākumus šādam lineārās programmēšanas uzdevumam.
    