---
layout: default
title: "Zudumradošā saspiešana: Attēli un audio"
lang: lv
permalink: /lectures/lossy_images_and_audio/index.lv.html
---
# 5. Zudumradošā saspiešana: Attēli un audio

Apskatām sekojošas sadaļas:

* Krāsas un kvantizācija
* Krāsu telpas: RGB, YIQ, YUV un YCbCr
* JPEG iekodēšana (7 soļi)
* Diskrētā kosinusu transformācija
* Citi attēlu formāti; kvantizācija citās jomās

## Krāsas un kvantizācija

**Piemērs:** Melnbalti attēli.

* Attēlā skaitlis $0-255$ apzīmē krāsu (no melnas līdz baltai).
* Visus $256$ toņus acs neatšķir, tāpēc var attēlot $256$ krāsas uz mazāku skaitu.
* Vienkāršākais attēlojums, piemēram $f(x) = \left\lfloor\frac{x}{4} \right\rfloor$. Tad $f\,:\,\lbrace 0,\ldots,255 \rbrace \rightarrow \lbrace 0,\ldots,63 \rbrace$.
* Praksē lieto sarežģītāku funkciju, kas kopā sagrupē krāsas, kuras acs sliktāk atšķir.

**Vektoru kvantizācija**

* Krāsainu punktu nosaka $3$ vērtības ($\text{Red}, \text{Green}, \text{Blue}$). Telpa $\lbrace 0,\ldots,255 \rbrace^3$.
* $f(x_1, x_2, x_3 ) = (y_1,y_2,y_3)$, tā, lai dažādi trijnieki $(x_1, x_2, x_3)$, kas attēlojas par vienu $(y_1,y_2,y_3)$, būtu grūti atšķirami.

Atkārtojums -- matricas reizināšana ar vektoru ir lineārs pārveidojums jeb funkcija: $\mathbf{R}^n \rightarrow \mathbf{R}^n$. To pieraksta šādi:

$$
\left( \begin{array}{c} x'_1 \\ x'_2 \\ \cdots \\ x'_n \end{array} \right)
=
\left( \begin{array}{cccc}
a_{11} &  a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \vdots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}
\end{array} \right)
\left( \begin{array}{c} x_1 \\ x_2 \\ \cdots \\ x_n \end{array} \right)
$$

## Krāsu telpas (*color spaces*)

Krāsu telpa nosaka, ar kādiem trim skaitļiem apraksta viena punkta (pikseļa) krāsu. Ekrāni un kameras strādā ar RGB, bet saspiešanai izdevīgāk krāsu sadalīt *gaišumā* (*luma*) un divās *krāsainības* (*chroma*) komponentēs. Redze gaišuma izmaiņas uztver daudz precīzāk nekā nokrāsas izmaiņas, tāpēc krāsainības komponentes var glabāt ar mazāku izšķirtspēju (sk. JPEG 2. soli).

### RGB

*RGB* ir aditīva krāsu telpa: krāsu iegūst, sajaucot sarkanu (R), zaļu (G) un zilu (B) gaismu. Parasti katru komponenti glabā kā $8$ bitu skaitli no $0$ līdz $255$; $(0,0,0)$ ir melns, $(255,255,255)$ -- balts. Visas trīs komponentes ir vienlīdz svarīgas, tāpēc nevienu no tām nevar saspiest vairāk par citām.

### YIQ

*YIQ* izmantoja analogās krāsu televīzijas standarts NTSC (ASV, 1953). "Y" ir gaišums (to rādīja arī melnbaltie televizori), bet "I" (*in-phase*) un "Q" (*quadrature*) -- krāsainība (nosaukumi nāk no signāla modulācijas). Ja $R, G, B \in [0;1]$ (8 bitu vērtība, dalīta ar $255$), tad

$$
\left( \begin{array}{c} Y \\ I \\ Q \end{array} \right)
= M
\left( \begin{array}{c} R \\ G \\ B \end{array} \right),
\qquad
M = \left( \begin{array}{rrr}
0.299 &  0.587 &  0.114 \\
0.5959 & -0.2746 & -0.3213 \\
0.2115 & -0.5227 &  0.3112
\end{array} \right).
$$

