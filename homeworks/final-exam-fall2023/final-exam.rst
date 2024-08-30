Galaeksāmens, 2024-01-08
==========================

Galaeksāmena vērtējums ir 30 procentpunkti.


**1. uzdevums:**
  
  **(A)**
    Uzzīmēt saspiestu sufiksu koku stringam :math:`\mathtt{AIZKARS\#AIZSKAR\$}`, kur simboli :math:`\mathtt{\#}` un :math:`\mathtt{\$}`
    ir alfabētiski pirms visiem citiem burtiem un :math:`\mathtt{\$}` ir pirms :math:`\mathtt{\#}`.
    Cik šim kokam lapu un cik iekšējo mezglu?

  **(B)**
    Sanumurēt visas punktā (A) uzzīmētā sufiksu koka lapas no kreisās uz labo pusi ar numuriem, sākot ar :math:`0`. 
    Uzzīmēt masīvu -- horizontālu tabulu, kurā ir visu sufiksa koka lapu numuri, bet zem katra 
    numura norādīta LCP (*longest common prefix*) vērtība, kas parāda, 
    cik garš ir kopīgais prefikss šim sufiksam ar to sufiksu, kurš ir alfabētiski tieši pirms viņa. 
    (Pieņemt, ka :math:`LCP(0) = 0`, jo pirmajam sufiksam, kas sastāv no viena simbola :math:`\mathtt{\$}`, 
    nav alfabētiski iepriekšējā.) 

  **(C)**
    Sufiksu koks ir *trie* -- kokveida datu struktūra, kurā katra lejupejoša šķautne apzīmēta ar burtu vai dažu burtu virknīti.  
    Katram iekšējam mezglam (mezglam, kas nav lapa), 
    ir vismaz divi bērni, jo koks ir saspiests. Tajā var būt līdz pat :math:`|\Sigma|` bērnu, kur :math:`\Sigma` apzīmē ievades 
    alfabētu (ieskaitot atdalītājsimbolus, piemēram, :math:`\mathtt{\#}` un :math:`\mathtt{\$}`). 
    Iekšējās virsotnes var attēlot datora atmiņā vairākos veidos: 

    **Masīvs:** 
      Katrs mezgls ir masīvs ar pointeriem, kur katram alfabēta burtam 
      atbilst pointeris, kas ved uz leju -- uz citu mezglu vai uz lapu (pabeigtu sufiksu). Ja attiecīgais 
      burts šajā mezglā neglabājas, tad attiecīgā pointera vietā ir ``NULL``.

    **Binārais meklēšanas koks (BST):** 
      Katrā mezglā glabājas neliels balansēts meklēšanas koks ar tajā esošajiem burtiem.
      Meklēšanas gaitā vispirms atrod vajadzīgo burtu un pa atbilstošo ārējo pointeri pāriet uz nākamo mezglu. 
      (Mezgla BST kokā izmantoti "iekšējie pointeri", kuri palīdz  
      atrast vajadzīgo burtu, bet neiziet ārpus šī mezgla.)

    **Heštabula:**
      Katrs mezgls ir neliela heštabula, kurā glabājas alfabēta burtu hešffunkciju vērtības; 
      heštabula ir aizpildīta līdz 70\% no kapacitātes un konstantā laikā var atrast pointeri, kas iet uz nākamo mezglu. 

    Pieņemt, ka lietotājs meklē paraugu :math:`P` (nelielu teksta fragmentu) garā tekstā :math:`T`, kas 
    glabājas atmiņā kā sufiksu koks. 
    Aizpildīt tabulu, kurā katram no 3 minētajiem mezglu glabāšanas veidiem dota asimptotiskā izteiksme (:math:`O(f(\ldots))`)
    **vaicājuma laikam**, lai tekstā :math:`T` atrastu vienu paraugu :math:`P`.
    un arī **telpai** (cik daudz RAM atmiņas aizņem viss teksts :math:`T`). 

    Asimptotiskajās izteiksmēs izmantot parametrus :math:`|\Sigma|` -- alfabēta burtu skaits, 
    :math:`|P|` -- meklējamā parauga garums, :math:`|T|` -- noindeksētā teksta garums. 
    Atbildes jāpamato.  

    ==========================  ================  =======
    Mezgla glabāšanas veids     Vaicājuma laiks   Telpa
    ==========================  ================  =======
    Masīvs
    Binārais meklēšanas koks
    Heštabula 
    ==========================  ================  ======= 




