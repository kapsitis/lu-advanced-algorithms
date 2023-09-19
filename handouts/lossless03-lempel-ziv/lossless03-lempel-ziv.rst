3. Bezzudumu saspiešana: Lempela-Ziva algoritms
=================================================

1. Sarežģītības apsvērumi (cik reizes lasa ievadi). 
2. Lietot un analizēt Lempela-Ziva algoritmu (LZ77). Arī LZ78 un Lempela-Ziva-Velša algoritmu (LZW). 
3. Vārdnīcu saspiešanas algoritmu lietojumi.

Motivācija saspiešanai ar vārdnīcas algoritmiem:

* Entropijas saspiešanas metodes nevar būt labākas par datu avota entropiju.
* Reālos datos nākošais simbols atkarīgs no iepriekšējā.
* Var veidot N-grammas (2 burtu virknes kā jaunus "simbolus": aa, ab, ac, ad, ...). 
  Tam pielieto Hafmana vai aritmētisko kodu. Jau nelielam skaitam simbolu 
  virknīšu kļūst ļoti daudz un Hafmana/aritmētiskie kodi kļūst sarežģīti.
* Var arī izmantojot to, ka ir simbolu virknes, kas atkārtojas. 
  Ievieš jaunus simbolus priekš šādām virknēm; 
  tās arī ir Lempela-Ziva metodes (LZ77 vai LZ78).


Entropijas kodu vispārinājumi
-------------------------------

Ne vienmēr burti saspiešanas algoritma ievadē ir 
neatkarīgi un vienādi sadalīti (kā tas ir entropijas koda gadījumā). 
Jau aritmētiskais kods labi atbalsta tādas gadījumlielumu 
virknes, kurām ir "atmiņa" -- tās atceras iepriekšējo burtu.

**Definīcija**
  Par *Markova ķēdi* (*Markov chain*) sauc varbūtisku procesu, 
  kas ģenerē burtu virknīti
  ar orientētu grafu: 
  
  * katrs izvades burts ir automāta stāvoklis
  * pāreja no viena burta uz citu ir izsakāma ar varbūtību
  * modelim nav atmiņas (tas neatceras neko citu kā vien iepriekšējo burtu)

**Piemērs:** 
  Šāds orientēts grafs ar :math:`3` stāvokļiem apraksta Markova ķēdi:

  .. figure:: figs/markov-chain.png
     :width: 1.5in

  :math:`18` burtu virknīte iegūta nejauši staigājot pa šo grafu, 
  sākot ar :math:`A`: `ABCABCBCAAABCABBAB`. 

**Apgalvojums:** 
  Hafmana koki var nebūt optimāli, saspiežot virknītes no Markova ķēdēm 
  (jo nākamais burts ir atkarīgs no iepriekšējā). 
  Savukārt aritmētisko kodu var pielāgot tā, lai tas mainītu burtiem 
  piesaistīto intervālu garumus atkarībā no iepriekš redzētā burta.


Ar Markova ķēdi iegūtā virknītē burti vairs nav *neatkarīgi un vienādi sadalīti*
(*independent and identically distributed*), jo burta parādīšanās 
varbūtību ietekmē iepriekšējais burts. Tie vairs nav entropijas kodi. 

**Definīcija:** 
  Aplūkojam :math:`X_1 X_2 X_3\ldots` - ziņojumu virkni, kas ģenerēta 
  ar Markova ķēdi. Par par šīs virknes *vidējo entropiju* (*entropy rate*)
  sauc robežu: 

  .. math::

    H(X) = \lim_{n \to \infty} \frac{1}{n} H\left( X_1, X_2, \ldots X_n \right). 

  Markova ķēdēm (un daudziem citiem varbūtiskiem procesiem) tā vienāda ar 
  entropiju, kas izrēķināta no nosacītajām varbūtībām
  (t.i. pieņemam, ka pirmos :math:`n-1` simbolus jau esam redzējuši, atrodam
  kārtējā :math:`n`-tā simbola nosacīto varbūtību sadalījumu un tā entropiju):  

  .. math:: 
  
    H'(X) = \lim_{n \to \infty} H\left( X_n \,\mid\, X_{n-1}, X_{n-2}, \ldots X_1 \right).

  Parasti :math:`H(X) = H'(X)`.


Dabīgo valodu apraksta vēl sarežģītāki modeļi (piemēram *Hidden Markov model*), 
kur atkal ir galīgs grafs ar stāvokļiem (kuri nav redzams burtu virknē)
un katru stāvokļu pāreju saistām ar noteikta burta izvadi (ir redzami virknē).
Slēptajam Markova modelim un citiem sarežģītākiem 
modeļiem (arī dabiskajai valodai) entropiju jeb saspiežamības robežu definēt
ir grūtāk, jo nav saprotams varbūtiskais modelis, kas to visu ģenerē. 
Dabiskajām valodām bieži izvēlas kādu no šiem diviem modeļiem: 

