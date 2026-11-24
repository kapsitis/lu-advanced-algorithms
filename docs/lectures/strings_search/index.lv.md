---
layout: default
title: "Stringu meklēšana"
lang: lv
permalink: /lectures/strings_search/lv/
---
# 13. Stringu meklēšana

Šajā nodaļā definējam stringu meklēšanas uzdevumu un tā variantus (garākā kopīgā apakšstringa meklēšana, paternu meklēšana vienlaikus vairākos dokumentos, dokumentu priekšapstrāde jeb indeksācija). Aplūkoti algoritmi:

* Naivais apakšstringa meklēšanas algoritms
* Algoritms Levenšteina attāluma atrašanai
* Ripojošās hešfunkcijas
* Rabina-Karpa algoritms apakšstringa meklēšanai
* Knuta-Morisa-Prata (*Knuth-Morris-Pratt*, KMP) algoritms
* Bojera-Mūra (*Boyer-Moore*, BM) algoritms

## Stringu meklēšanas ievads

Stringu meklēšana sastopama atšķirīgos lietojumos, kas prasa dažādus algoritmus:

* Teksta redaktori: 1 vārds, 1 dokuments
* Datu noplūdes novēršana (*Data Leak prevention (DLP)*): daudzi paraugi (vārdi, regulāras izteiksmes), 1 pārbaudāmais dokuments.
* Dokumentu atrašana (*Document retrieval*): nedaudzi paraugi, daudzi dokumenti, kam var veikt priekšapstrādi/indeksāciju, lai paātrinātu meklēšanu tajos (piemēram, Lucene/Elasticsearch).
* Plaģiāta meklēšana: Daudzi dokumenti, 1 pārbaudāmais dokuments, atrast "kopētos-ielīmētos" (*Copy-Paste*) gabalus vai "kopētos-ielīmētos" un drusku parediģētos.

**Apakšstringa meklēšanas uzdevums:** Dots *teksts* - strings no $n$ simboliem: $T = T[0], \ldots, T[n-1]$. Dots arī *paraugs* (*pattern*) - strings no $m$ simboliem: $P = P[0], \ldots, P[m-1]$.

Jautājums: Vai tekstā $T$ ir atrodams apakšstrings $P$ (algoritms izvada vai nu pirmo pozīciju, kur $P$ ieiet virknē $T$, vai arī tas izvada visas pozīcijas).

**Definīcija:** Pozīciju tekstā $T$ (skaitli no $0$ līdz $n-1$), kur var sākties meklējamais paraugs sauc par *nobīdi* (*shift*).

### Apakšstringi un apakšvirknes

Stringus dažreiz sauc par virknēm, kas arī ir pareizi, bet virkne var nozīmēt gan "sequence" (galīga vai bezgalīga, no jebkāda veida objektiem), gan "string" (galīga virkne ar galīga alfabēta burtiem). Ir piemērs, kur abi jēdzieni atšķiras:

**Definīcija:** Par virknes $T[0],T[1],\ldots,T[n-1]$ *apakšstringu* (*substring*) sauc simbolu virkni no $T[i]$, kur $i$ vērtības seko pēc kārtas. (Apakšstringu iegūst, sākotnējai virknei nosvītrojot gabalus sākumā un beigās. Arī tukšais strings $\varepsilon$ un pats teksts $T$ ir apakšstringi.)

**Definīcija:** Par virknes $T[0],T[1],\ldots,T[n-1]$ *apakšvirkni* (*subsequence*) sauc simbolu virkni no $T[i]$, kur $i$ vērtības aug, bet var nebūt pēc kārtas. (Apakšvirkni iegūst, sākotnējā virknē nosvītrojot $0$ vai vairāk simbolus jebkurās vietās.)

**Piemērs:** Virknē $\mathtt{ABCDE}$ apakšstringi ir $15$ stringi:

$$
\varepsilon,
\mathtt{A}, \mathtt{AB}, \mathtt{ABC}, \mathtt{ABCD}, \mathtt{ABCDE},
\mathtt{B}, \mathtt{BC}, \mathtt{BCD}, \mathtt{BCDE},
\mathtt{C}, \mathtt{CD}, \mathtt{CDE},
\mathtt{D}, \mathtt{DE},
\mathtt{E}
$$

$n$ simbolu virknei ir ne vairāk kā ${\displaystyle 1 + \frac{n(n+1)}{2}}$ apakšstringi (to ir visvairāk, ja visi burti dažādi).

**Piemērs:** Virknē $\mathtt{ABCDE}$ apakšvirknes ir šie $32$ stringi:

$$
\begin{array}{c}
\varepsilon,
\mathtt{A},
\mathtt{AB}, \mathtt{ABC}, \mathtt{ABCD}, \mathtt{ABCDE}, \mathtt{ABCE},
\mathtt{ABD}, \mathtt{ABDE}, \mathtt{ABE},
\mathtt{AC}, \mathtt{ACD}, \mathtt{ACDE}, \mathtt{ACE}, \mathtt{AD}, \mathtt{ADE}, \mathtt{AE},\\
\mathtt{B}, \mathtt{BC}, \mathtt{BCD}, \mathtt{BCDE}, \mathtt{BCE},
\mathtt{BD}, \mathtt{BDE}, \mathtt{BE},
\mathtt{C}, \mathtt{CD}, \mathtt{CDE}, \mathtt{CE},
\mathtt{D}, \mathtt{DE},
\mathtt{E}.\\
\end{array}
$$

$n$ simbolu virknei ir ne vairāk kā ${\displaystyle 2^n}$ apakšvirknes (to sasniedz, ja visi burti dažādi).

### Naivais stringa meklēšanas algoritms

$\textsf{NaiveStringMatcher}(T, P)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. **for** $i = 0$ **to** $n-m$:
4. $\quad$ **if** $(P[0],\ldots,P[m-1]) == (T[i],\ldots,T[i+m-1])$:
5. $\quad\quad \text{print "Paraugs parādās ar nobīdi" } i$

Algoritms novieto vienu virkni zem otras un salīdzinām burtus no kreisās puses uz labo:

$$
\begin{array}{llllll}
\ldots, & T[i], & T[i + 1], & \ldots, & T[i+m-1], & \ldots \\
& P[0], & P[1], & \ldots, & P[m-1] &
\end{array}
$$

Ja sakrīt visi $m$ elementi, kas ir paraugā, tad apakšstringu esam atraduši.

**Apgalvojums:** Naivā apakšstringu meklēšanas algoritma laika sarežģītība ir $O(n \cdot m)$ sliktākajā gadījumā.

**Pierādījums:** Ir $n - m + 1$ iespējamās vērtības mainīgajam $s$. Katrai no tām var gadīties salīdzināt līdz $m$ simboliem. Laiks $(n - m + 1) \cdot m \approx n \cdot m$.

Parasti pieņem, ka meklējamais paraugs ir daudz īsāks par pašu tekstu: $m \ll n$, tomēr arī $m$ var būt liels un tāpēc $O(n \cdot m)$ ir daudz sliktāk nekā, piemēram, $O(n)$ -- lineāra atkarība no teksta garuma.

**Piemērs:** Šīm $T$ un $P$ vērtībām nevar uzlabot ātrdarbību:

$$
\left\lbrace \begin{array}{ll}
T = & \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{burti}}\\
P = & \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m\;\text{burti}}\\
\end{array} \right.
$$

Arī šis ir sliktākais gadījums naivā algoritma ātrdarbībai:

$$
\left\lbrace \begin{array}{ll}
T = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{burti}}\\
P = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m-1\;\text{burti}}\mathtt{b}\\
\end{array} \right.
$$

## Labošanas attālums

Dotas simbolu virknes $A = A[0]\ldots{}A[m-1]$ un $B = B[0]\ldots{}B[n-1]$, kuru garumi ir attiecīgi $m$ un $n$. Atļautas sekojošas operācijas jeb *labojumi* (*edits*):

* Viena simbola aizstāšana ar citu simbolu;
* Jebkura viena simbola izdzēšana;
* Jauna simbola iespraušana patvaļīgā vietā.