Tad $Y \in [0;1]$, $I \in [-0.5959; 0.5959]$ un $Q \in [-0.5227; 0.5227]$. Pelēkām krāsām ($R = G = B$) $I = Q = 0$, jo matricas $M$ otrās un trešās rindas summa ir $0$. Matrica $M$ ir apgriežama, tāpēc pārveidojums ir bezzudumu: $(R, G, B)^T = M^{-1} (Y, I, Q)^T$. Noapaļojot līdz trim zīmēm aiz komata, matricas $M^{-1}$ elementi ir

$$
\left( \begin{array}{rrr}
1 &  0.956 &  0.621 \\
1 & -0.272 & -0.647 \\
1 & -1.107 &  1.704
\end{array} \right).
$$

Attēlā redzams fotoattēls un tā Y, I, Q komponentes (I un Q attēlotas ar krāsu, kas atbilst attiecīgajai komponentei, ja pārējās ir vidējas):

| | |
| --- | --- |
| ![Kuldīga](figs/kuldiga.png) | ![Kuldīga -- Y komponente](figs/kuldiga1.png) |
| *oriģināls (RGB)* | *Y komponente* |
| ![Kuldīga -- I komponente](figs/kuldiga2.png) | ![Kuldīga -- Q komponente](figs/kuldiga3.png) |
| *I komponente* | *Q komponente* |

Gandrīz visa attēla struktūra (kontūras, detaļas) ir Y komponentē, bet I un Q komponentes ir izplūdušas. Redze precīzāk uztver "I" (pāreju no oranžā uz zilo) nekā "Q" (pāreju no zaļā uz violeto), tāpēc NTSC pārraidē Q signālam atvēlēja šaurāku frekvenču joslu nekā I.

![IQ plakne](figs/YIQ_IQ_plane.svg.png)

*IQ plakne, ja $Y=0.5$.*

### YUV un YCbCr

*YUV* ir analogās televīzijas (PAL, SECAM) krāsu telpa. Gaišums $Y$ ir tas pats, kas YIQ telpā, bet krāsainību apraksta ar zilās un sarkanās krāsas starpību no gaišuma ($R, G, B \in [0;1]$):

$$
Y = 0.299\,R + 0.587\,G + 0.114\,B, \qquad
U = 0.492\,(B - Y), \qquad
V = 0.877\,(R - Y).
$$

(YIQ ir tā pati UV plakne, pagriezta par $33^\circ$.)

*YCbCr* ir YUV digitālais variants: $B - Y$ un $R - Y$ mērogo tā, lai tie ietilptu $8$ bitos, un pieskaita $128$. JPEG failu formāts JFIF izmanto YCbCr pilnā diapazonā (ITU-R BT.601 koeficienti). Ja $R, G, B \in \lbrace 0, \ldots, 255 \rbrace$, tad

$$
\begin{array}{rcl}
Y  & = & 0.299\,R + 0.587\,G + 0.114\,B, \\[4pt]
\mathrm{Cb} & = & 128 + \dfrac{B - Y}{1.772}, \\[8pt]
\mathrm{Cr} & = & 128 + \dfrac{R - Y}{1.402}.
\end{array}
$$

Dalītāji $1.772 = 2\,(1 - 0.114)$ un $1.402 = 2\,(1 - 0.299)$ izvēlēti tā, lai $\mathrm{Cb}$ un $\mathrm{Cr}$ paliktu intervālā $[0;255]$. Pēc aprēķina visas trīs vērtības noapaļo līdz veselam skaitlim un apgriež līdz intervālam $[0;255]$. Pretējais pārveidojums seko tieši no šīm formulām:

$$
\begin{array}{rcl}
R & = & Y + 1.402\,(\mathrm{Cr} - 128), \\
B & = & Y + 1.772\,(\mathrm{Cb} - 128), \\
G & = & (Y - 0.299\,R - 0.114\,B) \,/\, 0.587.
\end{array}
$$

