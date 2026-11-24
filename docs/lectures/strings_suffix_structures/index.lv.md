---
layout: default
title: "Sufiksu koki un sufiksu masīvi"
lang: lv
permalink: /lectures/strings_suffix_structures/lv/
---
# 14. Sufiksu koki un sufiksu masīvi

Šajā nodaļā aplūkojam datu struktūras, kas ļauj vienā un tajā pašā tekstā ātri meklēt daudzus dažādus paraugus:

1. Kas ir "trie" jeb burtu koki (traji). Saspiestie traji.
2. Sufiksu traji, sufiksu koki un sufiksu masīvi.
3. Dokumentu meklēšana.
4. Sufiksu koku iegūšana lineārā laikā.

## Vienreizēja un atkārtota meklēšana

**Stringu meklēšanas problēma:** Dotas divas virknes (teksts $T$ un paraugs $P$) kādā alfabētā $\Sigma$. Jāatrod dažas vai visas nobīdes, kurās $P$ sakrīt ar $T$ (vai jāsaskaita tās). Vēlamies atrast arī savstarpēji pārklājošos parauga parādījumus. (Varianti -- meklēt regulāras izteiksmes vai citus paraugus, aptuvenu sakritību.)

**Optimāli algoritmi vienreizējai meklēšanai:**

* Knuta-Morisa-Prata algoritms
* Bojera-Mūra algoritms
* Rabina-Karpa algoritms

Visi sasniedz lineāru laiku no teksta garuma. (Tie veic *parauga* priekšapstrādi -- izrēķina prefiksu funkciju, labā sufiksa funkciju, sliktā simbola funkciju vai parauga hešfunkciju; sk. [13. Stringu meklēšana]({{ '/lectures/strings_search/' | relative_url }}).)

**Atkārtotā meklēšana (datu struktūru uzdevums):** Uzdevums ir identisks, bet apgriezts: teksta dokuments $T$ nemainās, un tajā jāmeklē visādi paraugi $P$. Tāpēc veic *teksta* $T$ priekšapstrādi, un pēc tam atbild uz vaicājumiem ar dažādiem paraugiem $P$.

* Vienai meklēšanai gribam tērēt $O(|P|)$ laiku (meklējamo paraugu vienreiz jāizlasa), nevis $O(|T|)$ laiku (katrreiz no jauna skriet cauri tekstam).
* Gribam $O(|T|)$ vietu, lai nav jāglabā daudz lielāka datu struktūra nekā pats teksts.

## Traji

* Trajs (*trie*) ir koks, kas glabā nevis pilnas atslēgas (kā binārās meklēšanas koks), bet dala atslēgu sīkāk, izmantojot tās struktūru. Tas ir sakņots koks, kura šķautnes marķētas ar alfabēta $\Sigma$ burtiem.
* Stringu gadījumā trajs analizē meklējamo stringu pa atsevišķiem burtiem.
* Sufiksu traji ļauj atbildēt uz vairākiem interesantiem vaicājumiem.
* Lai traji neaizņemtu pārāk daudz vietas, tos reizēm saspiež, iegūstot *sufiksu kokus*.

### Priekšteča problēma

