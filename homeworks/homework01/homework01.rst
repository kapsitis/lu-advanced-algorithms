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

  Ar LZW algoritmu kodēt tekstu "POTATO TOMATO GO TO TORONTO". 
  Arī tukšums pieder ziņojumu alfabētam (bet pēdiņas nepieder). 

**4. uzdevums:** 

  **(A)**
    Veikt Berouza-Vīlera transformāciju simbolu virknei 
    :math:`\mathtt{POTATOTOMATO\$}` (var uzskatīt, ka beigu simbols :math:`\$` ir 
    alfabētiskajā secībā aiz visiem burtiem). 

  **(B)** 
    Izmantot "move-to-front" un "run-length encoding", lai iekodētu iepriekšējā 
    solī iegūto transformācijas rezultātu.

**Priekšnesumu tēmas**

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


**2. vingrinājums:** 
  Izveidot Python programmu, kas veic bijektīvo variantu 
  `Berouza-Vīlera transformācijai 
  <https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform#Bijective_variant>`_. 
  Ievades un izvades alfabēts var būt drukas simboli, ko izmanto Markdown tekstos. 
  Izmantot šo transformāciju, lai bijektīvi attēlotu garāku Markdown tekstu, 
  piemēram, O.Vācieša dzejoļu krājumu `Tālu ceļu vējš 
  <https://raw.githubusercontent.com/kapsitis/ddgatve-poetry/master/source-rst/talu-celu-vejs.rst>`_.

  