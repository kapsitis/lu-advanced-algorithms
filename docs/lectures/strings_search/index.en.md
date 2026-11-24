---
layout: default
title: "String Searching"
lang: en
permalink: /lectures/strings_search/en/
---
# 13. String Searching

In this chapter we define the string searching problem and its variants (finding the longest common substring, searching for patterns in many documents at once, preprocessing or indexing documents). The following algorithms are covered:

* The naive substring search algorithm
* An algorithm to compute the Levenshtein distance
* Rolling hash functions
* The Rabin–Karp substring search algorithm
* The Knuth–Morris–Pratt (KMP) algorithm
* The Boyer–Moore (BM) algorithm

## Introduction to String Searching

String searching appears in different applications, and they need different algorithms:

* Text editors: 1 word, 1 document
* Data leak prevention (DLP): many patterns (words, regular expressions), 1 document to check.
* Document retrieval: a few patterns, many documents that can be preprocessed/indexed to make searching in them faster (for example, Lucene/Elasticsearch).
* Plagiarism detection: many documents, 1 document to check; find the "copy-pasted" fragments, or the "copy-pasted" and slightly edited ones.

**Substring search problem:** We are given a *text* -- a string of $n$ symbols: $T = T[0], \ldots, T[n-1]$. We are also given a *pattern* -- a string of $m$ symbols: $P = P[0], \ldots, P[m-1]$.

Question: Does the text $T$ contain the substring $P$? (The algorithm outputs either the first position where $P$ occurs in $T$, or all such positions.)

**Definition:** A position in the text $T$ (a number from $0$ to $n-1$) where the pattern may start is called a *shift*.

### Substrings and Subsequences

The Latvian word *virkne* can mean both a "sequence" (finite or infinite, of objects of any kind) and a "string" (a finite sequence of letters of a finite alphabet). Here is an example where the two notions differ:

**Definition:** A *substring* of the string $T[0],T[1],\ldots,T[n-1]$ is a sequence of symbols $T[i]$ where the values of $i$ are consecutive. (A substring is obtained by deleting some pieces at the beginning and at the end of the original string. The empty string $\varepsilon$ and the text $T$ itself are also substrings.)

**Definition:** A *subsequence* of the string $T[0],T[1],\ldots,T[n-1]$ is a sequence of symbols $T[i]$ where the values of $i$ increase, but need not be consecutive. (A subsequence is obtained by deleting $0$ or more symbols anywhere in the original string.)

**Example:** The string $\mathtt{ABCDE}$ has these $15$ substrings:

$$
\varepsilon,
\mathtt{A}, \mathtt{AB}, \mathtt{ABC}, \mathtt{ABCD}, \mathtt{ABCDE},
\mathtt{B}, \mathtt{BC}, \mathtt{BCD}, \mathtt{BCDE},
\mathtt{C}, \mathtt{CD}, \mathtt{CDE},
\mathtt{D}, \mathtt{DE},
\mathtt{E}
$$

A string of $n$ symbols has at most ${\displaystyle 1 + \frac{n(n+1)}{2}}$ substrings (the maximum is reached when all letters are different).

**Example:** The string $\mathtt{ABCDE}$ has these $32$ subsequences:

$$
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
$$

A string of $n$ symbols has at most ${\displaystyle 2^n}$ subsequences (reached when all letters are different).

### The Naive String Searching Algorithm

$\textsf{NaiveStringMatcher}(T, P)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. **for** $i = 0$ **to** $n-m$:
4. $\quad$ **if** $(P[0],\ldots,P[m-1]) == (T[i],\ldots,T[i+m-1])$:
5. $\quad\quad \text{print "Pattern occurs with shift" } i$

The algorithm places one string under the other and compares the letters from left to right:

$$
\begin{array}{llllll}
\ldots, & T[i], & T[i + 1], & \ldots, & T[i+m-1], & \ldots \\
& P[0], & P[1], & \ldots, & P[m-1] &
\end{array}
$$

If all $m$ elements of the pattern match, the substring has been found.

**Claim:** The time complexity of the naive substring search algorithm is $O(n \cdot m)$ in the worst case.

**Proof:** There are $n - m + 1$ possible values of the variable $s$. For each of them, up to $m$ symbols may have to be compared. The time is $(n - m + 1) \cdot m \approx n \cdot m$.

Usually the pattern is assumed to be much shorter than the text: $m \ll n$. Still, $m$ can be large too, so $O(n \cdot m)$ is much worse than, for example, $O(n)$ -- a linear dependence on the text length.

**Example:** For these values of $T$ and $P$ the running time cannot be improved:

$$
\left\lbrace \begin{array}{ll}
T = & \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{letters}}\\
P = & \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m\;\text{letters}}\\
\end{array} \right.
$$

This is also a worst case for the naive algorithm:

$$
\left\lbrace \begin{array}{ll}
T = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{n\;\text{letters}}\\
P = \underbrace{\mathtt{aa}\ldots\mathtt{a}}_{m-1\;\text{letters}}\mathtt{b}\\
\end{array} \right.
$$

## Edit Distance

We are given strings $A = A[0]\ldots{}A[m-1]$ and $B = B[0]\ldots{}B[n-1]$ of lengths $m$ and $n$ respectively. The following operations, or *edits*, are allowed:

* Replace one symbol with another symbol;
* Delete any one symbol;
* Insert a new symbol at any position.

**Definition:** The *Levenshtein distance* (*edit distance*) $M(A,B)$ between two words $A=A[0]\ldots{}A[m-1]$ and $B=B[0]\ldots{}B[n-1]$ is the smallest number of edits that turn $A$ into $B$.

Other variants of the edit distance are also known:

* Replacing a symbol with another one costs twice as much as an insertion or a deletion.
* The string $A$ must be turned into some subsequence of $B$ (not into $B$ itself).
* The cost of an edit depends on the symbol that is deleted/inserted.
* A substring of $k$ symbols can be inserted/deleted in one move at cost $f(k)$ (here $f(k)<k$, i.e. inserting a substring is cheaper than changing $k$ letters one by one).

Such *sequence alignment* problems arise in bioinformatics. For example, how many mutations does it take to turn one DNA sequence into another? The Levenshtein distance is one of the simplest variants.

**Levenshtein distance as a shortest path in a graph:** If an $m$-letter word $u$ must be turned into an $n$-letter word $v$, we build a rectangular grid of circles with $m+1$ rows and $n+1$ columns. Each circle has "coordinates" $(i,j)$ if it is in row $i$ and column $j$ ($i \in [0;m]$, $j \in [0;n]$).

