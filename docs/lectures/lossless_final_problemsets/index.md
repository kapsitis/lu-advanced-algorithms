---
layout: default
title: "Bezzudumu saspiešana: uzdevumu krājums"
permalink: /lectures/lossless_final_problemsets/
---
# Bezzudumu saspiešana: Beigu uzdevumi

Uzdevumi aptver nodaļas par entropiju un Hafmana kodu, aritmētisko kodu un ANS, Lempela-Ziva algoritmiem un 
Berouza-Vīlera transformāciju. Visus aprēķinus var veikt uz papīra; algoritmu apzīmējumi ir tādi paši kā attiecīgajās nodaļās.

**Noderīgas vērtības:** $\log_2 3 \approx 1.585$, $\;\log_2 5 \approx 2.322$.

## Entropija un Hafmana kods

**1. uzdevums (Viltotā monēta):** Starp $4$ pēc izskata vienādām monētām viena ir viltota: tā ir vai nu vieglāka, vai smagāka par pārējām. Visi $8$ gadījumi (kura monēta ir viltota un vai tā ir vieglāka vai smagāka) ir vienādi varbūtīgi. Ir sviru svari bez atsvariem; katrai svēršanai ir trīs iznākumi: smagāks kreisais kauss, smagāks labais kauss vai līdzsvars. Uz abiem kausiem liek vienādu monētu skaitu.

* **(a)** Kāda ir entropija gadījumlielumam, kas nosaka, kura monēta ir viltota un vai tā ir vieglāka vai smagāka?
* **(b)** Atrodiet pirmās svēršanas iznākuma varbūtību sadalījumu un entropiju, ja salīdzina (1) vienu monētu ar vienu monētu; (2) divas monētas ar divām monētām. Kura svēršana dod vairāk informācijas?
* **(c)** Kāda ir lielākā iespējamā vienas svēršanas iznākuma entropija? Pamatojiet ar entropiju, ka ar vienu svēršanu uzdevumu atrisināt nevar.
* **(d)** Entropijas novērtējums neizslēdz divas svēršanas, jo $2 \log_2 3 \approx 3.17 > 3$. Pierādiet, ka ar divām svēršanām tomēr nepietiek (apskatiet, cik gadījumu var palikt pēc pirmās svēršanas), un atrodiet stratēģiju ar trim svēršanām.

**2. uzdevums (Cik bitu zaudē Hafmana kods):** Ziņojumu alfabētā ir $5$ ziņojumi ar varbūtībām $p = (0.4,\; 0.2,\; 0.2,\; 0.1,\; 0.1)$.

* **(a)** Aprēķiniet entropiju $H(S)$. *Norāde:* $\log_2 2.5 = \log_2 5 - 1$.
* **(b)** Katram ziņojumam izvēlamies kodavārda garumu $\ell_i = \left\lceil \log_2 \frac{1}{p_i} \right\rceil$. Pārbaudiet, ka šie garumi apmierina Krafta-Makmilana nevienādību, un uzrakstiet prefiksu kodu ar šādiem garumiem. Kāds ir tā vidējais garums? Kāpēc šis kods noteikti nav optimāls?
* **(c)** Pierādiet vispārīgi: ja $\ell_i = \left\lceil \log_2 \frac{1}{p_i} \right\rceil$, tad $\sum_i 2^{-\ell_i} \leq 1$ un $\sum_i p_i \ell_i < H(S) + 1$.
* **(d)** Uzbūvējiet Hafmana kodu un atrodiet tā vidējo garumu. Paskaidrojiet, kāpēc no (c) punkta un Hafmana koda optimalitātes seko, ka Hafmana kods vienmēr iztērē mazāk nekā $H(S) + 1$ bitu uz ziņojumu. Vai Hafmana koks šim sadalījumam ir viennozīmīgs?
* **(e)** Alfabētam ar diviem ziņojumiem, kuru varbūtības ir $0.99$ un $0.01$, entropija ir aptuveni $0.08$ biti. Cik bitu uz ziņojumu iztērē Hafmana kods? Kā šo zudumu var samazināt?

## Aritmētiskais kods un ANS

