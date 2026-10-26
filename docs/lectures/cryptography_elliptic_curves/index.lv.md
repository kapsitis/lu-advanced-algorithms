---
layout: default
title: "Kriptogrāfija TLS 1.3: eliptiskās līknes un atslēgu apmaiņa"
lang: lv
permalink: /lectures/cryptography_elliptic_curves/lv/
---
# 12. Kriptogrāfija TLS 1.3: eliptiskās līknes un atslēgu apmaiņa

> *Melnraksts:* Šī lekcija ir tikai plāns -- katrā nodaļā īsi aprakstīts, kāds materiāls tur
> varētu būt. Paredzētais apjoms: 90 minūtes auditorijā un daži mājas uzdevumi. Lekcija aplūko
> TLS 1.3 *asimetrisko* daļu: atslēgu apmaiņu (ECDHE), parakstus (ECDSA) un sertifikātus.
> Simetriskā daļa (AES-GCM, HKDF) ir iepriekšējā lekcijā.

**Mācīšanās rezultāti:**

* Saskaitīt punktus uz eliptiskās līknes virs galīga lauka $\mathbb{F}_p$ un aprēķināt
  skalāro reizinājumu $kG$ ar dubultošanas un saskaitīšanas algoritmu.
* Paskaidrot Difija-Helmana atslēgu apmaiņas ideju un to, kāpēc TLS 1.3 lieto tikai
  īslaicīgās (*ephemeral*) atslēgas (ECDHE).
* Parakstīt un pārbaudīt ziņojumu ar ECDSA (uz mazas līknes) un paskaidrot, kāpēc nonce $k$
  atkārtošana atklāj privāto atslēgu.
* Saprast un ar komandrindas rīkiem pārbaudīt, kā veidotas TLS sertifikātu ķēdes; 
  saprast secību no CSR līdz publiskam sertifikātam.


## Ievads: atslēgu apmaiņas (key agreement) uzdevums

TODO: Te būtu paskaidrots, kā divas puses, kas nekad nav tikušās, var publiskā tīklā vienoties par kopīgu
slepenu atslēgu, ko pēc tam izmanto AES-GCM. Varētu pieminēt vēsturi (Diffie-Hellman, 1976;
RSA, 1977; eliptisko līkņu kriptogrāfija -- Koblitz un Miller, 1985).

### Vienvirziena funkcijas un diskrētais logaritms

TODO: Definēts jēdziens *vienvirziena funkcija*: $x \mapsto g^x \bmod p$ ir viegli aprēķināma (ar ātro
kāpināšanu), bet apgrieztā funkcija -- *diskrētais logaritms* -- ir grūta.

**Difija-Helmana atslēgu apmaiņas piemērs:**

TODO: Protokols cikliskā grupā (šoreiz - multiplikatīvā grupa atlikumiem pēc 
pirmskaitļa) ar ģeneratoru $g$: Alise izvēlas slepenu $a$ un nosūta $A = g^a$,
Bobs izvēlas slepenu $b$ un nosūta $B = g^b$, un abi aprēķina $g^{ab} = B^a = A^b$.
Te būtu skaitlisks piemērs grupā $\mathbb{Z}_{23}^{\ast}$ ar $g = 5$: ja $a = 6$, $b = 15$, tad
$A = 8$, $B = 19$, un kopīgais noslēpums ir $8^{15} \equiv 19^{6} \equiv 2 \pmod{23}$. Varētu
paskaidrot, kāpēc noklausītājs, kas zina $p, g, A, B$, nevar viegli atrast $2$.

