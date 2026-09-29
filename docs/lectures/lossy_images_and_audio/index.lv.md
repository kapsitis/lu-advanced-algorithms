---
layout: default
title: "Zudumradošā saspiešana: Attēli un audio"
lang: lv
permalink: /lectures/lossy_images_and_audio/lv/
---
# 5. Zudumradošā saspiešana: Attēli un audio

Apskatām sekojošas sadaļas:

* Krāsas un kvantizācija
* Krāsu telpas: RGB, YIQ, YUV un YCbCr
* JPEG iekodēšana (7 soļi)
* Diskrētā kosinusu transformācija
* Citi attēlu formāti; kvantizācija citās jomās

* **Laboratorijas darbs:** {% include doc_links.html url="/lectures/lossy_images_and_audio/jpeg_lab/" %}
{: .small}

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

*Piezīme par apzīmējumu J:a:b.* Krāsainības izretināšanu apzīmē ar trim skaitļiem J:a:b, kas apraksta *atsauces apgabalu* -- J pikseļus platu un $2$ rindas augstu taisnstūri:

* **J** -- apgabala platums pikseļos (gandrīz vienmēr $4$). Gaišuma ($Y$) plakni neizretina: katrā apgabala rindā ir J gaišuma paraugi.
* **a** -- cik krāsainības paraugu ir apgabala *pirmajā* rindā. $a = J$ nozīmē, ka horizontāli neizretina, $a = J/2$ -- ka viens paraugs ir diviem blakus esošiem pikseļiem.
* **b** -- cik krāsainības paraugu ir apgabala *otrajā* rindā. $b = a$ nozīmē, ka otrajā rindā ir savi paraugi (vertikāli neizretina), bet $b = 0$ -- ka otrajā rindā savu paraugu nav un tā izmanto pirmās rindas paraugus, t.i., vertikāli izretina divas reizes.

Skaitļi a un b attiecas uz *katru* no abām krāsainības plaknēm ($\mathrm{Cb}$ un $\mathrm{Cr}$ tiek izretinātas vienādi). Tātad J:a:b **nav** attiecība "$Y : \mathrm{Cb} : \mathrm{Cr}$", un "0" apzīmējumā 4:2:0 nenozīmē, ka $\mathrm{Cr}$ komponentes nav -- tas nozīmē, ka katrā otrajā rindā nav jaunu krāsainības paraugu.

<img
  id="chroma_subsampling"
  alt="Krāsainības izretināšanas shēmas"
  src="{{ '/lectures/lossy_images_and_audio/figs/chroma-subsampling.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*Atsauces apgabals $4 \times 2$ pikseļi. Režģis -- gaišuma paraugi (katram pikselim savs); zaļie taisnstūri -- pikseļi, kuriem ir kopīgs krāsainības paraugs (tāds pats sadalījums gan $\mathrm{Cb}$, gan $\mathrm{Cr}$ plaknē).*

| Shēma | Krāsainība horizontāli | Krāsainība vertikāli | Vērtības uz pikseli | JPEG faktori $Y$ ($H \times V$) | Kur lieto |
| --- | --- | --- | --- | --- | --- |
| 4:4:4 | pilna | pilna | $3$ | $1 \times 1$ | augsta kvalitāte, grafika un teksts |
| 4:2:2 | $\frac{1}{2}$ | pilna | $2$ | $2 \times 1$ | profesionāls video, daļa kameru JPEG |
| 4:2:0 | $\frac{1}{2}$ | $\frac{1}{2}$ | $1.5$ | $2 \times 2$ | vairums JPEG un video (H.264, AV1), AVIF |
| 4:1:1 | $\frac{1}{4}$ | pilna | $1.5$ | $4 \times 1$ | DV video (NTSC) |
| 4:4:0 | pilna | $\frac{1}{2}$ | $2$ | $1 \times 2$ | reti (dažas kameras) |

Vērtību skaits uz pikseli ir $1 + 2 \cdot (\text{krāsainības paraugu daļa})$, piemēram, 4:2:0 gadījumā $1 + 2 \cdot \frac{1}{4} = 1.5$. JPEG failā pats apzīmējums J:a:b nav ierakstīts: SOF segmentā katrai komponentei norāda horizontālo un vertikālo izretināšanas faktoru $H \times V$ (relatīvo paraugu blīvumu). Ja $Y$ faktori ir $2 \times 2$, bet $\mathrm{Cb}$ un $\mathrm{Cr}$ -- $1 \times 1$, tā ir 4:2:0. Pelēktoņu attēlu, kurā ir tikai $Y$ plakne, dažkārt (piemēram, AV1 un AVIF dokumentācijā) apzīmē ar 4:0:0.

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

