---
layout: default
title: "Berouza-Vīlera transformācija"
permalink: /lectures/lossless_burrows_wheeler/
---
# 4. Berouza-Vīlera transformācija

To piedāvājuši M.Berouzs (*Michael Burrows*) un D.Vīlers (*David Wheeler*) 1994.gadā. Transformācija bija pazīstama D.Vīleram arī agrāk; M.Berouzs izdomāja efektīvu algoritmu, kā veikt šo transformāciju.

Berouza-Vīlera transformācijas (BWT) ideja: Ievades tekstā samaina burtu secību tā, ka tie burti, kuri atrodas tūlīt aiz (vai arī - tieši pirms) līdzīgiem kontekstiem, nonāk blakus.

Citiem vārdiem - teksta burtus ar īpašu pārveidojumu pārkārto tā, ka pārkārtojumā atspoguļojas teksta "iekšējās simetrijas"; nereti blakus nonāk atkārtoti burti.

## Kodēšana ar pārvietošanu uz priekšu

Pirms BWT aplūkojam citu kodējumu, ko sauc par *Move-to-front*. To bieži lieto tūlīt pēc Berouza-Vīlera transformācijas, bet to var izmantot arī neatkarīgi -- jebkuras ziņojumu virknes iekodēšanai.

Ja ievadē ir teksts, kurā mēdz bieži nonākt blakus vienādi burti (vai arī burti no nelielas kopas, kas mazāka par pilno alfabētu). to var efektīvi saspiest, ar *Move-to-front* kodējumu:

1. Alfabēta burtus sakārto sarakstā, kura pozīcijas numurē, sākot ar $0$.
2. Katru burtu kodē ar tā pozīciju šajā sarakstā, tad pārvieto šo burtu uz saraksta pašu sākumu.

Vajadzīga datu struktūra -- saraksts $L$, kas ļauj atrast burta kārtas numuru sarakstā $L.\textsf{index}(c)$, ļauj izmest elementu dotajā pozīcijā $L.\textsf{delete}(\textit{pos})$ un ļauj iespraust izmesto elementu saraksta sākumā $L.\textsf{insert}(\textit{pos},c)$. Biežāk lietotie burti atradīsies saraksta priekšā, izejā būs galvenokārt mazi skaitļi. (Ja ievadē biežāk lietotie burti lēnām mainās, attiecīgi adaptējas arī saraksts.)

**Piemērs:** Ar $\textsf{MoveToFrontEncode}()$ iekodēt šādu virkni: `abaccab` alfabētā $S=\lbrace \mathtt{a}, \mathtt{b}, \mathtt{c} \rbrace$.

Tabulā attēlojam katra ievades burta apstrādi - katra soļa beigās izvadei pievieno jaunu skaitli. Alfabēta permutācija parādīta *pirms* attiecīgā ievades burta apstrādes. Pēc kārtējā burta apstrādes alfabētu pārkārto, pārvietojot iekodēto burtu uz pašu sākumu.

| Ievade | Izvade | Alfabēts pirms soļa |
| --- | --- | --- |
| **a**, b, a, c, c, a, b | 0 | `[a,b,c]` |
| a, **b**, a, c, c, a, b | 0,1 | `[a,b,c]` |
| a, b, **a**, c, c, a, b | 0,1,1 | `[b,a,c]` |
| a, b, a, **c**, c, a, b | 0,1,1,2 | `[a,b,c]` |
| a, b, a, c, **c**, a, b | 0,1,1,2,0 | `[c,a,b]` |
| a, b, a, c, c, **a**, b | 0,1,1,2,0,1 | `[c,a,b]` |
| a, b, a, c, c, a, **b** | 0,1,1,2,0,1,2 | `[a,c,b]` |
| N/A | N/A | `[b,a,c]` |

**Piemērs:** Ar $\textsf{MoveToFrontEncode}()$ iekodēt šādu virkni: `abababca` alfabētā $S=\lbrace \mathtt{a}, \mathtt{b}, \mathtt{c} \rbrace$.

