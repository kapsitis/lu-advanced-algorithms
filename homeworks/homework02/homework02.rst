2. mājasdarbs: JPEG, H.264 un Kļūdu korekcija
====================================================

**1. uzdevums:** 

  Dots attēls "bumblebee.png"
  (PNG failu šeit izmanto kā "raw data" avotu -- krāsu pikseļu matricu, 
  kam var lietot dažādus JPEG-stila saspiešanas paņēmienus.)

  .. figure:: figs/bumblebee.png
     :width: 300px
  
  **(A)**
    Pārveidot attēlu YCbCr koordinātēs; katrai koordinātei izveidot 
    attēlu (attiecīgi melnbaltu Y koordinātei, zili-oranžu I koordinātei 
    un zaļi-violetu Q koordinātei). Iekopēt iegūtos 3 attēlus mājasdarbā.
    Pārveidojumu formulas var aizgūt no Vikipēdijas raksta 
    `YCbCr <https://en.wikipedia.org/wiki/YCbCr>`_. 


  **(B)** 
    Uzzīmēt histogrammas tam, kā attēlā sadalītas attiecīgi Y, Cb un Cr krāsas.
    T.i. katrai no YCbCr krāsu modeļa koordinātēm no itervāla :math:`[16, 240]` 
    uzzīmēt grafiku, kurā uz 
    horizontālās ass ir visas teorētiski iespējamās attiecīgās krāsu koordinātes 
    vērtības ar soli 5, bet uz vertikālās ass
    svītriņas augstums attēlo biežumu, ar kuru pikseļi attēlā `bumblebee.png` 
    pieņem attiecīgo vērtību.
    
    .. note:: 
      Starp citu, YCbCr koordinātu histogrammas var lietot, lai uzlabotu attēla kontrastu -- 
      `Histogram equalization <https://en.wikipedia.org/wiki/Histogram_equalization>`_.


**2. uzdevums:** 
  
  Par ievadi izmantot melnbalto `bumblebee.png` attēlu no iepriekšējā uzdevuma. 

  **(A)** 
    Izvadīt DCT rezultātu kamenes attēla kreisajā augšējā stūrī esošajam 
    :math:`8 \times 8` blokam (aplūkojot 
    tikai melnbalto Y krāsas komponenti). Izdrukāt to kā 
    :math:`8 \times 8` matricu ar reāliem skaitļiem (ar precizitāti 0.0001). 

  **(B)**
    Visiem kamenes attēla blokiem veikt DCT; pēc tam noapaļot uz :math:`0` visus tos 
    DCT koeficientus :math:`X_{ij}`, kam :math:`i > 4` vai :math:`j > 4` 
    (t.i. no visiem 64 koeficientiem paturēt tikai 25 koeficientus). 
    Veikt inverso DCT pārveidojumu no frekvenču pasaules atpakaļ uz 2D pasauli. 
    Izvadīt iegūto "noapaļoto" attēlu -- tā arī būs melnbalta PNG bilde. 
    (To var ielīmēt mājasdarba PDF tekstā.)


**3. uzdevums:** 
  Atrast kļūdas (ja tādas ir) sekojošos Heminga koda ziņojumos:
  
  **(A)** 
    `1100000`.
    
  **(B)**
    `0110011`.
    
  **(C)** 
    `001001111000101` (15-bitu Heminga kods, bitu secība - no `x1111` līdz `x0001`).


**4. uzdevums:** 
  Ar burtiem :math:`a` un :math:`b` apzīmēti Jūsu studentu apliecības pēdējie 2 cipari. 

  **(A)** 
    Datus kodē ar :math:`10` pakāpes polinomiem, 
    pārraidot `20` polinoma vērtības (:math:`f(0), f(1), \ldots, f(19)`). 
    Kāds ir maksimālais kļūdu skaits, pie kura iespējams viennozīmīgi atjaunot sākotnējo ziņojumu? 
    Pamatot, kāpēc šādu kļūdu skaitu var izlabot. Un arī, kāpēc nav iespējams koriģēt lielāku kļūdu skaitu.
  
  **(B)** 
    Atkodēt ar RS kodu (:math:`2` pakāpes polinoms, :math:`5` vērtības :math:`f(0), \ldots,f(4)`, 
    operācijas pēc :math:`\pmod {11}`) kodētu ziņojumu 
     
    .. math:: 
      
      2,\;\; \ast,\;\; (a + b) \operatorname{mod} 11,\;\; (3b + 2) \operatorname{mod} 11,\;\; \ast
     
    kur saņemtās vērtības visas ir pareizas, bet ar :math:`\ast` apzīmētās vērtības ir pazaudētas.





  