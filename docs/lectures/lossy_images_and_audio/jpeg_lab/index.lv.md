---
layout: default
title: "Laboratorijas darbs: Apzināti sabojājam JPEG"
lang: lv
permalink: /lectures/lossy_images_and_audio/jpeg_lab/index.lv.html

docx_header: "Laboratorijas darbs: Apzināti sabojājam JPEG"
docx_footer: "LU Algoritmi telekomunikācijās un drošības risinājumos: 5. Zudumradošā saspiešana: attēli un audio"
docx_font: "Calibri"
docx_fontsize: 10
docx_heading_font: "Calibri Light"
docx_heading_color: "2F5496"
docx_heading1_size: 14
geometry: "a4paper, top=2.54cm, bottom=2.54cm, left=2.54cm, right=2.54cm"
---
# Laboratorijas darbs: Apzināti sabojājam JPEG

Šis ir datorlaboratorijas darbs lekcijai
[5. Zudumradošā saspiešana: attēli un audio](../).
Katrs JPEG solis ir vajadzīgs kāda iemesla dēļ. Šajā darbā jūs pa vienam mainīsiet vai izņemsiet
soļus, aplūkosiet atkodēto attēlu un paskaidrosiet, kas nogāja greizi.

## Faili

* <a href="{{ '/lectures/lossy_images_and_audio/jpeg_lab/jpeg_lab.py' | relative_url }}" download>jpeg_lab.py</a>:
  JPEG līdzīgs kodētājs un atkodētājs ar komandrindas parametriem katram solim (Python 3, vajag `numpy` un `Pillow`).
* Testa attēli (labais klikšķis un "Saglabāt saiti kā..."):
  * <a href="{{ '/lectures/lossy_images_and_audio/figs/bumblebee.png' | relative_url }}" download>bumblebee.png</a>:
    fotogrāfija, $400 \times 300$ pikseļi.
  * <a href="{{ '/lectures/lossy_images_and_audio/figs/kuldiga1.png' | relative_url }}" download>kuldiga1.png</a>:
    fotogrāfija, $600 \times 450$ pikseļi.
  * <a href="{{ '/lectures/lossy_images_and_audio/figs/mandelbrot-picture.png' | relative_url }}" download>mandelbrot-picture.png</a>:
    datorā ģenerēts attēls ar piesātinātām krāsām un asām malām, $850 \times 850$ pikseļi.
  * <a href="{{ '/lectures/lossy_images_and_audio/jpeg_lab/test-chart.png' | relative_url }}" download>test-chart.png</a>:
    sintētiska testa tabula ar krāsu joslām, krāsainu tekstu, plānām līnijām un šaha galdiņu, $512 \times 384$ pikseļi.
    To uzzīmēja programma <a href="{{ '/lectures/lossy_images_and_audio/jpeg_lab/make_test_chart.py' | relative_url }}" download>make_test_chart.py</a>.
* Var izmantot arī savus attēlus. Nelielus attēlus (līdz apmēram $1000 \times 1000$ pikseļiem) ir vieglāk
  salīdzināt blakus, un tos apstrādā apmēram sekundē.

```bash
pip install numpy pillow
python jpeg_lab.py bumblebee.png out.png
python jpeg_lab.py --help
```

PNG izmanto tikai RGB pikseļu glabāšanai. `jpeg_lab.py` neveido `.jpg` failu.
Tā izpilda JPEG soļus ar pikseļiem, uzreiz atkodē rezultātu un saglabā
atkodētos pikseļus kā PNG attēlu. Programma arī izdrukā:

* katra krāsu kanāla kļūdu: vidējo kvadrātisko kļūdu (MSE) un
  $\mathrm{PSNR} = 10 \log_{10} \frac{255^2}{\mathrm{MSE}}$ decibelos (jo vairāk, jo labāk; ja vairāk par
  apmēram $40$ dB, kļūdu grūti saskatīt);
