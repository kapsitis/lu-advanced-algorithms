Skaitļošanas uzdevumi
=========================

**1. uzdevums:** 
  Izveidot datorprogrammu plaši pazīstamā programmēšanas valodā 
  (piemēram, C++, Python vai Java), lai veiktu aprakstītos pārveidojumus 
  un iegūtu skaitliskas vērtības JSON failiņam, kas programmai jāatgriež.

  Teksta dokuments šim vingrinājumam ir dzejoļu krājums `<https://bit.ly/3VISbSd>`_ 
  (89022 baitus garš fails, kas satur ASCII simbolus un arī 
  ar UTF-8 kodētus Unikoda simbolus latviešu burtiem ar diakritiskajām zīmītēm). 

  **(A)** 
    Noskaidrot alfabēta izmēru (pēc faila nolasīšanas UTF-8 kodējumā), 
    kurā pierakstīts šis krājums. Tajā visticamāk ietilpst 33+33 
    lielie un mazie burti latviešu alfabētā kā arī dažādas pieturzīmes un atstarpju simboli. 
    Aprēķināt "entropy1" - entropiju šim krājumam, ja katra simbola 
    varbūtība sakrīt ar šī simbola relatīvo biežumu krājumā.
    Noapaļot šo entropiju, iegūstot skaitli ar 4 cipariem aiz komata.
    Atrast, cik dziļš būtu Hafmana koks (attālums no koka saknes līdz visdziļākajai 
    lapai - jeb visgarākā bitu virknīte, kas iekodē vienu alfabēta burtu). 
    Un arī noskaidrot, cik garš būtu šī dzejoļu krājuma kodējums ar Hafmana koku baitos. 
    (Pašu koku nepārraidām, uzskatām, ka sūtītājs un saņēmējs burtu biežumus jau zina.)

  **(B)** 
    Aplūkot šo krājumu, ja tas pierakstīts alfabētā, ko veido burtu pārīši.
    (Dokuments sākas ar šiem burtu pārīšiem: ``["Tā", "lu", " c", "eļ", "u ", "vē", "jš"]``). 
    Arī šim alfabētam saskaitīt, cik pavisam ir simbolu un 
    kāda ir "entropy2" - entropija, ko veido ziņojumi, kas ir burtu pārīši. 
  
  **(C)** 
    Saspiest dokumentu ar Python "gzip" vai līdzīgu bibliotēku vai komandrindas
    utilītprogrammu. 
    ("gzip" izmanto "deflate" algoritmu, kas ir LZ77 un Hafmana 
    koda kombinācija). Atrast saspiestā arhīva garumu baitos. Vai šādi saspiests 
    dokuments ir mazāks par to, ko var iegūt ar Hafmana koku atsevišķiem simboliem 
    vai 2 simbolu pāriem?

  Jūsu datorprogramma saņem komandrindas ievadē ceļu uz failu (dzejoļu krājumu)
  un izvada JSON ar sekojošu struktūru:

  .. code-block:: javascript

    {
      "alphabet1_size": <positive-integer>, 
      "entropy1": <round to 4 decimal places as with "%.4f">,
      "huffman1_depth": <positive-integer>, 
      "huffman1_encoded_bytes": <positive-integer>,      
      "alphabet2_size": <positive-integer>, 
      "entropy2": <round to 4 decimal places as with "%.4f">,
      "huffman2_depth": <positive-integer>, 
      "huffman2_encoded_bytes": <positive-integer>
      "gzip_bytes": <positive-integer>
    }


**2. uzdevums:** 
  
  **(A)** 
    Šekspīra sonetu krājumam `<https://www.gutenberg.org/cache/epub/1041/pg1041.txt>`_ 
    veikt atstarpju normalizāciju: 
    Pārveidot to par simbolu virknīti, kurā ir tikai mazie latīņu burti, 
    defise (-), apostrofs un tukšums. 
    Citas pieturzīmes un rindu pārnesumus pārveidot par tukšumiem. Lielos burtus pārveidot par 
    mazajiem burtiem. Vairākus pēc kārtas sekojošus tukšumus pārveidot par 
    vienu tukšumu. No faila noņemt ievaddaļu un beigas, atstāt tikai sonetus
    un to numurus, krājuma beigās pievienot dolāra simbolu. 
    Iegūtais teksts izskatās kā viena gara rinda:

    .. code-block:: text

      i from fairest creatures ... water cools not love$

    Alfabētiskais sakārtojums visiem simboliem ir tāds pats kā ASCII alfabētā, 
    izņemot dolāru, ko uzskatām par alfabētiski pašu pirmo.

  **(B)**
    Izveidot no iegūtā (atstarpju normalizētā) teksta sufiksu masīvu 
    un Berouza-Vīlera transformāciju. Berouza-Vīlera transformācijas rezultātam 
    lietot Move-to-Front kodējumu un iegūt skaitļu virknīti, kurā skaitļus 
    atdala ar komatiem. Saskaitīt, cik Move-to-Front kodējumā ir nuļļu 
    (visu to vietu, kur Berouza-Vīlera transformācijā tas pats burts 
    atkārtojās - un tā atkārtojumus varēja nokodēt ar "0"). 
    Saspiest Move-to-Front skaitļu virknīti, izmantojot "gzip" algoritmu. 

  **(C)** 
    Saspiest Šekspīra sonetus (tukšumu normalizēto virkni), izmantojot 
    "bzip2" bibliotēku vai komandrindas utilītprogrammu. 
    Vai "bzip2" rezultāts ir īsāks nekā iepriekšējos soļos iegūtais Berouza-Vīlera 
    saspiešanas rezultāts?


  Jūsu datorprogramma saņem komandrindas ievadē ceļu uz failu (dzejoļu krājumu)
  un izvada JSON ar sekojošu struktūru:

  .. code-block:: javascript 

    {
      "mtf-zeroes": <positive-integer>, 
      "compressed_mtf_bytes": <positive-integer>
      "bzip2_bytes": <positive-integer>
    }

