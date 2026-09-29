---
layout: default
title: "Bezzudumu saspiešana: Beigu uzdevumu atrisinājumi"
lang: lv
permalink: /lectures/lossless_final_problemsets/solutions/lv/

docx_header: "Bezzudumu saspiešana. Beigu uzdevumi -- atrisinājumi"
docx_footer: "2026. gada rudens specseminārs: Algoritmi telekomunikācijās un drošības risinājumos"
docx_font: "Calibri"
docx_fontsize: 10
docx_heading_font: "Calibri Light"
docx_heading_color: "2F5496"
docx_heading1_size: 14
geometry: "a4paper, top=2.54cm, bottom=2.54cm, left=2.54cm, right=2.54cm"
---
# Bezzudumu saspiešana: Beigu uzdevumu atrisinājumi

Uzdevumu krājuma [Bezzudumu saspiešana: Beigu uzdevumi]({{ '/lectures/lossless_final_problemsets/' | relative_url }}) atrisinājumi.
Katru algoritmu izpildām soli pa solim ar tiem pašiem apzīmējumiem kā attiecīgajā nodaļā:
$\textsf{Huffman}$, aritmētiskā koda intervāli $[l_i;\,l_i+s_i)$, $\textsf{Rans-Encode}$ /
$\textsf{Rans-Decode}$, $\textsf{LZ77-Encode}$ / $\textsf{LZ77-Decode}$, $\textsf{LZ78-Encode}$ /
$\textsf{LZ78-Decode}$, $\textsf{MoveToFrontEncode}$ un $\textsf{efficientBWT}$.

**Noderīgas vērtības:** $\log_2 3 \approx 1.585$, $\;\log_2 5 \approx 2.322$, $\;\log_2 11 \approx 3.459$.

## Entropija un Hafmana kods

### 1. uzdevums (Viltotā monēta)

Sanumurēsim monētas ar $1,2,3,4$. Visus $8$ vienādi varbūtīgos gadījumus pierakstām kā $1^-, 1^+, 2^-, 2^+, \ldots$,
kur $c^-$ nozīmē "monēta $c$ ir vieglāka", bet $c^+$ -- "monēta $c$ ir smagāka".

**(a)** Visu $8$ gadījumu varbūtība ir $1/8$, tāpēc katra gadījuma informācijas saturs ir
$h = \log_2 8 = 3$ biti un

$$
H(S) = -\sum_{i=1}^{8} \frac{1}{8}\log_2 \frac{1}{8} = \log_2 8 = 3 \text{ biti}.
$$

**(b)** Svēršana ir gadījumlielums ar trim iznākumiem: $\text{L}$ (smagāks kreisais kauss),
$\text{Eq}$ (līdzsvars), $\text{R}$ (smagāks labais kauss).

*(1) Viena pret vienu,* piemēram, $1$ pret $2$. Monētas $3,4$ nav uz svariem, tāpēc visi $4$ gadījumi, kas
attiecas uz tām, dod $\text{Eq}$:

| Iznākums | Gadījumi | $p$ |
| --- | --- | --- |
| $\text{L}$ | $1^+, 2^-$ | $2/8 = 1/4$ |
| $\text{Eq}$ | $3^-, 3^+, 4^-, 4^+$ | $4/8 = 1/2$ |
| $\text{R}$ | $1^-, 2^+$ | $2/8 = 1/4$ |

$$
H = \tfrac14 \cdot 2 + \tfrac12 \cdot 1 + \tfrac14 \cdot 2 = 1.5 \text{ biti}.
$$

*(2) Divas pret divām,* $\lbrace 1,2 \rbrace$ pret $\lbrace 3,4 \rbrace$. Visas monētas ir uz svariem, tāpēc
līdzsvars nav iespējams:

| Iznākums | Gadījumi | $p$ |
| --- | --- | --- |
| $\text{L}$ | $1^+, 2^+, 3^-, 4^-$ | $4/8 = 1/2$ |
| $\text{Eq}$ | nav | $0$ |
| $\text{R}$ | $1^-, 2^-, 3^+, 4^+$ | $4/8 = 1/2$ |

$$
H = \tfrac12 \cdot 1 + \tfrac12 \cdot 1 = 1 \text{ bits}.
$$

Svēršana $1$ pret $1$ dod vairāk informācijas ($1.5 > 1$ biti). Tāpat kā Hafmana nodaļas 1.7. uzdevumā:
ja kaut kas ir *jānoskaidro*, tad atbildes entropijai jābūt pēc iespējas lielākai.

**(c)** Svēršanai ir $3$ iznākumi, tāpēc tās entropija nepārsniedz $\log_2 3 \approx 1.585$ bitus, un
vienādība ir tikai tad, ja $p(\text{L}) = p(\text{Eq}) = p(\text{R}) = 1/3$. Ar $4$ monētām pat šo robežu
nevar sasniegt: $8/3$ nav vesels skaitlis, tāpēc iznākumus nevar padarīt vienādi varbūtīgus, un labākā
sasniedzamā vērtība ir (b) punkta $1.5$ biti.

Tātad viena svēršana dod ne vairāk kā $1.585 < 3$ bitus, bet atbildei vajag $3$ bitus. Ar vienu
svēršanu gadījumu noskaidrot nevar. (Tas pats, skaitot gadījumus: $3 < 8$.)

**(d)** *Ar divām svēršanām nepietiek.* Gadījumu skaitīšana vien to neaizliedz, jo
$2\log_2 3 \approx 3.17 > 3$ un $3^2 = 9 \geq 8$. Bet apskatīsim pirmo svēršanu -- pēc (b) punkta
iespējamas tikai divas svēršanas:

* $1$ pret $1$: zaros paliek $2$, $4$, $2$ gadījumi;
* $2$ pret $2$: zaros paliek $4$, $0$, $4$ gadījumi.

Abos variantos kādā zarā paliek $4$ gadījumi, bet otrajai svēršanai ir tikai $3$ iznākumi. Pēc
Dirihlē principa diviem no šiem $4$ gadījumiem būs vienāds iznākums, un tos nevarēs atšķirt.
(Ar entropiju: atlikušo $4$ gadījumu nosacītā entropija ir $2$ biti, bet viena svēršana dod ne vairāk kā
$\log_2 3 \approx 1.585 < 2$ bitus.)

*Stratēģija ar trim svēršanām.*

**1. svēršana:** $1$ pret $2$.

* **$1$ smagāka par $2$** (gadījumi $1^+, 2^-$). **2. svēršana:** $1$ pret $3$ (zināms, ka monēta $3$ ir
  īsta). Ja $1$ ir smagāka -- atbilde ir $1^+$; ja līdzsvars -- atbilde ir $2^-$.
  (Šajā zarā pietiek ar divām svēršanām.)
* **$2$ smagāka par $1$** (gadījumi $1^-, 2^+$). Simetriski.
* **Līdzsvars** (gadījumi $3^-, 3^+, 4^-, 4^+$). **2. svēršana:** $3$ pret $4$; līdzsvars nav iespējams.
  * Ja $3$ ir smagāka, tad gadījums ir $3^+$ vai $4^-$. **3. svēršana:** $1$ pret $3$. Ja $3$ ir smagāka --
    $3^+$; ja līdzsvars -- $4^-$.
  * Ja $4$ ir smagāka, tad gadījums ir $4^+$ vai $3^-$, un **3. svēršana** ($1$ pret $4$) to izšķir
    tāpat. $\square$

### 2. uzdevums (Cik bitu zaudē Hafmana kods)

$p = (0.4,\; 0.2,\; 0.2,\; 0.1,\; 0.1)$; ziņojumus apzīmējam ar $x_1, \ldots, x_5$.

**(a)** Informācijas saturi $h(x_i) = \log_2 \frac{1}{p_i}$:

| $x_i$ | $p_i$ | $h(x_i) = \log_2 (1/p_i)$ | $p_i h(x_i)$ |
| --- | --- | --- | --- |
| $x_1$ | $0.4$ | $\log_2 2.5 = \log_2 5 - 1 \approx 1.322$ | $0.5288$ |
| $x_2$ | $0.2$ | $\log_2 5 \approx 2.322$ | $0.4644$ |
| $x_3$ | $0.2$ | $\log_2 5 \approx 2.322$ | $0.4644$ |
| $x_4$ | $0.1$ | $\log_2 10 = 1 + \log_2 5 \approx 3.322$ | $0.3322$ |
| $x_5$ | $0.1$ | $\log_2 10 \approx 3.322$ | $0.3322$ |

$$
H(S) = 0.5288 + 0.4644 + 0.4644 + 0.3322 + 0.3322 \approx 2.122 \text{ biti}.
$$