**Uzdevums:** Priekšteča problēma ([Predecessor problem](https://en.wikipedia.org/wiki/Predecessor_problem)): Doti teksta gabali $T_1<T_2 <\ldots <T_k$ (alfabētiski sakārtoti) un arī meklējamais paraugs $P$. Atrast priekšteci un sekotāju:

* $\text{predecessor}(P)$ - lielāko indeksu $i$, kuram $T_i \leq P$.
* $\text{successor}(P)$ - mazāko indeksu $j$, kuram $T_j \geq P$.

Priekšteča meklēšanas uzdevums ir praktiski noderīgs: ievadām kādu virknes prefiksu un vēlamies redzēt grāmatas nosaukumu, kas alfabētiskā katalogā ir tūlīt pirms vai aiz tā.

Vai to atrisina binārie meklēšanas koki? Virknes var sakārtot vai uzbūvēt bināro meklēšanas koku, bet tas ir neefektīvi, jo divu virkņu salīdzināšana var aizņemt ilgu laiku.

Tāpēc virknes $T_i$ attēlo kā ceļus trajā no saknes līdz lapai. Saknei pievieno bērnus, kas apzīmēti ar alfabēta burtiem (teiksim, $26$ alfabēta burtiem). Katras virknes beigās pievieno jaunu simbolu (dolāru $\mathtt{\$}$), kas nepieder alfabētam.

**Piemērs:** Trajs virknēm $\lbrace \mathtt{ANA}, \mathtt{ANN}, \mathtt{ANNA}, \mathtt{ANNE} \rbrace$ ir veidots 4 burtu alfabētā (burtiem $\mathtt{A}, \mathtt{E}, \mathtt{N}$ pievienojam $\mathtt{\$}$ simbolu). Izveidotajā trajā ar $O(|P|)$ soļiem var atrast alfabētisko priekšteci un alfabētisko pēcteci: nonāk līdz vietai, kur $P$ "nokrīt" no traja, un tur atrod maksimālo lapu vienā apakškokā un minimālo lapu otrā apakškokā. Minimumu un maksimumu var uzglabāt katrā mezglā.

### Kā attēlot traja mezglus

Ja alfabēts $\Sigma$ ir liels, svarīgi, kā glabāt viena traja mezgla bērnus. Tipiskie risinājumi ir masīvs, koks un heštabula. Šeit $T = T_1+\ldots +T_k$ (visu tekstu kopgarums):

| Mezgla attēlojums | Vaicājuma laiks | Vieta |
| --- | --- | --- |
| Masīvs (garumā $\lvert\Sigma\rvert$) | $O(\lvert P\rvert)$ | $O(\lvert T\rvert \cdot \lvert\Sigma\rvert)$ |
| Binārās meklēšanas koks | $O(\lvert P\rvert \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |
| Heštabula | $O(\lvert P\rvert)$ | $O(\lvert T\rvert)$ |
| Van Emde Boasa koks (vEB koks) | $O(\lvert P\rvert \cdot \log \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |
| "Treji" (*trays*) | $O(\lvert P\rvert + \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |

Heštabula ir labākā no abām pasaulēm (vaicājums $O(|P|)$ un vieta $O(|T|)$), tomēr tā neatrisina priekšteča sameklēšanas problēmu, jo sajauc burtu kārtību.

M.Farahs-Koltons (*Martin Farach-Colton*) izmantoja LCA (zemāko kopīgo priekšteci) un svara līdzsvarotu bināro meklēšanas koku (katra mezgla svars ir visu tā pēcnācēju lapu skaits). Tas sasniedz $O(|P| + \log_2 k)$ laiku, kur $k$ ir tekstu skaits.

### Saspiestais trajs

Saspiestajā trajā ceļus bez sazarošanās aizstāj ar vienu šķautni, uz kuras uzrakstīta vesela virkne. Uz šķautnes nav jāuzglabā visa virkne (meklējot pa šķautni, var "nokrist no koka" tās vidū). Saspiestajā trajā ir $O(k)$ mezgli (visi mezgli, izņemot sakni un lapas, ir mezgli, kuros notiek sazarošanās), un tajā joprojām var veikt visas tās pašas meklēšanas.

## Sufiksu traji

**Definīcija:** Teksta $T$ *sufiksu trajs* ir trajs, kurā ievietoti visi $T$ sufiksi $T[i:]$, katru no tiem noslēdzot ar īpašu simbolu -- dolāru $\mathtt{\$}$, kas nepieder alfabētam.

<img
  alt="Sufiksu trajs vārdam abaaba"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Sufiksa beigu apzīmējums:** Ja dolārus sufiksu beigās nelietotu, vairs neeksistētu 1:1 atbilstība starp koka lapām un sufiksiem, un daži lietojumi kļūtu neiespējami (nevarētu atšķirt, vai virkne ir sufikss vai arī iekšējs apakšstrings). Šī īpašība ir būtiska; $\mathtt{\$}$ tiks lietoti visur (reizēm tos atzīmē, iekrāsojot koka lapas).

<img
  alt="Sufiksu trajs vārdam abaaba bez dolāriem"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-no-dollars.png' | relative_url }}"
  style="width: 100%; max-width: 180px; border:none; background-color:#FFFFFF;"
/>

### Sufiksa links

* Katra lapa ir kāds sufikss.
* Katrs mezgls ir kāda sufiksa prefikss.
* Mezgla *sufiksa links* (*suffix link*) norāda uz tāda sufiksa prefiksu, kuram pirmais burts ir nodzēsts.

**Piemērs:** Gan $\mathtt{aab}$, gan $\mathtt{ab}$ ir vārda $\mathtt{abaaba}$ sufiksu prefiksi. Mezgla $\mathtt{aab}$ sufiksa links rāda uz $\mathtt{ab}$ (attēlā -- sarkanā bultiņa).

<img
  alt="Sufiksu links sufiksu trajā vārdam abaaba"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-suffix-links.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

### Traju rekursīva veidošana

Sufiksu traju var veidot, pievienojot teksta burtus pa vienam: no $\textsf{SufTrie}(\mathtt{abba})$ iegūst $\textsf{SufTrie}(\mathtt{abbac})$, ja visiem līdzšinējiem sufiksiem (sākot ar garāko) pievieno jauno burtu. Visu sufiksu beigu mezglus var apstaigāt pa sufiksu linkiem.

<img
  alt="Sufiksu traju rekursīva veidošana: SufTrie(abba) un SufTrie(abbac)"
  src="{{ '/lectures/strings_suffix_structures/figs/building-tries.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**Robežas pavirzīšana tālāk:** Ceļu pa sufiksu linkiem no garākā sufiksa beigām (*longest*) sauc par *robežceļu* (*boundary path*). Pievienojot burtu $s[i]$, iet pa robežceļu, katram mezglam pievieno jaunu bērnu ar burtu $s[i]$ un savieno jaunos mezglus ar sufiksu linkiem. Apstāties var, kad sasniegts mezgls (*current*), kuram jau ir bērns ar burtu $s[i]$.

<img
  alt="Robežceļa pavirzīšana tālāk"
  src="{{ '/lectures/strings_suffix_structures/figs/boundary-path.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**Viens pilns piemērs:** Sufiksu traja veidošana vārdam $\mathtt{abaaba\$}$, pievienojot burtus pa vienam.

<img
  alt="Sufiksu traja veidošana vārdam abaaba$"
  src="{{ '/lectures/strings_suffix_structures/figs/building-tries-dollar-at-end.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

## Sufiksu traju lietojumi

**Apakšstringa pārbaude:** Pārbaudīt, vai strings $Q$ ir teksta $T$ apakšstrings. Sāk traja saknē, seko parauga $Q$ burtiem. Ja to visu var trajā nolasīt, "neizkrītot" no tā, tad $Q$ ir $T$ apakšstrings.

**Piemērs:** Vai $\mathtt{baa}$ ir $\mathtt{abaaba}$ apakšstrings? Sekojam burtiem paraugā $\mathtt{baa}$. Pēc sufiksu traja izveides vaicājuma ilgums ir vienāds ar paša vaicājuma garumu $O(|Q|)$, pat ja teksts ir ļoti garš.

<img
  alt="Apakšstringa baa meklēšana sufiksu trajā"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-search-baa.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Sufiksa pārbaude:** Pārbaudīt, vai strings $Q$ ir teksta $T$ sufikss. Sāk traja saknē, seko parauga $Q$ burtiem. Ja to visu var trajā nolasīt un pēc tam pa $\mathtt{\$}$ šķautni nonākt lapā, tad tas ir sufikss.

**Piemērs:** Vai $\mathtt{baa}$ ir $\mathtt{abaaba}$ sufikss? No saknes meklējam uz leju (kamēr "nokrītam" no traja vai sasniedzam parauga beigas). Ja no sasniegtā mezgla iziet $\mathtt{\$}$ šķautne uz lapu, tad tas bija sufikss.

<img
  alt="Sufiksa pārbaude sufiksu trajā"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-suffix.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Eksemplāru saskaitīšana:** Saskaitīt, cik reizes paraugs $Q$ ietilpst tekstā $T$. Seko parauga $Q$ ceļam no saknes. Atkārtojumu skaits sakrīt ar lapu skaitu zem virsotnes, kurā nonāk.

**Piemērs:** Saskaitīt, cik reizes tekstā $\mathtt{abaaba}$ ietilpst $\mathtt{aba}$. Vai nu "nokrīt" no traja -- tad atbilde ir $0$, vai arī atrod virsotni $n$, zem kuras var saskaitīt lapas (šeit $2$).

<img
  alt="Parauga aba parādījumu skaitīšana sufiksu trajā"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-count.png' | relative_url }}"
  style="width: 100%; max-width: 300px; border:none; background-color:#FFFFFF;"
/>

**Garākais atkārtojums:** Atrast garāko paraugu $P$, kurš tekstā $T$ ietilpst atkārtoti. Jāatrod dziļākā virsotne, zem kuras ir vismaz $2$ lapas.

**Pirmais sufikss:** Atrast leksikogrāfiski (alfabētiski) mazāko sufiksu. Sāk saknē, ikreiz sekojot šķautnei, kas apzīmēta ar leksikogrāfiski mazāko burtu.

## Sufiksu koki

**Sliktākais traja gadījums:**

* Ja strings ir $S = \mathtt{a}^n\mathtt{b}^n$, tad dažādo apakšstringu (ieskaitot tukšo) ir $n(n+1) + n+1$ jeb $O(n^2)$, un sufiksu trajā ir tikpat daudz mezglu.
* Stringam garumā $n$ vispār ir ne vairāk kā $O(n^2)$ apakšstringi, bet tie visi var parādīties.
* Praksē sastopamiem tekstiem traja izmērs arī aug kvadrātiski (parasti drusku lēnāk nekā sliktākajā gadījumā), bet aizņemtā atmiņa ir milzīga.

<img
  alt="Sufiksu trajs vārdam aaabbb"
  src="{{ '/lectures/strings_suffix_structures/figs/large-suffix-tree.png' | relative_url }}"
  style="width: 100%; max-width: 300px; border:none; background-color:#FFFFFF;"
/>

**Sufiksu koki:** Tie ir saspiesti sufiksu traji.

* Saspiež ceļus, kuros nav izvēles.
* Lapu arvien ir $|T|$, bet katrā iekšējā mezglā notiek zarošanās.
* Tāpēc iekšējo mezglu skaits nepārsniedz lapu skaitu, un kopējais mezglu skaits ir $O(|T|)$.
* Šķautņu virknes neizraksta, bet glabā kā indeksu pāri tekstā $T$, tāpēc aizņemtā vieta ir $O(|T|)$.
* Efektīvs Ukonena (*Ukkonen*) algoritms sufiksu koku uzbūvē $O(|T|)$ laikā.

<img
  alt="Sufiksu koks vārdam abaaba$"
  src="{{ '/lectures/strings_suffix_structures/figs/suffix-tree.png' | relative_url }}"
  style="width: 100%; max-width: 350px; border:none; background-color:#FFFFFF;"
/>

**Piemērs:** Aplūkojam tekstu $T$ un visus tā sufiksus $T[i:]$. Dolāra zīmi pievienojam vienreiz -- $T$ beigās. Tad tā parādīsies visos sufiksos:

```text
banana$
0123456
```

Tukšā virkne nav jāuzglabā (tikai dolāra zīme). Lapās ierakstīti sufiksu sākuma indeksi, raustītās bultiņas ir sufiksu linki.

<img
  alt="Sufiksu koks vārdam banana$"
  src="{{ '/lectures/strings_suffix_structures/figs/suffix-tree-banana.png' | relative_url }}"
  style="width: 100%; max-width: 288px; border:none; background-color:#FFFFFF;"
/>

Šajā kokā var meklēt $\mathtt{nan}$, $\mathtt{an}$ vai pat $\mathtt{ana}$ (divi pārklājoši parādījumi). Šī datu struktūra meklē lineārā laikā no parauga garuma.

### Sufiksu koku lietojumi

* Parauga $P$ meklēšana dod apakškoku, kura lapas atbilst visiem $P$ parādījumiem tekstā $T$. Tās var saskaitīt, sekot saistītajam lapu sarakstam, atrast pirmos $10$ parādījumus. No apakškoka saknes var "teleportēties" uz tā lapām.
* Cik liela ir struktūra? Lapu skaits ir $|T|$; tā kā visi iekšējie mezgli ir zarojošie mezgli, arī kopējais mezglu skaits ir $O(|T|)$. Ar "trejiem" (*trays*) meklēšanas laiks ir $O(|P| + \log_2 |\Sigma|)$.
* Atrast pirmos $k$ parauga parādījumus.
* Saskaitīt, cik reizes $P$ parādās tekstā $T$.
* Ja $T$ ir ļoti garš dokuments (piemēram, Merriam-Webster vārdnīca), atrast garāko apakšstringu, kas tajā parādās vismaz divas reizes. (Jāatrod mezgls ar lielāko "burtu dziļumu", zem kura ir vismaz divas lapas.)
* Doti divi sufiksi (pozīcijas $i$ un $j$ tekstā) -- noskaidrot, cik garā prefiksā tie sakrīt. To var noteikt konstantā laikā -- jāatrod abu lapu zemākais kopīgais priekštecis (LCA), un tā burtu dziļums ir garākais kopīgais prefikss:

  $$
  \mathrm{lcp}(\mathtt{T[i:]}, \mathtt{T[j:]}) = \text{burtu dziļums}\left(\mathrm{LCA}(i, j)\right).
  $$

* Visu $T[i:j]$ parādījumu atrašana gandrīz konstantā laikā. Lieto LA (*level ancestor* -- līmeņa priekšteča) vaicājumu: vispirms dodas uz lapu $i$, tad lec uz augšu līdz priekštecim ar burtu dziļumu $j-i$. Šim nolūkam var izmantot *lēkšanas rādītājus* (*jump pointers*) vai *kāpņu dekompozīciju* (*ladder decomposition*). Ja vaicājumi zināmi iepriekš, tos var apstrādāt jau iepriekš, pievienojot tekstam.

**Definīcija:** *Zemākais kopīgais priekštecis* (*lowest common ancestor*, LCA) diviem koka mezgliem (iekšējiem mezgliem vai lapām) ir dziļākais mezgls, kas ir abu priekštecis -- vieta, kur abu ceļi no saknes atzarojas.

### Vispārinātie sufiksu koki

Vairākus dokumentus attēlo, savienojot tos vienā tekstā un aiz katra pievienojot savu dolāra zīmi:

$$
T = T_1\mathtt{\$}_1T_2\mathtt{\$}_2\cdots{}T_k\mathtt{\$}_k.
$$

Dažādus dolārus izmanto, lai katrs sufikss beigtos ar unikālu simbolu un no lapas varētu noteikt, kuram dokumentam tā pieder.

**Piemērs:** Vārdi $\mathtt{at}$, $\mathtt{tag}$, $\mathtt{gat}$. Izveido konkatenāciju $\mathtt{at\#_1tag\#_2gat\#_3}$ un būvē tai sufiksu koku (attēlā pa kreisi). Katrai lapai nomet tekstu aiz pirmā $\#$ simbola (attēlā pa labi).

<img
  alt="Vispārinātais sufiksu koks vārdiem at, tag, gat"
  src="{{ '/lectures/strings_suffix_structures/figs/generalized-suffix-trees.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**Garākais kopīgais apakšstrings:** Atrast garāko kopīgo apakšstringu tekstiem $S$ un $T$ (garumi $n_1$ un $n_2$).

* Uzbūvē vispārināto sufiksu koku $O(n_1 + n_2)$ laikā.
* Atrod dziļāko mezglu, zem kura ir gan tādas lapas, kas beidzas ar $\#_1$, gan arī tādas, kas beidzas ar $\#_2$.
* Tas ir efektīvāk nekā naivais algoritms $O(n_1^2 \cdot n_2^2)$ un arī nekā dinamiskā programmēšana $O(n_1 \cdot n_2)$.

### Dokumentu izgūšana

Kā atrast visus dokumentus, kas satur vienu vārdu? Var izmantot sufiksu koku kā iepriekš un veikt ātru meklēšanu. Bet kas notiek, ja ir divi dokumenti, kas atbilst paraugam, un vienā dokumentā tas parādās miljardu reižu, bet otrajā -- tikai vienu reizi?

**Dokumentu izgūšanas problēma:** Uzskaitīt visus dokumentus, kas satur paraugu $P$, laikā $O(|P| + k')$, kur $k' \leq k$ ir to dokumentu skaits, kas satur paraugu.

**Pielāgojums 1:** Vairākus dokumentus glabā sufiksu kokā tā, lai aiz jebkuras dolāra zīmes $\mathtt{\$}_i$ neko nepievienotu. Katra dolāra zīme ir sufiksu koka lapas mezgls.

**Pielāgojums 2:** Lapas, kas marķētas ar vienu un to pašu dolāra zīmi $\mathtt{\$}_i$, norāda viena uz otru -- tās veido saistīto sarakstu.

**Dokumentu izgūšanas algoritma pārskats:**

1. Atrod paraugu $P$ lielajā sufiksu kokā. Tas ir kāds iekšējs mezgls. Pieņemsim, ka visas lapas zem tā ir numurētas pēc kārtas; to numuri ir intervālā $[\ell, n]$.
2. Mērķis ir atrast pirmo $\mathtt{\$}_i$ parādījumu katram $i$. Vēlamies maksāt tikai par dažādu dokumentu skaitu, bet intervālā $[\ell, n]$ var būt ļoti daudz $\mathtt{\$}_i$ lapu.
3. Risinājums ir katrai lapai saglabāt numuru, kas ved uz iepriekšējo tā paša dokumenta lapu (kā "Pielāgojumā 2").

## Sufiksu masīvi

Sufiksu koka lapas, izrakstītas sufiksu alfabētiskā secībā, veido *sufiksu masīvu*.

**Definīcija:** *Sufiksu masīvs* (*suffix array*) ir visu teksta $T$ sufiksu sākuma indeksu saraksts, sakārtots sufiksu alfabētiskā secībā. Pašus sufiksus nav jāizraksta (jo tas aizņemtu $O(|T|^2)$ vietu) -- pietiek uzrakstīt indeksus.

**Piemērs:** Tekstam `banana$` sufiksu masīvs ir $[6, 5, 3, 1, 0, 4, 2]$:

```text
6: $
5: a$
3: ana$
1: anana$
0: banana$
4: na$
2: nana$
```

Sufiksu masīvam var pievienot arī LCP informāciju: LCP (*longest common prefix*, garākais kopīgais prefikss) diviem alfabētiskajā kārtībā blakus esošiem sufiksiem:

```text
    6: $
  0
    5: a$
  1
    3: ana$
  3
    1: anana$
  0
    0: banana$
  0
    4: na$
  2
    2: nana$
```

**Apgalvojums:** Ja ir dots sufiksu masīvs un LCP informācija, tad no tiem lineārā laikā var izveidot sufiksu koku. To dara ar **Dekarta koku** (*Cartesian tree*) LCP masīvam; tas ļauj arī atrast zemāko kopīgo priekšteci (LCA) un atbildēt uz LCP vaicājumiem par jebkuriem diviem sufiksiem.

Sufiksu masīvi ir cieši saistīti ar Berouza-Vīlera transformāciju (sk. [4. Berouza-Vīlera transformācija]({{ '/lectures/lossless_burrows_wheeler/' | relative_url }})).

## Uzdevumi

Rīks paraugu meklēšanai vārdnīcā: [Pattern Match](https://www.litscape.com/word_tools/pattern_match.php).

**14.1. uzdevums (Garākie kopīgie apakšstringi):** Garākais kopīgais apakšstrings tekstiem $T_1$ un $T_2$ ir garākais strings, kas ietilpst abos tekstos. Dinamiskā programmēšana dod $O(n_1 \cdot n_2)$ laika algoritmu, kur $|T_1| = n_1$ un $|T_2| = n_2$. (Sk. [tabulas veidošanas piemēru](https://bit.ly/3rcGUev).)

<img
  alt="Garākā kopīgā apakšstringa dinamiskās programmēšanas tabula"
  src="{{ '/lectures/strings_suffix_structures/figs/longest-common-substring-matrix.png' | relative_url }}"
  style="width: 100%; max-width: 480px; border:none; background-color:#FFFFFF;"
/>

*Dinamiskās programmēšanas tabula virknēm $\mathtt{ABCXYZAY}$ un $\mathtt{XYZABCB}$: šūnā ir garākā kopīgā sufiksa garums abu virkņu prefiksiem. Lielākā vērtība $4$ atbilst garākajam kopīgajam apakšstringam $\mathtt{XYZA}$.*

Aplūkot virknes $T_1 = \mathtt{banana\$}_1$ un $T_2 = \mathtt{guanabana\$}_2$. Tās ir uzrakstītas šādā alfabētā:

$$
\Sigma = \lbrace \mathtt{\$}_1, \mathtt{\$}_2, \mathtt{a}, \mathtt{b}, \mathtt{g}, \mathtt{n}, \mathtt{u} \rbrace.
$$

Algoritms ar laiku $O(n_1+n_2)$ var noteikt garāko kopīgo apakšstringu.

* **(A)** Uzzīmēt sufiksu koku tekstam $\mathtt{banana\$}_1$.
* **(B)** Pievienot esošajam kokam sufiksus arī no teksta $\mathtt{guanabana\$}_2$. (Var arī izveidot sufiksu koku uzreiz tekstam $\mathtt{banana\$}_1\mathtt{guanabana\$}_2$.)
* **(C)** Vizuāli noteikt garāko kopīgo apakšvirkni $\mathtt{banana}$ un $\mathtt{guanabana}$. Atzīmējiet atbilstošos mezglus sufiksu kokā. Kāda ir apakškoka saknes īpašība?
* **(D)** Atrast $O(n_1+n_2)$ algoritmu, lai noteiktu garāko kopīgo apakšstringu tekstiem attiecīgi garumā $n_1$ un $n_2$.

*Piezīme:* Attēlot sufiksu kokus saspiestā formā.

**14.2. uzdevums (Sufiksu masīva izveidošana):** Aplūkot šādu tekstu: $\mathtt{acabcabaabaabca\$}$. Tas pierakstīts 4 burtu alfabētā ar šādu secību: $\Sigma = \lbrace \mathtt{\$}, \mathtt{a}, \mathtt{b}, \mathtt{c} \rbrace$.

* **(A)** Izveidot sufiksu masīvu šim tekstam.
* **(B)** Pievienot LCP (garākā kopīgā prefiksa) informāciju sufiksu masīvam -- atrast garākos kopīgos prefiksus jebkuriem diviem alfabētiski blakus esošiem sufiksiem.
* **(C)** Izmantot sufiksu masīvu un tā LCP informāciju, lai izveidotu (saspiestu) sufiksu koku šim vārdam.

**Risinājums:**

```python
T = 'acabcabaabaabca$'
sorted_suffixes = sorted([T[x:] for x in range(0,len(T))])
suf_array = list(map(lambda w: len(T) - len(w), sorted_suffixes))
print(sorted_suffixes)
print(suf_array)
```

```text
['$', 'a$', 'aabaabca$', 'aabca$', 'abaabaabca$', 'abaabca$', 'abca$',
 'abcabaabaabca$', 'acabcabaabaabca$', 'baabaabca$', 'baabca$', 'bca$',
 'bcabaabaabca$', 'ca$', 'cabaabaabca$', 'cabcabaabaabca$']
[15, 14, 7, 10, 5, 8, 11, 2, 0, 6, 9, 12, 3, 13, 4, 1]
```

<img
  alt="Sufiksu koks, sufiksu masīvs un LCP informācija tekstam acabcabaabaabca$"
  src="{{ '/lectures/strings_suffix_structures/figs/long-suffix-tree.png' | relative_url }}"
  style="width: 100%; max-width: 720px; border:none; background-color:#FFFFFF;"
/>

## Atsauces

* [MIT 6.851 Advanced Data Structures: Session 16 -- Strings](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-851-advanced-data-structures-spring-2012/lecture-videos/session-16-strings/)
* [Suffix tries (video)](https://youtu.be/hLsrPsFHPcQ)
* [CMU: Suffix Trees (prezentācija)](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixtrees.pdf)
* [Suffix Arrays (Yale, J.Aspnes)](https://www.cs.yale.edu/homes/aspnes/pinewiki/SuffixArrays.html) -- par sufiksu masīviem un Berouza-Vīlera transformāciju.
* [Suffix arrays: papildu paskaidrojumi (arXiv:1311.1762)](https://arxiv.org/pdf/1311.1762.pdf)
* [MIT 6.854J Advanced Algorithms (1999)](https://dspace.mit.edu/bitstream/handle/1721.1/36897/6-854JFall-1999/OcwWeb/Electrical-Engineering-and-Computer-Science/6-854JAdvanced-AlgorithmsFall1999/CourseHome/index.htm)