**3.uzdevums:** 
  Skaņu un attēlu saspiešanā bieži izmanto dažādas trigonometriskās 
  transformācijas (Ātro Furjē transformāciju, Diskrēto kosinusu 
  transformāciju u.c.). 
  Lai ilustrētu to, kā tās palīdz ātri iegūt tuvinātus rezultātus, 
  aplūkojam šādu kombinatorikas uzdevumu par plusiem un mīnusiem: 

  > Izrakstīti visi naturāli skaitļi no $1$ līdz $n$ augošā secībā. 
  > Cik dažādos veidos var pirms katra no šiem skaitļiem ierakstīt "+" un "-" zīmes tā, 
  > lai visu skaitļu summa būtu $0$. 

  "Plus-mīnus uzdevumam" eksistē kaut viens atrisinājums  
  tikai tad, ja summa :math:`1 + 2 + \ldots + n` ir pāra skaitlis 
  (jeb  :math:`n` pieņem vērtības :math:`3, 4, 7, 8, 11, 12, 15, 16, \ldots`). 
  Efektīvs saskaitīšanas veids būtu, piemēram, dinamiskā programmēšana, kur veidojam 
  tabulu :math:`a_{n,k}` (kur :math:`n` ir uzdevumā doto skaitļu skaits, bet 
  :math:`k` pieņem visas vērtības starp :math:`-n(n+1)/2` un :math:`n(n+1)/2`). 
  Un var saskaitīt, cik dažādos veidos summa :math:`\pm 1 \pm 2 \pm \ldots \pm n`
  var pieņemt vērtību tieši :math:`k`.
  Diemžēl, dinamiskās programmēšanas algoritms ir lēns - tam nepieciešamais laiks 
  ir :math:`O(n^4)`. 

  Ātrāku algoritmu var iegūt, izrēķinot ģenerējošo funkciju: 

  .. math:: 

    \left( x^{-1} + x^1 \right) \left( x^{-2} + x^{2} \right) \ldots \left( x^{-n} + x^n \right)

  Veidi, kā katrā no iekavām var izvēlēties kādu no saskaitāmajiem augšminētajā 
  izteiksmē, sakrīt ar veidu skaitu, kā var atrisināt "plus-mīnus uzdevumu".
  Atrisinājums būs koeficients pie pakāpes :math:`x^0`. 

  Ja mums nepatīk negatīvas pakāpes, varam katru no iekavām piereizināt ar 
  :math:`x` pakāpi (pirmo iekavu ar :math:`x^1`, 
  otro iekavu ar :math:`x^2`, utt.). Iegūstam izteiksmi: 

  .. math::

    \left( 1 + x^2 \right) \left( 1 + x^4 \right) \ldots \left( 1 + x^{2n} \right).

  Plus-mīnus uzdevuma atrisinājums būs koeficients pie pakāpes :math:`\frac{n(n+1)}{2}`
  šajā izteiksmē (ja tāds vispār eksistē). 

  **(A)** 
    Izmantot Numpy FFT (Ātro Furjē transformāciju) vai līdzīgu bibliotēku, lai 
    efektīvi atrisinātu "plus-mīnus" uzdevumu vērtībām :math:`n=1,2,\ldots,100`
    (naturālajiem skaitļiem līdz 100). 

  Jūsu programma nesaņem ievadi, bet izdrukā šādu JSON failu (masīvu ar 100 elementiem): 

  .. code-block:: javascript 

    {
      "plus_minus": [[1,0], [2,0], [3,2], [4,2], [5,0], [6,0], [7,8], [8,14] ... ] 
    }

  Katrs pārītis šajā masīvā :math:`(n,N)` parāda skaitli :math:`N`, kas 
  ir "plusu-mīnusu" uzdevuma atrisinājums vērtībai :math:`n`. 