* n-grammu modelis: Faktiski pieņem, ka nākamā simbola (valodas burta vai arī vārda)
  parādīšanās varbūtību iespaido :math:`n` iepriekš saņemtie simboli. 
* Neironu tīklu modelis: Apmāca neironu tīklu, kurš pēc tam var prognozēt varbūtības.  

Novērojums (literatūrkritiķe Ruta Veidemane "Izteikt neizsakāmo") - dzejas valodas
informatīvais saturs ir lielāks nekā prozai. 

**Definīcija:** 
  Par *n-grammu* (*n-gram*) sauc dotajā tekstā sastopamu :math:`n` pēc kārtas 
  sekojošu simbolu virknīti. 

Ja simbolu virknē simboli nav neatkarīgi, tad divu simbolu pārīšiem 
(*digrammām* jeb 2-grammām) entropija ir mazāka nekā divkāršota entropija 
vienam ziņojumam.
Individuālo simbolu entropijas kodu vietā varētu izmantot 
*n-gramu* entropijas kodus, bet jau nelielām vērtībām (n=2,3) kodu tabulas 
mēdz būt nenormāli lielas -- saspiest it kā var efektīvāk, bet kodu tabulu 
kļūst nepraktiski nosūtīt. 

Ir adaptīvāki algoritmi, kuri iekodē n-grammas, balstoties uz to, kas datos redzams. 
Tāds piemērs ir *Prediction by partial matching* -- viens no stiprākajiem 
saspiešanas algoritmiem dabiskās valodas tekstam.


LZ77-veida algoritmi
-----------------------

Šajā gadījumā vārdnīca ir gabals no jau iekodētās virknes. 
Iekodētājs redz beigu gabalu no iekodētās virknes kā slīdošo logu: 

.. figure:: figs/lz77-window.png
   :width: 2in 

Logs ir kā atmiņas buferis, kurā var atrast nesen iekodētas virknes 
un izmantot tās, lai īsāk pierakstītu to virknes gabaliņu, kurš sekos. 

**Piemērs:** 
  Aizkodēt virkni :math:`\mathtt{abcabcabcdabc}`, ja loga garums :math:`k = 6`. 

  Vajadzētu sanākt :math:`\mathtt{(1,a),(1,b),(1,c),(0,1,6),(1,d),(0,3,3)}`. 





LZ78-veida algoritmi
----------------------


**LZ78 saspiešanas algoritms**
  **Ievade:** :math:`F` -- plūsma simbolu nolasīšanai.  
  **Izvade:** Simboli un cipari (adreses vārdnīcā).  
  
  | :math:`\text{\sc LZ78encode}(F)`:
  | 1. :math:`\;\;\;\;\;` :math:`D = \text{\sc Dictionary}(S)` :math:`\;\;\;\;\;\;\;\;\;\;`
    :math:`\textcolor{teal}{\text{\em saliek vārdnīcā visus burtus}}`
  | 2. :math:`\;\;\;\;\;` :math:`w = \varepsilon` :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;`
    :math:`\textcolor{teal}{\text{\em tukšais strings}}`
  | 3. :math:`\;\;\;\;\;` :math:`k = \text{\sc readSymbol}(F)`
  | 4. :math:`\;\;\;\;\;` **while** :math:`k \neq \text{\sc eof}`
  | 5. :math:`\;\;\;\;\;\;\;\;\;\;`  **if** :math:`wk \in D.\text{\sc keys}()`:
  | 6. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`w = wk`
  | 7. :math:`\;\;\;\;\;\;\;\;\;\;`  **else:**
  | 8. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc output}(D[w])`
  | 9. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc insert}(D,w)` :math:`\;\;\;\;\;\;\;\;\;\;`
    :math:`\textcolor{teal}{\text{\em pievieno vārdnīcai ar jaunu kārtas numuru}}`
  | 10. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`w=k`
  | 11. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`k = \text{\sc readSymbol}(F)`
  | 12. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc output}(D[w])`
    