**Definīcija:** Par *Levenšteina attālumu* (*Levenshtein distance*, *editing distance*) $M(A,B)$ diviem vārdiem $A=A[0]\ldots{}A[m-1]$ un $B=B[0]\ldots{}B[n-1]$ sauc mazāko iespējamo labojumu skaitu, kas pārtaisa $A$ par $B$.

Ir pazīstami arī citi labošanas attāluma varianti

* Ja viena simbola aizstāšana ar citu ir divreiz dārgāka par iespraušanu un izdzēšanu.
* Ja virkni $A$ jāpārveido par kādu $B$ apakšvirkni (nevis pašu $B$).
* Ja labojuma izmaksas atkarīgas no dzēšamā/iespraužamā simbola.
* Ja $k$ simbolu apakšvirkni var iespraust/izdzēst vienā gājienā ar izmaksu $f(k)$ (šeit $f(k)<k$ jeb apakšvirknes iespraušana ir lētāka nekā $k$ burtu mainīšana pa vienam).

Tādi uzdevumi par *aptuveno salīdzināšanu* (*Sequence alignment*) var parādīties bioinformātikā. Piemēram, cik mutāciju vajag, lai viena DNS virkne pārvērstos par otru virkni. Levenšteina attālums ir viens no vienkāršākajiem variantiem.

**Levenšteina attālums kā īsākais ceļš grafā:** Ja $m$ burtu vārds $u$ jāpārtaisa par $n$ burtu vārdu $v$, izveidojam taisnstūrveida režģi ar aplīšiem -- tajā ir $m+1$ rindas un $n+1$ kolonnas. Katram aplītim ir "koordinātas" $(i,j)$, ja tas atrodas $i$-tajā rindā un $j$-tajā kolonnā ($i \in [0;m]$, $j \in [0;n]$).

<img
  alt="Levenšteina attālums kā īsākais ceļš grafā"
  src="{{ '/lectures/strings_search/figs/graph-distances.png' | relative_url }}"
  style="width: 100%; max-width: 384px; border:none; background-color:#FFFFFF;"
/>

* Visas bultiņas virzienā pa labi ir ar svaru $1$ (burta iespraušana)
* Visas bultiņas virzienā uz leju ir ar svaru $1$ (burta dzēšana)
* Bultiņas pa diagonāli no $(i,j)$ uz $(i+1,j+1)$ ir ar svaru $1$ (burta aizstāšana ar citu), **izņemot**, ja burti sakrīt: $u[i] = v[j]$. Šajā gadījumā burts nav jāmaina un šādu bultiņu drīkst izmantot bez maksas.

Levenšteina attālums būs īsākais ceļš no kreisās augšējās virsotnes uz labo apakšējo.

**Levenšteina attālums ar matricu rekurencēm:** Doti vārdi $A=A[0]\ldots{}A[m-1]$ un $B=B[0]\ldots{}B[n-1]$. Definējam $(m+1) \times (n+1)$ izmēra matricu $M[i,j]$ ar šādām sakarībām:

$$
M[0,0]=0,
$$

$$
M[i,0]=i,\;1 \leq i \leq m,
$$

$$
M[0,j]=j,\;1 \leq j \leq n\\
$$

$$
M[i,j]=\min \left\lbrace \begin{array}{l}
  M[i-1,j-1] + 0,\;\text{ja}\;A[i-1] = B[j-1]\\
  M[i-1,j-1] + 1,\;\text{(burta aizstāšana)}\\
  M[i,j-1] + 1,\;\text{(burta iespraušana)}\\
  M[i-1,j] + 1,\;\text{(burta dzēšana)}
  \end{array} \right.
$$

Ar indukciju var pamatot, ka šādi rēķinot $M[i,j]$ visiem $i \in [1,m]$ un $j \in [1,n]$, matricas labajā apakšējā stūrī iegūsim $M[m,n]$, kas būs Levenšteina attālums starp vārdiem $A$ un $B$.