**4.uzdevums:** 
  Aplūkojam sekojošu spēli: Divi spēlētāji vienlaikus nosauc katrs 
  vienu naturālu skaitli no 1 līdz 10. 
  
    1. Ja abi skaitļi ir vienādi, tad ir neizšķirts (neviens nevienam neko nemaksā)
    2. Ja pirmā spēlētāja skaitlis :math:`a` ir lielāks par otra spēlētāja 
       skaitli :math:`b`, bet nepārsniedz to trīskārt (:math:`b < a < 3b`), 
       tad pirmais spēlētājs saņem no otrā 1 EUR. 
    3. Ja pirmā spēlētāja skaitlis :math:`a` vismaz trīskārt pārsniedz otrā 
       spēlētāja skaitli :math:`b` (:math:`a \geq 3b`), 
       tad pirmais spēlētājs maksā otrajam 2 EUR. 

  Izmantojot 11.lekcijā minētos paņēmienus vai jebkuru citu pieeju, 
  sastādīt lineāru programmu, kas ļautu atrast pirmajam spēlētājam 
  optimālu stratēģiju (identiska stratēģija der arī otrajam spēlētājam). 

  Jūsu datorprogramma saņem komandrindas ievadē matricu :math:`10 \times 10` 
  matricu (tie 100 skaitļi, kas apraksta 1.spēlētāja ieguvumu - tātad vērtības 
  -2,-1,0,1,2) un izvadē atgriež JSON ar sekojošu struktūru: 

  .. code-block:: javascript

    {
      "optimal_strategy": [<round to 4 decimal places>, ...] 
    }

  Šajā masīvā ir 10 skaitļi - visu 10 iespējamo gājienu optimālās varbūtības 
  noapaļotas līdz 4 cipariem aiz komata.


**5.uzdevums:** 
  Šekspīra sonetu krājumam `<https://www.gutenberg.org/cache/epub/1041/pg1041.txt>`_ 
  veikt atstarpju normalizāciju (tas pats, kas 2.uzdevuma (A)). 

  **(A)** 
    Iegūtajam garajam stringam (kas satur mazos latīņu burtus, 
    mīnusu, apostrofu un tukšumu) pielieto ripojošās hešfunkcijas: 

    .. math:: 
  
      \text{hash}_p(s) = (c_1 \times p^{9} + c_2 \times p^{8} + 
      \ldots + c_{10} \times p^0) \mod m

    Katra funkcija saņem ievadi - 10 burtus un rēķina polinomu, 
    kur polinoma mainīgais ir :math:`p=31, 37, 41, 43, 47, \ldots` (kāds 
    neliels pirmskaitlis, sākot ar :math:`31`), un modulis ir     
    :math:`m=2^{31} - 1`. 
    Pavisam izmantosim :math:`k` pirmskaitļi :math:`p` un tātad arī 
    :math:`k` dažādas hešfunkcijas.

  **(B)**
    Zināms, ka Blūma filtra izmērs ir tieši 1000000 (viens miljons) 
    bitu. Tajā glabāsim visus 10-burtu apakšstringus (10 secīgu burtu virknītes) 
    no Šekspīra sonetiem (un sonetu fails ir atstarpju normalizēts). Šāds 
    Blūma filtrs palīdz dzejas portālam izvairīties no plaģiāta mēģinājumiem, ja kāds 
    iesūtīs Šekspīra sonetiem līdzīgus dzejoļus. 

    Atrast optimālo hešfunkciju skaitu :math:`k`, lai Blūma filtrā 
    būtu iespējami maz aplamo pozitīvo (tādu 10 burtu virknīšu, kuru Šekspīra 
    oriģinālā nav, bet Blūma filtrs uzskata, ka tās ir atrodamas). 
    (Ja :math:`k` vērtība ir pārāk maza, tad ir iespējamas hešfunkciju nejaušas 
    kolīzijas un biežas kļūdas šādu sakritību dēļ. Ja :math:`k` vērtība ir pārāk 
    liela, tad Blūma filtrs aizpildās ar vieniniekiem - un arī šajā gadījumā 
    bieži nepareizi uzskatīsim, ka ir atrasta jau Šekspīra oriģinālā redzama virknīte.)

  
  Jūsu programma saņem ievadē Šekspīra sonetu failu, 
  bet izdrukā šādu JSON failu (masīvu ar 20 elementiem): 

  .. code-block:: javascript

    {
      "plus_minus": [[1,<round to 4 decimal places>], 
      [2,<round to 4 decimal places>], ...,  [20, <round to 4 decimal places>]] 
    }

  Katrs pārītis :math:`[k, p]` masīvā parāda varbūtību :math:`p` atrast aplamās pozitīvās kļūdas. 
  Mazākajai :math:`p` varbūtībai atbilst optimālais hešfunkciju skaits :math:`k`. 