* nenulles kvantizēto koeficientu skaitu;
* novērtēto saspiestā faila izmēru. Koeficientus pārvērš *baseline* JPEG
  simbolos (DC starpības, pāri $(\mathrm{RUN}, \mathrm{SIZE})$, ZRL, EOB), un simbolu entropijai
  pieskaita papildu bitu skaitu. Ar noklusētajiem iestatījumiem novērtējums
  atšķiras ne vairāk kā par apmēram $5\%$ no tādas pašas kvalitātes īsta JPEG faila izmēra, kas izmanto optimizētas
  Hafmana tabulas (galvenes neskaitot). Ar standarta pielikuma K Hafmana tabulām īsti faili ir
  lielāki, it īpaši sintētiskiem attēliem, piemēram, `test-chart.png`.

Divas papildu izvades palīdz saprast, kas notika:

* `--difference-png diff.png` ieraksta kļūdu attēlu: pelēks ($128$) nozīmē, ka kļūdas nav, bet gaišāki
  un tumšāki pikseļi -- ka atkodētā vērtība ir par lielu vai par mazu (kļūdu pareizina ar
  `--difference-amplification`, noklusēti $4$).
* `--planes-png planes.png` ieraksta trīs krāsu plaknes (piemēram, $Y$, $\mathrm{Cb}$, $\mathrm{Cr}$) kā pelēktoņu
  attēlus: sākotnējās plaknes augšējā rindā un atkodētās plaknes apakšējā rindā.

Vienmēr salīdziniet izmainītu palaidienu ar noklusēto palaidienu (`python jpeg_lab.py image.png default.png`)
un, ja iespējams, pie vienāda novērtētā izmēra. Labāku attēlu ir viegli iegūt, iztērējot
vairāk bitu.

## Kā programma ir veidota

Pirmkods seko lekcijas JPEG soļiem. Lai mainītu kādu soli, atrodiet tā sadaļu
failā; katrs tālāk minētais parametrs tiek glabāts `settings.<name>` (piemēram, `--block-size` ir
`settings.block_size`).

| Solis | Funkcijas | Parametri |
| --- | --- | --- |
| Pikseļu nolasīšana | `load_rgb_pixels` | `input_png` |
| 1. Krāsu telpas maiņa | `rgb_to_planes`, `planes_to_rgb` | `--color-space {ycbcr,yiq,rgb}` |
| 2. Krāsainības izretināšana | `subsample`, `upsample` | `--chroma-subsampling {4:4:4,4:2:2,4:2:0,4:1:1}` |
| 3. Bloki un līmeņa nobīde | `pad_to_multiple`, `split_into_blocks`, `merge_blocks` | `--block-size`, `--no-level-shift` |
| 4. Transformācija | `dct_matrix`, `dst7_matrix`, `hartley_matrix`, `walsh_hadamard_matrix`, `haar_matrix`, `klt_matrix` | `--transform` |
| 4b. Koeficientu atlase (JPEG tās nav) | `drop_high_frequencies`, `scale_up_kept_coefficients`, `fill_dropped_with_noise` | `--keep-coefficients`, `--energy-compensation {none,scale,noise}` |
| 5. Kvantizācija | `make_quantization_tables`, `scale_table_by_quality`, `quantize`, `dequantize` | `--quality`, `--quant-table`, `--flat-step`, `--luma-quant-multiplier`, `--chroma-quant-multiplier`, `--rounding` |
| 6.-7. Zig-zag, sēriju kodēšana, izmērs | `zigzag_order`, `estimate_plane_bits` | nav |
| Atkodētājs: bloku robežu gludināšana (JPEG tās nav) | `deblock` | `--deblocking-filter`, `--deblocking-threshold` |

Dažas detaļas:

* Katra transformācija ir ortonormēta $N \times N$ matrica $T$. Bloku $A$ pārveido par
  $B = T A T^T$ un atjauno kā $A = T^T B T$. DCT gadījumā $T$ ir lekcijas matrica $C$.
* Ja bloka izmērs nav $8$, tad $8 \times 8$ kvantizācijas tabulas izstiepj: $N \times N$ bloka
  koeficients $(u, v)$ saņem tabulas elementu
  $Q_{\lfloor 8u/N \rfloor, \lfloor 8v/N \rfloor}$.
* `--quality` mērogo tabulas tāpat kā *libjpeg* (sk. lekcijas 5. soli). Pēc tam
  `--luma-quant-multiplier` pareizina pirmās plaknes tabulu, bet `--chroma-quant-multiplier`
  pareizina otrās un trešās plaknes tabulu.