| Ievade | Izvade | Alfabēts pirms soļa |
| --- | --- | --- |
| **a**, b, a, b, a, b, c, a | 0 | `[a,b,c]` |
| a, **b**, a, b, a, b, c, a | 0,1 | `[a,b,c]` |
| a, b, **a**, b, a, b, c, a | 0,1,1 | `[b,a,c]` |
| a, b, a, **b**, a, b, c, a | 0,1,1,1 | `[a,b,c]` |
| a, b, a, b, **a**, b, c, a | 0,1,1,1,1 | `[b,a,c]` |
| a, b, a, b, a, **b**, c, a | 0,1,1,1,1,1 | `[a,b,c]` |
| a, b, a, b, a, b, **c**, a | 0,1,1,1,1,1,2 | `[b,a,c]` |
| a, b, a, b, a, b, c, **a** | 0,1,1,1,1,1,2,2 | `[c,b,a]` |
| N/A | N/A | `[a,c,b]` |

**Piemērs:** Atkodēt `010010` alfabētā $S=\lbrace \mathtt{a}, \mathtt{b} \rbrace$

| Ievade | Izvade | Alfabēts pirms soļa |
| --- | --- | --- |
| **0**, 1, 0, 0, 1, 0 | a | `[a,b]` |
| 0, **1**, 0, 0, 1, 0 | a,b | `[a,b]` |
| 0, 1, **0**, 0, 1, 0 | a,b,b | `[b,a]` |
| 0, 1, 0, **0**, 1, 0 | a,b,b,b | `[b,a]` |
| 0, 1, 0, 0, **1**, 0 | 0,b,b,b,a | `[b,a]` |
| 0, 1, 0, 0, 1, **0** | a,b,b,b,a,a | `[a,b]` |
| N/A | N/A | `[a,b]` |

## Berouza-Vīlera transformācija

**Definīcija:** Par $n$ elementu saraksta *permutāciju* (*permutation*) sauc jebkuru citu sarakstu, kurā izmainīta šo elementu secība. Par *ciklisku permutāciju* sauc tādu permutāciju, kurā elementiem saglabājas abi kaimiņi -- t.i. vienu vai vairākus elementus no saraksta beigām pārliek uz saraksta sākumu, nemainot pārvietoto elementu savstarpējo secību.

Ja visi burti ir atšķirami, tad $n$ elementu sarakstam ir ir $n!$ permutāciju (bet tikai $n$ cikliskas permutācijas).

**Piemērs:** Izrakstīt visas cikliskās permutācijas vārdiem `BONBON$`, un `BANANA$`, tad sakārtot tās alfabētiski.

```text
B O N B O N $              $ B O N B O N
$ B O N B O N              B O N $ B O N
N $ B O N B O              B O N B O N $
O N $ B O N B     --->     N $ B O N B O
B O N $ B O N              N B O N $ B O
N B O N $ B O              O N $ B O N B
O N B O N $ B              O N B O N $ B
```

```text
B A N A N A $              $ B A N A N A
$ B A N A N A              A $ B A N A N
A $ B A N A N              A N A $ B A N
N A $ B A N A     --->     A N A N A $ B
A N A $ B A N              B A N A N A $
N A N A $ B A              N A $ B A N A
A N A N A $ B              N A N A $ B A
```

Berouza-Vīlera transformācija ir šajā sakārtojumā iegūtā pēdējā kolonna -- BWT(`BONBON$`) = `NN$OOBB` un BWT(`BANANA$`) = `ANNB$AA`.

**Definīcija:** Par alfabēta burta $x \in S$ *labo kontekstu* dotajā tekstā $T$ sauc jebkuru stringu fiksētā garumā $k$, kas tieši seko aiz šī burta $x$ (ja burts $x$ ir tuvu vārda beigām, tad kontekstu iegūst cikliski pārvietojoties uz teksta sākumu).

Berouza-Vīlera transformācija sakārto visus labos kontekstus leksikogrāfiski un izraksta teksta burtus secībā, kuru nosaka šie labie konteksti.

