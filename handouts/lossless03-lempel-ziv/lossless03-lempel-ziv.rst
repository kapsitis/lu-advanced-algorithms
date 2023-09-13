3. Bezzudumu saspiešana: Lempela-Ziva algoritms
=================================================

1. Sarežģītības apsvērumi (cik reizes lasa ievadi?)
2. Lietot un analizēt Lempela-Ziva LZ77 algoritmu.
3. Saprast un lietot Lempela-Ziva LZ78 algoritmu un tā variantus.
4. Lempela Ziva algoritmu praktiski lietojumi.

Motivācija saspiešanai ar vārdnīcas algoritmiem:

* Datu saspiešanas metode nevar būt labāka par entropiju, ja simboli ir neatkarīgi.
* Reālos datos nākošais simbols atkarīgs no iepriekšējā.
* Var veidot N-grammas (2 burtu virknes kā jaunus "simbolus": aa, ab, ac, ad, ...). Tam pielieto Hafmana vai aritmētisko kodu).
* Var arī izmantojot to, ka ir simbolu virknes, kas atkārtojas (kodus veido tikai reāli esošajām). Ievieš jaunus simbolus priekš šādām virknēm; 
  tās arī ir Lempela-Ziva metodes (LZ77 vai LZ78).



Ne vienmēr burti saspiešanas algoritma ievadē ir 
neatkarīgi un vienādi sadalīti (kā tas ir entropijas koda gadījumā). 

Jau aritmētiskais kods labi atbalsta tādas gadījumlielumu 
virknes, kurām ir "atmiņa" -- tās atceras iepriekšējo burtu.  
Markova ķēde, ko ģenerē automāts ar :math:`3` stāvokļiem:

.. figure:: figs/markov-chain.png
   :width: 3in

   Markova ķēde

:math:`18` burtu virknīte, sākot ar :math:`A`: `ABCABCBCAAABCABBAB`

.. note:: 
   Var ģenerēt pastaigu pa automātu.
   
   ```r
   sample(1:4,size=17, replace=TRUE)  
   [1] 3 3 1 2 3 4 3 2 1 1 4 4 2 3 2 1 4 
   ```

   * `LZW algoritma piemērs 
     <http://web.mit.edu/6.02/www/f2010/handouts/recitations/Recitation21VergheseFall2010.pdf>`_  
   * `LZ78 sliktākā gadījuma teorija 
     <http://www-math.mit.edu/~shor/PAM/lempel_ziv_notes.pdf>`_  



**LZ78 iekodēšanas pseidokods**


.. table:: LZ78Encode.Pseudocode

   ========  ==============================================
    Line      Description
   ========  ==============================================
    1         :math:`D = \text{\sc Dictionary}(S)` :math:`\;\;\;\;`  *saliek vārdnīcā visus burtus*
    2         :math:`w = \varepsilon` :math:`\;\;\;\;` *tukšais strings*
    3         :math:`k = text{\sc ReadSymbol}(F)`
    4         **while** :math:`k \neq \text{\sc eof}`
    5         :math:`\;\;\;\;` **if** :math`wk \in D.\text{\sc keys}()`
    6         :math:`\;\;\;\;\;\;\;\;` :math:`w = wk`
    7         :math:`\;\;\;\;` **else:**
    8         :math:`\;\;\;\;\;\;\;\;` \text{\sc Output}(D[w])`
    9         :math:`\;\;\;\;\;\;\;\;` \text{\sc Insert}(D,w)` :math:`\;\;\;\;` *Pievieno vārdnīcai ar jaunu kārtas numuru*
    10        :math:`\;\;\;\;\;\;\;\;` :math:`w=k`
    11        :math:`k = \text{\sc ReadSymbol}(F)`
    12        :math:`\text{\sc Output}(D[w])`
   ========  ==============================================



**LZW(S$)** -- Kodē simbolu plūsmu/stream
==================================================
| 1. :math:`C = \text{\sc ReadSymbol}(S)`
| 2. **while** :math:`C \neq \text{\sc eof}`
| 3. :math:`C' = \text{\sc GetIndex}(C,x)`
| 4. **while** :math:`C' \neq -1`:
| 5. :math:`C = C'`
| 6. :math:`x = \text{\sc ReadSymbol}(S)`
| 7. :math:`C' = \text{\sc GetIndex}(C,x)`
| 8. :math:`\text{\sc Output}(C)`
| 9. :math:`\text{\sc AddDict}(C,x)`
| 10. :math:`C =x`




