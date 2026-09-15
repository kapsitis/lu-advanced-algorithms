---
layout: default
title: "Lossless Compression: Problem Set"
lang: en
permalink: /lectures/lossless_final_problemsets/
---
# Lossless Compression: Final Problem Set

The problems cover the chapters on entropy and Huffman coding, arithmetic coding and ANS, Lempel–Ziv algorithms, and 
the Burrows–Wheeler transform. All calculations can be done on paper; the notation for the algorithms is the same as in the corresponding chapters.

**Useful values:** $\log_2 3 \approx 1.585$, $\;\log_2 5 \approx 2.322$.

## Entropy and Huffman Coding

**Problem 1 (Counterfeit coin):** Among $4$ identical-looking coins, one is counterfeit: it is either lighter or heavier than the others. All $8$ cases (which coin is counterfeit and whether it is lighter or heavier) are equally likely. We have a balance scale without weights; each weighing has three outcomes: the left pan is heavier, the right pan is heavier, or the pans balance. The same number of coins is placed on both pans.

* **(a)** What is the entropy of the random variable that determines which coin is counterfeit and whether it is lighter or heavier?
* **(b)** Find the probability distribution and the entropy of the outcome of the first weighing if you compare (1) one coin against one coin; (2) two coins against two coins. Which weighing gives more information?
* **(c)** What is the largest possible entropy of the outcome of a single weighing? Use entropy to justify that the problem cannot be solved with one weighing.
* **(d)** The entropy estimate does not rule out two weighings, since $2 \log_2 3 \approx 3.17 > 3$. Prove that two weighings are nevertheless not enough (consider how many cases can remain after the first weighing), and find a strategy with three weighings.

**Problem 2 (How many bits Huffman coding loses):** A message alphabet has $5$ messages with probabilities $p = (0.4,\; 0.2,\; 0.2,\; 0.1,\; 0.1)$.

* **(a)** Compute the entropy $H(S)$. *Hint:* $\log_2 2.5 = \log_2 5 - 1$.
* **(b)** For each message we choose the codeword length $\ell_i = \left\lceil \log_2 \frac{1}{p_i} \right\rceil$. Check that these lengths satisfy the Kraft–McMillan inequality, and write down a prefix code with these lengths. What is its average length? Why is this code certainly not optimal?
* **(c)** Prove in general: if $\ell_i = \left\lceil \log_2 \frac{1}{p_i} \right\rceil$, then $\sum_i 2^{-\ell_i} \leq 1$ and $\sum_i p_i \ell_i < H(S) + 1$.
* **(d)** Build a Huffman code and find its average length. Explain why part (c) together with the optimality of Huffman codes implies that a Huffman code always spends fewer than $H(S) + 1$ bits per message. Is the Huffman tree unique for this distribution?
* **(e)** For an alphabet with two messages whose probabilities are $0.99$ and $0.01$, the entropy is approximately $0.08$ bits. How many bits per message does a Huffman code spend? How can this loss be reduced?

## Arithmetic Coding and ANS

**Problem 3 (Arithmetic coding):** The alphabet has letters `A`, `B`, `C` with probabilities $p(\mathtt{A}) = 0.5$, $p(\mathtt{B}) = 0.3$, $p(\mathtt{C}) = 0.2$; the intervals are ordered in this order.

* **(a)** Find the sequence of intervals $[l_i;\, l_i + s_i)$ that corresponds to the message `ACBA`.
* **(b)** Find the shortest binary fraction $\beta = 0.b_1 b_2 \ldots b_n$ such that the whole interval $[\beta;\, \beta + 2^{-n})$ lies inside the interval found in part (a). Compare $n$ with $\log_2 \frac{1}{s_4}$.
* **(c)** How many bits would a Huffman code spend on this message? Why is arithmetic coding not better for a short message, but better for a long one?
* **(d)** The transmitted number is $0.101_2$. Decode the first four letters of the message.

**Problem 4 (ANS):** In the word `ANANAS` the letter `A` occurs $3$ times, `N` occurs $2$ times, and `S` occurs $1$ time. We use these counts as rANS frequencies: $f(\mathtt{A}) = 3$, $f(\mathtt{N}) = 2$, $f(\mathtt{S}) = 1$, so $M = 6$, $c(\mathtt{A}) = 0$, $c(\mathtt{N}) = 3$, $c(\mathtt{S}) = 5$.

