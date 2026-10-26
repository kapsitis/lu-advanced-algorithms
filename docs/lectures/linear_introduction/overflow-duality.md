

## Dualitātes teorēmas

**Definīcija:** Vektoru $\mathbf{x}$ sauc par *iespējamu* (*feasible*) (arī (neoptimālu) LP uzdevuma *risinājumu*), ja tas apmierina visus ierobežojumus (vienādības, nevienādības).

**Definīcija:** LP uzdevumu sauc par *iespējamu* (*feasible*), ja tam ir iespējams risinājums $\mathbf{x}$.

**Definīcija:** LP uzdevums ir *neiespējams* (*infeasible*), ja tam šāds $\mathbf{x}$ neeksistē.

**Definīcija:** LP minimuma uzdevums ($\min\lbrace \mathbf{c}^T \mathbf{x}\;:\;A\mathbf{x}=\mathbf{b},\mathbf{x}\geq\mathbf{0}\rbrace$) ir *neierobežots* (*unbounded*), ja katram $\lambda \in \mathbb{R}$ eksistē $\mathbf{x} \in \mathbb{R}^n$, ka visi LP ierobežojumi izpildās un $\mathbf{c}^T \mathbf{x} \leq \lambda$.

Lineāru programmu var pārveidot, ieviešot *nokares mainīgos* (*slack variables*). Šajā gadījumā visas nevienādības var pārrakstīt par vienādībām, papildus prasot, lai mainīgie (ieskaitot nokares mainīgos) būtu nenegatīvi skaitļi.

$$
\begin{array}{ccc}
\max\{ \mathbf{c}^T \mathbf{x}\} & \rightarrow  & \min\{ -\mathbf{c}^T \mathbf{x}\}\\
\mathbf{a}_i^T \mathbf{x} = b_i & \rightarrow  &  (\mathbf{a}_i^T \mathbf{x} \leq b_i)
\wedge (\mathbf{a}_i^T \mathbf{x} \geq b_i)  \\
\mathbf{a}_i^T \mathbf{x} \leq b_i & \rightarrow  &  (\mathbf{a}_i^T \mathbf{x} + s_i = b_i)
\wedge (s_i \geq 0)  \\
\end{array}
$$

**Primārās un duālās LP apvienošana:** Ja dotas primārā LP un duālā LP, varam uzrakstīt jaunu LP, kas satur visus mainīgos (gan $x_1, x_2, \ldots, x_n$, gan $y_1, y_2, \ldots, y_k$), gan visus nosacījumus no abām programmām un pievienot tai vēl vienu nosacījumu:

$$
c_1 x_1 + c_2 x_2 + \ldots + c_n x_n = b_1 y_1 + b_2 y_2 + \ldots + b_k y_k.
$$

Vienīgais gadījums, kad izpildās visi nosacījumi ir, ja $x_1, x_2, \ldots, x_n$ sasniedz primārās LP maksimums, bet $y_1, y_2, \ldots, y_k$ sasniedz duālās LP minimumu.

**Secinājums:** Ja mums ir algoritms, kas prot patvaļīgai LP atrast vienu punktu, kas apmierina visus nosacījumus, tad šo algoritmu var izmantot arī maksimuma atrašanai.

### Vājā dualitāte

**Farkaša lemma:** Ja $A$ ir $m \times n$ matrica, tad izpildās tieši viens no apgalvojumiem: **(1)** $\exists\mathbf{x} \in \mathbb{R}^n\;:\;A\mathbf{x}=\mathbf{b}$, kur $\mathbf{x} \geq \mathbf{0}$, **(2)** $\exists\mathbf{y} \in \mathbb{R}^m\;:\;A^T \mathbf{y} \geq \mathbf{0}$, kur $\mathbf{b}^T \mathbf{y} < 0$.