![Berouza-Vīlera fragments](figs/burrows-wheeler-fragment.png)

> *Piezīme:* Varētu kārtot arī inversi leksikogrāfiski (t.i. alfabētiski, bet skatoties vārdam no otra gala). Šādā gadījumā pirmā kolonna kļūtu par Berouza-Vīlera transformāciju. T.i. var izmantot arī sakārtošanu pēc "kreisajiem kontekstiem". Šādi to apraksta Guy Blelloch *Introduction to Data Compression* grāmatā.

### Apgrieztā Berouza-Vīlera transformācija

No Berouza-Vīlera transformācijas (pēdējās kolonnas) var izsecināt, kāda būs pirmā kolonna (tie paši burti, bet alfabētiskā secībā). Var pamatot, ka vienādo burtu secība Berouza-Vīlera transformācijas rezultātā nemainās. Tāpēc pietiek zināt šīs divas kolonnas un izmantot L2F (Last-to-First) kodējuma tabulu.

Ir arī iespējams atjaunot visu matricu:

![Berouza-Vīlera atkodēšana](figs/burrows-decode.png)

*Decode*

**Algoritma apraksts**

1. Ciklā katru kolonnu pabīda vienu soli pa labi un tad pārkārto. Permutāciju nosaka pēdējā kolonna matricā.
2. Šādi, ja mēs varam atrast kolonnu $j$, varam iegūt kolonnu $j+1$ no kolonnas $j$. Šo atkārtojot, varam atjaunot visu matricu $M$.
3. Lai rekonstruētu sākotnējo tekstu $T$, mums pietiek atrast tikai vienu rindiņu matricā.

> *Piezīme:* Sk. 177 lapu no [https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf](https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf)

## Efektīvs BWT ar sufiksu kokiem

**Apgalvojums:** BWT naivā implementācija prasa laiku $O(n^2 \log n)$ un $O(n^2)$ telpu.

**Pierādījums:** Ciklisko permutāciju izrakstīšana prasa aizpildīt $n \times n$ matricu ar burtiem; aizņemtā telpa ir $O(n^2)$. Pēc tam jāšķiro $n$ stringi; divu stringu salīdzināšana sliktākajā gadījumā prasa $O(n)$ soļus. Pilnā laika sarežģītība ir $O(n \log_2 n) \cdot O(n) = O(n^2 \log_2 n)$.

Praksē garus tekstus saspiež veicot Berouza-Vīlera transformāciju atsevišķiem blokiem. Tipisks bloku garums ir daži simti kilobaitu. Blokiem nav labi būt pārāk gariem, lai tos būtu praktiski apstrādāt. Tiem nevajadzētu arī būt pārāk īsiem, lai atrastu un optimāli izmantotu atkārtotos kontekstus. Tomēr $O(n^2 \log_2 n)$ laika sarežģītība ir ļoti neefektīvi arī tipiskām $n$ vērtībām (100KiB līdz 1MiB).

Berouza-Vīlera transformāciju var veikt lineārā laikā no vārda garuma $O(n)$, izmantojot *sufiksu masīvus* (*suffix arrays*).

**Definīcija:** Par ievades stringa $w$ sufiksu masīvu sauc datu struktūru, kuras atslēgu kolonnā ir sanumurēti $w$ sufiksi (katra sufiksa numurs parāda, cik burti no vārda sākuma jānodzēš, lai dabūtu šo sufiksu), bet otrā kolonnā - katra sufiksa kārtas numurs alfabētiskajā sakārtojumā, sākot ar $0$.

**Piemērs:** Sufiksu masīvs stringam $w$ = `BANANA$`. Izveidojam alfabētisku sufiksu sakārtojumu:

* `$` -> 6 (cik burti jānodzēš no `BANANA$`, lai paliktu dolārs)
* `A$` -> 5
* `ANA$` -> 3
* `ANANA$` -> 1
* `BANANA$` -> 0
* `NA$` -> 4
* `NANA$` -> 2

Iegūstam, ka sufiksu masīvs ir `[6, 5, 3, 1, 0, 4, 2]`