**1. piemērs**
  Dota virkne :math:`\mathtt{abcabcabcdabcaba}`, 
  kura jānokodē, izmantojot Lempela - Ziva algoritmu.
  Vajadzētu sanākt 

  .. math:: 

    \mathtt{a,b,c,1,3,2,d,4,1,a}



**LZ78 atkodēšanas pseidokods**


.. figure:: figs/LZ78-decode.png
   :width: 6in

   LZ78 atkodēšana


**2. piemērs** 
  Izmantot LZ78, lai atkodētu virknīti: :math:`\mathtt{A.B.C.1.3.2.D.4.1.A}`

  Ja atkodēšana veikta pareizi, vajadzētu sanākt *`A.B.C.AB.CA.BC.D.ABC.AB.A`*.

**3. piemērs** 
  Atkodēt :math:`\mathtt{a,a,b,1,2,4,2}` par :math:`\mathtt{aabaaabaaaab}`

**4. piemērs:** 
  Atkodēt :math:`\mathtt{a,b,a,3,4}` par :math:`\mathtt{abaaaaaa}`



**LZ78 (biti par bitiem)**

Cits LZ78 variants (sāk ar tukšu vārdnīcu).

:math:`\mathtt{AABABBBABAABABBBABBABB}` (22 biti)  
:math:`\mathtt{A.AB.ABB.B.ABA.ABAB.BB.ABBA.BB}`

1. :math:`\mathtt{A}`
2. :math:`\mathtt{AB}`
3. :math:`\mathtt{ABB}`
4. :math:`\mathtt{B}`
5. :math:`\mathtt{ABA}`
6. :math:`\mathtt{ABAB}`
7. :math:`\mathtt{BB}`
8. :math:`\mathtt{ABBA}`
9. :math:`\mathtt{BB}`

:math:`\varnothing\mathtt{A}`

10. :math:`\mathtt{1A}`
11. :math:`\mathtt{2B}`
12. :math:`\varnothing\mathtt{B}`
13. :math:`\mathtt{2A}`
14. :math:`\mathtt{5B}`
15. :math:`\mathtt{4B}`
16. :math:`\mathtt{3A}`
17. :math:`\mathtt{7}`

LZ78 kods:  
:math:`\textcolor{blue}{\mathtt{01110100101001011100101100111}}` (29 biti)  
(Sākot no elementa :math:`2^k+1` 
viņa vārdnīcas adresi kodē ar :math:`k+1` bitiem.)






**Kur lieto LZ saimes algoritmus**

* Gzip, ZIP un V.42bis (modēmos lietots protokols) balstās uz LZ77. 
* Unix `compress`, un GIF formāti izmanto LZ78.

IBM patenti algoritmiem LZ78 un LZW iesniegti 1981 un 1983.g. 
(sk. `LZW Patents <https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch#Patents>`_)

Citi patenti saistībā ar saspiešanu:

* GIF (Unisys patents beidzās ap 2004.g.). 
  Radās aizstājējformāts PNG - tāda pati bezzudumu saspiesta rastra grafika 
  (tika pievienota "alpha-transparency"). 
* MP3 (patenti ASV beidzās ap 2017.g.). 
  Radās OGG Vorbis formāti skaņai un video. 
* MP3 patentu beigas: 23.aprīlis 2017.g. 
  `<https://www.audioblog.iis.fraunhofer.com/mp3-software-patents-licenses>`_

* Galalietotājam šie formāti arvien bijuši brīvi, bet dzelžu vai programmatūras ražotājiem, 
  kuri no tiem atvasina komerciālus produktus, reizēm bija jāmaksā - turklāt patentu tiesības 
  (MP3 gadījumā) bija samudžinātas (pamatos Technicolor and Fraunhofer).
* Debian Linux papildu repozitoriji.




Praktiski LZW algoritma apsvērumi:  
`What if dictionary is full 
<https://stackoverflow.com/questions/40054218/what-if-dictionary-size-in-lzw-algorithm-is-full>`. 




Saspiešanas rīki
^^^^^^^^^^^^^^^^^

**Kritēriji**

* Rīka standartizācija un saspiešanas/atspiešanas vispārēja pieejamība. 
  (Dažos gadījumos arī - nedaudz sabojātu arhīvu atjaunošana).
* Rīka izmaksas un licencēšanas kārtība.
* Vai tikai saspiež vai arī sapako lielākas direktorijas un/vai pievieno 
  šifrēšanu vai e-parakstu.
* Rīka saspiešanas attiecība, piemēram, cilvēku valodas tekstiem (arī 
  programmu izejas tekstiem, rastra grafikai, u.c.).
