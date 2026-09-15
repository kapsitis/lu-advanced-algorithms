13. Stringu meklēšana un hešings
========================================

Šajā nodaļā definējam stringu meklēšanas uzdevumu un tā
variantus (garākā kopīgā apakšstringa meklēšana, paternu meklēšana 
vienlaikus vairākos dokumentos, dokumentu priekšapstrāde jeb indeksācija). 
Aplūkoti algoritmi: 

* Naivais apakšstringa meklēšanas algoritms
* Algoritms Levenšteina attāluma atrašanai
* Ripojošās hešfunkcijas 
* Rabina-Karpa algoritms apakšstringa meklēšanai 


Stringu meklēšanas ievads 
---------------------------

Stringu meklēšana sastopama atšķirīgos lietojumos, kas prasa dažādus algoritmus: 

* Teksta redaktori: 1 vārds, 1 dokuments
* Datu noplūdes novēršana (*Data Leak prevention (DLP)*): 
  daudzi paraugi (vārdi, regulāras izteiksmes), 1 pārbaudāmais dokuments.
* Dokumentu atrašana (*Document retrieval*): nedaudzi paraugi, daudzi dokumenti, kam 
  var veikt priekšapstrādi/indeksāciju, lai paātrinātu meklēšanu tajos. 
* Plaģiāta meklēšana: Daudzi dokumenti, 1 pārbaudāmais dokuments, atrast 
  "kopētos-ielīmētos" (*Copy-Paste*) gabalus vai "kopētos-ielīmētos" 
  un drusku parediģētos.




**Apakšstringa meklēšanas uzdevums:** 
  Dots *teksts* - strings no :math:`n` simboliem:
  :math:`T = T[0], \ldots, T[n-1]`. 
  Dots arī *paraugs* (*pattern*) - strings no :math:`m` simboliem:
  :math:`P = P[0], \ldots, P[m-1]`. 

  Jautājums: Vai tekstā :math:`T` ir atrodams apakšstrings :math:`P` 
  (algoritms izvada vai nu pirmo pozīciju, kur :math:`P` ieiet virknē :math:`T`, 
  vai arī tas izvada visas pozīcijas).

**Definīcija:** 
  Pozīciju tekstā :math:`T` (skaitli no :math:`0` līdz 
  :math:`n-1`), kur var sākties meklējamais
  paraugs sauc par *nobīdi* (*shift*). 


Apakšstringi un apakšvirknes 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stringus dažreiz sauc par virknēm, kas arī ir pareizi, 
bet virkne var nozīmēt gan "sequence" (galīga vai bezgalīga, 
no jebkāda veida objektiem), gan "string" (galīga virkne ar galīga alfabēta burtiem). 
Ir piemērs, kur abi jēdzieni atšķiras: 

**Definīcija:** 
  Par virknes :math:`T[0],T[1],\ldots,T[n-1]` *apakšstringu* (*substring*) sauc 
  simbolu virkni no :math:`T[i]`, kur :math:`i` vērtības seko pēc kārtas.  
  (Apakšstringu iegūst, sākotnējai virknei nosvītrojot gabalus sākumā un beigās. 
  Arī tukšais strings :math:`\varepsilon` un pats teksts :math:`T` ir apakšstringi.)

**Definīcija:** 
  Par virknes :math:`T[0],T[1],\ldots,T[n-1]` *apakšvirkni* (*subsequence*) sauc 
  simbolu virkni no :math:`T[i]`, 
  kur :math:`i` vērtības aug, bet var nebūt pēc kārtas.  
  (Apakšvirkni iegūst, sākotnējā virknē nosvītrojot :math:`0` 
  vai vairāk simbolus jebkurās vietās.)


**Piemērs:** 
  Virknē :math:`\mathtt{ABCDE}` apakšstringi ir :math:`15` stringi:

  .. math:: 

    \varepsilon, 
    \mathtt{A}, \mathtt{AB}, \mathtt{ABC}, \mathtt{ABCD}, \mathtt{ABCDE}, 
    \mathtt{B}, \mathtt{BC}, \mathtt{BCD}, \mathtt{BCDE}, 
    \mathtt{C}, \mathtt{CD}, \mathtt{CDE},
    \mathtt{D}, \mathtt{DE}, 
    \mathtt{E}


:math:`n` simbolu virknei ir ne vairāk kā 
:math:`{\displaystyle 1 + \frac{n(n+1)}{2}}` apakšstringi
(to ir visvairāk, ja visi burti dažādi).


**Piemērs:** 
  Virknē :math:`\mathtt{ABCDE}` apakšvirknes ir šie :math:`32` stringi: 

  .. math:: 

    \begin{array}{c}
    \varepsilon,
    \mathtt{A}, 
    \mathtt{AB}, \mathtt{ABC}, \mathtt{ABCD}, \mathtt{ABCDE}, \mathtt{ABCE}, 
    \mathtt{ABD}, \mathtt{ABDE}, \mathtt{ABE}, 
    \mathtt{AC}, \mathtt{ACD}, \mathtt{ACDE}, \mathtt{ACE}, \mathtt{AD}, \mathtt{ADE}, \mathtt{AE},\\    
    \mathtt{B}, \mathtt{BC}, \mathtt{BCD}, \mathtt{BCDE}, \mathtt{BCE},
    \mathtt{BD}, \mathtt{BDE}, \mathtt{BE}, 
    \mathtt{C}, \mathtt{CD}, \mathtt{CDE}, \mathtt{CE}, 
    \mathtt{D}, \mathtt{DE}, 
    \mathtt{E}.\\
    \end{array}