### Skaitlisks piemērs: DCT ar $N = 4$

Ar roku ērtāk rēķināt DCT garumā $N = 4$. Tad $y = C x$, kur $C_{k,n} = \alpha_k \cos\frac{\pi (2n+1) k}{8}$, $\alpha_0 = \frac{1}{2}$ un $\alpha_1 = \alpha_2 = \alpha_3 = \frac{1}{\sqrt{2}}$. Matricā $C$ ir tikai trīs dažādi skaitļi (ar precizitāti līdz zīmei):

$$
C = \left( \begin{array}{rrrr}
a & a & a & a \\
b & c & -c & -b \\
a & -a & -a & a \\
c & -b & b & -c
\end{array} \right),
\qquad
\begin{array}{l}
a = \frac{1}{2}, \\[4pt]
b = \frac{1}{\sqrt{2}} \cos\frac{\pi}{8} = 0.65328\ldots, \\[4pt]
c = \frac{1}{\sqrt{2}} \cos\frac{3\pi}{8} = 0.27060\ldots
\end{array}
$$

Noderīgas sakarības: $b + c = \cos\frac{\pi}{8} = 0.92388\ldots$ un $b - c = \cos\frac{3\pi}{8} = 0.38268\ldots$ Matricas $C$ rindas ir ortonormētas ($C C^T = I$), tāpēc apgrieztā transformācija ir $x = C^T y$.

**Piemērs:** Vienmērīgi augošs signāls $x = (10, 20, 30, 40)$:

$$
\begin{array}{rcl}
y_0 & = & a\,(10 + 20 + 30 + 40) = 50, \\
y_1 & = & b\,(10 - 40) + c\,(20 - 30) = -30\,b - 10\,c = -22.304\ldots, \\
y_2 & = & a\,(10 - 20 - 30 + 40) = 0, \\
y_3 & = & c\,(10 - 40) - b\,(20 - 30) = -30\,c + 10\,b = -1.585\ldots
\end{array}
$$

$y_0 = 50$ ir DC koeficients ($2$ reizes lielāks par vidējo $25$), bet gandrīz viss pārējais ir koeficientā $y_1$ -- zemākajā frekvencē. Tā kā $C$ ir ortonormēta, kvadrātu summa nemainās (Parsevāla vienādība): $10^2 + 20^2 + 30^2 + 40^2 = 3000$ un $50^2 + 22.304^2 + 0^2 + 1.585^2 = 3000$ (ar noapaļošanas precizitāti). Gludam signālam "enerģija" koncentrējas pirmajos koeficientos, tāpēc pēdējos var kvantizēt rupji vai atmest (sk. 5.2. uzdevumu).

**Divdimensiju piemērs ($2 \times 2$):** Ja $N = 2$, tad $C = \frac{1}{\sqrt{2}} \left( \begin{array}{rr} 1 & 1 \\ 1 & -1 \end{array} \right)$, un $B = C A C^T$ var uzrakstīt vispārīgi:

$$
A = \left( \begin{array}{cc} p & q \\ r & s \end{array} \right)
\;\;\Rightarrow\;\;
B = \frac{1}{2} \left( \begin{array}{cc}
p + q + r + s & p - q + r - s \\
p + q - r - s & p - q - r + s
\end{array} \right).
$$

$B_{0,0}$ ir summa, $B_{0,1}$ -- starpība starp kreiso un labo kolonnu, $B_{1,0}$ -- starp augšējo un apakšējo rindu, $B_{1,1}$ -- "šaha galdiņa" komponente. Piemēram, $A = \left( \begin{array}{cc} 1 & 3 \\ 5 & 7 \end{array} \right)$ dod $B = \left( \begin{array}{rr} 8 & -2 \\ -4 & 0 \end{array} \right)$.

**Python (bez bibliotēkām).** Formulu var pierakstīt tieši ar *list comprehension*; `dct2` vispirms transformē katru kolonnu, pēc tam katru rindu, t.i., aprēķina $C A C^T$:

```python
from math import cos, pi, sqrt

def dct(x):
    """1D DCT-II (ortonormētā): y[k] = alpha_k * sum x[n] cos(pi (2n+1) k / 2N)."""
    N = len(x)
    return [(sqrt(1 / N) if k == 0 else sqrt(2 / N))
            * sum(xn * cos(pi * (2 * n + 1) * k / (2 * N)) for n, xn in enumerate(x))
            for k in range(N)]

def idct(y):
    """Apgrieztā transformācija: x[n] = sum alpha_k y[k] cos(pi (2n+1) k / 2N)."""
    N = len(y)
    return [sum((sqrt(1 / N) if k == 0 else sqrt(2 / N)) * yk
                * cos(pi * (2 * n + 1) * k / (2 * N)) for k, yk in enumerate(y))
            for n in range(N)]

def dct2(A):
    """2D DCT: vispirms katrai kolonnai, pēc tam katrai rindai (B = C A C^T)."""
    cols = [dct(col) for col in zip(*A)]
    return [dct(row) for row in zip(*cols)]

print([round(v, 3) + 0.0 for v in dct([10, 20, 30, 40])])   # [50.0, -22.304, 0.0, -1.585]
print([round(v, 3) + 0.0 for v in idct(dct([10, 20, 30, 40]))])  # [10.0, 20.0, 30.0, 40.0]
for row in dct2([[0, 0, 8, 8]] * 4):                   # vertikāla robeža 4x4 blokā
    print([round(v, 3) + 0.0 for v in row])
```

Pēdējā piemērā visām bloka rindām ir viena un tā pati vērtību virkne $(0, 0, 8, 8)$ (vertikāla robeža). Tāpēc nenulles ir tikai rezultāta pirmā rinda $(16, -14.782, 0, 6.123)$: blokam ir tikai horizontālas frekvences, bet vertikālo frekvenču nav.

### Ko glabā DCT koeficienti: amplitūda un enerģija

**Koeficienti ir kosinusoīdu amplitūdas.** Tā kā matrica $C$ ir ortonormēta, $x = C^T y$, t.i., signāls ir matricas $C$ rindu (*bāzes vektoru*) lineāra kombinācija:

$$
x = y_0\,c_0 + y_1\,c_1 + \ldots + y_{N-1}\,c_{N-1},
\qquad
c_k[n] = \alpha_k \cos\frac{\pi (2n+1) k}{2N}.
$$

Bāzes vektors $c_k$ ir kosinusoīda, kurai blokā ir $k$ pusviļņi: $c_0$ ir konstante, $c_1$ -- viens pusvilnis (lēna pāreja no viena gala uz otru), $c_{N-1}$ -- straujākās svārstības, kādas var attēlot $N$ punktos. Koeficients $y_k$ norāda, cik daudz šīs kosinusoīdas ir signālā; tās devums $y_k c_k$ svārstās ar amplitūdu $\alpha_k \lvert y_k \rvert$.

<img
  id="dct_bazes_vektori"
  alt="DCT bāzes vektori"
  src="{{ '/lectures/lossy_images_and_audio/figs/dct-basis.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

*DCT-II bāzes vektori $c_0, \ldots, c_7$ ($N = 8$): punkti ir vektora elementi, plānā līnija -- kosinusoīda, no kuras tie ņemti. JPEG $8 \times 8$ blokā divdimensiju bāzes attēli ir $c_u$ un $c_v$ reizinājumi (vertikālā un horizontālā kosinusoīda).*

Piemēram, signālam $x = (10, 20, 30, 40)$ ar $y = (50,\; -22.304,\; 0,\; -1.585)$ ("Skaitlisks piemērs") devumi ir šādi:

| Koeficients | Devums $y_k c_k$ |
| --- | --- |
| $y_0 = 50$ | $(25,\; 25,\; 25,\; 25)$ |
| $y_1 = -22.304$ | $(-14.571,\; -6.036,\; 6.036,\; 14.571)$ |
| $y_2 = 0$ | $(0,\; 0,\; 0,\; 0)$ |
| $y_3 = -1.585$ | $(-0.429,\; 1.036,\; -1.036,\; 0.429)$ |
| **summa** | $(10,\; 20,\; 30,\; 40)$ |

