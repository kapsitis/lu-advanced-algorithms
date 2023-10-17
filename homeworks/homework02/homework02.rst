2. mājasdarbs: JPEG, H.264 un Kļūdu korekcija
====================================================

**1. uzdevums:** 

  Dots attēls "bumblebee.png"
  (PNG failu šeit izmanto kā "raw data" avotu, kuram var lietot dažādus JPEG-stila saspiešanas paņēmienus.)

  .. figure:: figs/bumblebee.png
     :width: 300px
  
  **(A)**
    Pārveidot to YIQ koordinātēs; katrai koordinātei izveidot 
    attēlu (attiecīgi melnbaltu Y koordinātei, zili-oranžu I koordinātei 
    un zaļi-violetu Q koordinātei). Iekopēt iegūtos 3 attēlus mājasdarbā. 


  **(B)** 
    Uzzīmēt histogrammas tam, kā attēlā sadalītas attiecīgi Y, I un Q krāsas.
    T.i. katrai no YIQ krāsu modeļa 3 koordinātēm :math:`Y \in [0;1]`, 
    `I \in [-0.5;0.5]` un `Q \in [-0.5; 0.5]` uzzīmēt atsevišķu grafiku, kuram uz 
    horizontālās ass ir visas teorētiski iespējamās attiecīgās krāsu koordinātes 
    :math:`Y`, :math:`I`, vai :math:`Q` vērtības ar soli 0.01, bet uz vertikālās ass
    svītriņas augstums attēlo biežumu, ar kuru pikseļi attēlā `bumblebee.png` 
    pieņem attiecīgo vērtību (kas noapaļota līdz tuvākajai simtdaļai).
    Piemēram, virs horizontālās ass skaitļa :math:`0.51` stabiņa augstums parāda, 
    cik daudz attēlā bija pikseļu, kam :math:`Y` koordināte noapaļojas uz vērtību :math:`0.51`.
    
    .. note:: 
      Starp citu, YIQ koordinātu histogrammas var lietot, lai uzlabotu attēla kontrastu -- 
      `Histogram equalization <https://en.wikipedia.org/wiki/Histogram_equalization>`_.
      (Ja šādi mēģina izlīdzināt atsevišķi R, G, B krāsu koordinātes, kontrasts arī uzlabojas, bet 
      attēlā var pasliktināties krāsu līdzsvars - atsevišķi attēla apgabali var kļūt 
      nedaudz sarkanāki, zilāki utml. Savukārt YIQ krāsu modelī līdzīgas manipulācijas 
      krāsu līdzsvaru neiespaido.) Nekāds *histogram equalization* jums šajā uzdevumā nav jāveic.


**2. uzdevums:** 

  Dots kamenes attēls `bumblebee.png` (tas pats, kas iepriekšējā uzdevumā). 

  **(A)** 
    Izvadīt DCT rezultātu kamenes attēla kreisajā augšējā stūrī esošajam 8x8 blokam (aplūkojot 
    tikai melnbalto Y koordināti). Izdrukāt to kā 8x8 matricu ar reāliem skaitļiem (ar precizitāti 0.0001). 

  **(B)**
    Visiem kamenes attēla blokiem veikt DCT; tos DCT koeficientus, kas  mazāki par :math:`X`, noapaļot uz 0. 
    Veikt inverso DCT pārveidojumu no frekvenču pasaules atpakaļ uz 2D pasauli. 
    Izvadīt iegūto "noapaļoto" attēlu -- tā arī būs melnbalta PNG bilde. 


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
      
      2,\;\; \ast,\;\; (a + b) \operatorname{mod} 11,\;\; (3b + 2) \operatorname{mod} 11
     
    kur saņemtās vērtības visas ir pareizas, bet ar :math:`\ast` apzīmētās vērtības ir pazaudētas.





  