:math:`n` simbolu virknei ir ne vairāk kā :math:`{\displaystyle 2^n}` apakšvirknes
(to sasniedz, ja visi burti dažādi).



Naivais stringa meklēšanas algoritms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| :math:`\text{\sc NaiveStringMatcher}(T, P)`
| 1. :math:`\quad` :math:`n = T.\mathit{length}`
| 2. :math:`\quad` :math:`m = P.\mathit{length}`
| 3. :math:`\quad` **for** :math:`i = 0` **to** :math:`n-m`:
| 4. :math:`\quad\quad` **if** :math:`(P[0],\ldots,P[m-1]) == (T[i],\ldots,T[i+m-1])`:
| 5. :math:`\quad\quad\quad` :math:`\text{print "Paraugs parādās ar nobīdi" } i`


Algoritms novieto vienu virkni zem otras un salīdzinām burtus no kreisās puses uz labo: 

.. math:: 

  \begin{array}{llllll}
  \ldots, & T[i], & T[i + 1], & \ldots, & T[i+m-1], & \ldots \\
  & P[0], & P[1], & \ldots, & P[m-1] & 
  \end{array}

Ja sakrīt visi :math:`m` elementi, kas ir paraugā, tad apakšstringu esam atraduši. 


**Apgalvojums:** 
  Naivā apakšstringu meklēšanas algoritma laika sarežģītība ir 
  :math:`O(n \cdot m)` sliktākajā gadījumā.

**Pierādījums:**
  Ir :math:`n - m + 1` iespējamās vērtības mainīgajam :math:`s`. 
  Katrai no tām var gadīties salīdzināt līdz :math:`m` simboliem. Laiks
  :math:`(n - m + 1) \cdot m \approx n \cdot m`.

Parasti pieņem, ka meklējamais paraugs ir 
daudz īsāks par pašu tekstu: :math:`m << n`, tomēr arī :math:`m` var būt 
liels un tāpēc :math:`O(n \cdot m)` ir daudz sliktāk nekā, piemēram, :math:`O(n)` -- 
lineāra atkarība no teksta garuma.

**Piemērs:** 
  Šīm :math:`T` un :math:`P` vērtībām nevar uzlabot ātrdarbību: 

  .. math:: 
 
    \left\{ \begin{array}{ll}
    T = & \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{burti}}\\
    P = & \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m\;\text{burti}}\\
    \end{array} \right.

  Arī šis ir sliktākais gadījums naivā algoritma ātrdarbībai: 

  .. math:: 
 
    \left\{ \begin{array}{ll}
    T = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{burti}}\\
    P = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m-1\;\text{burti}}\mathtt{b}\\
    \end{array} \right.





Labošanas attālums
---------------------

Dotas simbolu virknes :math:`A = A[0]\ldots{}A[m-1]` un :math:`B = B[0]\ldots{}B[n-1]`, 
kuru garumi ir attiecīgi :math:`m` un :math:`n`. Atļautas sekojošas operācijas jeb 
*labojumi* (*edits*):

* Viena simbola aizstāšana ar citu simbolu;
* Jebkura viena simbola izdzēšana;
* Jauna simbola iespraušana patvaļīgā vietā.

**Definīcija:** 
  Par *Levenšteina attālumu*
  (*Levenshtein distance*, *editing distance*) :math:`M(A,B)` 
  diviem vārdiem :math:`A=A[0]\ldots{}A[m-1]` un 
  :math:`B=B[0]\ldots{}B[n-1]` sauc mazāko 
  iespējamo labojumu skaitu, kas pārtaisa :math:`A` par :math:`B`.


Ir pazīstami arī citi labošanas attāluma varianti

* Ja viena simbola aizstāšana ar citu ir divreiz dārgāka par iespraušanu un izdzēšanu.
* Ja virkni :math:`A` jāpārveido par kādu :math:`B` apakšvirkni (nevis pašu :math:`B`).
* Ja labojuma izmaksas atkarīgas no dzēšamā/iespraužamā simbola.
* Ja :math:`k` simbolu apakšvirkni var iespraust/izdzēst vienā
  gājienā ar izmaksu :math:`f(k)` (šeit :math:`f(k)<k` jeb apakšvirknes iespraušana
  ir lētāka nekā :math:`k` burtu mainīšana pa vienam). 

Tādi uzdevumi par *aptuveno salīdzināšanu* (*Sequence alignment*) var parādīties bioinformātikā. 
Piemēram, cik mutāciju vajag, lai viena DNS virkne pārvērstos par otru virkni.
Levenšteina attālums ir viens no vienkāršākajiem variantiem. 


**Levenšteina attālums kā īsākais ceļš grafā:**
  Ja :math:`m` burtu vārds :math:`u` jāpārtaisa par :math:`n` burtu vārdu :math:`v`, izveidojam 
  taisnstūrveida režģi ar aplīšiem -- tajā ir :math:`m+1` rindas un :math:`n+1` kolonnas.
  Katram aplītim ir "koordinātas" :math:`(i,j)`, ja tas atrodas :math:`i`-tajā rindā un 
  :math:`j`-tajā kolonnā (:math:`i \in [0;m]`, :math:`j \in [0;n]`). 

  .. image:: figs/graph-distances.png
      :width: 4in

  * Visas bultiņas virzienā pa labi ir ar svaru :math:`1` (burta iespraušana)
  * Visas bultiņas virzienā uz leju ir ar svaru :math:`1` (burta dzēšana)
  * Bultiņas pa diagonāli no :math:`(i,j)` uz :math:`(i+1,j+1)` 
    ir ar svaru :math:`1` (burta aizstāšana ar citu), 
    **izņemot**, ja burti sakrīt: :math:`u[i] = v[j]`. Šajā gadījumā burts nav 
    jāmaina un šādu bultiņu drīkst izmantot bez maksas.
   
  Levenšteina attālums būs īsākais ceļš no kreisās augšējās virsotnes uz 
  labo apakšējo. 