<img
  alt="Levenshtein distance as a shortest path in a graph"
  src="{{ '/lectures/strings_search/figs/graph-distances.png' | relative_url }}"
  style="width: 100%; max-width: 384px; border:none; background-color:#FFFFFF;"
/>

* All arrows pointing right have weight $1$ (inserting a letter)
* All arrows pointing down have weight $1$ (deleting a letter)
* Diagonal arrows from $(i,j)$ to $(i+1,j+1)$ have weight $1$ (replacing a letter with another one), **except** when the letters are equal: $u[i] = v[j]$. In that case the letter need not be changed, and the arrow can be used for free.

The Levenshtein distance is the shortest path from the top-left vertex to the bottom-right one.

**Levenshtein distance with matrix recurrences:** We are given words $A=A[0]\ldots{}A[m-1]$ and $B=B[0]\ldots{}B[n-1]$. We define an $(m+1) \times (n+1)$ matrix $M[i,j]$ with these relations:

$$
M[0,0]=0,
$$

$$
M[i,0]=i,\;1 \leq i \leq m,
$$

$$
M[0,j]=j,\;1 \leq j \leq n\\
$$

$$
M[i,j]=\min \left\lbrace \begin{array}{l}
  M[i-1,j-1] + 0,\;\text{if}\;A[i-1] = B[j-1]\\
  M[i-1,j-1] + 1,\;\text{(replacing a letter)}\\
  M[i,j-1] + 1,\;\text{(inserting a letter)}\\
  M[i-1,j] + 1,\;\text{(deleting a letter)}
  \end{array} \right.
$$

By induction one can show that, computing $M[i,j]$ in this way for all $i \in [1,m]$ and $j \in [1,n]$, the bottom-right corner of the matrix will contain $M[m,n]$, the Levenshtein distance between the words $A$ and $B$.