Augošais signāls ir galvenokārt vidējā vērtība plus viens kosinusa pusvilnis; $y_3$ tikai nedaudz "iztaisno" pusviļņa izliekumu līdz taisnei.

**DC koeficients ir vidējā vērtība.** Tā kā $c_0 = \left(\frac{1}{\sqrt{N}}, \ldots, \frac{1}{\sqrt{N}}\right)$, tad $y_0 = \sqrt{N} \cdot \bar{x}$, kur $\bar{x}$ ir signāla vidējā vērtība. Piemērā $y_0 = 2 \cdot 25$; $8 \times 8$ blokā $B_{0,0} = 8 \cdot \bar{A}$ (sk. JPEG 4. soli).

**Enerģija nemainās (Parsevāla vienādība).** Ortonormēta transformācija saglabā vektora garumu, tāpēc

$$
\sum_{n=0}^{N-1} x_n^2 = \sum_{k=0}^{N-1} y_k^2 .
$$

Izdalot ar $N$, iegūst signāla *vidējo kvadrātu* (vidējo jaudu), un tas sadalās divās daļās:

$$
\frac{1}{N} \sum_{n} x_n^2
= \underbrace{\frac{y_0^2}{N}}_{=\ \bar{x}^2}
+ \underbrace{\frac{1}{N} \sum_{k \geq 1} y_k^2}_{=\ \sigma^2},
$$

kur $\sigma^2 = \frac{1}{N} \sum_n (x_n - \bar{x})^2$ ir dispersija. DC koeficients glabā vidējo gaišumu, bet AC koeficienti kopā -- tikai svārstības ap to (kontrastu, faktūru, malas). Piemērā: $\frac{3000}{4} = 750 = 25^2 + 125$; enerģija sadalās tā: $y_0$ -- $83.3\%$, $y_1$ -- $16.6\%$, $y_3$ -- $0.08\%$. Gludam signālam gandrīz visa AC enerģija ir zemajās frekvencēs.