**Levenšteina attālums ar matricu rekurencēm:**
  Doti vārdi :math:`A=A[0]\ldots{}A[m-1]` un :math:`B=B[0]\ldots{}B[n-1]`. 
  Definējam :math:`(m+1) \times (n+1)` izmēra matricu :math:`M[i,j]` ar šādām sakarībām:

  .. math::

    M[0,0]=0, 

  .. math:: 

    M[i,0]=i,\;1 \leq i \leq m, 

  .. math:: 

    M[0,j]=j,\;1 \leq j \leq n\\

  .. math::   
      
    M[i,j]=\min \left\{ \begin{array}{l}
      M[i-1,j-1] + 0,\;\text{ja}\;A[i] = B[j]\\
      M[i-1,j-1] + 1,\;\text{(burta aizstāšana)}\\
      M[i,j-1] + 1,\;\text{(burta iespraušana)}\\
      M[i-1,j] + 1,\;\text{(burta dzēšana)}
      \end{array} \right. 


  Ar indukciju var pamatot, ka šādi rēķinot :math:`M[i,j]` visiem 
  :math:`i \in [1,m]` un :math:`j \in [1,n]`, matricas labajā apakšējā 
  stūrī iegūsim :math:`M[m,n]`, kas būs Levenšteina attālums
  starp vārdiem :math:`A` un :math:`B`.

  Sal. `Editierdistantz <https://de.wikipedia.org/wiki/Levenshtein-Distanz>`_




Levenšteina attālums ar dinamisko programmēšanu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| :math:`\text{\sc LevensteinDistance}(A, B)`
| 1. :math:`\quad` :math:`m = A.\mathit{length}`
| 2. :math:`\quad` :math:`n = B.\mathit{length}`
| 3. :math:`\quad` **for** :math:`i = 0` **to** :math:`m`:
| 4. :math:`\quad\quad` :math:`M[0,i] = 0`
| 5. :math:`\quad` **for** :math:`j = 0` **to** :math:`n`:
| 6. :math:`\quad\quad` :math:`M[j,0] = 0`
| 7. :math:`\quad` **for** :math:`i = 1` **to** :math:`m`:
| 8. :math:`\quad\quad` **for** :math:`j = 1` **to** :math:`n`:
| 9. :math:`\quad\quad\quad` **if** :math:`A[i] == B[j]`
| 10. :math:`\quad\quad\quad\quad` :math:`M[i,j] = M[i-1,j-1]`
| 11. :math:`\quad\quad\quad` **else** :math:`M[i, j] = \min (M[i-1, j]+1,`
| 12. :math:`\quad\quad\quad\quad` :math:`M[i, j-1]+1, M[i-1, j-1]+1)`
| 13. :math:`\quad` **return** :math:`M[m,n]`


**Piemērs:** 
  Atrast Levenšteina attālumu starp :math:`A=\mathtt{tcat}` 
  un :math:`B=\mathtt{atcaca}`. 
  Aizpildām :math:`5 \times 7` matricu: 

  .. figure:: figs/levenstein-distance.png
     :width: 2in


No šīs tabulas uzzinām, ka minimālais operāciju skaits ir :math:`3`.  
No tabulas var arī atjaunot optimālo labojumu virkni. To dara no beigām.

1. :math:`M[4,6]=3` iegūts, pieskaitot :math:`1` pie :math:`M[4,5]=2`.
2. :math:`M[4,5]=2` iegūts, pieskaitot :math:`1` pie :math:`M[3,4] = 1`.
3. :math:`M[3,4]=1` iegūts no :math:`M[2,3]=1`, iegūts no :math:`M[1,2]=1`, 
   iegūts no :math:`M[0,1]=1`.

Tas nozīmē, ka :math:`\mathtt{atcaca}` no :math:`\mathtt{tcat}` var iegūt šādi:

.. math::

  \mathtt{tcat} \rightarrow \mathtt{atcat} \rightarrow \mathtt{atcac} \rightarrow \mathtt{atcaca}.





Hešfunkcijas stringu salīdzināšanā
------------------------------------

Rabina-Karpa algoritms meklē apakšstringu :math:`P` tekstā :math:`T` 
ātrāk nekā naivais algoritms (uzlabojums no :math:`O(mn)` uz :math:`O(n)` jeb 
teksta garums). 
Stringu meklēšanu aizstāj ar skaitļu salīdzināšanu. 
Uztveram gan tekstu :math:`T`, gan meklējamo paraugu :math:`P` kā 
(lielus) veselus skaitļus.

Ja :math:`T` un :math:`P` pierakstīti 10-ciparu alfabētā, tad tie jau 
tāpat ir skaitļi. Vispārīgajā gadījumā 
alfabēta izmērs nav 10, bet tad pieraksta :math:`T` un :math:`P` skaitīšanas sistēmā 
ar citu bāzi (*radix-d notation*), kur :math:`d` - burtu skaits alfabētā.

**Piemērs:** 
  Dots strings "pt". Ievērojam, ka burtu "p" un "t" ASCII 
  baiti ir attiecīgi :literal:`x70` un :literal:`x74` (heksadecimālajā pierakstā). 
  Tātad to decimālās vērtības ir attiecīgi :math:`112` un :math:`116`. 
  Un ASCII alfabētā ir pavisam :math:`128` simboli. 

  Iegūstam, ka stringa "pt" vērtība bāzes-:math:`128` (*radix*-:math:`128`) 
  pierakstā būs :math:`112 \cdot 128 + 116 = 14452`. 


Rabina-Karpa algoritma pamatideja
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Tekstā :math:`T` meklēsim ciparu virknes garumā :math:`m` (parauga :math:`P` garums), 
   kas skaitliski vienādas ar :math:`P`. 
2. Ar :math:`t_s` apzīmējam (decimālajā sistēmā pārveidotu) skaitli, 
   ko veido skaitīšanas bāzē-:math:`d` (*radix*-:math:`d`) cipari: 
   :math:`T[s],T[s+1],\ldots,T[s+m-1]`, kur nobīde
   :math:`s` var būt :math:`0,1,\ldots,n-m`.
3. Ja zināms :math:`t_s`, tad :math:`t_{s+1}` var iegūt 
   ar algebrisku triku:

   .. math::

      t_{s+1} = \left( t_s - d^{m-1}T[s] \right) \cdot d + T[s+m].

   - No :math:`t_s` atņem kreisā/vecākā cipara vērtību :math:`d^{m-1}T[s]`,
   - Pabīda citus ciparus vienu pozīciju uz augšu (piereizina ar :math:`d`),
   - Visbeidzot pieskaita jaunāko ciparu :math:`T[s+m]`. 


**Piemērs:**

  * Dots "teksts" 10-ciparu alfabētā: :math:`T=\mathtt{31415926}`
    (garums :math:`n=8`); paraugs :math:`P = \mathtt{14159}` (garums :math:`m=5`).
  * Aplūkojam visus :math:`T` apakšstringus garumā :math:`m=5`:
    
    .. math::

     t_0 = 31415,\;t_1 = 14159,\,t_2=41592,\;t_3 = 15926.

  * Pirmo skaitli :math:`t_0 = \textcolor{red}{\mathtt{31415}}` iegūst ar *Hornera shēmu*:
  
    .. math::

       t_0 = 10 \cdot (10 \cdot (10 \cdot (10 \cdot \textcolor{red}{\mathtt{3}} + \textcolor{red}{\mathtt{1}}) + \textcolor{red}{\mathtt{4}}) + \textcolor{red}{\mathtt{1}}) + \textcolor{red}{\mathtt{5}} = 31415.

  * :math:`t_1` iegūst no :math:`t_0` konstantā laikā (tāpat :math:`t_2` no :math:`t_1` utt.):
    
    .. math::

      t_1 = (t_0 - 10^4 \cdot T[0])\cdot 10 + T[5] = (\textcolor{red}{\mathtt{3}}\textcolor{teal}{\mathtt{1415}} - 10000 \cdot \textcolor{red}{\mathtt{3}}) \cdot 10 + \textcolor{red}{\mathtt{9}} = \textcolor{teal}{\mathtt{1415}}\textcolor{red}{\mathtt{9}}.


**Ko darīt ar ļoti lieliem skaitļiem?**
  Meklējamie paraugi mēdz būt gari, polinomu vērtības, kas iegūstamas
  ar Hornera shēmu, var būt lieli skaitļi. Lai algoritma ātrdarbība
  no tā neciestu, pārbaudām nevis vienādību pašiem :math:`t_s` (teksta :math:`T` gabals
  garumā :math:`m` nobīdīts par :math:`s` simboliem) ar paraugam :math:`P` atbilstošo 
  bāzes-:math:`d` pieraksta skaitli :math:`p`, bet gan kongruenci: 

  .. math::

     t_s \equiv p\;(\text{mod}\,q),

  kur :math:`q` izvēlas pietiekami lielu, lai bieži neparādītos 
  *Viltus trāpījumi* (*spurious hits*).







Rabina-Karpa algoritma pseidokods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| :math:`\text{\sc RabinKarpMatcher}(T, P, d, q)`
| 1. :math:`\quad` :math:`n = T.\mathit{length}`
| 2. :math:`\quad` :math:`m = P.\mathit{length}`
| 3. :math:`\quad` :math:`h = d^{m-1}\,\text{mod}\,q`
| 4. :math:`\quad` :math:`p = 0`
| 5. :math:`\quad` :math:`t_0 = 0`
| 6. :math:`\quad` **for** :math:`i = 0` **to** :math:`m-1`: *// saskaita pēc Hornera shēmas*
| 7. :math:`\quad\quad` :math:`p = (d \cdot p + P[i])\,\text{mod}\,q`
| 8. :math:`\quad\quad` :math:`t_0 = (d \cdot t_0 + T[i])\,\text{mod}\,q`
| 9. :math:`\quad` **for** :math:`s = 0` **to** :math:`n-m`:
| 10. :math:`\quad\quad` **if** :math:`p == t_s`
| 11. :math:`\quad\quad\quad` **if** :math:`(P[0],\ldots,P[m-1]) == (T[s],\ldots,T[s+m-1])`
| 12. :math:`\quad\quad\quad\quad` :math:`\text{print "Paraugs parādās ar nobīdi" } s`
| 13. :math:`\quad\quad` **if** :math:`s < n-m`
| 14. :math:`\quad\quad\quad` :math:`t_{s+1} = (d(t_s - T[s]\cdot h) + T[s+m])\,\text{mod}\,q`


**Kā izvēlēties moduli:**
  Ja :math:`q` ir pārāk mazs, tad aritmētika pēc :math:`q` moduļa ir ļoti ātra, 
  bet bieži rodas viltus trāpījumi. 
  Ja :math:`q` ir pārāk liels, tad reizināšanas tabulas uzbūvēšana modulārajai 
  aritmētikai iznāk laikietilpīga.



Ripojošās hešfunkcijas
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hešfunkcijas aprēķināšanas sarežģītību 
parasti pieņem par konstanti :math:`O(1)`, bet ievadei garumā :math:`m` burti, 
tie parasti ir jāizlasa un jāapstrādā, tāpēc hešfunkcijas sarežģītība faktiski 
ir :math:`O(m)`. Par laimi, īpašās situācijās ir izņēmumi -- tādas hešfunkcijas, 
kuras var izrēķināt ātrāk, ja tās rēķina *slīdošajā logā*.  
Slīdošajā logā nākamais substrings līdzīgs iepriekšējam. 
Pirmā hešfunkcija prasa :math:`O(m)` laiku, bet katru nākamo 
var rēķināt konstantā laikā.


Ripojošo hešfunkciju var uztvert kā *abstraktu datu tipu* (ADT): 
Tas uzkrāj ievades fragmentu kā sarakstu/rindu un atbalsta šādas operācijas:

* :math:`RH` ``:=`` :math:`\text{\sc RollingHash}(\mathtt{[]})` -- 
  inicializē hešfunkciju uz tukša simbolu saraksta (piešķirot tam kādu skaitlisku vērtību).
* :math:`RH.\text{\sc hash}()` -- atgriež pašreizējā saraksta hash vērtību.
* :math:`RH.\text{\sc append}(val)` -- pievieno simbolu ``val`` saraksta beigām (līdzīgi kā ``Q.enqueue(val)`` rindai ``Q``).
* :math:`RH.\text{\sc skip}(val)` -- noņem priekšējo elementu no saraksta (līdzīgi kā ``Q.dequeue(val)`` rindai ``Q``).
  Parametru ``val`` funkcijai ``skip()`` bieži nenorāda, jo tas redzams 
  saraksta priekšā, kas jau glabājas kā hešfunkcijas datu parametrs.

Elementi šajā sarakstā tiek attēloti kā veseli skaitļi kādā skaitīšanas sistēmā.
Piemēram, ja mēs interpretējam rakstzīmes kā ASCII kodus, tad
rakstzīme ``'A'`` glabājas kā 65 un ``'B'`` glabājas kā 66.

Mēs aplūkojam tekošo ievades fragmentu kā daudzciparu skaitli :math:`u \in \mathcal{U}`
bāzē :math:`a` (ripojošās hešfunkcijas ievadi var interpretēt kā lielu skaitli).
Piemēram, mēs varam izvēlēties :math:`a = 256`, kas ir ASCII koda alfabēta izmērs.


Ir pazīstamas vairākas ripojošās hešfunkcijas ar labām īpašībām. 

**Polinomiālā hešfunkcija**
  Šīs hešfunkcijas vērtības ir atlikumi pēc moduļa :math:`q`. 

  .. math:: 

    H\left( \overline{c_1c_2\ldots{}c_k} \right) = 
    \left( c_1 a^{k-1} + c_2 a^{k-2} + c_3 a^{k-3} + ... + c_k a^{0} \right)\;\text{mod}\;q.

  Šāds polinoms ir līdzvērtīgs skaitļa pierakstam pozicionālajā skaitīšanas sistēmā 
  ar bāzi :math:`a`, kur :math:`a` var izvēlēties kā alfabēta izmēru, kas satur 
  visus :math:`c_i`. Savukārt :math:`q` ir kāds pietiekami liels pirmskaitlis,  
  kas tomēr ir ievērojami mazāks par :math:`a^k` -- slīdošajā logā esošo informāciju.

  Ja hešfunkcija ripo tālāk -- saņem jaunu burtu :math:`c_{k+1}`, 
  bet nomet :math:`c_1`, tad jaunā vērtība iegūstama no iepriekšējās :math:`H` šādi:

  .. math:: 

    H \left( \overline{c_2\ldots{}c_k{}c_{k+1}} \right) = 
    \left( \left( H - c_1 a^{k-1} \right) \cdot a + c_{k+1} \right)\;\text{mod}\;q.




**Cikliskie polinomi**

  Šīs hešfunkcijas vērtības ir bitu virknītes kaut kādā fiksētā garumā. 

  Šajā formulā ar :math:`s` apzīmēta bitu rotēšana 1 pozīciju pa kreisi. 
  Attiecīgi, :math:`s^2` ir rotēšana par 2 pozīcijām pa kreisi utt. 
  Operācija :math:`\oplus` ir bitveida XOR. 
  
  .. math:: 

    H \left( \overline{c_1c_2\ldots{}c_k} \right) = 
    s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) ) \oplus \ldots 
    \oplus  s( h(c_{k-1}) ) \oplus h(c_k)

  Ja hešfunkcija ripo tālāk -- saņem jaunu burtu :math:`c_{k+1}`, 
  bet nomet :math:`c_1`, tad jaunā vērtība iegūstama no iepriekšējās :math:`H` šādi:

  .. math:: 

     H \left( \overline{c_2\ldots{}c_k{}c_{k+1}} \right) = s(H) \oplus s^{k}(h( c_1 )) \oplus h(c_{k+1})


