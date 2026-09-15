---
layout: default
title: "Bezzudumu saspiešana: Lempela-Ziva algoritmi"
permalink: /lectures/lossless_lempel_ziv/
---
# 3. Bezzudumu saspiešana: Lempela-Ziva algoritmi

A.Lempels (*Abraham Lempel*), J.Zivs (*Jacob Ziv*) un T.Velčs (*Terry Welch*) izveidoja dažus radniecīgus saspiešanas algoritmus, kas izmanto adaptīvu vārdnīcu, kurā glabājas biežāk atkārtojamās apakšvirknes. Šos sauc par Lempela-Ziva algoritmiem. Tie ir [LZ77 un LZ78](https://en.wikipedia.org/wiki/LZ77_and_LZ78), [Lempel–Ziv–Welch (LZW)](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch), [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) un daži citi.

Kursā aplūkosim LZ77 un LZW (kas ir uzlabots LZ78 variants).

## Motivācija

Saspiešana ar vārdnīcu (LZ77 vai LZW) var sasniegt lielāku saspiešanas attiecību nekā entropijas kodi (Hafmana vai aritmētiskais), jo izmanto to, ka ievades datos nākošie simboli ir atkarīgi no iepriekšējiem.

Hafmana un aritmētiskais kods ir optimāli tad, ja ziņojumi ir neatkarīgi un to varbūtības ir zināmas. Reālos failos tā nav: tekstā, pirmkodā, HTML lapās un žurnālfailos atkārtojas veseli vārdi, identifikatori un rindiņas, bet Hafmana kods katru burtu kodē ar vienu un to pašu kodavārdu, pat ja viss vārds jau ir redzēts iepriekš. Turklāt entropijas kodam varbūtību modelis ir jāzina iepriekš vai jānosūta kopā ar datiem. Vārdnīcas metodes šīs problēmas apiet: atkārtotu fragmentu aizstāj ar atsauci uz tā iepriekšējo parādīšanos, modeli neviens neveido un nesūta, datus apstrādā vienā caurlaidē, un atspiešana ir vienkārša kopēšana, tāpēc ļoti ātra. Laikā, kad disku vieta un modemu pārraides ātrums bija dārgi, tas padarīja LZ algoritmus par pamatu lielākajai daļai vispārīgas nozīmes arhivatoru (izņēmums ir, piemēram, bzip2, sk. nodaļu par Berouza-Vīlera transformāciju). Teorētiski LZ algoritmi ir *universāli*: jebkuram stacionāram un ergodiskam avotam tie asimptotiski sasniedz tā vidējo entropiju, pat nezinot avota statistiku (sk. "Matemātiskais pamatojums").

## Vēsture

**Par LZ77 algoritmu:** LZ77 (publicēts 1977.gadā) izmanto pašu tekstu kā vārdnīcu; slīdošo logu un atpakaļejošās references. Saspiešanas formāti kā DEFLATE, ko izmanto ZIP un gzip failos un PNG attēlos.

**Par LZW algoritmu:** LZW (publicēts 1984.gadā) ievieš dinamisku vārdnīcas veidošanu, neprasot iepriekšdefinētu simbolu tabulu (ir adaptīva saspiešanas metode). Tas ir 
konkrēts variants algoritmam LZ78 (Lempela-Ziva 1978.gada algoritms). Sastopams GIF attēlu saspiešanas formātā un UNIX "compress" lietojumprogrammā.

Daudzveidīgākie mūsdienu lietojumi ir algoritmam LZ77. 
LZW lietojumi ir GIF un UNIX "compress" programma, 
bet licencēšanas ierobežojumu un arī citu iemeslu dēļ GIF šobrīd ir 
pamatos aizstāts ar PNG. 

A.Lempels un J.Zivs strādāja Tehnionā (Izraēlas Tehnoloģiju institūtā Haifā), un viņu mērķis sākotnēji bija teorētisks -- atrast *universālu* saspiešanas metodi, kurai nav jāzina avota varbūtības. Rezultāti publicēti žurnālā *IEEE Transactions on Information Theory* 1977.gadā (LZ77) un 1978.gadā (LZ78). T.Velčs, strādājot Sperry pētniecības centrā, 1984.gadā žurnālā *IEEE Computer* aprakstīja LZW -- LZ78 variantu, ko viegli realizēt ātri gan programmās, gan aparatūrā. LZW drīz izmantoja UNIX programma `compress`, bet 1987.gadā -- CompuServe izveidotais GIF attēlu formāts. LZW patents piederēja Sperry pēctecim Unisys, tāpēc brīvās programmatūras autori meklēja algoritmus bez patentu riska: 1992.gadā izveidotā programma `gzip` aizstāja `compress`, un tā lieto DEFLATE -- LZ77 kopā ar Hafmana kodu, ko F.Kacs (*Phil Katz*) 1993.gadā ieviesa arhivatorā PKZIP 2. Kad 1994.gada beigās Unisys un CompuServe paziņoja par licences maksu GIF programmatūrai, kā GIF aizstājējs tika izstrādāts PNG formāts (standartizēts 1996.gadā), kas arī lieto DEFLATE. LZW patenti beidzās 2003.-2004.gadā, taču tad DEFLATE jau bija kļuvis par standartu ZIP arhīvos, HTTP saspiešanā un PNG attēlos.

## Algoritmi

### LZ77 algoritms

#### Ideja

Algoritms izmanto logu (*view*) -- buferi ar fiksētu garumu (piemēram, 32 KiB jeb 32768 baiti). Tuvu loga beigām atrodas kursors, kas rāda uz kādu burtu.

* Pirms kursora ir atpakaļskata buferis (gandrīz viss 32 KiB logs)
* Pēc kursora ir priekšskata buferis -- piemēram, $32$ baiti. (Izvēlēties garāku priekšskata buferi apgrūtina prefiksu meklēšanu; bet $32$ burtu virknītes ir tādas, ko varam cerēt atrast iepriekšējos datos.)

Šajā gadījumā vārdnīca ir gabals no jau iekodētās virknes. Iekodētājs redz beigu gabalu no iekodētās virknes kā slīdošo logu:

![LZ77 logs](figs/lz77-window.png)

Logs ir kā atmiņas buferis, kurā var atrast nesen iekodētas virknes un izmantot tās, lai īsāk pierakstītu to virknes gabaliņu, kurš sekos.

#### Pseidokods

Kodētājs izvada trijniekus $(d, \ell, x)$: sakritība sākas $d$ pozīcijas pirms kursora, tās garums ir $\ell$, un $x$ ir simbols, kas seko aiz sakritības. Ja sakritības nav, izvada $(0, 0, x)$. Sakritība drīkst sākties logā, bet turpināties priekšskata buferī (pārklāties ar kodējamo daļu) -- tā ar vienu trijnieku iekodē garas atkārtojumu virknes.

$\textsf{LZ77-Encode}(T, n, W, L)$ $\quad$ *// $T[1:n]$ -- ievade; $W$ -- loga garums; $L$ -- priekšskata bufera garums*
1. $i = 1$ $\quad$ *// kursora pozīcija*
2. **while** $i \leq n$
3. $\quad d = 0$; $\;\;\ell = 0$ $\quad$ *// garākā līdz šim atrastā sakritība*
4. $\quad$ **for** $s = i - 1$ **downto** $\max(1, i - W)$ $\quad$ *// iespējamie sakritības sākumi logā, sākot ar tuvāko*
5. $\quad\quad k = 0$
6. $\quad\quad$ **while** $k < \min(L, n - i)$ **and** $T[s + k] == T[i + k]$
7. $\quad\quad\quad k = k + 1$
8. $\quad\quad$ **if** $k > \ell$ **then** $d = i - s$; $\;\ell = k$
9. $\quad \textsf{Output}(d, \ell, T[i + \ell])$
10. $\quad i = i + \ell + 1$

Rindiņā 6 nosacījums $k < n - i$ garantē, ka aiz sakritības paliek vismaz viens simbols $T[i + \ell]$, ko izvadīt 9.rindiņā. Rindiņās 4-8 ir naiva meklēšana -- katram trijniekam sliktākajā gadījumā $O(W \cdot L)$ simbolu salīdzināšanu. Tā kā $s$ iet no tuvākās pozīcijas uz tālāko un sakritību aizstāj tikai ar stingri garāku, vienāda garuma sakritībām tiek izvēlēta mazākā nobīde $d$.

$\textsf{LZ77-Decode}(C)$ $\quad$ *// $C$ -- trijnieku $(d, \ell, x)$ virkne*
1. $m = 0$ $\quad$ *// līdz šim atkodēto simbolu skaits masīvā $T$*
2. **for each** $(d, \ell, x) \in C$
3. $\quad$ **for** $k = 1$ **to** $\ell$
4. $\quad\quad T[m + k] = T[m + k - d]$ $\quad$ *// kopē pa vienam simbolam*
5. $\quad m = m + \ell + 1$
6. $\quad T[m] = x$
7. **return** $T[1:m]$

Atkodētājs neko nemeklē, tikai kopē, tāpēc tas ir daudz ātrāks par kodētāju. 4.rindiņā simbolus kopē pa vienam, jo avota apgabals var pārklāties ar tikko ierakstītajiem simboliem (ja $d < \ell$).

#### Piemērs

![LZ77 piemērs](figs/lz77-example.png)

Attēlā kodē virkni `aacaacabcabaaac` ar loga garumu $W = 6$ un priekšskata bufera garumu $L = 4$ (ar šiem parametriem $\textsf{LZ77-Encode}$ izvada tieši attēlā redzamos trijniekus). Rāmītī ir kursora simbols $T[i]$, treknrakstā -- logs (līdz $6$ simboliem pirms kursora), bet pasvītroti ir pārējie priekšskata bufera simboli.

1. Kursors $i = 1$: logs ir tukšs, tāpēc sakritību nav kur meklēt. Burtu izvada kā $(0, 0, \mathtt{a})$, un kursors pārvietojas par $1$.
2. Kursors $i = 2$: logā ir `a`, kas sakrīt ar kursora burtu `a`. Nākamie burti (`a` 2.pozīcijā un `c` 3.pozīcijā) vairs nesakrīt, tāpēc $d = 1$, $\ell = 1$, un aiz sakritības ir `c`. Izvada $(1, 1, \mathtt{c})$, kursors pārvietojas par $\ell + 1 = 2$.
3. Kursors $i = 4$: logā ir `aac`. Garākā sakritība sākas 1.pozīcijā ($d = 3$): pozīcijās $1 \ldots 4$ ir `aaca`, tieši tāpat kā pozīcijās $4 \ldots 7$. Avota apgabals pārklājas ar kodējamo daļu, jo tā pēdējais burts ir pati kursora pozīcija $4$. Aiz sakritības ir `b`: izvada $(3, 4, \mathtt{b})$, kursors pārvietojas par $5$.
4. Kursors $i = 9$: logā ir `caacab` (pozīcijas $3 \ldots 8$). Burts `c` logā ir divās vietās: no 3.pozīcijas sakrīt tikai `ca` ($\ell = 2$), bet no 6.pozīcijas -- `cab` ($\ell = 3$). Izvēlas garāko sakritību $d = 9 - 6 = 3$, $\ell = 3$, aiz kuras ir `a`: izvada $(3, 3, \mathtt{a})$, kursors pārvietojas par $4$.
5. Kursors $i = 13$: logā ir `abcaba` (pozīcijas $7 \ldots 12$), neiekodēti palikuši burti `aac`. Garākā sakritība `aa` sākas tūlīt pirms kursora ($d = 1$) un pārklājas ar kodējamo daļu -- atkodētājs to iegūs, divreiz nokopējot iepriekšējo burtu. Aiz tās paliek pēdējais burts `c`: izvada $(1, 2, \mathtt{c})$, un kodēšana beidzas.

Atkodētājs ar $\textsf{LZ77-Decode}$ katram trijniekam nokopē $\ell$ burtus un pieraksta $x$: `a` + `ac` + `aacab` + `caba` + `aac` = `aacaacabcabaaac`. Tātad $15$ burtu vietā ir $5$ trijnieki -- bet katrs trijnieks aizņem vairāk vietas nekā viens burts, tāpēc praksē tos kodē vēl tālāk (sk. "No trijniekiem līdz saspiestam failam").

#### Uzlabojumi gzip implementācijā

Dažas LZ77 izmaiņas, ko lieto "gzip".

**Divi izvades formāti:** Algoritms vai nu cenšas atrast prefiksu vismaz garumā trīs (un tad to izvada kā LZ77 trijnieku), vai arī izvada burtus pa vienam. (Izmanto vienu papildus bitu, lai atšķirtu abus izvades formātus). Šāda izmaiņa ļauj ietaupīt daudz vietas tādiem failiem, kurus nevar labi saspiest, jo tad nav jāizvada pilnvērtīgs trijnieks (ar pozīcijas un garuma laukiem).

**Hafmana kodi:** `gzip` burtus un sakritību garumus kodē ar vienu Hafmana koku, bet nobīdes -- ar otru (sk. nākamo apakšsadaļu).

**Nerijīgais variants:** LZ77 algoritms ir rijīgs -- tas vienmēr mēģina atrast garāko prefiksu, sākot ar priekšskata bufera pirmo simbolu. (Neatkarīgi no tā, kā tas iespaidos tālākos prefiksus.) Dažreiz ir izdevīgi izvadīt vienu simbolu pašreizējā pozīcijā, cerot atrast garāku prefiksu vēlāk.

**Heštabulas ar prefiksiem:** `gzip` būvē heštabulu, kurā salikti visi sastaptie stringi garumā 3 kā atslēgas. (Ja tiem ir vairāki turpinājumi, tos saliek heštabulas spainītī atpakaļejošā secībā). Ja ir vairāki prefiksi, tad LZ77 ir izdevīgāk izvēlēties pašu nesenāko (ar vismazāko nobīdi jeb *offset*), jo tas rada visnevienmērīgāko sadalījumu, ko labi saspiest ar Hafmana kodu.

#### No trijniekiem līdz saspiestam failam

LZ77 trijnieki paši par sevi vēl nav saspiests fails: ja katru $(d, \ell, x)$ glabātu $4$ baitos, iepriekšējā piemēra $15$ baitu virkne kļūtu par $20$ baitiem. Praktiskos formātos izvadi apstrādā tālāk. Visizplatītākais ir DEFLATE (ZIP, gzip, PNG, HTTP saspiešana):

1. **Divu veidu marķieri.** Trijnieka vietā izvada vai nu burtu (baitu), vai pāri (garums, nobīde), kur $3 \leq \ell \leq 258$ un $1 \leq d \leq 32\,768$ -- tāpat kā 3.1. uzdevuma *gzip* formātā.
2. **Kopīgs alfabēts burtiem un garumiem.** Burti ir simboli $0 \ldots 255$, bloka beigas -- simbols $256$, bet garumi -- simboli $257 \ldots 285$. Lielākiem garumiem viens simbols apzīmē intervālu, un precīzo vērtību norāda papildu biti: piemēram, $257$ nozīmē $\ell = 3$, $260$ nozīmē $\ell = 6$, bet $265$ ar vienu papildu bitu nozīmē $\ell \in \lbrace 11, 12 \rbrace$. Nobīdēm ir atsevišķs alfabēts $0 \ldots 29$ ar tādiem pašiem papildu bitiem: $0$ nozīmē $d = 1$, $2$ nozīmē $d = 3$, bet $29$ ar $13$ papildu bitiem nozīmē $d \in [24\,577; 32\,768]$.
3. **Hafmana kodi.** Datus sadala blokos. Katram blokam saskaita simbolu biežumus un uzbūvē divus Hafmana kokus -- vienu burtu un garumu alfabētam, otru nobīžu alfabētam; papildu bitus raksta nekodētus. Bieži burti, tipiski garumi un tuvas nobīdes iegūst īsus kodavārdus.
4. **Bloku veidi.** Bloka galvenes $3$ biti norāda, vai bloks ir pēdējais, un bloka veidu: *stored* (nesaspiesti dati -- tiem, kurus nevar saspiest), *fixed* (standartā noteikti Hafmana koki, kas nav jāsūta -- izdevīgi īsiem blokiem) vai *dynamic* (koki tiek nosūtīti kā kanoniska Hafmana koda garumi, sk. nodaļu par Hafmana kodu; paši garumi vēlreiz saspiesti ar atkārtojumu kodiem un Hafmana kodu).
5. **Konteiners.** DEFLATE plūsmu ietin faila formātā: *gzip* pievieno galveni (faila vārds, laiks) un beigās CRC-32 kontrolsummu un oriģinālo garumu, *zlib* (PNG, HTTP) -- $2$ baitu galveni un Adler-32 kontrolsummu, bet ZIP -- arī failu katalogu arhīva beigās.

**Piemērs:** 3.1. uzdevuma *gzip* formāta marķieri kā DEFLATE simboli *fixed* blokā:

| Marķieris | DEFLATE simboli | Biti |
| --- | --- | --- |
| `(1,a)`, `(1,b)`, `(1,c)` | $97$, $98$, $99$ | $3 \cdot 8$ |
| `(0,3,6)` | garums $260$, nobīde $2$ | $7 + 5$ |
| `(1,d)` | $100$ | $8$ |
| `(0,4,3)` | garums $257$, nobīde $3$ | $7 + 5$ |
| bloka beigas | $256$ | $7$ |

Kopā ar bloka galveni tie ir $3 + 24 + 12 + 8 + 12 + 7 = 66$ biti jeb $9$ baiti ($13$ baitu vietā). Reāli kompresori sakritības meklē ar heštabulām un heiristikām, tāpēc ne vienmēr atrod garāko sakritību: Python 3.14 `zlib` (zlib-ng 2.2.4) šo virkni sadala kā `a`, `b`, `c`, `a`, (garums $5$, nobīde $3$), `d`, `a`, `b`, `c` un izvada $86$ bitus jeb $11$ baitus. Ar *zlib* galveni tie ir $17$ baiti, *gzip* failā -- $29$ baiti, tātad tik īsai virknei galvenes aizņem vairāk nekā ietaupīts. Garākiem datiem tas atmaksājas: teksts `to be or not to be, that is the question. `, atkārtots $200$ reizes ($8\,400$ baiti), *gzip* failā aizņem $98$ baitus.

Jaunāki formāti (zstd, LZMA/7z) izmanto to pašu LZ77 ideju, bet marķierus kodē efektīvāk -- ar ANS (zstd) vai aritmētisko kodu (LZMA) Hafmana koda vietā (sk. nodaļu par aritmētisko kodu un ANS).

### LZ78 algoritms

#### Ideja

> **TODO:** Vārdnīca, kas sastāv no iepriekš sastaptām frāzēm (nevis slīdošais logs); katra jauna frāze ir kādas vārdnīcas frāzes turpinājums ar vienu burtu.

#### Pseidokods

Kodētājs lasa ievadi pa burtam un pagarina tekošo frāzi $w$, kamēr tā ir vārdnīcā. Ar $wk$ apzīmējam frāzi $w$, kurai galā pierakstīts burts $k$. Vārdnīcā $D$ sākumā ir visi alfabēta $S$ burti (burta kods ir pats burts), bet garākas frāzes saņem numurus $1, 2, 3, \ldots$

$\textsf{LZ78-Encode}(T, n)$ $\quad$ *// $T[1:n]$ -- ievade alfabētā $S$; $D[w]$ -- frāzes $w$ kods*
1. $D = \textsf{New-Dictionary}(S)$ $\quad$ *// $D[x] = x$ katram burtam $x \in S$*
2. $m = 0$ $\quad$ *// pēdējais piešķirtais frāzes numurs*
3. $w = T[1]$
4. **for** $i = 2$ **to** $n$
5. $\quad k = T[i]$
6. $\quad$ **if** $wk \in D$
7. $\quad\quad w = wk$ $\quad$ *// frāzi var pagarināt*
8. $\quad$ **else**
9. $\quad\quad \textsf{Output}(D[w])$
10. $\quad\quad m = m + 1$
11. $\quad\quad D[wk] = m$ $\quad$ *// jauna frāze ar nākamo numuru*
12. $\quad\quad w = k$
13. $\textsf{Output}(D[w])$ $\quad$ *// pēdējā frāze*

Kodētājs vienmēr izvada garāko vārdnīcā atrodamo frāzi $w$ (9. un 13.rindiņa) un vārdnīcai pievieno šo frāzi, pagarinātu par nākamo burtu (11.rindiņa).

$\textsf{LZ78-Decode}(c_1 c_2 \ldots c_r)$ $\quad$ *// $c_j$ -- burts vai frāzes numurs; $D[c]$ -- frāze ar kodu $c$*
1. $D = \textsf{New-Dictionary}(S)$ $\quad$ *// $D[x] = x$ katram burtam $x \in S$*
2. $m = 0$
3. $w = D[c_1]$
4. $\textsf{Output}(w)$
5. **for** $j = 2$ **to** $r$
6. $\quad$ **if** $c_j \in D$
7. $\quad\quad v = D[c_j]$
8. $\quad$ **else** $\quad$ *// $c_j = m + 1$: šī frāze vēl nav vārdnīcā*
9. $\quad\quad v = w\,w[1]$
10. $\quad \textsf{Output}(v)$
11. $\quad m = m + 1$
12. $\quad D[m] = w\,v[1]$ $\quad$ *// iepriekšējā frāze ar tekošās frāzes pirmo burtu*
13. $\quad w = v$

Atkodētājs uzzina katru jauno frāzi vienu soli vēlāk nekā kodētājs, jo 12.rindiņā tam jāzina tekošās frāzes $v$ pirmais burts. Tāpēc kods $c_j$ var norādīt uz frāzi $m + 1$, kuras vārdnīcā vēl nav. Šī frāze ir $w$ ar pievienotu savu pirmo burtu, kas sakrīt ar $w[1]$, tātad $v = w\,w[1]$ (8.-9.rindiņa; sk. 3.4. uzdevumu).

#### Piemērs

Dota virkne `abcabcabcdabcaba`, kura jānokodē, izmantojot LZ78 algoritmu.

| Solis | Garākais w vārdnīcā | k | Izvade | Pievieno vārdnīcai |
| --- | --- | --- | --- | --- |
| 1. | a | b | a | ab |
| 2. | b | c | b | bc |
| 3. | c | a | c | ca |
| 4. | ab | c | ab | abc |
| 5. | ca | b | ca | cab |
| 6. | bc | d | bc | bcd |
| 7. | d | a | d | da |
| 8. | abc | a | abc | abca |
| 9. | ab | a | ab | aba |
| 10. |  |  | a |  |

Parasti kodē burtus par burtiem, bet garākas virknes aizstāj ar tā soļa numuru, kurā šī virkne ir ievietota vārdnīcā. Tas nozīmē, ka šajā piemērā virkne `ab` tiktu kodēta kā 1, `bc` kā 2, `ca` kā 3, utt. Beigās iegūta virkne `a,b,c,1,3,2,d,4,1,a`

### LZW algoritms

LZW atsevišķi nevingrinām: tas ir LZ78 variants, un augstāk aprakstītais "LZ78" algoritms jau izmanto LZW galveno ideju. Svarīgākās sakarības:

* **Klasiskais LZ78** sāk ar tukšu vārdnīcu un izvada pārus $(i, x)$: garākās vārdnīcā atrastās frāzes numuru $i$ ($0$ -- tukšā frāze) un simbolu $x$, kas seko aiz tās. Vārdnīcai pievieno $i$-to frāzi, kurai galā pierakstīts $x$.
* **LZW** (T.Velčs, 1984) vārdnīcā jau sākumā ievieto visus alfabēta simbolus (piemēram, visus $256$ baitus). Tāpēc garākā atrastā frāze vienmēr eksistē, un izvadē pietiek ar frāžu numuriem -- nākamo simbolu $x$ nesūta, tas kļūst par nākamās frāzes pirmo simbolu.
* **Šajā kursā** aplūkotais algoritms ($\textsf{LZ78-Encode}$, $\textsf{LZ78-Decode}$) ir tieši šāds: vārdnīcā sākumā ir visi burti (tos izvada kā burtus), bet garākas frāzes numurē ar $1, 2, 3, \ldots$ Atkodētājs vārdnīcu būvē ar viena soļa nobīdi, tāpēc var saņemt numuru, kas vēl nav vārdnīcā -- tad jaunā frāze ir iepriekšējā frāze $w$ ar pievienotu tās pirmo burtu $w[1]$ (sk. 3.4. uzdevumu).
* **Praksē** LZW izmanto mainīga garuma kodus (UNIX `compress` sāk ar $9$ bitu kodiem un palielina tos līdz $16$ bitiem, GIF -- līdz $12$ bitiem) un notīra vārdnīcu, kad tā ir pilna (GIF formātā tam ir īpašs *Clear* kods). LZW patenti (sk. "Vēsture") mudināja GIF vietā izveidot PNG formātu, kas lieto LZ77 (DEFLATE).

## Matemātiskais pamatojums un sarežģītība

### Markova ķēdes

Entropijas kodu ievadei bija teorētisks modelis - neatkarīgi vienādi sadalīti gadījuma lielumi. Ir vienkāršs matemātisks modelis -- Markova ķēde (*Markov chain*), kurā ziņojumu (burtu vai vārdu) virknīte ir nejauša, tomēr ziņojumu varbūtības ir atkarīgas no konteksta -- tie vairs nav savstarpēji neatkarīgi. Markova procesos

**Definīcija:** Par *Markova ķēdi* (*Markov chain*) diskrētā laikā ar galīgu stāvokļu alfabētu sauc varbūtisku procesu, kurš pārvietojas galīgā stāvokļu/ziņojumu kopā $S = \lbrace x_1, x_2, \ldots, x_n \rbrace$ un uzvedas sekojoši:

* Pašā sākumā tas nostājas vienā no stāvokļiem atbilstoši noteiktam sākuma sadalījumam; tā ir pirmā Markova ķēdes izvade.
* Katrā laika solī Markova ķēdes izvade ir šobrīd sasniegtais stāvoklis.
* Pāreja no viena stāvokļa uz citu ir izsakāma ar varbūtību (no dotā stāvokļa visu izejošo varbūtību summa ir $1$). Šo varbūtību nosaka tikai pašreizējais stāvoklis.

Markova ķēdē stāvokļi nav neatkarīgi un var nebūt identiski sadalīti (*independent and identically distributed*). Markova ķēdei nav atmiņas -- visa uzkrātā informācija ir ietverta tekošajā stāvoklī.

**Piemērs:** Šāds orientēts grafs ar $3$ stāvokļiem apraksta Markova ķēdi:

![Markova ķēde](figs/markov-chain.png)

$18$ burtu virknīte iegūta nejauši staigājot pa šo grafu, sākot ar $A$: `ABCABCBCAAABCABBAB`.

### Vidējā entropija, stacionāri un ergodiski procesi

**Definīcija:** Aplūkojam $X_1 X_2 X_3\ldots$ - ziņojumu virkni, kas ģenerēta ar varbūtisku procesu (neatkarīgi gadījumlielumi, Markova ķēde, slēpta Markova ķēde, neironu tīkls u.c.). Par par šīs virknes *vidējo entropiju* (*entropy rate*) sauc robežu:

$$
H(X) = \lim_{n \to \infty} \frac{1}{n} H\left( X_1, X_2, \ldots X_n \right).
$$

Šajā formulā $H\left( X_1, X_2, \ldots X_n \right)$ apzīmē entropiju saliktam ziņojumam, kurā $X_1,X_2,\ldots,X_n$ seko pēc kārtas.

Otrs veids ir rēķināt entropiju, izejot no izrēķināta no nosacītajām varbūtībām (t.i. pieņemam, ka pirmos $n-1$ stāvokļus jau esam redzējuši, atrodam kārtējā $n$-tā simbola nosacīto varbūtību sadalījumu un tā entropiju):

$$
H'(X) = \lim_{n \to \infty} H\left( X_n \,\mid\, X_{n-1}, X_{n-2}, \ldots X_1 \right).
$$

Visās mūsu kursa situācijās abi vidējās entropijas jēdzieni sakrīt $H(X) = H'(X)$.

Varbūtiski procesi var apmierināt šādas īpašības:

**Ergodiski procesi:** Ziņojumu ģenerēšanas process ir ergodisks, ja darbinot vairākus identiskus procesus, iegūstam tādu pašu varbūtisko sadalījumu kā darbinot to pašu procesu ilgu laiku (*ensemble average* sakrīt ar *time average*).

**Piemēri:** Markova ķēdes, ja no katra stāvokļa var nonākt katrā citā, ir ergodiskas; rodas stabils stāvokļu maiņas paraugs. Bet ir Iespējamas jocīgas Markova ķēdes, kurās process var aiziet pa vienu vai otru zaru un veidot divus pilnīgi dažādus sadalījumus.

**Stacionāri procesi:** Process ir *stacionārs*, ja tā vidējā vērtība, dispersija un citas statistiskās īpašības nemainās, pabīdot novērojumu par laiku $T$ uz priekšu. Piemēram, $E(X_i) = E(X_{i + T})$. Var gadīties, ka varbūtisks process sākumā ģenerē ziņojumus atbilstoši kādam citam sadalījumam, bet kļūst *asimptotiski stacionārs*.

**Piemēri:** Markova ķēdes var veidot periodiskas virknes. Periodiskas virknes (ar periodu $T>1$) nevar būt stacionāras -- visi varbūtību sadalījumi atkarīgi no tā, kurā perioda fāzē mēs esam.

### Saspiešanas asimptotiskā optimalitāte

**Teorēma:** Ja $X$ ir bināru ziņojumu avots (alfabēts ir $\lbrace 0,1 \rbrace$), kas ir stacionārs un ergodisks, tad

$$
\limsup_n \frac{1}{n} \ell_{\text{LZW}}(X_{1:n}) \leq H(X).
$$

Šī nevienādība izpildās ar varbūtību $1$. Šeit $H(X)$ apzīmē ziņojumu avota vidējo entropiju. Un $\ell_{\text{LZW}}(X_{1:n})$ ir garums, kas rodas, saspiežot pirmos $n$ bitus no ziņojumu avota.

Līdzīga teorēma ir spēkā arī LZ77 saspiešanai. Praksē to ne vienmēr var izmantot, jo LZW vārdnīcas un LZ77 atpakaļskata loga izmērs nav neierobežots.

> **TODO:** Piemērs, kurā Markova ķēdes vidējā entropija $H(X)$ ir mazāka nekā viena simbola entropija $H(X_1)$ -- t.i. Hafmana kods katram simbolam atsevišķi nevar sasniegt $H(X)$, bet LZ algoritmi asimptotiski to sasniedz.

### Sarežģītība; LZ77 un LZW salīdzinājums

* LZ77 bieži panāk labāku saspiešanas attiecību nekā LZW (sākotnējo baitu skaita attiecība pret saspiestajiem baitiem). 
* LZW ātrdarbība mēdz būt labāka, jo ar vārdnīcu (heštabulu) var strādāt efektīvāk nekā pārskatīt visu tekstu.
* LZ77 ļauj kontrolēt izmantoto atmiņu - ierobežojot bufera izmēru. LZW algoritmam var vajadzēt daudz atmiņas, ja saspiežamie bloki ir gari.

> **TODO:** LZ77 laika sarežģītība ar naivu prefiksu meklēšanu logā un ar heštabulām; LZ78/LZW vārdnīcas (*trie*) izmērs un laika sarežģītība; atspiešanas ātrums salīdzinājumā ar saspiešanu.

## Papildu tēmas

### Arhīvi un DLP produkti

DLP (Data Leak Prevention) rīki var novērst konfidenciālu datu nekontrolētu noplūdi uzņēmumā, piemēram, ja darbinieks pārsūta jūtīgus failus vai teksta fragmentus nepiemērotam adresātam.

* Datu *klasifikatori* (*classifiers*) nosaka konfidenciālu datu tipus. Adreses, telefonu numuri, epasti, personas kodi, IBAN kontu numuri, kredītkaršu numuri tiek aizsargāti pateicoties īpašam formātam, atbilstībai regulārai izteiksmei (vai kredītkaršu numuru gadījumā - *Luhn check* kontrolsummai). Lai samazinātu viltus pozitīvos rezultātus, var arī apstaigāt lokālas datubāzes, izveidot no tām klasifikatorus (piemēram, aizsargāt tikai pazīstamu klientu kredītkartes). Datu klasifikatori var būt arī burtiski citēti gabali no aizsargātiem dokumentiem vai iegūstami ar mašīnmācīšanos.
* Datu *kanāli* (*channels*) ir novērojamas datu plūsmas. Piemēram, HTTP augšupielādes, izejošie epasti, "clipboard" jeb kopēšanas darbības, ekrānuzņēmumi.
* Aizsardzības politikas (*policies*) nosaka, ko pa kuru kanālu kuriem adresātiem drīkst vai nedrīkst sūtīt. Politikai (bez kanāla un klasifikatora) ir arī darbība -- piemēram "Monitor" un "Block" (neļauj sūtīt).

Daži populāri DLP produkti:

* [Symantec DLP risinājumi](https://www.symantec.com/products/dlp)
* [Forcepoint DLP risinājumi](https://www.forcepoint.com/product/dlp-data-loss-prevention)
* [Digital Guardian DLP aģents](https://digitalguardian.com/products/endpoint-dlp)

Arhīvu atspiešana, saspiešana (reizēm arī TLS atšifrēšana/aizšifrēšana) ir laikietilpīga. DLP notiek kanālos, kuri ir jūtīgi pret novēlošanos (Web, Email); ir failu izmēru limiti.

* Kas notiek, ja atarhivējot failu, rodas ļoti daudz failu?
* Kas notiek, ja atarhivējot failu, rodas ļoti garš fails?
* Vai saspiešanas algoritms ļauj sākt arhivēt un sūtīt prom datus pirms saņemts viss nosūtāmais fails vai faili? Starpniekserveris (*proxy server*) nevar analizēt lietotāju Web transakcijas ilgāk kā aptuveni 10 sekundes, jo pārlūkprogrammu lietotāji nav pieraduši ilgi gaidīt.
* Kas notiek, ja datus sāk sūtīt adresātam un pēkšņi pamana privātu datu noplūdi? Vai uzbrucējs arhīvu var saprast arī tad, ja saņemta daļa no tā?

Iespējamie risinājumi:

* DLP analīzi censties biežāk veikt lokāli uz lietotāja datora (*endpoint* jeb *agent* programmatūra, kas var veltīt vairāk CPU resursu konkrētā lietotāja failu analīzei).
* Konfigurēt DLP produktus novērošanas (*monitoring*) režīmā - tad ir vairāk laika analīzei, jo transakcijas var uzreiz atļaut neatkarīgi no to satura.
* Dažus grūti analizējamus failus (dīvaini saspiestus, ar parolēm aizsargātus biroja programmu dokumentus, šifrētus datus) var nelaist cauri vārtejām, piespiest lietotājus sūtīt DLP rīkam saprotami vai šifrēt tikai uz organizācijas drošības perimetra.

## Uzdevumi

**3.1. uzdevums:** Aizkodēt virkni `abcabcabcdabc` ar $\textsf{LZ77-Encode}$, ja loga garums $W = 6$, bet priekšskata buferis nav ierobežots. Pēc tam pierakstīt to pašu virkni *gzip* formātā (sk. "Uzlabojumi gzip implementācijā"), kurā atsevišķu burtu $x$ izvada kā $(1, x)$, bet sakritību, kuras garums ir vismaz $3$, izvada kā $(0, d, \ell)$.

**Atbilde:** Numurējam ievades pozīcijas no $1$ līdz $13$:

| Kursors $i$ | Logs | Garākā sakritība | Izvade |
| --- | --- | --- | --- |
| 1 | -- | nav | $(0, 0, \mathtt{a})$ |
| 2 | `a` | nav | $(0, 0, \mathtt{b})$ |
| 3 | `ab` | nav | $(0, 0, \mathtt{c})$ |
| 4 | `abc` | `abcabc` no 1.pozīcijas: $d = 3$, $\ell = 6$ | $(3, 6, \mathtt{d})$ |
| 11 | `bcabcd` | `ab` no 7.pozīcijas: $d = 4$, $\ell = 2$ | $(4, 2, \mathtt{c})$ |

Pie $i = 4$ sakritība sākas logā, bet turpinās priekšskata buferī: pozīcijas $4 \ldots 9$ tiek kopētas no pozīcijām $1 \ldots 6$. Pie $i = 11$ atlikušie burti `abc` sakrīt ar pozīcijām $7 \ldots 9$, tomēr $\ell = 3$ nav atļauts, jo aiz sakritības jāpaliek simbolam $x$.

Rezultāts: $(0,0,\mathtt{a}), (0,0,\mathtt{b}), (0,0,\mathtt{c}), (3,6,\mathtt{d}), (4,2,\mathtt{c})$.

*gzip* formātā simbols aiz sakritības nav jāizvada, tāpēc pie $i = 11$ var izmantot visu sakritību `abc`: `(1,a),(1,b),(1,c),(0,3,6),(1,d),(0,4,3)`. $\square$

**3.2. uzdevums:** Izmantot LZ78, lai atkodētu virknīti: `A.B.C.1.3.2.D.4.1.A`

**Atbilde:** Atkodētājs būvē to pašu vārdnīcu kā kodētājs. Katram nolasītajam kodam atrod frāzi (burtu vai vārdnīcas frāzi ar šo numuru), izvada to un -- sākot ar otro kodu -- pievieno vārdnīcai iepriekšējo frāzi $w$, kurai galā pierakstīts tekošās frāzes pirmais burts.

| Kods | Frāze | Pievieno vārdnīcai |
| --- | --- | --- |
| A | A | -- |
| B | B | 1: AB |
| C | C | 2: BC |
| 1 | AB | 3: CA |
| 3 | CA | 4: ABC |
| 2 | BC | 5: CAB |
| D | D | 6: BCD |
| 4 | ABC | 7: DA |
| 1 | AB | 8: ABCA |
| A | A | 9: ABA |

Atkodētās frāzes ir `A.B.C.AB.CA.BC.D.ABC.AB.A`, tātad virkne ir `ABCABCABCDABCABA`. Tā ir tā pati virkne, kuru kodējām LZ78 piemērā, un arī vārdnīca sakrīt. $\square$

**3.3. uzdevums:** Izmantot LZ78, lai atkodētu virknīti: `a,a,b,1,2,4,2`

**Atbilde:**

| Kods | Frāze | Pievieno vārdnīcai |
| --- | --- | --- |
| a | a | -- |
| a | a | 1: aa |
| b | b | 2: ab |
| 1 | aa | 3: ba |
| 2 | ab | 4: aaa |
| 4 | aaa | 5: aba |
| 2 | ab | 6: aaaa |

Atkodētās frāzes ir `a.a.b.aa.ab.aaa.ab`, tātad virkne ir `aabaaabaaaab`. $\square$

**3.4. uzdevums:** Izmantot LZ78, lai atkodētu virknīti: `a,b,a,3,4`

**Atbilde:**

| Kods | Frāze | Pievieno vārdnīcai |
| --- | --- | --- |
| a | a | -- |
| b | b | 1: ab |
| a | a | 2: ba |
| 3 | aa | 3: aa |
| 4 | aaa | 4: aaa |

Nolasot kodu $3$, vārdnīcā ir tikai frāzes $1$ un $2$ -- frāzi $3$ kodētājs jau izveidoja, bet atkodētājs to vēl nezina. Jaunā frāze sākas ar iepriekšējo frāzi $w$ un beidzas ar savu pirmo burtu, kas sakrīt ar $w[1]$. Tātad frāze ir $w\,w[1] = \mathtt{a}\,\mathtt{a} = \mathtt{aa}$ ($\textsf{LZ78-Decode}$ 9.rindiņa). Tāpat kodam $4$: $w = \mathtt{aa}$, tātad frāze ir $\mathtt{aa}\,\mathtt{a} = \mathtt{aaa}$. Atkodētās frāzes ir `a.b.a.aa.aaa`, tātad virkne ir `abaaaaaa`. $\square$

## Izmantotā literatūra

* [LZW algoritma piemērs](http://web.mit.edu/6.02/www/f2010/handouts/recitations/Recitation21VergheseFall2010.pdf).
* Praktiski LZW algoritma apsvērumi: [What if dictionary is full](https://stackoverflow.com/questions/40054218/what-if-dictionary-size-in-lzw-algorithm-is-full).
* [LZ78 sliktākā gadījuma teorija](http://www-math.mit.edu/~shor/PAM/lempel_ziv_notes.pdf).
* [PPM algoritms](https://en.wikipedia.org/wiki/Prediction_by_partial_matching).
* [https://stackabuse.com/python-zlib-library-tutorial/](https://stackabuse.com/python-zlib-library-tutorial/)
* [Python zlib tutorial](https://stackabuse.com/python-zlib-library-tutorial/)
* IBM patenti algoritmiem LZ78 un LZW iesniegti 1981 un 1983.g. (sk. [LZW Patents](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch#Patents))
* [https://linuxhint.com/install-7zip-compression-tool-on-ubuntu/](https://linuxhint.com/install-7zip-compression-tool-on-ubuntu/).
* [Kalgari korpuss](http://corpus.canterbury.ac.nz/descriptions/#calgary) - dažādi failu tipi (ieskaitot melnbaltus attēlus, faksus, veclaicīgu mašīnkodu); [dažu algoritmu salīdzinājums](https://en.wikipedia.org/wiki/Calgary_corpus#Benchmarks). Kalgari korpusu arvien lieto metožu salīdzināšanai un pat saspiešanas sacensībām.
* [Kenterberijas korpuss](http://corpus.canterbury.ac.nz/) - mūsdienīgāks korpuss.
