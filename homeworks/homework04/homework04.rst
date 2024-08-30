4. mājasdarbs: Sufiksu masīvi un lineārā programmēšana
=======================================================

**1. uzdevums:** 

  :math:`\mathtt{TORABORA}` ir nosaukums alu sistēmai Afganistānā. 
  Pierakstīt šim vārdam beigās dolāra simbolu (kas alfabētiski ir pirms visiem burtiem). 

  **(A)** 
    Apskatām *nesaspiestu sufiksu koku* (*suffix tree* jeb *trie*) šim 9 simbolu vārdam.
    Tas ir koks, kurā no katras virsotnes, ja apakšstringu šajā 
    vietā vēl var turpināt, iziet šķautnes; katra šķautne apzīmēta ar alfabēta simbolu  
    (*trie* datu struktūra, kas ļauj iet pa vienam burtam uz priekšu).
    No katras virsotnes izejošās šķautnes sakārtoti alfabētiski. 
    
    Uzzīmēt šo koku un uzrakstīt, cik virsotņu tajā ir. 

  **(B)** 
    Attēlot *saspiestu sufiksu koku* šim pašam vārdam.
    Atšķirībā no nesaspiesta sufiksu koka, šis koks nesatur tādas virsotnes, kurām ir tikai 
    viens bērns (jeb attiecīgo apakšstringu var turpināt tikai vienā veidā.) 
    Šķautnes saspiestajam sufiksu kokam var būt apzīmētas gan ar atsevišķiem simboliem, 
    gan arī ar garākām simbolu virknēm.  

    Uzzīmēt šo koku un uzrakstīt, cik virsotņu tajā ir. 


**2. uzdevums:** 

  Aplūkot stringu :math:`W = \mathtt{TORABORA}\mathtt{\$}_1\mathtt{LABORATORY}\mathtt{\$}_2`. 
  Atdalītājsimboli :math:`\mathtt{\$}_1, \mathtt{\$}_2` ir alfabētiski pirms visiem citiem 
  burtiem, turklāt :math:`\mathtt{\$}_1` ir pirms :math:`\mathtt{\$}_2`. 

  **(A)**
    Izveidot sufiksu masīvu šim stringam no :math:`20` simboliem. 
    Attēlot šo sufiksu masīvu kā tabulu ar četrām kolonnām (tabulu var pareizi sakārtot un 
    iekopēt no izklājlapas vai tml.): 

    * Masīva indeksu kolonna (augoša skaitļu virkne no :math:`0` līdz :math:`19`, kas sanumurē masīvā esošos elementus pēc kārtas). 
    * Sufiksa indeksa kolonna (skaitļi no :math:`0` līdz :math:`19` jauktā secībā) -- katram sufiksam norādīts, cik burtu no 
      sākotnējā stringa jānosvītro, lai iegūtu šo sufiksu. 
    * LCP (*longest common prefix*) kolonna -- tie ir dažādi veseli nenegatīvi skaitļi 
      kas parāda, cik garš ir kopīgais gabals šīs rindas sufiksam ar iepriekšējās rindas sufiksu. (Pašā pirmajā rindā 
      pieņemts rakstīt LCP vērtību :math:`0`, jo pirms šī sufiksa nekā alfabētiski agrāka nav. Tāpat LCP vērtība ir :math:`0` 
      ja šīs rindas sufikss sākas ar citu burtu nekā iepriekšējās rindas sufikss.) 
    * Pats sufikss, izmetot no :math:`W` tik daudz burtu, cik norādīts otrajā kolonnā. Tas palīdz pareizi izrēķināt citas kolonnas. 
      (Gariem tekstiem visus 
      sufiksus nav praktiski šādi izrakstīt, jo tas aizņem daudz laika un vietas.)

  **(B)**  
    Parādīt, kā šo sufiksu masīvu var izmantot, lai atrastu vārdu :math:`\mathtt{TORABORA}` un 
    :math:`\mathtt{LABORATORY}` garāko kopīgo apakšstringu, izmantojot slīdošā loga algoritmu.
    Sk. `Youtube. William Fisset: Longest common substring problem <https://youtu.be/DTLjHSToxmo?si=UDHJ0O74byKS_6QJ>`_. 
    Uzrakstīt šī algoritma pseidokodu (tieši 2 stringu gadījumam, ko atdala :math:`\mathtt{\$}_1` un :math:`\mathtt{\$}_2`) 
    un atrast tā laika sarežģītību 
    atkarībā no ievades vārda garuma :math:`|W| = n`. 

  **(C)**
    Izmantot sufiksu masīvu, lai atrastu stringam :math:`W` tā Berouza-Vīlera pārveidojumu 
    (sk. 4. lekciju). 
   

