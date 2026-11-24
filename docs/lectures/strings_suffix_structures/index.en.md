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

## One-Time and Repeated Searching

**The string searching problem:** We are given two strings (a text $T$ and a pattern $P$) over some alphabet $\Sigma$. We must find some or all shifts where $P$ matches $T$ (or count them). We also want to find occurrences of the pattern that overlap each other. (Variants -- searching for regular expressions or other patterns, approximate matching.)

**Optimal algorithms for one-time searching:**

* The Knuth–Morris–Pratt algorithm
* The Boyer–Moore algorithm
* The Rabin–Karp algorithm

All of them run in time linear in the length of the text. (They preprocess the *pattern* -- they compute the prefix function, the good suffix function, the bad character function or the hash of the pattern; see [13. String Searching]({{ '/lectures/strings_search/' | relative_url }}).)

**Repeated searching (a data structure problem):** The problem is the same, but reversed: the text document $T$ does not change, and all kinds of patterns $P$ must be searched for in it. So we preprocess the *text* $T$, and after that we answer queries with different patterns $P$.

* For one search we want to spend $O(|P|)$ time (the pattern has to be read once), rather than $O(|T|)$ time (running through the whole text again each time).
* We want $O(|T|)$ space, so that we do not need to store a data structure much larger than the text itself.

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

So the strings $T_i$ are represented as paths in a trie from the root to a leaf. The root gets children labeled with the letters of the alphabet (say, the $26$ letters of the alphabet). At the end of each string we add a new symbol (a dollar $\mathtt{\$}$) that does not belong to the alphabet.

**Example:** The trie for the strings $\lbrace \mathtt{ANA}, \mathtt{ANN}, \mathtt{ANNA}, \mathtt{ANNE} \rbrace$ is built over a 4-letter alphabet (we add the $\mathtt{\$}$ symbol to the letters $\mathtt{A}, \mathtt{E}, \mathtt{N}$). In the trie, the alphabetical predecessor and the alphabetical successor can be found in $O(|P|)$ steps: we go down to the place where $P$ "falls off" the trie, and there we find the maximal leaf in one subtree and the minimal leaf in the other subtree. The minimum and the maximum can be stored in each node.

### How to Represent Trie Nodes

If the alphabet $\Sigma$ is large, it matters how the children of one trie node are stored. Typical solutions are an array, a tree and a hash table. Here $T = T_1+\ldots +T_k$ (the total length of all texts):