* **(a)** Which symbols own the numbers $0, 1, \ldots, 17$?
* **(b)** Encode the message `ANANAS` with $\textsf{Rans-Encode}$, starting with $x = 0$. Write down the state after every step.
* **(c)** Decode the number obtained in part (b) with $\textsf{Rans-Decode}$ and verify that the state returns to zero.
* **(d)** Decode four symbols from the state $x = 131$.
* **(e)** Compare $\log_2 x$ from part (b) with the information content of the message $-\log_2 \left( p(\mathtt{A})^3 \, p(\mathtt{N})^2 \, p(\mathtt{S}) \right)$.
* **(f)** Show that the messages `NA` and `NAA` are encoded as the same number. Why does this happen, and why does the message `ANANAS` not have this problem?

## Lempel–Ziv Algorithms

**Problem 5 (LZ77):**

* **(a)** Encode the string `kakadukakadu` with $\textsf{LZ77-Encode}$, if the window length is $W = 6$ and the look-ahead buffer is unlimited. For each triple, give the cursor position and the contents of the window.
* **(b)** Repeat the same with $W = 4$. Why are there more triples?
* **(c)** Decode the sequence of triples $(0,0,\mathtt{l}), (0,0,\mathtt{a}), (2,5,\mathtt{i}), (4,3,\mathtt{a})$ with $\textsf{LZ77-Decode}$. In which step does the source region overlap with the letters just decoded?

**Problem 6 (LZ78):**

* **(a)** Encode the string `abababababa` with $\textsf{LZ78-Encode}$ (alphabet $S = \lbrace \mathtt{a}, \mathtt{b} \rbrace$). Write down which phrases are added to the dictionary and with which numbers.
* **(b)** Decode the code sequence obtained in part (a) with $\textsf{LZ78-Decode}$. In which step does the decoder receive a number that is not yet in its dictionary?
* **(c)** Decode the code sequence `l,a,1,3,2,5` (alphabet $S = \lbrace \mathtt{a}, \mathtt{l} \rbrace$).
* **(d)** A string consists of $n$ letters `a` (alphabet $S = \lbrace \mathtt{a} \rbrace$). How many codes does $\textsf{LZ78-Encode}$ output? Find the exact answer when $n = 1 + 2 + \ldots + r$, and an approximate answer as a function of $n$.

## Burrows–Wheeler Transform

**Problem 7 (BWT):**

* **(a)** Write down all cyclic rotations of the word `KAKAO$`, sort them alphabetically (`$` comes before all letters), and find BWT(`KAKAO$`). In which row of the sorted matrix is the original word?
* **(b)** Encode the string obtained in part (a) with *Move-to-front*, if the initial order of the alphabet is `$`, `A`, `K`, `O` (positions are numbered from $0$).
* **(c)** It is known that the Burrows–Wheeler transform of some word $w$ ending with `$` is `ASSAL$`. Reconstruct $w$.

**Problem 8 (BWT with a suffix array):**

* **(a)** Write down all suffixes of the word `BARBARA$`, sort them alphabetically, and write down the suffix array $A$ (each suffix is denoted by the number of letters deleted from the beginning of the word).
* **(b)** Find BWT(`BARBARA$`) with $\textsf{efficientBWT}$: for each $i$ output the letter $w[A[i]-1]$, where $w[-1]$ means the last letter. Check a few letters of the result using the cyclic rotations.
* **(c)** Explain why the order of the suffixes coincides with the order of the cyclic rotations if the word ends with a unique, alphabetically smallest symbol `$`.
* **(d)** How can you use the suffix array and binary search to find all occurrences of the substring `BAR` in the word? Why are the corresponding entries in the suffix array adjacent?
* **(e)** Compare the time complexity of the naive BWT implementation and of the suffix array method.

## Markov Chains

**Problem 9 (Markov chain and compression):** A simplified "language" has letters `A`, `B`, `C`. Text is generated by a Markov chain: after `A`, `A` follows with probability $1/2$ and `B` follows with probability $1/2$; after `B`, `C` always follows; after `C`, `A` always follows. The text starts with `A`.

* **(a)** Draw the graph of the chain and write down the transition matrix. What is the probability that the text starts with `ABCAABCA`?
* **(b)** Find the stationary distribution $\pi = (\pi_A, \pi_B, \pi_C)$, i.e., the distribution that does not change after one step of the chain.
* **(c)** Is the chain ergodic? Is it periodic? What would change if the transition $\mathtt{A} \to \mathtt{A}$ were removed, i.e., if `B` always followed `A`?
* **(d)** Compute the single-letter entropy $H(X_1)$ in the stationary distribution and the entropy rate $H(X) = \sum_i \pi_i \cdot H(\text{transitions from state } i)$. How many bits per letter would a Huffman code that encodes each letter separately spend?
* **(e)** Show that after the initial letter `A` the text can be split into pieces `A` and `BCA`, and that by encoding each piece with one bit we achieve on average $H(X)$ bits per letter. Which of the algorithms in this course finds such repeated pieces automatically, without knowing the probabilities of the chain?