**2. uzdevums:** 
  Aplūot lineārās programmēšanas uzdevumu: :math:`\max(2x_1 + 3x_2)`, kur 

  .. math:: 

    \left\{ 
    \begin{array}{l}
    x_1 + x_2 \leq 15 \\
    2x_1 - x_2 \geq 6 \\
    -x_1 + 4x_2 \leq 20 \\
    \end{array}
    \right.


  **(A)**
    Uzzīmēt iespējamo plaknes apgabalu (*feasible region*) plaknē, kur :math:`x_1` ir uz horizontālās 
    ass, bet :math:`x_2` ir uz vertikālās ass. 

  **(B)** 
    Ieviest papildmainīgos tā, lai visas nevienādības (izņemot prasību mainīgajiem būt nenegatīviem) 
    pārvērstos par vienādībām. Uzrakstīt iegūto lineāro programmu. 
    
  **(C)**   
    Atrisināt iegūto lineāro programmu  
    ar simpleksu metodi. Tā kā punkts :math:`(x_1,x_2) = (0,0)`
    neapmierina nevienādību sistēmu, izvēlēties par pirmo tuvinājumu punktu :math:`(x_1,x_2) = (3,0)`. 
    Katrā algoritma solī iezīmēt tabulu, kur tabulas kreisajā pusē doti *brīvie mainīgie* 
    (tie, kuru vērtības vienādas ar :math:`0`), bet labajā pusē doti *pamatmainīgie* (kuru vērtības 
    ir atšķirīgas no :math:`0`, bet vērtības nav palielināmas, nesabojājot kādu no nosacījumiem). 



.. https://medium.com/@jithmisha/solving-the-maximum-flow-problem-with-ford-fulkerson-method-3fccc2883dc7

**3. uzdevums:**
  Dots grafs, kura 6 virsotnes apzīmētas ar lielajiem burtiem: 
  :math:`V = \{ \mathtt{S}, \mathtt{A}, \mathtt{B}, \mathtt{C}, \mathtt{D}, \mathtt{T} \}` 
  (:math:`\mathtt{S}` ir izteka, :math:`\mathtt{T}` ir ieteka). 
  Grafa šķautnes ir: 

  .. math::
  
    e_1 = \mathtt{SA},\, e_2 = \mathtt{SC},\, e_3 = \mathtt{AB},\, e_4 = \mathtt{BA},\, e_5 = \mathtt{BT},\, e_6 = \mathtt{CA},\, e_7 = \mathtt{CD},\, e_8 = \mathtt{DB},\, e_9 = \mathtt{DT}
  
  un to kapacitātes ir attiecīgi: 

  .. math::

     c(\mathtt{SA})=15,\, c(\mathtt{SC})=12,\, c(\mathtt{AB})=11,\, c(\mathtt{BC})=8,\, c(\mathtt{BT})=19,\, c(\mathtt{CA})=5,\, c(\mathtt{CD})=15,\, c(\mathtt{DB})=6,\, c(\mathtt{DT})=21    


  **(A)**
    Dotajam grafam atrast maksimālo plūsmu, izmantojot Edmonda-Karpa algoritmu. Tas ir Forda-Falkersona algoritma variants, kur
    *papildinošo ceļu* (*augmented path*) atrod ar grafa apstaigāšanu BFS secībā. 

    Katram algoritma solim uzzīmēt divus grafus blakus vienu otram: 

    * Reziduālais grafs, kurā parādīts, par cik vienībām plūsmu uz šīs šķautnes var *palielināt*, nepārsniedzot kapacitāti. 
      (Pirmajā solī 
      reziduālais grafs sakrīt ar sākotnējo un nekādas plūsmas nav jāatņem.) Pievienot reziduālajam grafam arī šķautnes pretējā virzienā, kuru 
      kapacitātes sakrīt ar lielumu, par kuru plūsmu attiecīgajā šķautnē varētu *samazināt*.
      Reziduālajā grafā jāiekrāso jaunais papildinošais ceļš (ja eksistē vairāki vienāda garuma ceļi, starp tiem 
      izvēlas alfabētiski pirmo). Katra šķautne apzīmēta ar vienu skaitli -- tās reziduālo kapacitāti.
    * Blakus zīmē otru grafu, kurā plūsma jau ir izmainīta (plūsmām uz papildinošā ceļa pieskaitīta jaunā plūsma).
      Katra šķautne apzīmēta ar diviem skaitļiem :math:`f/c`, kur :math:`f` ir līdz šim atrastā plūsma, bet 
      :math:`c` ir attiecīgās šķautnes sākotnējā kapacitāte.  

    Edmonda-Karpa algoritms apstājas tad, kad kārtējā reziduālajā grafā vairs nevar atrast papildinošo ceļu (*augmenting path*)
    no :math:`S` uz :math:`T`. 
      

  **(B)** 
    Katrai no grafa šķautnēm :math:`e_i \in E` ar :math:`x_i` apzīmēta plūsma šajā šķautnē. 
    Aprakstīt maksimālās plūsmas uzdevumu kā lineāro programmu ar nevienādībām, vienādojumiem un mainīgajiem :math:`x_i`. 
    Lineārā programma nav jārisina, tikai jāuzraksta. Sanumurējiet vienādojumus un nevienādības 
    (ierobežojumi :math:`x_i \geq 0` nav jānumurē). 


  **(C)** 
    Uzrakstīt minētajai lineārajai programmai duālo lineāro programmu. Jaunie mainīgie :math:`y_j` atbilst vienādojumu/nevienādību 
    numuriem punktā (B). Arī šī lineārā programma nav jārisina, tikai jāuzraksta. 







 