Sal. [Editierdistantz](https://de.wikipedia.org/wiki/Levenshtein-Distanz)

### Levenšteina attālums ar dinamisko programmēšanu

$\textsf{LevensteinDistance}(A, B)$
1. $m = A.\mathit{length}$
2. $n = B.\mathit{length}$
3. **for** $i = 0$ **to** $m$:
4. $\quad M[i,0] = i$
5. **for** $j = 0$ **to** $n$:
6. $\quad M[0,j] = j$
7. **for** $i = 1$ **to** $m$:
8. $\quad$ **for** $j = 1$ **to** $n$:
9. $\quad\quad$ **if** $A[i-1] == B[j-1]$
10. $\quad\quad\quad M[i,j] = M[i-1,j-1]$
11. $\quad\quad$ **else** $M[i, j] = \min (M[i-1, j]+1,$
12. $\quad\quad\quad M[i, j-1]+1, M[i-1, j-1]+1)$
13. **return** $M[m,n]$

**Piemērs:** Atrast Levenšteina attālumu starp $A=\mathtt{tcat}$ un $B=\mathtt{atcaca}$. Aizpildām $5 \times 7$ matricu:

<img
  alt="Levenšteina attāluma matrica"
  src="{{ '/lectures/strings_search/figs/levenstein-distance.svg' | relative_url }}"
  style="width: 100%; max-width: 292px; border:none; background-color:#FFFFFF;"
/>

No šīs tabulas uzzinām, ka minimālais operāciju skaits ir $3$. No tabulas var arī atjaunot optimālo labojumu virkni. To dara no beigām.

1. $M[4,6]=3$ iegūts, pieskaitot $1$ pie $M[4,5]=2$.
2. $M[4,5]=2$ iegūts, pieskaitot $1$ pie $M[3,4] = 1$.
3. $M[3,4]=1$ iegūts no $M[2,3]=1$, iegūts no $M[1,2]=1$, iegūts no $M[0,1]=1$.

Tas nozīmē, ka $\mathtt{atcaca}$ no $\mathtt{tcat}$ var iegūt šādi:

$$
\mathtt{tcat} \rightarrow \mathtt{atcat} \rightarrow \mathtt{atcac} \rightarrow \mathtt{atcaca}.
$$

## Hešfunkcijas stringu salīdzināšanā

Rabina-Karpa algoritms meklē apakšstringu $P$ tekstā $T$ ātrāk nekā naivais algoritms (uzlabojums no $O(mn)$ uz $O(n)$ jeb teksta garums). Stringu meklēšanu aizstāj ar skaitļu salīdzināšanu. Uztveram gan tekstu $T$, gan meklējamo paraugu $P$ kā (lielus) veselus skaitļus.

Ja $T$ un $P$ pierakstīti 10-ciparu alfabētā, tad tie jau tāpat ir skaitļi. Vispārīgajā gadījumā alfabēta izmērs nav 10, bet tad pieraksta $T$ un $P$ skaitīšanas sistēmā ar citu bāzi (*radix-d notation*), kur $d$ - burtu skaits alfabētā.

**Piemērs:** Dots strings "pt". Ievērojam, ka burtu "p" un "t" ASCII baiti ir attiecīgi `x70` un `x74` (heksadecimālajā pierakstā). Tātad to decimālās vērtības ir attiecīgi $112$ un $116$. Un ASCII alfabētā ir pavisam $128$ simboli.

Iegūstam, ka stringa "pt" vērtība bāzes-$128$ (*radix*-$128$) pierakstā būs $112 \cdot 128 + 116 = 14452$.

### Rabina-Karpa algoritma pamatideja

1. Tekstā $T$ meklēsim ciparu virknes garumā $m$ (parauga $P$ garums), kas skaitliski vienādas ar $P$.
2. Ar $t_s$ apzīmējam (decimālajā sistēmā pārveidotu) skaitli, ko veido skaitīšanas bāzē-$d$ (*radix*-$d$) cipari: $T[s],T[s+1],\ldots,T[s+m-1]$, kur nobīde $s$ var būt $0,1,\ldots,n-m$.
3. Ja zināms $t_s$, tad $t_{s+1}$ var iegūt ar algebrisku triku:

   $$
   t_{s+1} = \left( t_s - d^{m-1}T[s] \right) \cdot d + T[s+m].
   $$

   - No $t_s$ atņem kreisā/vecākā cipara vērtību $d^{m-1}T[s]$,
   - Pabīda citus ciparus vienu pozīciju uz augšu (piereizina ar $d$),
   - Visbeidzot pieskaita jaunāko ciparu $T[s+m]$.

**Piemērs:**

* Dots "teksts" 10-ciparu alfabētā: $T=\mathtt{31415926}$ (garums $n=8$); paraugs $P = \mathtt{14159}$ (garums $m=5$).
* Aplūkojam visus $T$ apakšstringus garumā $m=5$:

  $$
  t_0 = 31415,\;t_1 = 14159,\,t_2=41592,\;t_3 = 15926.
  $$

* Pirmo skaitli $t_0 = \textcolor{red}{\mathtt{31415}}$ iegūst ar *Hornera shēmu*:

  $$
  t_0 = 10 \cdot (10 \cdot (10 \cdot (10 \cdot \textcolor{red}{\mathtt{3}} + \textcolor{red}{\mathtt{1}}) + \textcolor{red}{\mathtt{4}}) + \textcolor{red}{\mathtt{1}}) + \textcolor{red}{\mathtt{5}} = 31415.
  $$

* $t_1$ iegūst no $t_0$ konstantā laikā (tāpat $t_2$ no $t_1$ utt.):

  $$
  t_1 = (t_0 - 10^4 \cdot T[0])\cdot 10 + T[5] = (\textcolor{red}{\mathtt{3}}\textcolor{teal}{\mathtt{1415}} - 10000 \cdot \textcolor{red}{\mathtt{3}}) \cdot 10 + \textcolor{red}{\mathtt{9}} = \textcolor{teal}{\mathtt{1415}}\textcolor{red}{\mathtt{9}}.
  $$

**Ko darīt ar ļoti lieliem skaitļiem?** Meklējamie paraugi mēdz būt gari, polinomu vērtības, kas iegūstamas ar Hornera shēmu, var būt lieli skaitļi. Lai algoritma ātrdarbība no tā neciestu, pārbaudām nevis vienādību pašiem $t_s$ (teksta $T$ gabals garumā $m$ nobīdīts par $s$ simboliem) ar paraugam $P$ atbilstošo bāzes-$d$ pieraksta skaitli $p$, bet gan kongruenci:

$$
t_s \equiv p\;(\text{mod}\,q),
$$

kur $q$ izvēlas pietiekami lielu, lai bieži neparādītos *Viltus trāpījumi* (*spurious hits*).

### Rabina-Karpa algoritma pseidokods

$\textsf{RabinKarpMatcher}(T, P, d, q)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. $h = d^{m-1}\,\text{mod}\,q$
4. $p = 0$
5. $t_0 = 0$
6. **for** $i = 0$ **to** $m-1$: $\quad$ *// saskaita pēc Hornera shēmas*
7. $\quad p = (d \cdot p + P[i])\,\text{mod}\,q$
8. $\quad t_0 = (d \cdot t_0 + T[i])\,\text{mod}\,q$
9. **for** $s = 0$ **to** $n-m$:
10. $\quad$ **if** $p == t_s$
11. $\quad\quad$ **if** $(P[0],\ldots,P[m-1]) == (T[s],\ldots,T[s+m-1])$
12. $\quad\quad\quad \text{print "Paraugs parādās ar nobīdi" } s$
13. $\quad$ **if** $s < n-m$
14. $\quad\quad t_{s+1} = (d(t_s - T[s]\cdot h) + T[s+m])\,\text{mod}\,q$

**Kā izvēlēties moduli:** Ja $q$ ir pārāk mazs, tad aritmētika pēc $q$ moduļa ir ļoti ātra, bet bieži rodas viltus trāpījumi. Ja $q$ ir pārāk liels, tad reizināšanas tabulas uzbūvēšana modulārajai aritmētikai iznāk laikietilpīga.

### Ripojošās hešfunkcijas

Hešfunkcijas aprēķināšanas sarežģītību parasti pieņem par konstanti $O(1)$, bet ievadei garumā $m$ burti, tie parasti ir jāizlasa un jāapstrādā, tāpēc hešfunkcijas sarežģītība faktiski ir $O(m)$. Par laimi, īpašās situācijās ir izņēmumi -- tādas hešfunkcijas, kuras var izrēķināt ātrāk, ja tās rēķina *slīdošajā logā*. Slīdošajā logā nākamais substrings līdzīgs iepriekšējam. Pirmā hešfunkcija prasa $O(m)$ laiku, bet katru nākamo var rēķināt konstantā laikā.

Ripojošo hešfunkciju var uztvert kā *abstraktu datu tipu* (ADT): Tas uzkrāj ievades fragmentu kā sarakstu/rindu un atbalsta šādas operācijas:

* $RH$ `:=` $\textsf{RollingHash}(\mathtt{[]})$ -- inicializē hešfunkciju uz tukša simbolu saraksta (piešķirot tam kādu skaitlisku vērtību).
* $RH.\textsf{hash}()$ -- atgriež pašreizējā saraksta hash vērtību.
* $RH.\textsf{append}(val)$ -- pievieno simbolu `val` saraksta beigām (līdzīgi kā `Q.enqueue(val)` rindai `Q`).
* $RH.\textsf{skip}(val)$ -- noņem priekšējo elementu no saraksta (līdzīgi kā `Q.dequeue(val)` rindai `Q`). Parametru `val` funkcijai `skip()` bieži nenorāda, jo tas redzams saraksta priekšā, kas jau glabājas kā hešfunkcijas datu parametrs.

Elementi šajā sarakstā tiek attēloti kā veseli skaitļi kādā skaitīšanas sistēmā. Piemēram, ja mēs interpretējam rakstzīmes kā ASCII kodus, tad rakstzīme `'A'` glabājas kā 65 un `'B'` glabājas kā 66.

Mēs aplūkojam tekošo ievades fragmentu kā daudzciparu skaitli $u \in \mathcal{U}$ bāzē $a$ (ripojošās hešfunkcijas ievadi var interpretēt kā lielu skaitli). Piemēram, mēs varam izvēlēties $a = 256$, kas ir ASCII koda alfabēta izmērs.

Ir pazīstamas vairākas ripojošās hešfunkcijas ar labām īpašībām.

**Polinomiālā hešfunkcija:** Šīs hešfunkcijas vērtības ir atlikumi pēc moduļa $q$.

$$
H\left( \overline{c_1c_2\ldots{}c_k} \right) =
\left( c_1 a^{k-1} + c_2 a^{k-2} + c_3 a^{k-3} + ... + c_k a^{0} \right)\;\text{mod}\;q.
$$

Šāds polinoms ir līdzvērtīgs skaitļa pierakstam pozicionālajā skaitīšanas sistēmā ar bāzi $a$, kur $a$ var izvēlēties kā alfabēta izmēru, kas satur visus $c_i$. Savukārt $q$ ir kāds pietiekami liels pirmskaitlis, kas tomēr ir ievērojami mazāks par $a^k$ -- slīdošajā logā esošo informāciju.

Ja hešfunkcija ripo tālāk -- saņem jaunu burtu $c_{k+1}$, bet nomet $c_1$, tad jaunā vērtība iegūstama no iepriekšējās $H$ šādi:

$$
H \left( \overline{c_2\ldots{}c_k{}c_{k+1}} \right) =
\left( \left( H - c_1 a^{k-1} \right) \cdot a + c_{k+1} \right)\;\text{mod}\;q.
$$

**Cikliskie polinomi:** Šīs hešfunkcijas vērtības ir bitu virknītes kaut kādā fiksētā garumā.

Šajā formulā ar $s$ apzīmēta bitu rotēšana 1 pozīciju pa kreisi. Attiecīgi, $s^2$ ir rotēšana par 2 pozīcijām pa kreisi utt. Operācija $\oplus$ ir bitveida XOR.

$$
H \left( \overline{c_1c_2\ldots{}c_k} \right) =
s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) ) \oplus \ldots
\oplus  s( h(c_{k-1}) ) \oplus h(c_k)
$$

Ja hešfunkcija ripo tālāk -- saņem jaunu burtu $c_{k+1}$, bet nomet $c_1$, tad jaunā vērtība iegūstama no iepriekšējās $H$ šādi:

$$
H \left( \overline{c_2\ldots{}c_k{}c_{k+1}} \right) = s(H) \oplus s^{k}(h( c_1 )) \oplus h(c_{k+1})
$$

