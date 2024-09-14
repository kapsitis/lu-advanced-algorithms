# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 1</blue>

</hgroup><hgroup>

<span style="color:darkgreen">**(1) Ievads**</span>  
<span>(2) [Kļūdu detekcija un korekcija](#section-1)</span>  
<span>(3) [Kopsavilkums](#section-2)</span>

</hgroup>


<!--
* Izvākt vairumu R-S kodu uz 2.daļu. 
* Pievienot bildi, kurā 2d+1 attālums pamatots ar trijstūra nevienādību
* Pievienot bildi ar epsilon-apkārtnēm - pie Heminga kodu optimalitātes pierādījuma. 
* Atgādināt dzeltenajā slaidā par kreisi asociatīvām un labēji asociatīvām darbībām.

-->



--

## <lo-theory/> Mērķi

* Definēt kļūdu detekcijas un korekcijas atšķirības
* Pamatot apgalvojumu par divu kļūdu korekcijas kodu attālumu.
* Lietot un pamatot Heminga kodus. 




-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 1</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section-0)</span>  
<span style="color:darkgreen">**(2) Kļūdu detekcija un korekcija**</span>  
<span>(3) [Kopsavilkums](#section-2)</span>

</hgroup>


-----

# <lo-theory/> Kļūdu detekcija un korekcija

*Kļūdu detekcija:*

![Error detection](error-detection.png)<!-- .element: style="width:700px" -->

*Kļūdu korekcija:* Ideja visās metodēs - papildināt pārraidāmos datus ar 
papildinformāciju, cerot, ka papildinformācija ļaus pamanīt 
kļūdas. 

![Error detection](error-correction.png)<!-- .element: style="width:400px" -->


--

## <lo-summary/> Bitu paritātes metode

**Situācija:** Pārraida $n$ bitu virkni 
$x_1,x_2,\ldots,x_n \in \{ 0; 1\}$. 
Lai konstatētu iespējamu kļūdu $1$ bitā (kas var gan 
iestāties, gan neiestāties), pārraida $n+1$ bitus:  
Visus $x_1,x_2,\ldots,x_n$ un arī pēdējo bitu
$$\left( x_1 + x_2 + \ldots + x_n \right)\,\text{mod}\,2.$$

Pēdējais bits glabā visu iepriekšējo bitu paritāti. 
Tāpēc visu $n+1$ bitu paritāte ir $0$. Ja pārraidē rodas viena
kļūda, tad paritāte būs $1$, un kļūdu varēs konstatēt. 


--

## <lo-summary/> CRC kontrolsumma

![Ethernet frame](ethernet-frame.png)<!-- .element: style="width:600px" -->

<div style="font-size:70%">

"Frame Check Sequence" (FCS) izmanto 
32-bitu CRC (cyclical redundancy check). 
Tajā veic bitveida "XOR-ošanu stabiņā" ar maģisko 
skaitli `0xC704DD7B`. 

FCS 4 baitos ieraksta CRC doto atlikumu. Viena bita 
pārbaudīšana nav pietiekami droša; CRC32 ir noturīgāks
pret pārraides kļūdām, kas var pārmainīt vairākus blakusesošus
bitus. 

"Data link layer" (OSI Layer2) izmet tos freimus, 
kuri ir kļūdaini. Augstāka līmeņa transporta protokoli (TCP) 
palūdz kļūdainos freimus sūtīt atkārtoti. 

</div>

--

## <lo-summary/> MD5 hešfunkcija

Garākiem failiem (kuri varbūt tikuši bojāti apzināti) var 
izmantot hešfunkcijas. Piemēram MD5 izveido 128 bitu virknīti 
(pieraksta kā 32 hex ciparus). 

![Hešfunkcijas](hashtools-1.png)<!-- .element: style="width:400px" -->

MD5 hešfunkcijas kolīzijas ir zināmas.




-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 1</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section-0)</span>  
<span>(2) [Kļūdu detekcija un korekcija](#section-1)</span>  
<span style="color:darkgreen">**(3) Kopsavilkums**</span>

</hgroup>