* Rīka saspiešanas un atspiešanas ātrums. 



**Linux komandrindu rīks "tar"**

.. code-block:: bash

   # install on Ubuntu/Debian
   sudo apt-get install tar
   # install on CentOS
   sudo yum install tar

   # compress
   tar -cvfz result.tar.gz original.txt
   # uncompress
   tar xvzf result.tar.gz

* "c" - *create* (veidot arhīvu),
* "x" - *eXtract* (atpakot arhīvu),
* "z" - *gZip* (lietot gzip saspiedēju papildus "Tape ARchive").
* "z" vietā "j" - (lietot bzip2 saspiedēju - t.i. Berouza-Vīlera algoritmu).



**Rīks gzip**

  .. code-block:: bash

     # Uzstāda uz Ubuntu/Debian
     sudo apt-get install gzip
     # compress
     gzip examplefile
     # list properties
     gzip -l examplefile.gz
     # uncompress 
     gzip -d examplefile.gz


**Rīks LZMA**

  .. code-block:: bash

   # compress
   lzma -c --stdout examplefile> examplefile.lzma
   # uncompress
   lzma -d --stdout examplefile.lzma >examplefile



**Rīks 7Zip**
  `<https://linuxhint.com/install-7zip-compression-tool-on-ubuntu/>`_



**Kalgari un Kenterberijas korpusi**

* `Kalgari korpuss <http://corpus.canterbury.ac.nz/descriptions/#calgary>`_ - 
  dažādi failu tipi (ieskaitot melnbaltus attēlus, faksus, veclaicīgu mašīnkodu); 
  `dažu algoritmu salīdzinājums <https://en.wikipedia.org/wiki/Calgary_corpus#Benchmarks>`_.  
  Kalgari korpusu arvien lieto metožu salīdzināšanai un pat saspiešanas sacensībām.
* `Kenterberijas korpuss <http://corpus.canterbury.ac.nz/>`_ - 
  mūsdienīgāks korpuss.




**Izsaukumi no Pitona**

* `zlib` bibliotēka. 
* `<https://stackabuse.com/python-zlib-library-tutorial/>`_
* `Python zlib tutorial <https://stackabuse.com/python-zlib-library-tutorial/>`_


**Par PNG formātu**

* PNG ir bezzudumu = pēc atspiešanas vienmēr tas pats rezultāts 
  (turklāt atspiešanas ātrums būtiski nemainās).
* Augstāks līmenis - lielāks bloku izmērs, lielāka vārdnīca.
* `pngcrush` var piemeklēt optimālus parametrus, jei svarīgi iegūt vismazāko PNG.


**PNG saspiešanas līmeņi**

Saspiešanas līmenis (0 - nesaspiests, ātrākais), 
(9 - visvairāk saspiests, lēnākais). 

.. code-block:: bash

   $ fmpeg -i input -vframes 1 -compression_level 0 0.png
   $ ffmpeg -i input -vframes 1 -compression_level 9 9.png



Lietojumi DLP produktos
^^^^^^^^^^^^^^^^^^^^^^^^

**Arhivatori un datu noplūde**

* `Symantec DLP risinājumi <https://www.symantec.com/products/dlp>`_
* `Forcepoint DLP risinājumi <https://www.forcepoint.com/product/dlp-data-loss-prevention>`_
* `Digital Guardian DLP aģents <https://digitalguardian.com/products/endpoint-dlp>`_

* Arhīvu atspiešana, saspiešana (reizēm arī TLS atšifrēšana/aizšifrēšana) ir laikietilpīga. 
* DLP notiek kanālos, kuri ir jūtīgi pret novēlošanos (Web, Email) -
  sk. `failu izmēru limiti 
  <https://www.websense.com/content/support/library/data/v84/file_support/file_size_limits.aspx>`_, 
  `atbalstītie arhīvu formāti 
  <https://www.websense.com/content/support/library/data/v84/file_support/dlp_file_support.pdf>`_.






**Daži arhīvu lietojumi DLP**

* Kas notiek, ja atarhivējot failu, rodas ļoti daudz failu? 
* Kas notiek, ja atarhivējot failu, rodas ļoti garš fails?
* Vai saspiešanas algoritms ļauj sākt arhivēt un sūtīt prom datus pirms
  saņemts viss nosūtāmais fails vai faili?  
  Starpniekserveris (*proxy server*) nevar analizēt lietotāju Web transakcijas ilgāk 
  kā aptuveni 10 sekundes, jo pārlūkprogrammu lietotāji nav pieraduši ilgi gaidīt. 
