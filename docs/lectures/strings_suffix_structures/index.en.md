---
layout: default
title: "Suffix Trees and Suffix Arrays"
lang: en
permalink: /lectures/strings_suffix_structures/en/
---
# 14. Suffix Trees and Suffix Arrays

In this chapter we look at data structures that make it possible to quickly search for many different patterns in one and the same text:

1. What "tries" (letter trees) are. Compressed tries.
2. Suffix tries, suffix trees and suffix arrays.
3. Document retrieval.
4. Building suffix trees in linear time.
5. The FM-index: searching in the Burrows–Wheeler transform.
6. LZ77 compression with a suffix array.

## One-Time and Repeated Searching

**The string searching problem:** We are given two strings (a text $T$ and a pattern $P$) over some alphabet $\Sigma$. We must find some or all shifts where $P$ matches $T$ (or count them). We also want to find occurrences of the pattern that overlap each other. (Variants -- searching for regular expressions or other patterns, approximate matching.)

**Optimal algorithms for one-time searching:**

* The Knuth–Morris–Pratt algorithm
* The Boyer–Moore algorithm
* The Rabin–Karp algorithm

All of them run in time linear in the length of the text. (They preprocess the *pattern* -- they compute the prefix function, the good suffix function, the bad character function or the hash of the pattern; see [13. String Searching]({{ '/lectures/strings_search/' | relative_url }}).)

**Repeated searching (a data structure problem):** The problem is the same, but reversed: the text document $T$ does not change, and all kinds of patterns $P$ must be searched for in it. So we preprocess the *text* $T$, and after that we answer queries with different patterns $P$.

* For one search we want to spend $O(\lvert P\rvert )$ time (the pattern has to be read once), rather than $O(\lvert T\rvert )$ time (running through the whole text again each time).
* We want $O(\lvert T\rvert )$ space, so that we do not need to store a data structure much larger than the text itself.

## Tries

* A *trie* is a tree that does not store whole keys (as a binary search tree does), but splits a key into smaller parts, using its structure. It is a rooted tree whose edges are labeled with letters of the alphabet $\Sigma$.
* For strings, a trie processes the string being searched for letter by letter.
* Suffix tries make it possible to answer several interesting queries.
* To keep tries from taking too much space, they are sometimes compressed, which gives *suffix trees*.

### The Predecessor Problem