**Rabina-Karpa algoritms vienam stringam P:** 

  | :math:`\text{\sc RabinKarpStringMatching}(T,P,a,q)`
  |     :math:`rP = \text{\sc RollingHash}(\mathtt{[]})`
  |     :math:`rT = \text{\sc RollingHash}(\mathtt{[]})`
  |     **for** :math:`i` **in** :math:`\text{\sc range}(0,len(P))`:
  |         :math:`rP.\text{\sc append}(P[i])`
  |         :math:`rT.\text{\sc append}(T[i])`
  |     **for** :math:`i` **in** :math:`\text{\sc range}(len(P),len(T))`:
  |         **if** :math:`rP.\text{\sc hash}()` ``==`` :math:`rT.\text{\sc hash}()`:
  |             (*Here we need to double-check as collisions are possible*)
  |             **if** :math:`P` ``==`` :math:`T[i - len(P) + 1: i+1]`
  |                 **output** "Pattern found at offset", :math:`i - len(P)+1`
  |         :math:`rT.\text{\sc skip}(T[i - len(P)])`
  |         :math:`rT.\text{\sc append}(T[i])`


**Laika sarežģītība sliktākajā gadījumā:** 
  Vai var nodrošināt, ka arī sliktākajā gadījumā viltus pozitīvie
  (hešfunkciju sakritība pat tad, ja paterns nav atrasts) 
  negadās biežāk kā ar varbūtību :math:`1/len(P)`?