**Rabina-Karpa algoritms vienam stringam P:**

$\textsf{RabinKarpStringMatching}(T,P,a,q)$
1. $rP = \textsf{RollingHash}(\mathtt{[]})$
2. $rT = \textsf{RollingHash}(\mathtt{[]})$
3. **for** $i$ **in** $\textsf{range}(0,len(P))$:
4. $\quad rP.\textsf{append}(P[i])$
5. $\quad rT.\textsf{append}(T[i])$
6. **for** $i$ **in** $\textsf{range}(len(P),len(T))$:
7. $\quad$ **if** $rP.\textsf{hash}()$ `==` $rT.\textsf{hash}()$: $\quad$ *// Here we need to double-check as collisions are possible*
8. $\quad\quad$ **if** $P$ `==` $T[i - len(P) + 1: i+1]$
9. $\quad\quad\quad$ **output** "Pattern found at offset", $i - len(P)+1$
10. $\quad rT.\textsf{skip}(T[i - len(P)])$
11. $\quad rT.\textsf{append}(T[i])$

**Laika sarežģītība sliktākajā gadījumā:** Vai var nodrošināt, ka arī sliktākajā gadījumā viltus pozitīvie (hešfunkciju sakritība pat tad, ja paterns nav atrasts) negadās biežāk kā ar varbūtību $1/len(P)$?

**Rabina-Karpa algoritms vairākiem stringiem P:** Uzdevums: Mums ir teksts $T$ ar garumu $n$. Šobrīd mums ir $k$ meklējamie stringi $\mathcal{P} = \lbrace P_0, P_1, \ldots, P_{k-1} \rbrace$; visiem tiem ir vienāds garums $m$.

$\textsf{RabinKarpMultiString}(T, \mathcal{P}, m)$
1. $hashes$ `:=` $Set.\textsf{Empty}()$
2. **foreach** $P_i \in \mathcal{P}$:
3. $\quad rP_i = \textsf{RollingHash}(\mathtt{[]})$
4. $\quad$ **for** $j$ **in** $\textsf{range}(0,m)$:
5. $\quad\quad rP_i.\textsf{append}(P[j])$
6. $\quad hashes.\textsf{insert}(rP_i.\textsf{hash}())$
7. $rT = \textsf{RollingHash}(\mathtt{[]})$
8. **for** $j$ **in** $\textsf{range}(0,m)$:
9. $\quad rT.\textsf{append}(T[i])$
10. **for** $j$ **in** $\textsf{range}(1,n-m+1)$
11. $\quad$ **if** $rT.\textsf{hash}() \in hashes$ **and** $T[j:j+m-1] \in \mathcal{P}$
12. $\quad\quad$ **output** "Pattern found at offset", $j$
13. $\quad rT.\textsf{skip}(T[j])$
14. $\quad rT.\textsf{append}(T[j+m])$

Šim algoritmam ir laika sarežģītība $O(n + km)$. Naivajai stringu meklēšanai būtu laika sarežģītība $O(nmk)$, ja mēs pārbaudītu meklējamos stringus pa vienam.

### MinHash algoritmi