Atsevišķs gadījums ir lineārajā algebrā, kur vai nu $A\mathbf{x} = \mathbf{b}$ eksistē atrisinājums, vai arī sistēmai $A^T \mathbf{y} = 0$ (kur $\mathbf{b}^T \mathbf{y} \neq 0$) eksistē atrisinājums.

**Pierādījums:** Abi nosacījumi nevar vienlaicīgi izpildīties, jo šādu $\mathbf{x}$ un $\mathbf{y}$ pastāvēšana nozīmētu

$$
\begin{array}{l}
\mathbf{y}^T A \mathbf{x} = \mathbf{y}^T (A \mathbf{x}) = \mathbf{y} \mathbf{b} < 0 \\
\mathbf{y}^T A \mathbf{x} = (A^T \mathbf{y})^T \mathbf{x} \geq 0 \\
\end{array}
$$

jo divu nenegatīvu vektoru skalārais reizinājums ir nenegatīvs.

**Vājās dualitātes teorēma:** Primārā $P$: $\min \mathbf{c}^T \cdot \mathbf{x}$, kur $A\mathbf{x} = \mathbf{b}$, $\mathbf{x} \geq 0$.

Duālā $D$: $\max \mathbf{b}^T \cdot \mathbf{y}$, kur $A^T\mathbf{y} \leq \mathbf{c}$.

**Teorēma:** Zināms, ka $P$ atrisinājums ir $\mathbf{x} = \mathbf{x}_{\text{opt}}$ un $D$ atrisinājums ir $\mathbf{y} = \mathbf{y}_{\text{opt}}$. Apzīmējam optimālās vērtības ar $z_{\text{opt}} = \mathbf{c}^T \cdot \mathbf{x}_{\text{opt}}$ un $w_{\text{opt}} = \mathbf{b}^T \cdot \mathbf{y}_{\text{opt}}$.

Tad $z_{\text{opt}} \geq w_{\text{opt}}$.

**Pretrunīgi/neierobežoti nosacījumi:** Vājās dualitātes teorēma spēkā pat tad, ja primārā $P$ vai duālā $D$ ir pretrunīgas vai neierobežotas. Apzīmējam:

* Ja primārais/minimuma uzdevums $P$ ir pretrunīgs, tad optimums $z_{\text{opt}} = +\infty$.
* Ja primārais/minimuma uzdevums $P$ ir neierobežots, tad optimums $z_{\text{opt}} = -\infty$.
* Ja duālais/maksimuma uzdevums $D$ ir pretrunīgs, tad optimums $w_{\text{opt}} = -\infty$.
* Ja duālais/maksimuma uzdevums $D$ ir neierobežots, tad optimums $w_{\text{opt}} = +\infty$.

**Vājās dualitātes teorēmas pierādījums:** Duālā LP veidota tā, lai vājā dualitāte būtu spēkā. Iedomāsimies, ka ir kaut kāds vektors $\mathbf{y}$, kam $A^T\mathbf{y} \leq \mathbf{c}$. Pārrakstām:

$$
\mathbf{y}^T \mathbf{b} = \mathbf{y}^T A \mathbf{x} \leq \mathbf{c}^T \mathbf{x},
$$

kur $\mathbf{x}$ ir jebkurš (arī neoptimāls) risinājums, kas apmierina $P$ nosacījumus. Tādēļ $\mathbf{y}^T \mathbf{b}$ ir apakšējais novērtējums optimālajam risinājumam. Tas ir spēkā visiem $\mathbf{y}$, kas apmierina $A^T \mathbf{y} \leq \mathbf{c}$, tādēļ vislabāko apakšējo novērtējumu iegūsim, maksimizējot $\mathbf{y}^T \mathbf{b}$ pie nosacījuma $A^T \mathbf{y} \leq \mathbf{c}$. $\square$

### Stiprā dualitāte

**Duālais uzdevums, tikai nevienādības**

**Primārais LP uzdevums:** Maksimizēt skalāro reizinājumu $z = \mathbf{c} \cdot \mathbf{x}$, kur