**3. uzdevums:** 

  Apskatām lineāro programmu: Maksimizēt :math:`5x_1 + 7x_2 + 6x_3` pie nosacījumiem

  .. math::

    \left\{ \begin{array}{l}
    6x_1 + 5x_2 + 8x_3 \leq 16,\\
    10x_1 + 20x_2 + 10x_3 \leq 35,\\
    x_1 \geq 0,\;\; x_2 \geq 0,\;\; x_3 \geq 0,\\
    \end{array} \right.

  **(A)**
    Atrisināt šo lineāro programmu, izmantojot simpleksa metodes tabulas.
    Sākt ar tuvinājumu :math:`(x_1,x_2,x_3) = (0,0,0)`, katrā solī nākamo tuvinājumu var
    izvēlēties jekburā veidā, ja tas palielina mērķa funkcijas vērtību. 

  **(B)** 
    Uzrakstīt šai lineārajai programmai duālo programmu (ar diviem mainīgajiem :math:`y_1,y_2` un trim 
    nevienādībām) un atrisināt to 
    ar kādu bibliotēku (piemēram, Python ``linprog`` no ``scipy.optimize``). 
    Ja šai bibliotēkai labāk patīk lineāras programmas standartformātā (maksimizēt nevis minimizēt, vai 
    nevienādības uz otru pusi), varat pārveidot šo duālo lineāro programmu nepieciešamajā formātā, 
    pārmainot mainīgajiem zīmes vai ieviešot nokares (*slack*) mainīgos. 

  **(C)** 
    Iedomāsimies, ka primārajā uzdevumā :math:`X_1,X_2,X_3` ir trīs izstrādājumi, ko var pārdot attiecīgi par cenām
    :math:`5`, :math:`7`, un :math:`6` EUR. Tiem nepieciešamas divas izejvielas :math:`A` un :math:`B`, kuru 
    esošie krājumi ir attiecīgi :math:`16` un :math:`35` kilogrami. Zināms arī, ka pirmā izstrādājuma :math:`X_1` izgatavošanai 
    vajag :math:`6` vienības ar izejvielu :math:`A` un :math:`10` vienības ar izejvielu :math:`B`; 
    izstrādājumam :math:`X_2` vajag attiecīgi :math:`5` un :math:`20` (un tā tālāk -- 
    kā ierakstīts primārā uzdevuma matricā). 

    Primārā uzdevuma atrisinājums :math:`x_1,x_2,x_3` pasaka, cik vienības ar katru izstrādājumu :math:`X_1,X_2,X_3`
    jāražo, lai visu saražoto varētu iespējami dārgāk pārdot.

    Duālā uzdevuma atrisinājums :math:`y_1,y_2` parāda "ēnu cenas" jeb "shadow prices" (t.i. nevis reālās cenas, 
    bet konkrētajai izejvielai ekonomiski pamatotu iepirkuma cenu) -- piemēram :math:`y_1` parāda lielāko cenu (EUR/kg), cik 
    uzņēmums būtu gatavs maksāt par izejvielu :math:`A`, lai varētu palielināt ieņēmumus nedaudz virs 
    maksimālās summas :math:`5x_1 + 7x_2 + 6x_3`, ko pašlaik atļauj primārā uzdevuma atbilde. 

    * Atrast, kurai no izejvielām :math:`A` vai :math:`B` ir lielāka "ēnu cena" -- kuras izejvielas krājuma 
      palielināšana straujāk paaugstinātu mūsu ieņēmumus.
    * Pieņemsim, ka uzņēmums var palielināt šīs vērtīgākās izejvielas krājumu (otru atstājot nemainīgu). 
      Cik daudz šīs izejvielas jāiegādājas, lai duālās problēmas atrisinājums aizlēktu uz citu stūri un 
      attiecīgās izejvielas "ēnu cena" izmainītos?


**4. uzdevums:** 

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

    \begin{array}{c}
    \text{Maksimizēt}\;\sum x_{ij},\;\text{kur} \\
    \left\{ \begin{array}{l}
    \sum_{j \in [1;n]} x_{ij} \leq 1,\;\text{katram $i$}\\
    \sum_{i \in [1;n]} x_{ij} \leq 1,\;\text{katram $j$}\\
    x_{ij} \leq 1,\;\text{katriem $i,j$}\\
    x_{ij} \geq 0,\;\text{katriem $i,j$}\\
    \end{array} \right.
    \end{array}


  Pierādīt, ka šīs lineārās programmas atrisinājums reālos skaitļos (kas sasniedz, piemēram, summu :math:`S`), 
  ir vienlaikus arī atrisinājums veselos skaitļos -- to pašu maksimumu var sasniegt arī prasot, 
  lai visi :math:`x_{ij}` būtu veseli skaitļi no :math:`\{ 0, 1 \}`. 
    