**Rabina-Karpa algoritms vairākiem stringiem P:** 

  Uzdevums: Mums ir teksts :math:`T` ar garumu :math:`n`.
  Šobrīd mums ir :math:`k` meklējamie stringi 
  :math:`\mathcal{P} = \{ P_0, P_1, \ldots, P_{k-1} \}`; visiem 
  tiem ir vienāds garums :math:`m`.

  | :math:`\text{\sc RabinKarpMultiString}(T, \mathcal{P}, m)`:
  |     :math:`hashes` ``:=`` :math:`Set.\text{\sc Empty}()`
  |     **foreach** :math:`P_i \in \mathcal{P}`:
  |         :math:`rP_i = \text{\sc RollingHash}(\mathtt{[]})`
  |         **for** :math:`j` **in** :math:`\text{\sc range}(0,m)`:
  |             :math:`rP_i.\text{\sc append}(P[j])`
  |         :math:`hashes.\text{\sc insert}(rP_i.\text{\sc hash}())`
  |     :math:`rT = \text{\sc RollingHash}(\mathtt{[]})`
  |     **for** :math:`j` **in** :math:`\text{\sc range}(0,m)`:
  |         :math:`rT.\text{\sc append}(T[i])`
  |     **for** :math:`j` **in** :math:`\text{\sc range}(1,n-m+1)`
  |         **if** :math:`rT.\text{\sc hash}() \in hashes` **and** :math:`T[j:j+m-1] \in \mathcal{P}`
  |             **output** "Pattern found at offset", :math:`j`
  |         :math:`rT.\text{\sc skip}(T[j])`
  |         :math:`rT.\text{\sc append}(T[j+m])`