Pats pārveidojums ir apgriežams; informāciju zaudē tikai noapaļošana līdz veseliem skaitļiem.

<img
  id="cbcr_plakne"
  alt="CbCr plakne"
  src="{{ '/lectures/lossy_images_and_audio/figs/cbcr-plane.svg' | relative_url }}"
  style="width: 100%; max-width: 336px; border:none; background-color:#FFFFFF;"
/>

*CbCr plakne, ja $Y = 128$. Punktā $(\mathrm{Cb}, \mathrm{Cr}) = (128, 128)$ ir pelēks; krāsas, kas iziet ārpus RGB diapazona, ir apgrieztas.*

## JPEG iekodēšana

JPEG (*Joint Photographic Experts Group*) standarts ISO/IEC 10918-1 (1992) apraksta vairākus attēlu saspiešanas režīmus: secīgo (*baseline*) un progresīvo DCT kodēšanu, bezzudumu režīmu un hierarhisko režīmu. Tālāk aprakstīta visbiežāk lietotā -- secīgā (*baseline*) iekodēšana; rezultātu glabā JFIF faila formātā (`*.jpg`).

* Ievade: punktu attēls; katra punkta krāsu apraksta trīs $8$ bitu skaitļi $R, G, B \in \lbrace 0, \ldots, 255 \rbrace$.
* Izvade: baitu virkne (JFIF fails).

<img
  id="jpeg_kodesanas_soli"
  alt="JPEG kodēšanas soļi"
  src="{{ '/lectures/lossy_images_and_audio/figs/jpeg-pipeline.svg' | relative_url }}"
  style="width: 100%; max-width: 980px; border:none; background-color:#FFFFFF;"
/>

*JPEG kodēšanas soļi; numuri atbilst tālāk aprakstītajiem 1.-7. solim. Skaitļi ir īsti: paraugbloku pārveido ar DCT-II, kvantizē ar standarta gaišuma kvantizācijas tabulu un nolasa zig-zag secībā (sk. "Python piemēri").*

**1. solis: Krāsu telpas maiņa (RGB $\rightarrow$ YCbCr).** Katram pikselim no $(R, G, B)$ aprēķina $(Y, \mathrm{Cb}, \mathrm{Cr})$ ar JFIF formulām (sk. "YUV un YCbCr"), rezultātu noapaļo līdz veselam skaitlim un apgriež līdz $[0;255]$. Iegūst trīs attēla *komponentes* (plaknes): $Y$, $\mathrm{Cb}$ un $\mathrm{Cr}$.

**2. solis: Krāsainības izretināšana (4:2:0 *chroma subsampling*).** $Y$ komponenti atstāj nemainītu. $\mathrm{Cb}$ un $\mathrm{Cr}$ komponentēs katru $2 \times 2$ pikseļu kvadrātu aizstāj ar vienu vērtību -- četru vērtību vidējo aritmētisko (noapaļotu). Krāsainības komponentes kļūst divreiz šaurākas un divreiz zemākas, tāpēc datu apjoms samazinās no $3$ līdz $1 + \frac{1}{4} + \frac{1}{4} = 1.5$ vērtībām uz pikseli. Standarts pieļauj arī 4:4:4 (bez izretināšanas) un 4:2:2 (izretina tikai horizontāli).

![Režģa izretināšana](figs/sparser-grid.png)

*Režģa izretināšana (Skipping grid).*

**3. solis: Sadalīšana $8 \times 8$ blokos.** Attēla platumu un augstumu papildina līdz $16$ daudzkārtnim (parasti atkārtojot pēdējo kolonnu un rindu). Katru komponenti sadala $8 \times 8$ blokos. Ar 4:2:0 izretināšanu katram $16 \times 16$ pikseļu laukumam (*MCU, minimum coded unit*) atbilst četri $Y$ bloki, viens $\mathrm{Cb}$ bloks un viens $\mathrm{Cr}$ bloks; tos kodē šādā secībā. No katras bloka vērtības atņem $128$ (*level shift*), lai vērtības būtu intervālā $[-128; 127]$.