| Node representation | Query time | Space |
| --- | --- | --- |
| Array (of length $\lvert\Sigma\rvert$) | $O(\lvert P\rvert)$ | $O(\lvert T\rvert \cdot \lvert\Sigma\rvert)$ |
| Binary search tree | $O(\lvert P\rvert \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |
| Hash table | $O(\lvert P\rvert)$ | $O(\lvert T\rvert)$ |
| Van Emde Boas tree (vEB tree) | $O(\lvert P\rvert \cdot \log \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |
| Trays | $O(\lvert P\rvert + \log \lvert\Sigma\rvert)$ | $O(\lvert T\rvert)$ |

A hash table is the best of both worlds (query $O(|P|)$ and space $O(|T|)$), but it does not solve the predecessor problem, because it mixes up the order of the letters.

Martin Farach-Colton used the LCA (lowest common ancestor) and a weight-balanced binary search tree (the weight of each node is the number of leaves below it). This achieves $O(|P| + \log_2 k)$ time, where $k$ is the number of texts.

### Compressed Tries

In a compressed trie, paths without branching are replaced with a single edge labeled with a whole string. The whole string does not need to be stored on the edge (when searching along an edge, one can "fall off the tree" in its middle). A compressed trie has $O(k)$ nodes (all nodes except the root and the leaves are nodes where branching happens), and all the same searches can still be done in it.

## Suffix Tries

**Definition:** The *suffix trie* of a text $T$ is a trie that contains all suffixes $T[i:]$ of $T$, each of them terminated with a special symbol -- a dollar $\mathtt{\$}$ that does not belong to the alphabet.

<img
  alt="Suffix trie of the word abaaba"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-trie.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Marking the end of a suffix:** Without the dollars at the ends of the suffixes, there would no longer be a 1:1 correspondence between the leaves of the tree and the suffixes, and some applications would become impossible (one could not tell whether a string is a suffix or an inner substring). This property is essential; $\mathtt{\$}$ will be used everywhere (sometimes they are marked by coloring the leaves of the tree).

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

**One complete example:** Building the suffix trie of the word $\mathtt{abaaba\$}$ by adding letters one by one.

<img
  alt="Building the suffix trie of the word abaaba$"
  src="{{ '/lectures/strings_suffix_structures/figs/building-tries-dollar-at-end.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

## Applications of Suffix Tries

**Substring check:** Check whether a string $Q$ is a substring of the text $T$. Start at the root of the trie and follow the letters of the pattern $Q$. If all of it can be read in the trie without "falling off", then $Q$ is a substring of $T$.

**Example:** Is $\mathtt{baa}$ a substring of $\mathtt{abaaba}$? We follow the letters of the pattern $\mathtt{baa}$. Once the suffix trie has been built, a query takes time equal to the length of the query itself, $O(|Q|)$, even if the text is very long.

<img
  alt="Searching for the substring baa in a suffix trie"
  src="{{ '/lectures/strings_suffix_structures/figs/abaaba-suffix-search-baa.png' | relative_url }}"
  style="width: 100%; max-width: 280px; border:none; background-color:#FFFFFF;"
/>

**Suffix check:** Check whether a string $Q$ is a suffix of the text $T$. Start at the root of the trie and follow the letters of the pattern $Q$. If all of it can be read in the trie and then a leaf can be reached along a $\mathtt{\$}$ edge, it is a suffix.

**Example:** Is $\mathtt{baa}$ a suffix of $\mathtt{abaaba}$? We search downward from the root (until we "fall off" the trie or reach the end of the pattern). If a $\mathtt{\$}$ edge leads from the node reached to a leaf, it was a suffix.

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
* There are still $|T|$ leaves, but every inner node branches.
* So the number of inner nodes does not exceed the number of leaves, and the total number of nodes is $O(|T|)$.
* Edge labels are not written out, but stored as pairs of indices into the text $T$, so the space used is $O(|T|)$.
* The efficient Ukkonen's algorithm builds a suffix tree in $O(|T|)$ time.

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
* How large is the structure? There are $|T|$ leaves; since all inner nodes are branching nodes, the total number of nodes is also $O(|T|)$. With trays, the search time is $O(|P| + \log_2 |\Sigma|)$.
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

**Example:** The words $\mathtt{at}$, $\mathtt{tag}$, $\mathtt{gat}$. Build the concatenation $\mathtt{at\#_1tag\#_2gat\#_3}$ and its suffix tree (left in the figure). For each leaf, drop the text after the first $\#$ symbol (right in the figure).

<img
  alt="Generalized suffix tree of the words at, tag, gat"
  src="{{ '/lectures/strings_suffix_structures/figs/generalized-suffix-trees.png' | relative_url }}"
  style="width: 100%; max-width: 700px; border:none; background-color:#FFFFFF;"
/>

**Longest common substring:** Find the longest common substring of the texts $S$ and $T$ (of lengths $n_1$ and $n_2$).

* Build the generalized suffix tree in $O(n_1 + n_2)$ time.
* Find the deepest node below which there are both leaves ending with $\#_1$ and leaves ending with $\#_2$.
* This is more efficient than the naive algorithm $O(n_1^2 \cdot n_2^2)$ and also than dynamic programming $O(n_1 \cdot n_2)$.

### Document Retrieval

How do we find all documents that contain a word? We can use a suffix tree as before and search quickly. But what happens if two documents match the pattern, and in one of them it occurs a billion times, but in the other only once?

**The document retrieval problem:** List all documents that contain the pattern $P$ in $O(|P| + k')$ time, where $k' \leq k$ is the number of documents that contain the pattern.

**Modification 1:** Several documents are stored in a suffix tree so that nothing is appended after any dollar sign $\mathtt{\$}_i$. Each dollar sign is a leaf node of the suffix tree.

**Modification 2:** Leaves labeled with the same dollar sign $\mathtt{\$}_i$ point to each other -- they form a linked list.

**Overview of the document retrieval algorithm:**

1. Find the pattern $P$ in the large suffix tree. It is some inner node. Suppose all leaves below it are numbered consecutively; their numbers lie in the interval $[\ell, n]$.
2. The goal is to find the first occurrence of $\mathtt{\$}_i$ for each $i$. We want to pay only for the number of different documents, but the interval $[\ell, n]$ may contain very many $\mathtt{\$}_i$ leaves.
3. The solution is to store in each leaf the number of the previous leaf of the same document (as in "Modification 2").

## Suffix Arrays

The leaves of a suffix tree, listed in alphabetical order of the suffixes, form a *suffix array*.

**Definition:** A *suffix array* is the list of the start indices of all suffixes of the text $T$, sorted in alphabetical order of the suffixes. The suffixes themselves need not be written out (that would take $O(|T|^2)$ space) -- it is enough to write the indices.

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

## Problems

A tool for searching patterns in a dictionary: [Pattern Match](https://www.litscape.com/word_tools/pattern_match.php).

**Problem 14.1 (Longest common substrings):** The longest common substring of the texts $T_1$ and $T_2$ is the longest string contained in both texts. Dynamic programming gives an $O(n_1 \cdot n_2)$ time algorithm, where $|T_1| = n_1$ and $|T_2| = n_2$. (See an [example of building the table](https://bit.ly/3rcGUev).)

<img
  alt="Dynamic programming table for the longest common substring"
  src="{{ '/lectures/strings_suffix_structures/figs/longest-common-substring-matrix.png' | relative_url }}"
  style="width: 100%; max-width: 480px; border:none; background-color:#FFFFFF;"
/>

*Dynamic programming table for the strings $\mathtt{ABCXYZAY}$ and $\mathtt{XYZABCB}$: each cell contains the length of the longest common suffix of the two prefixes. The largest value $4$ corresponds to the longest common substring $\mathtt{XYZA}$.*

Consider the strings $T_1 = \mathtt{banana\$}_1$ and $T_2 = \mathtt{guanabana\$}_2$. They are written over this alphabet:

$$
\Sigma = \lbrace \mathtt{\$}_1, \mathtt{\$}_2, \mathtt{a}, \mathtt{b}, \mathtt{g}, \mathtt{n}, \mathtt{u} \rbrace.
$$

An algorithm with time $O(n_1+n_2)$ can find the longest common substring.

* **(A)** Draw the suffix tree of the text $\mathtt{banana\$}_1$.
* **(B)** Add to the existing tree the suffixes of the text $\mathtt{guanabana\$}_2$ as well. (One can also build the suffix tree of the text $\mathtt{banana\$}_1\mathtt{guanabana\$}_2$ at once.)
* **(C)** Find visually the longest common substring of $\mathtt{banana}$ and $\mathtt{guanabana}$. Mark the corresponding nodes in the suffix tree. What is the property of the root of the subtree?
* **(D)** Find an $O(n_1+n_2)$ algorithm to determine the longest common substring of texts of lengths $n_1$ and $n_2$ respectively.

*Note:* Draw the suffix trees in compressed form.

**Problem 14.2 (Building a suffix array):** Consider the text $\mathtt{acabcabaabaabca\$}$. It is written over a 4-letter alphabet with this order: $\Sigma = \lbrace \mathtt{\$}, \mathtt{a}, \mathtt{b}, \mathtt{c} \rbrace$.

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

## References

* [MIT 6.851 Advanced Data Structures: Session 16 -- Strings](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-851-advanced-data-structures-spring-2012/lecture-videos/session-16-strings/)
* [Suffix tries (video)](https://youtu.be/hLsrPsFHPcQ)
* [CMU: Suffix Trees (slides)](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixtrees.pdf)
* [Suffix Arrays (Yale, J. Aspnes)](https://www.cs.yale.edu/homes/aspnes/pinewiki/SuffixArrays.html) -- on suffix arrays and the Burrows–Wheeler transform.
* [Suffix arrays: additional explanations (arXiv:1311.1762)](https://arxiv.org/pdf/1311.1762.pdf)
* [MIT 6.854J Advanced Algorithms (1999)](https://dspace.mit.edu/bitstream/handle/1721.1/36897/6-854JFall-1999/OcwWeb/Electrical-Engineering-and-Computer-Science/6-854JAdvanced-AlgorithmsFall1999/CourseHome/index.htm)