**(b)** Noapaļojam informācijas saturus uz augšu:

$$
\ell = \left( \lceil 1.322 \rceil, \lceil 2.322 \rceil, \lceil 2.322 \rceil,
\lceil 3.322 \rceil, \lceil 3.322 \rceil \right) = (2,\,3,\,3,\,4,\,4).
$$

Krafta-Makmilana nevienādība:

$$
\sum_i 2^{-\ell_i} = \frac14 + \frac18 + \frac18 + \frac{1}{16} + \frac{1}{16} = \frac{5}{8} = 0.625 \leq 1 .
$$

Tā kā summa nepārsniedz $1$, pēc Krafta-Makmilana teorēmas pretējā virziena eksistē prefiksu koks ar
tieši šādiem lapu dziļumiem. Piešķiram kodus kanoniski (vispirms īsākos, tad pēc kārtas):

$$
C' = \lbrace (x_1,\mathtt{00}),\; (x_2,\mathtt{010}),\; (x_3,\mathtt{011}),\;
(x_4,\mathtt{1000}),\; (x_5,\mathtt{1001}) \rbrace .
$$

$$
\ell_a(C') = 0.4 \cdot 2 + 0.2 \cdot 3 + 0.2 \cdot 3 + 0.1 \cdot 4 + 0.1 \cdot 4 = 2.8 \text{ biti}.
$$

Kods noteikti nav optimāls, jo Krafta summa ir **stingri** mazāka par $1$: prefiksu kokā ir neizmantota
vieta. Konkrēti, viss apakškoks $\mathtt{11}$ ir tukšs, tāpēc $x_4$ un $x_5$ var saīsināt līdz
$\mathtt{100}$ un $\mathtt{101}$, nepārkāpjot prefiksu īpašību -- un tas jau dod $2.6$ bitus.

**(c)** *Krafta summa.* Tā kā $\ell_i = \lceil \log_2 (1/p_i) \rceil \geq \log_2 (1/p_i)$, iegūstam
$2^{-\ell_i} \leq 2^{-\log_2 (1/p_i)} = p_i$ un tātad

$$
\sum_i 2^{-\ell_i} \leq \sum_i p_i = 1 .
$$

*Vidējais garums.* Tā kā $\lceil t \rceil < t + 1$,

$$
\sum_i p_i \ell_i = \sum_i p_i \left\lceil \log_2 \frac{1}{p_i} \right\rceil <
\sum_i p_i \left( \log_2 \frac{1}{p_i} + 1 \right) =
\sum_i p_i \log_2 \frac{1}{p_i} + \sum_i p_i = H(S) + 1 . \;\; \blacksquare
$$

(Tieši tā Hafmana nodaļā pierāda teorēmu $\ell_a(C) \leq H(S) + 1$; šeit nevienādība ir stingra, jo ne
visas $p_i$ ir precīzas divnieka pakāpes.)

**(d)** $\textsf{Huffman}(S)$ ar prioritāšu rindu $Q$:

| Solis | $Q$ pirms soļa | Divreiz $\textsf{ExtractMin}$ | Jaunā virsotne $z.\mathit{freq}$ |
| --- | --- | --- | --- |
| 1 | $0.1_{x_4},\,0.1_{x_5},\,0.2_{x_2},\,0.2_{x_3},\,0.4_{x_1}$ | $x_4$, $x_5$ | $u = 0.2$ |
| 2 | $0.2_{x_2},\,0.2_{x_3},\,0.2_{u},\,0.4_{x_1}$ | $x_2$, $x_3$ | $v = 0.4$ |
| 3 | $0.2_{u},\,0.4_{x_1},\,0.4_{v}$ | $u$, $x_1$ | $t = 0.6$ |
| 4 | $0.4_{v},\,0.6_{t}$ | $v$, $t$ | sakne $= 1.0$ |

```text
sakne
├─0─ v ─0─ x2          x1 = 10     (2 biti)
│      └─1─ x3         x2 = 00     (2 biti)
└─1─ t ─0─ x1          x3 = 01     (2 biti)
       └─1─ u ─0─ x4   x4 = 110    (3 biti)
              └─1─ x5  x5 = 111    (3 biti)
```

$$
\ell_a(C^{\ast}) = 0.4 \cdot 2 + 0.2 \cdot 2 + 0.2 \cdot 2 + 0.1 \cdot 3 + 0.1 \cdot 3
= 2.2 \text{ biti}.
$$

*Kāpēc mazāk nekā $H(S)+1$ bits.* (c) punktā uzbūvēts **kāds** prefiksu kods $C'$, kuram
$\ell_a(C') < H(S) + 1$. Hafmana kods ir optimāls, tāpēc $\ell_a(C^{\ast}) \leq \ell_a(C') < H(S)+1$.
Šeit tiešām $2.122 \leq 2.2 < 3.122$.

*Vai koks ir viennozīmīgs?* Nē. 2. solī rindā ir trīs elementi ar svaru $0.2$, bet 3. solī -- divi elementi
ar svaru $0.4$, un vienādos svarus var izšķirt dažādi. Piemēram, ja $u$ apvieno ar $v$, nevis ar $x_1$,
tad kodavārdu garumi ir $(1,3,3,3,3)$ un

$$
0.4 \cdot 1 + 0.2 \cdot 3 + 0.2 \cdot 3 + 0.1 \cdot 3 + 0.1 \cdot 3 = 2.2 \text{ biti} ,
$$

tas pats vidējais garums. Abi koki ir optimāli; atšķiras pat *kodavārdu garumu multikopa*.

**(e)** Ja ir divi ziņojumi, jebkuram prefiksu kodam jālieto kodavārdi $\mathtt{0}$ un $\mathtt{1}$, tāpēc

$$
\ell_a(C) = 1 \text{ bits}, \qquad H(S) = -0.99\log_2 0.99 - 0.01 \log_2 0.01 \approx 0.0808 \text{ biti}.
$$

Zudums ir $\approx 0.92$ biti uz ziņojumu -- kods ir vairāk nekā $12$ reizes sliktāks par entropiju.
(Tas joprojām atbilst garantijai $\ell_a \leq H(S)+1$; vienkārši šī robeža ir ļoti vāja, ja $H(S)$ ir
mazs.)

Zudumu var samazināt, **grupējot simbolus**, kā Hafmana nodaļā. Pāriem
$T = \lbrace AA, AB, BA, BB \rbrace$ ar varbūtībām $(0.9801,\, 0.0099,\, 0.0099,\, 0.0001)$ Hafmana
kodavārdu garumi ir $(1,3,2,3)$ un

$$
\ell_a(C_2) = 0.9801 \cdot 1 + 0.0099 \cdot 3 + 0.0099 \cdot 2 + 0.0001 \cdot 3 = 1.0299
$$

biti uz **pāri**, t.i., $0.515$ biti uz ziņojumu. Garāki bloki šo vērtību tuvina $H(S)$, bet konverģence
ir lēna; īstais risinājums ir **aritmētiskais kods vai ANS**, kuriem uz simbolu nav jātērē vesels bitu
skaits. $\square$

## Aritmētiskais kods un ANS

### 3. uzdevums (Aritmētiskais kods)

$p(\mathtt{A}) = 0.5$, $p(\mathtt{B}) = 0.3$, $p(\mathtt{C}) = 0.2$, tāpēc kumulatīvās varbūtības ir

$$
f(\mathtt{A}) = 0, \qquad f(\mathtt{B}) = 0.5, \qquad f(\mathtt{C}) = 0.8 .
$$

**(a)** Lietojam $l_i = l_{i-1} + f(x_i) \cdot s_{i-1}$ un $s_i = s_{i-1} \cdot p(x_i)$, sākot ar
$l_0 = 0$, $s_0 = 1$:

| $i$ | $x_i$ | $l_i = l_{i-1} + f(x_i)s_{i-1}$ | $s_i = s_{i-1}p(x_i)$ | Intervāls $[l_i;\,l_i+s_i)$ |
| --- | --- | --- | --- | --- |
| 1 | `A` | $0 + 0 \cdot 1 = 0$ | $1 \cdot 0.5 = 0.5$ | $[0;\,0.5)$ |
| 2 | `C` | $0 + 0.8 \cdot 0.5 = 0.4$ | $0.5 \cdot 0.2 = 0.1$ | $[0.4;\,0.5)$ |
| 3 | `B` | $0.4 + 0.5 \cdot 0.1 = 0.45$ | $0.1 \cdot 0.3 = 0.03$ | $[0.45;\,0.48)$ |
| 4 | `A` | $0.45 + 0 \cdot 0.03 = 0.45$ | $0.03 \cdot 0.5 = 0.015$ | $[0.45;\,0.465)$ |

$$
[0;1] \supset [0;\,0.5) \supset [0.4;\,0.5) \supset [0.45;\,0.48) \supset [0.45;\,0.465).
$$

**(b)** Vajag $[\beta;\, \beta+2^{-n}) \subseteq [0.45;\, 0.465)$, t.i., diādisku intervālu ar garumu
$2^{-n}$ intervālā, kura garums ir $s_4 = 0.015$. Vispirms no $2^{-n} \leq 0.015$ seko

$$
n \geq \log_2 \frac{1}{0.015} \approx 6.06, \qquad\text{tātad}\qquad n \geq 7 .
$$

($n = 6$ nav iespējams jau tāpēc, ka $2^{-6} = 0.015625 > 0.015$.) Ja $n = 7$, meklējam veselu skaitli
$k$, kuram $k/128 \geq 0.45$ un $(k+1)/128 \leq 0.465$:

$$
k \geq 0.45 \cdot 128 = 57.6 \;\Rightarrow\; k \geq 58, \qquad
k + 1 \leq 0.465 \cdot 128 = 59.52 \;\Rightarrow\; k \leq 58 .
$$

Tātad $k = 58 = 0111010_2$ un

$$
\beta = 0.0111010_2 = \frac{58}{128} = 0.453125, \qquad
\left[ \tfrac{58}{128};\, \tfrac{59}{128} \right) = [0.453125;\, 0.4609375) \subset [0.45;\, 0.465).
$$

Šeit $n = 7 = \left\lceil \log_2 \frac{1}{s_4} \right\rceil$ -- kods ir mazāk nekā par vienu bitu garāks
par ziņojuma informācijas saturu $6.06$ biti. Vispārīgā gadījumā var zaudēt līdz $2$ bitiem, jo
diādiskajam intervālam *pilnībā* jāietilpst intervālā $[l_4;\,l_4+s_4)$.

**(c)** $\textsf{Huffman}$ varbūtībām $(0.5, 0.3, 0.2)$ apvieno $0.3 + 0.2 = 0.5$ un pēc tam $0.5 + 0.5 = 1$:

$$
C^{\ast} = \lbrace (\mathtt{A},\mathtt{0}),\; (\mathtt{B},\mathtt{10}),\; (\mathtt{C},\mathtt{11}) \rbrace,
\qquad \mathtt{ACBA} \rightarrow \mathtt{0}\,\mathtt{11}\,\mathtt{10}\,\mathtt{0} = \mathtt{011100}
\;\; (6 \text{ biti}).
$$

Tātad šim īsajam ziņojumam Hafmana kods ir **labāks**: $6$ biti pret $7$.

Iemesls ir tas, *kur* abi algoritmi zaudē. Hafmana kods zaudē
$\ell_a(C^{\ast}) - H(S) = 1.5 - 1.4855 \approx 0.0145$ bitus **uz simbolu**, t.i., zudums aug lineāri ar
ziņojuma garumu. Aritmētiskais kods zaudē ne vairāk kā $1$--$2$ bitus **visam ziņojumam**, lai cik garš tas
būtu. $n$ simboliem:

$$
\text{Hafmana kods} \approx nH(S) + 0.0145 n, \qquad \text{aritmētiskais kods} \approx nH(S) + 2 .
$$

Konstante $2$ dominē, kamēr $n$ ir mazs (šeit $n = 4$), un aritmētiskais kods kļūst izdevīgāks, kad
$0.0145 n > 2$, t.i., sākot no aptuveni $n \approx 140$ simboliem. Ļoti nevienmērīgiem sadalījumiem (kā
2.(e) uzdevumā, kur Hafmana kods zaudē $0.92$ bitus uz simbolu) aritmētiskais kods uzvar gandrīz uzreiz.

**(d)** $\beta = 0.101_2 = 0.625$. Katrā solī atrodam apakšintervālu, kurā ir $\beta$, un sašaurinām
intervālu -- tieši kā $\textsf{Arithmetic-Decode}$:

| $i$ | Intervāls $[l_{i-1};\,l_{i-1}+s_{i-1})$ | Apakšintervāli | Satur $0.625$ | $x_i$ |
| --- | --- | --- | --- | --- |
| 1 | $[0;\,1)$ | $\mathtt{A}\,[0;.5)$, $\mathtt{B}\,[.5;.8)$, $\mathtt{C}\,[.8;1)$ | $[0.5;\,0.8)$ | `B` |
| 2 | $[0.5;\,0.8)$ | $\mathtt{A}\,[.5;.65)$, $\mathtt{B}\,[.65;.74)$, $\mathtt{C}\,[.74;.8)$ | $[0.5;\,0.65)$ | `A` |
| 3 | $[0.5;\,0.65)$ | $\mathtt{A}\,[.5;.575)$, $\mathtt{B}\,[.575;.62)$, $\mathtt{C}\,[.62;.65)$ | $[0.62;\,0.65)$ | `C` |
| 4 | $[0.62;\,0.65)$ | $\mathtt{A}\,[.62;.635)$, $\mathtt{B}\,[.635;.644)$, $\mathtt{C}\,[.644;.65)$ | $[0.62;\,0.635)$ | `A` |

Pirmie četri burti ir `BACA`.

*Tas pats ar mērogošanu* (tā dara implementācijā -- intervāla sašaurināšanas vietā skaitli izstiepj
atpakaļ uz $[0;1)$):

$$
0.625 \xrightarrow{\;\mathtt{B}\;} \frac{0.625 - 0.5}{0.3} = 0.41\overline{6}
\xrightarrow{\;\mathtt{A}\;} \frac{0.41\overline{6}}{0.5} = 0.8\overline{3}
\xrightarrow{\;\mathtt{C}\;} \frac{0.8\overline{3} - 0.8}{0.2} = 0.1\overline{6}
\xrightarrow{\;\mathtt{A}\;} 0.\overline{3} . \;\; \square
$$

### 4. uzdevums (ANS)

$f(\mathtt{A}) = 3$, $f(\mathtt{N}) = 2$, $f(\mathtt{S}) = 1$, $M = 6$, $c(\mathtt{A}) = 0$,
$c(\mathtt{N}) = 3$, $c(\mathtt{S}) = 5$.

**(a)** Simbolam $s$ pieder tie stāvokļi $x$, kuru atlikums $r = x \bmod 6$ apmierina
$c(s) \leq r < c(s) + f(s)$:

| simbols | `A` | `N` | `S` |
| --- | --- | --- | --- |
| $f(s)$ | 3 | 2 | 1 |
| $c(s)$ | 0 | 3 | 5 |
| spraugas $r = x \bmod 6$ | $0,1,2$ | $3,4$ | $5$ |

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| īpašnieks | `A` | `A` | `A` | `N` | `N` | `S` | `A` | `A` | `A` | `N` | `N` | `S` | `A` | `A` | `A` | `N` | `N` | `S` |
| kārtas nr. | 0 | 1 | 2 | 0 | 1 | 0 | 3 | 4 | 5 | 2 | 3 | 1 | 6 | 7 | 8 | 4 | 5 | 2 |

Tātad `A` pieder $0,1,2,6,7,8,12,13,14,\ldots$ (apmēram $1/2$ no visiem skaitļiem), `N` pieder
$3,4,9,10,15,16,\ldots$ (apmēram $1/3$), bet `S` pieder $5,11,17,\ldots$ (apmēram $1/6$) -- tieši
proporcijās $f(s)/M$. Rinda "kārtas nr." ir spraugas numurs šī simbola paša skaitīšanas sistēmā; tieši šo
vērtību $x$ atgriež atkodētājs.

**(b)** $\textsf{Rans-Encode}$ apstrādā ziņojumu **no beigām**, tāpēc secība ir
`S`, `A`, `N`, `A`, `N`, `A`. Algoritma 4. rindiņa aprēķina
$x = M \lfloor x/f(s) \rfloor + (x \bmod f(s)) + c(s)$:

| solis | $s$ | $f(s)$ | $c(s)$ | $x$ pirms | $C(s,x)$ aprēķins | $x$ pēc |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `S` | 1 | 5 | 0 | $6 \cdot \lfloor 0/1 \rfloor + 0 + 5 = 0 + 5$ | **5** |
| 2 | `A` | 3 | 0 | 5 | $6 \cdot \lfloor 5/3 \rfloor + 2 + 0 = 6 + 2$ | **8** |
| 3 | `N` | 2 | 3 | 8 | $6 \cdot \lfloor 8/2 \rfloor + 0 + 3 = 24 + 3$ | **27** |
| 4 | `A` | 3 | 0 | 27 | $6 \cdot \lfloor 27/3 \rfloor + 0 + 0 = 54 + 0$ | **54** |
| 5 | `N` | 2 | 3 | 54 | $6 \cdot \lfloor 54/2 \rfloor + 0 + 3 = 162 + 3$ | **165** |
| 6 | `A` | 3 | 0 | 165 | $6 \cdot \lfloor 165/3 \rfloor + 0 + 0 = 330 + 0$ | **330** |

Viss ziņojums ir viens skaitlis

$$
x = 330 = 101001010_2 \qquad (9 \text{ biti}).
$$

**(c)** $\textsf{Rans-Decode}(330, f, c, 6)$; 2. rindiņa aprēķina $r = x \bmod 6$, 5. rindiņa --
$x = f(s)\lfloor x/6 \rfloor + r - c(s)$:

| solis | $x$ pirms | $r = x \bmod 6$ | $s = \textsf{Lookup}(r)$ | $x = f(s)\lfloor x/6\rfloor + r - c(s)$ | $x$ pēc |
| --- | --- | --- | --- | --- | --- |
| 1 | 330 | 0 | `A` | $3 \cdot 55 + 0 - 0$ | **165** |
| 2 | 165 | 3 | `N` | $2 \cdot 27 + 3 - 3$ | **54** |
| 3 | 54 | 0 | `A` | $3 \cdot 9 + 0 - 0$ | **27** |
| 4 | 27 | 3 | `N` | $2 \cdot 4 + 3 - 3$ | **8** |
| 5 | 8 | 2 | `A` | $3 \cdot 1 + 2 - 0$ | **5** |
| 6 | 5 | 5 | `S` | $1 \cdot 0 + 5 - 5$ | **0** |

Izvade ir `A`, `N`, `A`, `N`, `A`, `S` -- ziņojums `ANANAS` **pareizajā** secībā (LIFO: pēdējais
iekodētais simbols tiek atkodēts pirmais), un stāvoklis atgriežas $x = 0$, kas ir ANS dabiskais
apstāšanās nosacījums.

**(d)** Tas pats atkodētājs, sākot no $x = 131$:

| solis | $x$ pirms | $r = x \bmod 6$ | $s$ | $x = f(s)\lfloor x/6\rfloor + r - c(s)$ | $x$ pēc |
| --- | --- | --- | --- | --- | --- |
| 1 | 131 | 5 | `S` | $1 \cdot 21 + 5 - 5$ | **21** |
| 2 | 21 | 3 | `N` | $2 \cdot 3 + 3 - 3$ | **6** |
| 3 | 6 | 0 | `A` | $3 \cdot 1 + 0 - 0$ | **3** |
| 4 | 3 | 3 | `N` | $2 \cdot 0 + 3 - 3$ | **0** |

Četri simboli ir `SNAN`, un stāvoklis sasniedz $0$ tieši pēc tiem -- tātad $131$ ir pilna ziņojuma
`SNAN` $\textsf{Rans-Encode}$ izvade.

**(e)** Ja $p(\mathtt{A}) = 3/6$, $p(\mathtt{N}) = 2/6$, $p(\mathtt{S}) = 1/6$:

$$
-\log_2 \left( p(\mathtt{A})^3 p(\mathtt{N})^2 p(\mathtt{S}) \right) =
-\log_2 \left( \tfrac18 \cdot \tfrac19 \cdot \tfrac16 \right) = \log_2 432 = 4 + 3\log_2 3
\approx 8.755 \text{ biti},
$$

$$
\log_2 330 = 1 + \log_2 3 + \log_2 5 + \log_2 11 \approx 8.366 \text{ biti}.
$$

Stāvoklis ir nedaudz *mazāks* par informācijas saturu tikai tāpēc, ka kodētājs sāka no $x = 0$: pirmais
solis deva $C(\mathtt{S},0) = c(\mathtt{S}) = 5$, t.i., stāvoklis palielinājās līdz $5$, nevis līdz
apmēram $6$, bet $\log_2 x$ patieso izmaksu mēra tikai asimptotiski. Faktiski jānosūta skaitlis $330$
veselā bitu skaitā -- $9$ biti pret $8.755$ bitiem entropijas, tātad visam ziņojumam zūd apmēram $0.25$
biti. Tas saskan ar nodaļas piemēru `GACGU$`, kur iztērēja $15$ bitus pret $14.18$ bitiem entropijas.

**(f)** Abus ziņojumus kodē no beigām, sākot ar $x = 0$:

| `NA`: $s$ | $x$ pirms | $x$ pēc | | `NAA`: $s$ | $x$ pirms | $x$ pēc |
| --- | --- | --- | --- | --- | --- | --- |
| `A` | 0 | $6 \cdot 0 + 0 + 0 =$ **0** | | `A` | 0 | $6 \cdot 0 + 0 + 0 =$ **0** |
| `N` | 0 | $6 \cdot 0 + 0 + 3 =$ **3** | | `A` | 0 | $6 \cdot 0 + 0 + 0 =$ **0** |
| | | | | `N` | 0 | $6 \cdot 0 + 0 + 3 =$ **3** |

Abi dod $x = 3$.

*Kāpēc.* Vispārīgi $C(s, 0) = c(s)$, un šeit $c(\mathtt{A}) = 0$, tāpēc $C(\mathtt{A}, 0) = 0$: iekodējot
`A` tukšā stāvoklī, nekas nemainās. Tā ir tieši parastas pozicionālās skaitīšanas sistēmas **vadošo
nuļļu** problēma -- $\mathtt{007}$ un $\mathtt{7}$ ir viens un tas pats skaitlis. ANS simbols ar
$c(s) = 0$ (alfabētā pirmais) spēlē cipara $0$ lomu, un jebkurš skaits tā kopiju ziņojuma *beigās* --
kuras kodētājs apstrādā *vispirms* -- pazūd.

Ziņojumam `ANANAS` šīs problēmas nav, jo tas beidzas ar `S` un $c(\mathtt{S}) = 5 \neq 0$, tāpēc jau pats
pirmais solis stāvokli attālina no $0$. Praksē ir divi standarta risinājumi, abi minēti nodaļā: paturēt
beigu marķieri `$` (LIFO dēļ to iekodē pirmo, un $c(\$) \neq 0$) vai paziņot atkodētājam simbolu skaitu
$n$. Straumēšanas variants $\textsf{Rans-Encode-Stream}$ to atrisina strukturāli -- tas sāk no $x = L$, nevis
no $x = 0$. $\square$

## Lempela-Ziva algoritmi

### 5. uzdevums (LZ77)

Ievade ir `kakadukakadu`, $n = 12$; pozīcijas numurējam no $1$:

```text
 1 2 3 4 5 6 7 8 9 10 11 12
 k a k a d u k a k a  d  u
```

**(a)** $W = 6$, $L$ nav ierobežots. $\textsf{LZ77-Encode}$ 6. rindiņa tomēr ierobežo sakritību ar
$k < n - i$, lai trijniekam paliktu simbols $T[i+\ell]$.

| Kursors $i$ | Logs $T[\max(1,i-6) \ldots i-1]$ | Garākā sakritība | Izvade $(d,\ell,x)$ | Nākamais $i$ |
| --- | --- | --- | --- | --- |
| 1 | -- (tukšs) | nav | $(0,0,\mathtt{k})$ | 2 |
| 2 | `k` | nav (`k` $\neq$ `a`) | $(0,0,\mathtt{a})$ | 3 |
| 3 | `ka` | `ka` no 1. pozīcijas: $d = 2$, $\ell = 2$ | $(2,2,\mathtt{d})$ | 6 |
| 6 | `kakad` | nav (`u` nav logā) | $(0,0,\mathtt{u})$ | 7 |
| 7 | `kakadu` | `kakad` no 1. pozīcijas: $d = 6$, $\ell = 5$ | $(6,5,\mathtt{u})$ | 13 |

Divu interesantāko soļu detaļas:

* **$i = 3$:** meklēšana iet $s = 2, 1$. Ja $s = 2$, jau $T[2] = \mathtt{a} \neq \mathtt{k} = T[3]$.
  Ja $s = 1$: $T[1..2] = \mathtt{ka}$ sakrīt ar $T[3..4] = \mathtt{ka}$, un pēc tam
  $T[3] = \mathtt{k} \neq \mathtt{d} = T[5]$. Tātad $d = 3-1 = 2$, $\ell = 2$, un nākamais burts ir
  $T[5] = \mathtt{d}$.
* **$i = 7$:** ja $s = 3$, sakritība ir `ka` ($\ell = 2$), bet ja $s = 1$, tā turpinās
  $\mathtt{k}\mathtt{a}\mathtt{k}\mathtt{a}\mathtt{d}\mathtt{u}$ -- sešus burtus. Cikls apstājas pie
  $k = 5$, jo nosacījums ir $k < n - i = 12 - 7 = 5$; sestais burts $T[12] = \mathtt{u}$ kļūst par
  trijnieka simbolu $x$. Tātad $d = 7 - 1 = 6$ (lielākā nobīde, ko logs vēl sasniedz), $\ell = 5$.

Rezultāts: $(0,0,\mathtt{k}), (0,0,\mathtt{a}), (2,2,\mathtt{d}), (0,0,\mathtt{u}), (6,5,\mathtt{u})$ --
$12$ burti $5$ trijniekos.

**(b)** $W = 4$: logs ir $T[\max(1,i-4) \ldots i-1]$.

| Kursors $i$ | Logs | Garākā sakritība | Izvade $(d,\ell,x)$ | Nākamais $i$ |
| --- | --- | --- | --- | --- |
| 1 | -- | nav | $(0,0,\mathtt{k})$ | 2 |
| 2 | `k` | nav | $(0,0,\mathtt{a})$ | 3 |
| 3 | `ka` | `ka` no 1. pozīcijas: $d = 2$, $\ell = 2$ | $(2,2,\mathtt{d})$ | 6 |
| 6 | `akad` | nav | $(0,0,\mathtt{u})$ | 7 |
| 7 | `kadu` | `ka` no 3. pozīcijas: $d = 4$, $\ell = 2$ | $(4,2,\mathtt{k})$ | 10 |
| 10 | `ukak` | `a` no 8. pozīcijas: $d = 2$, $\ell = 1$ | $(2,1,\mathtt{d})$ | 12 |
| 12 | `akad` | nav | $(0,0,\mathtt{u})$ | 13 |

Rezultāts: $(0,0,\mathtt{k}), (0,0,\mathtt{a}), (2,2,\mathtt{d}), (0,0,\mathtt{u}), (4,2,\mathtt{k}), (2,1,\mathtt{d}), (0,0,\mathtt{u})$
-- $7$ trijnieki $5$ vietā.

*Kāpēc trijnieku ir vairāk.* Virkne ir divreiz uzrakstīts vārds `kakadu`, tāpēc ideālais sadalījums ir
"nokopēt $6$ burtus no attāluma $6$". Ja $W = 6$, nobīde $d = 6$ ir tieši pēdējā, ko logs sasniedz, un viens
trijnieks aptver visu atkārtojumu. Ja $W = 4$, nobīde $6$ nav sasniedzama: pie $i = 7$ kodētājs vairs
neredz pirmā `kakadu` sākumu, un atkārtojums jāsaliek no īsām tuvām sakritībām ($\ell = 2$, tad
$\ell = 1$), tērējot vienu trijnieku uz diviem vai trim burtiem. Tas ir vispārīgs kompromiss -- īss logs
ir lētāks (mazāk bitu nobīdei $d$, ātrāka meklēšana), bet tas nevar izmantot tālus atkārtojumus.

**(c)** $\textsf{LZ77-Decode}$ virknei
$(0,0,\mathtt{l}), (0,0,\mathtt{a}), (2,5,\mathtt{i}), (4,3,\mathtt{a})$. Atkodētājs glabā $m$ -- jau
izvadīto burtu skaitu -- un katram trijniekam kopē $\ell$ burtus **pa vienam** no $T[m+k-d]$, pēc tam
pievieno $x$:

| Trijnieks | $m$ pirms | Kopētie burti $T[m+k] = T[m+k-d]$ | $T$ pēc trijnieka | $m$ pēc |
| --- | --- | --- | --- | --- |
| $(0,0,\mathtt{l})$ | 0 | -- | `l` | 1 |
| $(0,0,\mathtt{a})$ | 1 | -- | `la` | 2 |
| $(2,5,\mathtt{i})$ | 2 | $T[3]{=}T[1]{=}\mathtt{l}$, $T[4]{=}T[2]{=}\mathtt{a}$, $T[5]{=}T[3]{=}\mathtt{l}$, $T[6]{=}T[4]{=}\mathtt{a}$, $T[7]{=}T[5]{=}\mathtt{l}$ | `lalalali` | 8 |
| $(4,3,\mathtt{a})$ | 8 | $T[9]{=}T[5]{=}\mathtt{l}$, $T[10]{=}T[6]{=}\mathtt{a}$, $T[11]{=}T[7]{=}\mathtt{l}$ | `lalalalilala` | 12 |

Atkodētā virkne ir `lalalalilala`.

**Pārklāšanās notiek trešajā trijniekā** $(2,5,\mathtt{i})$, kur $d = 2 < \ell = 5$: avota apgabals
$T[1..5]$ pārklājas ar rakstāmo apgabalu $T[3..7]$. Sākot ar $k = 3$, atkodētājs kopē burtus, kurus tas
izvadījis *šajā pašā solī* ($T[5]$ ieraksta pie $k = 3$ un nolasa pie $k = 5$). Tieši tāpēc
$\textsf{LZ77-Decode}$ 4. rindiņa kopē pa vienam simbolam, nevis pārvieto visu bloku uzreiz -- un tas ļauj
ar vienu trijnieku iekodēt patvaļīgi garu periodisku virkni. Ceturtajā trijniekā $d = 4 > \ell = 3$, tāpēc
pārklāšanās nav. $\square$

### 6. uzdevums (LZ78)

**(a)** $\textsf{LZ78-Encode}$ virknei `abababababa` ($n = 11$), $S = \lbrace \mathtt{a}, \mathtt{b} \rbrace$.
Sākumā $D[\mathtt{a}] = \mathtt{a}$, $D[\mathtt{b}] = \mathtt{b}$, $m = 0$, $w = T[1] = \mathtt{a}$.
Tabulā parādīti tikai tie soļi, kuros 6. rindiņas nosacījums neizpildās, t.i., izvada frāzi $w$ un pievieno
$wk$:

| Solis | $i$ | Garākā $w$ vārdnīcā $D$ | $k = T[i]$ | Izvade $D[w]$ | $m$ | Pievienots: $D[wk]$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | `a` | `b` | `a` | 1 | 1: `ab` |
| 2 | 3 | `b` | `a` | `b` | 2 | 2: `ba` |
| 3 | 5 | `ab` | `a` | 1 | 3 | 3: `aba` |
| 4 | 8 | `aba` | `b` | 3 | 4 | 4: `abab` |
| 5 | 10 | `ba` | `b` | 2 | 5 | 5: `bab` |
| 6 | -- | `ba` | -- | 2 (13. rindiņa) | -- | -- |

(Neparādītajos soļos $wk \in D$, un kodētājs tikai pagarina $w$; piemēram, pie $i = 4$ ir
$wk = \mathtt{ab} \in D$, tāpēc $w$ kļūst par `ab`.)

Vārdnīcai pievienotās frāzes: `1: ab`, `2: ba`, `3: aba`, `4: abab`, `5: bab`. Ievērojiet, ka frāzes $4$
un $5$ tiek izveidotas, bet nekad netiek izmantotas -- katra jaunā frāze ir veca frāze, pagarināta tieši
par vienu burtu, tāpēc frāzes aug tikai lēni.

Kodu virkne ir `a,b,1,3,2,2`, un sadalījums ir `a.b.ab.aba.ba.ba`.

**(b)** $\textsf{LZ78-Decode}(\mathtt{a},\mathtt{b},1,3,2,2)$. 12. rindiņa pievieno **iepriekšējo** frāzi $w$,
kurai pierakstīts **pašreizējās** frāzes $v$ pirmais burts:

| $j$ | $c_j$ | Ir vārdnīcā $D$? | Frāze $v$ | Izvade | $m$ | Pievienots: $D[m] = w\,v[1]$ | Jaunais $w$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `a` | jā (burts) | `a` | `a` | 0 | -- | `a` |
| 2 | `b` | jā (burts) | `b` | `b` | 1 | 1: `ab` | `b` |
| 3 | 1 | jā | `ab` | `ab` | 2 | 2: `ba` | `ab` |
| 4 | 3 | **nē** ($m = 2$) | $w\,w[1] = \mathtt{ab}\,\mathtt{a} = $ `aba` | `aba` | 3 | 3: `aba` | `aba` |
| 5 | 2 | jā | `ba` | `ba` | 4 | 4: `abab` | `ba` |
| 6 | 2 | jā | `ba` | `ba` | 5 | 5: `bab` | `ba` |

Atkodētās frāzes ir `a.b.ab.aba.ba.ba`, t.i., virkne `abababababa`, un vārdnīca ir tāda pati kā
kodētājam.

**Atkodētājs saņem nezināmu numuru solī $j = 4$**, kur $c_4 = 3$, bet vārdnīcā ir tikai frāzes $1$ un $2$.
Kodētājs frāzi $3$ bija izveidojis jau tad, kad to izvadīja; atkodētājs atpaliek par vienu soli,
jo 12. rindiņai vajag pašreizējās frāzes pirmo burtu. Tad der 8.--9. rindiņas īpašais gadījums: $c_j = m+1$,
tāpēc jaunā frāze sākas ar iepriekšējo frāzi $w$ un beidzas ar savu pirmo burtu, kas ir $w[1]$ -- tātad
$v = w\,w[1] = \mathtt{ab} + \mathtt{a} = \mathtt{aba}$.

**(c)** $\textsf{LZ78-Decode}(\mathtt{l},\mathtt{a},1,3,2,5)$, $S = \lbrace \mathtt{a}, \mathtt{l} \rbrace$:

| $j$ | $c_j$ | Ir vārdnīcā $D$? | Frāze $v$ | Izvade | $m$ | Pievienots: $D[m] = w\,v[1]$ | Jaunais $w$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `l` | jā (burts) | `l` | `l` | 0 | -- | `l` |
| 2 | `a` | jā (burts) | `a` | `a` | 1 | 1: `la` | `a` |
| 3 | 1 | jā | `la` | `la` | 2 | 2: `al` | `la` |
| 4 | 3 | **nē** ($m = 2$) | $w\,w[1] = \mathtt{la}\,\mathtt{l} = $ `lal` | `lal` | 3 | 3: `lal` | `lal` |
| 5 | 2 | jā | `al` | `al` | 4 | 4: `lala` | `al` |
| 6 | 5 | **nē** ($m = 4$) | $w\,w[1] = \mathtt{al}\,\mathtt{a} = $ `ala` | `ala` | 5 | 5: `ala` | `ala` |

Frāzes ir `l.a.la.lal.al.ala`, tātad virkne ir `lalalalalala` ($12$ burti). Šeit 8.--9. rindiņas īpašais
gadījums gadās **divreiz**, pie $j = 4$ un $j = 6$. (Iekodējot `lalalalalala` no jauna ar
$\textsf{LZ78-Encode}$, tiešām atkal iegūst `l,a,1,3,2,5`.)

**(d)** Alfabētā ir viens burts, tāpēc $D[\mathtt{a}] = \mathtt{a}$, un vārdnīca aug šādi:
`1: aa`, `2: aaa`, `3: aaaa`, ... Katra jaunā frāze ir iepriekšējā, pagarināta par vienu burtu, un katru
frāzi izmanto tikai vienreiz, tāpēc sadalījums ir

$$
\underbrace{\mathtt{a}}_{1} \mid \underbrace{\mathtt{aa}}_{2} \mid
\underbrace{\mathtt{aaa}}_{3} \mid \underbrace{\mathtt{aaaa}}_{4} \mid \ldots
$$

-- $r$-tais izvadītais kods aptver tieši $r$ burtus. Pēc $r$ kodiem kodētājs ir apstrādājis

$$
1 + 2 + \ldots + r = \frac{r(r+1)}{2}
$$

burtus. **Precīza atbilde:** ja $n = 1 + 2 + \ldots + r$, tad $\textsf{LZ78-Encode}$ izvada tieši
$r$ kodus, proti, `a, 1, 2, ..., r-1`. (Pārbaude: $n = 1 \rightarrow 1$ kods `a`; $n = 3 \rightarrow 2$
kodi `a,1`; $n = 6 \rightarrow 3$ kodi `a,1,2`; $n = 10 \rightarrow 4$; $n = 15 \rightarrow 5$.)

**Aptuvena atbilde:** atrisinot $r(r+1)/2 = n$, iegūstam

$$
r = \frac{\sqrt{8n+1} - 1}{2} \approx \sqrt{2n},
$$

un patvaļīgam $n$ kodu skaits ir $\left\lceil \frac{\sqrt{8n+1}-1}{2} \right\rceil$ -- pēdējā frāze
vienkārši ir nepilna. Tātad $n$ burti kļūst par apmēram $\sqrt{2n}$ kodiem: saspiešanas attiecība aug
neierobežoti. Tas ir asimptotiskās optimalitātes teorēmas galējais gadījums, jo šāda avota vidējā
entropija ir $0$. $\square$

## Berouza-Vīlera transformācija

### 7. uzdevums (BWT)

**(a)** Visas vārda `KAKAO$` cikliskās permutācijas un pēc tam tās pašas, sakārtotas ar
$\mathtt{\$} < \mathtt{A} < \mathtt{K} < \mathtt{O}$:

```text
K A K A O $              $ K A K A O
A K A O $ K              A K A O $ K
K A O $ K A    --->      A O $ K A K
A O $ K A K              K A K A O $     <- 4. rinda
O $ K A K A              K A O $ K A
$ K A K A O              O $ K A K A
```

(Kārtošanas detaļas: abām rindām, kas sākas ar `A`, otrie burti ir `K` un `O`, tāpēc `AKAO$K` ir pirmā;
abām rindām, kas sākas ar `K`, trešie burti ir `K` un `O`.)

Transformācija ir pēdējā kolonna:

$$
\text{BWT}(\mathtt{KAKAO\$}) = \mathtt{OKK\$AA} .
$$

Sākotnējais vārds `KAKAO$` ir sakārtotās matricas **4. rindā** (rindas numurējot no $1$).

**(b)** $\textsf{MoveToFrontEncode}$ virknei `OKK$AA` ar sākotnējo alfabētu `[$,A,K,O]` (pozīcijas
numurē no $0$). Parādīts alfabēts *pirms* soļa:

| Ievade | Izvade | Alfabēts pirms soļa |
| --- | --- | --- |
| **O**, K, K, `$`, A, A | 3 | `[$,A,K,O]` |
| O, **K**, K, `$`, A, A | 3,3 | `[O,$,A,K]` |
| O, K, **K**, `$`, A, A | 3,3,0 | `[K,O,$,A]` |
| O, K, K, **`$`**, A, A | 3,3,0,2 | `[K,O,$,A]` |
| O, K, K, `$`, **A**, A | 3,3,0,2,3 | `[$,K,O,A]` |
| O, K, K, `$`, A, **A** | 3,3,0,2,3,0 | `[A,$,K,O]` |
| -- | -- | `[A,$,K,O]` |

Kods ir `3,3,0,2,3,0`. Katrs BWT izveidotais atkārtotais pāris (`KK` un `AA`) pārvērtās par $0$ -- tieši
tāpēc pēc BWT lieto *Move-to-front*.

**(c)** Dots $L = \text{BWT}(w) = \mathtt{ASSAL\$}$; pirmā kolonna $F$ ir sakārtots $L$:

| rinda $i$ | $F[i]$ | $L[i]$ | $L[i]$ kārtas numurs | $\textsf{LF}(i)$ |
| --- | --- | --- | --- | --- |
| 0 | `$` | `A` | 1. `A` | 1 |
| 1 | `A` | `S` | 1. `S` | 4 |
| 2 | `A` | `S` | 2. `S` | 5 |
| 3 | `L` | `A` | 2. `A` | 2 |
| 4 | `S` | `L` | 1. `L` | 3 |
| 5 | `S` | `$` | 1. `$` | 0 |

Attēlojums *Last-to-First* $\textsf{LF}(i)$ burta $k$-to parādīšanos kolonnā $L$ pārvērš par tā paša burta
$k$-to parādīšanos kolonnā $F$ -- vienādi burti abās kolonnās saglabā savstarpējo secību. Tā kā katra
rinda ir cikliskā permutācija, $L[i]$ vārdā $w$ ir burts, kas atrodas *pirms* $F[i]$. Tāpēc sākam no
$0$. rindas -- permutācijas, kas sākas ar `$`, t.i., $\mathtt{\$}w_1w_2\ldots w_5$ -- un lasām $w$
**no beigām**:

| Solis | rinda $i$ | $L[i]$ | pozīcija vārdā $w$ | nākamā rinda $\textsf{LF}(i)$ |
| --- | --- | --- | --- | --- |
| 1 | 0 | `A` | $w_5$ | 1 |
| 2 | 1 | `S` | $w_4$ | 4 |
| 3 | 4 | `L` | $w_3$ | 3 |
| 4 | 3 | `A` | $w_2$ | 2 |
| 5 | 2 | `S` | $w_1$ | 5 |

$$
w = \mathtt{S}\,\mathtt{A}\,\mathtt{L}\,\mathtt{S}\,\mathtt{A}\,\mathtt{\$} = \mathtt{SALSA\$} .
$$

Pārbaude pēc definīcijas:

```text
S A L S A $              $ S A L S A          A
A L S A $ S              A $ S A L S          S
L S A $ S A    --->      A L S A $ S          S
S A $ S A L              L S A $ S A          A
A $ S A L S              S A $ S A L          L
$ S A L S A              S A L S A $          $
```

Pēdējā kolonna ir `ASSAL$`, kā vajadzīgs. $\square$

### 8. uzdevums (BWT ar sufiksu masīvu)

$w = \mathtt{BARBARA\$}$, $n = 8$; pozīcijas numurējam no $0$:

```text
 0 1 2 3 4 5 6 7
 B A R B A R A $
```

**(a)** Visi sufiksi, sakārtoti ar $\mathtt{\$} < \mathtt{A} < \mathtt{B} < \mathtt{R}$:

| Sufikss (netiek glabāts) | Sufiksa numurs |
| --- | --- |
| `$` | 7 |
| `A$` | 6 |
| `ARA$` | 4 |
| `ARBARA$` | 1 |
| `BARA$` | 3 |
| `BARBARA$` | 0 |
| `RA$` | 5 |
| `RBARA$` | 2 |

$$
A = [\,7,\; 6,\; 4,\; 1,\; 3,\; 0,\; 5,\; 2\,] .
$$

(`ARA$` ir pirms `ARBARA$`, jo trešie burti ir `A` < `B`; līdzīgi `BARA$` ir pirms `BARBARA$` un `RA$` --
pirms `RBARA$`.)

**(b)** $\textsf{efficientBWT}(w)$: katram $i$ izvada $w[A[i]-1]$, kur $j = -1$ aizstāj ar
$j = n - 1 = 7$:

| $i$ | $A[i]$ | $j = A[i]-1$ | $w[j]$ |
| --- | --- | --- | --- |
| 0 | 7 | 6 | `A` |
| 1 | 6 | 5 | `R` |
| 2 | 4 | 3 | `B` |
| 3 | 1 | 0 | `B` |
| 4 | 3 | 2 | `R` |
| 5 | 0 | $-1 \rightarrow 7$ | `$` |
| 6 | 5 | 4 | `A` |
| 7 | 2 | 1 | `A` |

$$
\text{BWT}(\mathtt{BARBARA\$}) = \mathtt{ARBBR\$AA} .
$$

Pārbaude ar cikliskajām permutācijām:

```text
B A R B A R A $              $ B A R B A R A     A
A R B A R A $ B              A $ B A R B A R     R
R B A R A $ B A              A R A $ B A R B     B
B A R A $ B A R    --->      A R B A R A $ B     B
A R A $ B A R B              B A R A $ B A R     R
R A $ B A R B A              B A R B A R A $     $
A $ B A R B A R              R A $ B A R B A     A
$ B A R B A R A              R B A R A $ B A     A
```

Pēdējā kolonna ir `ARBBR$AA`, un sakārtotās permutācijas ir tādā pašā secībā kā sakārtotie sufiksi:
rindas $0,1,\ldots,7$ sākas pozīcijās $7, 6, 4, 1, 3, 0, 5, 2$, t.i., tieši $A$. $5$. rinda, kas beidzas ar
`$`, ir sākotnējais vārds `BARBARA$`.

**(c)** Apzīmēsim ar $\text{rot}_i$ permutāciju, kas sākas pozīcijā $i$, un ar $\text{suf}_i$ sufiksu, kas
sākas pozīcijā $i$. Tad

$$
\text{rot}_i = \text{suf}_i \cdot w[0 \ldots i-1],
$$

t.i., katra permutācija *sākas* ar atbilstošo sufiksu. Ņemsim $i \neq j$ un salīdzināsim $\text{suf}_i$ ar
$\text{suf}_j$. Simbols `$` vārdā $w$ ir tieši vienu reizi un tikai pašās beigās, tāpēc neviens no
sufiksiem nav otra prefikss: pozīcijā, kurā īsākajam (teiksim, $\text{suf}_i$) ir `$`, garākajam vēl ir
parasts burts, un `$` ir mazāks par visiem burtiem. Tātad salīdzināšanas rezultāts izšķiras **pie pirmā
`$` vai agrāk**.

Līdz šai pozīcijai $\text{rot}_i$ burtu pa burtam sakrīt ar $\text{suf}_i$ (permutācija atšķiras no sava
sufiksa tikai *pēc* sufiksa beigām), un tāpat arī $j$. Tāpēc tā pati pozīcija izšķir arī $\text{rot}_i$ un
$\text{rot}_j$ salīdzināšanu, un rezultāts ir tas pats:

$$
\text{suf}_i < \text{suf}_j \iff \text{rot}_i < \text{rot}_j .
$$

Tātad abi sakārtojumi sakrīt, un $A[i]$ norāda, kura permutācija ir $i$-tajā rindā. Bez unikāla, mazākā
beigu simbola tas neizpildās -- sk. nodaļas piemēru `CAA`, kur naivā BWT dod `CAA`, bet
$\textsf{efficientBWT}$ dod `AAC`.

**(d)** Apakšvirknes `BAR` sastapšanās vietas ir tieši to sufiksu sākuma pozīcijas, kuru prefikss ir
`BAR`. Tā kā sufiksu masīvs ir sakārtots **leksikogrāfiski**, visas virknes ar kopīgu prefiksu $P$ veido
vienu nepārtrauktu bloku: ja $\text{suf}_{A[i]} < \text{suf}_{A[k]} < \text{suf}_{A[j]}$ un abi galējie
sākas ar $P$, tad arī vidējam jāsākas ar $P$ -- citādi tas būtu vai nu mazāks par visām virknēm, kas sākas
ar $P$, vai lielāks par tām visām. Tāpēc atbildes ir blakus esoši masīva $A$ elementi.

Tātad pietiek ar divām binārajām meklēšanām masīvā $A$:

* *apakšējā* robeža -- mazākais $i$, kuram $\text{suf}_{A[i]} \geq \mathtt{BAR}$;
* *augšējā* robeža -- mazākais $i$, kuram $\text{suf}_{A[i]}$ vairs nesākas ar `BAR`.

Vārdam `BARBARA$`:

| $i$ | $A[i]$ | Sufikss | Sākas ar `BAR`? |
| --- | --- | --- | --- |
| 3 | 1 | `ARBARA$` | nē |
| 4 | 3 | `BARA$` | **jā** |
| 5 | 0 | `BARBARA$` | **jā** |
| 6 | 5 | `RA$` | nē |

Bloks ir $A[4 \ldots 5] = \lbrace 3,\, 0 \rbrace$: `BAR` sastopams pozīcijās $0$ un $3$, un sastapšanās
reižu skaitu ($2$) var nolasīt kā bloka garumu, pašas vietas nepārbaudot.

Katra salīdzināšana prasa $O(|P|)$ simbolu salīdzinājumu, tāpēc meklēšana aizņem $O(|P| \log n)$ laiku un
vēl $O(\textit{occ})$ atbilžu izvadīšanai.

**(e)**

| | Naivā BWT | Ar sufiksu masīvu |
| --- | --- | --- |
| Datu izveide | izrakstīt $n$ permutācijas ar garumu $n$ | uzbūvēt sufiksu masīvu $A$ |
| Atmiņa | $O(n^2)$ | $O(n)$ |
| Kārtošana | $O(n \log n)$ salīdzinājumi $\times$ $O(n)$ katram salīdzinājumam | $O(n)$ (lineāra laika konstrukcija) |
| BWT nolasīšana | pēdējā kolonna, $O(n)$ | $n$ piekļuves $w[A[i]-1]$, $O(n)$ |
| **Kopējais laiks** | $O(n^2 \log n)$ | $O(n)$ |

Tipiskam bzip2 blokam ar $n = 900\,000$ baitiem atšķirība ir izšķiroša:
$n^2 \log_2 n \approx 1.6 \cdot 10^{13}$ pret $n \approx 10^6$ -- un naivajai metodei vajadzētu arī apmēram
$8 \cdot 10^{11}$ baitu tikai matricas glabāšanai. (Pat vienkārša, uz salīdzināšanu balstīta sufiksu masīva
konstrukcija ar $O(n \log^2 n)$ ir pilnīgi praktiska; lineāra laika algoritmi ir sufiksu masīvu nodaļā
kursa beigās.) $\square$

## Markova ķēdes

### 9. uzdevums (Markova ķēde un saspiešana)

**(a)** Ķēdes grafs:

```text
        1/2
       ┌───┐
       │   ↓
    ┌─────────┐   1/2    ┌─────────┐    1     ┌─────────┐
    │    A    │ ───────> │    B    │ ───────> │    C    │
    └─────────┘          └─────────┘          └─────────┘
         ↑                                         │
         └─────────────────────────────────────────┘
                            1
```

Ja stāvokļi ir secībā $(\mathtt{A}, \mathtt{B}, \mathtt{C})$ un rindas atbilst pašreizējam stāvoklim:

$$
P = \left( \begin{array}{ccc}
1/2 & 1/2 & 0 \\
0 & 0 & 1 \\
1 & 0 & 0
\end{array} \right) .
$$

Teksts sākas ar `A` ar varbūtību $1$, tāpēc virknei `ABCAABCA` sareizinām $7$ pāreju varbūtības:

$$
p = \underbrace{P_{AB}}_{1/2} \cdot \underbrace{P_{BC}}_{1} \cdot \underbrace{P_{CA}}_{1} \cdot
\underbrace{P_{AA}}_{1/2} \cdot \underbrace{P_{AB}}_{1/2} \cdot \underbrace{P_{BC}}_{1} \cdot
\underbrace{P_{CA}}_{1} = \left( \frac12 \right)^3 = \frac18 .
$$

Gadījuma rakstura ir tikai trīs pārejas no `A`; visas pārējās ir noteiktas.

**(b)** Stacionārais sadalījums apmierina $\pi P = \pi$, t.i.,

$$
\left\lbrace \begin{array}{l}
\pi_A = \tfrac12 \pi_A + \pi_C \\
\pi_B = \tfrac12 \pi_A \\
\pi_C = \pi_B
\end{array} \right.
\qquad \Longrightarrow \qquad \pi_C = \pi_B = \tfrac12 \pi_A ,
$$

un pēc tam pirmais vienādojums izpildās automātiski. Normējot
$\pi_A + \tfrac12 \pi_A + \tfrac12 \pi_A = 2\pi_A = 1$:

$$
\pi = \left( \pi_A, \pi_B, \pi_C \right) = \left( \tfrac12,\; \tfrac14,\; \tfrac14 \right) .
$$

(Pārbaude: vidēji puse burtu ir `A`, bet `B` un `C` vienmēr nāk pāros, tāpēc tiem jābūt vienlīdz biežiem.)

**(c)** *Nereducējama:* jā -- cikls $\mathtt{A} \to \mathtt{B} \to \mathtt{C} \to \mathtt{A}$ ļauj no katra
stāvokļa nonākt katrā citā. Lempela-Ziva nodaļas formulējumā ("Markova ķēdes, ja no katra stāvokļa var
nonākt katrā citā, ir ergodiskas") ķēde ir **ergodiska**.

*Periodiska:* nē. Ciklu garumi ir $1$ (cilpa $\mathtt{A} \to \mathtt{A}$) un $3$, un
$\gcd(1,3) = 1$, tāpēc ķēde ir **aperiodiska**. Tāpēc sadalījums laikā $n$ no jebkura sākuma stāvokļa
konverģē uz $\pi$, un process ir asimptotiski stacionārs.

*Ja pāreju $\mathtt{A} \to \mathtt{A}$ noņem,* ķēde kļūst par deterministisku ciklu
$\mathtt{A} \to \mathtt{B} \to \mathtt{C} \to \mathtt{A}$:

* tā joprojām ir nereducējama, un tās stacionārais sadalījums kļūst $\pi = (1/3, 1/3, 1/3)$;
* bet tagad tai ir **periods $3$**: sākot no `A`, burts laikā $n$ ir precīzi noteikts, tāpēc sadalījums
  laikā $n$ nekad nekonverģē. Kā teikts nodaļā, periodiska virkne nevar būt stacionāra -- visi varbūtību
  sadalījumi atkarīgi no perioda fāzes. (Stingrākajā Markova ķēžu terminoloģijā periodisku ķēdi arī
  nesauc par ergodisku.)
* Teksts kļūst `ABCABCABC...`, kurā nav nekādas nejaušības: vidējā entropija ir $0$, un jebkurš saprātīgs
  saspiešanas algoritms $n$ burtus saspiež līdz $O(\log n)$ bitiem.

**(d)** *Viena burta entropija* stacionārajā sadalījumā $\pi = (1/2, 1/4, 1/4)$:

$$
H(X_1) = \tfrac12 \log_2 2 + \tfrac14 \log_2 4 + \tfrac14 \log_2 4
= \tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 = 1.5 \text{ biti}.
$$

*Vidējā entropija.* Matricas $P$ rindu entropijas ir

| stāvoklis $i$ | pārejas | $H(\text{pārejas no } i)$ |
| --- | --- | --- |
| `A` | $(1/2,\, 1/2,\, 0)$ | $1$ bits |
| `B` | $(0,\, 0,\, 1)$ | $0$ biti |
| `C` | $(1,\, 0,\, 0)$ | $0$ biti |

$$
H(X) = \sum_i \pi_i \cdot H(\text{pārejas no } i)
= \tfrac12 \cdot 1 + \tfrac14 \cdot 0 + \tfrac14 \cdot 0 = 0.5 \text{ biti uz burtu}.
$$

*Hafmana kods atsevišķiem burtiem.* Ar varbūtībām $(1/2, 1/4, 1/4)$ Hafmana kods ir
$\mathtt{A} \to \mathtt{0}$, $\mathtt{B} \to \mathtt{10}$, $\mathtt{C} \to \mathtt{11}$, un

$$
\ell_a(C^{\ast}) = \tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 = 1.5 \text{ biti uz burtu}.
$$

Šeit Hafmana kods ir **precīzi optimāls viena burta modelim** ($\ell_a = H(X_1)$, jo visas varbūtības ir
divnieka pakāpes) un tomēr tērē **trīsreiz** vairāk par vidējo entropiju $0.5$. Zudums nav saistīts ar
Hafmana algoritmu -- tas rodas no modeļa, kas neņem vērā kontekstu.

**(e)** Sadalām tekstu pēc katra `A`. Ķēde ir stāvoklī `A` sākumā un -- pēc konstrukcijas -- uzreiz pēc katra
`A`. No `A` ir tieši divi turpinājumi:

* ar varbūtību $1/2$ nākamais burts ir `A` -- gabals ir `A`, un mēs atkal esam stāvoklī `A`;
* ar varbūtību $1/2$ nākamais burts ir `B`, pēc kura noteikti seko `C` un tad `A` -- gabals ir `BCA`, un
  atkal nonākam stāvoklī `A`.

Abi gabali beidzas vienā un tajā pašā stāvoklī `A`, tāpēc gabali ir **neatkarīgi un vienādi sadalīti**,
katrs ar varbūtību $1/2$. Piemēram,

$$
\mathtt{A}\,|\,\mathtt{BCA}\,|\,\mathtt{A}\,|\,\mathtt{BCA}\,|\,\mathtt{A} \ldots
$$

Kodējam katru gabalu ar vienu bitu: $\mathtt{A} \to \mathtt{0}$, $\mathtt{BCA} \to \mathtt{1}$. (Tas ir
Hafmana kods diviem vienādi varbūtīgiem ziņojumiem -- optimāls, un tā vidējais garums ir vienāds ar viena
gabala entropiju, kas ir tieši $1$ bits.) Vidējais gabala garums ir

$$
\mathbb{E}[\text{burti gabalā}] = \tfrac12 \cdot 1 + \tfrac12 \cdot 3 = 2 \text{ burti},
$$

tāpēc izmaksas uz burtu ir

$$
\frac{1 \text{ bits}}{2 \text{ burti}} = 0.5 \text{ biti uz burtu} = H(X) .
$$

Tā ir tieši vidējā entropija -- trešdaļa no tā, ko tērē Hafmana kods atsevišķiem burtiem.

**Kurš algoritms gabalus atrod pats?** **Lempela-Ziva algoritmi.** $\textsf{LZ78-Encode}$ būvē atkārtotu
frāžu vārdnīcu un ātri tajā ievieto `BCA` (un `A`, `BCAB`, ...), pēc tam katra sastapšanās maksā vienu
kodu; $\textsf{LZ77-Encode}$ dara to pašu ar sakritībām slīdošajā logā. Nevienam no tiem nepaziņo pāreju
matricu -- struktūru tie atklāj no pašiem datiem. Tieši to apgalvo Lempela-Ziva nodaļas asimptotiskās
optimalitātes teorēma: stacionāram ergodiskam avotam

$$
\limsup_n \frac{1}{n} \ell_{\text{LZW}}(X_{1:n}) \leq H(X)
$$

ar varbūtību $1$. Šeit $H(X) = 0.5$ biti uz burtu, bet entropijas kods, kas veidots pēc viena burta
sadalījuma, nevar nokāpt zemāk par $1.5$. $\square$