* Atkodētājs palielina krāsainības izšķirtspēju, atkārtojot paraugus. Īsti atkodētāji bieži interpolē, tāpēc
  to attēli izskatās nedaudz gludāki.

## 1. uzdevums: Bez krāsu telpas maiņas

Ar `--color-space rgb` programma izlaiž 1. soli: $R$ kodē tā, it kā tas būtu $Y$, $G$ -- kā $\mathrm{Cb}$,
bet $B$ -- kā $\mathrm{Cr}$. Tātad $G$ un $B$ tiek izretināti un kvantizēti ar krāsainības tabulu, kas ir rupjāka.

```bash
python jpeg_lab.py bumblebee.png ycbcr.png
python jpeg_lab.py bumblebee.png rgb.png --color-space rgb
python jpeg_lab.py test-chart.png chart-ycbcr.png --planes-png chart-ycbcr-planes.png
python jpeg_lab.py test-chart.png chart-rgb.png --color-space rgb
```

1. Salīdziniet attēlus, PSNR un novērtēto izmēru. Kurš attēls ir vairāk izplūdis, un kāpēc?
   Atcerieties, kuram no $R$, $G$, $B$ ir lielākais svars formulā $Y = 0.299 R + 0.587 G + 0.114 B$.
2. Aplūkojiet `test-chart.png` vertikālās melnās līnijas abos rezultātos. No kurienes rodas
   krāsa, kas parādās failā `chart-rgb.png`?
3. Tagad izslēdziet izretināšanu un izmantojiet vienu un to pašu tabulu visām trim plaknēm, lai
   atšķirtos tikai krāsu telpa:
   ```bash
   python jpeg_lab.py test-chart.png a.png --chroma-subsampling 4:4:4 --quant-table luma-for-all
   python jpeg_lab.py test-chart.png b.png --chroma-subsampling 4:4:4 --quant-table luma-for-all --color-space rgb
   ```
   Kurš ir mazāks? Aplūkojiet abu palaidienu `--planes-png`. Kāpēc tipiskas fotogrāfijas $\mathrm{Cb}$ un
   $\mathrm{Cr}$ plaknes saspiežas tik labi, bet $G$ un $B$ plaknes -- nē?
4. Kvantizējiet otro un trešo plakni agresīvāk. Divkāršojiet krāsainības tabulu
   (`--chroma-quant-multiplier 2`), tad izmēģiniet $4$ un $8$. Dariet to abās krāsu telpās
   (ar `--chroma-subsampling 4:4:4`):
   ```bash
   python jpeg_lab.py bumblebee.png c.png --chroma-subsampling 4:4:4 --chroma-quant-multiplier 4
   python jpeg_lab.py bumblebee.png d.png --chroma-subsampling 4:4:4 --chroma-quant-multiplier 4 --color-space rgb
   ```
   Kurā krāsu telpā krāsainības plaknes var kvantizēt rupji bez redzamiem bojājumiem?
   Kāda veida kļūda rodas RGB telpā: nepareizs gaišums vai nepareiza krāsa?
5. Atkārtojiet 1. punktu ar `--color-space yiq`. Vai starp YIQ un YCbCr ir jūtama atšķirība? Kāpēc
   (sk. lekciju: kā saistītas $IQ$ un $UV$ plaknes)?

## 2. uzdevums: Lieli bloki un bloku artefakti

```bash
python jpeg_lab.py bumblebee.png b8.png  --quality 10
python jpeg_lab.py bumblebee.png b32.png --quality 10 --block-size 32
python jpeg_lab.py bumblebee.png b32-deblocked.png --quality 10 --block-size 32 --deblocking-filter
```

1. Zemā kvalitātē katrā blokā paliek tikai daži koeficienti. Tas pats attiecas uz vidējo
   gaišumu un lēzenu slīpumu bloka iekšpusē. Kāpēc tie nesakrīt kaimiņu bloku robežās?
   Kāpēc režģis ir daudz labāk redzams ar $32 \times 32$ blokiem nekā ar $8 \times 8$ blokiem?
   Izmēģiniet arī `--quality 5`.
2. Atrodiet asu malu (lapu vai zieda ziedlapiņu) un aplūkojiet viļņošanos (*ringing*) blakus tai. Cik tālu
   no malas viļņošanās izplatās ar $8 \times 8$ blokiem un ar $32 \times 32$ blokiem? Ko tas
   pasaka par bloka izmēra izvēli (salīdziniet ar AVIF adaptīvajiem bloku izmēriem lekcijā)?
