4. mājasdarbs: Stringu algoritmi
====================================================

**1. uzdevums:** 

  Alfabētā ir :math:`100` simboli, kas apzīmēti ar ciparu pāriem: 
  :math:`\{ \mathtt{00}, \mathtt{01}, \ldots, \mathtt{99} \}`. 
  Iedomāsimies, ka hešinga funkcijai Rabina-Karpa algoritmā jāaprēķina
  hešfunkcijas vērtības teksta simbolu virknītēm garumā 
  :math:`k = 5` un pirmskaitlis moduļa rēķināšanai ir :math:`n = 23`.
  Hešfunkcija definēta ar izteiksmi 
  
  .. math::
  
    H = (c_1 a^{k-1} + c_2 a^{k-2} + c_3 a^{k-3} + ... + c_k a^{0})\,\text{mod}\,n, 
	
  kur :math:`a = 100` ir alfabēta burtu skaits 
  un :math:`c_i` ir ievades simboli (skaitļi no 0 līdz 99).
  Sal. `Polynomial Rolling Hash
  <https://en.wikipedia.org/wiki/Rolling_hash#Polynomial_rolling_hash>`_ definīciju. 

  **(A)**
    
    Uzrakstīt formulu funkcijai `skip(oldval,c)`, kas veco hešfunkcijas vērtību 
    (iepriekšējai 5 simbolu virknītei) pārveido par hešfunkcijas vērtību, kurai burts "c"
    virknītes sākumā ir nodzēsts (t.i. jaunā virknīte ir tikai 4 simbolus gara). 
	
    Uzrakstīt formulu funkcijai `append(oldval,c)`, kas veco hešfunkcijas vērtību 
    (4 simbolu virknītei) pārveido par jaunu vērtību, kur virknītei galā pierastīts
    burts "c" (jaunā virknīte ir 5 simbolus gara). 
	
  **(B)** 	
    Uzrakstīt ripojošās hešfunkcijas pārveidojumu, ja ievades virkne ir  
    ``[03, 14, 15, 92, 65, 35, 89, 79, 31]``,  un ievades vārds 
    aizveļas no ``[03, 14, 15, 92, 65]`` uz ``[14, 15, 92, 65, 35]``. 
    To dara 3 soļos: 
	
    * Aprēķina hešfunkciju H no ``[03, 14, 15, 92, 65]``,
    * Lieto `skip()` lai nomestu burtu "03" vārda sākumā, 
    * Lieto `append()`, lai pievienotu burtu "35" vārda beigās.
	
    Pārbaudīt, ka pēc šiem soļiem iegūta tā pati vērtība, kas
    būtu rēķinot polinomiālo hešfunkciju tieši no ievades ``[14, 15, 92, 65, 35]``. 


**2. uzdevums:** 

  **(A)** 
    Uzrakstīt Knuta-Morisa-Prata algoritmā izmantoto tabulu 
    (prefiksu funkciju :math:`\pi(i)`, `i \in [1;m]`, 
    ja meklējamais vārds ir :math:`P=\mathtt{ABCDABD}`. 
	
  **(B)** 
    Uzrakstīt šī algoritma izpildi tabulas veidā šī vārda meklēšanai, ja teksts ir 
    :math:`\mathtt{ABC\_ABCDAB\_ABCDABCDABDE}`, kur pasvītrojumzīme 
    ir atsevišķs burts ievades alfabētā.
    *Tabulā katra rindiņa atbilst noteiktai nobīdei starp vārdu un tekstu un 
    pie tās pašas nobīdes tiek salīdzināti 1 vai vairāki burti.*


**3. uzdevums:** 

  **(A)** 
    Uzrakstīt Bojera-Mūra algoritmā izmantotās tabulas
    (sliktā simbola funkciju :math:`\lambda(i)` un 
    labā sufiksa funkciju :math:`\gamma(i)`), ja
    meklējamais vārds ir :math:`\mathtt{ABCBCAB}`. 
	
  **(B)** 
    Uzrakstīt šī algoritma izpildi tabulas veidā šī vārda meklēšanai, ja teksts ir 
    :math:`\mathtt{ABCABBCABCBCABABABABCBCAB}`. 

**4. uzdevums:** 

  Dota :math:`n \times m` tabula, katrā rūtiņā ir ierakstīts 
  tieši viens simbols. Teiksim, ka vārds ir *paslēpts* tabulā, 
  ja to var nolasīt, sākot ar kādu rūtiņu un katru nākamo 
  simbolu nolasot no rūtiņas, kurai ar iepriekšējo ir kopīga mala. 
  Vārds, paslēpts tabulā, drīkst arī pārklāties pats ar sevi.

  Piemēram, šajā tabulā ir paslēpti vārdi :math:`\mathtt{SAULE}` un 
  :math:`\mathtt{SOS}`:  

  ===  ===  ===
  S    A    E
  O    U    L
  ===  ===  ===

  Aprakstīt algoritmu, kas noskaidro, vai dotais vārds garumā 
  :math:`w` paslēpts tabulā un pamatot, ka tas strādā laikā 
  :math:`O(wnm)`. 




  