$$
\left\{
\begin{array}{l}
A\mathbf{x} \leq \mathbf{b}\\
\mathbf{x} \geq \mathbf{0}
\end{array}
\right.
$$

**Duālais LP uzdevums:** Minimizēt skalāro reizinājumu $Z = \mathbf{y} \cdot \mathbf{b}$, kur

$$
\left\{
\begin{array}{l}
A^{T}\mathbf{y} \geq \mathbf{c}\\
\mathbf{y} \geq \mathbf{0}
\end{array}
\right.
$$

**Dualitātes teorēma:**

* **(1)** Ja $\mathbf{x}^{\ast}$ ir pieļaujams vektors primārajai problēmai (apmierina nevienādības $A\mathbf{x}^{\ast} \leq \mathbf{b}$ un $\mathbf{x}^{\ast} \geq \mathbf{0}$),
* **(2)** Un ja $\mathbf{y}^{\ast}$ ir pieļaujams risinājums duālajai problēmai (apmierina nevienādības $A^{T}\mathbf{y} \geq \mathbf{c}$ un $\mathbf{y} \geq \mathbf{0}$), TAD $\mathbf{c}\cdot \mathbf{x}^{\ast} \leq \mathbf{b} \cdot \mathbf{y}^{\ast}$.

Ja turklāt $\mathbf{x}^{\ast}$ un $\mathbf{y}^{\ast}$ ir optimālie atrisinājumi attiecīgi primārajai un duālajai lineārajām programmām, tad

$$
\mathbf{c}\cdot \mathbf{x}^{\ast} = \mathbf{b} \cdot \mathbf{y}^{\ast}
$$

**Definīcija:** Atšķirību $\mathbf{b} \cdot \mathbf{y}^{\ast} - \mathbf{c} \cdot \mathbf{x}^{\ast}$ sauc par *dualitātes atstarpi* (*duality gap*). Šīs atstarpes lielums palīdz noteikt, cik tālu pašreizējais atrisinājums (neoptimāls, bet pieļaujams vektors $\mathbf{x}$ vai attiecīgi $\mathbf{y}$) ir no optimālā.

## Dualitāte grafu uzdevumos

**Maksimālās plūsmas atrašana grafā**

![Maksimālās plūsmas grafs](figs/max-flow-graph.png)

*Maksimālās plūsmas grafs.*

Aplūkotajā grafā katrai šķautnei ir pierakstīta skaitliska vērtība - maksimālā atļautā plūsma, kuru pa šo šķautni var sūtīt (vai nu vienā, vai otrā virzienā). Var sūtīt arī mazāku plūsmu.

**Lineārā programma plūsmai:** Katrai (neorientētai) šķautnei ieviešam divus mainīgos, piemēram, $x_1$ un $x'_1$ (nenegatīvas plūsmas katrā no iespējamajiem virzieniem).

1. Katrai virsotnei grafā rakstām "plūsmas saglabāšanās" ("flow preservation") vienādojumus. Piemēram,

   $$
   x_1 + x_2 + x'_3 = x'_1 + x'_2 + x_3.
   $$

2. Katrai šķautnei grafā rakstām divas nevienādības caurlaidībai ("edge capacity"). Piemēram,

   $$
   x_1 \leq 3,\;\;x'_1 \leq 3.
   $$

   (Ja šķautne, kas atbilst $x_1$ un $x'_1$ ir ar caurlaidību $3$.)

3. Visas plūsmas ir nenegatīvas. Piemēram,

   $$
   x_1 \geq 0,\;\;x'_1 \geq 0.
   $$

**Maksimizējamā funkcija:** Var maksimizēt plūsmu summu visām no "IN" izejošajām virsotnēm. Biežāk izmanto triku: pievieno fiktīvu šķautni no "OUT" atpakaļ uz "IN" un maksimizē plūsmu uz šīs vienas šķautnes.