3. Bloku robežu gludināšanas filtrs (*deblocking*, funkcija `deblock`) aplūko trīs pikseļus katrā bloka
   robežas pusē. Ja lēciens pāri robežai ir mazāks par `--deblocking-threshold` un abas puses
   ir gludas, lēcienu aizstāj ar lineāru pāreju. Izmēģiniet sliekšņus $10$, $24$, $60$, $200$.
   Kas notiek ar attēla īstajām malām, ja slieksnis ir par lielu? Kāpēc
   filtrs nevar pilnībā noņemt režģi?
4. Transformācijas dēļ kļūdas var koncentrēties arī *blakus* bloku robežām.
   Salīdziniet kļūdu attēlus:
   ```bash
   python jpeg_lab.py bumblebee.png dct16.png     --block-size 16 --difference-png dct16-diff.png
   python jpeg_lab.py bumblebee.png hartley16.png --block-size 16 --transform hartley --difference-png hartley16-diff.png
   python jpeg_lab.py bumblebee.png dst16.png     --block-size 16 --transform dst7 --difference-png dst16-diff.png
   ```
   Hārtlija transformācija (diskrētās Furjē transformācijas reālā versija) bloku uzskata par
   periodiska signāla vienu periodu, tāpēc bloka kreisā mala "turpinās" tā labajā malā.
   DCT uzvedas tā, it kā bloks būtu turpināts ar savu spoguļattēlu. DST-VII pieņem, ka
   signāls tieši pirms augšējās/kreisās malas ir $0$. Katrai transformācijai uzzīmējiet
   bloka vienu rindu (1D) kopā ar pieņemto turpinājumu un paskaidrojiet, kur turpinājumam ir lēciens.
   Kur kļūdu attēlos ir lielākās kļūdas?

## 3. uzdevums: Paturam tikai zemās frekvences

`--keep-coefficients K` katrā blokā patur tikai augšējo kreiso $K \times K$ stūri (DC
koeficientu un zemākās frekvences), bet pārējos koeficientus aizstāj ar $0$. Izmantojiet augstu
kvalitāti, lai kļūdu radītu koeficientu atmešana, nevis kvantizācija.

```bash
python jpeg_lab.py bumblebee.png keep3.png --keep-coefficients 3 --quality 90
python jpeg_lab.py test-chart.png chart-keep3.png --keep-coefficients 3 --quality 90
```

1. No $64$ koeficientiem paliek $9$. Kāda ir rezultāta izšķirtspēja, mērot "detaļās uz
   bloku"? Kuras testa tabulas daļas tiek pilnībā iznīcinātas, un kuras saglabājas?
   Izmēģiniet $K = 1, 2, 4, 6$.
2. Pēc Parsevāla vienādības (sk. lekciju) bloka kvadrātiskā kļūda ir tieši atmesto koeficientu
   kvadrātu summa. Ja $K = 3$, salīdziniet PSNR ar noklusēto palaidienu pie tā paša novērtētā izmēra
   (pielāgojiet noklusētā palaidiena `--quality`). Kurš attēls izskatās labāk? Ko tas pasaka par
   koeficientu atmešanu pēc pozīcijas, salīdzinot ar to kvantizēšanu pēc lieluma?
3. Tagad kompensējiet zaudēto enerģiju. Ar `--energy-compensation scale` kodētājs pareizina
   katra bloka paturētos AC koeficientus ar tādu reizinātāju, lai bloka enerģija
   (kvadrātu summa) nemainītos. Ar `--energy-compensation noise` atkodētājs aizpilda
   atmestās pozīcijas ar gadījuma skaitļiem, kuru kopējā enerģija ir tāda pati ("trokšņa aizpildīšana",
   *noise filling*; kodētājs katram blokam nosūta vienu skaitli -- atmesto enerģiju).
   ```bash
   python jpeg_lab.py bumblebee.png keep3-scale.png --keep-coefficients 3 --quality 90 --energy-compensation scale
   python jpeg_lab.py bumblebee.png keep3-noise.png --keep-coefficients 3 --quality 90 --energy-compensation noise
   python jpeg_lab.py test-chart.png chart-keep3-noise.png --keep-coefficients 3 --quality 90 --energy-compensation noise
   ```
   Abiem attēliem ir pareiza enerģija, bet PSNR kļūst *sliktāks*. Kāpēc? Vai kāds no attēliem izskatās
   asāks? Kur troksnis palīdz (zāle, lapas) un kur tas kaitē (vienmērīgi apgabali, līnijas, teksts)?