**Piemērs:** Sufiksu masīvs stringam $w$ = `TATACATTAG$`.

| Sufikss (to neglabā) | Sufiksa numurs |
| --- | --- |
| `$` | 10 |
| `ACATTAG$` | 3 |
| `AG$` | 8 |
| `ATACATTAG$` | 1 |
| `ATTAG$` | 5 |
| `CATTAG$` | 4 |
| `G$` | 9 |
| `TACATTAG$` | 2 |
| `TAG$` | 7 |
| `TATACATTAG$` | 0 |
| `TTAG$` | 6 |

Sufiksu kokus var izmantot stringu meklēšanā. (Piemēram, var informāciju labajā kolonnā pielietot, lai atrastu `TA` visās vietās, var izmantot bināro meklēšanu -- atrodot burtu `T` sākotnējā stringā tajās pozīcijās, uz kurām norāda sufiksu masīvs. Pēc tam meklē, kur atrodas otrs burts `A`.)

**Apgalvojums:** Stringam $w$ no $|w| = n$ burtiem sufiksu masīvu var izveidot $O(n)$ laikā un tas aizņem $O(n)$ vietu.

(Šo apgalvojumu pamato pašās kursa beigās - sufiksu koka/masīva algoritmā par stringu meklēšanu).

**Apgalvojums:** Sufiksu masīvs stringam $w$, kura beigās ir dolārs (alfabētiski pirms visiem citiem burtiem alfabētā), sufiksu masīva pozīcijas sakrīt ar Berouza-Vīlera sakārtoto rotāciju pozīcijām:

![Rotācijas un sufiksi](figs/rotations-and-suffixes.png)

Tā kā Berouza-Vīlera transformācija ir redzama pēdējā kolonnā, tad to var iegūt

**BWT Transformācija ar Sufiksu Masīvu**

Ievade ir vārds $w$, kura pēdējais simbols ir `$`.

$\textsf{efficientBWT}(w)$
1. $\quad A = \textsf{getSuffixArray}(w) \quad$ *// inicializē sufiksu masīvu*
2. $\quad n = |w| \quad$ *// n ir stringa w garums, ieskaitot beigu dolāru*
3. $\quad$ **for** $i = 0$ **to** $n-1$ *// atkārto n reizes*
4. $\quad\quad j = A[i]-1$ *// j ir vienu pozīciju pirms A[i]*
5. $\quad\quad$ **if** $j == -1$
6. $\quad\quad\quad j == n-1$ *// "-1" pozīcija cikliskā permutācijā ir stringa beigās*
7. $\quad\quad \textsf{output}(w[j])$

**Piemērs:** Stringam $w$ = `BANANA$` sufiksu masīvs ir `[6, 5, 3, 1, 0, 4, 2]`. Tāpēc algoritma rezultāts būs šāds:

| $i$ | $A[i]$ | $j=A[i]-1$ | $w[j]$ |
| --- | --- | --- | --- |
| 0 | 6 | 5 | `A` |
| 1 | 5 | 4 | `N` |
| 2 | 3 | 2 | `N` |
| 3 | 1 | 0 | `B` |
| 4 | 0 | 6 | `$` |
| 5 | 4 | 3 | `A` |
| 6 | 2 | 1 | `A` |

Jau agrākā piemērā redzējām, ka BWT(`BANANA$`) = `ANNB$AA`, kas sakrīt ar šī algoritma izvadi.

**Piemērs:** Izveidot BWT un sufiksu masīvu stringam `CAA` (bez beigu dolāra).

Izrakstām un alfabētiski sakārtojam cikliskās permutācijas:

```text
C A A             A A C
A C A     -->     A C A
A A C             C A A
```

Pēdējā kolonna (BWT transformācijas rezultāts) ir `CAA`.

> *Piezīme:* Lai šādu BWT transformāciju bez dolāra atkodētu, atodētājam ir arī jāzina, kur BWT transformācijas rezultātā atrodas pirmais burts. Pretējā gadījumā viņš var atjaunot BWT matricu, bet nevar uzzināt, kura no matricā norādītajām cikliskajām permutācijām ir īstā.