TODO: Izmantojot Python un (vēlams0 Matplotlib, izveidot SVG attēlu, kurā visi 23 atlikumi (ar atsevišķi 
apzīmētu 0 elementu, kurš nepiedalās) ir izrakstīti pa apli un savienoti ar 
lauztu līniju, atbilstoši ģeneratora $g=5$ pakāpēm. Aplītī ierakstīta kārta jeb diskrētais logaritms, 
bet pa "ciparnīcas" ārpusi - paši skaitļi no $0$ līdz $22$ regulāra $23$-stūra virsotnēs.
(Python un SVG noglabāt apakšdirektorijā /figs)


**Ģeneratora reizināšana ar veselu skaitli:**

TODO: Te būtu paskaidrota pamatideja: ja grupas operāciju raksta kā saskaitīšanu, tad $g^a$
vietā raksta $aG = G + G + \ldots + G$ ($a$ reizes), un DH protokols kļūst par $A = aG$, $B = bG$,
$abG = aB = bA$. Šis aditīvais pieraksts tieši atbilst eliptiskajām līknēm.

**Cilvēks pa vidu (man-in-the-middle):**  

TODO: Rindkopa, kurā paskaidrots, ka bez autentifikācijas DH ir neaizsargāts pret uzbrucēju, kas izveido divas
atsevišķas atslēgas ar katru pusi. Tas motivē parakstus un sertifikātus (nodaļas zemāk).


## Eliptiskās līknes virs galīga lauka

TODO: Te būtu līkne Veierštrāsa formā $y^2 = x^3 + ax + b$ virs $\mathbb{F}_p$ (ar $4a^3 + 27b^2 \neq 0$)
un tās punkti kopā ar bezgalīgi tālo punktu $\mathcal{O}$. Varētu parādīt līknes attēlu virs reālajiem
skaitļiem. 

**Punktu saskaitīšana:**

TODO: Te būtu ģeometriskā "hordas un pieskares" konstrukcija un formulas
$\lambda = \frac{y_2 - y_1}{x_2 - x_1}$ (saskaitīšana) vai $\lambda = \frac{3x_1^2 + a}{2y_1}$
(dubultošana), $x_3 = \lambda^2 - x_1 - x_2$, $y_3 = \lambda(x_1 - x_3) - y_1$. Varētu pieminēt,
ka punkti veido Ābela grupu ar neitrālo elementu $\mathcal{O}$.
(Python attēls ar Matplotlib - tsk. ar pieskari un saskaitītiem punktiem. 
(Python un SVG noglabāt apakšdirektorijā /figs)). 

### Mazs piemērs: līkne virs F_17

TODO: Klasiskais piemērs $y^2 = x^3 + 2x + 2$ virs $\mathbb{F}_{17}$ ar ģeneratoru $G = (5, 1)$:
$2G = (6, 3)$, $3G = (10, 6)$, $4G = (3, 1)$, ..., un $19G = \mathcal{O}$, tātad grupas kārta ir $19$.
Šajā mazajā grupā varētu izspēlēt ECDH un ECDSA ar rokām.

### Skalārā reizināšana: dubultošana un saskaitīšana

TODO: Te būtu algoritms $\textsf{Scalar-Mult}(k, P)$, kas aprēķina $kP$ ar $O(\log k)$ grupas operācijām,
ejot pa $k$ bitiem (analogs ātrajai kāpināšanai). 
Algoritma pseidokods pierakstīts Cormen-Leiserson-Rivest-Stein
grāmatas stilā.

### Eliptisko līkņu diskrētā logaritma problēma

TODO: Te būtu paskaidrots, ka, zinot $P$ un $Q = kP$, atrast $k$ ir grūti (labākie zināmie algoritmi,
piemēram, Polarda $\rho$, prasa apmēram $\sqrt{n}$ soļus). Tāpēc 256 bitu līkne dod apmēram
128 bitu drošību, bet RSA tādai pašai drošībai vajag apmēram 3072 bitu moduli.


### Montgomerija kāpnes

TODO: Neliels piemērs ar Montgomerija kāpnēm
(*Montgomery ladder*), kas katram bitam izpilda vienādas operācijas.
Sagatavot 12.4 uzdevumam līdzīgu piemēru - ar ne visai lieliem skaitļiem (daži simti).
Paskaidrot, kā Montgomerija kāpnes var palīdzēt EC aprēķinos.




## NIST P-256 līkne

TODO: Te būtu P-256 (secp256r1) parametri: $p = 2^{256} - 2^{224} + 2^{192} + 2^{96} - 1$, $a = -3$,
konstante $b$, ģenerators $G$ un pirmskaitļa kārta $n$ (kofaktors $1$). Varētu paskaidrot, kāpēc
$p$ izvēlēts šādā formā (ātra modulārā redukcija) un kāpēc $a = -3$ paātrina dubultošanu.

**Punktu kodēšana:**  
TODO: Rindkopa, kas paskaidro, kā punktu pārraida TLS ziņojumā: nesaspiestā formā `04 || x || y`
(65 baiti) vai saspiestā formā (tikai $x$ un $y$ paritāte). Varētu parādīt, kā no $x$ atjauno $y$,
izvelkot kvadrātsakni pēc moduļa $p$.

**Citas TLS 1.3 grupas:**  
TODO: Rindkopa, kurā pieminēta līkne X25519 (Montgomerija forma, Bernstein, 2006), kas TLS 1.3 ir
izplatītākā, kā arī P-384 un galīgo lauku DH grupas (`ffdhe2048` u.c.). Pieminēts, ka
X25519 ir vieglāk implementēt drošā veidā ar īsu intuitīvu paskaidrojumu, kāpēc.


## ECDHE atslēgu apmaiņa TLS 1.3

TODO: Te būtu parādīts, kā klients ziņojumā `ClientHello` (paplašinājumā `key_share`) nosūta $aG$,
serveris ziņojumā `ServerHello` -- $bG$, un abi aprēķina $abG$, kura $x$ koordināti ievada HKDF
atslēgu grafikā.

### Īslaicīgās un statiskās atslēgas

TODO: Te būtu atbilde uz jautājumu par atslēgu veidiem: TLS 1.3 atslēgu apmaiņā lieto tikai
*īslaicīgās* atslēgas (jaunas katram savienojumam), bet servera *statiskā* atslēga (no sertifikāta)
tiek lietota tikai parakstam ziņojumā `CertificateVerify`. Varētu salīdzināt ar TLS 1.2, kur bija
atļauta statiskā RSA atslēgu transportēšana un statiskais ECDH.
Pierakstīt, kuros gadījumos lietots $C(0s,2e)$ un kuros gadījumos $C(2s,2e)$ algoritma variants.

### Rokasspiediena pārskats

TODO: Te būtu vienkāršota TLS 1.3 pilnā rokasspiediena shēma (1-RTT): `ClientHello`, `ServerHello`,
`EncryptedExtensions`, `Certificate`, `CertificateVerify`, `Finished`. Varētu atzīmēt, kuri ziņojumi
jau ir šifrēti un kurā brīdī katra puse zina kopīgo noslēpumu.


**Uz priekšu vērstā slepenība:**  
TODO: Rindkopa, kur paskaidrota *uz priekšu vērstā slepenība* (*forward secrecy*): ja servera ilgtermiņa
privātā atslēga vēlāk nonāk uzbrucēja rokās, iepriekš ierakstītos savienojumus tas tik un tā nevar
atšifrēt. Tas ir galvenais iemesls, kāpēc TLS 1.3 atteicās no statiskajām atslēgu apmaiņām.



## ECDSA paraksti

TODO: Izstāstīts ECDSA algoritms: privātā atslēga $d$, publiskā atslēga $Q = dG$; paraksts ir pāris
$(r, s)$, kur $r = (kG)_x \bmod n$ un $s = k^{-1}(h + rd) \bmod n$ ar nejaušu nonce $k$ un
ziņojuma hešu $h$. Pārbaude aprēķina $u_1 G + u_2 Q$ un salīdzina tā $x$ koordināti ar $r$.
(ECDSA paraksta un arī paraksta pārbaudes algoritmu pseidokods Cormen-Leiserson-Rivest-Stein
grāmatas stilā. Sk. pseidokodu citās lekcijās.)

### ECDSA piemērs mazā grupā

TODO: Te būtu ECDSA parakstīšana un pārbaude līknei 
$y^2 \equiv x^3 + x + 4 \pmod{23}$ virs $GF(p)$, kur $p = 23$. 
Grupas kārta $n=29$. 
Vēlams, lai visus soļus varētu izsekot ar rokām.
Lūdzu pievienot apakšdirektorijā Python skriptu, kas ģenerē Matplotlib attēlu (SVG formātā), 
kurā būtu attēlots režģis ar visiem $(x,y)$ pāriem - un pāri, kuri atrodas uz līknes - atzīmēti ar 
aplīšiem.
(Ja nepieciešams, var pievienot arī linku uz kādu tiešsaistes rīku, kurā var operēt ar šo līkni.
Ja ir cita līkne demonstrācijām, kurai ir vieglāk atrodami tiešsaistes demo, var ņemt arī to.)

### Paraksti TLS 1.3

TODO: Te būtu paskaidrots, ko paraksta `CertificateVerify` (rokasspiediena ziņojumu hešu) un kādas
paraksta shēmas TLS 1.3 atļauj: `ecdsa_secp256r1_sha256`, `rsa_pss_rsae_sha256`, `ed25519` u.c.
Varētu pieminēt deterministisko nonce izvēli pēc RFC 6979.


## TLS sertifikāti

TODO: Aprakstīt procesu vairākos soļos, kurus lietotāji var atkārtot un pārskatīt.
Izklāstīt X.509 sertifikāta saturu (subjekts, publiskā atslēga, izdevējs, derīguma termiņš, paraksts). 
Kā lietotājs izveido publiskās/privātās atslēgas pāri, izveido paku ar
sertifikāta domēna informāciju un publisko atslēgu un paraksta to ar savu privāto atslēgu, 
iegūstot CSR.  Sertifikāta (DER vai PEM) apskatīšana; ASN.1 datu struktūru 
skatītājs [https://lapo.it/asn1js/](https://lapo.it/asn1js/). 
Sertifikāta parakstīšanas pieprasījuma parakstīšana, iegūstot uzticības ķēdi 
līdz saknes sertificēšanas iestādei, kas iekonfigurēta pārlūkprogrammā. 
Katru soli īsi definēt (un tur, kur nepieciešams, pierakstīt arī komandrindu - vai kādu 
citu rīku, ar kuru kaut ko izdarīt/pārbaudīt).

TODO: Vienā atsevišķā rindkopā (vai sarakstā ar apakšpunktiem) piedāvāt 
arī praktisku īsu kopsavilkumu, kā šo uzlikt bez maksas
ar Let's Encrypt un certbot iekonfigurēšanu savā web lapā - tā, lai ik pēc 3 mēnešiem 
sertifikāts atjaunotos (uzrakstot pieņēmumus, kad tas ir iespējams).

**Sertifikātu pārbaude un atsaukšana:** 
TODO: Te varētu īsi pieminēt sertifikātu caurspīdīguma žurnālus (*Certificate Transparency*)
vai Certificate Revocation lists, OCSP
atbildes un to, ka sertifikātu derīguma termiņi pakāpeniski tiek saīsināti.



### RSA un EC sertifikātu salīdzinājums

TODO: Tabula, kas salīdzina RSA-2048/RSA-3072 un ECDSA P-256 sertifikātus: publiskās atslēgas
un paraksta izmērs (apmēram 256 baiti pret 64-72 baitiem), drošības līmenis un parakstīšanas un
pārbaudes ātrums (EC ātrāk paraksta, RSA ātrāk pārbauda). Varētu paskaidrot, kāpēc mazāki
sertifikāti ir svarīgi rokasspiediena latentumam.




## Postkvantu kriptogrāfija TLS 1.3

TODO: Te būtu paskaidrots, ka Šora algoritms kvantu datorā efektīvi atrisina gan sadalīšanu reizinātājos,
gan (eliptisko līkņu) diskrētā logaritma problēmu, tātad apdraud RSA, ECDH un ECDSA, bet AES un
SHA-256 pietiek ar lielāku atslēgas vai izvades garumu (Grovera algoritms).
Abiem algoritmiem (Šora un Grovera) doti intuitīvi apraksti, ko viņi izdara (un kādi resursi tam nepieciešami; 
vai sagaidāms atbilstošs skaits q-bitu). Katru var aprakstīt 1 rindkopā (bet pietiek ar intuīciju; 
nav formāli jādefinē šie algoritmi, jo kurss nav par kvantu skaitļošanu).


**Saglabā tagad, atšifrē vēlāk:** 
TODO: Viena rindkopa ar motivāciju, kāpēc atslēgu apmaiņu vajag aizsargāt jau tagad: uzbrucējs var ierakstīt
šifrētu datplūsmu un atšifrēt to nākotnē, kad būs pietiekami jaudīgs kvantu dators.

**ML-KEM un hibrīdā atslēgu apmaiņa:** 
TODO: Aprakstīt ML-KEM (FIPS 203, agrāk Kyber) kā atslēgu iekapsulēšanas mehānismu (KEM) un
hibrīdā grupa `X25519MLKEM768`, kurā kopīgais noslēpums ir abu algoritmu noslēpumu salikums.
Varētu pieminēt, ka atslēgas un šifrteksti ir ap 1 KB lieli, tāpēc `ClientHello` kļūst ievērojami garāks.

**Postkvantu paraksti:**  
TODO: īsi pieminēts ML-DSA (FIPS 204) un SLH-DSA (FIPS 205) un tas, kāpēc postkvantu sertifikāti
TLS ieviešas lēnāk nekā atslēgu apmaiņa (lieli paraksti, gara sertifikātu ķēde, nav steidzamības
"saglabā tagad, atšifrē vēlāk" dēļ).


## Asimetriskās kriptogrāfijas riski

TODO: Te būtu īss pārskats par uzbrukumiem, kuros pati matemātika nav salauzta, bet implementācija vai
parametru izvēle pieļauj kļūdu.

### Nederīgas līknes un mazas apakšgrupas uzbrukumi

TODO: Te būtu paskaidrots, ka saskaitīšanas formulas neizmanto koeficientu $b$, tāpēc implementācija,
kas nepārbauda, vai saņemtais punkts atrodas uz līknes, var tikt piespiesta rēķināt uz citas,
vājas līknes ar mazu kārtu (*invalid-curve attack*), un privāto atslēgu var atgūt pa daļām ar
Ķīniešu atlikumu teorēmu. Aizsardzība: punkta pārbaude un īslaicīgās atslēgas.
(Iespējams, tas nozīmē izklāstīt *Biehl–Meyer–Müller invalid-curve attack* - ar atbilstošu 
literatūras norādi. Un, arī Pohlig–Hellman algoritmu - ja tas 
ir tieši tas veids, kā izmantota ķīniešu atlikumu teorēma.)

**Vājas līknes:**
TODO: Ja nepieciešams, var pievienot dažas rindkopas, kur būtu pieminētas līkņu klases, 
kurām diskrētais logaritms ir viegls (anomālās līknes, līknes ar
mazu iegulšanas pakāpi -- MOV uzbrukums, gludas grupas kārtas), un diskusija par uzticēšanos
standartizētām konstantēm ("nekas piedurknē", Dual_EC_DRBG gadījums).

### Nonce atkārtošana un novirzīti nonce ECDSA

TODO: Te būtu parādīts, ka divi paraksti ar vienu un to pašu $k$ ļauj atrast $k$ un pēc tam privāto
atslēgu $d$ (Sony PlayStation 3, 2010), un ka pat dažu bitu novirze $k$ vērtībās ļauj režģu
uzbrukumus. Risinājums: deterministisks $k$ (RFC 6979) vai Ed25519.

### Sabojāts gadījumskaitļu ģenerators

TODO: Aprakstīt, kas kļūst pieejams uzbrucējam, ja viņam izdodas "nofiksēt" nejaušo skaitļu 
ģeneratora vērtības, nodarbojoties ar ECDSA (vai līdzīgu EC algoritmu). 

### Laika uzbrukumi skalārajai reizināšanai

TODO: Te būtu paskaidrots, kāpēc dubultošanas un saskaitīšanas algoritms ar zarošanos pēc atslēgas bitiem
nopludina atslēgu caur izpildes laiku, un kā to novērš konstanta laika implementācija vai Montgomerija kāpnes.

### Citi TLS 1.3 aspekti

**Uzticamās sertifikātu iestādes un TLS pārtveršana.** Pārlūkprogramma uzticas jebkuram sertifikātam, ko
parakstījusi kāda no simtiem saknes sertifikātu iestāžu (CA) operētājsistēmas vai pārlūka sarakstā. Uzņēmumos
administratori bieži pievieno savu saknes CA visiem datoriem (piemēram, ar Active Directory grupu politikām),
lai tīkla starpniekserveris varētu "pārtvert" TLS: tas izveido viltotu sertifikātu katrai vietnei, atšifrē
satiksmi un pārbauda to. Tas ir likumīgs *cilvēks pa vidu* (*man in the middle*), bet tas kļūst bīstams, ja
CA privātā atslēga noplūst vai ja starpniekserveris pats slikti pārbauda īstos sertifikātus vai izvēlas vājus
algoritmus. Bīstamākie gadījumi: 2011.gadā uzlauztā CA DigiNotar izdeva viltotus `*.google.com` sertifikātus,
ar kuriem noklausījās lietotājus Irānā; 2015.gadā Lenovo klēpjdatoros iepriekš instalētā reklāmu programma
Superfish visos datoros pievienoja saknes CA ar **vienu un to pašu** privāto atslēgu. Aizsardzība: *Certificate
Transparency* (visi publiski izdotie sertifikāti jāieraksta publiskos žurnālos), atslēgu piespraušana lietotnēs
(*pinning*), stingra korporatīvo saknes CA pārvaldība.

**Klientu sertifikāti un pārbaudes apiešana.** Abpusējā TLS (*mutual TLS*, mTLS) arī klients uzrāda sertifikātu
un paraksta CertificateVerify -- to lieto, piemēram, mikroservisos, bankas API un IoT ierīcēs. Lai katru reizi
neveiktu pilnu CA ķēdes un atsaukšanas pārbaudi, sistēmas mēdz to apiet: sesijas atjaunošana ar PSK pārmanto
iepriekšējā rokasspiediena klienta identitāti (biļete var būt derīga līdz $7$ dienām), serveris var kešot pārbaudes
rezultātu vai "piespraust" klienta publiskās atslēgas SHA-256 nospiedumu un pieņemt pašparakstītu sertifikātu
(tā dara, piemēram, Syncthing un daudzas IoT platformas). Tas ir ātri, bet atsaukts sertifikāts vai nozagta
ierīces atslēga var palikt derīga līdz kešatmiņas vai biļetes derīguma beigām, tāpēc šie termiņi jāizvēlas
apzināti un jāļauj tos piespiedu kārtā anulēt.

TODO: Te varētu pieminēt pazemināšanas (*downgrade*) aizsardzību `ServerHello.random` laukā, 0-RTT datu
atkārtošanas risku sesiju atsākšanā ar PSK un `ClientHello` šifrēšanu (*Encrypted Client Hello*),
kas paslēpj apmeklētā servera vārdu.



## Uzdevumi

TODO: Katram no uzdevumiem papildināt trūkstošos nosacījumus un pierakstīt 
atrisinājumus/atbildes. 
Atrisinājumos/atbildēs, kur nepieciešams, pievienot SVG attēlus, kuri 
parāda, kā notiek G elementa saskaitīšana pašam ar sevi (x un y koordinātēs) - 
var numurēt punktus uz līknes, ierakstot numurus aplīšos.
Montgomerija kāpnēm arī ieteicama vizualizācija. 
(SVG attēlus veidot ar Python skriptiem un vēlams Matplotlib, 
ko ievietot /figs apakšdirektorijā kopā ar 
uzģenerētajiem SVG attēliem - tā, lai lietotājs varētu pamainīt latviešu/angļu valodai 
specifiskus stringus nosaukumos.)

**12.1. uzdevums:**  
Uz līknes $y^2 = x^3 + 2x + 2$ virs $\mathbb{F}_{17}$ aprēķināt $5G$ un $13G$ 
ar dubultošanas un saskaitīšanas algoritmu. 
TODO: Atgādināt, kas šajā kontekstā ir $G$. (Ja tas palīdz izklāstam, var 
GF(17) vietā izvēlēties arī citu lauku - varbūt ar nedaudz lielāku izmēru, bet 
nepārsniedzot 32.)

**12.2. uzdevums:**  
Augšminētjai līknei veikt ECDH atslēgu apmaiņu slepenajiem skaitļiem $a$ un $b$. 
Pārbaudīt, ka abām pusēm sanāk tas pats punkts.

**12.3. uzdevums:**  
Parakstīt ziņojuma hešu ar ECDSA mazajā grupā un pārbaudīt parakstu.

**12.4. uzdevums:**  
Uzrakstīt skaitliskus piemērus, lai iepazītos ar Montgomerija kāpnēm 
kā efektīvu EC aritmētikas implementāciju. Pārbaudīt uz kādas 
līknes (vēlams - nedaudz lielākā laukā nekā $\mathbb{F}_{17}$ - kur skaitļi 
būtu dažus simtus lieli - lai varētu aprēķināt uz kalkulatora, bet
nerastos priekšstats, ka Montgomerija redukcija strādāja dīvainas sagadīšanās dēļ.)

**12.5. uzdevums:**  
Doti divi ECDSA paraksti ar vienu un to pašu $k$ -- atrast privāto atslēgu $d$.

**12.6. uzdevums:**  
Salīdzināt TLS 1.3 rokasspiediena apjomu baitos ar RSA-2048 un ar ECDSA P-256 sertifikātu ķēdi.


## Izmantotā literatūra

TODO: Te būtu avotu saraksts, piemēram: RFC 8446 (TLS 1.3), NIST FIPS 186-5 (ECDSA), NIST SP 800-186
(līkņu parametri), SEC 1 un SEC 2 (Certicom), RFC 7748 (X25519), RFC 6979, NIST FIPS 203-205
(postkvantu standarti), C.Paar, J.Pelzl, *Understanding Cryptography* (Springer) un
D.Hankerson, A.Menezes, S.Vanstone, *Guide to Elliptic Curve Cryptography*.