4. Audio kodeki (AAC, Opus) augstajām frekvencēm izmanto trokšņa aizpildīšanu, bet attēlu kodeki malām to
   gandrīz nekad neizmanto. AV1 un AVIF no jauna sintezē tikai fotogrāfijas graudainību (*film grain*).
   Paskaidrojiet, kāpēc šī ideja labāk der šņākoņai un graudainībai nekā līnijām un tekstam.

## 4. uzdevums: Kāpēc tieši šādas detaļas? Noapaļošana, tabula un līmeņa nobīde

Katrs punkts maina vienu nelielu 3.-5. soļa detaļu.

**(a) Noapaļošana.** JPEG noapaļo $B_{u,v} / Q_{u,v}$ līdz *tuvākajam* veselajam skaitlim.

```bash
python jpeg_lab.py bumblebee.png floor.png --rounding floor
python jpeg_lab.py bumblebee.png trunc.png --rounding toward-zero
```

1. Ar `floor` attēls tiek sabojāts un izmērs palielinās, lai gan mainīta tikai noapaļošana.
   Paskaidrojiet, kas notiek ar nelielu negatīvu koeficientu, piemēram, $B/Q = -0.1$.
   Cik ir nenulles koeficientu, salīdzinot ar noklusēto palaidienu?
2. Ar `toward-zero` (atmetot daļu aiz komata) attēls ir tikai nedaudz sliktāks, bet izmērs
   ir mazāks. Salīdziniet to ar noklusēto palaidienu pie *tāda paša* izmēra (zemāka noklusētā palaidiena
   `--quality`). Īsti kodētāji dažkārt apzināti noapaļo mazas vērtības uz nulles pusi (*dead zone*)
   vai izvēlas noapaļošanas virzienu katram koeficientam atsevišķi (*trellis quantization* AVIF formātā).
   Kāpēc tas var būt labs kompromiss?

**(b) Kvantizācijas tabulas forma.** Standarta tabulā zemajām frekvencēm ir mazi soļi, bet
augstajām frekvencēm -- lieli.

```bash
python jpeg_lab.py bumblebee.png flat.png --quant-table flat --flat-step 30
```

Atrodiet tādas `--flat-step` un `--quality` vērtības, lai palaidienam ar vienmērīgo tabulu un palaidienam ar
standarta tabulu būtu vienāds novērtētais izmērs. Salīdziniet PSNR un salīdziniet attēlus. Vai augstāks PSNR arī
izskatās labāk? Kāda veida kļūdu acs pamana vispirms: troksni smalkā faktūrā vai kļūdas lielos vienmērīgos
apgabalos?

**(c) Līmeņa nobīde.** JPEG pirms DCT no katra parauga atņem $128$.

```bash
python jpeg_lab.py bumblebee.png no-shift.png --no-level-shift
```

Rezultāts ir gandrīz identisks. Parādiet, ka ortonormētai transformācijai, kuras pirmā bāzes funkcija ir
konstante, $128$ atņemšana maina tikai DC koeficientu (par cik, ja $N = 8$?). Kāpēc standarts
to tomēr dara? Norāde: $B_{0,0}$ vērtību diapazons un tas, ka DC vērtības kodē kā starpības.

**(d) Bez transformācijas.** `--transform identity` kvantizē pašus pikseļus
("koeficienti" ir pikseļu vērtības).

```bash
python jpeg_lab.py bumblebee.png identity.png --transform identity
python jpeg_lab.py bumblebee.png identity-flat.png --transform identity --quant-table flat --flat-step 40
```

Paskaidrojiet rakstu pirmajā attēlā (kuru tabulas elementu izmanto kuram pikselim?). Otrajā
attēlā katru pikseli vienkārši noapaļo līdz $40$ daudzkārtnim. Kāpēc tas ir lielāks *un* sliktāks par noklusēto palaidienu?
Ko dara transformācija, ko nevar izdarīt, kvantizējot pikseļus?

