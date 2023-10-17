1. mājasdarbs: Bezzudumu saspiešana
====================================

**1. uzdevums:** 

  Teksts sastāv no tukšuma simbola `' '` (kurš alfabētiskajā sakārtojumā ir pirmais) 
  un vēl :math:`7` citiem simboliem: 
  `A`, `C`, `E`, `I` , `N` ,`S`, `T`. Simbolu biežumi doti tabulā: 

  ======  ====  ====  ====  ====  ====  ====  ====  
  `' '`   `A`   `C`   `E`   `I`   `N`   `S`   `T`
  ======  ====  ====  ====  ====  ====  ====  ====  
  18%     10%   8%    23%   4%    6%    19%   12%
  ======  ====  ====  ====  ====  ====  ====  ====  
 
  **(A)** 
    Izveidot vienalga kādu Hafmana koku šim alfabētam un tā varbūtību sadalījumam.

  **(B)** 
    Pārveidot Hafmana koku kanoniskajā formā. 
    Sk. `<https://en.wikipedia.org/wiki/Canonical_Huffman_code>`_. 

  **(C)** 
    Izmantot Hafmana koku, lai iekodētu simbolu virknīti: `"CATS SENSE NICE TEAS"`

    Tajā ir :math:`20` simboli, ieskaitot tukšumus (pēdiņas nepieder virknītei un nav jākodē). 



**2. uzdevums:** 

  Doti simboli :math:`\{ \mathtt{N}, \mathtt{S}, \mathtt{U}, \mathtt{\$} \}` (šeit 
  :math:`\mathtt{\$}` apzīmē ziņojumu virknes beigas `EOF` un ir arī alfabētiski pēdējais) 
  ar varbūtībām attiecīgi :math:`(0.2, 0.4, 0.3, 0.1)`. 
  
  **(A)** 
    Atrast reālo skaitļu nogriezni :math:`[a;b) \subseteq [0;1]`, kas atbilst 
    ziņojumu virknei :math:`\mathtt{SUNS\$}`
  
  **(B)** 
    Atrast mazāko :math:`k` vērtību, kurai atrodas :math:`i`, kas apmierina sakarību 
    :math:`\left[ \frac{i}{2^k}; \frac{i+1}{2^k} \right) \subseteq [a; b)`. 

    Pierakstīt skaitli :math:`i` ar tieši :math:`k` bitiem, lai iegūtu 
    virknes :math:`\mathtt{SUNS\$}` *aritmētisko kodu*. 

  **(C)**
    Atrast, kāda ziņojumu virkne (vai virknes) tiktu atkodētas ar šo aritmētisko 
    kodu, ja ieejā bitu virkne ir bināri pierakstīta :math:`1/3` jeb 
    bezgalīga periodiska virkne ar periodu "01": 

    .. math::

      \mathtt{01010101010101010101010101010101}\ldots

    Ja ziņojumu virknē atkodējas vairāk nekā :math:`20` simboli, tad pietiek 
    atbildē norādīt pirmos :math:`20` no tiem. 


**3. uzdevums:** 

  Ar LZ78 algoritmu kodēt tekstu "POTATO TOMATO GO TO TORONTO". 
  Arī tukšums pieder ziņojumu alfabētam (bet pēdiņas nepieder). 

**4. uzdevums:** 

  **(A)**
    Veikt Berouza-Vīlera transformāciju simbolu virknei 
    :math:`\mathtt{POTATOTOMATO\$}` (var uzskatīt, ka beigu simbols :math:`\$` ir 
    alfabētiskajā secībā aiz visiem burtiem). 

  **(B)** 
    Izmantot "move-to-front" un "run-length encoding", lai iekodētu iepriekšējā 
    solī iegūto transformācijas rezultātu.

**Brīvprātīgi vingrinājumi un skaitļošanas eksperimenti**

Izpildīts vingrinājums (programma, dati, apraksts un ieskaitīšana konsultācijā) 
var aizstāt semestra vidus eksāmenu -- līdz 30% no atzīmes.  
Var piedāvāt arī savu tēmu, saskaņojot ar pasniedzēju.
Šeit dažas idejas par entropiju un saspiešanu (1.-4. nodarbība). 