[MinHash](https://en.wikipedia.org/wiki/MinHash) algoritmu dokumentu līdzības novērtēšanai 1997.gadā ieviesa A.Broders (*Andrei Broder*), strādājot meklētājā AltaVista.

**Definīcija:** Teksta dokumenta sadalīšana n-grammās (*shingling*) ir procedūra, kurā no teksta izgriež noteikta garuma gabalus (piemēram, visas burtu virknītes garumā $5$ simboli, vai visi vārdi, vai visas $5$ vārdu virknītes). Der arī citas procedūras, kas izveido kolekciju ar savstarpēji pārklājošamies burtu virknītēm.

Sadalīšana n-grammās pārvieto uz priekšu fiksēta vai mainīga izmēra *slīdošo logu* un pārvērš dokumentu par n-grammu kopu. Ja mūs interesē veseli vārdi (nevis vārdu fragmenti fiksētā garumā) pirms n-grammu iegūšanas dokumentam var lietot atstarpju normalizēšanu (*space normalization*) - to pārraksta ar mazajiem burtiem, izmet visas pieturzīmes, un dažāda veida atstarpes (tabulācijas, parastas atstarpes, rindu pārnesumus utml.) aizstāj ar vienkāršām atstarpēm.

Plaģiāta vai citas teksta kopēšanas atpazīšanai var izmantot, piemēram, $5$ vārdu slīdošo logu. Ja divos dokumentos ir daudzas identiskas virknītes ar 5 pēc kārtas sekojošiem vārdiem, tad to parasti nevar izskaidrot ar nejaušu sagadīšanos -- dokumenti ir kopēti viens no otra (vai no kopīga pirmavota). Pati šī sakritība plaģiātu vēl nepierāda, jo var gadīties, ka abi dokumenti izmanto to pašu citātu.

**Definīcija:** Par divu kopu $A$ un $B$ Žakāra indeksu (*Jaccard coefficient*) sauc abu kopu šķēluma attiecību pret to apvienojumu:

$$
J(A,B) = \frac{\lvert A \cap B\rvert }{\lvert A \cup B\rvert } = \frac{\lvert A \cap B\rvert }{\lvert A\rvert  + \lvert B\rvert  - \lvert A \cap B\rvert }.
$$

Līdzīgām kopām (vai dokumentu n-grammu sadalījumiem) atbilst $J(A,B)$, kas ir tuvu skaitlim $1$.

*Piezīme:* MinHash algoritmiem ir svarīgi, lai hešfunkciju vērtības būtu savstarpēji neatkarīgas un ar vienmērīgiem varbūtiskiem sadalījumiem. Var izmantot Python iebūvēto hešfunkciju, bet ar dažādiem moduļiem. Ripojošās hešfunkcijas nav piemērotas.

Šis algoritms rēķina Žakāra indeksa novērtējumu $J(S_1, S_2)$, ja dots saraksts $\mathcal{H}$ -- kolekcija ar hešfunkcijām.

$\textsf{MinHash}(S_1, S_2, \mathcal{H})$
1. $\mathrm{sig}_1 = []$, $\mathrm{sig}_2 = []$ $\quad$ *// inicializē MinHash sarakstus*
2. **for** $h_i$ **in** $\mathcal{H}$:
3. $\quad \mathrm{minHash}_1 = \infty$, $\mathrm{minHash}_2 = \infty$ $\quad$ *// sāk ar bezgalību, lai rēķinātu minimumu*
4. $\quad$ **for** $s$ **in** $S_1$:
5. $\quad\quad \mathrm{hValue} = h_i(s)$ $\quad$ *// aprēķina hešfunkciju*
6. $\quad\quad$ **if** $\mathrm{hValue} < \mathrm{minHash}_1$:
7. $\quad\quad\quad \mathrm{minHash}_1 = \mathrm{hValue}$
8. $\quad$ **for** $s$ **in** $S_2$:
9. $\quad\quad \mathrm{hValue} = h_i(s)$ $\quad$ *// aprēķina hešfunkciju*
10. $\quad\quad$ **if** $\mathrm{hValue} < \mathrm{minHash}_2$:
11. $\quad\quad\quad \mathrm{minHash}_2 = \mathrm{hValue}$
12. $\quad \mathrm{sig}_1.append(\mathrm{minHash}_1)$, $\mathrm{sig}_2.append(\mathrm{minHash}_2)$ $\quad$ *// pievieno MinHash sarakstiem*
13. $intersection = 0$
14. **for** $i = 0$ **to** $\lvert \mathcal{H}\rvert  - 1$:
15. $\quad$ **if** $\mathrm{sig}_1[i] == \mathrm{sig}_2[i]$:
16. $\quad\quad \mathrm{intersection} = \mathrm{intersection} + 1$
17. **return** $\frac{\mathrm{intersection}}{\lvert \mathcal{H}\rvert }$ $\quad$ *// atgriež Žakāra indeksa novērtējumu*

### Blūma filtri

Bieži ir jāmeklē stringi ļoti lielā dokumentu kolekcijā. Optimālās hash tabulas, kas atrisina sadursmes ar *linear probing*, izmanto noslodzes koeficientus (glabāto objektu skaits, dalīts ar heštabulas izmēru) ap $\ln 2 \approx 0.7$. Piemēram, ja sagaidāms, ka heštabulā glabāsies $1000$ elementi, tad optimālās heštabulas masīvs ir apmēram $1400$.

Izveidojot n-grammu sarakstu daudziem gigabaitiem dokumentu, arī heštabulas izmērs būtu daudzi miljardi šūnu. Tas nav praktiski, ja plaģiāta programmai ir jāsalīdzina iesūtāmie dokumenti ar lielu jau esošo dokumentu kopu. Tāpēc ir noderīga optimizācija, ko sauc par *Blūma filtru*.

*Blūma filtrs* ir datu struktūra, kas līdzīga parastai kopai; tā atbalsta šādas operācijas:

* Izveido tukšu Blūma filtru: `BF = EmptySet()`
* Pievienot jaunu kopas elementu: `BF.add(item)`.
* Pārbaudīt, vai elements pieder kopai: `BF.contains(item)` (atgriež Boolean vērtību true/false).

*Piezīme:* Atšķirībā no parastām kopām (tsk. kopām parastās heštabulās) Blūma filtri parasti neatbalsta elementu dzēšanu. Tie ir noderīgi situācijās, kad jānosaka elementa piederība kādai lielai kopai, bet ir ierobežota vieta, kur šo kopu glabāt.

To var realizēt, izveidojot $k$ hešfunkcijas -- katra no tām nejauši un neatkarīgi no citām hash funkcijām, attēlo objektu uz vienu no $m$ bitiem. Funkcija `BF.add(item)` izrēķina visas $k$ hešfunkcijas un uzstāda attiecīgos bitus.

Funkcija `BF.contains(item)` tāpat izrēķina visas $k$ hešfunkcijas un atgriež `true` tad un tikai tad, ja visās $k$ vietās atrasti vieninieki. Iespējamas divas situācijas:

* Ja `item` tiešām ir pievienots Blūma filtram, to vienmēr arī atradīs. Blūma filtros nevar būt *false negatives*.
* Ja `item` nekad nebija pievienots Blūma filtram, pastāv varbūtība, ka citu elementu pievienošanas dēļ ir uzstādīti vieninieki visās $k$ pārbaudītajās vietās. Novērtēsim šo *false positive* varbūtību.

Pieņemsim, ka esam ievietojuši $n$ elementus, iespējamība, ka noteikts bits joprojām ir $0$, ir:

$$
p = \left(1-\frac{1}{m}\right)^{kn} \approx e^{-kn/m};
$$

Lai pārbaudītu elementa piederību kopai, ar katru no $k$ hešfunkcijām aprēķinātās pozīcijas masīvā būs $1$ ar varbūtību $(1-p)$. Iespējamība, ka tās visas ir $1$, kā rezultātā Blūma filtrs kļūdaini norāda, ka elements pieder kopai, ir šāda:

$$
\varepsilon = \left(1-\left[1-\frac{1}{m}\right]^{kn}\right)^k \approx
\left( 1-e^{-kn/m} \right)^k.
$$

Ņemot vērā bitu masīva lielumu $m$ un ievietojamo vienumu skaitu $n$, varam atrast optimālo skaitli $k$:

$$
k = \frac{m}{n} \ln 2
$$

Ja zinām pieļaujamo viltus pozitīvu rezultātu maksimālo $\varepsilon$, tad var pielāgot $m$ vērtību atbilstoši, lai ierobežotu viltus pozitīvo varbūtību.

**Tekstu ciparnospiedumu lietojumi:** Ciparnospiedumi (*fingerprints*) -- MinHash, Blūma filtri vai līdzīgas hešfunkciju vērtības vai to komplekti ļauj atrast sakrītošos gabalus dokumentos. Plaģiāta atrašanas algoritmi un arī Datu noplūdes novēršana (*Data Leak Prevention, DLP*) palīdz atklāt, vai jaunais dokuments ir līdzīgs kādam no esošajiem. Šo derīgo īpašību var izmantot komerciālos produktos:

* **Turnitin** - komerciāls serviss, pārbauda studentu eseju līdzību ar tur jau esošiem darbiem. Abonēšanas modelis, darbojas kopš 1997.g. Vai ir ētiski gūt peļņu no studentu radītiem oriģināliem darbiem?
* **Plag.lv** - kaut kas līdzīgs. Sk. rakstu [Latvijā palaista programma](https://www.tvnet.lv/4838652/latvija-palaista-programma-kas-atklaj-plagiatu-akademiskos-darbos).
* **Symantec DLP**, **Forcepoint DLP** - organizāciju pasargāšana no konfidenciālu dokumentu noplūdes (pat ja dokumentu saturs ir izmainīts).

## Meklēšana ar automātu

Ja nav veikta teksta $T$ priekšapstrāde un tajā jāatrod tikai viens paraugs $P$, tad parasti efektīvākā pieeja ir apstrādāt meklējamo paraugu $P$, izveidot tā meklēšanai piemērotas datu struktūras un pēc tam lasīt tekstu $T$. Viens datu struktūras veids ir *galīgs automāts-akceptors* (*finite automaton (acceptor)*), kas, nolasot kārtējo teksta $T$ simbolu, maina stāvokli. Un tiklīdz kā ievadītajā tekstā ir pilnībā nolasījis meklējamo paraugu, tad nonāk akceptējošā stāvoklī.

Regulāru izteiksmju meklēšanai vispārīgajā gadījumā galīgs automāts ir ļoti piemērots, bet apakšstringa meklēšanai automāta stāvokļu diagrammas vietā pietiek ar dažām mazām tabuliņām. Turpinājumā aplūkosim KMP jeb Knuta-Morisa-Prata (*Knuth-Morris-Pratt*) algoritmu un BM jeb Bojera-Mūra (*Boyer-Moore*) algoritmu. Nobeigumā pieskarsimies arī vispārīgai regulāru izteiksmju meklēšanai ievades tekstā.

Paraugu meklēšanai tekstā ir vairāki apakšgadījumi:

1. Ja tekstā $T$ jāmeklē viens paraugs (**Ctrl-F** teksta redaktorā), tad tekstu parasti lasa pa burtiem kā galīgā automātā (KMP un BM algoritmi).
2. Ja tekstā $T$ jāmeklē vienlaikus daudzi vienāda garuma paraugi (intelektuālā īpašuma aizsardzība, plaģiāta atrašana), tad tekstam parasti lieto ripojošo hešfunkciju kā iepriekšējā sadaļā - lai hešfunkcijas vērtību var salīdzināt ar visiem paraugiem (Rabina-Karpa algoritms).
3. Ja tekstā $T$ bieži jāmeklē dažāda garuma paraugi (Interneta meklētāji), tad tekstu parasti *indeksē* - izveido sufiksu koku, sufiksu masīvu vai līdzīgu datu struktūru (Ukonena algoritms nākamajās lekcijās).

Pieņemsim, ka lietojam naivo meklēšanas algoritmu un nobīdes (*shift*) pašreizējā vērtība ir $i$, bet salīdzināšanu esam veikuši līdz pozīcijai $j$.

Ja izrādās, ka

$$
T[i] = P[0], \ldots, T[i + j - 1] = P[j - 1],
$$

bet $T[i + j] \neq P[j]$, tad to izmanto, lai izvēlētos nākamo pāri $(i^{\ast},j^{\ast})$. Nav obligāti izvēlēties $(i^{\ast},j^{\ast}) = (i+1,0)$ kā naivajā algoritmā.

**Automāta pamatideja:** Apakšstringa meklēšana ar galīgu automātu: Automāta stāvokļi $q_0, q_1, \ldots, q_{m-1}$.

**Prefiksu īpašība:** Stāvoklī $q_i$ atrodamies tad un tikai tad, ja "pēdējie $i$ simboli no $T$ sakrīt ar pirmajiem $i$ simboliem no $P$".

**Piemērs:** Parauga $P = \mathtt{abab}$ meklēšanas automāts:

<img
  alt="Automāts parauga abab meklēšanai"
  src="{{ '/lectures/strings_search/figs/abab-automaton.png' | relative_url }}"
  style="width: 100%; max-width: 288px; border:none; background-color:#FFFFFF;"
/>

*Piezīme.* Pēc $P = \mathtt{abab}$ atrašanas pārejam uz $q_2$ (nevis $q_0$), jo paraugi var pārklāties.

$$
\mathtt{...ababab...}
$$

**Automāta piemērs:** Uzzīmēt galīgu automātu, kas meklē `aabab` kā apakšvirkni ievadāmajā tekstā.

**Atrisinājums:**

<img
  alt="Automāts parauga aabab meklēšanai"
  src="{{ '/lectures/strings_search/figs/aabab-automaton.png' | relative_url }}"
  style="width: 100%; max-width: 384px; border:none; background-color:#FFFFFF;"
/>

**Laiks meklēšanai ar automātu:**

1. Teksta lasīšanas laiks: Gatava automāta darbināšanai vajag $O(n)$ laiku: katram teksta burtam viena operācija.
2. Parauga priekšapstrādes laiks: Lai izveidotu automātu, jānosaka nākošais stāvoklis $q'$ jebkurai pašreizējā stāvokļa $q$ un pašreizējā burta kombinācijai. Pavisam ir $m$ stāvokļi. Ar $\lvert \mathcal{A}\rvert $ apzīmējam alfabēta $\mathcal{A}$ burtu skaitu. Veidojas tabula ar $m \cdot \lvert \mathcal{A}\rvert $ elementiem. Tam vajadzīgas vismaz $O(m \cdot \lvert \mathcal{A}\rvert )$ operācijas.
3. Pilnais laiks ir $O(n + m \cdot \lvert \mathcal{A}\rvert )$.

*Piezīme:* Priekšapstrādes laiks ir pārāk liels; praksē tā cenšas nedarīt - par to ir KMP algoritms. Pat pieņemot, ka $n \gg m$, arī $m \cdot \lvert \mathcal{A}\rvert $ var būt liels.

## Knuta-Morisa-Prata (KMP) algoritms

**KMP algoritma pamatideja:** Izveidojam tabuliņu ar *prefiksu funkciju* (*prefix function*) $\pi$. Funkcija $\pi$ veidojama meklējamam *paraugam* (*pattern*). Šī funkcija ietver zināšanas par to, kā paraugs $P$ sakrīt pats ar savām nobīdēm. Tā var izvairīties no nevajadzīgām nobīdēm naivajā meklēšanas algoritmā un nav jāveido atsevišķa stāvokļu pāreja katram ievades simbolam $s \in S$.

1. Ievades tekstu lasa tikai vienreiz: $O(n)$, nevis $O(n \cdot m)$, kā naivajam algoritmam.
2. Parauga $P$ priekšapstrāde notiks laikā $O(m)$, nevis $O(m\cdot\lvert S\rvert )$, kā pilnīgi izveidotam automātam.

Knuta-Morisa-Prata algoritma variantu -- Aho-Korasikas (*Aho-Corasick*) stringu meklēšanas algoritmu -- izmanto ielaušanās atklāšanas sistēmās (*intrusion detection systems*), lai pakešu saturā vienlaikus meklētu daudzus paraugus.

### Prefiksu funkcija

Prefiksu funkcija atkarīga no meklējamā parauga $P=P[0]\ldots{}P[m-1]$.

**Definīcija:** Katram $j = 1,\ldots,m$ atrod maksimālo $k$ ($k<j$), kam izpildās:

$$
\left\lbrace
  \begin{array}{l}
    P[0] = P[j - k]\\
    P[1] = P[j - k + 1]\\
    \ldots\\
    P[k - 1] = P[j - 1]
  \end{array}
\right.
$$

Prefiksu funkcijas vērtība: $\pi[j]=k$. Ja tāda $k$ ($k<j$) nav, tad $\pi[j]=0$.

**Cita definīcija:** Ar $P_k$ apzīmē virknes $P$ prefiksu garumā $k$. Tad $\pi(j)=k$ ir $P$ $j$-tā prefiksa ($P_j$) visgarākā sufiksa garums, kas īsāks par pašu $j$:

$$
\pi(j) = \max \left\lbrace k\,:\,k<j\;\text{un}\;P_k\;\text{ir virknes}\;P_j\;\text{sufikss} \right\rbrace
$$

**Uzdevums:** Atrast prefiksu funkciju, kas atbilst meklējamajam paraugam $P = \mathtt{abab}$.

**Atrisinājums:** Risinājumu var iztēloties kā "maksimālu teleskopisku sabīdīšanu":

<img
  alt="Prefiksu funkcija paraugam abab"
  src="{{ '/lectures/strings_search/figs/prefix-functions1.png' | relative_url }}"
  style="width: 100%; max-width: 288px; border:none; background-color:#FFFFFF;"
/>

| $j$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $0$ | $1$ | $2$ |

**Uzdevums:** Atrast prefiksu funkciju, kas atbilst meklējamajam paraugam $P = \mathtt{aabaab}$.

**Atrisinājums:**

<img
  alt="Prefiksu funkcija paraugam aabaab"
  src="{{ '/lectures/strings_search/figs/prefix-functions2.png' | relative_url }}"
  style="width: 100%; max-width: 336px; border:none; background-color:#FFFFFF;"
/>

| $j$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $1$ | $0$ | $1$ | $2$ | $3$ |

**KMP algoritma pseidokods:** *Ievade:* Teksts $T$ un meklējamais paraugs $P$. *Izvade:* Visas nobīdes, ar kādām tekstā parādās paraugs.

$\textsf{KMPmatcher}(T, P)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. $\pi = \textsf{Compute\\_Prefix\\_Function}(P)$
4. $k = 0$
5. **for** $i = 0$ **to** $n-1$ $\quad$ *// lasa T no kreisās uz labo*
6. $\quad$ **while** $k > 0$ **and** $P[k] \neq T[i]$
7. $\quad\quad k = \pi(k)$ $\quad$ *// hipotēze bija aplama, paraugu pārceļ uz priekšu*
8. $\quad$ **if** $P[k] == T[i]$
9. $\quad\quad k = k + 1$ $\quad$ *// hipotēze pagaidām apstiprinās, salīdzina tālāk*
10. $\quad$ **if** $k == m$ $\quad$ *// vai viss paraugs P jau nolasīts?*
11. $\quad\quad$ print `"Paraugs parādās ar nobīdi"` $i-m$
12. $\quad\quad k = \pi(k)$ $\quad$ *// nākamā vieta, uz kuru pārcelt paraugu*

**Kāpēc KMP strādā pareizi?** Pieņemsim, ka tekošā nobīde (*shift*) ir $i \in \lbrace 0,\ldots,n-m\rbrace$: Ceram, ka paraugs $P$ atradīsies tekstā $T$, sākot ar $i$-to pozīciju.

Bet izrādās, ka kārtējais $T$ simbols ($T[i+j]$) nesakrīt ar $P[j]$ (kur $j \in \lbrace 0,\ldots,m-1\rbrace$). Tad ir spēkā vienādības:

$$
\left\lbrace \begin{array}{lll}
T[i+j-k] & =P[j-k] & =P[0]\\
T[i+j-k+1] & =P[j-k+1] & =P[1]\\
\ldots & \ldots & \ldots\\
T[i+j-1] & =P[j-1] & =P[k-1]
\end{array} \right.
$$

Nākamā pozīcija tekstā $T$, no kuras var sākties apakšstrings $P$, ir, sākot ar pēdējiem $k$ burtiem no jau nolasītā $T$ gabala.

**Piemērs:** Meklējam paraugu $P=\mathtt{ababaca}$ tekstā $T = \mathtt{ababaababaca}$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{c}$ | $\mathtt{a}$ | $k=0$ |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | | | | | $k=1,2,3,4,5$ |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\textcolor{red}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | | | | | $k=\pi(5)=3$ |
| | | | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\textcolor{red}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | | | $k=\pi(3)=1$ |
| | | | | | $\mathtt{a}$ | $\textcolor{red}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | $k=\pi(1)=0$ |
| | | | | | | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{c}$ | $\mathtt{a}$ | $k=1,2,3,4,5,6,7$ |

Prefiksu funkcija paraugam $P=\mathtt{ababaca}$:

| $j$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $0$ | $1$ | $2$ | $3$ | $0$ | $1$ |

**KMPmatcher ātrdarbības novērtējums:** Pieņemsim, ka $\pi(j)$ jau izrēķināta. Ievērojam, ka jebkurā parauga $P$ un teksta $T$ salīdzināšanā izpildās viena no divām lietām:

* ja $P[k] = T[i]$, tad palielinās $i$, bet $i-k$ nemainās.
* ja $P[k] \neq T[i]$, tad palielinās $i-k$, bet $i$ nemainās.

Tā kā $i$ un $i-k$ ir veseli skaitļi, kas sākumā ir $0$ un nevar pārsniegt $n$, tad algoritmā ir ne vairāk kā $2n$ salīdzināšanas. Tātad KMP ātrdarbība ir $O(n)$.

### Prefiksu funkcijas pseidokods

$\textsf{ComputePrefixFunction}(P)$
1. $m = P.\mathit{length}$
2. Rezervē tabulu $\pi(1)\ldots{}\pi(m)$
3. $\pi(1)=0$
4. $k=0$
5. **for** $q=2$ **to** $m$
6. $\quad$ **while** $k>0$ **and** $P[k]\neq P[q-1]$
7. $\quad\quad k=\pi(k)$
8. $\quad$ **if** $P[k]==P[q-1]$
9. $\quad\quad k=k+1$
10. $\quad \pi(q)=k$
11. **return** $\pi$

**Piemērs:** Atrast prefiksu funkciju, kas atbilst meklējamajam paraugam $P = \mathtt{ababaca}$.

<img
  alt="Prefiksu funkcija paraugam ababaca"
  src="{{ '/lectures/strings_search/figs/prefix-functions3.png' | relative_url }}"
  style="width: 100%; max-width: 384px; border:none; background-color:#FFFFFF;"
/>

| $j$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $0$ | $1$ | $2$ | $3$ | $0$ | $1$ |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{c}$ | $\mathtt{a}$ |
| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| $q=1$ | $\textcolor{blue}{0}$ | | | | | | |
| $q=2$ | 0 | $\textcolor{blue}{0}$ | | | | | |
| $q=3$ | 0 | 0 | $\textcolor{blue}{1}$ | | | | |
| $q=4$ | 0 | 0 | 1 | $\textcolor{blue}{2}$ | | | |
| $q=5$ | 0 | 0 | 1 | 2 | $\textcolor{blue}{3}$ | | |
| $q=6$ | 0 | 0 | 1 | 2 | 3 | $\textcolor{red}{3\downarrow}$ 1 | |
| $q=6$ | 0 | 0 | 1 | 2 | 3 | $\textcolor{red}{1\downarrow}$ 0 | |
| $q=6$ | 0 | 0 | 1 | 2 | 3 | $\textcolor{blue}{0}$ | |
| $q=7$ | 0 | 0 | 1 | 2 | 3 | 0 | $\textcolor{blue}{1}$ |

**Prefiksu funkcijas laika sarežģītība:** Prefiksu funkcijas veidošanas laiks ir $O(m)$.

1. Ārējais cikls izpildās $m-1$ reizes.
2. Katrā iekšējā cikla iterācijā $\pi[i+1]$ vērtība tiek samazināta.
3. Tā kā šī vērtība tiek palielināta tikai katrā ārējā cikla iterācijā par $1$, tad tā var sasniegt ne vairāk kā $m$. Tā kā tā nevar būt negatīva, tad samazināties var ne vairāk kā $m$ reizes, tātad iekšējais cikls kopumā izpildās ne vairāk kā $m$ reizes.

## Bojera-Mūra algoritms

**Pamatideja:** Bojera-Mūra algoritms sāk salīdzināšanu no pēdējā simbola ($P[m-1]$ un $T[i+m-1]$). Nesakritības gadījumā salīdzināmo virkni var būt iespējams pabīdīt uz priekšu vairāk nekā par $1$ simbolu. Piemēram, ja $T[i+m-1]$ ir simbols, kas nesakrīt ne ar vienu no $P[0],\ldots,P[m-1]$, tad varam pārbīdīt virkni par $m$ simboliem uz priekšu.

Tāpēc naivajam algoritmam un KMP nepieciešamas vismaz $O(n)$ darbības, bet Bojera-Mūra algoritmam dažreiz pietiek ar $O(n/m)$ darbībām. (Sliktākajos gadījumos gan Bojera-Mūra algoritms nav labāks par KMP.)

### Bojera-Mūra pseidokods

$\textsf{BMmatcher}(T,P)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. $s = 0$
4. **while** $s \leq n-m$
5. $\quad j=m$
6. $\quad$ **while** $j>0$ **and** $P[j-1] = T[s+j-1]$:
7. $\quad\quad j=j-1$
8. $\quad$ **if** $j=0$ **then**
9. $\quad\quad$ print `"Paraugs parādās ar nobīdi"` $s$
10. $\quad\quad s = s + \gamma[0]$
11. $\quad$ **else** $s = s + \max(\gamma[j], j-1-\lambda[T[s+j-1]])$

Pārbīdes nosaka tabulas ($\gamma$ un $\lambda$) - no abām pārbīdēm izvēlamies maksimālo. Šo tabulu konstruēšanu tūlīt aplūkosim.

### Sliktā simbola tabula

BM algoritms paraugam $P$ izveido divus pārbīžu masīvus: sliktā simbola tabulu $\lambda$ un labā sufiksa tabulu $\gamma$.

Sliktā simbola tabulu indeksē ar simboliem, kas var būt sastopami $P$. Katram simbolam $x$ tajā ieraksta lielāko $i$, kur $P[i]=x$. Ja $x$ nav sastopams vārdā, tad $\lambda[x]=-1$. Piemēram, ja $P=\mathtt{abcab}$, tad tabula izskatās šādi:

| $x$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{c}$ | $\mathtt{*}$ |
| --- | --- | --- | --- | --- |
| $\lambda(x)$ | $3$ | $4$ | $2$ | $-1$ |

Ar $\mathtt{*}$ apzīmēts jebkurš simbols, kas nav $\mathtt{a,b,c}$.

**Sliktā simbola pseidokods:**

$\textsf{BadCharacterTable}(P)$
1. **for** $a \in S$: $\quad$ *// katram alfabēta simbolam*
2. $\quad \lambda[a] = -1$
3. **for** $j=0$ **to** $m-1$:
4. $\quad \lambda[P[j]] = j$
5. **return** $\lambda$

### Labā sufiksa tabula

Labā sufiksa tabulu $\gamma[i]$ indeksē ar skaitļiem $i$ no $0$ līdz $m$. Šīs tabulas semantika ir šāda: ja $P[i]\ldots{}P[m-1]$ sakrīt ar $T[k+i]\ldots{}T[k+m-1]$, bet $P[i-1] \neq T[k+i-1]$, tad $\gamma[i]$ ir mazākā pārbīde $j$, kuru ir vērts mēģināt.

- Ja $i=m$, tad $\gamma[i]=1$.
- Ja $i \leq m$, tad $\gamma[i]$ ir vienāds ar mazāko $j>0$, kam piemīt viena no šīm divām īpašībām:
  - $i \geq j$ un $P[i]\ldots{}P[m-1]$ sakrīt ar $P[i-j]\ldots{}P[m-j-1]$;
  - $i \leq j$ un $P[j]\ldots{}P[m-1]$ sakrīt ar $P[0]\ldots{}P[m-j-1]$. Ja tāds $j$ neeksistē, tad $\gamma[i] = m$;

**Piemērs:** Meklējamam paraugam $P = \mathtt{abcab}$ labā sufiksa tabula izskatīsies šādi:

| $j$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $\gamma[j]$ | $3$ | $3$ | $3$ | $3$ | $5$ | $1$ |

Saturiski, tas nozīmē, ka ja nav sakritis pēdējais simbols, tad nākošā iespēja, kas jāmēģina ir $T[i+1]\ldots{}T[i+5]$, bet, ja nav sakritis kāds no iepriekšējiem simboliem, tad varam uzreiz pāriet uz $T[i+3]\ldots{}T[i+7]$.

(Šajā gadījumā to mums garantē simbols $P[4]=T[i+4]=\mathtt{b}$, jo $\mathtt{b}$ vārdā $P$ ir tikai $P[4]$ un $P[1]$.)

**Labā sufiksa tabulas pseidokods:**

$\textsf{GoodSuffixTable}(P)$
1. $\pi = \textsf{ComputePrefixFunction}(P)$
2. $P' = \textsf{Reverse}(P)$
3. $\pi' = \textsf{ComputePrefixFunction}(P')$
4. **for** $j=0$ **to** $m$:
5. $\quad \gamma[j] = m - \pi[m]$
6. **for** $\ell=1$ **to** $m$:
7. $\quad j = m - \pi'[\ell]$
8. $\quad \gamma[j] = \min(\gamma[j], \ell - \pi'[\ell])$
9. **return** $\gamma$

Šajā algoritmā $\textsf{ComputePrefixFunction}(P)$ ir funkcija, kas saņem virkni $P$, izrēķina šai virknei atbilstošo Knuta-Morisa-Prata algoritma prefiksu funkciju $\pi[j]$ un atgriež šo masīvu.

**BM algoritma piemērs:**

| $\mathtt{a}$ | $\mathtt{d}$ | $\mathtt{a}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{c}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{a}$ | $\mathtt{b}$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{red}{\mathtt{c}}$ | $\mathtt{a}$ | $\mathtt{b}$ | | | | | | | | |
| | | | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{red}{\mathtt{b}}$ | | | | | |
| | | | | | $\textcolor{green}{\mathtt{a}}$ | $\textcolor{green}{\mathtt{b}}$ | $\textcolor{green}{\mathtt{c}}$ | $\textcolor{green}{\mathtt{a}}$ | $\textcolor{green}{\mathtt{b}}$ | | | |
| | | | | | | | | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{red}{\mathtt{c}}$ | $\mathtt{a}$ | $\mathtt{b}$ |

Apskatīsim $T = \mathtt{daababcabaab}$ un $P = \mathtt{abcab}$. Meklējam no labās puses uz kreiso: Katra rindiņa attēlo vienu mēģinājumu atrast apakšstringu. Ar **sarkanu** apzīmē burtu, kurā simbols no $P$ nav sakritis ar atbilstošo simbolu no $T$.

1. Pirmajā mēģinājumā sakrita $P[4]$ un $P[3]$, bet ne $P[2]$. Tad pavirzāmies $3$ simbolus uz priekšu (saskaņā ar "labā sufiksa tabulu").
2. Skatāmies vai $P[0]\ldots{}P[4]$ sakrīt ar $T[3]\ldots{}T[7]$. Nesakritība ir jau $P[4]$ un tad saskaņā ar "sliktā simbola tabulu" pavirzāmies pa $2$ simboliem, lai atrastais "c" sakristu ar pirmo iespējamo "c", kas ir apakšvirknē $P$ (pirmo - no beigām).
3. Trešajā mēģinājumā sakrīt viss apakšstrings. Ja nepieciešams atrast visas vietas tekstā $T$, kur ir apakšvirkne $P$, tad saskaņā ar $\gamma[0]$ pārvietojamies $3$ simbolus uz priekšu un mēģinām vēl.
4. Pēdējais mēģinājums ir neveiksmīgs, un tad esam sasnieguši teksta beigas.

**Varbūt var būt tikai sliktā simbola tabula?** Praktiskai apakšvirkņu meklēšanai lielajā vairumā gadījumu pietiktu ar sliktā simbola tabulu vienu pašu. Varētu rakstīt šādu pseidokodu:

1. **if** $j=0$ **then**
2. $\quad$ print "Paraugs parādās ar nobīdi" $s$
3. $\quad s = s+ \gamma[0]$
4. **else** $s = s + \max(\textcolor{red}{1}, j-1-\lambda[T[s+j-1]])$

Tā vietā, lai rakstītu "labā sufiksa likumu" $\gamma[j]$, ievietojam vērtību $1$. Ja $T = \mathtt{BBBBBBBBBB...BBB}$ un paraugs ir $P = \mathtt{ABBBB}$, kļūst par "naivo" algoritmu.

**Labā sufiksa tabulas piemērs:** Aplūkosim paraugu $P = \mathtt{CTTACTTAC}$. Pamatosim, ka labā sufiksa tabula ir šāda:

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\gamma(j)$ | 4 | 4 | 4 | 4 | 4 | 8 | 8 | 8 | 8 | 1 |

## Uzdevumi

**13.1. uzdevums (Ripojošā hešfunkcija ar polinomu):** Pieņemsim, ka alfabētā ir $a = 100$ simboli. Katru simbolu pieraksta ar ciparu pāriem: $\lbrace 00, 01, \ldots, 99 \rbrace$. Izvēlieties ripojošā loga izmēru $m = 5$ un pirmskaitli $q = 23$.

Ievade ir šāda: `[03, 14, 15, 92, 65, 35, 89, 79, 31]`.

* Inicializējiet tukšu ripojošo hash `rH` un pievienojiet pirmos piecus virknes locekļus, izmantojot `append()` funkciju:

  $$
  append(val) = ((u \cdot a) + val)\,\text{mod}\,q = ((u\,\text{mod}\,q) \cdot a + val)\,\text{mod}\,q.
  $$

* Parādiet, kā ripojošā hash var "ripot" no saraksta `[03, 14, 15, 92, 65]` uz `[14, 15, 92, 65, 35]` (vispirms izsaukt `skip(03)`, tad izsaukt `append(35)`).

**13.2. uzdevums (Ripojošā hešfunkcija ar ciklisku polinomu):** Aplūkosim $16$ latīņu burtus ar nejauši piešķirtiem 4-bitu kodiem (t.i., $L = 4$):

| Burts | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| h(x) | 1100 | 0100 | 0010 | 0110 | 0111 | 0000 | 1001 | 1111 | 0101 | 1101 | 1110 | 1011 | 0011 | 1010 | 1000 | 0001 |

Pieņemsim, ka ripojošā loga izmērs ir $k = 5$. Atrodiet hash vērtību $ABIDE$ un pēc tam rotējiet to uz $BIDEN$. Lūdzu, atgādiniet, ka ripojošā hešfunkcija izmanto šādu formulu:

$$
H = s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) )  \oplus \ldots \oplus  s( h(c_{k-1}) ) \oplus   h(c_k),
$$