Cf. [Editierdistantz](https://de.wikipedia.org/wiki/Levenshtein-Distanz)

### Levenshtein Distance with Dynamic Programming

$\textsf{LevensteinDistance}(A, B)$
1. $m = A.\mathit{length}$
2. $n = B.\mathit{length}$
3. **for** $i = 0$ **to** $m$:
4. $\quad M[i,0] = i$
5. **for** $j = 0$ **to** $n$:
6. $\quad M[0,j] = j$
7. **for** $i = 1$ **to** $m$:
8. $\quad$ **for** $j = 1$ **to** $n$:
9. $\quad\quad$ **if** $A[i-1] == B[j-1]$
10. $\quad\quad\quad M[i,j] = M[i-1,j-1]$
11. $\quad\quad$ **else** $M[i, j] = \min (M[i-1, j]+1,$
12. $\quad\quad\quad M[i, j-1]+1, M[i-1, j-1]+1)$
13. **return** $M[m,n]$

**Example:** Find the Levenshtein distance between $A=\mathtt{tcat}$ and $B=\mathtt{atcaca}$. We fill in a $5 \times 7$ matrix:

<img
  alt="Levenshtein distance matrix"
  src="{{ '/lectures/strings_search/figs/levenstein-distance.svg' | relative_url }}"
  style="width: 100%; max-width: 292px; border:none; background-color:#FFFFFF;"
/>

From this table we learn that the minimum number of operations is $3$. The table also lets us reconstruct an optimal sequence of edits. This is done from the end.

1. $M[4,6]=3$ is obtained by adding $1$ to $M[4,5]=2$.
2. $M[4,5]=2$ is obtained by adding $1$ to $M[3,4] = 1$.
3. $M[3,4]=1$ is obtained from $M[2,3]=1$, which is obtained from $M[1,2]=1$, which is obtained from $M[0,1]=1$.

This means that $\mathtt{atcaca}$ can be obtained from $\mathtt{tcat}$ like this:

$$
\mathtt{tcat} \rightarrow \mathtt{atcat} \rightarrow \mathtt{atcac} \rightarrow \mathtt{atcaca}.
$$

## Hash Functions for Comparing Strings

The Rabin–Karp algorithm searches for a substring $P$ in a text $T$ faster than the naive algorithm (an improvement from $O(mn)$ to $O(n)$, the length of the text). String searching is replaced by comparing numbers. We treat both the text $T$ and the pattern $P$ as (large) integers.

If $T$ and $P$ are written in the alphabet of the 10 digits, they are numbers already. In general the alphabet size is not 10; then $T$ and $P$ are written in a numeral system with a different base (*radix-d notation*), where $d$ is the number of letters in the alphabet.

**Example:** We are given the string "pt". Note that the ASCII bytes of the letters "p" and "t" are `x70` and `x74` respectively (in hexadecimal). So their decimal values are $112$ and $116$. And the ASCII alphabet has $128$ symbols in total.

So the value of the string "pt" in base $128$ (*radix*-$128$) notation is $112 \cdot 128 + 116 = 14452$.

### The Main Idea of the Rabin–Karp Algorithm

1. In the text $T$ we search for strings of digits of length $m$ (the length of the pattern $P$) that are numerically equal to $P$.
2. Let $t_s$ denote the number (converted to the decimal system) formed by the base-$d$ (*radix*-$d$) digits $T[s],T[s+1],\ldots,T[s+m-1]$, where the shift $s$ can be $0,1,\ldots,n-m$.
3. If $t_s$ is known, $t_{s+1}$ can be obtained with an algebraic trick:

   $$
   t_{s+1} = \left( t_s - d^{m-1}T[s] \right) \cdot d + T[s+m].
   $$

   - Subtract the value of the leftmost/most significant digit $d^{m-1}T[s]$ from $t_s$,
   - Shift the other digits one position up (multiply by $d$),
   - Finally, add the new least significant digit $T[s+m]$.

**Example:**

* We are given a "text" in the 10-digit alphabet: $T=\mathtt{31415926}$ (length $n=8$); the pattern is $P = \mathtt{14159}$ (length $m=5$).
* Consider all substrings of $T$ of length $m=5$:

  $$
  t_0 = 31415,\;t_1 = 14159,\,t_2=41592,\;t_3 = 15926.
  $$

* The first number $t_0 = \textcolor{red}{\mathtt{31415}}$ is obtained with *Horner's scheme*:

  $$
  t_0 = 10 \cdot (10 \cdot (10 \cdot (10 \cdot \textcolor{red}{\mathtt{3}} + \textcolor{red}{\mathtt{1}}) + \textcolor{red}{\mathtt{4}}) + \textcolor{red}{\mathtt{1}}) + \textcolor{red}{\mathtt{5}} = 31415.
  $$

* $t_1$ is obtained from $t_0$ in constant time (and likewise $t_2$ from $t_1$, etc.):

  $$
  t_1 = (t_0 - 10^4 \cdot T[0])\cdot 10 + T[5] = (\textcolor{red}{\mathtt{3}}\textcolor{teal}{\mathtt{1415}} - 10000 \cdot \textcolor{red}{\mathtt{3}}) \cdot 10 + \textcolor{red}{\mathtt{9}} = \textcolor{teal}{\mathtt{1415}}\textcolor{red}{\mathtt{9}}.
  $$

**What to do with very large numbers?** Patterns can be long, and the polynomial values computed with Horner's scheme can be large numbers. To keep the algorithm fast, we do not check whether $t_s$ itself (the piece of the text $T$ of length $m$ at shift $s$) equals the base-$d$ number $p$ of the pattern $P$; instead we check the congruence:

$$
t_s \equiv p\;(\text{mod}\,q),
$$

where $q$ is chosen large enough to avoid frequent *spurious hits*.

### Pseudocode of the Rabin–Karp Algorithm

$\textsf{RabinKarpMatcher}(T, P, d, q)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. $h = d^{m-1}\,\text{mod}\,q$
4. $p = 0$
5. $t_0 = 0$
6. **for** $i = 0$ **to** $m-1$: $\quad$ *// compute with Horner's scheme*
7. $\quad p = (d \cdot p + P[i])\,\text{mod}\,q$
8. $\quad t_0 = (d \cdot t_0 + T[i])\,\text{mod}\,q$
9. **for** $s = 0$ **to** $n-m$:
10. $\quad$ **if** $p == t_s$
11. $\quad\quad$ **if** $(P[0],\ldots,P[m-1]) == (T[s],\ldots,T[s+m-1])$
12. $\quad\quad\quad \text{print "Pattern occurs with shift" } s$
13. $\quad$ **if** $s < n-m$
14. $\quad\quad t_{s+1} = (d(t_s - T[s]\cdot h) + T[s+m])\,\text{mod}\,q$

**How to choose the modulus:** If $q$ is too small, arithmetic modulo $q$ is very fast, but spurious hits are frequent. If $q$ is too large, building the multiplication table for modular arithmetic takes too much time.

### Rolling Hash Functions

The complexity of computing a hash function is usually taken to be constant, $O(1)$. But for an input of $m$ letters, the letters normally have to be read and processed, so the complexity of the hash function is actually $O(m)$. Fortunately, there are exceptions in special situations -- hash functions that can be computed faster when they are computed over a *sliding window*. In a sliding window the next substring is similar to the previous one. The first hash value takes $O(m)$ time, but each next one can be computed in constant time.

A rolling hash can be seen as an *abstract data type* (ADT): it stores a fragment of the input as a list/queue and supports these operations:

* $RH$ `:=` $\textsf{RollingHash}(\mathtt{[]})$ -- initializes the hash function on an empty list of symbols (assigning some numeric value to it).
* $RH.\textsf{hash}()$ -- returns the hash value of the current list.
* $RH.\textsf{append}(val)$ -- appends the symbol `val` to the end of the list (similar to `Q.enqueue(val)` for a queue `Q`).
* $RH.\textsf{skip}(val)$ -- removes the front element from the list (similar to `Q.dequeue(val)` for a queue `Q`). The parameter `val` of `skip()` is often omitted, since it is visible at the front of the list, which is already stored in the data of the hash function.

The elements of this list are represented as integers in some numeral system. For example, if we interpret characters as ASCII codes, the character `'A'` is stored as 65 and `'B'` is stored as 66.

We treat the current input fragment as a multi-digit number $u \in \mathcal{U}$ in base $a$ (the input of a rolling hash can be interpreted as a large number). For example, we can choose $a = 256$, the size of the ASCII code alphabet.

Several rolling hash functions with good properties are known.

**Polynomial hash function:** The values of this hash function are remainders modulo $q$.

$$
H\left( \overline{c_1c_2\ldots{}c_k} \right) =
\left( c_1 a^{k-1} + c_2 a^{k-2} + c_3 a^{k-3} + ... + c_k a^{0} \right)\;\text{mod}\;q.
$$

Such a polynomial is equivalent to writing a number in a positional numeral system with base $a$, where $a$ can be chosen as the size of an alphabet that contains all $c_i$. And $q$ is some sufficiently large prime that is still much smaller than $a^k$ -- the information in the sliding window.

If the hash rolls on -- receives a new letter $c_{k+1}$ and drops $c_1$ -- the new value is obtained from the previous value $H$ like this:

$$
H \left( \overline{c_2\ldots{}c_k{}c_{k+1}} \right) =
\left( \left( H - c_1 a^{k-1} \right) \cdot a + c_{k+1} \right)\;\text{mod}\;q.
$$

**Cyclic polynomials:** The values of this hash function are bit strings of some fixed length.

In this formula $s$ denotes rotating the bits by 1 position to the left. Accordingly, $s^2$ is a rotation by 2 positions to the left, etc. The operation $\oplus$ is bitwise XOR.

$$
H \left( \overline{c_1c_2\ldots{}c_k} \right) =
s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) ) \oplus \ldots
\oplus  s( h(c_{k-1}) ) \oplus h(c_k)
$$

If the hash rolls on -- receives a new letter $c_{k+1}$ and drops $c_1$ -- the new value is obtained from the previous value $H$ like this:

$$
H \left( \overline{c_2\ldots{}c_k{}c_{k+1}} \right) = s(H) \oplus s^{k}(h( c_1 )) \oplus h(c_{k+1})
$$

**The Rabin–Karp algorithm for a single string P:**

