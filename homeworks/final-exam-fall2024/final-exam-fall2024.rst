Galaeksāmens, 2025-01-06
==========================

Galaeksāmena vērtējums ir 30 procentpunkti.

**1. uzdevums:**
  
  Dots automāts ar trim stāvokļiem :math:`\mathtt{A}`, :math:`\mathtt{B}` un :math:`\mathtt{C}`. 
  Katrai pārejai starp stāvokļiem ir noteikta varbūtība kā redzams attēlā.

  .. figure:: figs/automaton.png
     :width: 1.5in

  Šis automāts ģenerē ziņojumus no kopas :math:`S`, kas sastāv no  
  burtu pāriem :math:`AA`, :math:`AB`, :math:`AC`, :math:`BA` utt. 
  Ja, piemēram, automāts, pārvietojoties ar aprakstītajām 
  varbūtībām, apmeklēja sešus stāvokļus secībā :math:`\mathtt{AABCAB}`, 
  tad radās trīs ziņojumi: :math:`\mathtt{AA}`, :math:`\mathtt{BC}` un 
  :math:`\mathtt{AB}`.

  Atrast ziņojumu kopas entropiju :math:`H(S)` un pamatot šo aprēķinu. 


**2. uzdevums:** 
  Dots strings :math:`w`, kas sastāv no 9 ASCII simboliem, kas sakārtoti pēc Latīņu 
  alfabēta (dolārs ir alfabētiski pirms visiem burtiem). Pēc iekodēšanas 
  ar Berouza-Vīlera algoritmu tika iegūts šāds Berouza-Vīlera transformācijas rezultāts:

  .. math::

    \mathtt{N\$IIPBEZE}

  Atkodēt Berouza-Vīlera transformāciju un atrast, kāds ir sākotnējais strings :math:`w`. 
  Parādīt apgrieztās transformācijas iegūšanas secību. 

**3. uzdevums:** 
  Kādā zemē izmanto domino kauliņus, kas sastāv no :math:`k=3` kvadrātiņiem, uz katra 
  kvadrātiņa var būt uzzīmēts skaitlis no :math:`0` līdz :math:`6` ieskaitot. 
  Piemēram, attēlā redzamais kauliņš ir izsakāms ar :math:`3` skaitļu virknīti 
  :math:`(m_0, m_1, m_2) = (2,0,1)`:

  .. figure:: figs/domino.png
     :width: 1in 

  Lai nosūtītu informāciju par vienu domino kauliņu, tur izmanto Rīda-Solomona kodu: 
  aprēķina sekojošas polinoma vērtības: 
  
  .. math:: 

     p(a) = \sum_{i=0}^{k-1} m_i a^{(k-1)-i} \pmod {7},\;\;\mbox{kur $a = 0,1,\ldots,n-1$}.

  Visas iegūtās :math:`n` vērtības :math:`p(0), \ldots, p(n-1)` 
  tiek nosūtītas saņēmējam pa trokšņainu sakaru kanālu; saņēmējs 
  vēlas atkodēt nosūtītā domino kauliņa lauciņu vērtības jeb skaitļus :math:`m_i`.

  **(A)** 
    Kādam mazākajam :math:`n` saņēmējs vienmēr varēs pareizi atkodēt domino kauliņu, 
    ja sakaru kanāls drīkst sabojāt (t.i. aizstāt ar nepareizām vērtībām) 
    ne vairāk kā :math:`2` no :math:`n` nosūtītajām vērtībām. 

  **(B)** 
    Izrēķināt visas :math:`n` vērtības (bez kļūdām), kuras jāsagatavo nosūtītājam, 
    ja domino kauliņš ir jau minētais :math:`(2,0,1)`. 


**4. uzdevums:** 
  Rūpnīcā ir neapmācītie strādnieki, kuru darba samaksa ir 270 EUR nedēļā un 
  apmācītie strādnieki, kam darba samaksa ir 540 EUR nedēļā. 
  Rūpnīcai ir svarīgi, lai nedēļas darba samaksa visiem 
  strādniekiem kopā nepārsniegtu 48600 EUR. 

  Rūpnīcas darbam nepieciešami vismaz 110 darbinieki, 
  no kuriem vismaz 40 jābūt apmācītiem. 
  Arodbiedrību noteikumi prasa, lai apmācīto darbinieku 
  skaits būtu vismaz puse no neapmācīto darbinieku skaita. 

  Ar :math:`x_1` apzīmējam neapmācīto darbinieku 
  skaitu, ar :math:`x_2` apzīmējam apmācīto darbinieku skaitu. 

  **(A)**
    Uzrakstīt lineāro programmu, kas apraksta visus ierobežojumus, 
    kas jāapmierina mainīgajiem :math:`x_1,x_2` un izmanto iespējami mazu kopīgo darba samaksu.
    (Lineārā programma nav jārisina tikai pareizi jāpieraksta 
    visas sakarības.)

  **(B)** 
    Uzrakstīt duālo lineāro programmu mainīgajiem :math:`y_i`. 
    Izvēlēties kādu no mainīgajiem :math:`y_i` un aprakstīt 
    cilvēku valodā, ko saturīgi izsaka :math:`y_i` optimālā 
    vērtība duālās lineārās programmas atrisinājumā.
    (Arī duālā programma nav jārisina; tikai pareizi jāpieraksta visas 
    sakarības.)
  

**5. uzdevums:** 
  Aplūkojam parauga :math:`P = \mathtt{ABAC}` meklēšanu tekstā 
  :math:`T = \mathtt{CABABABACABAC}` ar Knuta-Morisa-Prata algoritmu. 

  **(A)**
    Atrast prefiksu funkciju paraugam :math:`P`; visas tās vērtības :math:`\pi(i)`
    attēlot tabulā. 

  **(B)** 
    Zīmēt meklējamo paraugu zem teksta visām tām nobīdēm, kurām 
    to pārbauda KMP algoritms. Vizuāli izlīdzināt tekstu un nobīdīto paraugu 
    rūtiņu lapā tā, lai vienmēr burts tekstā un burts paraugā, 
    kurus savstarpēji salīdzina, atrastos tieši 
    viens zem otra.     
    Saskaitīt, cik burtu salīdzināšanas jāveic, 
    līdzkamēr algoritms atrod visas parauga atrašanās vietas tekstā. š



 