**13.3. uzdevums (Formulas ripojošajai hešfunkcijai):** Uzzīmējiet formulas Cikliskā polinoma ripojošajai hešfunkcijai:

* Formula, kas piešķir sākumvērtību `RH` tukšai ievadei.
* Formula, kas pievieno jaunu rakstzīmi $c_i$ tekošajam stringam.
* Formula, kas izlaiž esošā saraksta pirmo elementu $c_j$, saīsinot tekošo stringu.

**13.4. uzdevums (Naivās tekstu meklēšanas vidējā sarežģītība):** Pieņemsim, ka paraugs $P$ un teksts $T$ ir nejauši izvēlēti virknēm ar garumiem $m$ un $n$ no alfabēta ar $a$ burtiem ($a \geq 2$). Kāds ir sagaidāmais burtu salīdzināšanu skaits naivajā algoritmā, ja katram salīdzinājumam ir izdošanās iespēja $1/a$?

## Atsauces

BM algoritma aprēķinu piemērs.

* [Good Suffix Heuristic](https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/)
* [Visualizing String Matching](http://whocouldthat.be/visualizing-string-matching/)

<!--
Piezīmes par avotiem (no strings02-kmp-and-bm/figs/README.txt):
1. [Lekciju konspekts](../algorithms-bin/liet2008-13-v3.doc) - Noderīgi pseidokodi, bet
labā sufiksa tabulas piemēram "abcab" izmanto "vājo" definīciju.
2. [BM algoritma vispārīgs apraksts](https://www.youtube.com/watch?v=4Xyhb72LCX4) - "Ģenētisks" virkņu meklēšanas piemērs;
labi skaidrots, bet arī tur labā sufiksa tabulas rēķināšanai izmanto "vājo" definīciju.
3. [Sliktā simbola tabula](https://www.youtube.com/watch?v=G-h1Dph9IOE) - Sliktā simbola tabulu
definē neparasti (`$m - \lambda(j)$` mūsu apzīmējumos) un to pašu rēķina kļūdaini.
4. [Labo sufiksu tabulas zīmējums](https://www.youtube.com/watch?v=lkL6RkQvpMM) - tikai
grafisks attēlojums bez burtu piemēriem.
-->
