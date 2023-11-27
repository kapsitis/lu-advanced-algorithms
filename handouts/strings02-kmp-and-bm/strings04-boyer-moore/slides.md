# Introduction<!-- .element: style="visibility:hidden" --> 

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 4</blue>

</hgroup><hgroup style="font-size:90%">

<span style="color:darkgreen">**(1) Ievads**</span>  
<span>(2) [Bojera-Mūra algoritms](#/boyer-moore-algorithm)</span>  
<span>(3) [BM algoritma piemēri](#/bm-examples)</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>

<!--
Meklēšana virknēs - 2
------
Ievads
Bojera-Mūra algoritms
BM algoritma piemēri
Dinamiskā programmēšana (Fibonači virknes; Daijkstras algoritms)
Rekursīvu algoritmu sarežģītība
Labošanas attālums
(P) Regulāru izteiksmju meklēšana
Kopsavilkums



Meklēšana virknēs - 3
------------
Ievads

Sufiksu koku jēdziens
Ukkonena algoritms
(P) Failu digitālnospiedumi (fingerprinting) un Blūma filtri
Kopsavilkums
-->


-----



# <lo-why/> why

<div class="bigWhy">

Kāpēc jāizmanto dinamiskā programmēšana?

</div>

<div class="smallWhy">

* Dažiem optimizācijas uzdevumiem 
jādala uzdevums apakšuzdevumos.
* Starprezultātu iegaumēšana var būtiski paātrināt
dažus algoritmus.

</div>


--

## <lo-summary/> Nodarbības mērķi 

* Aprakstīt Bojera Mūra algoritmu. 
* Aplūkot BM piemērus un darbības pareizību. 


-----

# Boyer-Moore Algorithm<!-- .element: style="visibility:hidden" --> 

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 4</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span style="color:darkgreen">**(2) Bojera-Mūra algoritms**</span>  
<span>(3) [BM algoritma piemēri](#/bm-examples)</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>


-----

# <lo-summary/> Stringu meklēšana: Atkārtojums

**Uzdevums:** Dots teksts `$T[0]\ldots{}T[n-1]$` un meklējamais
paraugs `$P[0]\ldots{}P[m-1]$`; jāatrod visi gadījumi, kur `$P$` ir `$T$` apakšstrings
(un jāizvada atbilstošās nobīdes). 

Naivais un Knuta-Morisa-Prata algoritmi to dara, sākot ar pirmajiem simboliem 
(`$P[0]$` un `$T[i]$`, tad `$P[1]$` un `$T[i+1]$`, utt.). Ja kāds no burtiem atšķiras
(piemēram, `$P[0] \neq T[i]$`), tad salīdzināmo apakšvirkni 
pabīda vienu pozīciju tālāk: `$T[i]\ldots{}T[i-m-1]$` vietā mēģina `$T[i+1]\ldots{}T[i-m]$`. 


--

## <lo-summary/> Bojera-Mūra algoritma pamatideja

Bojera-Mūra algoritms sāk salīdzināšanu no pēdējā simbola (`$P[m-1]$` un `$T[i+m-1]$`). 
Nesakritības gadījumā salīdzināmo virkni var būt iespējams pabīdīt uz priekšu 
vairāk nekā par `$1$` simbolu.  
Piemēram, ja `$T[i+m-1]$` ir simbols, kas nesakrīt ne ar vienu no `$P[0],\ldots,P[m-1]$`, 
tad varam pārbīdīt virkni par `$m$` simboliem uz priekšu.

Tāpēc naivajam algoritmam un KMP vienmēr nepieciešamas `$O(n)$` darbības, 
bet Bojera-Mūra algoritmam dažos gadījumos var pietikt ar `$O(n/m)$` darbībām. 
(Sliktākajos gadījumos gan Bojera-Mūra algoritms nav labāks par KMP.)


--

# <lo-summary/> Bojera-Mūra pseidokods

<table class="pseudocode" style="font-size:65%">
<tr><th colspan="2">KMP_Matcher($T$, $P$)</th></tr>
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
<td>$s = 0$</td>
</tr>
<tr>
<td>4</td>
<td><b>while</b> $s \leq n-m$</td>
</tr>
<tr>
<td>5</td>
<td class="ind1">$j=m$</td>
</tr>
<tr>
<td>6</td>
<td class="ind1"><b>while</b> $j>0$ <b>and</b> $P[j-1] = T[s+j-1]$ <b>do</b></td>
</tr>
<tr>
<td>7</td>
<td class="ind2">$j=j-1$</td>
</tr>
<tr>
<td>8</td>
<td class="ind1"><b>if</b> $j=0$ <b>then</b></td>
</tr>
<tr>
<td>9</td>
<td class="ind2">print <tt style="font-family:'Courier New'">"Paraugs parādās ar nobīdi"</tt> $s$</td>
</tr>
<tr>
<td>10</td>
<td class="ind2">$s = s+ \gamma[0]$</td>
</tr>
<tr>
<td>11</td>
<td class="ind1"><b>else</b> $s = s + \max(\gamma[j], j-1-\lambda[T[s+j-1]])$</td>
</tr>
</table>

<div style="font-size:90%">

Pārbīdes nosaka tabulas (`$\gamma$` un `$\lambda$`) - 
no abām pārbīdēm izvēlamies maksimālo. Šo tabulu konstruēšanu tūlīt aplūkosim.

</div>


-----

# <lo-summary/> Sliktā simbola tabula

BM algoritms meklējamam paraugam `$P$` izveido divus pārbīžu masīvus:  
sliktā simbola tabulu `$\lambda$` un labā sufiksa tabulu `$\gamma$`.

Sliktā simbola tabulu indeksē ar simboliem, kas var būt sastopami `$P$`. 
Katram simbolam `$x$` tajā ieraksta lielāko `$i$`, kur `$P[i]=x$`. 
Ja `$x$` nav sastopams vārdā, tad `$\lambda[x]=-1$`. 
Piemēram, ja `$P=\mathtt{abcab}$`, tad tabula izskatās šādi:

<table>
<tr><th>$x$</th><td>$\mathtt{a}$</td><td>$\mathtt{b}$</td><td>$\mathtt{c}$</td><td>$\mathtt{*}$</td></tr>
<tr><th>$\lambda(x)$</th><td>$3$</td><td>$4$</td><td>$2$</td><td>$-1$</td></tr>
</table>

Ar `$\mathtt{*}$` apzīmēts jebkurš simbols, kas nav `$\mathtt{a,b,c}$`.


--

## <lo-summary/> Sliktā simbola pseidokods



<table class="pseudocode">
<tr><th colspan="2">Bad_Character_Table($P$)</th></tr>
<tr>
<td>1</td>
<td><b>for</b> $a \in S$&nbsp;&nbsp;<green>// katram alfabēta simbolam</green></td>
</tr>
<tr>
<td>2</td>
<td class="ind1">$\lambda[a] = -1$</td>
</tr>
<tr>
<td>3</td>
<td><b>for</b> $j=0$ <b>to</b> $m-1$ <b>do</b></td>
</tr>
<tr>
<td>4</td>
<td class="ind1">$\lambda[P[j]] = j$</td>
</tr>
<tr>
<td>5</td>
<td><b>return</b> $\lambda$</td>
</tr>

</table>



-----

# <lo-summary/> Labā sufiksa tabula

Labā prefiksa tabulu `$\gamma[i]$` indeksē ar skaitļiem 
`$i$` no `$0$` līdz `$m$`. Šīs tabulas semantika ir šāda: 
ja `$P[i]\ldots{}P[m-1]$` sakrīt ar `$T[k+i]\ldots{}T[k+m-1]$`, 
bet `$P[i-1] \neq T[k+i-1]$`, tad `$\gamma[i]$` ir mazākā 
pārbīde `$j$`, kuru ir vērts mēģināt.

* Ja `$i=m$`, tad `$\gamma[i]=1$`. 
* Ja `$i \leq m$`, tad `$\gamma[i]$` ir vienāds ar mazāko `$j>0$`, 
kam piemīt viena no šīm divām īpašībām:
    - `$i \geq j$` un `$P[i]\ldots{}P[m-1]$` sakrīt ar `$P[i-j]\ldots{}P[m-j-1]$`;
    - `$i \leq j$` un `$P[j]\ldots{}P[m-1]$` sakrīt ar `$P[0]\ldots{}P[m-j-1]$`.
Ja tāds `$j$` neeksistē, tad `$\gamma[i] = m$`;



--

## <lo-summary/> Labā sufiksa tabulas piemērs

Meklējamam paraugam `$P = \mathtt{abcab}$` labā sufiksa tabula izskatīsies šādi:

<table>
<tr><th>$j$</th><td>$0$</td><td>$1$</td><td>$2$</td><td>$3$</td><td>$4$</td><td>$5$</td></tr>
<tr><th>$\gamma[j]$</th><td>$3$</td><td>$3$</td><td>$3$</td><td>$3$</td><td>$5$</td><td>$1$</td></tr>
</table>

Saturiski, tas nozīmē, ka ja nav sakritis pēdējais simbols, 
tad nākošā iespēja, kas jāmēģina ir `$T[i+1]\ldots{}T[i+5]$`, 
bet, ja nav sakritis kāds no iepriekšējiem simboliem, tad varam 
uzreiz pāriet uz `$T[i+3]\ldots{}T[i+7]$`.   
(Šajā gadījumā to mums garantē simbols 
`$P[4]=T[i+4]=\mathtt{b}$`, jo `$\mathtt{b}$` vārdā `$P$` ir tikai `$P[4]$` un `$P[1]$`.)


--

## <lo-summary/> Labā sufiksa tabulas pseidokods


<table class="pseudocode">
<tr><th colspan="2"><span style="font-variant: small-caps;">Good_Suffix_Table</span>($P$)</th></tr>
<tr>
<td>1</td>
<td>$\pi =$<span style="font-variant: small-caps;">Compute_Prefix_Function</span>($P$)</td>
</tr>
<tr>
<td>2</td>
<td>$P' = \mathit{reverse}(P)$</td>
</tr>
<tr>
<td>3</td>
<td>$\pi' =$<span style="font-variant: small-caps;">Compute_Prefix_Function</span>($P'$)</td>
</tr>
<tr>
<td>4</td>
<td><b>for</b> $j=0$ <b>to</b> $m$ <b>do</b></td>
</tr>
<tr>
<td>5</td>
<td class="ind1">$\gamma[j] = m - \pi[m]$</td>
</tr>
<tr>
<td>6</td>
<td><b>for</b> $l=1$ <b>to</b> $m$ <b>do</b></td>
</tr>
<tr>
<td>7</td>
<td class="ind1">$j = m - \pi'[l]$</td>
</tr>
<tr>
<td>8</td>
<td class="ind1">$\gamma[j] = \min(\gamma[j], l - \pi'[l])$</td>
</tr>
<tr>
<td>9</td>
<td><b>return</b> $\gamma$</td>
</tr>
</table>

Šajā algoritmā <span style="font-variant: small-caps;">Compute_Prefix_Function</span>
ir funkcija, kas saņem virkni `$P$`, izrēķina šai virknei atbilstošo 
Knuta-Morisa Prata algoritma prefiksu funkciju `$\pi[j]$` un atgriež šo masīvu.


-----

# BM Examples<!-- .element: style="visibility:hidden" --> 


<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 4</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span>(2) [Bojera-Mūra algoritms](#/boyer-moore-algorithm)</span>  
<span style="color:darkgreen">**(3) BM algoritma piemēri**</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>




-----

# <lo-sample/> BM algoritma piemērs - 1

<hgroup style="font-size:80%">

<table>
<tr>
<th>$\mathtt{a}$</th><th>$\mathtt{d}$</th><th>$\mathtt{a}$</th><th>$\mathtt{a}$</th><th>$\mathtt{b}$</th>
<th>$\mathtt{a}$</th><th>$\mathtt{b}$</th><th>$\mathtt{c}$</th><th>$\mathtt{a}$</th><th>$\mathtt{b}$</th>
<th>$\mathtt{a}$</th><th>$\mathtt{a}$</th><th>$\mathtt{b}$</th>
</tr>
<tr>
<td>$\color{#CCC}{\mathtt{a}}$</td><td>$\color{#CCC}{\mathtt{b}}$</td>
<td>$\color{#F00}{\mathtt{c}}$</td><td>$\mathtt{a}$</td><td>$\mathtt{b}$</td>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
</tr>
<tr>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>$\color{#CCC}{\mathtt{a}}$</td><td>$\color{#CCC}{\mathtt{b}}$</td>
<td>$\color{#CCC}{\mathtt{c}}$</td><td>$\color{#CCC}{\mathtt{a}}$</td><td>$\color{#F00}{\mathtt{b}}$</td><td>&nbsp;</td><td>&nbsp;</td>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
</tr>
<tr>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
<td>$\color{#080}{\mathtt{a}}$</td><td>$\color{#080}{\mathtt{b}}$</td><td>$\color{#080}{\mathtt{c}}$</td><td>$\color{#080}{\mathtt{a}}$</td><td>$\color{#080}{\mathtt{b}}$</td>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
</tr>
<tr>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>$\color{#CCC}{\mathtt{a}}$</td><td>$\color{#CCC}{\mathtt{b}}$</td>
<td>$\color{#F00}{\mathtt{c}}$</td><td>$\mathtt{a}$</td><td>$\mathtt{b}$</td>
</tr>
</table>

Apskatīsim `$T = \mathtt{daababcabaab}$` un `$P = \mathtt{abcab}$`.   
Meklējam no labās puses uz kreiso: 
Katra rindiņa attēlo vienu mēģinājumu atrast apakšstringu. 
Ar <red>sarkanu</red> apzīmē burtu, kurā simbols no `$P$` nav sakritis ar 
atbilstošo simbolu no `$T$`. 

</hgroup>
<hgroup style="font-size:70%">

1. Pirmajā mēģinājumā sakrita `$P[4]$` un `$P[3]$`, bet ne `$P[2]$`. 
Tad pavirzāmies `$3$` simbolus uz priekšu (saskaņā ar „labā sufiksa tabulu”). 
2. skatāmies vai `$P[0]\ldots{}P[4]$` sakrīt ar `$T[3]\ldots{}[7]$`. 
Nesakritība ir jau `$P[4]$` un tad saskaņā ar „sliktā simbola tabulu” pavirzāmies pa `$2$` simboliem, 
lai atrastais "c" sakristu ar pirmo iespējamo "c", kas ir apakšvirknē `$P$` (pirmo – no beigām).
3. Trešajā mēģinājumā sakrīt viss apakšstrings. Ja nepieciešams atrast visas 
vietas tekstā `$T$`, kur ir apakšvirkne `$P$`, tad saskaņā ar `$\gamma[0]$` 
pārvietojamies `$3$` simbolus uz priekšu un mēģinām vēl. 
4. Pēdējais mēģinājums ir neveiksmīgs un tad esam sasnieguši teksta beigas.


</hgroup>


-----

# <lo-sample/> Tikai sliktā simbola tabula?

Praktiskai apakšvirkņu meklēšanai lielajā vairumā gadījumu pietiktu 
ar sliktā simbola tabulu vienu pašu. Varētu rakstīt šādu pseidokodu:

<table class="pseudocode">
<td>8</td>
<td class="ind1"><b>if</b> $j=0$ <b>then</b></td>
</tr>
<tr>
<td>9</td>
<td class="ind2">print <tt style="font-family:'Courier New'">"Paraugs parādās ar nobīdi"</tt> $s$</td>
</tr>
<tr>
<td>10</td>
<td class="ind2">$s = s+ \gamma[0]$</td>
</tr>
<tr>
<td>11</td>
<td class="ind1"><b>else</b> $s = s + \max(\color{#F00}{1}, j-1-\lambda[T[s+j-1]])$</td>
</tr>
</table>

Tai vietā, lai rakstītu "labā sufiksa likumu" `$\gamma[j]$`, ievietojam vērtību `$1$`. 
Ja `$T = \mathtt{BBBBBBBBBB...BBB}$` un 
paraugs ir `$T = \mathtt{ABBBB}$`, kļūst par "naivo" algoritmu.








<!-- 
Video par Bojera Mūra algoritmu
 

Krāsojumu video (bet bez piemēriem ar stringiem)
https://www.youtube.com/watch?v=lkL6RkQvpMM

Weak and Strong 
-->



-----

# <lo-sample/> Labā sufiksa tabulas piemērs

Aplūkosim paraugu `$P = \mathtt{CTTACTTAC}$`. 

Pamatosim, ka labā sufiksa tabula ir šāda:

<table>
<tr><th>$j$</th>
<td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td></tr>
<tr><th>$\gamma(j)$</th>
<td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>8</td><td>8</td><td>8</td><td>8</td><td>1</td></tr>
</table>


-----

# <lo-yellow/> Norādes

BM algoritma aprēķinu piemērs. 

* [Good Suffix Heuristic](https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/)
* [Visualizing String Matching](http://whocouldthat.be/visualizing-string-matching/)

<!--
1. [Lekciju konspekts](../algorithms-bin/liet2008-13-v3.doc) - Noderīgi pseidokodi, bet 
labā sufiksa tabulas piemēram "abcab" izmanto "vājo" definīciju.
2. [BM algoritma vispārīgs apraksts](https://www.youtube.com/watch?v=4Xyhb72LCX4) - "Ģenētisks" virkņu meklēšanas piemērs; 
labi skaidrots, bet arī tur labā sufiksa tabulas rēķināšanai izmanto "vājo" definīciju.
3. [Sliktā simbola tabula](https://www.youtube.com/watch?v=G-h1Dph9IOE) - Sliktā simbola tabulu 
definē neparasti (`$m - \lambda(j)$` mūsu apzīmējumos) un to pašu rēķina kļūdaini. 
4. [Labo sufiksu tabulas zīmējums](https://www.youtube.com/watch?v=lkL6RkQvpMM) - tikai 
grafisks attēlojums bez burtu piemēriem.

https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/
-->


-----

# Summary<!-- .element: style="visibility:hidden" --> 


<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 4</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span>(2) [Bojera-Mūra algoritms](#/boyer-moore-algorithm)</span>  
<span>(3) [BM algoritma piemēri](#/bm-examples)</span>  
<span style="color:darkgreen">**(4) Kopsavilkums**</span>

</hgroup>