**3. uzdevums (Aritmētiskais kods):** Alfabētā ir burti `A`, `B`, `C` ar varbūtībām $p(\mathtt{A}) = 0.5$, $p(\mathtt{B}) = 0.3$, $p(\mathtt{C}) = 0.2$; intervālus sakārto šādā secībā.

* **(a)** Atrodiet intervālu virkni $[l_i;\, l_i + s_i)$, kas atbilst ziņojumam `ACBA`.
* **(b)** Atrodiet īsāko bināro daļu $\beta = 0.b_1 b_2 \ldots b_n$, kurai viss intervāls $[\beta;\, \beta + 2^{-n})$ ietilpst (a) punktā atrastajā intervālā. Salīdziniet $n$ ar $\log_2 \frac{1}{s_4}$.
* **(c)** Cik bitu šim ziņojumam iztērētu Hafmana kods? Kāpēc aritmētiskais kods īsam ziņojumam nav izdevīgāks, bet garam ziņojumam ir?
* **(d)** Nosūtītais skaitlis ir $0.101_2$. Atkodējiet ziņojuma pirmos četrus burtus.

**4. uzdevums (ANS):** Vārdā `ANANAS` burts `A` ir $3$ reizes, `N` -- $2$ reizes, bet `S` -- $1$ reizi. Izmantojam šos skaitus kā rANS frekvences: $f(\mathtt{A}) = 3$, $f(\mathtt{N}) = 2$, $f(\mathtt{S}) = 1$, tātad $M = 6$, $c(\mathtt{A}) = 0$, $c(\mathtt{N}) = 3$, $c(\mathtt{S}) = 5$.

* **(a)** Kuriem simboliem pieder skaitļi $0, 1, \ldots, 17$?
* **(b)** Iekodējiet ziņojumu `ANANAS` ar $\textsf{Rans-Encode}$, sākot ar $x = 0$. Pierakstiet stāvokli pēc katra soļa.
* **(c)** Atkodējiet (b) punktā iegūto skaitli ar $\textsf{Rans-Decode}$ un pārliecinieties, ka stāvoklis atgriežas nullē.
* **(d)** Atkodējiet četrus simbolus no stāvokļa $x = 131$.
* **(e)** Salīdziniet $\log_2 x$ (b) punktā ar ziņojuma informācijas saturu $-\log_2 \left( p(\mathtt{A})^3 \, p(\mathtt{N})^2 \, p(\mathtt{S}) \right)$.
* **(f)** Parādiet, ka ziņojumi `NA` un `NAA` tiek iekodēti ar vienu un to pašu skaitli. Kāpēc tā notiek, un kāpēc ziņojumam `ANANAS` šādas problēmas nav?

## Lempela-Ziva algoritmi

**5. uzdevums (LZ77):**

* **(a)** Aizkodējiet virkni `kakadukakadu` ar $\textsf{LZ77-Encode}$, ja loga garums $W = 6$, bet priekšskata buferis nav ierobežots. Katram trijniekam norādiet kursora pozīciju un loga saturu.
* **(b)** Atkārtojiet to pašu ar $W = 4$. Kāpēc trijnieku ir vairāk?
* **(c)** Atkodējiet trijnieku virkni $(0,0,\mathtt{l}), (0,0,\mathtt{a}), (2,5,\mathtt{i}), (4,3,\mathtt{a})$ ar $\textsf{LZ77-Decode}$. Kurā solī avota apgabals pārklājas ar tikko atkodētajiem burtiem?

**6. uzdevums (LZ78):**

* **(a)** Aizkodējiet virkni `abababababa` ar $\textsf{LZ78-Encode}$ (alfabēts $S = \lbrace \mathtt{a}, \mathtt{b} \rbrace$). Pierakstiet, kādas frāzes un ar kādiem numuriem tiek pievienotas vārdnīcai.
* **(b)** Atkodējiet (a) punktā iegūto kodu virkni ar $\textsf{LZ78-Decode}$. Kurā solī atkodētājs saņem numuru, kura vēl nav tā vārdnīcā?
* **(c)** Atkodējiet kodu virkni `l,a,1,3,2,5` (alfabēts $S = \lbrace \mathtt{a}, \mathtt{l} \rbrace$).
* **(d)** Virkne sastāv no $n$ burtiem `a` (alfabēts $S = \lbrace \mathtt{a} \rbrace$). Cik kodu izvada $\textsf{LZ78-Encode}$? Atrodiet precīzu atbildi, ja $n = 1 + 2 + \ldots + r$, un aptuvenu atbildi kā funkciju no $n$.