$\textsf{RabinKarpStringMatching}(T,P,a,q)$
1. $rP = \textsf{RollingHash}(\mathtt{[]})$
2. $rT = \textsf{RollingHash}(\mathtt{[]})$
3. **for** $i$ **in** $\textsf{range}(0,len(P))$:
4. $\quad rP.\textsf{append}(P[i])$
5. $\quad rT.\textsf{append}(T[i])$
6. **for** $i$ **in** $\textsf{range}(len(P),len(T))$:
7. $\quad$ **if** $rP.\textsf{hash}()$ `==` $rT.\textsf{hash}()$: $\quad$ *// Here we need to double-check as collisions are possible*
8. $\quad\quad$ **if** $P$ `==` $T[i - len(P) + 1: i+1]$
9. $\quad\quad\quad$ **output** "Pattern found at offset", $i - len(P)+1$
10. $\quad rT.\textsf{skip}(T[i - len(P)])$
11. $\quad rT.\textsf{append}(T[i])$

**Worst-case time complexity:** Can we guarantee that, even in the worst case, false positives (equal hash values although the pattern has not been found) occur with probability at most $1/len(P)$?

**The Rabin–Karp algorithm for multiple strings P:** Problem: We have a text $T$ of length $n$. Now we have $k$ strings to search for, $\mathcal{P} = \lbrace P_0, P_1, \ldots, P_{k-1} \rbrace$; all of them have the same length $m$.

$\textsf{RabinKarpMultiString}(T, \mathcal{P}, m)$
1. $hashes$ `:=` $Set.\textsf{Empty}()$
2. **foreach** $P_i \in \mathcal{P}$:
3. $\quad rP_i = \textsf{RollingHash}(\mathtt{[]})$
4. $\quad$ **for** $j$ **in** $\textsf{range}(0,m)$:
5. $\quad\quad rP_i.\textsf{append}(P[j])$
6. $\quad hashes.\textsf{insert}(rP_i.\textsf{hash}())$
7. $rT = \textsf{RollingHash}(\mathtt{[]})$
8. **for** $j$ **in** $\textsf{range}(0,m)$:
9. $\quad rT.\textsf{append}(T[i])$
10. **for** $j$ **in** $\textsf{range}(1,n-m+1)$
11. $\quad$ **if** $rT.\textsf{hash}() \in hashes$ **and** $T[j:j+m-1] \in \mathcal{P}$
12. $\quad\quad$ **output** "Pattern found at offset", $j$
13. $\quad rT.\textsf{skip}(T[j])$
14. $\quad rT.\textsf{append}(T[j+m])$

This algorithm has time complexity $O(n + km)$. Naive string searching would have time complexity $O(nmk)$ if we checked the strings one by one.

### MinHash Algorithms

The [MinHash](https://en.wikipedia.org/wiki/MinHash) algorithm for estimating document similarity was introduced in 1997 by Andrei Broder while working on the AltaVista search engine.

**Definition:** *Shingling* a text document is a procedure that cuts pieces of a certain length out of the text (for example, all strings of $5$ characters, or all words, or all sequences of $5$ words). Other procedures that produce a collection of mutually overlapping strings also work.

Shingling moves a sliding window of fixed or variable size forward and turns the document into a set of shingles (n-grams). If we are interested in whole words (rather than word fragments of fixed length), *space normalization* can be applied to the document before extracting the shingles: it is converted to lowercase, all punctuation is removed, and whitespace of various kinds (tabs, ordinary spaces, line breaks, etc.) is replaced with single spaces.

To detect plagiarism or other copying of text one can use, for example, a sliding window of $5$ words. If two documents share many identical sequences of 5 consecutive words, this usually cannot be explained by coincidence -- the documents were copied from each other (or from a common source). The match alone does not prove plagiarism, since both documents may use the same quotation.

**Definition:** The *Jaccard coefficient* of two sets $A$ and $B$ is the ratio of their intersection to their union:

$$
J(A,B) = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}.
$$

Similar sets (or the shingle sets of similar documents) have $J(A,B)$ close to $1$.

*Note:* For MinHash algorithms it is important that the values of the hash functions are mutually independent and uniformly distributed. One can use Python's built-in hash function, but with different moduli. Rolling hash functions are not suitable.

This algorithm computes an estimate of the Jaccard coefficient $J(S_1, S_2)$, given a list $\mathcal{H}$ -- a collection of hash functions.

$\textsf{MinHash}(S_1, S_2, \mathcal{H})$
1. $\mathrm{sig}_1 = []$, $\mathrm{sig}_2 = []$ $\quad$ *// initialize the MinHash lists*
2. **for** $h_i$ **in** $\mathcal{H}$:
3. $\quad \mathrm{minHash}_1 = \infty$, $\mathrm{minHash}_2 = \infty$ $\quad$ *// start with infinity to compute the minimum*
4. $\quad$ **for** $s$ **in** $S_1$:
5. $\quad\quad \mathrm{hValue} = h_i(s)$ $\quad$ *// compute the hash function*
6. $\quad\quad$ **if** $\mathrm{hValue} < \mathrm{minHash}_1$:
7. $\quad\quad\quad \mathrm{minHash}_1 = \mathrm{hValue}$
8. $\quad$ **for** $s$ **in** $S_2$:
9. $\quad\quad \mathrm{hValue} = h_i(s)$ $\quad$ *// compute the hash function*
10. $\quad\quad$ **if** $\mathrm{hValue} < \mathrm{minHash}_2$:
11. $\quad\quad\quad \mathrm{minHash}_2 = \mathrm{hValue}$
12. $\quad \mathrm{sig}_1.append(\mathrm{minHash}_1)$, $\mathrm{sig}_2.append(\mathrm{minHash}_2)$ $\quad$ *// append to the MinHash lists*
13. $intersection = 0$
14. **for** $i = 0$ **to** $|\mathcal{H}| - 1$:
15. $\quad$ **if** $\mathrm{sig}_1[i] == \mathrm{sig}_2[i]$:
16. $\quad\quad \mathrm{intersection} = \mathrm{intersection} + 1$
17. **return** $\frac{\mathrm{intersection}}{|\mathcal{H}|}$ $\quad$ *// return the estimate of the Jaccard coefficient*

### Bloom Filters

Often strings must be searched for in a very large collection of documents. Optimal hash tables that resolve collisions with *linear probing* use load factors (the number of stored objects divided by the size of the hash table) of about $\ln 2 \approx 0.7$. For example, if the hash table is expected to store $1000$ elements, the array of an optimal hash table has about $1400$ cells.

When building a list of shingles for many gigabytes of documents, the hash table would also have many billions of cells. This is not practical if a plagiarism checker must compare submitted documents with a large set of existing documents. So an optimization called a *Bloom filter* is useful.

A *Bloom filter* is a data structure similar to an ordinary set; it supports these operations:

* Create an empty Bloom filter: `BF = EmptySet()`
* Add a new element to the set: `BF.add(item)`.
* Check whether an element belongs to the set: `BF.contains(item)` (returns a Boolean value true/false).

*Note:* Unlike ordinary sets (including sets stored in ordinary hash tables), Bloom filters usually do not support deleting elements. They are useful when we must decide membership in some large set, but the space for storing the set is limited.

It can be implemented with $k$ hash functions, each of which maps an object to one of $m$ bits randomly and independently of the other hash functions. The function `BF.add(item)` computes all $k$ hash functions and sets the corresponding bits.

The function `BF.contains(item)` likewise computes all $k$ hash functions and returns `true` if and only if ones are found in all $k$ positions. Two situations are possible:

* If `item` has indeed been added to the Bloom filter, it will always be found. Bloom filters cannot have *false negatives*.
* If `item` was never added to the Bloom filter, there is a probability that, because other elements were added, ones are set in all $k$ checked positions. Let us estimate this *false positive* probability.

Suppose we have inserted $n$ elements; the probability that a given bit is still $0$ is:

$$
p = \left(1-\frac{1}{m}\right)^{kn} \approx e^{-kn/m};
$$

To check whether an element belongs to the set, each of the $k$ array positions computed by the hash functions is $1$ with probability $(1-p)$. The probability that all of them are $1$, so that the Bloom filter wrongly reports that the element belongs to the set, is:

$$
\varepsilon = \left(1-\left[1-\frac{1}{m}\right]^{kn}\right)^k \approx
\left( 1-e^{-kn/m} \right)^k.
$$

Given the size $m$ of the bit array and the number $n$ of items to insert, we can find the optimal number $k$:

$$
k = \frac{m}{n} \ln 2
$$

If we know the maximum allowed false positive rate $\varepsilon$, we can adjust the value of $m$ accordingly to limit the probability of false positives.

**Applications of text fingerprints:** *Fingerprints* -- MinHash, Bloom filters, or similar hash values or sets of them -- make it possible to find matching pieces in documents. Plagiarism detection algorithms and also data leak prevention (*DLP*) help to detect whether a new document is similar to one of the existing ones. This useful property can be used in commercial products:

* **Turnitin** - a commercial service that checks how similar student essays are to the works it already stores. Subscription model, in operation since 1997. Is it ethical to profit from original works created by students?
* **Plag.lv** - something similar. See the article [Latvijā palaista programma](https://www.tvnet.lv/4838652/latvija-palaista-programma-kas-atklaj-plagiatu-akademiskos-darbos) (in Latvian).
* **Symantec DLP**, **Forcepoint DLP** - protect organizations from leaks of confidential documents (even if the content of the documents has been changed).

## Searching with an Automaton

If the text $T$ has not been preprocessed and only one pattern $P$ must be found in it, the most efficient approach is usually to process the pattern $P$, build data structures suitable for searching for it, and then read the text $T$. One kind of such data structure is a *finite automaton (acceptor)*, which changes its state after reading each next symbol of the text $T$. As soon as it has read the whole pattern in the input text, it enters an accepting state.

For searching regular expressions in general a finite automaton is very suitable, but for substring searching a few small tables are enough instead of a state diagram of the automaton. Below we look at the KMP or Knuth–Morris–Pratt algorithm and the BM or Boyer–Moore algorithm. At the end we also touch upon general regular expression searching in the input text.

There are several subcases of searching for patterns in a text:

1. If one pattern must be found in the text $T$ (**Ctrl-F** in a text editor), the text is usually read letter by letter as in a finite automaton (the KMP and BM algorithms).
2. If many patterns of equal length must be found in the text $T$ at once (intellectual property protection, plagiarism detection), a rolling hash is usually applied to the text, as in the previous section, so that the hash value can be compared with all the patterns (the Rabin–Karp algorithm).
3. If patterns of different lengths must be searched for in the text $T$ often (Internet search engines), the text is usually *indexed* -- a suffix tree, a suffix array or a similar data structure is built (Ukkonen's algorithm in the next lectures).

Suppose we use the naive search algorithm, the current value of the shift is $i$, and we have compared up to position $j$.

If it turns out that

$$
T[i] = P[0], \ldots, T[i + j - 1] = P[j - 1],
$$

but $T[i + j] \neq P[j]$, this is used to choose the next pair $(i^{\ast},j^{\ast})$. It is not necessary to choose $(i^{\ast},j^{\ast}) = (i+1,0)$ as in the naive algorithm.

**The main idea of the automaton:** Substring searching with a finite automaton: the states of the automaton are $q_0, q_1, \ldots, q_{m-1}$.

**Prefix property:** We are in the state $q_i$ if and only if "the last $i$ symbols of $T$ match the first $i$ symbols of $P$".

**Example:** The search automaton for the pattern $P = \mathtt{abab}$:

<img
  alt="Automaton for searching the pattern abab"
  src="{{ '/lectures/strings_search/figs/abab-automaton.png' | relative_url }}"
  style="width: 100%; max-width: 288px; border:none; background-color:#FFFFFF;"
/>

*Note.* After finding $P = \mathtt{abab}$ we move to $q_2$ (not to $q_0$), since occurrences of the pattern may overlap.

$$
\mathtt{...ababab...}
$$

**Automaton example:** Draw a finite automaton that searches for `aabab` as a substring of the input text.

**Solution:**

<img
  alt="Automaton for searching the pattern aabab"
  src="{{ '/lectures/strings_search/figs/aabab-automaton.png' | relative_url }}"
  style="width: 100%; max-width: 384px; border:none; background-color:#FFFFFF;"
/>

**Time for searching with an automaton:**

1. Time to read the text: Running a ready automaton takes $O(n)$ time: one operation for each letter of the text.
2. Time to preprocess the pattern: To build the automaton, the next state $q'$ must be determined for every combination of the current state $q$ and the current letter. There are $m$ states in total. Let $|\mathcal{A}|$ denote the number of letters in the alphabet $\mathcal{A}$. This gives a table with $m \cdot |\mathcal{A}|$ entries, which takes at least $O(m \cdot |\mathcal{A}|)$ operations.
3. The total time is $O(n + m \cdot |\mathcal{A}|)$.

*Note:* The preprocessing time is too large; in practice one tries to avoid it -- this is what the KMP algorithm is for. Even assuming $n \gg m$, $m \cdot |\mathcal{A}|$ can be large too.

## The Knuth–Morris–Pratt (KMP) Algorithm

**The main idea of the KMP algorithm:** We build a small table with the *prefix function* $\pi$. The function $\pi$ is built for the *pattern* being searched for. It captures how the pattern $P$ matches shifted copies of itself. This avoids unnecessary shifts in the naive search algorithm, and no separate state transition has to be built for each input symbol $s \in S$.

1. The input text is read only once: $O(n)$, rather than $O(n \cdot m)$ as in the naive algorithm.
2. The pattern $P$ is preprocessed in $O(m)$ time, rather than $O(m\cdot|S|)$ as for a fully built automaton.

A variant of the Knuth–Morris–Pratt algorithm, the Aho–Corasick string matching algorithm, is used in intrusion detection systems to scan packet payloads for many patterns simultaneously.

### The Prefix Function

The prefix function depends on the pattern $P=P[0]\ldots{}P[m-1]$.

**Definition:** For each $j = 1,\ldots,m$, find the largest $k$ ($k<j$) such that:

$$
\left\lbrace
  \begin{array}{l}
    P[0] = P[j - k]\\
    P[1] = P[j - k + 1]\\
    \ldots\\
    P[k - 1] = P[j - 1]
  \end{array}
\right.
$$

The value of the prefix function is $\pi[j]=k$. If there is no such $k$ ($k<j$), then $\pi[j]=0$.

**Another definition:** Let $P_k$ denote the prefix of the string $P$ of length $k$. Then $\pi(j)=k$ is the length of the longest suffix of the $j$-th prefix of $P$ ($P_j$) that is shorter than $j$ itself:

$$
\pi(j) = \max \left\lbrace k\,:\,k<j\;\text{and}\;P_k\;\text{is a suffix of the string}\;P_j \right\rbrace
$$

**Problem:** Find the prefix function of the pattern $P = \mathtt{abab}$.

**Solution:** The solution can be pictured as "maximal telescopic shifting":

<img
  alt="Prefix function of the pattern abab"
  src="{{ '/lectures/strings_search/figs/prefix-functions1.png' | relative_url }}"
  style="width: 100%; max-width: 288px; border:none; background-color:#FFFFFF;"
/>

| $j$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $0$ | $1$ | $2$ |

**Problem:** Find the prefix function of the pattern $P = \mathtt{aabaab}$.

**Solution:**

<img
  alt="Prefix function of the pattern aabaab"
  src="{{ '/lectures/strings_search/figs/prefix-functions2.png' | relative_url }}"
  style="width: 100%; max-width: 336px; border:none; background-color:#FFFFFF;"
/>

| $j$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $1$ | $0$ | $1$ | $2$ | $3$ |

**Pseudocode of the KMP algorithm:** *Input:* A text $T$ and a pattern $P$. *Output:* All shifts with which the pattern occurs in the text.

$\textsf{KMPmatcher}(T, P)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. $\pi = \textsf{Compute\_Prefix\_Function}(P)$
4. $k = 0$
5. **for** $i = 0$ **to** $n-1$ $\quad$ *// read T from left to right*
6. $\quad$ **while** $k > 0$ **and** $P[k] \neq T[i]$
7. $\quad\quad k = \pi(k)$ $\quad$ *// the hypothesis was wrong; move the pattern forward*
8. $\quad$ **if** $P[k] == T[i]$
9. $\quad\quad k = k + 1$ $\quad$ *// the hypothesis holds so far; compare further*
10. $\quad$ **if** $k == m$ $\quad$ *// has the whole pattern P been read?*
11. $\quad\quad$ print `"Pattern occurs with shift"` $i-m$
12. $\quad\quad k = \pi(k)$ $\quad$ *// the next place to move the pattern to*

**Why does KMP work correctly?** Suppose the current shift is $i \in \lbrace 0,\ldots,n-m\rbrace$: we hope that the pattern $P$ occurs in the text $T$ starting at position $i$.

But it turns out that the next symbol of $T$ ($T[i+j]$) does not match $P[j]$ (where $j \in \lbrace 0,\ldots,m-1\rbrace$). Then these equalities hold:

$$
\left\lbrace \begin{array}{lll}
T[i+j-k] & =P[j-k] & =P[0]\\
T[i+j-k+1] & =P[j-k+1] & =P[1]\\
\ldots & \ldots & \ldots\\
T[i+j-1] & =P[j-1] & =P[k-1]
\end{array} \right.
$$

The next position in the text $T$ where the substring $P$ can start is at the beginning of the last $k$ letters of the already read piece of $T$.

**Example:** We search for the pattern $P=\mathtt{ababaca}$ in the text $T = \mathtt{ababaababaca}$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{c}$ | $\mathtt{a}$ | $k=0$ |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | | | | | $k=1,2,3,4,5$ |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\textcolor{red}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | | | | | $k=\pi(5)=3$ |
| | | | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\textcolor{red}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | | | $k=\pi(3)=1$ |
| | | | | | $\mathtt{a}$ | $\textcolor{red}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | | $k=\pi(1)=0$ |
| | | | | | | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{c}$ | $\mathtt{a}$ | $k=1,2,3,4,5,6,7$ |

The prefix function of the pattern $P=\mathtt{ababaca}$:

| $j$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $0$ | $1$ | $2$ | $3$ | $0$ | $1$ |

**Running time of KMPmatcher:** Suppose $\pi(j)$ has already been computed. Note that in every comparison of the pattern $P$ and the text $T$ one of two things happens:

* if $P[k] = T[i]$, then $i$ increases, but $i-k$ does not change.
* if $P[k] \neq T[i]$, then $i-k$ increases, but $i$ does not change.

Since $i$ and $i-k$ are integers that start at $0$ and cannot exceed $n$, the algorithm makes at most $2n$ comparisons. So the running time of KMP is $O(n)$.

### Pseudocode of the Prefix Function

$\textsf{ComputePrefixFunction}(P)$
1. $m = P.\mathit{length}$
2. Allocate the table $\pi(1)\ldots{}\pi(m)$
3. $\pi(1)=0$
4. $k=0$
5. **for** $q=2$ **to** $m$
6. $\quad$ **while** $k>0$ **and** $P[k]\neq P[q-1]$
7. $\quad\quad k=\pi(k)$
8. $\quad$ **if** $P[k]==P[q-1]$
9. $\quad\quad k=k+1$
10. $\quad \pi(q)=k$
11. **return** $\pi$

**Example:** Find the prefix function of the pattern $P = \mathtt{ababaca}$.

<img
  alt="Prefix function of the pattern ababaca"
  src="{{ '/lectures/strings_search/figs/prefix-functions3.png' | relative_url }}"
  style="width: 100%; max-width: 384px; border:none; background-color:#FFFFFF;"
/>

| $j$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $\pi(j)$ | $0$ | $0$ | $1$ | $2$ | $3$ | $0$ | $1$ |
| | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{c}$ | $\mathtt{a}$ |
| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| $q=1$ | $\textcolor{blue}{0}$ | | | | | | |
| $q=2$ | 0 | $\textcolor{blue}{0}$ | | | | | |
| $q=3$ | 0 | 0 | $\textcolor{blue}{1}$ | | | | |
| $q=4$ | 0 | 0 | 1 | $\textcolor{blue}{2}$ | | | |
| $q=5$ | 0 | 0 | 1 | 2 | $\textcolor{blue}{3}$ | | |
| $q=6$ | 0 | 0 | 1 | 2 | 3 | $\textcolor{red}{3\downarrow}$ 1 | |
| $q=6$ | 0 | 0 | 1 | 2 | 3 | $\textcolor{red}{1\downarrow}$ 0 | |
| $q=6$ | 0 | 0 | 1 | 2 | 3 | $\textcolor{blue}{0}$ | |
| $q=7$ | 0 | 0 | 1 | 2 | 3 | 0 | $\textcolor{blue}{1}$ |

**Time complexity of the prefix function:** Computing the prefix function takes $O(m)$ time.

1. The outer loop runs $m-1$ times.
2. Each iteration of the inner loop decreases the value of $\pi[i+1]$.
3. Since this value increases only by $1$ in each iteration of the outer loop, it can reach at most $m$. Since it cannot be negative, it can decrease at most $m$ times, so in total the inner loop runs at most $m$ times.

## The Boyer–Moore Algorithm

**Main idea:** The Boyer–Moore algorithm starts comparing from the last symbol ($P[m-1]$ and $T[i+m-1]$). On a mismatch it may be possible to shift the compared string forward by more than $1$ symbol. For example, if $T[i+m-1]$ is a symbol that matches none of $P[0],\ldots,P[m-1]$, we can shift the string forward by $m$ symbols.

So the naive algorithm and KMP need at least $O(n)$ steps, while the Boyer–Moore algorithm sometimes needs only $O(n/m)$ steps. (In the worst cases, however, the Boyer–Moore algorithm is no better than KMP.)

### Boyer–Moore Pseudocode

$\textsf{BMmatcher}(T,P)$
1. $n = T.\mathit{length}$
2. $m = P.\mathit{length}$
3. $s = 0$
4. **while** $s \leq n-m$
5. $\quad j=m$
6. $\quad$ **while** $j>0$ **and** $P[j-1] = T[s+j-1]$:
7. $\quad\quad j=j-1$
8. $\quad$ **if** $j=0$ **then**
9. $\quad\quad$ print `"Pattern occurs with shift"` $s$
10. $\quad\quad s = s + \gamma[0]$
11. $\quad$ **else** $s = s + \max(\gamma[j], j-1-\lambda[T[s+j-1]])$

The shifts are determined by tables ($\gamma$ and $\lambda$); of the two shifts we choose the larger one. We will look at how these tables are built right away.

### The Bad Character Table

For the pattern $P$ the BM algorithm builds two shift arrays: the bad character table $\lambda$ and the good suffix table $\gamma$.

The bad character table is indexed by the symbols that can occur in $P$. For each symbol $x$ it stores the largest $i$ such that $P[i]=x$. If $x$ does not occur in the word, then $\lambda[x]=-1$. For example, if $P=\mathtt{abcab}$, the table looks like this:

| $x$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{c}$ | $\mathtt{*}$ |
| --- | --- | --- | --- | --- |
| $\lambda(x)$ | $3$ | $4$ | $2$ | $-1$ |

Here $\mathtt{*}$ denotes any symbol other than $\mathtt{a,b,c}$.

**Bad character pseudocode:**

$\textsf{BadCharacterTable}(P)$
1. **for** $a \in S$: $\quad$ *// for each symbol of the alphabet*
2. $\quad \lambda[a] = -1$
3. **for** $j=0$ **to** $m-1$:
4. $\quad \lambda[P[j]] = j$
5. **return** $\lambda$

### The Good Suffix Table

The good suffix table $\gamma[i]$ is indexed by numbers $i$ from $0$ to $m$. Its meaning is as follows: if $P[i]\ldots{}P[m-1]$ matches $T[k+i]\ldots{}T[k+m-1]$, but $P[i-1] \neq T[k+i-1]$, then $\gamma[i]$ is the smallest shift $j$ worth trying.

- If $i=m$, then $\gamma[i]=1$.
- If $i \leq m$, then $\gamma[i]$ equals the smallest $j>0$ that has one of these two properties:
  - $i \geq j$ and $P[i]\ldots{}P[m-1]$ matches $P[i-j]\ldots{}P[m-j-1]$;
  - $i \leq j$ and $P[j]\ldots{}P[m-1]$ matches $P[0]\ldots{}P[m-j-1]$. If no such $j$ exists, then $\gamma[i] = m$;

**Example:** For the pattern $P = \mathtt{abcab}$ the good suffix table looks like this:

| $j$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $\gamma[j]$ | $3$ | $3$ | $3$ | $3$ | $5$ | $1$ |

In terms of content, this means that if the last symbol did not match, the next option to try is $T[i+1]\ldots{}T[i+5]$, but if one of the earlier symbols did not match, we can move straight to $T[i+3]\ldots{}T[i+7]$.

(In this case this is guaranteed by the symbol $P[4]=T[i+4]=\mathtt{b}$, since $\mathtt{b}$ occurs in the word $P$ only as $P[4]$ and $P[1]$.)

**Good suffix table pseudocode:**

$\textsf{GoodSuffixTable}(P)$
1. $\pi = \textsf{ComputePrefixFunction}(P)$
2. $P' = \textsf{Reverse}(P)$
3. $\pi' = \textsf{ComputePrefixFunction}(P')$
4. **for** $j=0$ **to** $m$:
5. $\quad \gamma[j] = m - \pi[m]$
6. **for** $\ell=1$ **to** $m$:
7. $\quad j = m - \pi'[\ell]$
8. $\quad \gamma[j] = \min(\gamma[j], \ell - \pi'[\ell])$
9. **return** $\gamma$

In this algorithm $\textsf{ComputePrefixFunction}(P)$ is a function that takes a string $P$, computes the Knuth–Morris–Pratt prefix function $\pi[j]$ of this string and returns this array.

**BM algorithm example:**

| $\mathtt{a}$ | $\mathtt{d}$ | $\mathtt{a}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{c}$ | $\mathtt{a}$ | $\mathtt{b}$ | $\mathtt{a}$ | $\mathtt{a}$ | $\mathtt{b}$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{red}{\mathtt{c}}$ | $\mathtt{a}$ | $\mathtt{b}$ | | | | | | | | |
| | | | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{gray}{\mathtt{c}}$ | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{red}{\mathtt{b}}$ | | | | | |
| | | | | | $\textcolor{green}{\mathtt{a}}$ | $\textcolor{green}{\mathtt{b}}$ | $\textcolor{green}{\mathtt{c}}$ | $\textcolor{green}{\mathtt{a}}$ | $\textcolor{green}{\mathtt{b}}$ | | | |
| | | | | | | | | $\textcolor{gray}{\mathtt{a}}$ | $\textcolor{gray}{\mathtt{b}}$ | $\textcolor{red}{\mathtt{c}}$ | $\mathtt{a}$ | $\mathtt{b}$ |

Consider $T = \mathtt{daababcabaab}$ and $P = \mathtt{abcab}$. We search from right to left: each row shows one attempt to find the substring. **Red** marks the letter where the symbol of $P$ did not match the corresponding symbol of $T$.

1. In the first attempt $P[4]$ and $P[3]$ matched, but $P[2]$ did not. Then we move $3$ symbols forward (according to the "good suffix table").
2. We check whether $P[0]\ldots{}P[4]$ matches $T[3]\ldots{}T[7]$. The mismatch is already at $P[4]$, and then, according to the "bad character table", we move $2$ symbols forward so that the "c" found aligns with the first possible "c" in the substring $P$ (the first one from the end).
3. In the third attempt the whole substring matches. If all places in the text $T$ where the substring $P$ occurs must be found, we move $3$ symbols forward according to $\gamma[0]$ and try again.
4. The last attempt fails, and we have reached the end of the text.

**Could the bad character table alone be enough?** For practical substring searching, in the vast majority of cases the bad character table alone would be enough. One could write this pseudocode:

1. **if** $j=0$ **then**
2. $\quad$ print "Pattern occurs with shift" $s$
3. $\quad s = s+ \gamma[0]$
4. **else** $s = s + \max(\textcolor{red}{1}, j-1-\lambda[T[s+j-1]])$

Instead of the "good suffix rule" $\gamma[j]$ we insert the value $1$. If $T = \mathtt{BBBBBBBBBB...BBB}$ and the pattern is $P = \mathtt{ABBBB}$, the algorithm becomes the "naive" one.

**Good suffix table example:** Consider the pattern $P = \mathtt{CTTACTTAC}$. Let us justify that its good suffix table is:

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\gamma(j)$ | 4 | 4 | 4 | 4 | 4 | 8 | 8 | 8 | 8 | 1 |

## Problems

**Problem 13.1 (Rolling hash with a polynomial):** Suppose the alphabet has $a = 100$ symbols. Each symbol is written as a pair of digits: $\lbrace 00, 01, \ldots, 99 \rbrace$. Choose the rolling window size $m = 5$ and the prime $q = 23$.

The input is: `[03, 14, 15, 92, 65, 35, 89, 79, 31]`.

* Initialize an empty rolling hash `rH` and add the first five members of the sequence with the `append()` function:

  $$
  append(val) = ((u \cdot a) + val)\,\text{mod}\,q = ((u\,\text{mod}\,q) \cdot a + val)\,\text{mod}\,q.
  $$

* Show how the rolling hash can "roll" from the list `[03, 14, 15, 92, 65]` to `[14, 15, 92, 65, 35]` (first call `skip(03)`, then call `append(35)`).

**Problem 13.2 (Rolling hash with a cyclic polynomial):** Consider $16$ Latin letters with randomly assigned 4-bit codes (i.e. $L = 4$):

| Letter | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| h(x) | 1100 | 0100 | 0010 | 0110 | 0111 | 0000 | 1001 | 1111 | 0101 | 1101 | 1110 | 1011 | 0011 | 1010 | 1000 | 0001 |

Suppose the size of the rolling window is $k = 5$. Find the hash value of $ABIDE$ and then roll it to $BIDEN$. Recall that the rolling hash uses this formula:

$$
H = s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) )  \oplus \ldots \oplus  s( h(c_{k-1}) ) \oplus   h(c_k),
$$