**4. solis: Diskrētā kosinusu transformācija (DCT-II).** Katram blokam $A$ aprēķina tāda paša izmēra koeficientu matricu $B = C A C^T$ (sk. "Diskrēto kosinusu transformācijas"):

$$
B_{u,v} = \alpha_u \alpha_v \sum_{x=0}^{7} \sum_{y=0}^{7} A_{x,y} \cos\frac{(2x+1)u\pi}{16} \cos\frac{(2y+1)v\pi}{16},
\qquad
\alpha_0 = \sqrt{\tfrac{1}{8}},\;\; \alpha_k = \sqrt{\tfrac{2}{8}} \;\; (k \geq 1).
$$

$B_{0,0}$ ir *DC koeficients* -- tas ir $8$ reizes lielāks par bloka vidējo vērtību. Pārējie $63$ ir *AC koeficienti*; jo lielāki $u$ un $v$, jo augstākai vertikālai un horizontālai frekvencei (sīkākām detaļām) tie atbilst. Gludos attēla apgabalos gandrīz visa "enerģija" koncentrējas dažos koeficientos kreisajā augšējā stūrī. Šis solis pats par sevi ir bezzudumu (DCT ir apgriežama).

**5. solis: Kvantizācija.** Katru koeficientu dala ar kvantizācijas tabulas elementu un noapaļo līdz tuvākajam veselajam skaitlim:

$$
\hat{B}_{u,v} = \operatorname{round}\left( \frac{B_{u,v}}{Q_{u,v}} \right).
$$

Šis ir galvenais solis, kurā zūd informācija: atkodētājs varēs atjaunot tikai $\hat{B}_{u,v} \cdot Q_{u,v}$. Augstām frekvencēm, kuras acs uztver vājāk, $Q_{u,v}$ ir lielāks, tāpēc lielākā daļa šo koeficientu kļūst par $0$. JPEG standarta (pielikums K) gaišuma tabula ir

$$
Q = \left( \begin{array}{rrrrrrrr}
16 & 11 & 10 & 16 & 24 & 40 & 51 & 61 \\
12 & 12 & 14 & 19 & 26 & 58 & 60 & 55 \\
14 & 13 & 16 & 24 & 40 & 57 & 69 & 56 \\
14 & 17 & 22 & 29 & 51 & 87 & 80 & 62 \\
18 & 22 & 37 & 56 & 68 & 109 & 103 & 77 \\
24 & 35 & 55 & 64 & 81 & 104 & 113 & 92 \\
49 & 64 & 78 & 87 & 103 & 121 & 120 & 101 \\
72 & 92 & 95 & 98 & 112 & 100 & 103 & 99
\end{array} \right);
$$

mazākā vērtība ir $Q_{0,2} = 10$, lielākā -- $Q_{6,5} = 121$ (indeksus $u, v$ skaita no $0$). Krāsainības komponentēm ir cita tabula ar lielākām vērtībām. Kvalitātes parametrs $q \in \lbrace 1, \ldots, 100 \rbrace$ tabulu mērogo; bibliotēkā *libjpeg* $S = 5000/q$, ja $q < 50$, un $S = 200 - 2q$, ja $q \geq 50$, bet jaunā tabula ir $\max\left(1, \left\lfloor (S \cdot Q_{u,v} + 50)/100 \right\rfloor\right)$. Tabulas ($q = 50$ gadījumā -- tieši augstāk dotā) ieraksta failā, lai atkodētājs varētu tās izmantot.

**6. solis: Zig-zag secība, DC un AC koeficientu kodēšana.** Kvantizēto bloku nolasa zig-zag secībā -- pa diagonālēm no kreisā augšējā stūra uz labo apakšējo. Skaitlis matricas pozīcijā $(u, v)$ ir šī koeficienta numurs virknē:

$$
\left( \begin{array}{rrrrrrrr}
0 & 1 & 5 & 6 & 14 & 15 & 27 & 28 \\
2 & 4 & 7 & 13 & 16 & 26 & 29 & 42 \\
3 & 8 & 12 & 17 & 25 & 30 & 41 & 43 \\
9 & 11 & 18 & 24 & 31 & 40 & 44 & 53 \\
10 & 19 & 23 & 32 & 39 & 45 & 52 & 54 \\
20 & 22 & 33 & 38 & 46 & 51 & 55 & 60 \\
21 & 34 & 37 & 47 & 50 & 56 & 59 & 61 \\
35 & 36 & 48 & 49 & 57 & 58 & 62 & 63
\end{array} \right)
$$

Tā zemo frekvenču koeficienti nonāk virknes sākumā, bet nulles -- beigās.

* **DC koeficients** (numurs $0$) kaimiņu blokos parasti ir līdzīgs, tāpēc kodē starpību $\mathrm{DIFF} = \mathrm{DC}_k - \mathrm{DC}_{k-1}$ ar tās pašas komponentes iepriekšējā bloka DC vērtību (pirmajam blokam $\mathrm{DC}_{k-1} = 0$). Šo paņēmienu sauc par DPCM (*differential pulse-code modulation*).
* **AC koeficientus** (numuri $1 \ldots 63$) pārveido par pāru virkni $(\mathrm{RUN}, \mathrm{VALUE})$, kur $\mathrm{VALUE} \neq 0$ ir kārtējais nenulles koeficients, bet $\mathrm{RUN} \in \lbrace 0, \ldots, 15 \rbrace$ -- nuļļu skaits pirms tā. $16$ nulles pēc kārtas kodē ar īpašu pāri ZRL $= (15, 0)$. Ja līdz bloka beigām paliek tikai nulles, izvada simbolu EOB (*end of block*).

Katru nenulles vērtību $v$ (gan $\mathrm{DIFF}$, gan $\mathrm{VALUE}$) pieraksta kā *kategoriju* $\mathrm{SIZE}$ -- skaitļa $\lvert v \rvert$ bināro ciparu skaitu -- un $\mathrm{SIZE}$ papildu bitiem: pozitīvam $v$ tie ir $v$ binārais pieraksts, negatīvam -- skaitļa $v + 2^{\mathrm{SIZE}} - 1$ binārais pieraksts. Piemēram, $-3$: $\mathrm{SIZE} = 2$, papildu biti `00`; $-26$: $\mathrm{SIZE} = 5$, papildu biti `00101`.

*Piemērs* (attēlā redzamais bloks): $\mathrm{DC} = -26$, un AC virkne ir `−3 0 −3 −2 −6 2 −4 1 −3 1 1 5 1 2 −1 1 −1 2 0 0 0 0 0 −1 −1` un vēl $38$ nulles. Pāri: $(0,-3)$, $(1,-3)$, $(0,-2)$, $(0,-6)$, $(0,2)$, $(0,-4)$, $(0,1)$, $(0,-3)$, $(0,1)$, $(0,1)$, $(0,5)$, $(0,1)$, $(0,2)$, $(0,-1)$, $(0,1)$, $(0,-1)$, $(0,2)$, $(5,-1)$, $(0,-1)$, EOB.

**7. solis: Entropijas kodēšana un faila izveide.** Baseline režīmā izmanto Hafmana kodu. DC koeficientam kodē simbolu $\mathrm{SIZE}$, bet AC pārim -- baitu $16 \cdot \mathrm{RUN} + \mathrm{SIZE}$ (EOB ir $0$, ZRL ir $240$). Aiz katra Hafmana kodavārda nekodētus pieraksta papildu bitus. Hafmana kodu tabulas (atsevišķas DC un AC simboliem, gaišumam un krāsainībai) var ņemt no standarta pielikuma K vai izveidot katram attēlam (optimizētas tabulas); tās ieraksta failā. Standarts pieļauj arī aritmētisko kodēšanu, bet to atbalsta reti.