**Atmestie koeficienti nosaka kļūdu.** Ja koeficientus $y$ aizstāj ar citiem $y'$ (atmet, t.i., aizstāj ar $0$, vai kvantizē), tad atjaunotā signāla kļūda ir $x - x' = C^T (y - y')$, un tās kvadrātu summa ir tieši

$$
\sum_n (x_n - x'_n)^2 = \sum_k (y_k - y'_k)^2 .
$$

Tātad *vidējā kvadrātiskā kļūda* (MSE) signālā ir $\frac{1}{N}$ reizes atmesto koeficientu kvadrātu summa, un katrs koeficients kļūdā piedalās neatkarīgi no pārējiem. No tā izriet:

* Labākā aproksimācija ar $M$ koeficientiem ir paturēt $M$ koeficientus ar lielāko $\lvert y_k \rvert$. Piemērā, atmetot $y_3$, $\mathrm{MSE} = 1.585^2 / 4 = 0.63$ (vidēji $\sqrt{0.63} = 0.79$ vienības uz punktu), bet paturot tikai $y_0$, $\mathrm{MSE} = \sigma^2 = 125$ -- signālu aizstāj ar tā vidējo vērtību.
* Kvantizējot ar soli $Q$, katra koeficienta kļūda ir ne lielāka par $Q/2$; ja noapaļošanas kļūda ir vienmērīgi sadalīta, tās vidējais kvadrāts ir $Q^2/12$. Tāpēc iekodētājs kļūdu var novērtēt tieši koeficientos, nepārrēķinot pikseļus, un rupjāka kvantizācija augstajām frekvencēm maksā maz, jo tur koeficienti jau tā ir mazi.
* Attēlu kvalitāti bieži mēra ar PSNR (*peak signal-to-noise ratio*) $= 10 \log_{10} \frac{255^2}{\mathrm{MSE}}$ decibelos; labas kvalitātes JPEG attēliem tas parasti ir $30$--$40$ dB.

## AVIF attēlu formāts

* Izņemot JPEG, ir populārs Google izveidotais formāts WebP, kas labi saspiežams un ir populārs pārlūkprogrammās.
* HEIF/HEIC (High Efficiency Image Format) ir radniecīgs video kodekam H.265; to veicina Apple.
* AVIF ir radniecīgs pazīstamajam atvērtajam video kodekam AV1.
* JPEG XL ir vēl visai jauns formāts (nav sevišķi plaši atbalstīts), bet ar vairākām jaunām iespējām, labu saspiešanu dažādos robežgadījumos un arī pilnu savietojamību ar JPEG.

*AVIF* (*AV1 Image File Format*, Alliance for Open Media, 2019) glabā attēlu kā vienu AV1 video kodeka *intra kadru* -- kadru, ko kodē bez atsaucēm uz citiem kadriem --, ietītu HEIF konteinerā (tas pats konteinera formāts, ko izmanto HEIC faili). Tā kā AV1 ir veidots video saspiešanai, tajā ir daudz vairāk izvēles iespēju nekā JPEG: iekodētājs katram attēla apgabalam meklē izdevīgāko bloku izmēru, prognozes režīmu un transformāciju. Tāpēc AVIF iekodēšana ir daudz lēnāka par JPEG, bet tāda paša izmēra failā kvalitāte ir ievērojami labāka.

### AVIF iekodēšana

Tipisks gadījums: digitāla fotogrāfija, ko saspiež ar zudumiem (piemēram, ar programmu `avifenc` no bibliotēkas *libavif*, kas izmanto AV1 iekodētāju *libaom*, *SVT-AV1* vai *rav1e*).

<img
  id="avif_kodesanas_soli"
  alt="AVIF kodēšanas soļi"
  src="{{ '/lectures/lossy_images_and_audio/figs/avif-pipeline.svg' | relative_url }}"
  style="width: 100%; max-width: 980px; border:none; background-color:#FFFFFF;"
/>

*AVIF kodēšanas soļi; numuri atbilst tālāk uzskaitītajiem soļiem. Pārtrauktā bultiņa rāda, ka nākamo bloku prognozei izmanto jau atjaunotos (atkodētos) pikseļus.*

1. **Krāsu telpas maiņa (RGB $\rightarrow$ YCbCr).** Tāpat kā JPEG, bet koeficientu matrica (piemēram, BT.601 vai BT.709), vērtību diapazons (pilns $0 \ldots 255$ vai ierobežots $16 \ldots 235$) un bitu dziļums ($8$, $10$ vai $12$ biti uz komponenti) ir izvēlami, un izvēli ieraksta failā. $10$ un $12$ bitu attēli ļauj glabāt arī HDR (*high dynamic range*) fotogrāfijas.
2. **Krāsainības izretināšana.** Tāpat kā JPEG: fotogrāfijām parasti 4:2:0; augstas kvalitātes iestatījumos bieži izmanto 4:4:4 (bez izretināšanas).
3. **Sadalīšana superblokos un blokos.** Katru komponenti sadala $64 \times 64$ (vai $128 \times 128$) *superblokos*, un katru superbloku rekursīvi sadala mazākos blokos -- ne tikai četros kvadrātos, bet arī divos vai četros taisnstūros un T veida daļās -- līdz pat $4 \times 4$. Iekodētājs sadalījumu izvēlas, salīdzinot, cik bitu prasa un cik lielu kļūdu dod katrs variants (*rate–distortion optimization*). *Atšķirība no JPEG:* JPEG bloks vienmēr ir $8 \times 8$; AVIF gludos apgabalos (debesis, siena) izmanto lielus blokus, bet detaļās -- mazus.
4. **Intra prognoze.** Katra bloka vērtības paredz no jau iekodētajiem (un atjaunotajiem) kaimiņu pikseļiem virs bloka un pa kreisi no tā. Ir $56$ virziena režīmi (turpina malas un līnijas noteiktā leņķī), DC režīms (vidējā vērtība), gludie režīmi (*smooth*, *Paeth*), krāsainības prognoze no gaišuma (*chroma from luma*, CfL) un palete attēla apgabaliem ar dažām krāsām. Tālāk kodē tikai *atlikumu* -- starpību starp bloku un prognozi. *Atšķirība no JPEG:* JPEG no iepriekšējā bloka paredz tikai DC koeficientu; AV1 paredz visu bloku, tāpēc atlikums parasti ir tuvu nullei.
5. **Atlikuma transformācija.** Atlikumu transformē blokos no $4 \times 4$ līdz $64 \times 64$ (arī taisnstūros). Horizontālajam un vertikālajam virzienam var izvēlēties dažādas 1D transformācijas: DCT, ADST (*asymmetric discrete sine transform* -- piemērota atlikumam, kas aug, attālinoties no bloka malas, no kuras prognozēja), spoguļoto ADST vai identitāti (bez transformācijas). Visas transformācijas rēķina veselos skaitļos, lai iekodētājs un atkodētājs iegūtu precīzi vienādu rezultātu. *Atšķirība no JPEG:* JPEG vienmēr lieto $8 \times 8$ DCT.
6. **Kvantizācija.** Kvantizācijas soli nosaka viens parametrs *qindex* ($0 \ldots 255$; jo lielāks, jo rupjāka kvantizācija un mazāks fails), ar atsevišķām korekcijām DC un AC koeficientiem un katrai komponentei. Soli var mainīt arī pa superblokiem. Noapaļošanas virzienu katram koeficientam iekodētājs var izvēlēties tā, lai ietaupītu bitus (*trellis quantization*). *Atšķirība no JPEG:* JPEG izmanto $8 \times 8$ kvantizācijas tabulu un vienkāršu noapaļošanu.
7. **Atjaunošana un cilpas filtri** (*in-loop filters*). Iekodētājs atjauno attēlu tieši tāpat kā atkodētājs (apgrieztā kvantizācija un transformācija, pieskaita prognozi), jo nākamie bloki jāprognozē no tiem pašiem pikseļiem, kas būs pieejami atkodētājam. Uz atjaunotā attēla piemēro trīs filtrus: *deblocking* (nogludina bloku robežas), CDEF (*constrained directional enhancement filter* -- noņem viļņošanos gar malām, ievērojot malas virzienu) un *loop restoration* (Wiener vai *self-guided* filtrs). Iekodētājs izvēlas filtru parametrus, kas atjaunoto attēlu padara vistuvāko oriģinālam, un ieraksta tos bitu plūsmā. Pēc izvēles var arī noņemt fotogrāfijas graudainību (*film grain*) un nosūtīt tikai tās statistiskos parametrus, lai atkodētājs graudainību uzzīmētu no jauna. *Atšķirība no JPEG:* JPEG filtru nav, tāpēc zemā kvalitātē redzamas $8 \times 8$ bloku robežas.
8. **Entropijas kodēšana.** Visus lēmumus (bloku sadalījumu, prognozes režīmus, transformāciju tipus, filtru parametrus) un kvantizētos koeficientus kodē ar adaptīvu aritmētisko kodu, kura simboliem ir līdz $16$ vērtībām. Varbūtību sadalījumi pielāgojas pēc katra simbola, un tie atkarīgi no konteksta (piemēram, no kaimiņu bloku koeficientiem). Rezultāts ir AV1 bitu plūsma, kas sastāv no OBU (*open bitstream unit*) vienībām: secības galvenes un kadra datiem. *Atšķirība no JPEG:* JPEG izmanto Hafmana kodu, kura tabulas visā attēlā nemainās un kurš katram simbolam tērē vismaz $1$ bitu.
9. **Konteiners.** AV1 datus ieliek HEIF (ISO bāzes mediju faila) konteinerā, kas sastāv no "kastēm" (*boxes*): `ftyp` (faila tips `avif`), `meta` (attēla izmēri, AV1 konfigurācija `av1C`, krāsu telpa `colr`, bitu dziļums) un `mdat` (paši AV1 dati). Tajā pašā failā var glabāt arī caurspīdīguma kanālu (kā otru AV1 attēlu), Exif metadatus un attēlu virknes (animāciju).

**Atkodēšana** izpilda soļus pretējā secībā: nolasa konteineru un AV1 datus, aritmētiski atkodē, katram blokam aprēķina prognozi, pieskaita apgriezti transformēto atlikumu, piemēro cilpas filtrus un pārveido YCbCr $\rightarrow$ RGB. Atkodētājam nav jāmeklē labākie režīmi (tie ir ierakstīti failā), tāpēc atkodēšana ir daudz ātrāka par iekodēšanu.

### Animēta AVIF faila piemērs

AVIF var glabāt arī attēlu virkni (animāciju) -- tad tie ir vairāki AV1 kadri, kurus var kodēt arī ar atsaucēm uz iepriekšējiem kadriem, tāpat kā video. Šī animācija ir izveidota ar Python skriptu [animated_avif.py]({{ '/lectures/lossy_images_and_audio/figs/animated_avif.py' | relative_url }}), kas izmanto bibliotēkas Pillow un NumPy:

<img
  id="animets_avif"
  alt="Animēts AVIF: bumba atstarojas no taisnstūra malām"
  src="{{ '/lectures/lossy_images_and_audio/figs/bouncing-ball.avif' | relative_url }}"
  style="width: 100%; max-width: 640px; border:none; background-color:#F4F1E8;"
/>

*Bumba pārvietojas $45^\circ$ leņķī un atstarojas no malām. $280$ kadri ($640 \times 360$ pikseļi, $50$ kadri sekundē, $5.6$ sekundes) aizņem apmēram $12$ KB.*

* Bumbas malas pikseļu krāsa ir fona un bumbas krāsu sajaukums proporcionāli tam, kāda pikseļa daļa ir bumbas iekšpusē (*anti-aliasing*; katru pikseli sadala $4 \times 4$ apakšpikseļos). Tāpēc bumba izskatās apaļa, un kustība ir gluda arī tad, ja bumbas centrs neatrodas pikseļa centrā.
* Izmēri izvēlēti tā, lai animācija būtu bezšuvju cilpa: bumbas centrs pārvietojas $560$ pikseļus horizontāli un $280$ pikseļus vertikāli, tāpēc pēc $2 \cdot 560 = 1120$ pikseļu ceļa (pa $4$ pikseļiem kadrā) bumba atgriežas sākuma stāvoklī.
* Kadrus saglabā ar `Image.save(..., format="AVIF", save_all=True, append_images=...)`; jaunākās Pillow versijās AVIF atbalsts ir iebūvēts.

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

**Laboratorijas darbs:** [Apzināti sabojājam JPEG]({{ '/lectures/lossy_images_and_audio/jpeg_lab/' | relative_url }}) -- ar Python programmu soli pa solim saspiežam attēlu "gandrīz kā JPEG", mainot krāsu telpu, bloku izmēru, kvantizāciju un transformāciju, un skaidrojam, kas notiek ar attēlu.

**5.1. uzdevums:** Izmantojam krāsu saspiešanai kvantizācijas algoritmu, kas lieto tikai pārlūkprogrammām draudzīgās krāsas: [Web Safe Color palette](https://www.rapidtables.com/web/color/Web_Safe.html) jeb 6x6x6 krāsu kubu. 

* Pārlūkprogrammām draudzīgas ir tās krāsu koordinātes, kam abi hex cipariņi ir vienādi un dalās ar $3$ ($00,33,66,99,\text{CC},\text{FF}$). Ja krāsai visas 3 koordinātes ir draudzīgas, tad arī pati krāsa ir draudzīga. Teiksim, `00FF99` ir draudzīga krāsa, bet `22BB99` nav, jo "22" un "BB" koordinātes nav atļautas.
* Katru attēlā esošo pikseli (katru no RGB koordinātēm) noapaļo līdz tuvākajai draudzīgajai no kopas ($00,33,66,99,\text{CC},\text{FF}$), lai iegūtu pārlūkprogrammai draudzīgu krāsu.

Kāds ir saspiešanas koeficients šādam pārveidojumam (jaunais izmērs pret veco izmēru)?

*Piezīme:* Mūsdienu pārlūkprogrammas var attēlot jebkādas RGB krāsas; šim 6x6x6 krāsu kubam ir drīzāk vēsturiska nozīme: 
Daudzās agrīnās lietojumprogrammās krāsu pikseļa vērtību izteica ar 1 baitu (256 dažādas vērtības, kurām lietotājs varēja 
piekārtot faktiskās krāsas, izmantojot paleti). Šajā paletē bieži $6^3 = 216$ vērtības tika rezervētas "drošajām krāsām",
kuras (neatkarīgi no pārējā paletes aizpildījuma) attēlojās vienādi. 

**5.2. uzdevums:** Dots signāls $x = (8, 8, 0, 0)$ (pakāpiens). Izmantojiet DCT ar $N = 4$ (sk. "Skaitlisks piemērs: DCT ar $N = 4$").

* **(a)** Aprēķiniet $y = C x$. Izsakiet koeficientus ar $\cos\frac{\pi}{8}$ un $\cos\frac{3\pi}{8}$ un pēc tam aprēķiniet to vērtības.
* **(b)** Pārbaudiet, ka $\sum x_n^2 = \sum y_k^2$.
* **(c)** Vienkāršākā "saspiešana": atmetam augstāko frekvenci, t.i., aizstājam $y_3$ ar $0$. Aprēķiniet atjaunoto signālu $x' = C^T y'$, kur $y' = (y_0, y_1, y_2, 0)$. Cik liela ir kvadrātiskā kļūda $\sum (x_n - x'_n)^2$ un kāpēc tā sakrīt ar $y_3^2$?

**Atbilde:**

**(a)** No matricas $C$ rindām:

$$
\begin{array}{rcl}
y_0 & = & a\,(8 + 8 + 0 + 0) = 8, \\
y_1 & = & 8\,b + 8\,c = 8\,(b + c) = 8 \cos\frac{\pi}{8} = 7.391\ldots, \\
y_2 & = & a\,(8 - 8 - 0 + 0) = 0, \\
y_3 & = & 8\,c - 8\,b = -8\,(b - c) = -8 \cos\frac{3\pi}{8} = -3.061\ldots
\end{array}
$$

**(b)** $\sum x_n^2 = 64 + 64 = 128$. $\sum y_k^2 = 64 + 64 \cos^2\frac{\pi}{8} + 64 \cos^2\frac{3\pi}{8} = 64 + 64 = 128$, jo $\cos\frac{3\pi}{8} = \sin\frac{\pi}{8}$.

**(c)** $x' = C^T y'$, t.i., $x'_n = a\,y_0 + C_{1,n}\,y_1$ (jo $y_2 = 0$ un $y'_3 = 0$):