**1. vingrinājums (Wordle):** 
  Videoblogs 3brown1blue satur `Video1 <https://youtu.be/v68zYyaEmEA?si=Eoc_cKs0Qn-XqqdL>`_ 
  un `Video2 <https://youtu.be/fRed0Xmc2Wg?si=pJe4vIZwscwhN3si>`_ par labāko "Wordle" 
  sākumvārdu. Šajā vingrinājumā var līdzīgi izvest vārdu, ar kuru labāk sākt "Wordle" latviski -- 
  sk. `<https://vardulis.lv/>`_, `<https://wordle.lielakeda.lv/>`_, 
  `<https://wordle.global/lv>`_. Ieteicamie soļi: 

  * Iegūt vārdnīcu (Tezaurs) ar vārdiem fiksētā garumā (5 vai varbūt 4, 6, 7, 8). 
  * Katram no atverošajiem vārdiem atrast iespējamos krāsojumus (un to varbūtības). 
  * Atrast vārdu (vai vārdus), kas pirmajā solī sasniedz vislielāko entropiju.
  * Pēc vajadzības, katrai no atbildēm uz pirmo vārdu, piedāvāt otro vārdu ar vislielāko entropiju. 

**2. vingrinājums (Divkāršā iekodēšana):** 
  Pieņemsim, ka angļu valodas teksts satur 26 burtus
  un tukšumus. Kāds to iekodējis, izmantojot Morzes kodu (iegūstot virkni ar "1" - pīkstieniem 
  un "0" - klusumiem). Piemēram, vārdu "PARIS" kodētu šādi: 

  .. figure:: figs/morse-sample.png
    :width: 4in

  Šajā uzdevumā Jūs salīdzināt saspiešanu tieši no angļu valodas teksta ar 26+1 simboliem un 
  saspiešanu no tā paša teksta Morzes koda. Mērķis ir atrast to saspiešanas metodi, kura 
  dod labu rezultātu neatkarīgi no ievades reprezentācijas veida.
  Salīdzināšanai var izmantot Python pakas (var instalēt ar Conda vai pip): 
  `zlib` un/vai `gzip` (LZ77 - Lempela Ziva algoritms), `bz2` (Berouza-Vīlera algoritms), 
  `lzma` ("range encoding" kas ir aritmētiskā koda variants). 

  Katram no saspiešanas algoritmiem (aritmētiskajam, LZ77, BW) iekodēt un atkodēt pietiekami 
  garu angļu tekstu (nepārveidotu) un to pašu tekstu (jau iekodētu ar Morzes kodu). 
  Kurai saspiešanas metodei pārkodēšana caur Morzes kodu 
  vismazāk pasliktina galarezultātu? Apkopot rezultātus tabulā - pavisam 6 mērījumi: 
  katrai no 3 saspiešanas metodēm tiek iegūti divi skaitļi.

**3. vingrinājums:** 
  Izveidot Python programmu, kas veic bijektīvo variantu 
  `Berouza-Vīlera transformācijai 
  <https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform#Bijective_variant>`_. 
  Ievades un izvades alfabēts var būt drukas simboli, ko izmanto Markdown tekstos. 
  Izmantot šo transformāciju, lai bijektīvi attēlotu garāku Markdown tekstu, 
  piemēram, O.Vācieša dzejoļu krājumu `Tālu ceļu vējš 
  <https://raw.githubusercontent.com/kapsitis/ddgatve-poetry/master/source-rst/talu-celu-vejs.rst>`_.

**4. vingrinājums (AES128 laušana ar DCA):** 
  "Baltā kaste" ir tāds kriptogrāfijas modelis, kurā uzbrucējs var lasīt 
  mašīnas izpildes laika atmiņu vai mainīt to (memory faults), 
  debugot programmas, utml. Jautājums -- vai šādā modelī ir iespējams nodarboties 
  ar kriptogrāfiju (iekodējot un atkodējot kriptotekstu) tā, lai neatklātu uzbrucējam 
  atslēgu -- un viņam/viņai nebūtu viegli nozagt šo algoritmu, lai to darbinātu citur.
  "Baltās kastes" modeli reizēm izmanto DRM - ar autortiesībām saistītu darbu 
  izplatīšanā: Lietotājam ļauj atšifrēt datu plūsmu tikai tad, ja to dara
  autentificēts lietotājs, izmantojot atļautu ierīci un programmatūru. 

  * Iepazīties ar `DCA Hiding your White-Box Designs is Not Enough <https://eprint.iacr.org/2015/753.pdf>`_ -- 
    rakstu par to, kā novērojot korelācijas starp teksta ievadi un AES128 kriptoalgoritma 
    pirmās iterācijas (round) rezultātu var uzminēt kriptoatslēgas bitus. 
  * Darbināt kādu no 
    `Side-Channel Marvels <https://github.com/SideChannelMarvels/Deadpool/blob/master/README_dca.md>`_ 
    uzbrukumiem, lai atminētu agrāko gadu kriptogrāfijas konferencēs piedāvātos "challenges". 

  