## Berouza-Vīlera transformācija

**7. uzdevums (BWT):**

* **(a)** Izrakstiet visas vārda `KAKAO$` cikliskās permutācijas, sakārtojiet tās alfabētiski (`$` ir pirms visiem burtiem) un atrodiet BWT(`KAKAO$`). Kurā sakārtotās matricas rindā ir sākotnējais vārds?
* **(b)** Iekodējiet (a) punktā iegūto virkni ar *Move-to-front*, ja sākotnējā alfabēta secība ir `$`, `A`, `K`, `O` (pozīcijas numurē no $0$).
* **(c)** Zināms, ka kāda vārda $w$, kas beidzas ar `$`, Berouza-Vīlera transformācija ir `ASSAL$`. Atjaunojiet $w$.

**8. uzdevums (BWT ar sufiksu masīvu):**

* **(a)** Izrakstiet visus vārda `BARBARA$` sufiksus, sakārtojiet tos alfabētiski un uzrakstiet sufiksu masīvu $A$ (katru sufiksu apzīmē ar to, cik burtu nodzēsts no vārda sākuma).
* **(b)** Atrodiet BWT(`BARBARA$`) ar $\textsf{efficientBWT}$: katram $i$ izvada burtu $w[A[i]-1]$, kur $w[-1]$ nozīmē pēdējo burtu. Pārbaudiet dažus rezultāta burtus ar cikliskajām permutācijām.
* **(c)** Paskaidrojiet, kāpēc sufiksu sakārtojums sakrīt ar ciklisko permutāciju sakārtojumu, ja vārds beidzas ar unikālu, alfabētiski mazāko simbolu `$`.
* **(d)** Kā ar sufiksu masīvu un bināro meklēšanu atrast visas apakšvirknes `BAR` sastapšanās vietas vārdā? Kāpēc tām atbilstošie ieraksti sufiksu masīvā atrodas blakus?
* **(e)** Salīdziniet naivās BWT implementācijas un sufiksu masīva metodes laika sarežģītību.

## Markova ķēdes

**9. uzdevums (Markova ķēde un saspiešana):** Vienkāršotā "valodā" ir burti `A`, `B`, `C`. Tekstu ģenerē Markova ķēde: pēc `A` ar varbūtību $1/2$ seko `A` un ar varbūtību $1/2$ seko `B`; pēc `B` vienmēr seko `C`; pēc `C` vienmēr seko `A`. Teksts sākas ar `A`.

* **(a)** Uzzīmējiet ķēdes grafu un uzrakstiet pāreju varbūtību matricu. Kāda ir varbūtība, ka teksts sākas ar `ABCAABCA`?
* **(b)** Atrodiet stacionāro sadalījumu $\pi = (\pi_A, \pi_B, \pi_C)$, t.i., sadalījumu, kas pēc viena ķēdes soļa nemainās.
* **(c)** Vai ķēde ir ergodiska? Vai tā ir periodiska? Kas mainītos, ja pāreju $\mathtt{A} \to \mathtt{A}$ noņemtu, t.i., pēc `A` vienmēr sekotu `B`?
* **(d)** Aprēķiniet viena burta entropiju $H(X_1)$ stacionārajā sadalījumā un vidējo entropiju $H(X) = \sum_i \pi_i \cdot H(\text{pārejas no stāvokļa } i)$. Cik bitu uz burtu iztērētu Hafmana kods, kas kodē katru burtu atsevišķi?
* **(e)** Parādiet, ka tekstu pēc sākuma burta `A` var sadalīt gabalos `A` un `BCA` un, kodējot katru gabalu ar vienu bitu, sasniegt vidēji $H(X)$ bitu uz burtu. Kurš no kursa algoritmiem šādus atkārtotus gabalus atrod automātiski, nezinot ķēdes varbūtības?
