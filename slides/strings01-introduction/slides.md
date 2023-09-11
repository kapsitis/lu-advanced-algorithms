# Introduction<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 1</blue>

</hgroup><hgroup style="font-size:90%">

<span style="color:darkgreen">**(1) Ievads**</span>  
<span>(2) [Pamatfakti un naivais algoritms](#/naive-algorithm)</span>  
<span>(3) [Levenšteina attālums](#/levenshtein-distance)</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>

<!--
Meklēšana virknēs - 2
------
Ievads
Galīgi automāti
Bojera-Mūra algoritms
BM algoritma pareizība
(P) Regulāru izteiksmju atrašana
Kopsavilkums



Meklēšana virknēs - 3
------------
Ievads
Rekursīvu algoritmu sarežģītība
Dinamiskā programmēšana
Sufiksu koku jēdziens
Ukkonena algoritms
(P) Failu digitālnospiedumi (fingerprinting) un Blūma filtri
Kopsavilkums
-->




-----


# <lo-why/> why

<div class="bigWhy">

Kāpēc nepieciešami ātri un daudzveidīgi 
virkņu/stringu meklēšanas algoritmi?

</div>

<div class="smallWhy">

* Teksta redaktori un dokumentu skatītāji
* Datu noplūdes novēršana, *Data Leak Prevention (DLP)*
* Dokumentu atrašana *Document retrieval*, Lucene/Elasticsearch.
* Plaģiāta meklēšana.

</div>



--

## <lo-summary/> Nodarbības mērķi 

* Lietot naivo stringu meklēšanas algoritmu. 
* Analizēt naivā algoritma sarežģītību.
* Analizēt Rabina-Karpa algoritmu, tā sarežģītību.
* Veidot KMP algoritma starprezultātu struktūras.
* Pamatot KMP algoritma pareizību un sarežģītību.


--

## <lo-summary/> Stringu meklēšanas lietojumi

* Teksta redaktori: 1 vārds, 1 dokuments
* Datu noplūdes novēršana (DLP): daudzi paraugi (vārdi, reg.izteiksmes), 
1 pārbaudāmais dokuments.
* Dokumentu atrašana (*Document retrieval*): nedaudzi paraugi, daudzi dokumenti, kam 
drīkst veikt priekšapstrādi/indeksāciju.
* Plaģiāta meklēšana: Daudzi dokumenti, 1 pārbaudāmais dokuments, atrast 
"kopētos-ielīmētos" (*Copy-Paste*) gabalus vai "kopētos-ielīmētos" un drusku parediģētos.







-----

# Naive Algorithm<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 1</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span style="color:darkgreen">**(2) Pamatfakti un naivais algoritms**</span>  
<span>(3) [Levenšteina attālums](#/levenshtein-distance)</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>


-----

# <lo-theory/> Uzdevuma izklāsts

<div style="font-size:80%">

Dots <emblue>teksts</emblue> (*text*) - virkne no `$n$` simboliem:
`$$T = T[0], \ldots, T[n-1]$$`

Dots arī <emblue>paraugs</emblue> (*pattern*) - virkne no `$m$` simboliem:
`$$P = P[0], \ldots, P[m-1]$$`

Vai virknē `$T$` ir atrodama apakšvirkne `$P$` (algoritms izvada vai nu tikai 1.pozīciju, kur `$P$` ieiet virknē `$T$`, 
vai arī tas izvada visas pozīcijas).

**Definīcija:** Pozīciju tekstā `$T$` (skaitli no `$0$` līdz `$n-1$`), kur var sākties meklējamais
paraugs sauc par <emblue>nobīdi</emblue> (*shift*). 

</div>


--

## <lo-theory/> Apakšstringi un apakšvirknes

<div style="font-size:70%">

<emblue>Virkne</emblue> var nozīmēt gan "sequence" (galīga vai bezgalīga, 
no jebkāda veida objektiem), gan "string" (galīga virkne ar galīga alfabēta burtiem). 
Parasti <emblue>virkni</emblue> var droši lietot kā sinonīmu vārdam <emblue>strings</emblue>, 
bet ir daži izņēmumi. 

**Definīcija:** Par virknes `$T[0],T[1],\ldots,T[n-1]$` <emblue>apakšstringu</emblue> (*substring*) sauc 
simbolu virkni no `$T[i]$` (ieskaitot virknes garumā `$0,1,2,\ldots$`), kur `$i$` vērtības seko pēc kārtas.  
(Apakšstringu iegūst, sākotnējai virknei nosvītrojot (varbūt tukšus) gabalus sākumā un beigās.)

**Definīcija:** Par virknes `$T[0],T[1],\ldots,T[n-1]$` <emblue>apakšvirkni</emblue> (*subsequence*) sauc 
simbolu virkni no `$T[i]$` (ieskaitot virknes garumā `$0,1,2,\ldots$`), kur `$i$` vērtības aug, bet var nebūt pēc kārtas.  
(Apakšvirkni iegūst, sākotnējā virknē nosvītrojot `$0$` vai vairāk simbolus jebkurās vietās.)

</div>


--

## <lo-theory/> Apakšstringu, apakšvirkņu piemēri

<hgroup style="font-size:80%">

Virknes `"APPLE"` apakšstringi ir šīs `$15$` virknes:  
`""` (tukšā virkne), `"A"`, `"E"`, `"L"`, `"P"`, `"AP"`, `"LE"`, `"PL"`, `"PP"`, 
`"APP"`, `"PLE"`, `"PPL"`, `"APPL"`, `"PPLE"` un `"APPLE"`.

`$n$` simbolu virknei ir ne vairāk kā `${\displaystyle 1 + \frac{n(n+1)}{2}}$` apakšstringi
(to sasniedz, ja visi burti dažādi).

</hgroup>
<hgroup style="font-size:80%">

Virknes `"APPLE"` apakšvirknes ir šīs `$24$` virknes:  
`""` (tukšā virkne), `"A"`, `"E"`, `"L"`, `"P"`, 
`"AE"`, `"AL"`, `"AP"`, `"LE"`, `"PE"`, `"PL"`, `"PP"`,
`"ALE"`, `"APE"`, `"APL"`, `"APP"`,  `"PLE"`, `"PPE"`, `"PPL"`, 
`"APLE"`, `"APPE"`, `"APPL"`, `"PPLE"`, `"APPLE"`.

`$n$` simbolu virknei ir ne vairāk kā `${\displaystyle 2^n}$` apakšvirknes
(to sasniedz, ja visi burti dažādi).

</hgroup>




-----

# <lo-theory/> Naivā algoritma pseidokods


<table class="pseudocode">
<tr><th colspan="2"><tt>Naive_String_Matcher</tt>($T$, $P$)</th></tr>
<tr>
<td>1</td>
<td>$n = T.\mathit{length}$</td>
</tr>
<tr>
<td>2</td>
<td>$m = P.\mathit{length}$</td>
</tr>
<tr>
<td>3</td>
<td><b>for</b> $i=0$ <b>to</b> $n-m$</td>
</tr>
<tr>
<td>4</td>
<td class="ind1"><b>if</b> ($P[0],\ldots,P[m-1]) == (T[i],\ldots,T[i+m-1]])$</td>
</tr>
<tr>
<td>5</td>
<td class="ind2">print "Paraugs parādās ar nobīdi" $i$</td>
</tr>
</table>

<div style="font-size: 70%">

Novietojam vienu virkni zem otras un sākam salīdzināt:
`$$ \begin{array}{llllll}
\ldots, & T[i], & T[i + 1], & \ldots, & T[i+m-1], & \ldots \\
& P[0], & P[1], & \ldots, & P[m-1] & 
\end{array}$$`
Ja sakrīt visi `$m$` elementi, kas ir paraugā, tad apakšstringu esam atraduši. 

</div>



-----

# <lo-theory/> Naivā algoritma ātrdarbība

<hgroup style="font-size:70%;">

**Apgalvojums:** Naivā apakšstringu meklēšanas algoritma laika sarežģītība ir `$O(n \cdot m)$` sliktākajā gadījumā.

Ir `$n - m + 1$` iespējamās vērtības mainīgajam `$s$`. Katrai no tām var gadīties salīdzināt līdz `$m$` simboliem. Laiks
`$$(n - m + 1) \cdot m \approx n \cdot m.$$`

**Piezīme:** Parasti pieņemam, ka meklējamais paraugs ir daudz īsāks par pašu tekstu: `$m << n$`.

</hgroup>
<hgroup style="font-size:70%;">

**Piemērs 1:** Uzlabot to nevar: 

`$$T = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{burti}}$$`
`$$P = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m\;\text{burti}}$$`


**Piemērs 2:** Cits sliktākais gadījums (pat ja meklētu 
tikai vienu apakšstringu):

`$$T = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{burti}}$$`
`$$P = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m-1\;\text{burti}}\mathtt{b}$$`

</hgroup>






-----

# Levenshtein Distance<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 1</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span>(2) [Pamatfakti un naivais algoritms](#/naive-algorithm)</span>  
<span style="color:darkgreen">**(3) Levenšteina attālums**</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>



-----

# <lo-theory/> Labošanas attālums

Dotas simbolu virknes `$A = A[0]\ldots{}A[m-1]$` un `$B = B[0]\ldots{}B[n-1]$`, 
kuru garumi ir attiecīgi `$m$` un `$n$`. Atļautas sekojošas operācijas jeb 
<emblue>labojumi</emblue> (*edits*):

* Viena simbola aizstāšana ar citu simbolu;
* Jebkura viena simbola izdzēšana;
* Jauna simbola iespraušana patvaļīgā vietā.

**Definīcija:** Par <emblue>Levenšteina attālumu</emblue>
(*Levenshtein distance*, *editing distance*) 
`$M(A,B)$` diviem vārdiem `$A=A[0]\ldots{}A[m-1]$` 
un `$B=B[0]\ldots{}B[n-1]$` sauc mazāko 
iespējamo labojumu skaitu, kas pārtaisa `$A$` par `$B$`.



--

## <lo-theory/> Citi labošanas attāluma varianti

* Ja viena simbola aizstāšana ar citu ir divreiz dārgāka par iespraušanu un izdzēšanu?
* Ja virkni `$A$` jāpārveido par kādu `$B$` apakšvirkni (nevis pašu `$B$`)?
* Ja labojuma izmaksas atkarīgas no dzēšamā/iespraužamā simbola?
* Ja `$k$` simbolu apakšvirkni var iespraust/izdzēst vienā
gājienā ar izmaksu `$f(k)$` (šeit `$f(k)<k$` jeb apakšvirknes iespraušana
ir lētāka nekā `$k$` burtu mainīšana pa vienam).

**Motivācija:** Uzdevums parādās, piemēram, bioinformātikā. 
Šādus uzdevumus sauc par <emblue>aptuveno salīdzināšanu</emblue> (*Sequence alignment*). 
Piemēram, cik mutāciju vajag, lai viena DNS virkne pārvērstos par otru virkni.


--

## <lo-theory/> Līdzība ar īsāko ceļu grafā

![Shortest Paths](graph-distances.png)<!-- .element: style="width:500px" --> 


--

## <lo-theory/> Levenšteina attālums ar matricu rekurencēm

<div style="font-size:70%">

Doti vārdi `$A=A[0]\ldots{}A[m-1]$` un `$B=B[0]\ldots{}B[n-1]$`. 
Definējam `$(m+1) \times (n+1)$` izmēra matricu `$M[i,j]$` ar šādām sakarībām

`$$\begin{array}{l}
M[0,0]=0\\
M[i,0]=i,\;1 \leq i \leq m\\
M[0,j]=j,\;1 \leq j \leq n\\
M[i,j]=\min \left\{ \begin{array}{l}
M[i-1,j-1] + 0,\;\text{ja}\;A[i] = B[j]\\
M[i-1,j-1] + 1,\;\text{(burta aizstāšana)}\\
M[i,j-1] + 1,\;\text{(burta iespraušana)}\\
M[i-1,j] + 1,\;\text{(burta dzēšana)}
\end{array} \right. 
\end{array}$$`

Ar indukciju var pamatot, ka šādi rēķinot `$M[i,j]$` visiem 
`$i \in [1,m]$` un `$j \in [1,n]$`, matricas labajā apakšējā 
stūrī iegūsim `$M[m,n]$`, kas būs Levenšteina attālums
starp vārdiem `$A$` un `$B$`.

</div>

Sal. [Editierdistantz](https://de.wikipedia.org/wiki/Levenshtein-Distanz)



--

## <lo-summary/> Labošanas attāluma pseidokods


<table class="pseudocode" style="font-size:70%">
<tr><th colspan="2"><tt>Levenstein_Distance</tt>($A$, $B$)</th></tr>
<tr>
<td>1</td>
<td>$m = A.\mathit{length}$</td>
</tr>
<tr>
<td>2</td>
<td>$n = B.\mathit{length}$</td>
</tr>
<tr>
<td>3</td>
<td><b>for</b> $i = 0$ <b>to</b> $m$</td>
</tr>
<tr>
<td>4</td>
<td class="ind1">$M[0,i] = 0$</td>
</tr>
<tr>
<td>5</td>
<td><b>for</b> $j = 0$ <b>to</b> $n$</td>
</tr>
<tr>
<td>6</td>
<td class="ind1">$M[j,0] = 0$</td>
</tr>
<tr>
<td>7</td>
<td><b>for</b> $i = 1$ <b>to</b> $m$</td>
</tr>
<tr>
<td>8</td>
<td class="ind1"><b>for</b> $j = 1$ <b>to</b> $n$</td>
</tr>
<tr>
<td>9</td>
<td class="ind2"><b>if</b> $A[i] == B[j]$</td>
</tr>
<tr>
<td>10</td>
<td class="ind3">$M[i,j] = M[i-1,j-1]$</td>
</tr>
<tr>
<td>11</td>
<td class="ind2"><b>else</b> $M[i, j] = \min (M[i-1, j]+1,$</td>
</tr>
<tr>
<td>&nbsp;</td>
<td class="ind4">$M[i, j-1]+1, M[i-1, j-1]+1)$</td>
<tr>
<td>12</td>
<td><b>return</b> $M[m,n]$</td>
</tr>
</table>



-----

# <lo-sample/> Dinamiskās programmēšanas piemērs

<div style="font-size:70%">

Atrast Levenšteina attālumu starp `$A=\mathtt{tcat}$` un `$B=\mathtt{atcaca}$`. 
Aizpildām `$5 \times 7$` matricu: 

<table>
<tr>
<th>&nbsp;</th>
<th>$\mathtt{-}$</th>
<th>$\mathtt{a}$</th>
<th>$\mathtt{t}$</th>
<th>$\mathtt{c}$</th>
<th>$\mathtt{a}$</th>
<th>$\mathtt{c}$</th>
<th>$\mathtt{a}$</th>
</tr>
<tr>
<th>$\mathtt{-}$</th>
<td>$\color{#F00}{0}$</td>
<td>$\color{#F00}{1}$</td>
<td>$2$</td>
<td>$3$</td>
<td>$4$</td>
<td>$5$</td>
<td>$6$</td>
</tr>
<tr>
<th>$\mathtt{t}$</th>
<td>$1$</td>
<td>$1$</td>
<td>$\color{#F00}{1}$</td>
<td>$2$</td>
<td>$3$</td>
<td>$4$</td>
<td>$5$</td>
</tr>
<tr>
<th>$\mathtt{c}$</th>
<td>$2$</td>
<td>$2$</td>
<td>$2$</td>
<td>$\color{#F00}{1}$</td>
<td>$3$</td>
<td>$3$</td>
<td>$4$</td>
</tr>

<tr>
<th>$\mathtt{a}$</th>
<td>$3$</td>
<td>$2$</td>
<td>$3$</td>
<td>$2$</td>
<td>$\color{#F00}{1}$</td>
<td>$4$</td>
<td>$3$</td>
</tr>

<tr>
<th>$\mathtt{t}$</th>
<td>$4$</td>
<td>$3$</td>
<td>$2$</td>
<td>$3$</td>
<td>$2$</td>
<td>$\color{#F00}{2}$</td>
<td>$\color{#F00}{3}$</td>
</tr>
</table>


Pirmkārt, no šīs tabulas uzzinām, ka minimālais operāciju skaits ir `$3$`.  
Otrkārt, no tās var atjaunot optimālo labojumu virkni. To dara no beigām. 



--

## <lo-sample/> Īsākā labojumu secība

<hgroup style="font-size:80%">

<table>
<tr>
<th>&nbsp;</th>
<th>$\mathtt{-}$</th>
<th>$\mathtt{a}$</th>
<th>$\mathtt{t}$</th>
<th>$\mathtt{c}$</th>
<th>$\mathtt{a}$</th>
<th>$\mathtt{c}$</th>
<th>$\mathtt{a}$</th>
</tr>
<tr>
<th>$\mathtt{-}$</th>
<td>$\color{#F00}{0}$</td>
<td>$\color{#F00}{1}$</td>
<td>$2$</td>
<td>$3$</td>
<td>$4$</td>
<td>$5$</td>
<td>$6$</td>
</tr>
<tr>
<th>$\mathtt{t}$</th>
<td>$1$</td>
<td>$1$</td>
<td>$\color{#F00}{1}$</td>
<td>$2$</td>
<td>$3$</td>
<td>$4$</td>
<td>$5$</td>
</tr>
<tr>
<th>$\mathtt{c}$</th>
<td>$2$</td>
<td>$2$</td>
<td>$2$</td>
<td>$\color{#F00}{1}$</td>
<td>$3$</td>
<td>$3$</td>
<td>$4$</td>
</tr>

<tr>
<th>$\mathtt{a}$</th>
<td>$3$</td>
<td>$2$</td>
<td>$3$</td>
<td>$2$</td>
<td>$\color{#F00}{1}$</td>
<td>$4$</td>
<td>$3$</td>
</tr>

<tr>
<th>$\mathtt{t}$</th>
<td>$4$</td>
<td>$3$</td>
<td>$2$</td>
<td>$3$</td>
<td>$2$</td>
<td>$\color{#F00}{2}$</td>
<td>$\color{#F00}{3}$</td>
</tr>
</table>

</hgroup>
<hgroup style="font-size:80%">

No Dinamiskās programmēšanas tabuliņas atjauno labojumu secību:

1. `$M[4,6]=3$` iegūts, pieskaitot `$1$` pie `$M[4,5]=2$`.
2. `$M[4,5]=2$` iegūts, pieskaitot `$1$` pie `$M[3,4] = 1$`.
3. `$M[3,4]=1$` iegūts no `$M[2,3]=1$`, iegūts no `$M[1,2]=1$`, iegūts no `$M[0,1]=1$`.

Tas nozīmē, ka `$\mathtt{atcaca}$` no `$\mathtt{tcat}$` var iegūt šādi:
`$$\mathtt{tcat} \rightarrow \mathtt{atcat} \rightarrow \mathtt{atcac} \rightarrow \mathtt{atcaca}.$$`

</hgroup>




-----


# Summary<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 1</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span>(2) [Pamatfakti un naivais algoritms](#/naive-algorithm)</span>  
<span>(3) [Levenšteina attālums](#/levenshtein-distance)</span>  
<span style="color:darkgreen">**(4) Kopsavilkums**</span>

</hgroup>







-----

# <lo-summary/> Ko darījām šajā nodarbībā

1. Definējām virkņu/stringu meklēšanas uzdevumu.
2. Apskatījām naivo apakšstringa meklēšanas algoritmu. 
3. Definējām Levenšteina attālumu starp stringiem.
4. Aplūkojām dinamiskās programmēšanas metodi Levenšteina attāluma atrašanai.
(Turpmākajās sadaļās dinamiskās programmēšanas paradigma parādīsies vēl.)