**Problem 13.3 (Formulas for a rolling hash):** Write down the formulas for the cyclic polynomial rolling hash:

* The formula that assigns the initial value `RH` for an empty input.
* The formula that appends a new character $c_i$ to the current string.
* The formula that skips the first element $c_j$ of the current list, shortening the current string.

**Problem 13.4 (Average complexity of naive text searching):** Suppose the pattern $P$ and the text $T$ are random strings of lengths $m$ and $n$ over an alphabet of $a$ letters ($a \geq 2$). What is the expected number of letter comparisons in the naive algorithm if each comparison succeeds with probability $1/a$?

## References

An example of computations for the BM algorithm.

* [Good Suffix Heuristic](https://www.geeksforgeeks.org/boyer-moore-algorithm-good-suffix-heuristic/)
* [Visualizing String Matching](http://whocouldthat.be/visualizing-string-matching/)

<!--
Notes on sources (from strings02-kmp-and-bm/figs/README.txt):
1. [Lecture notes](../algorithms-bin/liet2008-13-v3.doc) - Useful pseudocode, but
the good suffix table example "abcab" uses the "weak" definition.
2. [General description of the BM algorithm](https://www.youtube.com/watch?v=4Xyhb72LCX4) - A "genetic" string searching example;
well explained, but it also uses the "weak" definition to compute the good suffix table.
3. [Bad character table](https://www.youtube.com/watch?v=G-h1Dph9IOE) - Defines the bad character table
in an unusual way (`$m - \lambda(j)$` in our notation) and computes it incorrectly.
4. [Drawing of good suffix tables](https://www.youtube.com/watch?v=lkL6RkQvpMM) - only
a graphical representation without letter examples.
-->