Šim algoritmam ir laika sarežģītība :math:`O(n + km)`.
Naivajai stringu meklēšanai būtu laika sarežģītība :math:`O(nmk)`, ja 
mēs pārbaudītu meklējamos stringus pa vienam. 




MinHash Algoritmi
~~~~~~~~~~~~~~~~~~~~

**Definīcija:** 
  Teksta dokumenta sadalīšana n-grammās (*shingling*) ir procedūra, kurā
  no teksta izgriež noteikta garuma gabalus (piemēram, visas burtu virknītes 
  garumā :math:`5` simboli, vai visi vārdi, vai visas :math:`5` vārdu virknītes). 
  Der arī citas procedūras, kas izveido kolekciju ar savstarpēji pārklājošamies 
  burtu virknītēm. 


Sadalīšana n-grammās pārvieto uz priekšu fiksēta vai mainīga izmēra 
*slīdošo logu* un pārvērš dokumentu par n-grammu kopu. 
Ja mūs interesē veseli vārdi (nevis vārdu fragmenti fiksētā garumā) 
pirms n-grammu iegūšanas dokumentam 
var lietot atstarpju normalizēšanu (*space normalization*) - to pārraksta 
ar mazajiem burtiem, izmet visas pieturzīmes, un dažāda veida 
atstarpes (tabulācijas, parastas atstarpes, rindu pārnesumus utml.) aizstāj 
ar vienkāršām atstarpēm. 

Plaģiāta vai citas teksta kopēšanas atpazīšanai var izmantot, 
piemēram, :math:`5` vārdu slīdošo logu. 
Ja divos dokumentos ir daudzas identiskas virknītes ar 5 pēc kārtas 
sekojošiem vārdiem, tad to parasti nevar izskaidrot ar nejaušu 
sagadīšanos -- dokumenti ir kopēti viens no otra (vai no kopīga pirmavota). 
Pati šī sakritība plaģiātu vēl nepierāda, jo var gadīties, ka abi 
dokumenti izmanto to pašu citātu.



**Definīcija:** 
  Par divu kopu :math:`A` un :math:`B` Žakāra indeksu (Jaccard coefficient)
  sauc abu kopu šķēluma attiecību pret to apvienojumu: 

  .. math:: 

    J(A,B) = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}. 
  
Līdzīgām kopām (vai dokumentu n-grammu sadalījumiem) atbilst :math:`J(A,B)`, kas 
ir tuvu skaitlim :math:`1`. 


*Piezīme:* MinHash algoritmiem ir svarīgi, lai hešfunkciju vērtības būtu savstarpēji 
neatkarīgas un ar vienmērīgiem varbūtiskiem sadalījumiem. Var izmantot
Python iebūvēto hešfunkciju, bet ar dažādiem moduļiem. 
Ripojošās hešfunkcijas nav piemērotas.

