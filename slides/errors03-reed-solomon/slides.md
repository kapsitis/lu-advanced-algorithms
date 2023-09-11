# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span style="color:darkgreen">**(1) Ievads**</span>  
<span>(2) [Kļūdu korekcijas piemēri](#section-1)</span>  
<span>(3) [Rīda-Solomona kodi](#section-2)</span>  
<span>(4) [Galīgi lauki](#section-3)</span>  
<span>(5) [R-S kodu atkodēšana](#section-4)</span>  
<span>(6) [Berlekampa-Velča atkodēšana](#section-5)</span>  
<span>(7) [Kopsavilkums](#section-6)</span>

</hgroup>



-----

# <lo-why/> why

<div class="bigWhy">

Kāpēc kļūdu korekcijas algoritma izvēle (un pat atkodēšana) 
atkarīga no situācijas?

</div>
<div class="smallWhy">

* Kā vienkārši atkodēt Heminga kodus? 
* Kādu skaitļu pasaulē darbojas Rīda-Solomona kodi?

</div>




-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section)</span>  
<span style="color:darkgreen">**(2) Rīda-Solomona ievads**</span>  
<span>(3) [Rīda-Solomona kodi](#section-2)</span>  
<span>(4) [Galīgi lauki](#section-3)</span>  
<span>(5) [R-S kodu atkodēšana](#section-4)</span>  
<span>(6) [Berlekampa-Velča atkodēšana](#section-5)</span>  
<span>(7) [Kopsavilkums](#section-6)</span>

</hgroup>


-----

# <lo-theory/> Rīda-Solomona metodes ievads

* Ļauj labot lielu daudzumu kļūdu.
* Ziņojums pirms un pēc kodēšanas būs skaitļu virkne. 

**Metode:** Sadala datus grupās pa `$k$` skaitļiem.  
`$a_1,a_2,\ldots,a_k$` - viena grupa. Definē polinomu:  
`$$f(x) = a_1x^{k-1} + a_2x^{k-2}+\ldots + a_{k-1}x + a_k.$$`

Skaitļu `$a_1,\ldots,a_k$` vietā nosūta polinoma vērtības:
`$$f(0),f(1),\ldots,f(s-1)$$`
atbilstoši izraudzītam `$s>k$`.


--

## <lo-theory/> Rīda-Solomona kodu lietojumi

Patērētāju tehnoloģijas, kur nolasīšanā var rasties kļūdas

* Audio CD, DVD, Blu-ray diski, 
* QR codes, 
* Datu pārraide ar DSL un WiMAX, 
* Satelītu sakari, DVB un ATSC, 
* RAID 6.

[Reed-Solomon error correction](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction)


-----

# <lo-theory/> Algebras pamatteorēma

**Algebras pamatteorēma:** Polinomu
`$P(x)$` ar pakāpi `$n>0$` var vienā vienīgā veidā izteikt 
sekojošā veidā:
`$$P(x)=c(x-x_1)(x-x_2)\cdots(x-x_n),$$`
kur `$x_i$` ir polinoma `$P(x)$` (kompleksas) saknes.  
Izteikšanas veidus, kas atšķiras tikai ar reizinātāju secību 
uzskatām par vienādiem. Šeit 
`$c \neq 0$` un kompleksie skaitļi `$x_1,\ldots,x_n$`
ne obligāti ir visi dažādi. 



--

## <lo-theory/> Vienas sekas no pamatteorēmas

**Sekas 1:** Ja ir polinoms `$h(x)$` ar 
pakāpi ne lielāku par `$k$` un `$h(x) \neq 0$` 
(nav identiski vienāds ar `$0$`), 
tad ir ne vairāk kā `$k$` tādi `$x$`, kam 
`$h(x) = 0$`.  
Citiem vārdiem: `$h(x)$` ir ne vairāk 
kā `$k$` saknes.

**Pierādījums:** 
Izriet no algebras pamatteorēmas: ja sakņu `$x_i$`
būtu vairāk, `$h(x)$` varētu izteikt kā visu `$(x-x_i)$` 
reizinājumu. Atverot iekavas izrādītos, ka `$h(x)$` 
pakāpe pārsniedz `$k$`. Pretruna.


--

## <lo-theory/> Otras sekas no pamatteorēmas

<div style="font-size:80%">

**Sekas 2:** Ja diviem polinomiem `$f(x)$` un `$g(x)$` pakāpes
nepārsniedz `$k-1$` un to vērtības sakrīt `$k$` dažādos punktos, 
tad tie ir identiski vienādi.

**Pierādījums:** Atņemam abus polinomus un apzīmējam:
`$$h(x) = f(x)-g(x).$$`
Katrs punkts `$x_i$`, kur `$f(x)=g(x)$` ir sakne polinomam 
`$h(x)$`. Arī polinoma `$h(x)$` pakāpe nepārsniedz `$k-1$`. 
Ja sakņu būtu vairāk par `$k$`, tad `$h(x)$` būtu identiska nulle. 

*Piemēri:* Caur diviem punktiem var novilkt tikai vienu 
taisni (1.pakāpes polinomu) `$P(x)=a_1x+a_2$`.  
Caur trim punktiem `$(a_1,b_1)$`,`$(a_2,b_2)$`,`$(a_3,b_3)$`, 
kur `$a_1,a_2,a_3$` ir pa pāriem dažādi,
var novilkt tikai vienu parabolu vai taisni 
(t.i. 2.pakāpes vai 1.pakāpes polinomu, utt.).

</div>






-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section)</span>  
<span>(2) [Rīda-Solomona ievads](#section-1)</span>  
<span style="color:darkgreen">**(3) Rīda-Solomona kodi**</span>  
<span>(4) [Galīgi lauki](#section-3)</span>  
<span>(5) [R-S kodu atkodēšana](#section-4)</span>  
<span>(6) [Berlekampa-Velča atkodēšana](#section-5)</span>   
<span>(7) [Kopsavilkums](#section-6)</span>

</hgroup>


-----

# <lo-summary/> Rīda-Solomona koda analīze

Ja ir `$2$` ziņojumi: `$a_1,\ldots,a_k$` un 
`$b_1, \ldots, b_k$`, tad 
`$$f(x) = a_1x^{k-1} + a_2x^{k-2}+\ldots+a_{k-1}x + a_k,$$`
`$$g(x) = b_1x^{k-1} + b_2x^{k-2}+\ldots+b_{k-1}x + b_k.$$`

* Tā kā katram no šiem polinomiem pakāpe nepārsniedz `$k-1$`, 
tad `$f(x)$` un `$g(x)$` sakrīt ne vairāk kā `$k-1$` vietās. (Tās
ir otrās sekas no algebras pamatteorēmas.)
* Ja nosūta `$s$` polinoma vērtības, tad 
viņi atšķiras pārējās `$s - (k-1)$` vietās. 


--

## <lo-summary/> Cik no pārraidītajām drīkst būt kļūdas?

Augstāk redzējām, ka ja divi kodētie ziņojumi atšķiras vismaz 
`$2c+1$` vietās, tad kods spēj labot jebkuras `$c$` kļūdas. 

`$$s-(k-1) \geq 2c+1 \;\;\Rightarrow\;\; s - k \geq 2c \;\;\Rightarrow$$`
`$$\Rightarrow\;\;c \leq (s-k)/2$$`

* Rīda-Solomona kods spēj labot līdz `$(s-k)/2$` kļūdām. 
* Ja `$s=2k$`, tad var labot `$c \leq (2k-k)/2 = k/2$` kļūdas.
* Ja `$\leq 1/4$` no ziņojuma garumā `$2k$` saņem nepareizi, tad 
iespējams atgūt sākotnējo tekstu.


--

## <lo-sample/> Piemērs

* Cik kļūdas var labot, ja `$k=4$`, `$s=9$`, tad 
`$c \leq (s-k)/2 = 2.5$`. **Tātad varēs labot `$2$` kļūdas.**

* Kāpēc nevaram labot `$3$` kļūdas. Lai tās labotu, 
katriem diviem pārraidītajiem ziņojumiem jāatšķiras `$2c+1$` 
vietās (`$2\cdot 3 + 1 = 7$` vietās). 
* No algebras pamatteorēmas seko, ka `$f(x)$` un `$g(x)$` 
sakrīt ne vairāk kā `$k-1$` vietās un atšķiras vismaz
`$s - (k-1)$` vietās. 
* Tātad tieši `$s-(k-1)=6$` vietās var atšķirties. Tā ir pretruna: 
Ja mēģinātu labot `$3$` kļūdas, tad `$2$` kodus, kas atšķiras
`$6$` vietās, nevarētu atšķirt. 



--

## <lo-sample/> Piemērs ar polinomiem. 

`$$f(x) = x(x-1)(x-2) = x^3 - 3x^2 + 2x + 0.$$`
`$$g(x) = 2x(x-1)(x-2) = 2x^3 - 6x^2 + 4x + 0.$$`

Ja sākotnējās virknes ir `$(1;-3;2;0)$` un `$(2;-6;4;0)$`, 
tad pārraida ziņojumu argumentu vērtībām `$(0,1,2,3,4,5,6,7,8)$`: 
`$$0,0,0,f(3),f(4),f(5),g(6),g(7),g(8).$$`

Tas var rasties gan pārraidot `$f$` (ar kļūdām pēdējās `$3$` vietās), 
gan arī pārraidot `$g$` (ar kļūdām ziņojumos `$f(3),f(4),f(5)$`). 




-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section)</span>  
<span>(2) [Rīda-Solomona ievads](#section-1)</span>  
<span>(3) [Rīda-Solomona kodi](#section-2)</span>  
<span style="color:darkgreen">**(4) Galīgi lauki**</span>  
<span>(5) [R-S kodu atkodēšana](#section-4)</span>  
<span>(6) [Berlekampa-Velča atkodēšana](#section-5)</span>  
<span>(7) [Kopsavilkums](#section-6)</span>

</hgroup>


-----

# <lo-theory/> Galuā lauki un Rīds-Solomons

* Ja polinomus rēķina parastiem veseliem skaitļiem, tad to 
vērtības ātri kļūst lielas. 
* Rīda-Solomona kodiem veselo skaitļu vietā izmanto 
polinomu koeficientus un vērtības no galīga lauka,
piemēram `$\text{GF}\!\left(2^{12}\right)$` (Galuā lauks 
ar `$2^{12}$` elementiem).

[Sk. primitīvo polinomu sarakstu](https://www.partow.net/programming/polynomials/index.html), 
lai konstruētu `$\text{GF}\!\left(2^n\right)$` pakāpēm līdz `$2^{32}$`.




--

## <lo-theory/> Lauka jēdziens

<div style="font-size:80%">

**Definīcija:** Par <blue>*lauku*</blue> (*field*) sauc kopu `$L$`, 
kurā definētas operācijas `$+$` un `$\ast$` ar šādām īpašībām:

* Visurdefinētība: jebkuriem `$a$` un `$b$` ir definēts gan `$a+b$`, gan `$a \ast b$`.
* Komutativitāte: `$a + b = b + a$`,   
`$a \ast b = b \ast a$`.
* Asociativitāte: `$(a + b) + c = a + (b + c)$`,   
`$(a \ast b) \ast c = a \ast (b \ast c)$`.
* Distributivitāte: `$a \ast (b + c) = a \ast b + a \ast c$`.
* `$0$` elements: Eksistē elements `$0$` ar īpašību, ka `$0 + a = a$` jebkuram `$a$`.
* `$1$` elements: Eksistē elements `$1$` ar īpašību, ka `$1 \ast a = a$` jebkuram `$a$`.
* Apgriezto elementu eksistence:  
*saskaitīšanai:* Katram `$a$` eksistē `$-a$`, ka `$a + (-a) = 0$`,  
*reizināšanai:* Ja `$a \neq 0$`, tad eksistē `$a^{-1}$`, kuram `$a \ast a^{-1} = 1$`.

</div>



-----

# <lo-summary/> Bezgalīgi lauki

Lauks ir jebkura skaitļu vai citu objektu kopa, kurā var izpildīt visas četras aritmētiskās darbības
pēc parastajiem likumiem. 

* Racionālo skaitļu kopa `$\mathbb{Q}$` ir lauks (katrai racionālai daļai `$a/b$` eksistē pretējā: `$-a/b$` un 
apgrieztā: `$b/a$`). 
* Reālo skaitļu kopa `$\mathbb{R}$` ir lauks
* Komplekso skaitļu kopa `$\mathbb{C}$` (vai arī tikai 
to komplekso skaitļu kopa `$a+bi$`, kur `$a,b \in \mathbb{Q}$`) ir lauks. 
* Visu to nogriežņu garumu attiecību kopa, ko var uzkonstruēt ar cirkuli un lineālu (pievienojas 
kvadrātsaknes operācija, bet ne augstāku pakāpju saknes). 
* Visu racionālu daļu `$\frac{P(x)}{Q(x)}$` kopa ir lauks.


--

## <lo-summary/> Galīgi lauki

**Apgalvojums:** (1) Galīgs lauks ar elementu skaitu `$q$` eksistē
tad un tikai tad, ja `$q$` ir izsakāms kā pakāpe `$p^k$`, kur `$p$` ir pirmskaitlis, bet `$k=1,2,3,\ldots$`.  
Šo skaitu sauc arī par <emblue>kārtu</emblue> (<i>order</i>).  
(2) Ja `${\displaystyle q=p^{k}}$`, tad visi lauki ar kārtu `$q$` ir <emblue>izomorfi</emblue> (<i>isomorphic</i>) - 
to struktūra attiecībā pret saskaitīšanas un reizināšanas 
operācijām ir vienāda, atšķiras tikai elementu apzīmējumi. 

**Definīcija:** Galīgu lauku ar `$q = p^k$` elementiem sauc par <emblue>Galuā lauku</emblue> (<i>Galois field</i>); apzīmē `$\text{GF}(q)$` jeb
`$\text{GF}(p^k)$`. 


--

## <lo-summary/> GF pirmskaitļiem

<hgroup>

`$\text{GF}(2)$`: saskaitīšana
un reizināšana pēc moduļa `$2$`. 

<table class="optable">
<tr>
<td>$a+b$</td>
<th>$0$</th>
<th>$1$</th>
</tr>
<tr>
<th>$0$</th>
<td>$0$</td>
<td>$1$</td>
</tr>
<tr>
<th>$1$</th>
<td>$1$</td>
<td>$0$</td>
</tr>
</table>

&nbsp;

<table class="optable">
<tr>
<td>$a \ast b$</td>
<th>$0$</th>
<th>$1$</th>
</tr>
<tr>
<th>$0$</th>
<td>$0$</td>
<td>$0$</td>
</tr>
<tr>
<th>$1$</th>
<td>$0$</td>
<td>$1$</td>
</tr>
</table>

</hgroup>
<hgroup>

`$\text{GF}(3)$`: saskaitīšana
un reizināšana pēc moduļa `$3$`. 

<table class="optable">
<tr>
<td>$a+b$</td>
<th>$0$</th>
<th>$1$</th>
<th>$2$</th>
</tr>
<tr>
<th>$0$</th>
<td>$0$</td>
<td>$1$</td>
<td>$2$</td>
</tr>
<tr>
<th>$1$</th>
<td>$1$</td>
<td>$2$</td>
<td>$0$</td>
</tr>
<tr>
<th>$2$</th>
<td>$2$</td>
<td>$0$</td>
<td>$1$</td>
</tr>
</table>

&nbsp;

<table class="optable">
<tr>
<td>$a \ast b$</td>
<th>$0$</th>
<th>$1$</th>
<th>$2$</th>
</tr>
<tr>
<th>$0$</th>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
</tr>
<tr>
<th>$1$</th>
<td>$0$</td>
<td>$1$</td>
<td>$2$</td>
</tr>
<tr>
<th>$2$</th>
<td>$0$</td>
<td>$2$</td>
<td>$1$</td>
</tr>
</table>


</hgroup>


--

## <lo-sample/> Ja q nav pirmskaitlis

* Aplūkojam `$\text{GF}(8)$`. Nevar
izmantot saskaitīšanu un reizināšanu pēc `$8$` moduļa, jo 
`$2 \cdot 0 = 2 \cdot 4 = 0$`  un `$2 \cdot 1 = 2 \cdot 5 = 2$`.
* Neeksistēs `$2^{-1}$`, jo skaitlis `$2 \neq 0$` reizināšanā `$(\text{mod} 8)$` salipina rezultātus: 
Var gadīties, ka `$a \neq b$`, bet `$2a = 2b$`. 
* Atlikumus pēc moduļiem `$q$`, kas **nav** pirmskaitļi var aplūkot
(piemēram, paturot tikai tos, kas ir savstarpēji pirmskaitļi ar `$q$`), bet
tie veido tikai multiplikatīvu grupu, nevis lauku. 

<red>**Svarīga piezīme:**</red> Modulārā aritmētika `$(\text{mod}\,q)$` veido 
laukus tad un tikai tad, ja `$q$` ir pirmskaitlis. Ja `$q = p^k$` (`$k > 1$`), 
`$\text{GF}(q)$` jākonstruē ar citu metodi. 

* [Multiplikatīvas grupas pēc jebkura moduļa](https://en.wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n)
* [Galīgi lauki](https://en.wikipedia.org/wiki/Finite_field)


--

## <lo-sample/> Piemērs: GF(8)

* `$p(x) = x^3 + x + 1$` ir <blue>*nereducējams*</blue> (*irreducible*) 
polinoms; citiem vārdiem - to nevar sadalīt reizinātājos tā, lai 
reizinātāju koeficienti būtu veseli skaitļi.
* Veidojam visus iespējamos "atlikumus", dalot ar polinomu `$p(x)$`, 
turklāt šo polinomu koeficientus visur saskaitām un reizinām pēc moduļa `$2$`. 
* Tad visi `$8$` iespējamie atlikumi veido Galuā lauku `$\text{GF}\!\left(2^3\right)$`: 
`$$0,\;1,\;x,\;x+1,\;x^2,\;x^2+1,\;x^2+x,\;x^2+x+1.$$`




--

## <lo-sample/> Saskaitīšana un reizināšana GF(8)

<div style="font-size:60%">

<table class="optable">
<tr>
<td>$P(x)+Q(x)$</td>
<th>$0$</th>
<th>$1$</th>
<th>$x$</th>
<th>$x+1$</th>
<th>$x^2$</th>
<th>$x^2+1$</th>
<th>$x^2+x$</th>
<th>$x^2+x+1$</th>
</tr>
<tr>
<th>$0$</th>
<td>$0$</td>
<td>$1$</td>
<td>$x$</td>
<td>$x+1$</td>
<td>$x^2$</td>
<td>$x^2+1$</td>
<td>$x^2+x$</td>
<td>$x^2+x+1$</td>
</tr>
<tr>
<th>$1$</th>
<td>$1$</td>
<td>$0$</td>
<td>$x+1$</td>
<td>$x$</td>
<td>$x^2+1$</td>
<td>$x^2$</td>
<td>$x^2+x+1$</td>
<td>$x^2+x$</td>
</tr>
<tr>
<th>$x$</th>
<td>$x$</td>
<td>$x+1$</td>
<td>$0$</td>
<td>$1$</td>
<td>$x^2+x$</td>
<td>$x^2+x+1$</td>
<td>$x^2$</td>
<td>$x^2+1$</td>
</tr>
<tr>
<th>$x+1$</th>
<td>$x+1$</td>
<td>$x$</td>
<td>$1$</td>
<td>$0$</td>
<td>$x^2+x+1$</td>
<td>$x^2+x$</td>
<td>$x^2+1$</td>
<td>$x^2$</td>
</tr>
<tr>
<th>$x^2$</th>
<td>$x^2$</td>
<td>$x^2+1$</td>
<td>$x^2+x$</td>
<td>$x^2+x+1$</td>
<td>$0$</td>
<td>$1$</td>
<td>$x$</td>
<td>$x+1$</td>
</tr>
<tr>
<th>$x^2+1$</th>
<td>$x^2+1$</td>
<td>$x^2$</td>
<td>$x^2+x+1$</td>
<td>$x^2+x$</td>
<td>$1$</td>
<td>$0$</td>
<td>$x+1$</td>
<td>$x$</td>
</tr>
<tr>
<th>$x^2+x$</th>
<td>$x^2+x$</td>
<td>$x^2+x+1$</td>
<td>$x^2$</td>
<td>$x^2+1$</td>
<td>$x$</td>
<td>$x+1$</td>
<td>$0$</td>
<td>$1$</td>
</tr>
<tr>
<th>$x^2+x+1$</th>
<td>$x^2+x+1$</td>
<td>$x^2+x$</td>
<td>$x^2+1$</td>
<td>$x^2$</td>
<td>$x+1$</td>
<td>$x$</td>
<td>$1$</td>
<td>$0$</td>
</tr>
</table>


&nbsp;


<table class="optable">
<tr>
<td>$P(x) \ast Q(x)$</td>
<th style="width:11%">$0$</th>
<th>$1$</th>
<th>$x$</th>
<th>$x+1$</th>
<th>$x^2$</th>
<th>$x^2+1$</th>
<th>$x^2+x$</th>
<th>$x^2+x+1$</th>
</tr>
<tr>
<th>$0$</th>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
<td>$0$</td>
</tr>
<tr>
<th>$1$</th>
<td>$0$</td>
<td>$1$</td>
<td>$x$</td>
<td>$x+1$</td>
<td>$x^2$</td>
<td>$x^2+1$</td>
<td>$x^2+x$</td>
<td>$x^2+x+1$</td>
</tr>
<tr>
<th>$x$</th>
<td>$0$</td>
<td>$x$</td>
<td>$x^2$</td>
<td>$x^2+x$</td>
<td>$x+1$</td>
<td>$1$</td>
<td>$x^2+x+1$</td>
<td>$x^2+1$</td>
</tr>
<tr>
<th>$x+1$</th>
<td>$0$</td>
<td>$x+1$</td>
<td>$x^2+x$</td>
<td>$x^2+1$</td>
<td>$x^2+x+1$</td>
<td>$x^2$</td>
<td>$1$</td>
<td>$x$</td>
</tr>
<tr>
<th>$x^2$</th>
<td>$0$</td>
<td>$x^2$</td>
<td>$x+1$</td>
<td>$x^2+x+1$</td>
<td>$x^2+x$</td>
<td>$x$</td>
<td>$x^2+1$</td>
<td>$1$</td>
</tr>
<tr>
<th>$x^2+1$</th>
<td>$0$</td>
<td>$x^2+1$</td>
<td>$1$</td>
<td>$x^2$</td>
<td>$x$</td>
<td>$x^2+x+1$</td>
<td>$x+1$</td>
<td>$x^2+x$</td>
</tr>
<tr>
<th>$x^2+x$</th>
<td>$0$</td>
<td>$x^2+x$</td>
<td>$x^2+x+1$</td>
<td>$1$</td>
<td>$x^2+1$</td>
<td>$x+1$</td>
<td>$x$</td>
<td>$x^2$</td>
</tr>
<tr>
<th>$x^2+x+1$</th>
<td>$0$</td>
<td>$x^2+x+1$</td>
<td>$x^2+1$</td>
<td>$x$</td>
<td>$1$</td>
<td>$x^2+x$</td>
<td>$x^2$</td>
<td>$x+1$</td>
</tr>


</table>


</div>



-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section)</span>  
<span>(2) [Rīda-Solomona ievads](#section-1)</span>  
<span>(3) [Rīda-Solomona kodi](#section-2)</span>  
<span>(4) [Galīgi lauki](#section-3)</span>  
<span style="color:darkgreen">**(5) R-S kodu atkodēšana**</span>  
<span>(6) [Berlekampa-Velča atkodēšana](#section-5)</span>  
<span>(7) [Kopsavilkums](#section-6)</span>

</hgroup>



-----

# <lo-theory> Galīgie lauki R-S kodos

<div style="font-size:80%">

`$\text{GF}(p^k)$` elementus (kuri paši bieži izskatās kā polinomi!) izmanto kā koeficientus Solomona-Rīda
algoritmā esošajos polinomos - viņi tur ir gan argumenti, gan vērtības.

Izvēlamies galīgu lauku `$\text{GF}(q)$`. Datus pārveidojam par šī lauka elementu virkni.
Virknes elementus sadalām blokos garumā `$k$`:  
`$a_0, a_1, \ldots, a_{k-1}$` (kur `$k < q$`). Definējam polinomu
`$$f(x) = a_{k-1} x^{k-1} + \ldots + a_1 x + a_0.$$`
Izrēķinām vērtības `$f(a_0), f(a_1), \ldots, f(a_{s-1})$` galīgā lauka elementiem `$a_0, a_1, \ldots, a_{s-1} \in \text{GF}(q)$`,
par darbībām izmantojot `$+$` un `$\ast$`, kas definētas šajā galīgajā laukā.

</div>


--

## <lo-theory/> R-S kodēšana un atkodēšana

<div style="font-size:80%">

Atkodēšanas algoritms un izlabojamo kļūdu skaits nemainās, 
jo pierādījumā par kļūdu korekcijas spējām neizmanto neko
tādu, kas neizpildās patvaļīgam laukam. 
Galīgi lauki toties ļauj izvairīties 
no darbībām ar lieliem skaitļiem.

**Piemēri ar `$\text{GF}(5)$`:** Turpmākajos trijos piemēros izmantojam galīgu lauku 
`$$\text{GF}(5) = \{0, 1, 2, 3, 4\},$$` 
kur aritmētiskās darbības notiek pēc moduļa `$5$`.   
Informāciju kodē ar `$2$` pakāpes polinomu
`$f(x) = a \cdot x^2 + b \cdot x + c$`,
ņemot 5 polinoma vērtības: 
`$f(0)$`, `$f(1)$`, `$f(2)$`, `$f(3)$` un `$f(4)$`.

</div>


-----

# <lo-sample/> Piemērs Nr.1

Nokodēt `$3, 2, 1$`.  
Izmantot polinomus ar koeficientiem, argumentiem un vērtībām no `$\text{GF}(5)$`. 


--

## <lo-soln/> Piemērs Nr.1: Risinājums

<div style="font-size:80%">

Ņemam polinomu
`$f(x) = 3\cdot{}x^2 + 2\cdot{}x + 1$`.

Izrēķinām vērtības

`$$\left\{ \begin{array}{l}
f(0) = 3\cdot{}0^2 + 2\cdot{}0 + 1 = 1,\\
f(1) = \left(3\cdot{}1^2 + 2\cdot{}1 + 1\right)\;\text{mod}\;5 = 6\;\text{mod}\;5 = 1,\\
f(2) = \left(3\cdot{}2^2 + 2\cdot{}2 + 1\right)\;\text{mod}\;5 = 17\;\text{mod}\;5 = 2,\\
f(3) = \left(3\cdot{}3^2 + 2\cdot{}3 + 1\right)\;\text{mod}\;5 = 34\;\text{mod}\;5 = 4,\\
f(4) = \left(3\cdot{}4^2 + 2\cdot{}4 + 1\right)\;\text{mod}\;5 = 57\;\text{mod}\;5 = 2.
\end{array} \right.$$`

Tātad, tiek pārraidītas vērtības `$1, 1, 2, 4, 2$`.

</div>



-----

# <lo-sample/> Piemērs Nr.2

Atkodēt `$1, 1, \ast, 4, \ast$`, kur `$\ast$` ir pazaudēta vērtība (saņemtās vērtības visas ir pareizas).  
Izmantot polinomus ar koeficientiem, argumentiem un vērtībām no `$\text{GF}(5)$`. 


--

## <lo-soln/> Piemērs Nr.2: Risinājums - 1

<div style="font-size:80%">

Sastādām vienādojumu sistēmu (pēc mod `$5$`):

`$$\left\{ \begin{array}{l}
0^2\cdot{}a + 0\cdot{}b + c \equiv 1\;(\text{mod}\,5),\\
1^2\cdot{}a + 1\cdot{}b + c \equiv 1\;(\text{mod}\,5),\\
3^2\cdot{}a + 3\cdot{}b + c \equiv 4\;(\text{mod}\,5).
\end{array} \right.$$`

Tā kā `$3^2 = 9 \equiv 4\;(\text{mod}\,5)$`: 

`$$\left\{ \begin{array}{l}
c \equiv 1\;(\text{mod}\,5),\\
a + b + c \equiv 1\;(\text{mod}\,5),\\
4 a + 3 b + c \equiv 4\;(\text{mod}\,5).
\end{array} \right.$$`

--

## <lo-soln/> Piemērs Nr.2: Risinājums - 2

<div style="font-size:80%">

`$$\left\{ \begin{array}{l}
\mbox{}a + b = 1 - 1 = 0\;(\text{mod}\,5),\\
4 a + 3 b = 4 - 1 = 3\;(\text{mod}\,5).
\end{array} \right.$$`


Atrisinām šo divu vienādojumu sistēmu ar izslēgšanas metodi. Pareizinot pirmo
vienādojumu ar `$3$` un atņemot no otrā vienādojuma iegūst
`$$(4a+3b) - 3(a+b) = a = 3 - 3\cdot{}0 \equiv 3\;(\text{mod}\,5).$$`

No vienādojuma `$a + b \equiv 0\;(\text{mod}\,5)$` iegūstam, ka
`$b = 0 - 3 = -3 = 2\;(\text{mod}\,5)$`. Tātad polinoms bija
`$$f(x)=3x^2 + 2x + 1.$$`

</div>


-----

# <lo-sample/> Piemērs Nr.3

Atkodēt `$2, 3, \ast, \ast, 2$`, kur `$\ast$` ir pazaudēta vērtība (saņemtās vērtības visas ir pareizas).
Izmantot polinomus ar koeficientiem, argumentiem un vērtībām no `$\text{GF}(5)$`. 


--

## <lo-soln/> Piemērs Nr.3: Risinājums - 1

<div style="font-size:70%">

Sastādām vienādojumu sistēmu (pēc mod 5):

`$$\left\{ \begin{array}
\mbox{}0^2 \cdot a + 0 \cdot b + c \equiv 2\;(\text{mod}\,5),\\
1^2 \cdot a + 1 \cdot b + c \equiv 3\;(\text{mod}\,5),\\
4^2 \cdot a + 4 \cdot b + c \equiv 2\;(\text{mod}\,5).
\end{array} \right.$$`

Tā kā `$4^2 = 16 \equiv 1\;(\text{mod}\,5)$`, tad šo sistēmu var pārrakstīt:

`$$\left\{ \begin{array}
\mbox{}c \equiv 2\;(\text{mod}\,5),\\
a + b + c \equiv 3\;(\text{mod}\,5),\\
a + 4 \cdot{} b + c \equiv 2\;(\text{mod}\,5).
\end{array} \right.$$`

Ievietojot `$c=2$` otrajā un trešajā vienādojumā, iegūstam

`$$\left\{ \begin{array}
\mbox{}a + b = 3 - 2 \equiv 1\;(\text{mod}\,5),\\
a + 4 b = 2 - 2 \equiv 0\;(\text{mod}\,5).
\end{array} \right.$$`

</div>



--

## <lo-soln/> Piemērs Nr.3: Risinājums - 2

<div style="font-size:70%">

`$$\left\{ \begin{array}
\mbox{}a + b = 3 - 2 \equiv 1\;(\text{mod}\,5),\\
\mbox{}a + 4 b = 2 - 2 \equiv 0\;(\text{mod}\,5).
\end{array} \right.$$`

Atrisinām šo sistēmu ar izslēgšanas metodi. Atņemot pirmo
vienādojumu no otrā:

`$$(a+4b)-(a+b) = 3b = 0 - 1 \equiv 4\;(\text{mod}\,5).$$`

Jāatrisina `$3b \equiv 4\;(\text{mod}\,5).$`

*Piezīme:* Atrisinājums nebūs daļskaitlis 4/3, jo tas nav lauka elements!
Pārbaudot `$b = 0, 1, 2, 3, 4$`, secinām, ka `$3 \cdot 3 = 9 \equiv 4\;(\text{mod}\,5)$`.   
Tātad `$b \equiv 3\;(\text{mod}\,5)$`.  
*Piezīme:* Ir algoritmi, kā atrast `$b$`, neizmantojot pilno pārlasi. Bet priekš `$(\text{mod}\,5)$`, 
iespējamo `$b$` ir tik maz, ka pārlase ir ātrāka.

No vienādojuma `$a + b \equiv 1\;(\text{mod}\,5)$` iegūstam, ka
`$a = 1 - 3 = -2 \equiv 3\;(\text{mod}\,5)$`. Tātad polinoms bija
`$$f(x) = 3 x^2 + 3x + 2.$$`


</div>




-----

# <lo-theory/> Lagranža interpolācija

<div style="font-size:70%">

Vēl viens veids, kā veikt atkodēšanu ir interpolācija 
(labi strādā pie neliela polinomu skaita un pakāpēm). 

Ja zinām, ka
`$$f(x_1)=r_1;\;\;f(x_2)=r_2;\;\;\ldots,\;\;f(x_k)=r_k,$$`
tad definējam polinomus:

$$f_i (x) = \frac{(x-r_1)\cdot\ldots\cdot(x-r_{i-1})\cdot(x-r_{i+1})\cdot\ldots\cdot(x-r_k)}
{(r_i-r_1)\cdot\ldots\cdot(r_i-r_{i-1})\cdot(r_i-r_{i+1})\cdot\ldots\cdot(r_i-r_k)}.$$

Šiem polinomiem `$f_i(x)$` ir šādas īpašības:  
(1) Ja `$x=r_i$`, tad `$f_i(x) = 1$`,<br/>
(2) Ja `$x=r_j$`, (`$i \neq j$`), tad `$f_i(x)=0$`, jo kaut kur polinomā ir reizinātājs 
`$(x-r_j)=0$`, kas visu reizinājumu padara par `$0$`.

</div>


--

## <lo-theory/> Interpolāciju lietošana atkodēšanai

Meklētais polinoms ir:
`$$f(x) = r_1 \cdot f_1(x) + r_2 \cdot f_2 (x) + \ldots + r_k \cdot f_k (x).$$`

Kāpēc šis polinoms dod pareizu rezultātu?
Ja `$x = r_i$`, tad visi `$f_j(x)$` (`$i \neq j$`) vienādi ar `$0$`, 
un vienīgi `$f_i (r_i) = 1$`. 

Tātad `$f(r_i) = r_i  \cdot f_i(r_i) = r_i$`.   
Ja vienīgais kļūdu veids ir dažu vērtību pazušana, tad pietiek ar šo pieeju.


--

## <lo-summary/> Interpolācija, ja var būt citas kļūdas

Ja ir kļūdas, kurās vienas vērtības vietā ir saņemta cita, tad ir grūtāk:  
`$k$`: sākotnējie skaitļi;   
`$s$` pārraidītās vērtības: `$(f(0), f(1), \ldots, f(s-1))$`.

* `$c \leq (s-k)/2$`: maksimālais pieļaujamais kļūdu skaits, 
* Vismaz `$s-c$` vērtības ir pareizas.

Rezultātā ir pietiekami daudz pareizo vērtību, lai atrastu kļūdas, taču nezinām
tieši kuras ir pareizas, lai tās varētu izmantot kļūdu meklēšanā.




-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section)</span>  
<span>(2) [Rīda-Solomona ievads](#section-1)</span>  
<span>(3) [Rīda-Solomona kodi](#section-2)</span>  
<span>(4) [Galīgi lauki](#section-3)</span>  
<span>(5) [R-S kodu atkodēšana](#section-4)</span>  
<span style="color:darkgreen">**(6) Berlekampa-Velča atkodēšana**</span>  
<span>(7) [Kopsavilkums](#section-6)</span>

</hgroup>



-----

# <lo-theory/> Polinoms Y(x) - kļūdu lokators

<div style="font-size:70%">

Berlekampa-Velča algoritms ir Rīda-Solomona atkodēšanas metode, ko lieto tad, 
ja iespējama ne tikai datu pazušana, bet arī nepareizu datu saņemšana pareizo datu vietā.
Ieviešam apzīmējumus:

* Kļūdas ir `$x_1, x_2, \ldots, x_c$` (pagaidām nezināmās vietās)
* Pārraidītais polinoms bija `$k-1$` pakāpes polinoms `$p(x)$`
* Vērtību `$p(x_i)$` vietā saņemtās vērtības apzīmējam ar `$r_i$`.
* Atskaitot `$c$` vērtības (punktos `$x_1,\ldots,x_c$`), citas vērtības ir pareizas.

Definējam kļūdu lokatoru:
`$$Y(x) = (x-x_1)(x-x_2) \ldots (x-x_c).$$`
Polinoma pakāpe `$\text{deg}\,Y(x) \leq c$`. 
Šis polinoms ir `$0$` visām tām argumenta vērtībām `$x_i$`, kurām saņemta nepareiza `$p(x)$` vērtība.

</div>


--

## <lo-theory/> Polinoms Z(x): Y(x) un p(x) reizinājums

<div style="font-size:70%">

Definējam polinomu `$Z(x)$`, kas ir kļūdu lokatora un sākotnējā polinoma reizinājums:
`$$Z(x) = Y(x) \cdot p(x).$$`
Pakāpe `$\text{deg}\,Z(x) = \text{deg}\,Y(x) + \text{deg}\,p(x) \leq c+(k-1) = k + c - 1$`.

Iedomājamies, ka protam atrast `$Y$` un `$Z$`. Tad, izdalot abas vienādības puses ar `$Y$`, iegūstam
`$p(x) = Z(x) / Y(x)$`.

Tātad, lai atrastu `$p(x)$`, pietiek izrēķināt `$Z(x)$` un `$Y(x)$`.
Ja `$r$` ir vērtība, kas saņemta kā `$p(x)$`, tad
`$$Z(x) = Y(x) \cdot r.$$`

Šāda vienādība ir spēkā, jo  
(1) Ja `$r = p(x)$`, tad `$Z(x) = Y(x) \cdot p(x)$` - ir saņemta pareiza vērtība  
(2) Ja `$r \neq p(x)$`, tad `$Y(x) = 0$` un `$Z(x) = 0$`.

Tātad `$Z(x) = Y(x) \cdot r$` ir spēkā visos `$s$` pārraidītajos punktos.

</div>


--

## <lo-theory/> Y, Z atrašana

<div style="font-size:70%">

Pieņemsim, ka
`$$Y(x) = b_c x^c + b_{c-1} x^{c-1} + \ldots + b_0.$$`
Tā kā `$p(x)$` – polinoms ar pakāpi `$k-1$`, tad
`$$Z(x) = a_{k+c-1} x^{k+c-1} + a_{k+c-2} x^{k+c-2} + \ldots + a_0.$$`

* polinoms ar pakāpi `$c$`
* polinoms ar pakāpi `$k+c-1$`

Katra saņemtā vērtība dod pa vienam nosacījumam:

`$$\left\{ \begin{array}{l}
Z(0) = Y(0) \cdot r_0\\
Z(1) = Y(1) \cdot r_1\\
\ldots\\
Z(s-1) = Y(s-1) \cdot r_{s-1}
\end{array} \right.$$`


--

## <lo-theory/> Y, Z atrašana (turpinājums)

<div style="font-size:70%">

`$$\left\{ \begin{array}{l}
Z(0) = Y(0) \cdot r_0\\
Z(1) = Y(1) \cdot r_1\\
\ldots\\
Z(s-1) = Y(s-1) \cdot r_{s-1}
\end{array} \right.$$`

Katrā nosacījumā ievietojot `$i$` un `$r_i$`, iegūst vienādojumu, 
kura nezināmie ir `$a_0, \ldots, a_{k+c-1}, b_0, \ldots b_c$`. 

`$Z(i) = Y(i) \cdot r_i$` - `$s$` vienādojumu sistēma ar `$k+2 \cdot c +1$` nezināmajiem.
Atrisinām šo vienādojumu sistēmu un no nezināmajiem iegūstam `$Z(x)$` un `$Y(x)$`. Tad
izmantojot `$p(x) = Z(x)/Y(x)$` aprēķinām `$p(x)$`.

</div>


-----

# <lo-theory/> Jautājumi par Berlekampu-Velču

<hgroup style="font-size:70%">

**Jautājumi:**

1. Vai vienādojumu sistēmai ir atrisinājums?
2. Vai vienādojumu sistēmai nav vairāki atrisinājumi?
3. Vai varam atrast algoritmisku metodi, kā atrisināt vienādojumu sistēmu?

</hgroup>

<hgroup style="font-size:70%">

**Atbildes:**

1. Jā, atrisinājums vienmēr būs pareizais (meklējamais) `$Y(x)$` un `$Z(x)$` polinomu
pāris, jo tas apmierina visus nosacījumus.
2. Principā varētu būt vairāki atrisinājumi `$(Y(x), Z(x))$` un `$(Y’(x), Z’(x))$` un
`$Z(x)/Y(x) \neq Z’(x)/Y’(x)$`.  
Vai tā var būt?  
Ja tiek pārraidītas pietiekami daudzas vērtības, tad atrisinājums izrādīsies viennozīmīgi
noteikts `$(Y(x), Z(x))$`.
3. Jā; tālākos slaidos piedāvāsim pakāpeniskas izslēgšanas metodi.

</hgroup>


--

## <lo-theory/> Berlekampa-Velča atrisināmība

<div style="font-size:70%">

**Apgalvojums:** Doti polinomi `$Y$` un `$Z$`, kuriem:  
(1) `$\text{deg}\,Y \leq c$`,  
(2) `$\text{deg}\,Z \leq k + c - 1$`  
(3) `$Y \neq 0$`
un visiem `$i$`: `$Z(i) = Y(i) \cdot r_i$`. Pieņemsim, ka `$Y’, Z’$` vēl divi polinomi ar tādām pašām īpašībām.   
Tad `$Z(x)/Y(x) = Z’(x)/Y’(x)$`.

**Pierādījums:**  
`$Z(i) = Y(i) \cdot r_i$`, kur `$r_i$` – saņemtā vērtība priekš `$p(i)$`.  
`$Z’(i) = Y’(i) \cdot r_i$`. 

Sareizinām krustiski un iegūstam
`$$Z(i) \cdot Y’(i) \cdot r_i = Z’(i) * Y(i) * r_i.$$`

Noīsinām `$r_i$` un iegūstam
`$$Z(i) \cdot Y’(i) = Z’(i) * Y(i)$$`

</div>


--

## <lo-summary/> Berlekampa-Velča atrisināmība (turpinājums)

<div style="font-size:70%">

`$Z’(i) \cdot Y(i)$` pakāpe ir `$k + 2c + 1$`. 

Mainīgais `$i$` pieņem vērtības `$0, 1, \ldots, s-1$`.  
`$Z(i) \cdot Y’(i)$` un `$Z’(i) \cdot Y(i)$` sakrīt pie `$s$` dažādiem `$x$`.

> *Algebras pamatteorēma:* Ja divi polinomi ir dažādi, tad maksimālais 
> argumentu skaits, pie kuriem tie sakrīt, ir šo polinomu pakāpju maksimums.

Tas nozīmē, ka, ja `$k+c-1<s$`, tad `$Z(i) \cdot Y’(i) = Z’(i) \cdot Y(i)$`.  
Izdalām abas puses ar `$Y(x)$` un `$Y’(x)$` un iegūstam
`$$Z(x) / Y(x) = Z’(x) / Y’(x)$$`

</div>


--

## <lo-summary/> Algoritmiska Berlekampa-Velča atrisināšana

Nosacījumos `$Z(i) = Y(i) \cdot r_i$` ievietojot `$i$` un `$r_i$`, 
iegūst lineārus vienādojumus ar nezināmajiem `$a_i$`, `$b_i$`, 
kuriem ir koeficienti `$y_i$` un `$z_i$`:
`$$y_{1,1} a_{k+c-1} + \ldots + y_{1,k+c} a_0 = z_{1,1} b_c + \ldots + z_{1,c+1}b_0.$$`
Ja lineārai vienādojumu sistēmai ir atrisinājums, tad izslēdzot pa vienam
mainīgajam (ar apzīmēšanas palīdzību) var atrast atrisinājumu.




-----

# &nbsp;

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Kļūdu korekcija - 2</blue>

</hgroup><hgroup>

<span>(1) [Ievads](#section)</span>  
<span>(2) [Rīda-Solomona ievads](#section-1)</span>  
<span>(3) [Rīda-Solomona kodi](#section-2)</span>  
<span>(4) [Galīgi lauki](#section-3)</span>  
<span>(5) [R-S kodu atkodēšana](#section-4)</span>  
<span>(6) [Berlekampa-Velča atkodēšana](#section-5)</span>  
<span style="color:darkgreen">**(7) Kopsavilkums**</span>


</hgroup>


-----

# <lo-theory/> Ko darījām nodarbībā

* Nokodējām un atkodējām Heminga kodus
* Definējām Rīda-Solomona kodus
* Saskaitījām un reizinājām galīgu lauku elementus
* Aplūkojām dažas Rīda-Solomona kodu atkodēšanas metodes, t.sk. Berlekampa-Velča algoritmu.
* Aplūkojām dažus vienkāršus Tornado kodu piemērus.