**Problem:** The [predecessor problem](https://en.wikipedia.org/wiki/Predecessor_problem): We are given pieces of text $T_1<T_2 <\ldots <T_k$ (sorted alphabetically) and also a pattern $P$. Find the predecessor and the successor:

* $\text{predecessor}(P)$ - the largest index $i$ such that $T_i \leq P$.
* $\text{successor}(P)$ - the smallest index $j$ such that $T_j \geq P$.

The predecessor problem is useful in practice: we type in some prefix of a string and want to see the book title that comes immediately before or after it in an alphabetical catalog.

Do binary search trees solve it? The strings can be sorted, or a binary search tree can be built, but this is inefficient, since comparing two strings can take a long time.

So the strings $T_i$ are represented as paths in a trie from the root to a leaf. The root gets children labeled with the letters of the alphabet (say, the $26$ letters of the alphabet). At the end of each string we add a new symbol (a dollar $\mathtt{\\$}$) that does not belong to the alphabet.

**Example:** The trie for the strings $\lbrace \mathtt{ANA}, \mathtt{ANN}, \mathtt{ANNA}, \mathtt{ANNE} \rbrace$ is built over a 4-letter alphabet (we add the $\mathtt{\\$}$ symbol to the letters $\mathtt{A}, \mathtt{E}, \mathtt{N}$). In the trie, the alphabetical predecessor and the alphabetical successor can be found in $O(vert P
vert )$ steps: we go down to the place where $P$ "falls off" the trie, and there we find the maximal leaf in one subtree and the minimal leaf in the other subtree. The minimum and the maximum can be stored in each node.

### How to Represent Trie Nodes

If the alphabet $\Sigma$ is large, it matters how the children of one trie node are stored. Typical solutions are an array, a tree and a hash table. Here $T = T_1+\ldots +T_k$ (the total length of all texts):

| Node representation | Query time | Space |
| --- | --- | --- |
| Array (of length $\lvert\Sigma\rvert$) | $O(\lvert P\rvert)$ | $O(\lvert T\rvert \cdot \lvert\Sigma\rvert)$ |
| Binary search tree | $O(\lvert P\rvert \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |
| Hash table | $O(\lvert P\rvert)$ | $O(\lvert T\rvert)$ |
| Van Emde Boas tree (vEB tree) | $O(\lvert P\rvert \cdot \log \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |
| Trays | $O(\lvert P\rvert + \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |

A hash table is the best of both worlds (query $O(\lvert P\rvert )$ and space $O(\lvert T\rvert )$), but it does not solve the predecessor problem, because it mixes up the order of the letters.

Martin Farach-Colton used the LCA (lowest common ancestor) and a weight-balanced binary search tree (the weight of each node is the number of leaves below it). This achieves $O(\lvert P\rvert  + \log_2 k)$ time, where $k$ is the number of texts.

### Compressed Tries

In a compressed trie, paths without branching are replaced with a single edge labeled with a whole string. The whole string does not need to be stored on the edge (when searching along an edge, one can "fall off the tree" in its middle). A compressed trie has $O(k)$ nodes (all nodes except the root and the leaves are nodes where branching happens), and all the same searches can still be done in it.

## Suffix Tries

**Definition:** The *suffix trie* of a text $T$ is a trie that contains all suffixes $T[i:]$ of $T$, each of them terminated with a special symbol -- a dollar $\mathtt{\\$}$ that does not belong to the alphabet.

<img
  alt="Suffix trie of the word abaaba"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Marking the end of a suffix:** Without the dollars at the ends of the suffixes, there would no longer be a 1:1 correspondence between the leaves of the tree and the suffixes, and some applications would become impossible (one could not tell whether a string is a suffix or an inner substring). This property is essential; $\mathtt{\\$}$ will be used everywhere (sometimes they are marked by coloring the leaves of the tree).

<img
  alt="Suffix trie of the word abaaba without dollars"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-no-dollars.png' | relative_url }}"
  style="width: 100%; max-width: 180px; border:none; background-color:#FFFFFF;"
/>

### Suffix Links

* Each leaf is a suffix.
* Each node is a prefix of some suffix.
* The *suffix link* of a node points to the prefix of the suffix whose first letter has been deleted.

**Example:** Both $\mathtt{aab}$ and $\mathtt{ab}$ are prefixes of suffixes of the word $\mathtt{abaaba}$. The suffix link of the node $\mathtt{aab}$ points to $\mathtt{ab}$ (the red arrow in the figure).

<img
  alt="A suffix link in the suffix trie of the word abaaba"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-suffix-links.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

### Building Tries Recursively

A suffix trie can be built by adding the letters of the text one by one: $\textsf{SufTrie}(\mathtt{abbac})$ is obtained from $\textsf{SufTrie}(\mathtt{abba})$ by appending the new letter to all existing suffixes (starting with the longest one). The end nodes of all suffixes can be visited by following the suffix links.

<img
  alt="Building suffix tries recursively: SufTrie(abba) and SufTrie(abbac)"
  src="{{ '/lectures/strings_suffix_structures/figs/building-tries.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**Moving the boundary forward:** The path along the suffix links from the end of the longest suffix (*longest*) is called the *boundary path*. When the letter $s[i]$ is added, we walk along the boundary path, add a new child with the letter $s[i]$ to each node and connect the new nodes with suffix links. We can stop when we reach a node (*current*) that already has a child with the letter $s[i]$.

<img
  alt="Moving the boundary path forward"
  src="{{ '/lectures/strings_suffix_structures/figs/boundary-path.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**One complete example:** Building the suffix trie of the word $\mathtt{abaaba\\$}$ by adding letters one by one.

<img
  alt="Building the suffix trie of the word abaaba$"
  src="{{ '/lectures/strings_suffix_structures/figs/building-tries-dollar-at-end.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

## Applications of Suffix Tries

**Substring check:** Check whether a string $Q$ is a substring of the text $T$. Start at the root of the trie and follow the letters of the pattern $Q$. If all of it can be read in the trie without "falling off", then $Q$ is a substring of $T$.

**Example:** Is $\mathtt{baa}$ a substring of $\mathtt{abaaba}$? We follow the letters of the pattern $\mathtt{baa}$. Once the suffix trie has been built, a query takes time equal to the length of the query itself, $O(\lvert Q\rvert )$, even if the text is very long.

<img
  alt="Searching for the substring baa in a suffix trie"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-search-baa.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Suffix check:** Check whether a string $Q$ is a suffix of the text $T$. Start at the root of the trie and follow the letters of the pattern $Q$. If all of it can be read in the trie and then a leaf can be reached along a $\mathtt{\\$}$ edge, it is a suffix.

**Example:** Is $\mathtt{baa}$ a suffix of $\mathtt{abaaba}$? We search downward from the root (until we "fall off" the trie or reach the end of the pattern). If a $\mathtt{\\$}$ edge leads from the node reached to a leaf, it was a suffix.

<img
  alt="Suffix check in a suffix trie"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-suffix.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Counting occurrences:** Count how many times the pattern $Q$ occurs in the text $T$. Follow the path of the pattern $Q$ from the root. The number of occurrences equals the number of leaves below the vertex reached.

**Example:** Count how many times $\mathtt{aba}$ occurs in the text $\mathtt{abaaba}$. Either we "fall off" the trie -- then the answer is $0$, or we find a vertex $n$ below which the leaves can be counted (here $2$).

<img
  alt="Counting occurrences of the pattern aba in a suffix trie"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie-count.png' | relative_url }}"
  style="width: 100%; max-width: 300px; border:none; background-color:#FFFFFF;"
/>

**Longest repeat:** Find the longest pattern $P$ that occurs in the text $T$ more than once. We must find the deepest vertex that has at least $2$ leaves below it.

**First suffix:** Find the lexicographically (alphabetically) smallest suffix. Start at the root and each time follow the edge labeled with the lexicographically smallest letter.

## Suffix Trees

**The worst case for a trie:**

* If the string is $S = \mathtt{a}^n\mathtt{b}^n$, it has $n(n+1) + n+1$, i.e. $O(n^2)$, distinct substrings (including the empty one), and the suffix trie has just as many nodes.
* In general, a string of length $n$ has at most $O(n^2)$ substrings, but all of them can occur.
* For texts found in practice the size of the trie also grows quadratically (usually a bit slower than in the worst case), but the memory used is huge.

<img
  alt="Suffix trie of the word aaabbb"
  src="{{ '/lectures/strings_suffix_structures/figs/large-suffix-tree.png' | relative_url }}"
  style="width: 100%; max-width: 300px; border:none; background-color:#FFFFFF;"
/>

**Suffix trees:** These are compressed suffix tries.

* Paths without choices are compressed.
* There are still $\lvert T\rvert $ leaves, but every inner node branches.
* So the number of inner nodes does not exceed the number of leaves, and the total number of nodes is $O(\lvert T\rvert )$.
* Edge labels are not written out, but stored as pairs of indices into the text $T$, so the space used is $O(\lvert T\rvert )$.
* The efficient Ukkonen's algorithm builds a suffix tree in $O(\lvert T\rvert )$ time.

<img
  alt="Suffix tree of the word abaaba$"
  src="{{ '/lectures/strings_suffix_structures/figs/suffix-tree.png' | relative_url }}"
  style="width: 100%; max-width: 350px; border:none; background-color:#FFFFFF;"
/>

**Example:** Consider a text $T$ and all its suffixes $T[i:]$. We add the dollar sign once -- at the end of $T$. Then it will appear in all suffixes:

```text
banana$
0123456
```

The empty string need not be stored (only the dollar sign). The leaves contain the start indices of the suffixes; the dashed arrows are suffix links.

<img
  alt="Suffix tree of the word banana$"
  src="{{ '/lectures/strings_suffix_structures/figs/suffix-tree-banana.png' | relative_url }}"
  style="width: 100%; max-width: 288px; border:none; background-color:#FFFFFF;"
/>

In this tree one can search for $\mathtt{nan}$, $\mathtt{an}$ or even $\mathtt{ana}$ (two overlapping occurrences). This data structure searches in time linear in the length of the pattern.

### Applications of Suffix Trees

* Searching for a pattern $P$ gives a subtree whose leaves correspond to all occurrences of $P$ in the text $T$. They can be counted, one can follow the linked list of leaves, or find the first $10$ occurrences. From the root of the subtree one can "teleport" to its leaves.
* How large is the structure? There are $\lvert T\rvert $ leaves; since all inner nodes are branching nodes, the total number of nodes is also $O(\lvert T\rvert )$. With trays, the search time is $O(\lvert P\rvert  + \log_2 \lvert \Sigma\rvert )$.
* Find the first $k$ occurrences of a pattern.
* Count how many times $P$ occurs in the text $T$.
* If $T$ is a very long document (for example, the Merriam-Webster dictionary), find the longest substring that occurs in it at least twice. (Find the node with the largest "letter depth" that has at least two leaves below it.)
* Given two suffixes (positions $i$ and $j$ in the text), find how long a prefix they share. This can be determined in constant time -- find the lowest common ancestor (LCA) of the two leaves; its letter depth is the longest common prefix:

  $$
  \mathrm{lcp}(\mathtt{T[i:]}, \mathtt{T[j:]}) = \text{letter depth}\left(\mathrm{LCA}(i, j)\right).
  $$

* Finding all occurrences of $T[i:j]$ in almost constant time. A LA (*level ancestor*) query is used: first go to the leaf $i$, then jump up to the ancestor with letter depth $j-i$. For this one can use *jump pointers* or *ladder decomposition*. If the queries are known in advance, they can be processed in advance by adding them to the text.

**Definition:** The *lowest common ancestor* (LCA) of two tree nodes (inner nodes or leaves) is the deepest node that is an ancestor of both -- the place where their paths from the root branch apart.

### Generalized Suffix Trees

Several documents are represented by joining them into one text and adding a separate dollar sign after each of them:

$$
T = T_1\mathtt{\$}_1T_2\mathtt{\$}_2\cdots{}T_k\mathtt{\$}_k.
$$

Different dollars are used so that each suffix ends with a unique symbol and the leaf tells which document it belongs to.

**Example:** The words $\mathtt{at}$, $\mathtt{tag}$, $\mathtt{gat}$. Build the concatenation $\mathtt{at\\#_1tag\\#_2gat\\#_3}$ and its suffix tree (left in the figure). For each leaf, drop the text after the first $\\#$ symbol (right in the figure).

<img
  alt="Generalized suffix tree of the words at, tag, gat"
  src="{{ '/lectures/strings_suffix_structures/figs/generalized-suffix-trees.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**Longest common substring:** Find the longest common substring of the texts $S$ and $T$ (of lengths $n_1$ and $n_2$).

* Build the generalized suffix tree in $O(n_1 + n_2)$ time.
* Find the deepest node below which there are both leaves ending with $\\#_1$ and leaves ending with $\\#_2$.
* This is more efficient than the naive algorithm $O(n_1^2 \cdot n_2^2)$ and also than dynamic programming $O(n_1 \cdot n_2)$.

### Document Retrieval

How do we find all documents that contain a word? We can use a suffix tree as before and search quickly. But what happens if two documents match the pattern, and in one of them it occurs a billion times, but in the other only once?

**The document retrieval problem:** List all documents that contain the pattern $P$ in $O(\lvert P\rvert  + k')$ time, where $k' \leq k$ is the number of documents that contain the pattern.

**Modification 1:** Several documents are stored in a suffix tree so that nothing is appended after any dollar sign $\mathtt{\\$}_i$. Each dollar sign is a leaf node of the suffix tree.

**Modification 2:** Leaves labeled with the same dollar sign $\mathtt{\\$}_i$ point to each other -- they form a linked list.

**Overview of the document retrieval algorithm:**

1. Find the pattern $P$ in the large suffix tree. It is some inner node. Suppose all leaves below it are numbered consecutively; their numbers lie in the interval $[\ell, n]$.
2. The goal is to find the first occurrence of $\mathtt{\\$}_i$ for each $i$. We want to pay only for the number of different documents, but the interval $[\ell, n]$ may contain very many $\mathtt{\\$}_i$ leaves.
3. The solution is to store in each leaf the number of the previous leaf of the same document (as in "Modification 2").

## Suffix Arrays

The leaves of a suffix tree, listed in alphabetical order of the suffixes, form a *suffix array*.

**Definition:** A *suffix array* is the list of the start indices of all suffixes of the text $T$, sorted in alphabetical order of the suffixes. The suffixes themselves need not be written out (that would take $O(\lvert T\rvert ^2)$ space) -- it is enough to write the indices.

**Example:** For the text `banana$` the suffix array is $[6, 5, 3, 1, 0, 4, 2]$:

```text
6: $
5: a$
3: ana$
1: anana$
0: banana$
4: na$
2: nana$
```

LCP information can also be added to a suffix array: the LCP (*longest common prefix*) of two suffixes adjacent in alphabetical order:

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

**Claim:** Given a suffix array and its LCP information, a suffix tree can be built from them in linear time. This is done with a **Cartesian tree** of the LCP array; it also makes it possible to find the lowest common ancestor (LCA) and answer LCP queries for any two suffixes.

Suffix arrays are closely related to the Burrows–Wheeler transform (see [4. Burrows–Wheeler Transform]({{ '/lectures/lossless_burrows_wheeler/' | relative_url }})).

### The FM-Index

A suffix array for a text of length $n$ takes $n$ integers, i.e. $4n$ or $8n$ bytes -- many times more than the text itself. The human genome has about $3 \cdot 10^9$ letters $\mathtt{A}, \mathtt{C}, \mathtt{G}, \mathtt{T}$, and its suffix array does not fit into the memory of an ordinary computer. Paolo Ferragina and Giovanni Manzini (2000) discovered that for pattern searching the Burrows–Wheeler transform and a few small tables are enough. This data structure is called the *FM-index*.

**BWT from the suffix array:** The sorted cyclic permutations (in Lecture 4) correspond to the sorted suffixes, since $\mathtt{\\$}$ is the smallest symbol. So the last column of the BWT consists of the letters that stand immediately *before* each suffix:

$$
L[r] = T[SA[r] - 1] \quad (\text{if } SA[r] = 0, \text{ then } L[r] = \mathtt{\$}).
$$

For the text $\mathtt{banana\\$}$:

| $r$ | $SA[r]$ | Suffix (the $F$ column is its first letter) | $L[r]$ |
| --- | --- | --- | --- |
| $0$ | $6$ | $\mathtt{\\$}$ | $\mathtt{a}$ |
| $1$ | $5$ | $\mathtt{a\\$}$ | $\mathtt{n}$ |
| $2$ | $3$ | $\mathtt{ana\\$}$ | $\mathtt{n}$ |
| $3$ | $1$ | $\mathtt{anana\\$}$ | $\mathtt{b}$ |
| $4$ | $0$ | $\mathtt{banana\\$}$ | $\mathtt{\\$}$ |
| $5$ | $4$ | $\mathtt{na\\$}$ | $\mathtt{a}$ |
| $6$ | $2$ | $\mathtt{nana\\$}$ | $\mathtt{a}$ |

So $L = \mathtt{annb\\$aa}$ (the same as BWT($\mathtt{BANANA\\$}$) = $\mathtt{ANNB\\$AA}$ in Lecture 4).

**Two auxiliary tables:**

* $C[c]$ -- the number of letters in the text that are alphabetically smaller than $c$. The rows whose suffixes start with the letter $c$ occupy the interval of the suffix array from $C[c]$ (inclusive) to $C[c] + (\text{frequency of } c)$ (exclusive). In the example $C[\mathtt{\\$}] = 0$, $C[\mathtt{a}] = 1$, $C[\mathtt{b}] = 4$, $C[\mathtt{n}] = 5$.
* $\textit{Occ}(c, i)$ -- the number of occurrences of the letter $c$ in the prefix $L[0]\ldots{}L[i-1]$ of the string $L$ (in its first $i$ letters).

These tables express the LF mapping of Lecture 4: $\textit{LF}(r) = C[L[r]] + \textit{Occ}(L[r], r)$. It relies on the same fact as the inverse BWT: equal letters in the column $L$ and in the column $F$ are ordered in the same way.

**Backward search:** All suffixes that start with the pattern $P$ occupy one contiguous interval $[sp, ep)$ of the suffix array. This interval is found by reading the pattern *from the end*: if we know the interval of the suffixes that start with $P[j+1]\ldots{}P[m-1]$, then the rows in it whose $L$ letter is $c = P[j]$ are mapped by the LF mapping exactly to the suffixes that start with $cP[j+1]\ldots{}P[m-1]$. Moreover, they are mapped to a contiguous interval that is determined by its endpoints alone.

$\textsf{BackwardSearch}(P)$
1. $sp = 0$; $\;ep = n$ $\quad$ *// initially -- all rows*
2. **for** $j = m-1$ **downto** $0$:
3. $\quad c = P[j]$
4. $\quad sp = C[c] + \textit{Occ}(c, sp)$
5. $\quad ep = C[c] + \textit{Occ}(c, ep)$
6. $\quad$ **if** $sp \geq ep$: **return** "not found"
7. **return** $[sp, ep)$ $\quad$ *// the number of occurrences is $ep - sp$*

**Example:** We search for $P = \mathtt{ana}$ in the text $\mathtt{banana\\$}$ ($L = \mathtt{annb\\$aa}$).

| Step | Letter $c$ | $sp = C[c] + \textit{Occ}(c, sp)$ | $ep = C[c] + \textit{Occ}(c, ep)$ | Suffixes in the interval |
| --- | --- | --- | --- | --- |
| start | | $0$ | $7$ | all |
| $j = 2$ | $\mathtt{a}$ | $1 + 0 = 1$ | $1 + 3 = 4$ | $\mathtt{a\\$}, \mathtt{ana\\$}, \mathtt{anana\\$}$ |
| $j = 1$ | $\mathtt{n}$ | $5 + 0 = 5$ | $5 + 2 = 7$ | $\mathtt{na\\$}, \mathtt{nana\\$}$ |
| $j = 0$ | $\mathtt{a}$ | $1 + 1 = 2$ | $1 + 3 = 4$ | $\mathtt{ana\\$}, \mathtt{anana\\$}$ |

The pattern $\mathtt{ana}$ occurs $ep - sp = 2$ times; the positions are $SA[2] = 3$ and $SA[3] = 1$.

**Time and space:**

* Counting the occurrences takes $m$ steps, each with two $\textit{Occ}$ queries. If the $\textit{Occ}$ values are stored only at every $b$-th position (at checkpoints) and the rest is counted from $L$, a query takes $O(b)$ time; with bit operations it can be done in constant time.
* To find the *positions* of the occurrences, only every $s$-th element of the suffix array is stored; a missing $SA[r]$ is found by walking back with LF steps until a stored element is reached ($\leq s$ steps).
* The string $L$ itself compresses well (see Lecture 4 -- move-to-front and entropy codes), so the FM-index can take *less* space than the original text and still allows searching for any pattern. Such data structures are called *compressed indexes*.

The FM-index is used by the DNA read aligners Bowtie and BWA: millions of short DNA fragments must be found in the human genome, and the index of the whole genome fits into a few gigabytes of memory.

### LZ77 with a Suffix Array

At each cursor position $i$ the LZ77 encoder (see [3. Lempel–Ziv Algorithms]({{ '/lectures/lossless_lempel_ziv/' | relative_url }})) solves a string searching problem: find the longest string that starts at position $i$ and has already occurred earlier in the text (starts at some position $j < i$; the match may overlap the part being encoded). Practical encoders do this with hash tables and a limited window. A suffix array solves this problem for *all* positions together in linear time and without a window limit.

**Definition:** The *longest previous factor* array (LPF) is

$$
\textit{LPF}[i] = \max \left\lbrace \mathrm{lcp}(T[i:], T[j:]) \,:\, 0 \leq j < i \right\rbrace,
$$

where $\mathrm{lcp}$ is the length of the longest common prefix of two suffixes (if $i = 0$, then $\textit{LPF}[0] = 0$).

**Main idea:** In a suffix array the $\mathrm{lcp}$ of two suffixes is the minimum of the LCP values between their rows. So moving away from the row of the suffix $T[i:]$ in the suffix array, the $\mathrm{lcp}$ can only decrease. Of all earlier suffixes ($j < i$), the longest common prefix is attained by one of the two *nearest* ones -- the nearest one above in the suffix array and the nearest one below:

* $\textit{PSV}(i)$ (*previous smaller value*) -- the nearest row above the row of the suffix $T[i:]$ with $SA[r] < i$;
* $\textit{NSV}(i)$ (*next smaller value*) -- the nearest row below the row of the suffix $T[i:]$ with $SA[r] < i$.

Then $\textit{LPF}[i] = \max\left(\mathrm{lcp}(T[i:], T[SA[\textit{PSV}(i)]:]),\; \mathrm{lcp}(T[i:], T[SA[\textit{NSV}(i)]:])\right)$, and the source position is the one of the two that gives the larger value. All $\textit{PSV}$ and $\textit{NSV}$ values can be found in one pass over the suffix array with a stack (similarly to building a Cartesian tree), and the $\textit{LPF}$ array can also be computed in $O(n)$ time (Maxime Crochemore, Lucian Ilie, 2008).

**LZ77 encoding with LPF:** The encoder outputs the same triples $(d, \ell, x)$ as in Lecture 3:

$\textsf{LZ77-SA}(T)$ $\quad$ *// $T[0:n-1]$ ends with $\mathtt{\\$}$*
1. Build $SA$, $LCP$ and $\textit{LPF}$ (together with the source positions $\textit{src}[i]$)
2. $i = 0$
3. **while** $i < n-1$:
4. $\quad \ell = \min(\textit{LPF}[i],\; n-2-i)$ $\quad$ *// leave at least one letter $x$*
5. $\quad$ **if** $\ell = 0$: output $(0, 0, T[i])$
6. $\quad$ **else** output $(i - \textit{src}[i], \ell, T[i+\ell])$
7. $\quad i = i + \ell + 1$

**Example:** $T = \mathtt{abcabcabd\\$}$ ($n = 10$). The suffix array is $[9, 0, 3, 6, 1, 4, 7, 2, 5, 8]$.

| $i$ | Suffix | $\textit{PSV}$ source | $\textit{NSV}$ source | $\textit{LPF}[i]$ | $\textit{src}[i]$ |
| --- | --- | --- | --- | --- | --- |
| $0$ | $\mathtt{abcabcabd\\$}$ | -- | -- | $0$ | -- |
| $1$ | $\mathtt{bcabcabd\\$}$ | $0$ | -- | $0$ | -- |
| $2$ | $\mathtt{cabcabd\\$}$ | $1$ | -- | $0$ | -- |
| $3$ | $\mathtt{abcabd\\$}$ | $0$ | $1$ | $5$ | $0$ |
| $4$ | $\mathtt{bcabd\\$}$ | $1$ | $2$ | $4$ | $1$ |
| $5$ | $\mathtt{cabd\\$}$ | $2$ | -- | $3$ | $2$ |

(The "source" columns contain the position $SA[r]$ in the corresponding row $r$; the table shows only the positions needed for encoding.) For example, immediately above the suffix $T[3:] = \mathtt{abcabd\\$}$ in the suffix array is $T[0:] = \mathtt{abcabcabd\\$}$ ($0 < 3$, LCP $= 5$), so $\textit{LPF}[3] = 5$.

The encoder outputs $(0,0,\mathtt{a})$, $(0,0,\mathtt{b})$, $(0,0,\mathtt{c})$, and then at position $i = 3$ -- $(3, 5, \mathtt{d})$: $5$ letters $\mathtt{abcab}$ are copied from $3$ positions back (the match overlaps the part being encoded), and $\mathtt{d}$ is appended.

**Where it is used:** Practical compressors (gzip, zstd) limit the window and search with hash tables or binary trees, since this is faster and needs less memory. Suffix arrays are used when an *optimal* factorization or a very long window is needed, for example, when compressing large collections of similar texts (the genomes of many people, the version history of documents). The number $z$ of LZ77 phrases is a measure of how repetitive a text is, and it is also the basis of compressed indexes (the LZ-index, the r-index) that, like the FM-index, allow searching directly in compressed text.

## Problems

A tool for searching patterns in a dictionary: [Pattern Match](https://www.litscape.com/word_tools/pattern_match.php).

**Problem 14.1 (Longest common substrings):** The longest common substring of the texts $T_1$ and $T_2$ is the longest string contained in both texts. Dynamic programming gives an $O(n_1 \cdot n_2)$ time algorithm, where $\lvert T_1\rvert  = n_1$ and $\lvert T_2\rvert  = n_2$. (See an [example of building the table](https://bit.ly/3rcGUev).)

<img
  alt="Dynamic programming table for the longest common substring"
  src="{{ '/lectures/strings_suffix_structures/figs/longest-common-substring-matrix.png' | relative_url }}"
  style="width: 100%; max-width: 480px; border:none; background-color:#FFFFFF;"
/>

*Dynamic programming table for the strings $\mathtt{ABCXYZAY}$ and $\mathtt{XYZABCB}$: each cell contains the length of the longest common suffix of the two prefixes. The largest value $4$ corresponds to the longest common substring $\mathtt{XYZA}$.*

Consider the strings $T_1 = \mathtt{banana\\$}_1$ and $T_2 = \mathtt{guanabana\\$}_2$. They are written over this alphabet:

$$
\Sigma = \lbrace \mathtt{\$}_1, \mathtt{\$}_2, \mathtt{a}, \mathtt{b}, \mathtt{g}, \mathtt{n}, \mathtt{u} \rbrace.
$$

An algorithm with time $O(n_1+n_2)$ can find the longest common substring.

* **(A)** Draw the suffix tree of the text $\mathtt{banana\\$}_1$.
* **(B)** Add to the existing tree the suffixes of the text $\mathtt{guanabana\\$}_2$ as well. (One can also build the suffix tree of the text $\mathtt{banana\\$}_1\mathtt{guanabana\\$}_2$ at once.)
* **(C)** Find visually the longest common substring of $\mathtt{banana}$ and $\mathtt{guanabana}$. Mark the corresponding nodes in the suffix tree. What is the property of the root of the subtree?
* **(D)** Find an $O(n_1+n_2)$ algorithm to determine the longest common substring of texts of lengths $n_1$ and $n_2$ respectively.

*Note:* Draw the suffix trees in compressed form.

**Problem 14.2 (Building a suffix array):** Consider the text $\mathtt{acabcabaabaabca\\$}$. It is written over a 4-letter alphabet with this order: $\Sigma = \lbrace \mathtt{\\$}, \mathtt{a}, \mathtt{b}, \mathtt{c} \rbrace$.

* **(A)** Build the suffix array of this text.
* **(B)** Add LCP (longest common prefix) information to the suffix array -- find the longest common prefixes of any two alphabetically adjacent suffixes.
* **(C)** Use the suffix array and its LCP information to build the (compressed) suffix tree of this word.

**Solution:**

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
  alt="Suffix tree, suffix array and LCP information for the text acabcabaabaabca$"
  src="{{ '/lectures/strings_suffix_structures/figs/long-suffix-tree.png' | relative_url }}"
  style="width: 100%; max-width: 720px; border:none; background-color:#FFFFFF;"
/>

**Problem 14.3 (Searching with the FM-index):** Consider the text $T = \mathtt{abaaba\\$}$ over the alphabet $\Sigma = \lbrace \mathtt{\\$}, \mathtt{a}, \mathtt{b} \rbrace$.

* **(A)** Find the suffix array and the BWT string $L$ (use $L[r] = T[SA[r]-1]$).
* **(B)** Find the table $C[c]$.
* **(C)** Use backward search to determine how many times $\mathtt{aba}$ occurs in the text, and at which positions.
* **(D)** Use backward search to verify that $\mathtt{bb}$ does not occur in the text.

**Solution:**

* **(A)** The sorted suffixes: $\mathtt{\\$}$ (6), $\mathtt{a\\$}$ (5), $\mathtt{aaba\\$}$ (2), $\mathtt{aba\\$}$ (3), $\mathtt{abaaba\\$}$ (0), $\mathtt{ba\\$}$ (4), $\mathtt{baaba\\$}$ (1). So $SA = [6, 5, 2, 3, 0, 4, 1]$ and $L = \mathtt{abba\\$aa}$.
* **(B)** The text has one $\mathtt{\\$}$, four $\mathtt{a}$ and two $\mathtt{b}$, so $C[\mathtt{\\$}] = 0$, $C[\mathtt{a}] = 1$, $C[\mathtt{b}] = 5$.
* **(C)** Start $[0, 7)$. Letter $\mathtt{a}$: $sp = 1 + \textit{Occ}(\mathtt{a}, 0) = 1$, $ep = 1 + \textit{Occ}(\mathtt{a}, 7) = 1 + 4 = 5$. Letter $\mathtt{b}$: $sp = 5 + \textit{Occ}(\mathtt{b}, 1) = 5$, $ep = 5 + \textit{Occ}(\mathtt{b}, 5) = 5 + 2 = 7$. Letter $\mathtt{a}$: $sp = 1 + \textit{Occ}(\mathtt{a}, 5) = 1 + 2 = 3$, $ep = 1 + \textit{Occ}(\mathtt{a}, 7) = 5$. The interval is $[3, 5)$: $\mathtt{aba}$ occurs $2$ times, at the positions $SA[3] = 3$ and $SA[4] = 0$.
* **(D)** Letter $\mathtt{b}$: $[5, 7)$ (as before). The next letter $\mathtt{b}$: $sp = 5 + \textit{Occ}(\mathtt{b}, 5) = 7$, $ep = 5 + \textit{Occ}(\mathtt{b}, 7) = 7$. Since $sp \geq ep$, the pattern does not occur. (In the rows $5$ and $6$, whose suffixes start with $\mathtt{b}$, the $L$ letters are $\mathtt{a}$ -- no $\mathtt{b}$ is preceded by a $\mathtt{b}$.)

**Problem 14.4 (LZ77 with the longest previous factor):** Consider the text $T = \mathtt{abababb\\$}$ ($n = 8$).

* **(A)** Find the suffix array and the LCP values of adjacent suffixes.
* **(B)** Use $\textit{PSV}$ and $\textit{NSV}$ to find $\textit{LPF}[2]$ and its source position.
* **(C)** Find the LZ77 triples $(d, \ell, x)$ output by $\textsf{LZ77-SA}$.

**Solution:**

* **(A)** The sorted suffixes and the LCP with the previous one:

  | $r$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $7$ |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | $SA[r]$ | $7$ | $0$ | $2$ | $4$ | $6$ | $1$ | $3$ | $5$ |
  | Suffix | $\mathtt{\\$}$ | $\mathtt{abababb\\$}$ | $\mathtt{ababb\\$}$ | $\mathtt{abb\\$}$ | $\mathtt{b\\$}$ | $\mathtt{bababb\\$}$ | $\mathtt{babb\\$}$ | $\mathtt{bb\\$}$ |
  | $LCP[r]$ | -- | $0$ | $4$ | $2$ | $0$ | $1$ | $3$ | $1$ |

* **(B)** The suffix $T[2:] = \mathtt{ababb\\$}$ is in row $2$. The nearest row above it with $SA[r] < 2$ is row $1$ ($SA[1] = 0$), $\mathrm{lcp} = LCP[2] = 4$. The nearest row below it with $SA[r] < 2$ is row $5$ ($SA[5] = 1$), $\mathrm{lcp} = \min(LCP[3], LCP[4], LCP[5]) = 0$. So $\textit{LPF}[2] = 4$ with source $0$.
* **(C)** At positions $0$ and $1$ the letters $\mathtt{a}$ and $\mathtt{b}$ occur for the first time: $(0, 0, \mathtt{a})$, $(0, 0, \mathtt{b})$. At position $2$: $\ell = \min(4, n-2-2) = 4$, $d = 2 - 0 = 2$, $x = T[6] = \mathtt{b}$, so $(2, 4, \mathtt{b})$. Then $i = 7 = n-1$, and the encoding ends. Decoding: $\mathtt{a}$, $\mathtt{b}$, then $4$ letters are copied from $2$ positions back (one by one: $\mathtt{a}, \mathtt{b}, \mathtt{a}, \mathtt{b}$) and $\mathtt{b}$ is appended -- this gives $\mathtt{abababb}$.

## References

* [MIT 6.851 Advanced Data Structures: Session 16 -- Strings](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-851-advanced-data-structures-spring-2012/lecture-videos/session-16-strings/)
* [Suffix tries (video)](https://youtu.be/hLsrPsFHPcQ)
* [CMU: Suffix Trees (slides)](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixtrees.pdf)
* [Suffix Arrays (Yale, J. Aspnes)](https://www.cs.yale.edu/homes/aspnes/pinewiki/SuffixArrays.html) -- on suffix arrays and the Burrows–Wheeler transform.
* [Suffix arrays: additional explanations (arXiv:1311.1762)](https://arxiv.org/pdf/1311.1762.pdf)
* P. Ferragina, G. Manzini. [Opportunistic data structures with applications](https://doi.org/10.1109/SFCS.2000.892127). *FOCS 2000* -- the original paper of the FM-index.
* M. Crochemore, L. Ilie. [Computing Longest Previous Factor in linear time and applications](https://doi.org/10.1016/j.ipl.2007.10.006). *Information Processing Letters* 106(2), 2008.
* [MIT 6.854J Advanced Algorithms (1999)](https://dspace.mit.edu/bitstream/handle/1721.1/36897/6-854JFall-1999/OcwWeb/Electrical-Engineering-and-Computer-Science/6-854JAdvanced-AlgorithmsFall1999/CourseHome/index.htm)