**LZ78 atspiešanas algoritms** 
  **Ievade:** :math:`F` -- saspiesto datu plūsma
  **Izvade:** Atspiestais teksts


  | :math:`\text{\sc LZ78decode}(F)`:
  | 1. :math:`\;\;\;\;\;` :math:`w = \text{\sc lookup}(\text{\sc readCode}())`
  | 2. :math:`\;\;\;\;\;` :math:`\text{\sc output}(w)`
  | 3. :math:`\;\;\;\;\;` :math:`c = \text{\sc readCode()}` 
  | 4. :math:`\;\;\;\;\;` **while** :math:`c \neq \text{\sc eof}`:
  | 5. :math:`\;\;\;\;\;\;\;\;\;\;` **if** :math:`c \in D`: :math:`\;\;\;\;\;\;\;\;\;\;` 
    :math:`\textcolor{teal}{\text{\em if $c$ is in the dictionary}}`
  | 6. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`wn = \text{\sc lookup}(c)`
  | 7. :math:`\;\;\;\;\;\;\;\;\;\;` **else**:
  | 8. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`wn = \text{\sc stringcat}(w, w[0])`
  | 9. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc output}(wn)`
  | 10. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`k = wn[0]`
  | 11. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`D.\text{\sc add}(wk)` :math:`\;\;\;\;\;\;\;\;\;\;` 
    :math:`\textcolor{teal}{\text{\em add wk to dictionary}}`
  | 12. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`w = wn`





**Piemērs:**
  Dota virkne :math:`\mathtt{abcabcabcdabcaba}`, 
  kura jānokodē, izmantojot LZ78 algoritmu.

=======  =====================  ====  ========  ===================
Solis    Garākais w vārdnīcā    k     Izvade    Pievieno vārdnīcai
=======  =====================  ====  ========  ===================
1.       a                      b     a         ab
2.       b                      c     b         bc
3.       c                      a     c         ca
4.       ab                     c     ab        abc
5.       ca                     b     ca        cab
6.       bc                     d     bc        dbc
7.       d                      a     d         da
8.       abc                    a     abc       abca
9.       ab                     a     ab        aba
10.                                   a
=======  =====================  ====  ========  ===================

Parasti kodē burtus par burtiem, bet garākas virknes aizstāj ar tā soļa numuru, 
kurā šī virkne ir ievietota vārdnīcā. Tas nozīmē, ka 1. piemērā virkne `ab` 
tiktu kodēta kā 1, `bc` kā 2, `ca`` kā 3, utt.
Beigās iegūta virkne :math:`\mathtt{a,b,c,1,3,2,d,4,1,a}` 


**2. piemērs** 
  Izmantot LZ78, lai atkodētu virknīti: :math:`\mathtt{A.B.C.1.3.2.D.4.1.A}`

  Ja atkodēšana veikta pareizi, vajadzētu sanākt *`A.B.C.AB.CA.BC.D.ABC.AB.A`*.

**3. piemērs** 
  Atkodēt :math:`\mathtt{a,a,b,1,2,4,2}` par :math:`\mathtt{aabaaabaaaab}`

**4. piemērs:** 
  Atkodēt :math:`\mathtt{a,b,a,3,4}` par :math:`\mathtt{abaaaaaa}`




Lempel-Ziv-Welch algoritms (LZW) 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Saspiešanas algoritms:**
  * Ievade: :math:`F` -- plūsma (sākotnējais teksts)
  * Izvade: saarhivēts teksts.

  | :math:`\text{\sc LZWencode}(F)` 
  | 1. :math:`\;\;\;\;\;` :math:`C = \text{\sc ReadSymbol}(F)`
  | 2. :math:`\;\;\;\;\;` **while** :math:`C \neq \text{\sc eof}`
  | 3. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`x = \text{\sc ReadSymbol}(F)`
  | 4. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`C' = \text{\sc getIndex}` 
  | 5. :math:`\;\;\;\;\;\;\;\;\;\;` **while** :math:`C' \neq -1`: 
  | 6. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`C  = C'`
  | 7. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`C' = \text{\sc getIndex}(C,x)`
  | 8. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc output}(C)`
  | 9. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc addDict}(C,x)`
  | 10. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`C = x`


