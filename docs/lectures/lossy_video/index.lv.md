---
layout: default
title: "Video saspiešana"
lang: lv
permalink: /lectures/lossy_video/index.lv.html
---
# 6. Video saspiešana

Video satura saspiešanai nepieciešami divi kodeki -- audio un video. Daži kodeki ir pietiekami plaši sastopami kā standarti, ietver mūsdienīgas idejas (labu līdzsvaru starp saspiešanas ātrumu, faila izmēru un kvalitāti), ir atskaņojami Web pārlūkos un dažādās citās vidēs un arī rediģējami ar Open Source programmatūru.

Mūsu kursā tie būs **AV1** video saturam un **Opus** audio saturam. Agrākajās desmitgadēs bija citi populāri standarti - H.264 (video) un MP3 (audio); jau tajos parādījās visas svarīgākās saspiešanas idejas un tie izplatījās pateicoties Napster un BitTorrent failu apmaiņas kustībām.

Filmas parasti atskaņo no viena konteinera faila, kurā audio un video plūsmas tiek *multipleksētas*. Tipiski konteineru standarti, kurus apskatīsim ir **MKV (Matroska)** atskaņošanai, piemēram, ar VLC. Un arī **WebM** -- atskaņošanai pārlūkprogrammās.

## Redzes sajūta, HVS modelis

*Human Visual System* (HVS) Model - attēlu un audio apstrādei izveidots vidējots cilvēka redzes modelis.

Redzes uztveri veido nūjiņas un konusiņi; modelis pieņem, ka nūjiņu izšķirtspēja ir divreiz labāka. Tāpēc melnbaltajai attēla komponentei (gaismas intensitātei, neatkarīgi no krāsas) jādod precīzs attēls; krāsas toties drīkst būt ar zemāku izšķirtspēju.

Krāsu televīzijas rītausmā bija teiciens: "Chrominance is at half resolution of luminance".

### Mirgošanas frekvence

Mirgošana (*flicker*) ir efekts, ko rada kadru pārslēgšana. Filmu ieraksts: 24 kadri sekundē (un leģendas par 25.kadru). Lai mazinātu mirgošanas sajūtu, kadrus atkārto (parasti bez izmaiņām), lai mirgotu 48 vai 72 reizes sekundē.

Televīzijas ierakstos ir 25 vai 30 kadri sekundē; mirgošana mēdz būt divreiz biežāk (50 Hz vai 60 Hz), kas izmanto "interlacing" -- pārzīmē tikai daļu no pikseļu rindām. Katodstaru lampas mirgo ar 50 Hz vai 60 Hz frekvenci (regulāri maina gaismas intensitāti); šādu mirgošanu cilvēks var pamanīt.

## Konteineri un kodeki

Filma pie patērētāja nonāk kā fails vai kā straumējams video. Šie ir konteineru formāti, ko atbalsta YouTube:

* MP4 (daļa no MPEG-4 standarta); paplašinājums `*.mp4`
* AVI (Audio Video Interleaved/Microsoft); paplašinājums `*.avi`
* WMV (Windows Media Video priekš WM Player); paplašinājums `*.wmv`
* WebM (BSD licencēts konteiners/Google)
* MOV (QuickTime/Apple); paplašinājums `*.mov`
* FLV (Flash Video)
* 3GP (3G mobilo sakaru video)

Google piedāvā vienkāršus konteinerus **WebP** (attēliem) un **WebM** (filmām). Nopietnai videomateriāla pasniegšanai (daudzi kanāli, subtitri vairākās valodās, navigācija pa filmu utt.) ir piemērotāks **MKV** jeb Matrjoškas konteiners.

**WebP:** WebP nodrošina nedaudz labāku saspiešanu kā JPEG vai MPEG-4. **WebP**, kam ir gan bezzudumu, gan zudumradošās saspiešanas funkcijas, panāk mazākus attēlu izmērus, salīdzinot attiecīgi ar PNG un JPEG (gan tipiskiem failiem Internetā, gan ļoti optimāli saspiestiem ar `pngcrush` u.c.)

**WebM:** Video formāts **WebM** ir draudzīgi licencēts, patīk Vikipēdijai. Lietojams ar pārlūkprogrammās iebūvēto HTML5 video atskaņotāju kā arī ar daudziem citiem.

### Kodeki

Codec (*coder-decoder*) ir konkrētais audio un video kanāla saspiešanas standarts. Katram konteineru formātam lietojami daži populāri kodeki:

* DivX, Xvid (AVI konteinerā)
* MPEG (MP4 konteinerā) izmanto dažādās aplikācijās un arī dzelžos. Tas ilgstoši bijis industrijas standarts.

Vairums CD/DVD atskaņotāju, telefoni, viedie TV un mediju atskaņotāji atbalsta Xvid kodeku. Tas būs ērts vairumam lietotāju. Xvid kodeks ir ātrāks par MPEG-1 un arī mazāk noslogo procesoru.

### Video saspiešana

Video visvienkāršākajā izpratnē ir daudzu rastra attēlu secība. Pat iekodējot ar JPEG (katru attēlu atsevišķi) radīsies milzīgi lieli faili. Secīgi attēli stipri korelē (ja vien tieši attiecīgajā vietā netika samontēti divi gabali vai krasi mainīts kameras stāvoklis).

**MPEG freimu tipi:** MPEG piemērots gan statiski saspiestiem, gan straumētiem datiem; katru attēlu iekodē vienā no šiem 3 veidiem:

* I-frame (*intra-frame*) - bilde, kuru kodē kā pilnu attēlu.
* P-frame (*predictive coded frame*) balstās uz iepriekšējo I-freimu vai P-freimu
* B-frame (*bidirectionally predictive coded frame*) izmanto gan iepriekšējo, gan nākamo freimu, kas var būt gan I-, gan P-freims.