## 5. uzdevums: Citas ortogonālas transformācijas

Aizstājiet DCT ar citām ortonormētām bāzēm. Visas tās izmanto praksē:

| `--transform` | Bāzes funkcijas | Kur izmanto |
| --- | --- | --- |
| `dct` | kosinusi (DCT-II) | JPEG, MPEG-2, H.264/H.265 (veselo skaitļu tuvinājumi), AV1 |
| `dst7` | sinusi, $0$ pie augšējās/kreisās malas (DST-VII) | H.265 $4 \times 4$ intra gaišuma bloki, AV1 (ADST) |
| `hartley` | $\cos + \sin$ (reāla DFT) | spektrālā analīze; tuvs FFT radinieks |
| `walsh-hadamard` | tikai $+1$ un $-1$ (sakārtotas pēc zīmes maiņu skaita) | H.264 (DC koeficienti), video kodētāji izmaksu novērtēšanai (SATD), CDMA kodi |
| `haar` | īsi pakāpieni dažādos mērogos (vienkāršākais vilnītis) | attēlu kodēšana ar vilnīšiem (JPEG 2000 visam attēlam izmanto gludākus vilnīšus) |
| `klt` | *šī* attēla pikseļu korelācijas matricas īpašvektori (PCA) | teorētiskais optimums; seju atpazīšana ("eigenfaces"), datu analīze |
| `identity` | atsevišķi pikseļi | bez transformācijas (sk. 4d) |

```bash
python jpeg_lab.py bumblebee.png t.png --transform walsh-hadamard --print-tables --difference-png t-diff.png
```

1. Katrai transformācijai pierakstiet PSNR, nenulles koeficientu skaitu un izmēru. Ierakstiet
   tos tabulā un sakārtojiet pēc izmēra. Izmantojiet vismaz divus attēlus (fotogrāfiju un `test-chart.png`).
2. Aplūkojiet `walsh-hadamard` un `haar` attēlus. Kāda ir tipiskā artefaktu forma,
   un kā tā izriet no bāzes funkciju formas (izmantojiet `--print-tables`, lai redzētu
   matricas rindas)?
3. `klt` aprēķina labāko ortonormēto transformāciju dotā attēla rindām un kolonnām. Salīdziniet tās
   izdrukāto matricu (`--block-size 4 --transform klt --print-tables`) ar lekcijas DCT matricu, ja $N = 4$.
   Ko jūs pamanāt? Kāpēc tas izskaidro, ka JPEG izmanto fiksētu DCT un
   nesūta katram attēlam savu KLT matricu?
4. Kvantizācijas tabula ir veidota DCT koeficientiem. Vai salīdzinājums ir godīgs pret citām
   transformācijām? Atkārtojiet salīdzinājumu ar `--quant-table flat` pie vienāda izmēra.
5. *(Neobligāti, programmēšana.)* Pievienojiet funkcijai `transform_matrix` savu transformāciju (piemēram, DCT-IV
   vai līdz veseliem skaitļiem noapaļotu DCT kā H.264, pēc tam normētu). Pārbaudiet, ka `T @ T.T` ir vienības matrica.

## 6. uzdevums (neobligāts): Jūsu pašu modifikācija

Izmainiet kodu vienā vietā un pirms palaišanas paredziet rezultātu. Dažas idejas:

* Pārraidiet *zig-zag* secību apgrieztā virzienā vai izmantojiet secību pa rindām. `estimate_plane_bits` izmanto
  `zigzag_order`. Vai novērtētais izmērs mainās? Kāpēc?
* Funkcijā `quantize` pirms noapaļošanas pieskaitiet gadījuma troksni (*dithering*). Vai tas palīdz
  pret 2. uzdevuma režģi?
* Palieliniet krāsainības izšķirtspēju ar lineāru interpolāciju, nevis atkārtošanu (funkcija `upsample`).
* Rupji kvantizējiet tikai katru otro bloku. Vai redzat šaha galdiņu?

Katru eksperimentu apkopojiet divos vai trijos teikumos: ko jūs mainījāt, ko gaidījāt, ko redzējāt
un kurš īstā JPEG solis novērš šo problēmu.