**Atspiešanas algoritms:**
  * Ievade: :math:`F` -- plūsma (saspiests teksts)
  * Izvade: atarhivēts teksts.

  | :math:`\text{\sc LZWdecode}(F)` 
  | 1. :math:`\;\;\;\;\;` :math:`C = \text{\sc readIndex}(F)`
  | 2. :math:`\;\;\;\;\;` :math:`W = \text{\sc getString}(C)`
  | 3. :math:`\;\;\;\;\;` :math:`\text{\sc output}(W)`
  | 4. :math:`\;\;\;\;\;` **while** :math:`C \neq \text{\sc eof}`:
  | 5. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`C' = \text{\sc readIndex}(F)`
  | 6. :math:`\;\;\;\;\;\;\;\;\;\;` **if** :math:`\text{\sc indexInDict}(C')`:
  | 7. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`W = \text{\sc getString}(C')`
  | 8. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc addDict}(C,W[0])`
  | 9. :math:`\;\;\;\;\;\;\;\;\;\;` **else**: 
  | 10. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`C' = \text{\sc addDict}(C, W[0])`
  | 11. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` :math:`W = \text{\sc getString}(C')`
  | 12. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`\text{\sc output}(W)`
  | 13. :math:`\;\;\;\;\;\;\;\;\;\;` :math:`C = C'`








Vārdnīcas saspiešanas algoritmu lietojumi 
-------------------------------------------

**Saspiešanas standarti:** 
  Saspiešanas standartus un rīkus var dažādi salīdzināt:

  * Rīka standartizācija un licences. 
  * Iespēja atjaunot nepilnīgi nosūtītus arhīvus?
  * Papildu īpašības (direktoriju sapakošana 1 failā, šifrēšana vai e-paraksts).
  * Saspiešanas attiecība cilvēku valodai, rastra grafikai, u.c.
  * Rīka saspiešanas un atspiešanas ātrums, prasības pēc RAM. 

**Standarti ar LZ77:**
  Gzip, ZIP, PNG balstās uz LZ77 (reizēm kopā ar Hafmana kodu - t.s. "deflate" algoritms).  

**Standarti ar LZ78:**
  Unix `compress`, un GIF formāti. 






**Linux rīki "tar" un "gzip"**
  "Tape archive" - lenšu arhīvs:

  .. code-block:: bash

     tar -cvfz result.tar.gz original.txt
     tar xvzf result.tar.gz
     # gzip komandas:
     gzip -l examplefile.gz
     gzip -d examplefile.gz

  * "c" - *create* (veidot arhīvu),
  * "x" - *eXtract* (atpakot arhīvu),
  * "z" - *gZip* (lietot gzip saspiedēju papildus "Tape ARchive").
  * "z" vietā "j" - (lietot bzip2 saspiedēju - t.i. Berouza-Vīlera algoritmu).



**Rīks LZMA**

  .. code-block:: bash

    lzma -c --stdout examplefile > examplefile.lzma
    lzma -d --stdout examplefile.lzma > examplefile

**Par PNG formātu**
  PNG ir bezzudumu = pēc atspiešanas vienmēr tas pats rezultāts 
  (turklāt atspiešanas ātrums būtiski nemainās).
  
  * Augstāks līmenis - lielāks bloku izmērs, lielāka vārdnīca.
  * `pngcrush` var piemeklēt optimālus parametrus, ja svarīgi iegūt vismazāko PNG.
  * Saspiešanas līmenis (0 - nesaspiests, ātrākais), (9 - visvairāk saspiests, lēnākais). 

  .. code-block:: bash

    $ fmpeg -i input -vframes 1 -compression_level 0 0.png
    $ ffmpeg -i input -vframes 1 -compression_level 9 9.png


  .. code-block:: python 

    from PIL import Image
    import numpy as np

    # 100x100 nejauši reāli skaitļi intervālā [0;1]
    imageArray = np.random.rand(100,100)
    # Izmaina mērogu uz [0;255] melnbaltā attēlā "255" ir balts
    img = Image.fromarray(imageArray * 255)
    # Eksportē uz PNG failu
    img.convert('RGB').save('raster_output.png')


  .. figure:: figs/raster_output.png
     :width: 2in



**Lietojumi DLP produktos**
  DLP (Data Leak Prevention) rīki var novērst konfidenciālu datu 
  nekontrolētu noplūdi uzņēmumā -- piemēram, ja darbinieks pārsūta 
  jūtīgus failus, teksta fragmentus u.c. nepiemērotam mērķim. 
  
  
  * Datu *klasifikatori* (*classifiers*) ir likumi, kas definē konfidenciālu datu tipus. 
    (Adreses, telefonu numuri, epasti, personas kodi, IBAN kontu numuri, 
    kredītkaršu numuri, rindkopas no konfidenciāliem dokumentiem utml.)
    Daži klasifikatori ir kā universāli paterni (visi faili noteiktā formātā, 
    stringi atbilstoši regulārai izteiksmei), citi ir nolasāmi no datubāzēm 
    (piemēram, tikai mūsu klientu telefonu numuri) vai iegūstami ar mašīnmācīšanos.
  * Datu *kanāli* (*channels*) ir viss, ko var novērot -- piemēram 
    HTTP augšupielādes, izejošie epasti, "clipboard" jeb kopēšanas darbības, 
    ekrānuzņēmumi. 
  * Aizsardzības politikas (*policies*) nosaka, ko pa kuru kanālu kuriem adresātiem 
    drīkst vai nedrīkst sūtīt. Politikai (bez kanāla un klasifikatora) ir arī darbība -- 
    piemēram "Monitor" un "Block" (neļauj sūtīt).


  Ir vairāki komerciāli produkti par DLP: 

  * `Symantec DLP risinājumi <https://www.symantec.com/products/dlp>`_
  * `Forcepoint DLP risinājumi <https://www.forcepoint.com/product/dlp-data-loss-prevention>`_
  * `Digital Guardian DLP aģents <https://digitalguardian.com/products/endpoint-dlp>`_
  * Arhīvu atspiešana, saspiešana (reizēm arī TLS atšifrēšana/aizšifrēšana) ir laikietilpīga. 
  * DLP notiek kanālos, kuri ir jūtīgi pret novēlošanos (Web, Email) -
    sk. `failu izmēru limiti 
    <https://www.websense.com/content/support/library/data/v84/file_support/file_size_limits.aspx>`_, 
    `atbalstītie arhīvu formāti 
    <https://www.websense.com/content/support/library/data/v84/file_support/dlp_file_support.pdf>`_.


  **Arhīvu lietojumi DLP**
    Bieži datu noplūde ir arhīvs. Tāpēc ir vairāki praktiski apsvērumi: 

    * Kas notiek, ja atarhivējot failu, rodas ļoti daudz failu? 
    * Kas notiek, ja atarhivējot failu, rodas ļoti garš fails?
    * Vai saspiešanas algoritms ļauj sākt arhivēt un sūtīt prom datus pirms
      saņemts viss nosūtāmais fails vai faili?  
      Starpniekserveris (*proxy server*) nevar analizēt lietotāju Web transakcijas ilgāk 
      kā aptuveni 10 sekundes, jo pārlūkprogrammu lietotāji nav pieraduši ilgi gaidīt. 
    * Kas notiek, ja datus sāk sūtīt adresātam un pēkšņi pamana privātu datu noplūdi?  
      Vai saņēmējs arhīvu var saprast arī tad, ja saņemta daļa no tā?


  **Kā DLP atbild uz izaicinājumiem**
    
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

  Ierakstīt atbildē trīs racionālus skaitļus. 

.. only:: Internal 

  **Atbilde:**

    .. figure:: figs/markov-chain.png
       :width: 1.5in

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



**Kopsavilkums:**

1. Apspriedām entropijas kodu lietojamības robežas.
2. Ieviesām Lempela Ziva algoritmu LZ77.
3. Ieviesām Lempela Ziva algoritmu LZ78.
4. Apspriedām LZ77, LZ78 lietojumus, failu formātus un 
   arhivēšanas bibliotēkas.


**Bibliogrāfija:** 

  * `LZW algoritma piemērs 
    <http://web.mit.edu/6.02/www/f2010/handouts/recitations/Recitation21VergheseFall2010.pdf>`_.
  * Praktiski LZW algoritma apsvērumi:  
    `What if dictionary is full 
    <https://stackoverflow.com/questions/40054218/what-if-dictionary-size-in-lzw-algorithm-is-full>`. 
  * `LZ78 sliktākā gadījuma teorija 
    <http://www-math.mit.edu/~shor/PAM/lempel_ziv_notes.pdf>`_.
  * `PPM algoritms <https://en.wikipedia.org/wiki/Prediction_by_partial_matching>`_. 
  * `<https://stackabuse.com/python-zlib-library-tutorial/>`_
  * `Python zlib tutorial <https://stackabuse.com/python-zlib-library-tutorial/>`_
  * IBM patenti algoritmiem LZ78 un LZW iesniegti 1981 un 1983.g. 
    (sk. `LZW Patents <https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch#Patents>`_)
  * `<https://linuxhint.com/install-7zip-compression-tool-on-ubuntu/>`_. 
  * `Kalgari korpuss <http://corpus.canterbury.ac.nz/descriptions/#calgary>`_ - 
    dažādi failu tipi (ieskaitot melnbaltus attēlus, faksus, veclaicīgu mašīnkodu); 
    `dažu algoritmu salīdzinājums <https://en.wikipedia.org/wiki/Calgary_corpus#Benchmarks>`_.  
    Kalgari korpusu arvien lieto metožu salīdzināšanai un pat saspiešanas sacensībām.
  * `Kenterberijas korpuss <http://corpus.canterbury.ac.nz/>`_ - 
    mūsdienīgāks korpuss.