Izrakstām un alfabētiski sakārtojam sufiksus:

```text
C A A              A      (idx=2, šajā sufiksā nodzēsti pirmie 2 burti)
A A       --->     A A    (idx=1, nodzēsts pirmais 1 burts)
A                  C A A  (idx=0, nodzēsti 0 burti)
```

Sufiksu masīvs ir `[2,1,0]` (sufiksu indeksi izrakstīti alfabētiski sakārtotajā secībā). Mēģinām šādam stringam lietot $\textsf{efficientBWT}(w)$:

| $i$ | $A[i]$ | $j=A[i]-1$ | $w[j]$ |
| --- | --- | --- | --- |
| 0 | 2 | 1 | `A` |
| 1 | 1 | 0 | `A` |
| 2 | 0 | 2 | `C` |

Ievērojam, ka iegūtais rezultāts `AAC` nesakrīt ar BWT īsto rezultātu `CAA`. Tāpēc $\textsf{efficientBWT}(w)$ ir svarīgs pieņēmums, ka $w$ beidzas ar dolāru (pašu pirmo burtu alfabētā).

## Uzdevumi

**4.1. uzdevums:** Ierakstīt Berouza-Vīlera transformāciju vārdam `ABBA$`. Aiz tās norādīt, kurā vietā šajā transformācijā ir strings `ABBA$`. *Piezīme.* Sakārtotajā matricā virkņu numerācija sākas no $1$.

**Atbilde:** Iegūst cikliskas `ABBA$` permutācijas, sakārto leksikogrāfiski:

$$
\left( \begin{array}{ccccc}
\text{A} & B & B & A & \$ \\
\$ & A & B & B & A \\
A & \$ & A & B & B \\
B & A & \$ & A & B \\
B & B & A & \$ & A
\end{array} \right) \rightarrow
\left( \begin{array}{ccccc}
\text{\$} & A & B & B & A \\
A & \$ & A & B & B \\
A & B & B & A & \$ \\
B & A & \$ & A & B \\
B & B & A & \$ & A
\end{array} \right).
$$

Transformācijas rezultāts ir labējā kolonna: `AB$BA`. Sākotnējā virkne ir 3.rindiņa. $\square$

**4.2. uzdevums:** Iepriekšējā jautājumā iegūtajai `ABBA$` Berouza-Vīlera transformācijas virknei uzrakstīt **Move-to-Front** kodu, ja sākotnējā burtu secība alfabētā ir `$` < `A` < `B`. *Piezīme.* **Move-to-Front** algoritmos alfabēta numerācija sākas no $0$.

* Uzrakstīt virkni, kas iegūta ar Berouza-Vīlera transformāciju.
* Uzrakstīt šīs virknes move-to-front kodu.

**Atbilde:** Katrā **Move-to-Front** kodēšanas solī pārliekam tekošo simbolu uz alfabēta sākumu.

| Virkne | Kods | Alfabēts |
| --- | --- | --- |
| `*A*B$BA` | 1 | `($,A,B)` |
| `A*B*$BA` | 2 | `(A,$,B)` |
| `AB*$*BA` | 2 | `(B,A,$)` |
| `AB$*B*A` | 2 | `($,B,A)` |
| `AB$B*A*` | 2 | `(B,$,A)` |

Iegūtais kods ir `12222`. $\square$

## Izmantotā literatūra

* [https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf](https://www.cs.helsinki.fi/u/tpkarkka/opetus/12s/spa/lecture11.pdf)
* [https://docs.python.org/3/library/bz2.html](https://docs.python.org/3/library/bz2.html)
* [https://serverfault.com/questions/2600/how-do-you-set-bzip2-block-size-when-using-tar](https://serverfault.com/questions/2600/how-do-you-set-bzip2-block-size-when-using-tar)
* [https://youtu.be/w-Cnkg6ANG8?si=wC5UeoUDhXq56qzw](https://youtu.be/w-Cnkg6ANG8?si=wC5UeoUDhXq56qzw).