*Piemērs:* Ja iepriekšējā bloka DC ir $0$, tad $\mathrm{DIFF} = -26$, $\mathrm{SIZE} = 5$; standarta gaišuma DC tabulā kategorijai $5$ atbilst kodavārds `110`, tātad izvada `110` `00101`. Pirmais AC pāris $(0, -3)$ ir simbols $16 \cdot 0 + 2 = 2$ ar kodavārdu `01` un papildu bitiem `00`. Bitu virkne sākas ar `1100 0101 0100`...

Bitus sapako baitos. Ja datos rodas baits `FF`, aiz tā ieraksta `00` (*byte stuffing*), lai to nevarētu sajaukt ar marķieri. JFIF failu veido marķieru segmenti: SOI (`FF D8`, attēla sākums), APP0 (JFIF galvene), DQT (kvantizācijas tabulas), SOF0 (attēla izmēri un komponentes), DHT (Hafmana tabulas), SOS (skenēšanas sākums) un tai sekojošie saspiestie dati, EOI (`FF D9`, attēla beigas).

**Atkodēšana** izpilda tos pašus soļus pretējā secībā: Hafmana atkodēšana, DC un AC atjaunošana, $B_{u,v} = \hat{B}_{u,v} \cdot Q_{u,v}$, apgrieztā DCT $A = C^T B C$, $+128$, krāsainības komponenšu palielināšana un YCbCr $\rightarrow$ RGB. Informācija zūd tikai 2. un 5. solī (un noapaļojot 1. solī).

### Python piemēri

**DCT ar SciPy.** Funkcija `dct` ar `norm='ortho'` aprēķina tieši DCT-II, kas definēta augstāk (`dct2(A)` ir $C A C^T$):

```python
import numpy as np
from scipy.fftpack import dct, idct

def dct2(arr):
    return dct(dct(arr.T, norm='ortho').T, norm='ortho')

def idct2(arr):
    return idct(idct(arr.T, norm='ortho').T, norm='ortho')

# Create an 8x8 matrix with random values between 0 and 1
matrix = np.random.rand(8, 8)
print(matrix)
dct_coefficients = dct2(matrix)
print(dct_coefficients)
inverse_dct = idct2(dct_coefficients)
print(inverse_dct)
```

**Viens bloks cauri 3.-6. solim.** Programma iegūst attēlā redzamos skaitļus: kvantizēto bloku, $\mathrm{DC} = -26$ un $(\mathrm{RUN}, \mathrm{VALUE})$ pārus.

```python
import numpy as np

# 8x8 gaišuma (Y) bloks, vērtības 0..255
A = np.array([
    [52, 55, 61, 66, 70, 61, 64, 73],
    [63, 59, 55, 90, 109, 85, 69, 72],
    [62, 59, 68, 113, 144, 104, 66, 73],
    [63, 58, 71, 122, 154, 106, 70, 69],
    [67, 61, 68, 104, 126, 88, 68, 70],
    [79, 65, 60, 70, 77, 68, 58, 75],
    [85, 71, 64, 59, 55, 61, 65, 83],
    [87, 79, 69, 68, 65, 76, 78, 94]])

# JPEG standarta gaišuma kvantizācijas tabula (kvalitāte 50)
Q = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]])

# 3. solis: līmeņa nobīde
A0 = A - 128

# 4. solis: DCT-II, B = C A C^T
k, n = np.meshgrid(range(8), range(8), indexing="ij")
C = np.cos((2 * n + 1) * k * np.pi / 16)
C[0, :] *= np.sqrt(1 / 8)
C[1:, :] *= np.sqrt(2 / 8)
B = C @ A0 @ C.T

# 5. solis: kvantizācija
Bq = np.round(B / Q).astype(int)

# 6. solis: zig-zag secība un (RUN, VALUE) pāri
order = sorted(((u, v) for u in range(8) for v in range(8)),
               key=lambda p: (p[0] + p[1], p[1] if (p[0] + p[1]) % 2 == 0 else p[0]))
zz = [int(Bq[u, v]) for u, v in order]
dc, ac = zz[0], zz[1:]
pairs, run = [], 0
last = max((i for i, x in enumerate(ac) if x != 0), default=-1)
for x in ac[:last + 1]:
    if x == 0:
        run += 1
        if run == 16:
            pairs.append((15, 0))   # ZRL: 16 nulles pēc kārtas
            run = 0
    else:
        pairs.append((run, x))
        run = 0
pairs.append("EOB")

print(Bq)
print("DC =", dc)
print(pairs)
```

