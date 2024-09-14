# Introduction<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 2</blue>

</hgroup><hgroup style="font-size:90%">

<span style="color:darkgreen">**(1) Ievads**</span>  
<span>(2) [Rabina-Karpa algoritms](#/rabin-karp-algorithm)</span>  
<span>(3) [Plaģiāta atrašana](#/finding-plagiarism)</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>

<!--

Vēl viena daļa
==============
Ievads
Galīgi automāti
Bojera-Mūra algoritms
BM algoritma pareizība
(P) Regulāru izteiksmju atrašana
Kopsavilkums



Vēl viena daļa
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

Kāpēc stringu meklēšanai vajadzīgs ripojošais hešings?

</div>

<div class="smallWhy">

* Apakšvirkņu meklēšanā būtisks slīdošais logs
* Slīdošajā logā nākamais substrings līdzīgs iepriekšējam
* Var ietaupīt, rēķinot hešfunkciju vērtības

</div>



--

## <lo-summary/> Nodarbības mērķi 

* Analizēt Rabina-Karpa algoritmu, tā sarežģītību.
* Raksturot citus ripojošā hešinga variantus.
* Tekstu ciparnospiedumi un plaģiāta apkarošana.


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

# Rabin-Karp Algorithm<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 2</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span style="color:darkgreen">**(2) Rabina-Karpa algoritms**</span>  
<span>(3) [Plaģiāta atrašana](#/finding-plagiarism)</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>


-----

# <lo-summary/> Stringu meklēšanas vietā skaitļi

<div style="font-size:80%">

Uztveram gan tekstu `$T$`, gan meklējamo paraugu `$P$` kā 
(lielus) veselus skaitļus.

* Alfabētu (kurā pierakstīti `$T$` un `$P$`) varbūt veido 
decimālcipari: `$S = \{ 0,1,2,\ldots,9 \}$`.
* Ja alfabēts ir lielāks, tad pieraksta `$T$` un `$P$` skaitīšanas sistēmā ar citu bāzi
(*radix-`$d$` notation*), kur `$d$` - burtu skaits alfabētā.

**Piemērs:** Dots strings `"pt"`. Ievērojam, ka burtu "p" un "t" ASCII 
baiti ir attiecīgi `x70` un `x74` (heksadecimālajā pierakstā). 
Tātad to decimālās vērtības ir attiecīgi `$112$` un `$116$`. 
Un ASCII alfabētā ir pavisam `$128$` simboli. 

Iegūstam, ka stringa `"pt"` vērtība bāzes-`$128$` (*radix*-`$128$`) 
pierakstā būs `$112 \cdot 128 + 116 = 14452$`. 

</div>



--

## <lo-summary/> Rabina-Karpa algoritma pamatideja

1. Tekstā `$T$` meklēsim ciparu virknes garumā `$m$` (parauga `$P$` garums), 
kas skaitliski vienādas ar `$P$`. 
2. Ar `$t_s$` apzīmējam (decimālajā sistēmā pārveidotu) skaitli, 
ko veido skaitīšanas bāzē-`$d$` (*radix*-`$d$`) cipari: 
`$T[s],T[s+1],\ldots,T[s+m-1]$`, kur nobīde
`$s$` var būt `$0,1,\ldots,n-m$`.
3. Ja zināms `$t_s$`, tad `$t_{s+1}$` var iegūt 
ar algebrisku triku:
`$$t_{s+1} = \left( t_s - d^{m-1}T[s] \right) \cdot d + T[s+m].$$`
    - No `$t_s$` atņem kreisā/vecākā cipara vērtību `$d^{m-1}T[s]$`, 
    - Pabīda citus ciparus vienu pozīciju uz augšu (piereizina ar `$d$`),
    - Visbeidzot pieskaita jaunāko ciparu `$T[s+m]$`. 


--

## <lo-summary/> Pamatidejas piemērs

<div style="font-size:80%">

* Dots "teksts" 10-ciparu alfabētā: `$T=\mathtt{31415926}$` 
(garums `$n=8$`); paraugs `$P = \mathtt{14159}$` (garums `$m=5$`).
* Aplūkojam visus `$T$` apakšstringus garumā `$m=5$`:
`$$t_0 = 31415,\;t_1 = 14159,\,t_2=41592,\;t_3 = 15926.$$`
* Pirmo skaitli `$t_0 = \color{#F00}{\mathtt{31415}}$` iegūst ar <emblue>Hornera shēmu</emblue>:
`$$t_0 = 10 \cdot (10 \cdot (10 \cdot (10 \cdot \color{#F00}{\mathtt{3}} + \color{#F00}{\mathtt{1}}) + \color{#F00}{\mathtt{4}}) + \color{#F00}{\mathtt{1}}) + \color{#F00}{\mathtt{5}} = 31415.$$`
* `$t_1$` iegūst no `$t_0$` konstantā laikā (tāpat `$t_2$` no `$t_1$` utt.):
`$$t_1 = (t_0 - 10^4 \cdot T[0])\cdot 10 + T[5] = (\color{#F00}{\mathtt{3}}\color{#0C0}{\mathtt{1415}} - 10000 \cdot \color{#F00}{\mathtt{3}}) \cdot 10 + \color{#F00}{\mathtt{9}} = \color{#0C0}{\mathtt{1415}}\color{#F00}{\mathtt{9}}.$$`

</div>


--

## <lo-summary/> Ko dara ar ļoti lieliem skaitļiem

Meklējamie paraugi mēdz būt gari, polinomu vērtības, kas iegūstamas
ar Hornera shēmu, var būt lieli skaitļi. Lai algoritma ātrdarbība
no tā neciestu, pārbaudām nevis vienādību pašiem `$t_s$` (teksta `$T$` gabals
garumā `$m$` nobīdīts par `$s$` simboliem) ar paraugam `$P$` atbilstošo 
bāzes-`$d$` pieraksta skaitli `$p$`, bet gan kongruenci: 
`$$t_s \equiv p\;(\text{mod}\,q),$$`
kur `$q$` izvēlas pietiekami lielu, lai bieži neparādītos 
<emblue>viltus trāpījumi</emblue> (*spurious hits*). 


--

# <lo-summary/> Rabina-Karpa pseidokods

<table class="pseudocode" style="font-size:60%">
<tr><th colspan="2"><tt>Rabin_Karp_Matcher</tt>($T$, $P$,$d$,$q$)</th></tr>
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
<td>$h = d^{m-1}\,\text{mod}\,q$</td>
</tr>
<tr>
<td>4</td>
<td>$p = 0$</td>
</tr>
<tr>
<td>5</td>
<td>$t_0 = 0$</td>
</tr>
<tr>
<td>6</td>
<td><b>for</b> $i = 0$ <b>to</b> $m-1$&nbsp;&nbsp;<green>// saskaita pēc Hornera shēmas</green></td> 
</tr>
<tr>
<td>7</td>
<td class="ind1">$p = (d \cdot p + P[i])\,\text{mod}\,q$</td>
</tr>
<tr>
<td>8</td>
<td class="ind1">$t_0 = (d \cdot t_0 + T[i])\,\text{mod}\,q$</td>
</tr>
<tr>
<td>9</td>
<td><b>for</b> $s=0$ <b>to</b> $n-m$</td>
</tr>
<tr>
<td>10</td>
<td class="ind1"><b>if</b> $p==t_s$</td>
</tr>
<tr>
<td>11</td>
<td class="ind2"><b>if</b> $(P[0],\ldots,P[m-1]) == (T[s],\ldots,T[s+m-1])$</td>
</tr>
<tr>
<td>12</td>
<td class="ind3">print <span style="font-family:'Courier New'">"Paraugs parādās ar nobīdi"</span> $s$</td>
</tr>
<tr>
<td>13</td>
<td class="ind1"><b>if</b> $s < n-m$</td>
</tr>
<tr>
<td>14</td>
<td class="ind2">$t_{s+1} = (d(t_s - T[s]\cdot{}h) + T[s+m])\,\text{mod}\,q$</td>
</tr>
</table>


--

## <lo-summary/> Cik liela ir q vērtība

* Ja `$q$` ir pārāk mazs, tad aritmētika pēc `$q$` moduļa ir ļoti ātra, 
bet bieži rodas viltus trāpījumi. 
* Ja `$q$` ir pārāk liels, tad reizināšanas tabulas uzbūvēšana modulārajai 
aritmētikai iznāk laikietilpīga.






-----

# Finding Plagiarism<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 2</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span>(2) [Rabina-Karpa algoritms](#/rabin-karp-algorithm)</span>  
<span style="color:darkgreen">**(3) Plaģiāta atrašana**</span>  
<span>(4) [Kopsavilkums](#/summary)</span>

</hgroup>


-----

# <lo theory/> Daži tiešsaistes servisi

* **Turnitin** - komerciāls serviss, pārbauda studentu eseju līdzību ar 
tur jau esošiem darbiem. Abonēšanas modelis, darbojas kopš 1997.g.  
Vai ir ētiski gūt peļņu no studentu radītiem oriģināliem darbiem?
* **Plag.lv** - kaut kas līdzīgs. Sk. rakstu 
[Latvijā palaista programma...](https://www.tvnet.lv/4838652/latvija-palaista-programma-kas-atklaj-plagiatu-akademiskos-darbos). 
* **Symantec DLP**, **Forcepoint DLP** - organizāciju pasargāšana no 
konfidenciālu dokumentu noplūdes (pat ja dokumentu saturs ir izmainīts).


--

## <lo-summary/> Daži algoritmi

* Sufiksu koki 
* N-gramu algoritmi 
* [MinHash](https://en.wikipedia.org/wiki/MinHash); Andrei Broder (AltaVista, 1997).





-----

# Summary<!-- .element: style="visibility:hidden;" -->

<hgroup>

<h1 style="font-size:28pt">Lietišķie algoritmi</h1>

<blue>Virkņu meklēšana - 2</blue>

</hgroup><hgroup style="font-size:90%">

<span>(1) [Ievads](#/introduction)</span>  
<span>(2) [Rabina-Karpa algoritms](#/rabin-karp-algorithm)</span>  
<span>(3) [Plaģiāta atrašana](#/finding-plagiarism)</span>  
<span style="color:darkgreen">**(4) Kopsavilkums**</span>

</hgroup>


-----

# <lo-summary/> Ko darījām šajā nodarbībā

1. Apskatījām naivo virkņu meklēšanas algoritmu. 
2. Apskatījām Rabina-Karpa algoritmu. 
3. Apskatījām vispārīgo ideju - ripojošo hešingu un Blūma filtrus.
4. Aplūkojām lietojumus plaģiāta meklēšanā un DLP (datu noplūdes novēršanā), 
veidojot tekstu ciparnospiedumus (*digital fingerprints*). 