$$
\begin{array}{rcl}
x'_0 & = & 4 + b \cdot 8 \cos\frac{\pi}{8} = 4 + 4 \cos^2\frac{\pi}{8} \cdot \sqrt{2} = 6 + 2\sqrt{2} = 8.828\ldots, \\
x'_1 & = & 4 + c \cdot 8 \cos\frac{\pi}{8} = 6, \\
x'_2 & = & 4 - c \cdot 8 \cos\frac{\pi}{8} = 2, \\
x'_3 & = & 4 - b \cdot 8 \cos\frac{\pi}{8} = 2 - 2\sqrt{2} = -0.828\ldots
\end{array}
$$

(Izmantojam $b \cos\frac{\pi}{8} = \frac{1}{\sqrt{2}} \cos^2\frac{\pi}{8} = \frac{2 + \sqrt{2}}{4\sqrt{2}}$ un $c \cos\frac{\pi}{8} = \frac{1}{\sqrt{2}} \cos\frac{3\pi}{8} \cos\frac{\pi}{8} = \frac{1}{4}$.)

Atjaunotais signāls $(8.83,\; 6,\; 2,\; -0.83)$ ir "izplūdis" pakāpiens, kas pie malām pārlec pāri sākotnējām vērtībām -- tāds pats efekts JPEG attēlos rada viļņošanos ap asām malām (*ringing*). Kļūda ir $x - x' = (-0.83,\; 2,\; -2,\; 0.83)$, un $\sum (x_n - x'_n)^2 = 2 \cdot (2\sqrt{2} - 2)^2 + 2 \cdot 2^2 = 32 - 16\sqrt{2} = 9.37\ldots$ Tā sakrīt ar $y_3^2 = 64 \cos^2\frac{3\pi}{8} = 32 - 16\sqrt{2}$, jo $x - x' = C^T (y - y')$ un ortonormēta transformācija saglabā kvadrātu summu: atmesta koeficienta kvadrāts ir tieši kvadrātiskā kļūda. $\square$

## Izmantotā literatūra

1. [The MP3 is dead, say creators after terminating licensing](https://www.cnbc.com/2017/05/15/mp3-dead-say-creators-after-terminating-licensing.html) -- par audioformātu attīstību.
2. [Ungārijas 2018.g. vēlēšanas](https://en.wikipedia.org/wiki/2018_Hungarian_parliamentary_election) -- kā Donta metode palīdz noapaļot rezultātus par labu lielākajai partijai.
3. [The Theory Behind Mp3](http://www.mp3-tech.org/programmer/docs/mp3_theory.pdf) -- galvenās idejas audiofailu saspiešanai.