## Diskrēto kosinusu transformācijas

Nasirs Ahmeds 1972.gadā piedāvāja šo algoritmu signālu saspiešanai:

$$
y_k = \alpha_k \sum_{n=0}^{N-1} x_n \cos \left[ \frac{\pi (2n + 1) k}{2N} \right]
$$

kur $k \in \lbrace 0, \ldots, N-1 \rbrace$ un normalizācijas reizinātājs ir $\alpha_k$, kur

$$
\alpha_k = \begin{cases}
\sqrt{\frac{1}{N}} & \text{if } k = 0 \\
\sqrt{\frac{2}{N}} & \text{if } k \neq 0
\end{cases}
$$

Divu dimensiju gadījums parādījās drīz pēc tam un ir dabisks vispārinājums. To var pierakstīt matricu formā šādi:

Katrai $8 \times 8$ krāsu intensitāšu matricai (*spatial domain*) izveidojam matricu $A$. DCT transformācijas rezultāts ir tāda paša izmēra matrica $B$ (*frequency domain*), ko var iegūt šādi:

$$
B = C A C^T,
$$

kur $C$ ir $8 \times 8$ koeficientu matrica, ko definē šādi:

$$
C_{k, n} = \alpha_k \cos\left(\frac{(2n + 1)k\pi}{16}\right),
$$

kur $k, n = 0, 1, \ldots, 7$, un normalizācijas reizinātāji $\alpha_k$ ir šādi:

$$
\alpha_k = \begin{cases}
\sqrt{\frac{1}{8}} & \text{if } k = 0 \\
\sqrt{\frac{2}{8}} & \text{if } k \neq 0
\end{cases}
$$

Vienu elementu $B_{u,v}$ matricā $B$ var pierakstīt šādi:

$$
B_{u, v} = \sum_{x=0}^{7} \sum_{y=0}^{7} A_{x, y} \cos\left(\frac{(2x + 1)u\pi}{16}\right) \cos\left(\frac{(2y + 1)v\pi}{16}\right) \alpha_u \alpha_v
$$

kur $u, v, x, y \in \lbrace 0, 1, \ldots, 7 \rbrace$.

## AVIF attēlu formāts

* Izņemot JPEG, ir populārs Google izveidotais formāts WebP, kas labi saspiežams un ir populārs pārlūkprogrammās.
* HEIF/HEIC (High Efficiency Image Format) ir radniecīgs video kodekam H.265; to veicina Apple.
* AVIF ir radniecīgs pazīstamajam atvērtajam video kodekam AV1.
* JPEG XL ir vēl visai jauns formāts (nav sevišķi plaši atbalstīts), bet ar vairākām jaunām iespējām, labu saspiešanu dažādos robežgadījumos un arī pilnu savietojamību ar JPEG.

AVIF idejas mazliet apskatām šajā kursā.

### Python piemērs

```bash
pip install pillow imageio pillow-avif-plugin
```

```python
from PIL import Image, ImageDraw
import imageio

# Create a white square image
image_size = 256
white_image = Image.new("RGB", (image_size, image_size), "white")

# Draw a red circle in the middle
draw = ImageDraw.Draw(white_image)
circle_radius = 50
circle_center = (image_size // 2, image_size // 2)
draw.ellipse(
    [
        (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
        (circle_center[0] + circle_radius, circle_center[1] + circle_radius)
    ],
    fill="red"
)

import pillow_avif
white_image.save("output.avif", format="AVIF")
print("Image saved as output.avif")
```

## Kvantizācija citās jomās

**Definīcija:** Dotai punktu kopai $S$ par *Voronoja diagrammu* (*Voronoi diagram*) sauc plaknes apgabala punktu sadalījumu klasēs atkarībā no tā, kurš punkts no $S$ ir tuvākais.