Šis algoritms rēķina Žakāra indeksa novērtējumu :math:`J(S_1, S_2)`, 
ja dots saraksts :math:`\mathcal{H}` -- kolekcija ar hešfunkcijām. 


| :math:`\text{\sc MinHash}(S_1, S_2, \mathcal{H})`
| 1. :math:`\quad` :math:`\mathrm{sig}_1 = []`, :math:`\mathrm{sig}_2 = []` :math:`\quad` *// inicializē MinHash sarakstus* 
| 2. :math:`\quad` **for** :math:`h_i` **in** :math:`\mathcal{H}`:
| 3. :math:`\quad\quad` :math:`\mathrm{minHash}_1 = \infty`, :math:`\mathrm{minHash}_2 = \infty` :math:`\quad` *// sāk ar bezgalību, lai rēķinātu minimumu* 
| 4. :math:`\quad\quad` **for** :math:`s` **in** :math:`S_1`:
| 5. :math:`\quad\quad\quad` :math:`\mathrm{hValue} = h_i(s)` :math:`\quad` *// aprēķina hešfunkciju* 
| 6. :math:`\quad\quad\quad` **if** :math:`\mathrm{hValue} < \mathrm{minHash}_1`:
| 7. :math:`\quad\quad\quad\quad` :math:`\mathrm{minHash}_1 = \mathrm{hValue}`
| 8. :math:`\quad\quad` **for** :math:`s` **in** :math:`S_2`:
| 9. :math:`\quad\quad\quad` :math:`\mathrm{hValue} = h_i(s)`  :math:`\quad` *// aprēķina hešfunkciju*
| 10. :math:`\quad\quad\quad` **if** :math:`\mathrm{hValue} < \mathrm{minHash}_2`:
| 11. :math:`\quad\quad\quad\quad` :math:`\mathrm{minHash}_2 = \mathrm{hValue}`
| 12. :math:`\quad\quad` :math:`\mathrm{sig}_1.append(\mathrm{minHash}_1)`, :math:`\mathrm{sig}_2.append(\mathrm{minHash}_2)` :math:`\quad` *// pievieno MinHash sarakstiem* 
| 14. :math:`\quad` :math:`intersection = 0`
| 15. :math:`\quad` **for** :math:`i = 0` **to** :math:`|\mathcal{H}| - 1`:
| 16. :math:`\quad\quad` **if** :math:`\mathrm{sig}_1[i] == \mathrm{sig}_2[i]`:
| 17. :math:`\quad\quad\quad` :math:`\mathrm{intersection} = \mathrm{intersection} + 1`
| 18. :math:`\quad` **return** :math:`\frac{\mathrm{intersection}}{|\mathcal{H}|}`  :math:`\quad` *// atgriež Žakāra indeksa novērtējumu*


Blūma filtri 
~~~~~~~~~~~~~~~~

Bieži ir jāmeklē stringi ļoti lielā dokumentu kolekcijā.
Optimālās hash tabulas, kas atrisina sadursmes ar *linear probing*, izmanto 
noslodzes koeficientus (glabāto objektu skaits, dalīts ar heštabulas izmēru)
ap :math:`\ln 2 \approx 0.7`. 
Piemēram, ja sagaidāms, ka heštabulā glabāsies :math:`1000` elementi,
tad optimālās heštabulas masīvs ir apmēram :math:`1400`.

Izveidojot n-grammu sarakstu daudziem gigabaitiem dokumentu, arī heštabulas 
izmērs būtu daudzi miljardi šūnu. Tas nav praktiski, ja plaģiāta programmai 
ir jāsalīdzina iesūtāmie dokumenti ar lielu jau esošo dokumentu kopu. 
Tāpēc ir noderīga optimizācija, ko sauc par *Blūma filtru*.

*Blūma filtrs* ir datu struktūra, kas līdzīga parastai kopai; tā 
atbalsta šādas operācijas:

* Izveido tukšu Blūma filtru: ``BF = EmptySet()``
* Pievienot jaunu kopas elementu: ``BF.add(item)``.
* Pārbaudīt, vai elements pieder kopai: ``BF.contains(item)`` (atgriež Boolean vērtību true/false).


*Piezīme:* Atšķirībā no parastām kopām (tsk. kopām parastās heštabulās) 
Blūma filtri parasti neatbalsta elementu dzēšanu. 
Tie ir noderīgi situācijās, kad jānosaka elementa piederība kādai lielai 
kopai, bet ir ierobežota vieta, kur šo kopu glabāt.

To var realizēt, izveidojot :math:`k` hešfunkcijas -- katra no tām nejauši
un neatkarīgi no citām hash funkcijām, attēlo objektu uz vienu no :math:`m` bitiem.
Funkcija ``BF.add(item)`` izrēķina visas :math:`k` hešfunkcijas un uzstāda 
attiecīgos bitus. 

Funkcija ``BF.contains(item)`` tāpat izrēķina visas :math:`k` hešfunkcijas
un atgriež ``true`` tad un tikai tad, ja visās :math:`k` vietās atrasti vieninieki. 
Iespējamas divas situācijas: 

* Ja ``item`` tiešām ir pievienots Blūma filtram, to vienmēr arī atradīs. 
  Blūma filtros nevar būt *false negatives*. 
* Ja ``item`` nekad nebija pievienots Blūma filtram, pastāv varbūtība, ka
  citu elementu pievienošanas dēļ ir uzstādīti vieninieki visās :math:`k` 
  pārbaudītajās vietās. Novērtēsi šo *false positive* varbūtību. 


Pieņemsim, ka esam ievietojuši :math:`n` elementus, iespējamība, ka noteikts
bits joprojām ir :math:`0`, ir:

.. math::

  p = \left(1-\frac{1}{m}\right)^{kn} \approx e^{-kn/m};

Lai pārbaudītu elementa piederību kopai, ar katru no :math:`k` 
hešfunkcijām aprēķinātās pozīcijas masīvā būs :math:`1` ar varbūtību :math:`(1-p)`.
Iespējamība, ka tās visas ir :math:`1`, kā rezultātā Blūma filtrs kļūdaini norāda,
ka elements pieder kopai, ir šāda:

.. math::

  \varepsilon = \left(1-\left[1-\frac{1}{m}\right]^{kn}\right)^k \approx 
  \left( 1-e^{-kn/m} \right)^k.

Ņemot vērā bitu masīva lielumu :math:`m` un ievietojamo vienumu skaitu :math:`n`, 
varam atrast optimālo skaitli :math:`k`:

.. math::

  k = \frac{m}{n} \ln 2

Ja zinām pieļaujamo viltus pozitīvu rezultātu maksimālo :math:`\varepsilon`, 
tad var pielāgot :math:`m` vērtību atbilstoši,
lai ierobežotu viltus pozitīvo varbūtību.


**Tekstu ciparnospiedumu lietojumi:** 
  Ciparnospiedumi (*fingerprints*) -- MinHash, Blūma filtri vai 
  līdzīgas hešfunkciju vērtības vai to komplekti ļauj atrast sakrītošos gabalus dokumentos.
  Plaģiāta atrašanas algoritmi un arī Datu noplūdes novēršana (*Data Leak Prevention, DLP*)
  palīdz atklāt, vai jaunais dokuments ir līdzīgs kādam no esošajiem. 
  Šo derīgo īpašību var izmantot komerciālos produktos: 

  * **Turnitin** - komerciāls serviss, pārbauda studentu eseju līdzību ar 
    tur jau esošiem darbiem. Abonēšanas modelis, darbojas kopš 1997.g.  
    Vai ir ētiski gūt peļņu no studentu radītiem oriģināliem darbiem?
  * **Plag.lv** - kaut kas līdzīgs. Sk. rakstu 
    `Latvijā palaista programma <https://www.tvnet.lv/4838652/latvija-palaista-programma-kas-atklaj-plagiatu-akademiskos-darbos>`_. 
  * **Symantec DLP**, **Forcepoint DLP** - organizāciju pasargāšana no 
    konfidenciālu dokumentu noplūdes.


Uzdevumi
----------


**13.1. uzdevums (Ripojošā hešfunkcija ar polinomu):** 
  Pieņemsim, ka alfabētā ir :math:`a = 100` simboli.
  Katru simbolu pieraksta ar ciparu pāriem: :math:`\{ 00, 01, \ldots, 99 \}`.
  Izvēlieties ripojošā loga izmēru :math:`m = 5` un pirmskaitli :math:`q = 23`.

  Ievade ir šāda: ``[03, 14, 15, 92, 65, 35, 89, 79, 31]``.

  * Inicializējiet tukšu ripojošo hash ``rH`` un pievienojiet pirmos piecus 
    virknes locekļus, izmantojot ``append()`` funkciju:

    .. math::

      append(val) = ((u \cdot a) + val)\,\text{mod}\,q = ((u\,\text{mod}\,q) \cdot a + val)\,\text{mod}\,q.

  * Parādiet, kā ripojošā hash var "ripot" no saraksta ``[03, 14, 15, 92, 65]`` uz ``[14, 15, 92, 65, 35]`` 
    (vispirms izsaukt ``skip(03)``, tad izsaukt ``append(35)``).

**13.2. uzdevums (Ripojošā hešfunkcija ar ciklisku polinomu):**
  Aplūkosim :math:`16` latīņu burtus ar nejauši piešķirtiem 4-bitu kodiem 
  (t.i., :math:`L = 4`):

  ==========  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====
  Burts          A     B     C     D     E     F     G     H     I     J     K     L     M     N     O     P
  h(x)        1100  0100  0010  0110  0111  0000  1001  1111  0101  1101  1110  1011  0011  1010  1000  0001
  ==========  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====

  Pieņemsim, ka ripojošā loga izmērs ir :math:`k = 5`.
  Atrodiet hash vērtību :math:`ABIDE` un pēc tam rotējiet to uz :math:`BIDEN`.
  Lūdzu, atgādiniet, ka ripojošā hešfunkcija izmanto šādu formulu:

  .. math::

    H = s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) )  \oplus \ldots \oplus  s( h(c_{k-1}) ) \oplus   h(c_k),


**13.3. uzdevums (Formulas ripojošajai hešfunkcijai):**
  Uzzīmējiet formulas Cikliskā polinoma ripojošajai hešfunkcijai:

  * Formula, kas piešķir sākumvērtību ``RH`` tukšai ievadei.
  * Formula, kas pievieno jaunu rakstzīmi :math:`c_i` tekošajam stringam.
  * Formula, kas izlaiž esošā saraksta pirmo elementu :math:`c_j`, saīsinot tekošo stringu.

**13.4. uzdevums (Naivās tekstu meklēšanas vidējā sarežģītība)**
  Pieņemsim, ka paraugs :math:`P` un teksts :math:`T` ir nejauši izvēlēti 
  virknēm ar garumiem :math:`m` un :math:`n`
  no alfabēta ar :math:`a` burtiem (:math:`a \geq 2`). 
  Kāds ir sagaidāmais burtu salīdzināšanu skaits naivajā algoritmā,
  ja katram salīdzinājumam ir izdošanās iespēja :math:`1/a`?