**I-freimu kodēšana:** Līdzīgi kā JPEG (8x8 bloki), arī MPEG kodē vienādus blokus: 16x16 pikseļi. I-freimiem algoritms līdzīgs kā JPEG. I-freimi ir "pieturas punkti", uz kuriem būvē citus. [YCbCr krāsu plakne](https://en.wikipedia.org/wiki/YCbCr) - nav tas pats kas YIQ.

**P-freimu kodēšana:** **Kustības vektors:** P-freima 16x16 pikseļu blokam meklē līdzīgāko iepriekšējā I-freimā vai P-freimā. Dažreiz tas var būt nobīdīts - ja video attēlota kustība vai kameras slīdēšana - *panning*.

![P-freima kodēšana](figs/p-frame-encoding.png)

**B-freimus atliek nosūtītajos datos:**

| Playback order | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frame type | I | B | B | P | B | B | P | B | B | I |
| Data stream order | 0 | 2 | 3 | 1 | 5 | 6 | 4 | 8 | 9 | 7 |

Ja filmas scēna strauji mainās, ir izdevīgi biežāk lietot I-freimus, ja tā ir relatīvi statiska, tad - sajauktus P-freimus un B-freimus. Kodeki parasti ir optimizēti kaut kādam "caurmēra" ritmam.

### Saspiešanas datu piemēri

Ja video ir $356 \times 260$ pikseļi, tad freimu izmēri un saspiešanas attiecības ir sekojošas:

| Freims | Izmērs | Saspiešana |
| --- | --- | --- |
| I-Freims | 18 KiB | 7:1 |
| P-Freims | 6 KiB | 20:1 |
| B-Freims | 2.5 KiB | 50:1 |
| Vidēji | 4.8 KiB | 27:1 |

Šādu attēlu pārraidīšanai vajadzīgais tīkla savienojums:

$$
30\,\text{frame/s}\cdot 4.8\,\text{Kb/frame}\,\cdot 8 = 1.2\,\text{Mbit/s}.
$$

Kopā ar audio tas var būt 1.45 megabiti sekundē, kas aizņem T1 Interneta savienojumu (viens vītais pāris; 1.544 Mbps).

### MPEG lietojumi

* Satelīttelevīzijas pārraides, kas digitālu signālu no satelīta pārtaisa krāsainā TV signālā (kas var joprojām būt analogs).
* Kabeļtelevīzija.
* On-demand televīzija ar desmitiem tūkstošu lejupielādējamu vai straumējamu filmu.

## MP3 Saspiešana

MP3 mērķis ir saspiest mūziku u.c. audiofailus, lai tos varētu pārraidīt datortīklos un glabāt mūzikas atskaņotājos. MP3 atskaņošanai publiska programmatūra parādījās ap 1994.g. Napster parādījās 1999.gadā; agrīns failu apmaiņas serviss, bet failu direktoriju glabāja centralizēti, tāpēc pret to vērsās tiesā un servisu 2001.gadā nācās slēgt.

Līdz pat 2017.g. Fraunhofer Institute for Integrated Circuits (svarīgāko patentu turētāji) uzlika tam ierobežojošas licences; ievāca maksu no softa ražotājiem.

Mūsdienās MP3 ir "mantots" (*legacy*) jeb "miris" formāts, bet tam joprojām plašs rīku atbalsts.

### Parauga ātrums (sample rate)

*Sample rate* mēra hercos (1 Hz = $1\ \mathrm{s}^{-1}$) - cik reizes sekundē kaut kas notiek (piemēram, cik bieži nomēra skaņu kā membrānas stāvokli). CD-ROM kvalitātes ierakstam parasti vajag ap 44.1 kHz (CD). (Ir arī standarti, kas izmanto 48 kHz, 88.2 kHz, vai 96 kHz.)

**Naikvista-Šenona teorēma:** Ja funkcijai $x(t)$ (pēc Furjē transformācijas pielietošanas) nav frekvenču, kas pārsniegtu $B$ hercus, tad to var pilnībā atjaunot, ja zināmas tās vērtības ik pēc laika intervāliem ${\displaystyle \Delta t = \frac{1}{2B}}$. (*Nyquist-Shannon Sampling theorem*)

Šie divi apgalvojumi ir ekvivalenti

**Nyquist-Shannon 1:** Funkciju $f(t)$, kuras vērtības zināmas pēc vienādiem laika intervāliem $\Delta T$ var viennozīmīgi atjaunot no šīm vērtībām $\lbrace f_n \rbrace$ tad un tikai tad, ja $f(t)$ enerģijas spektrs nesatur frekvences virs $\frac{\pi}{\Delta T}\ \mathrm{rad/s}$.

**Nyquist-Shannon 2:** Ir tikai viena funkcija $f(t)$, kuras frekvenču spektrs viss atrodas zem $\frac{\pi}{\Delta T}$, ko apmierina dotās vērtības $\lbrace f_n \rbrace$.

[Lecture10 in 2.161](https://ocw.mit.edu/courses/mechanical-engineering/2-161-signal-processing-continuous-and-discrete-fall-2008/lecture-notes/lecture_10.pdf).

Pretpiemērs augstām frekvencēm (divu sinusu starpība):

![Divu sinusu starpība](figs/sinus-functions.png)

### Bitrate (Bitu pārraides ātrums)

Svarīgākais saspiešanas parametrs.

* MP3 (MPEG layer 3 standarts) atļauj bitu ātrumus no 8 kbit/s līdz 320 kbit/s. Noklusējums ir 128 kbit/s.
* Salīdzinājumam, [audio CD-ROM](https://en.wikipedia.org/wiki/Compact_Disc_Digital_Audio#Bit_rate) satur 2048 baitus sektorā (un atskaņo 75 sektorus sekundē). Tātad = 153,600 baiti sekundē jeb 1200 kbit/s.

Tipiski MP3 faili ir $10 \times$ mazāki par audio kompaktdiska failiem.

### *Constant bitrate* (CBR) un *Variable bitrate* (VBR)

* Mūzikas sarežģītība var būt atkarīga no tā, cik daudzi instrumenti spēlē. VBR to risina, ļaujot bitu ātrumam mainīties atkarībā no signāla. Mūzikas gabalu sadala vairākos *freimos* (*frames*) un iekodē ar atšķirīgiem bitu ātrumiem.
* Ieraksta kvalitāti VBR gadījumā nosaka lietotāja izraudzīts parametrs (maksimāli atļautais bitu ātrums).
* VBR var radīt dažiem atskaņotājiem (dekoderiem) grūtības pateikt, cik ilgi gabals skanēs.
* VBR nav piemērots straumēšanai.

### Dzirdamās skaņas frekvences

* Cilvēka ausis var uztvert no $20$ līdz $20\,000$ hercu skaņas frekvenci. Pusmūža cilvēki - no $16\,000$ herciem (*dog whistle* uz dzirdamības diapazona robežas).
* Pirmās oktāvas "la" (jeb **A4**) izmanto toņdakšu, ko sauc **Stuttgart pitch**, kam ir 440 Hz (nosvārsta gaisu 440 reizes sekundē). Ja frekvence palielinās divkārt, skaņa par oktāvu augstāka.
* "Labi temperēta" skaņu skala saliek $12$ pustoņus ar vienādām blakusesošo pustoņu frekvenču attiecībām.
* Piemēram, "do" (C) un "do diēzs" (Cis) frekvenču attiecība ir $1$ pret $\sqrt[12]{2}$.

**Analizējošās filtrubankas (filterbanks):** Atdarina cilvēka ausī esošās struktūras, no kurām katra uztver skaņas kaut kādā šaurā frekvenču diapazonā. Šo diapazonu ir ap $24$.

![Filtrubankas](figs/filter-banks.png)

Skaņu plūsmā ir dažas situācijas, kad viens tonis nomaskē otru (MP3 paredz, ka otru toni nevarēs dzirdēt; tāpēc tas tiek nomaskēts). Divi gadījumi - tuva frekvence, laika sakritība.

**Skaņas maskēšana:** Tuvo frekvenču maskēšana (*frequency masking*):

![Tuvo frekvenču maskēšana](figs/frequency-masking.png)

Temporālā maskēšana (*temporal masking*):

![Temporālā maskēšana](figs/temporal-masking.png)

<!-- https://www.soundonsound.com/sound-advice/q-can-you-help-me-mp3-file-conversion -->

### Stereo skaņa

* *Joint Stereo* pārraida kreisās un labās auss skaņu divos kanālos: Vienā kanālā summu, otrā kanālā - starpību.
* Tā kā abām ausīm ir ļoti līdzīga skaņa, tad summa ir vidējota skaņa, bet starpība ir neliela un to var labi saspiest.
* Cilvēka telpiskā skaņas uztvere (*immersive sound*) ir ļoti niansēta: skaņas virzienu/azimutu var sadzirdēt ar 1 grāda precizitāti; augstumu virs horizonta - ar apmēram 10 grādu precizitāti.
* Joprojām grūti risināms jautājums, kā novietot skaļruņus un mainīt austiņās dzirdamās lietas, ja cilvēks pārvietojas telpā. Bet MP3 šo nerisina.

## Opus kodeks

Failu nosaukumos var parādīties, bet to bieži aizstāj konteinera faila paplašinājums.

* `audiofile.opus` (noteikti iekodēts ar Opus),
* `audiofile.ogg` (Ogg konteiners, ja tas nelieto citu kodeku, piemēram, Vorbis; reāli izmantoto kodeku var redzēt Ogg metadatos),
* `audiofile.webm` (WebM konteiners straumēšanai vai Web lietojumiem)
* `audiofile.mka` (Matreska vai MKV konteiners; paplašinājums `*.mka` nozīmē tikai audio)

Opus māk pārslēgties starp divām modēm, kas optimizē dažādas lietas -- vai nu augsta skaņas kvalitāte vai arī spēja pielāgoties dažādas caurlaidības transporta kanāliem un zema aizture (*latency*).

**CELT Mode:** Parasti izmanto mūzikas saspiešanai. Tas nozīmē CELT (Constrained Energy Lapped Transform). Tas izmanto Izmainīto Diskrēto Kosinusu pārveidojumu (*Modified Discrete Cosine Transform*, MDCT).

**SILK Mode:** SILK mode ir piemērotāka runas saspiešanai. SILK izmanto lineāru paredzošo kodējumu (*Linear Predictive Coding*, LPC) nevis MDCT.

## VP9 kodējums

*VP9* ir Google izstrādāts atvērts un bezmaksas (bez licences maksām) video kodeks. Tā pamatideja ir tāda pati kā MPEG saimes kodekiem: katru kadru sadala blokos, katru bloku *prognozē* -- no tā paša kadra jau atkodētajiem kaimiņiem (*intra*) vai no iepriekšējiem kadriem ar kustības vektoru (*inter*) --, un kodē tikai prognozes kļūdu jeb *atlikumu*: to transformē (DCT vai ADST), kvantizē un saspiež ar aritmētisko kodu.

**Vēsture.** VP9 ir On2 Technologies kodeku (VP3, VP6, VP8) turpinājums; Google 2010.gadā nopirka On2 un atvēra VP8 kā daļu no WebM projekta. VP9 bitu plūsmu nofiksēja 2013.gadā. Salīdzinot ar VP8 (un H.264), tas pie tādas pašas kvalitātes dod apmēram par trešdaļu līdz pusei mazākus failus; to lieto YouTube, WebRTC videozvani un pārlūkprogrammas. VP9 idejas (un daļa neizlaistā VP10) kļuva par pamatu kodekam AV1 (Alliance for Open Media, 2018), kura intra kadri ir AVIF attēlu pamatā. Atsauces realizācija ir bibliotēka *libvpx* ar programmām `vpxenc` (iekodētājs) un `vpxdec` (atkodētājs).

### Konteineri: IVF, WebM, MP4

Pats VP9 kodeks definē tikai *freimu* (viena kodēta kadra) bitu virkni; kadru laiku, izmērus un audio glabā konteiners.

* **IVF** ir vienkāršākais konteiners, ko lieto libvpx testos un pētniecības rīkos. Faila sākumā ir $32$ baitu galvene: paraksts `DKIF`, kodeka kods (`VP90`), platums, augstums, laika bāze (piemēram, $25$ kadri sekundē) un freimu skaits. Pēc tās katram ierakstam ir $12$ baitu galvene (datu garums $4$ baitos un laika zīmogs $8$ baitos) un pati VP9 freima bitu virkne. Tā kā nekā cita nav, IVF ir ērts, lai freimus pa vienam izgrieztu, aizstātu vai analizētu.
* **WebM** ir Matroska (MKV) apakškopa, ko izmanto pārlūkprogrammas; tajā parasti ir VP9 video un Opus audio. **MP4** konteinerā VP9 plūsmas kods ir `vp09`.
* **YouTube** lielāko daļu video piedāvā arī VP9 formātā (WebM, DASH straumēšana, katra izšķirtspēja kā atsevišķa video plūsma bez audio). Lejupielādētu WebM (ievērojot autortiesības un pakalpojuma noteikumus) var pārlikt IVF konteinerā bez pārkodēšanas: `ffmpeg -i video.webm -c:v copy -an video.ivf` (`-c:v copy` saglabā VP9 bitus nemainītus, `-an` atmet audio).

Viens IVF ieraksts var saturēt arī vairākus VP9 freimus -- to sauc par *superfreimu* (*superframe*): freimus saliek pēc kārtas un beigās pievieno indeksu ar katra freima garumu. Tā kopā glabā slēpto freimu un nākamo rādāmo freimu (sk. nākamo apakšnodaļu), lai katram konteinera ierakstam atbilstu tieši viens parādāms kadrs.

### Video klipa struktūra: freimu veidi un GOP

VP9 freimam ir viena no šīm lomām:

* **Atslēgas freims** (*keyframe*, `frame_type = KEY_FRAME`) -- visi bloki ir *intra*; atkodētājs no tā var sākt darbu, un tas atiestata visas atsauces. Ar to sākas katrs klips (un katrs punkts, uz kuru var "pārtīt").
* **Inter freims** -- blokus var prognozēt no līdz pat trim *atsauces freimiem* (*reference frames*): `LAST` (parasti iepriekšējais kadrs), `GOLDEN` (senāks augstas kvalitātes kadrs) un `ALTREF`. Atsauces glabā $8$ atmiņas vietās (*reference slots*); freima galvenes lauks `refresh_frame_flags` norāda, kurās vietās pēc atkodēšanas ierakstīt šo freimu.
* **Intra-only freims** -- tikai intra bloki (kā atslēgas freimā), bet atsauces netiek atiestatītas.
* **Slēptais ALTREF freims** (`show_frame = 0`) -- inter freims, ko atkodē un saglabā kā atsauci, bet **neparāda**. Kodētājs to izveido no *nākotnes* kadra (parasti temporāli filtrētu, t.i., vidējotu no vairākiem blakus kadriem un tāpēc ar mazāku troksni) un no tā prognozē vairākus nākamos kadrus.
* **`show_existing_frame`** -- dažus baitus garš freims bez kodētiem datiem, kas vienkārši parāda kādu jau atkodētu atsauces freimu (piemēram, iepriekš slēpto ALTREF).

*GOP* (*group of pictures*) ir kadru grupa no viena "enkura" (atslēgas freima vai ALTREF) līdz nākamajam. Tā kā ALTREF ir nākotnes kadrs, kas jāatkodē **pirms** kadriem, kuri no tā prognozē, *dekodēšanas secība* (kādā freimi ir failā) nesakrīt ar *rādīšanas secību*. Tas ir līdzīgi MPEG B-freimiem (sk. "Video saspiešana" augstāk), tikai VP9 nekodē atsevišķus B-freimus, bet izmanto slēptos freimus.

<img
  id="vp9_gop"
  alt="VP9 dekodēšanas un rādīšanas secība"
  src="{{ '/lectures/lossy_video/figs/vp9-gop.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*Faila `bouncing_ball_ARF.ivf` (sk. galeriju) pirmie $16$ kodētie freimi: $33$ IVF ierakstos ir $36$ kodēti freimi, no kuriem $3$ ir slēpti ALTREF, katrs superfreimā kopā ar nākamo rādāmo freimu.*

Iekodētāja iestatījumi nosaka GOP struktūru: *low-delay* režīmā (`--lag-in-frames=0`) kodētājs neredz nākotnes kadrus, tāpēc dekodēšanas secība sakrīt ar rādīšanas secību un slēptu freimu nav (vajadzīgs videozvaniem); ar `--auto-alt-ref=1` un nākotnes kadru "skatīšanos uz priekšu" (`--lag-in-frames=25`) rodas ALTREF freimi un labāka saspiešana (video pēc pieprasījuma).

### Freima uzbūve: galvenes, flīzes, superbloki, bloki

Katrs freims sastāv no trim daļām:

1. **Nesaspiestā galvene** (*uncompressed header*) -- parastiem bitiem: freima tips, `show_frame`, `show_existing_frame`, izmēri, atsauču izvēle, `refresh_frame_flags`, cilpas filtra un kvantizācijas parametri (`base_q_idx`), segmentācija, flīžu izkārtojums. To var nolasīt, neko neatkodējot aritmētiski.
2. **Saspiestā galvene** (*compressed header*) -- aritmētiski kodēta: transformāciju izmēru režīms un varbūtību tabulu labojumi šim freimam.
3. **Flīžu dati** (*tiles*) -- paši bloki. Freimu var sadalīt vairākās flīžu kolonnās (katra vismaz $256$ pikseļus plata), ko var atkodēt paralēli; katrā flīzē aritmētiskais kods sāk no jauna.

Flīzi sadala *superblokos* $64 \times 64$ pikseļi, un katru superbloku rekursīvi sadala (*partition*): bloku var atstāt veselu (`PARTITION_NONE`), sadalīt divos horizontālos vai vertikālos taisnstūros (`HORZ`, `VERT`) vai četros kvadrātos (`SPLIT`), līdz $8 \times 8$, un $8 \times 8$ blokam ir arī $4 \times 4$ apakšbloki. Katram *blokam* (*block*) glabā:

* prognozes veidu (intra vai inter) un *režīmu* (*mode*): intra režīmam -- prognozes virzienu, inter režīmam -- atsauces freimu un kustības vektoru;
* transformācijas izmēru (`tx_size`) un karodziņu `skip` (ja `skip = 1`, bloka atlikums ir $0$ un koeficientus nekodē);
* segmenta numuru (`segment_id`, sk. "Cilpas filtrs un segmentācija").

Pēc tam seko atlikuma *transformācijas bloku* (`tx_size` lielumā) kvantizētie koeficienti.

### YUV pikseļi un prognoze

VP9 kodē *YUV* (precīzāk -- YCbCr) pikseļu datus: gaišuma plakni $Y$ un divas krāsainības plaknes $U$ un $V$ (sk. JPEG un AVIF lekcijas nodaļu par krāsu telpām un 4:2:0 izretināšanu). Pamata profils (*profile 0*) ir $8$ biti un 4:2:0, t.i., $256 \times 256$ kadrā ir $65\,536$ gaišuma un $2 \cdot 16\,384$ krāsainības vērtības. Profils 1 atļauj 4:2:2 un 4:4:4, profili 2 un 3 -- $10$ vai $12$ bitu vērtības (HDR). Iekodētājs parasti saņem jau YUV kadrus (piemēram, `.y4m` failā: teksta galvene un katram kadram secīgi $Y$, $U$, $V$ plaknes baitos), un atkodētājs izvada tieši tādas pašas plaknes. Divas atkodētas plūsmas uzskata par vienādām, ja visas YUV plaknes sakrīt baitu līmenī (to ērti pārbaudīt, salīdzinot katra kadra SHA-256).

**Intra prognoze** aizpilda bloku no jau atkodētajiem pikseļiem virs tā un pa kreisi no tā: VP9 ir $10$ režīmi -- DC (vidējā vērtība), vertikālais, horizontālais, sešas diagonāles un TM ("TrueMotion", gradienta turpinājums).

**Inter prognoze** ņem bloku no atsauces freima, nobīdītu par *kustības vektoru* (*motion vector*, MV). Kustības vektoru precizitāte ir $\frac{1}{8}$ pikseļa (vai $\frac{1}{4}$). Ja vektors nav vesels, starpvērtības aprēķina ar $8$ punktu *interpolācijas filtru* -- parasto (`EIGHTTAP`), gludo (`EIGHTTAP_SMOOTH`) vai aso (`EIGHTTAP_SHARP`); ja freimā filtrs ir `SWITCHABLE`, to var izvēlēties katram blokam. Veselam (*full-pel*) vektoram visi trīs filtri dod vienu un to pašu rezultātu. Bloku var prognozēt arī kā divu atsauču vidējo (*compound prediction*).

Kustības vektoru pašu arī prognozē no kaimiņu blokiem: atkodētājs no kaimiņiem sastāda divus kandidātus, un bloka inter režīms izvēlas `NEARESTMV` (pirmais kandidāts), `NEARMV` (otrais), `ZEROMV` (nulles vektors) vai `NEWMV` (kodē starpību no kandidāta). Tāpēc vienādu kustību bieži var pierakstīt ar vairākiem dažādiem simboliem.

### Transformācija un kvantizācija: DCT un ADST

Atlikumu transformē blokos $4 \times 4$, $8 \times 8$, $16 \times 16$ vai $32 \times 32$. Izmanto DCT vai *ADST* (*asymmetric discrete sine transform*); ADST ir piemērotāka intra blokiem, kuru atlikums aug, attālinoties no prognozes malas. VP9 transformācijas tipu (`tx_type`: DCT vai ADST katrā virzienā) nekodē atsevišķi: gaišuma plaknes intra blokiem līdz $16 \times 16$ tas izriet no prognozes virziena, visiem pārējiem (inter blokiem, krāsainības plaknēm, $32 \times 32$) vienmēr ir DCT. Visas transformācijas ir definētas veselos skaitļos (ar noapaļošanu), lai iekodētājs un jebkurš atkodētājs iegūtu bitu līmenī vienādu rezultātu.

Koeficientus kvantizē, dalot ar kvantizācijas soli un noapaļojot (sk. JPEG 5. soli). Soli nosaka *kvantizācijas indekss* `qindex` ($0 \ldots 255$; jo lielāks, jo rupjāk) caur standarta tabulām, atsevišķi DC un AC koeficientiem; `vpxenc` parametrs `--cq-level` izvēlas mērķa kvalitāti. Kvantizētos koeficientus nolasa noteiktā *skenēšanas secībā* (līdzīgi JPEG zig-zag) un kodē kā *žetonus* (*tokens*): `ZERO_TOKEN`, `ONE_TOKEN`, …, lielām vērtībām -- kategorijas ar papildu bitiem. *EOB* (*end of block*) žetons norāda, ka pārējie koeficienti ir nulles; lauks `eob` ir pozīcija skenēšanas secībā, kurā koeficientu kodēšana beidzas.

### Aritmētiskā kodēšana un varbūtību tabulas

Visu freima saturu pēc nesaspiestās galvenes kodē ar *Būla aritmētisko kodētāju* (*boolean arithmetic coder*) -- bināru aritmētisko kodu (sk. lekciju par [aritmētisko kodu]({{ '/lectures/lossless_arithmetic_and_ans/' | relative_url }})). Katram bitam ir varbūtība, ka tas ir $0$, pierakstīta kā skaitlis $1 \ldots 255$ (t.i., $p/256$); ļoti paredzams bits aizņem daudz mazāk par $1$ bitu. Simbolus ar vairākām vērtībām (režīmus, žetonus, sadalījumus) kodē kā binārā koka ceļu, katram koka mezglam ar savu varbūtību.

Varbūtības atkarīgas no *konteksta*: piemēram, `skip` varbūtība atkarīga no tā, vai kaimiņu blokiem ir `skip`, bet koeficienta žetona varbūtība -- no transformācijas izmēra, plaknes, pozīcijas un kaimiņu koeficientiem. Visu varbūtību kopums ir *freima konteksts* (*frame context*, tabula `fc`). Atkodētājs glabā $4$ šādus kontekstus; freims izvēlas vienu (`frame_context_idx`), saspiestajā galvenē var to labot (*forward update*), un pēc freima atkodēšanas konteksts var pielāgoties faktiskajam simbolu skaitam (*backward adaptation*), ja to atļauj galvenes lauki `refresh_frame_context`, `error_resilient_mode` un `frame_parallel_decoding_mode`.

### Kodētāja un atkodētāja stāvoklis

VP9 ir stāvokli saglabājošs kodeks: freimu var atkodēt tikai tad, ja ir atkodēti visi iepriekšējie freimi, no kuriem tas atkarīgs. Atkodēšanas laikā tiek uzturētas šādas datu struktūras (iekodētājs uztur tieši tās pašas, lai prognozētu tāpat kā atkodētājs):

* $8$ **atsauces kadru bufferi** (atkodētas YUV plaknes) un to piesaiste `LAST`, `GOLDEN`, `ALTREF`;
* $4$ **freimu konteksti** (varbūtību tabulas) un simbolu skaitītāji to pielāgošanai;
* **blokos izmantoto režīmu un kustības vektoru režģis** -- kaimiņu (virs un pa kreisi) konteksti un iepriekšējā freima kustības vektori, no kuriem prognozē jaunos vektorus;
* **segmentācijas karte** un cilpas filtra iestatījumi, kurus var pārņemt no iepriekšējā freima.

Tāpēc freima baitu nomaiņa ietekmē arī visus nākamos freimus, kuri no tā atkarīgi -- pārbaudot, vai divas plūsmas dod vienādus kadrus, jāatkodē visa plūsma no sākuma (vai no atslēgas freima).

### Cilpas filtrs un segmentācija

Pēc bloku atjaunošanas freimam piemēro **cilpas filtru** (*loop filter*): tas nogludina bloku robežas, ja tur ir tikai nelielas atšķirības (bloku artefakti), bet saglabā īstas malas. Filtra stiprumu nosaka freima līmenis (`filter_level` $0 \ldots 63$) un asums, kā arī bloku režīmi, atsauces un `skip`. Filtrēto kadru izmanto gan rādīšanai, gan kā atsauci nākamajiem freimiem ("cilpā"). Tāpēc atkodēto kadru salīdzina **pēc** cilpas filtra: simbola maiņa, kas nemaina atlikumu, joprojām var mainīt pikseļus caur filtra lēmumu.

**Segmentācija** ļauj blokus sadalīt līdz $8$ segmentos (`segment_id`); katram segmentam var iestatīt savu kvantizācijas indeksu, cilpas filtra līmeni, fiksētu atsauces freimu vai obligātu `skip`. Kodētājs to izmanto, piemēram, adaptīvai kvantizācijai (`--aq-mode`): sarežģītiem apgabaliem viens `qindex`, gludiem -- cits.

### Bezzudumu VP9: Volša-Adamāra transformācija

Ja `base_q_idx = 0` un visas kvantizācijas korekcijas ir $0$, freims ir **bezzudumu** (`vpxenc --lossless=1`): atkodētie pikseļi precīzi sakrīt ar ievades YUV. Tad DCT/ADST vietā izmanto tikai $4 \times 4$ *Volša-Adamāra transformāciju* (*Walsh–Hadamard transform*, WHT), un cilpas filtru nepiemēro.

WHT bāzes vektori sastāv tikai no $\pm 1$, piemēram, $4 \times 4$ gadījumā

$$
H_4 = \left( \begin{array}{rrrr}
1 & 1 & 1 & 1 \\
1 & 1 & -1 & -1 \\
1 & -1 & -1 & 1 \\
1 & -1 & 1 & -1
\end{array} \right),
$$

tāpēc to aprēķina tikai ar saskaitīšanu, atņemšanu un bīdēm. VP9 to realizē ar veselu skaitļu soļiem, kurus var precīzi apgriezt (*lifting*): no koeficientiem atjauno tieši to pašu atlikumu, bez noapaļošanas kļūdām. DCT šādas īpašības nav -- tās veselo skaitļu versija ir tikai tuvinājums, tāpēc pat ar vissīkāko kvantizāciju dažas vienības var mainīties. Bezzudumu režīmā informācija netiek zaudēta, un saspiešana notiek tikai prognozes un aritmētiskā koda dēļ, tāpēc faili ir daudz lielāki (ja vien saturs nav ļoti vienkāršs).

### Kodētāja lēmumi: Rate-Distortion Optimization

Standarts nosaka tikai atkodēšanu; iekodētājs pats izlemj, kā sadalīt superblokus, kādus režīmus, kustības vektorus, transformāciju izmērus un koeficientus izvēlēties. *Rate-distortion optimization* (RDO) šos lēmumus pieņem, minimizējot

$$
J = D + \lambda \cdot R,
$$

kur $D$ ir kropļojums (piemēram, kvadrātisko kļūdu summa starp oriģinālo un atjaunoto bloku), $R$ -- bitu skaits, kas vajadzīgs šim variantam (aprēķināts no pašreizējām aritmētiskā koda varbūtībām), bet $\lambda$ -- "bitu cena", kas aug līdz ar `qindex`. Iekodētājs katram blokam izmēģina daudzus variantus un izvēlas mazāko $J$; pat kvantizētos koeficientus var mainīt par $\pm 1$, ja tas ietaupa vairāk bitu nekā pieaug kļūda (*trellis* kvantizācija). Pilna pārlase ir ļoti lēna, tāpēc `vpxenc` ātruma iestatījumi (`--good`/`--best`/`--rt`, `--cpu-used`) nosaka, cik daudz variantu atmest ar heiristikām. Divu gājienu režīmā (`--passes=2`) pirmais gājiens savāc statistiku par visu video, un otrajā to izmanto bitu sadalīšanai starp kadriem un ALTREF izvietošanai.

Tā kā RDO izvēlas lētāko pierakstu, tipiskā plūsmā katram blokam ir "dabiskā" simbolu izvēle. Taču bieži vienu un to pašu atkodēto rezultātu var iegūt arī ar citiem simboliem: piemēram, `skip = 0` blokam ar nulles atlikumu, vēlāku `eob`, cita interpolācijas filtra izvēle veselam kustības vektoram vai `NEWMV` vietā `NEARESTMV`, ja tie dod to pašu vektoru. Šādas "pikseļus nemainošas" simbolu izmaiņas var izmantot steganogrāfijai un ūdenszīmēm (sk. "Kodeku lietojumi"), bet pārrakstīšana uz RDO dabisko izvēli -- to noņemšanai.

### Piemēru galerija

Šie IVF faili ($256 \times 256$ pikseļi, ja nav norādīts citādi, $33$ kadri, $25$ kadri sekundē, profils 0) ir sintētiski testa video, kas kodēti ar `vpxenc`. *LD* (*low delay*) failos dekodēšanas secība sakrīt ar rādīšanas secību; *ARF* failos ir slēpti ALTREF freimi superfreimos. Nesaspiestā veidā viens šāds klips ($33$ kadri 4:2:0) aizņem $3.2$ MB. Failus var atskaņot, piemēram, ar `ffplay` vai VLC, vai pārvērst YUV ar `vpxdec --i420 -o kadri.yuv fails.ivf`.

1. [white_static_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/white_static_LD.ivf' | relative_url }}) (1 KB) -- nemainīgs balts kadrs. Pēc atslēgas freima visi bloki ir `skip` ar `ZEROMV`, tāpēc katrs nākamais freims aizņem tikai dažus baitus.
2. [bouncing_ball_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/bouncing_ball_LD.ivf' | relative_url }}) (2 KB) -- vienkrāsaina bumba pa $2$ pikseļiem kadrā pārvietojas pa vienkrāsainu fonu. Bumbas iekšpuse tiek prognozēta ar veselu kustības vektoru, fons -- ar `skip`.
3. [bouncing_ball_ARF.ivf]({{ '/lectures/lossy_video/vp9-examples/bouncing_ball_ARF.ivf' | relative_url }}) (2 KB) -- tas pats saturs divu gājienu režīmā ar ALTREF: $36$ kodēti freimi, no tiem $3$ slēpti, superfreimos (sk. shēmu "Video klipa struktūra").
4. [integer_pan_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/integer_pan_LD.ivf' | relative_url }}) (6 KB) -- sīka trīskrāsu rūtiņu tekstūra pārvietojas par veselu pikseļu skaitu. Viss kadrs ir labi prognozējams ar vienu kustības vektoru, tāpēc atlikuma gandrīz nav, lai gan attēls ir detalizēts.
5. [screen_content_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/screen_content_LD.ivf' | relative_url }}) (7 KB) -- ekrāna saturs: vienkrāsaini paneļi un ritinošs "teksts". Lieli nemainīgi apgabali un asas malas.
6. [saturation_field_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/saturation_field_LD.ivf' | relative_url }}) (8 KB) -- melns un balts lauks ($Y = 0$ un $Y = 255$) ar kustīgu robežu. Atjaunotās vērtības tiek apgrieztas līdz intervālam $[0; 255]$.
7. [lowq_gradient_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/lowq_gradient_LD.ivf' | relative_url }}) (33 KB) -- lēni mainīgs gluds krāsu gradients ar zemu `qindex` (augsta kvalitāte): daudz mazu AC koeficientu un kustības vektori ar daļpikseļu precizitāti.
8. [midband_noise_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/midband_noise_LD.ivf' | relative_url }}) (1 MB) -- katrā kadrā jauns nejaušs troksnis. Nekas nav prognozējams, tāpēc fails ir tikai apmēram $3$ reizes mazāks par nesaspiesto video.
9. [lossless_wht_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/lossless_wht_LD.ivf' | relative_url }}) (2 KB) -- bumbas saturs bezzudumu režīmā (`qindex` $0$, Volša-Adamāra transformācija, bez cilpas filtra); atkodētais YUV precīzi sakrīt ar ievadi.
10. [clone_segment_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/clone_segment_LD.ivf' | relative_url }}) (2 KB) -- bumbas saturs, kodēts ar segmentāciju (`--aq-mode=1`): freimu galvenēs ir segmentu karte un vairāki segmenti.
11. [yuv444_gradient_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/yuv444_gradient_LD.ivf' | relative_url }}) (68 KB) -- krāsains gradients profilā 1 ar pilnas izšķirtspējas krāsainību (4:4:4); $U$ un $V$ plaknēs ir tikpat daudz vērtību kā $Y$ plaknē.
12. [hbd_gradient10_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/hbd_gradient10_LD.ivf' | relative_url }}) (23 KB) -- gradients profilā 2 ar $10$ bitu vērtībām ($0 \ldots 1023$).
13. [tiled_multicolumn_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/tiled_multicolumn_LD.ivf' | relative_url }}) (24 KB) -- $512 \times 256$ kadri, sadalīti divās flīžu kolonnās, kuras var atkodēt paralēli.
14. [natural_clip_foreman_ARF.ivf]({{ '/lectures/lossy_video/vp9-examples/natural_clip_foreman_ARF.ivf' | relative_url }}) (74 KB) -- reāls video (klasiskā testa secība *foreman*, izgriezums $256 \times 256$) ar kameras kustību, jauktiem intra un inter blokiem, dažādiem transformāciju izmēriem un slēptiem ALTREF freimiem.

## Kodeku lietojumi

### Steganogrāfija

Steganogrāfija nodarbojas ar datu noslēpšanu cita veida failos -- piemēram, teksta failos, audio vai video failos kā arī attēlos. Var izmantot gan mediju faila saturisko daļu (redzamie pikseļi, skaņas u.c.), gan hederus (*metadatus*).

Ekstrēms piemērs - informācijas slēpšana DNS protokolā: [Michal Drzymala, et al. Network Steganography in the DNS Protocol](http://www.czasopisma.pan.pl/Content/101654/PDF/47.pdf?handler=pdf)

Aizsardzība pret steganogrāfiju var būt divējāda:

* Steganalīze (*steganalysis*) reizēm var atrast modificētā materiāla oriģinālu (kurā vēl nav slepenā ziņojuma) un salīdzināt ar pārsūtīto ziņojumu. Vai arī meklēt citas neraksturīgas izmaiņas mediju failos, sabojātas ūdenszīmes u.c.
* Steganogrāfija mēdz nebūt noturīga pret nelielām faila izmaiņām, ko tipisks lietotājs (filmas vai attēla skatītājs nepamanītu). Zudumradošie kodeki var netīšām steganogrāfisko ziņojumu sabojāt pat nepamanot tā klātbūtni.

### Ūdenszīmju tehnoloģijas

*Ūdenszīmju tehnoloģijas* (*Watermark techniques*) pievieno failam kādu papildu informāciju. Tās var izmantot autortiesību aizsardzībai, individuālu kopiju marķēšanai, sekojot medija vai tā fragmentu izplatīšanai vai mediju satura aizsardzībai pret izmainīšanu.

Informatīvākās ūdenszīmes var noskaidrot, kurš aizsargātā medija eksemplārs nopludināts. Ūdenszīmju ievietošana ir radniecīgs uzdevums steganogrāfijai.

![Ūdenszīmes ievietošana](figs/embedding-watermark.png)

Ūdenszīmes ievieto jau gatavā mediju failā vai nu radīšanas brīdī, vai vēlāk - izveidojot speciālu kopiju lietotājam. Tās var pievienot arī, mediju failam šķērsojot organizācijas drošības perimetru.

* Izšķir *redzamas ūdenszīmes* (*visible watermarks*) -- Visām PDF faila lappusēm uzkrāsot kādu attēlu vai visu bibliotēkai piederošu grāmatu 17.lpp. iespiest zīmogu.
* Ir arī *neredzamas ūdenszīmes* (*invisible watermarks*). Tās palīdz atzīmēt faila izcelsmi, saņēmēju. Reizēm arī šīs informācijas *nenoliedzamību* (*nonrepudiation*).

<!-- -->

* Izšķir *trauslas ūdenszīmes* (*fragile*), ko viegli sabojāt pat nelieliem medija pārveidojumiem - var palīdzēt atklāt, ja fails ticis mainīts.
* Un *noturīgas ūdenszīmes* (*robust*), kas labi saglabājas arī pēc mediju faila manipulēšanas vai pat apzināta mēģinājuma no tā izdzēst ūdenszīmi.

Bieži vajag gan trauslas, gan noturīgas - lai noskaidrotu faila patieso izcelsmi un vēl arī - vai tas nav ticis mainīts pa ceļam līdz saņēmējam.

* Izšķir *telpiskas ūdenszīmes* (*spatial*), kas parādās noteiktā medija vietā. Noteiktos pikseļos var kvalitatīvi noglabāt datus, bet tie parasti nav noturīgi.
* Un *spektrālas ūdenszīmes* (*spectral*) kas izmaina mediju faila spektrālā pārveidojumā (DCT, DFT vai DWT - t.i. kosinusu, Furjē vai vilnīšu/wavelet pārveidojumā) esošos koeficientus - piemēram, tos, kas atbilst augstākajām frekvencēm, jo cilvēki šīs frekvences grūtāk atšķir.

Spektrālas ūdenszīmes mēdz būt noturīgākas. Ūdenszīmēm vēl arī būtiska ietilpība (*capacity*) - cik daudz datu ūdenszīmē var ievietot. Un zema sarežģītība (*low complexity*), ja digitāla satura izmantošanas pārkāpumu jāvar pamatot vispārsaprotamā veidā.

Lai uzbruktu ūdenszīmēm, attēlus (piemēram JPEG vai citu zudumradošu formātu attēlus) var saspiest vai pārveidot -- permutēt pikseļus, apgriezt, mērogot, ģeometriski deformēt.

## Izmantotā literatūra

<a id="Guru14"></a>**[Guru14]** Guru, J. and Damecha, H. (2014). A review of watermarking algorithms for digital image. *Int. J. Innov. Res. Comput. Commun. Eng.*, 2, 5701--5708. Available at [https://api.semanticscholar.org/CorpusID:44191784](https://api.semanticscholar.org/CorpusID:44191784).

<a id="Pol16"></a>**[Pol16]** Yury Polyanskiy, *Information Theory*, MIT OpenCourseWare, Massachusetts Institute of Technology, Spring 2016. Available at [https://bit.ly/47EfIZ8](https://bit.ly/47EfIZ8), [Archived](https://web.archive.org/web/20240000000000*/https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/).