Voronoja diagrammas klašu skaits sakrīt ar kopas $S$ elementu skaitu. Voronoja diagramma sastāv no daudzstūrveida šūnām, kur katras šūnas iekšpusē ir $S$ punkts.

![Kvantizācijas piemērs](figs/quantization-illustration.png)

*Kvantizācijas piemērs.*

### Proporcionālās vēlēšanu sistēmas

**Definīcija:** Baricentriskās koordinātes 3 dimensijās piekārto katram punktam regulārā trijstūrī $ABC$ nenegatīvu skaitļu trijnieku $(x,y,z)$, kas apmierina sakarību $x+y+z = 1$.

![Baricentriskās koordinātes](figs/surface-xyz.png)

Baricentriskās koordinātes ļauj attēlot proporcijas starp trim pozitīviem (vai nenegatīviem) skaitļiem. (Ja atļauj arī negatīvas baricentriskās koordinātes, tad tās piekārto skaitļu trijnieku $x + y + z = 1$ katram plaknes punktam, bet tādas šajā kursā neizmantosim.)

**Donta (D'Hondt) sistēma**

<img
  id="donta_metode"
  alt="Donta metode"
  src="{{ '/lectures/lossy_images_and_audio/figs/hondt.svg' | relative_url }}"
  style="width: 100%; max-width: 520px; border:none; background-color:#FFFFFF;"
/>

*Donta (D'Hondt) metode 5 deputātu krēsliem un 3 partijām. Punkts trijstūrī ir balsu sadalījums starp partijām A, B, C; apgabals rāda, kādu vietu sadalījumu K:M:N tas dod. Aplītis katrā apgabalā ir balsu attiecība, kas tieši atbilst šim vietu sadalījumam.*

**Senlaga (Sainte-Laguë) sistēma**

<img
  id="senlaga_metode"
  alt="Senlaga metode"
  src="{{ '/lectures/lossy_images_and_audio/figs/sainte-lague.svg' | relative_url }}"
  style="width: 100%; max-width: 520px; border:none; background-color:#FFFFFF;"
/>

*Senlaga (Sainte-Laguë) metode 5 deputātu krēsliem un 3 partijām (apzīmējumi kā iepriekš).*

## Uzdevumi

**5.1. uzdevums:** Izmantojam krāsu saspiešanai kvantizācijas algoritmu, kas lieto tikai pārlūkprogrammām draudzīgās krāsas: [Browser-safe color palette](https://whatis.techtarget.com/definition/216-color-browser-safe-palette).

* Pārlūkprogrammām draudzīgas ir tās krāsu koordinātes, kam abi hex cipariņi ir vienādi un dalās ar $3$ ($00,33,66,99,\text{CC},\text{FF}$). Ja krāsai visas 3 koordinātes ir draudzīgas, tad arī pati krāsa ir draudzīga. Teiksim, `00FF99` ir draudzīga krāsa, bet `22BB99` nav, jo "22" un "BB" koordinātes nav atļautas.
* Katru attēlā esošo pikseli (katru no RGB koordinātēm) noapaļo līdz tuvākajai draudzīgajai no kopas ($00,33,66,99,\text{CC},\text{FF}$), lai iegūtu pārlūkprogrammai draudzīgu krāsu.

Kāds ir saspiešanas koeficients šādam pārveidojumam (jaunais izmērs pret veco izmēru)?

## Izmantotā literatūra

1. [The MP3 is dead, say creators after terminating licensing](https://www.cnbc.com/2017/05/15/mp3-dead-say-creators-after-terminating-licensing.html) -- par audioformātu attīstību.
2. [Ungārijas 2018.g. vēlēšanas](https://en.wikipedia.org/wiki/2018_Hungarian_parliamentary_election) -- kā Donta metode palīdz noapaļot rezultātus par labu lielākajai partijai.
3. [The Theory Behind Mp3](http://www.mp3-tech.org/programmer/docs/mp3_theory.pdf) -- galvenās idejas audiofailu saspiešanai.