* Kas notiek, ja datus sāk sūtīt adresātam un pēkšņi pamana privātu datu noplūdi?  
  Vai saņēmējs arhīvu var saprast arī tad, ja saņemta daļa no tā?


**DLP atbildes uz izaicinājumiem**

* DLP analīzi censties biežāk veikt lokāli uz lietotāja datora 
  (*endpoint* jeb *agent* programmatūra, kas var veltīt vairāk CPU resursu
  konkrētā lietotāja failu analīzei).
* Konfigurēt DLP produktus novērošanas (*monitoring*) režīmā - tad
  ir vairāk laika analīzei, jo transakcijas var uzreiz atļaut neatkarīgi no to satura.
* Dažus grūti analizējamus failus (dīvaini saspiestus, ar parolēm aizsargātus
  biroja programmu dokumentus, šifrētus datus) var nelaist cauri vārtejām, 
  piespiest lietotājus sūtīt DLP rīkam saprotami.








Uzdevumi 
------------

**3.1. uzdevums**

  .. figure:: figs/markov-chain.png
     :width: 3in

     Markova ķēde

  Dota Markova ķēde, kurā automāta sākumstāvoklis (un 
  izvades pirmais burts) vienmēr ir :math:`A`. 
  Atrast tajā trešā burta varbūtību sadalījumu (ar kādām 
  varbūtībām tur ir attiecīgi :math:`A, B, C`).  

  Ierakstīt trīs racionālus skaitļus, atdalot tos 
  ar komatiem formātā `a/b,c/d,e/f` _____

.. only:: Internal 

  **Atbilde:**

    .. figure:: figs/markov-chain.png
       :width: 3in

       Markova ķēde

    1. Trešo burtu :math:`A` šajā Markova ķēdē var iegūt divos veidos:  

      **(i)** 
        Pāreja :math:`A \rightarrow A` un vēlreiz :math:`A \rightarrow A`.
        Varbūtība :math:`\frac{1}{4}\cdot\frac{1}{4}=\frac{1}{16}`.  

      **(ii)** 
        Pāreja :math:`A \rightarrow B` un tad :math:`B \rightarrow A`.
        Varbūtība :math:`\frac{3}{4}\cdot\frac{1}{4}=\frac{3}{16}`.  
        Abu varbūtību summa ir :math:`\frac{1}{16} + \frac{3}{16} = \frac{1}{4}`.

    2. Trešo burtu :math:`B` arī var iegūt divos veidos:  

      **(i)** 
        Pāreja :math:`A \rightarrow A` un tad :math:`A \rightarrow B`.
        Varbūtība :math:`\frac{1}{4}\cdot\frac{3}{4} = \frac{3}{16}`.  

      **(ii)** 
        Pāreja :math:`A \rightarrow B` un tad :math:`B \rightarrow B`.
        Varbūtība :math:`\frac{3}{4}\cdot\frac{1}{4} = \frac{3}{16}`.  
        Abu varbūtību summa :math:`\frac{3}{16} + \frac{3}{16} = \frac{3}{8}`.

    3. Trešo burtu :math:`C` var iegūt vienā veidā:
       :math:`A \rightarrow B` un tad :math:`B \rightarrow C`.
       Varbūtība  :math:`\frac{3}{4}\cdot\frac{1}{2} = \frac{3}{8}`.

    Tātad varbūtību sadalījums ir :math:`\left( \frac{1}{4}, \frac{3}{8}, \frac{3}{8} \right)`. 






    Starp citu, trešajam burtam atbilstošā varbūtību sadalījuma :math:`\{ 1/4, 3/8, 3/8 \}` 
    entropija ir :math:`1.56`. Bet faktiski no Markova ķēdes
    saņemtās virknes var saspiest labāk 
    nekā šī entropija, jo burti :math:`A,B,C` nav pilnīgi neatkarīgi.

    Salīdzināt šāda veida datiem aritmētisko kodu, LZ78 un Berouza-vīlera 
    saspiešanu. 
    Tādēļ aritmētisko saspiešanu šajā gadījumā lietot nav optimāli.

  `\square`



Kopsavilkums
-------------

1. Apspriedām entropijas kodu lietojamības robežas.
2. Ieviesām Lempela Ziva algoritmu LZ77.
3. Ieviesām Lempela Ziva algoritmu LZ78.
4. Apspriedām LZ77, LZ78 lietojumus, failu formātus un 
   arhivēšanas bibliotēkas.
