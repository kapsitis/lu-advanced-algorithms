---
layout: default
title: "Lossless Compression: Problem Set Solutions"
lang: en
permalink: /lectures/lossless_final_problemsets/solutions.html

docx_header: "Lossless Compression. Sample Problems -- Solutions"
docx_footer: "Fall 2026 Seminar: Algorithms in Telecommunications and Security"
docx_font: "Calibri"
docx_fontsize: 10
docx_heading_font: "Calibri Light"
docx_heading_color: "2F5496"
docx_heading1_size: 14
geometry: "a4paper, top=2.54cm, bottom=2.54cm, left=2.54cm, right=2.54cm"
---
# Lossless Compression: Solutions of the Sample Problems

Solutions of the problems in [Lossless Compression: Sample Problems]({{ '/lectures/lossless_final_problemsets/' | relative_url }}).
Every algorithm is run step by step with the same notation as in the corresponding chapter:
$\textsf{Huffman}$, the intervals $[l_i;\,l_i+s_i)$ of arithmetic coding, $\textsf{Rans-Encode}$ /
$\textsf{Rans-Decode}$, $\textsf{LZ77-Encode}$ / $\textsf{LZ77-Decode}$, $\textsf{LZ78-Encode}$ /
$\textsf{LZ78-Decode}$, $\textsf{MoveToFrontEncode}$ and $\textsf{efficientBWT}$.

**Useful values:** $\log_2 3 \approx 1.585$, $\;\log_2 5 \approx 2.322$, $\;\log_2 11 \approx 3.459$.

## Entropy and Huffman Coding

### Problem 1 (Counterfeit coin)

Number the coins $1,2,3,4$. The $8$ equally likely cases are written as $1^-, 1^+, 2^-, 2^+, \ldots$,
where $c^-$ means "coin $c$ is lighter" and $c^+$ means "coin $c$ is heavier".

**(a)** All $8$ cases have probability $1/8$, so every case has information content
$h = \log_2 8 = 3$ bits and

$$
H(S) = -\sum_{i=1}^{8} \frac{1}{8}\log_2 \frac{1}{8} = \log_2 8 = 3 \text{ bits}.
$$

**(b)** The weighing is a random variable with three outcomes: $\text{L}$ (the left pan is heavier),
$\text{Eq}$ (balance), $\text{R}$ (the right pan is heavier).

*(1) One against one,* say $1$ vs. $2$. Coins $3,4$ are not on the scale, so all $4$ cases about them
give $\text{Eq}$:

| Outcome | Cases | $p$ |
| --- | --- | --- |
| $\text{L}$ | $1^+, 2^-$ | $2/8 = 1/4$ |
| $\text{Eq}$ | $3^-, 3^+, 4^-, 4^+$ | $4/8 = 1/2$ |
| $\text{R}$ | $1^-, 2^+$ | $2/8 = 1/4$ |

$$
H = \tfrac14 \cdot 2 + \tfrac12 \cdot 1 + \tfrac14 \cdot 2 = 1.5 \text{ bits}.
$$

*(2) Two against two,* $\lbrace 1,2 \rbrace$ vs. $\lbrace 3,4 \rbrace$. Every coin is on the scale, so
balance is impossible:

| Outcome | Cases | $p$ |
| --- | --- | --- |
| $\text{L}$ | $1^+, 2^+, 3^-, 4^-$ | $4/8 = 1/2$ |
| $\text{Eq}$ | none | $0$ |
| $\text{R}$ | $1^-, 2^-, 3^+, 4^+$ | $4/8 = 1/2$ |

$$
H = \tfrac12 \cdot 1 + \tfrac12 \cdot 1 = 1 \text{ bit}.
$$

The weighing $1$ vs. $1$ gives more information ($1.5 > 1$ bits). Just as in Problem 1.7 of the
Huffman chapter: when something has to be *found out*, the entropy of the answer should be made as
large as possible.

**(c)** A weighing has $3$ outcomes, so its entropy is at most $\log_2 3 \approx 1.585$ bits, with
equality only when $p(\text{L}) = p(\text{Eq}) = p(\text{R}) = 1/3$. With $4$ coins even this bound is
not reached: $8/3$ is not an integer, so the outcomes cannot be made equally likely, and the best
achievable value is the $1.5$ bits of part (b).

One weighing therefore carries at most $1.585 < 3$ bits, while the answer requires $3$ bits. A single
weighing cannot identify the case. (The same by counting: $3 < 8$.)

**(d)** *Two weighings are not enough.* Counting alone does not forbid it, because
$2\log_2 3 \approx 3.17 > 3$ and $3^2 = 9 \geq 8$. But look at the first weighing -- by part (b) only
two weighings are possible:

* $1$ vs. $1$: the branches leave $2$, $4$, $2$ cases;
* $2$ vs. $2$: the branches leave $4$, $0$, $4$ cases.

In both cases some branch leaves $4$ cases, and the second weighing has only $3$ outcomes. By the
pigeonhole principle two of those $4$ cases end up with the same outcome and cannot be told apart.
(In entropy terms: the conditional entropy of the remaining $4$ cases is $2$ bits, and one weighing
gives at most $\log_2 3 \approx 1.585 < 2$ bits.)

*A strategy with three weighings.*

**Weighing 1:** $1$ vs. $2$.

* **$1$ heavier than $2$** (cases $1^+, 2^-$). **Weighing 2:** $1$ vs. $3$ (coin $3$ is known to be
  genuine). If $1$ is heavier -- the answer is $1^+$; if they balance -- the answer is $2^-$.
  (Two weighings suffice in this branch.)
* **$2$ heavier than $1$** (cases $1^-, 2^+$). Symmetric.
* **Balance** (cases $3^-, 3^+, 4^-, 4^+$). **Weighing 2:** $3$ vs. $4$; they cannot balance.
  * If $3$ is heavier, the case is $3^+$ or $4^-$. **Weighing 3:** $1$ vs. $3$. If $3$ is heavier --
    $3^+$; if they balance -- $4^-$.
  * If $4$ is heavier, the case is $4^+$ or $3^-$, and **weighing 3** ($1$ vs. $4$) decides it in the
    same way. $\square$

### Problem 2 (How many bits Huffman coding loses)

$p = (0.4,\; 0.2,\; 0.2,\; 0.1,\; 0.1)$; call the messages $x_1, \ldots, x_5$.

**(a)** The information contents $h(x_i) = \log_2 \frac{1}{p_i}$:

| $x_i$ | $p_i$ | $h(x_i) = \log_2 (1/p_i)$ | $p_i h(x_i)$ |
| --- | --- | --- | --- |
| $x_1$ | $0.4$ | $\log_2 2.5 = \log_2 5 - 1 \approx 1.322$ | $0.5288$ |
| $x_2$ | $0.2$ | $\log_2 5 \approx 2.322$ | $0.4644$ |
| $x_3$ | $0.2$ | $\log_2 5 \approx 2.322$ | $0.4644$ |
| $x_4$ | $0.1$ | $\log_2 10 = 1 + \log_2 5 \approx 3.322$ | $0.3322$ |
| $x_5$ | $0.1$ | $\log_2 10 \approx 3.322$ | $0.3322$ |

$$
H(S) = 0.5288 + 0.4644 + 0.4644 + 0.3322 + 0.3322 \approx 2.122 \text{ bits}.
$$

**(b)** Rounding the information contents up:

$$
\ell = \left( \lceil 1.322 \rceil, \lceil 2.322 \rceil, \lceil 2.322 \rceil,
\lceil 3.322 \rceil, \lceil 3.322 \rceil \right) = (2,\,3,\,3,\,4,\,4).
$$

Kraft--McMillan inequality:

$$
\sum_i 2^{-\ell_i} = \frac14 + \frac18 + \frac18 + \frac{1}{16} + \frac{1}{16} = \frac{5}{8} = 0.625 \leq 1 .
$$

Since the sum is at most $1$, the converse direction of the Kraft--McMillan theorem gives a prefix
tree with exactly these leaf depths. Assigning the codes canonically (shortest first, then in order):

$$
C' = \lbrace (x_1,\mathtt{00}),\; (x_2,\mathtt{010}),\; (x_3,\mathtt{011}),\;
(x_4,\mathtt{1000}),\; (x_5,\mathtt{1001}) \rbrace .
$$

$$
\ell_a(C') = 0.4 \cdot 2 + 0.2 \cdot 3 + 0.2 \cdot 3 + 0.1 \cdot 4 + 0.1 \cdot 4 = 2.8 \text{ bits}.
$$

The code is certainly not optimal, because the Kraft sum is **strictly** smaller than $1$: the prefix
tree has unused space. Concretely, the whole subtree $\mathtt{11}$ is empty, so $x_4$ and $x_5$ can be
shortened to $\mathtt{100}$ and $\mathtt{101}$ without breaking the prefix property -- and that already
gives $2.6$ bits.

**(c)** *The Kraft sum.* Since $\ell_i = \lceil \log_2 (1/p_i) \rceil \geq \log_2 (1/p_i)$, we get
$2^{-\ell_i} \leq 2^{-\log_2 (1/p_i)} = p_i$ and therefore

$$
\sum_i 2^{-\ell_i} \leq \sum_i p_i = 1 .
$$

*The average length.* Since $\lceil t \rceil < t + 1$,

$$
\sum_i p_i \ell_i = \sum_i p_i \left\lceil \log_2 \frac{1}{p_i} \right\rceil <
\sum_i p_i \left( \log_2 \frac{1}{p_i} + 1 \right) =
\sum_i p_i \log_2 \frac{1}{p_i} + \sum_i p_i = H(S) + 1 . \;\; \blacksquare
$$

(This is exactly the proof of the theorem $\ell_a(C) \leq H(S) + 1$ in the Huffman chapter; here the
inequality is strict, because the $p_i$ are not all exact powers of $2$.)

**(d)** $\textsf{Huffman}(S)$ with the priority queue $Q$:

| Step | $Q$ before the step | $\textsf{ExtractMin}$ twice | New node $z.\mathit{freq}$ |
| --- | --- | --- | --- |
| 1 | $0.1_{x_4},\,0.1_{x_5},\,0.2_{x_2},\,0.2_{x_3},\,0.4_{x_1}$ | $x_4$, $x_5$ | $u = 0.2$ |
| 2 | $0.2_{x_2},\,0.2_{x_3},\,0.2_{u},\,0.4_{x_1}$ | $x_2$, $x_3$ | $v = 0.4$ |
| 3 | $0.2_{u},\,0.4_{x_1},\,0.4_{v}$ | $u$, $x_1$ | $t = 0.6$ |
| 4 | $0.4_{v},\,0.6_{t}$ | $v$, $t$ | root $= 1.0$ |

```text
root
├─0─ v ─0─ x2          x1 = 10     (2 bits)
│      └─1─ x3         x2 = 00     (2 bits)
└─1─ t ─0─ x1          x3 = 01     (2 bits)
       └─1─ u ─0─ x4   x4 = 110    (3 bits)
              └─1─ x5  x5 = 111    (3 bits)
```

$$
\ell_a(C^{\ast}) = 0.4 \cdot 2 + 0.2 \cdot 2 + 0.2 \cdot 2 + 0.1 \cdot 3 + 0.1 \cdot 3
= 2.2 \text{ bits}.
$$

*Why fewer than $H(S)+1$ bits.* Part (c) constructs **some** prefix code $C'$ with
$\ell_a(C') < H(S) + 1$. The Huffman code is optimal, so $\ell_a(C^{\ast}) \leq \ell_a(C') < H(S)+1$.
Here indeed $2.122 \leq 2.2 < 3.122$.

*Is the tree unique?* No. In step 2 the queue contains three elements of weight $0.2$, and in step 3
two elements of weight $0.4$ -- the ties can be broken differently. For example, merging $u$ with $v$
instead of with $x_1$ gives the code lengths $(1,3,3,3,3)$ and

$$
0.4 \cdot 1 + 0.2 \cdot 3 + 0.2 \cdot 3 + 0.1 \cdot 3 + 0.1 \cdot 3 = 2.2 \text{ bits} ,
$$

the same average length. Both trees are optimal; even the *multiset of code lengths* differs.

**(e)** With two messages every prefix code must use the codewords $\mathtt{0}$ and $\mathtt{1}$, so

$$
\ell_a(C) = 1 \text{ bit}, \qquad H(S) = -0.99\log_2 0.99 - 0.01 \log_2 0.01 \approx 0.0808 \text{ bits}.
$$

The loss is $\approx 0.92$ bits per message -- the code is more than $12$ times worse than the entropy.
(It is still within the guarantee $\ell_a \leq H(S)+1$; the bound is just very weak when $H(S)$ is
small.)

The loss can be reduced by **grouping symbols**, as in the Huffman chapter. For pairs
$T = \lbrace AA, AB, BA, BB \rbrace$ with probabilities $(0.9801,\, 0.0099,\, 0.0099,\, 0.0001)$ the
Huffman code lengths are $(1,3,2,3)$ and

$$
\ell_a(C_2) = 0.9801 \cdot 1 + 0.0099 \cdot 3 + 0.0099 \cdot 2 + 0.0001 \cdot 3 = 1.0299
$$

bits per **pair**, i.e. $0.515$ bits per message. Longer blocks push this towards $H(S)$, but the
convergence is slow; the real remedy is **arithmetic coding or ANS**, which do not need a whole number
of bits per symbol. $\square$

## Arithmetic Coding and ANS

### Problem 3 (Arithmetic coding)

$p(\mathtt{A}) = 0.5$, $p(\mathtt{B}) = 0.3$, $p(\mathtt{C}) = 0.2$, so the cumulative probabilities are

$$
f(\mathtt{A}) = 0, \qquad f(\mathtt{B}) = 0.5, \qquad f(\mathtt{C}) = 0.8 .
$$

**(a)** We use $l_i = l_{i-1} + f(x_i) \cdot s_{i-1}$ and $s_i = s_{i-1} \cdot p(x_i)$, starting from
$l_0 = 0$, $s_0 = 1$:

| $i$ | $x_i$ | $l_i = l_{i-1} + f(x_i)s_{i-1}$ | $s_i = s_{i-1}p(x_i)$ | Interval $[l_i;\,l_i+s_i)$ |
| --- | --- | --- | --- | --- |
| 1 | `A` | $0 + 0 \cdot 1 = 0$ | $1 \cdot 0.5 = 0.5$ | $[0;\,0.5)$ |
| 2 | `C` | $0 + 0.8 \cdot 0.5 = 0.4$ | $0.5 \cdot 0.2 = 0.1$ | $[0.4;\,0.5)$ |
| 3 | `B` | $0.4 + 0.5 \cdot 0.1 = 0.45$ | $0.1 \cdot 0.3 = 0.03$ | $[0.45;\,0.48)$ |
| 4 | `A` | $0.45 + 0 \cdot 0.03 = 0.45$ | $0.03 \cdot 0.5 = 0.015$ | $[0.45;\,0.465)$ |

$$
[0;1] \supset [0;\,0.5) \supset [0.4;\,0.5) \supset [0.45;\,0.48) \supset [0.45;\,0.465).
$$

**(b)** We need $[\beta;\, \beta+2^{-n}) \subseteq [0.45;\, 0.465)$, i.e. a dyadic interval of length
$2^{-n}$ inside an interval of length $s_4 = 0.015$. First, $2^{-n} \leq 0.015$ forces

$$
n \geq \log_2 \frac{1}{0.015} \approx 6.06, \qquad\text{so}\qquad n \geq 7 .
$$

($n = 6$ is impossible already because $2^{-6} = 0.015625 > 0.015$.) With $n = 7$ we look for an
integer $k$ with $k/128 \geq 0.45$ and $(k+1)/128 \leq 0.465$:

$$
k \geq 0.45 \cdot 128 = 57.6 \;\Rightarrow\; k \geq 58, \qquad
k + 1 \leq 0.465 \cdot 128 = 59.52 \;\Rightarrow\; k \leq 58 .
$$

So $k = 58 = 0111010_2$ and

$$
\beta = 0.0111010_2 = \frac{58}{128} = 0.453125, \qquad
\left[ \tfrac{58}{128};\, \tfrac{59}{128} \right) = [0.453125;\, 0.4609375) \subset [0.45;\, 0.465).
$$

Here $n = 7 = \left\lceil \log_2 \frac{1}{s_4} \right\rceil$ -- the code is less than one bit longer
than the information content $6.06$ bits of the message. In general up to $2$ bits may be lost, because
the dyadic interval must fit *entirely* inside $[l_4;\,l_4+s_4)$.

**(c)** $\textsf{Huffman}$ for $(0.5, 0.3, 0.2)$ merges $0.3 + 0.2 = 0.5$ and then $0.5 + 0.5 = 1$:

$$
C^{\ast} = \lbrace (\mathtt{A},\mathtt{0}),\; (\mathtt{B},\mathtt{10}),\; (\mathtt{C},\mathtt{11}) \rbrace,
\qquad \mathtt{ACBA} \rightarrow \mathtt{0}\,\mathtt{11}\,\mathtt{10}\,\mathtt{0} = \mathtt{011100}
\;\; (6 \text{ bits}).
$$

So for this short message the Huffman code is **better**: $6$ bits against $7$.

The reason is *where* the two algorithms lose. Huffman loses
$\ell_a(C^{\ast}) - H(S) = 1.5 - 1.4855 \approx 0.0145$ bits **per symbol**, i.e. the loss grows
linearly with the message length. Arithmetic coding loses at most $1$--$2$ bits on the **whole
message**, no matter how long it is. For $n$ symbols:

$$
\text{Huffman} \approx nH(S) + 0.0145 n, \qquad \text{arithmetic} \approx nH(S) + 2 .
$$

The constant $2$ dominates while $n$ is small (here $n = 4$), and arithmetic coding wins once
$0.0145 n > 2$, i.e. from about $n \approx 140$ symbols on. For very skewed distributions (as in
Problem 2(e), where Huffman loses $0.92$ bits per symbol) arithmetic coding wins almost immediately.

**(d)** $\beta = 0.101_2 = 0.625$. At each step we find the subinterval that contains $\beta$ and
narrow the interval, exactly as in $\textsf{Arithmetic-Decode}$:

| $i$ | Interval $[l_{i-1};\,l_{i-1}+s_{i-1})$ | Subintervals | Contains $0.625$ | $x_i$ |
| --- | --- | --- | --- | --- |
| 1 | $[0;\,1)$ | $\mathtt{A}\,[0;.5)$, $\mathtt{B}\,[.5;.8)$, $\mathtt{C}\,[.8;1)$ | $[0.5;\,0.8)$ | `B` |
| 2 | $[0.5;\,0.8)$ | $\mathtt{A}\,[.5;.65)$, $\mathtt{B}\,[.65;.74)$, $\mathtt{C}\,[.74;.8)$ | $[0.5;\,0.65)$ | `A` |
| 3 | $[0.5;\,0.65)$ | $\mathtt{A}\,[.5;.575)$, $\mathtt{B}\,[.575;.62)$, $\mathtt{C}\,[.62;.65)$ | $[0.62;\,0.65)$ | `C` |
| 4 | $[0.62;\,0.65)$ | $\mathtt{A}\,[.62;.635)$, $\mathtt{B}\,[.635;.644)$, $\mathtt{C}\,[.644;.65)$ | $[0.62;\,0.635)$ | `A` |

The first four letters are `BACA`.

*The same by rescaling* (this is how an implementation does it -- instead of narrowing the interval,
the number is stretched back to $[0;1)$):

$$
0.625 \xrightarrow{\;\mathtt{B}\;} \frac{0.625 - 0.5}{0.3} = 0.41\overline{6}
\xrightarrow{\;\mathtt{A}\;} \frac{0.41\overline{6}}{0.5} = 0.8\overline{3}
\xrightarrow{\;\mathtt{C}\;} \frac{0.8\overline{3} - 0.8}{0.2} = 0.1\overline{6}
\xrightarrow{\;\mathtt{A}\;} 0.\overline{3} . \;\; \square
$$

### Problem 4 (ANS)

$f(\mathtt{A}) = 3$, $f(\mathtt{N}) = 2$, $f(\mathtt{S}) = 1$, $M = 6$, $c(\mathtt{A}) = 0$,
$c(\mathtt{N}) = 3$, $c(\mathtt{S}) = 5$.

**(a)** A symbol $s$ owns the states $x$ whose remainder $r = x \bmod 6$ satisfies
$c(s) \leq r < c(s) + f(s)$:

| symbol | `A` | `N` | `S` |
| --- | --- | --- | --- |
| $f(s)$ | 3 | 2 | 1 |
| $c(s)$ | 0 | 3 | 5 |
| slots $r = x \bmod 6$ | $0,1,2$ | $3,4$ | $5$ |

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| owner | `A` | `A` | `A` | `N` | `N` | `S` | `A` | `A` | `A` | `N` | `N` | `S` | `A` | `A` | `A` | `N` | `N` | `S` |
| rank | 0 | 1 | 2 | 0 | 1 | 0 | 3 | 4 | 5 | 2 | 3 | 1 | 6 | 7 | 8 | 4 | 5 | 2 |

So `A` owns $0,1,2,6,7,8,12,13,14,\ldots$ (about $1/2$ of all numbers), `N` owns
$3,4,9,10,15,16,\ldots$ (about $1/3$), and `S` owns $5,11,17,\ldots$ (about $1/6$) -- exactly the
proportions $f(s)/M$. The "rank" row is the number of the slot in that symbol's own numeral system;
it is the value $x$ that the decoder returns.

**(b)** $\textsf{Rans-Encode}$ processes the message **backwards**, so the order is
`S`, `A`, `N`, `A`, `N`, `A`. Line 4 computes
$x = M \lfloor x/f(s) \rfloor + (x \bmod f(s)) + c(s)$:

| step | $s$ | $f(s)$ | $c(s)$ | $x$ before | computing $C(s,x)$ | $x$ after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `S` | 1 | 5 | 0 | $6 \cdot \lfloor 0/1 \rfloor + 0 + 5 = 0 + 5$ | **5** |
| 2 | `A` | 3 | 0 | 5 | $6 \cdot \lfloor 5/3 \rfloor + 2 + 0 = 6 + 2$ | **8** |
| 3 | `N` | 2 | 3 | 8 | $6 \cdot \lfloor 8/2 \rfloor + 0 + 3 = 24 + 3$ | **27** |
| 4 | `A` | 3 | 0 | 27 | $6 \cdot \lfloor 27/3 \rfloor + 0 + 0 = 54 + 0$ | **54** |
| 5 | `N` | 2 | 3 | 54 | $6 \cdot \lfloor 54/2 \rfloor + 0 + 3 = 162 + 3$ | **165** |
| 6 | `A` | 3 | 0 | 165 | $6 \cdot \lfloor 165/3 \rfloor + 0 + 0 = 330 + 0$ | **330** |

The whole message is the single number

$$
x = 330 = 101001010_2 \qquad (9 \text{ bits}).
$$

**(c)** $\textsf{Rans-Decode}(330, f, c, 6)$; line 2 takes $r = x \bmod 6$, line 5 computes
$x = f(s)\lfloor x/6 \rfloor + r - c(s)$:

| step | $x$ before | $r = x \bmod 6$ | $s = \textsf{Lookup}(r)$ | $x = f(s)\lfloor x/6\rfloor + r - c(s)$ | $x$ after |
| --- | --- | --- | --- | --- | --- |
| 1 | 330 | 0 | `A` | $3 \cdot 55 + 0 - 0$ | **165** |
| 2 | 165 | 3 | `N` | $2 \cdot 27 + 3 - 3$ | **54** |
| 3 | 54 | 0 | `A` | $3 \cdot 9 + 0 - 0$ | **27** |
| 4 | 27 | 3 | `N` | $2 \cdot 4 + 3 - 3$ | **8** |
| 5 | 8 | 2 | `A` | $3 \cdot 1 + 2 - 0$ | **5** |
| 6 | 5 | 5 | `S` | $1 \cdot 0 + 5 - 5$ | **0** |

The output is `A`, `N`, `A`, `N`, `A`, `S` -- the message `ANANAS` in the **correct** order (LIFO: the
symbol encoded last is decoded first), and the state returns to $x = 0$, which is the natural stopping
condition of ANS.

**(d)** The same decoder started at $x = 131$:

| step | $x$ before | $r = x \bmod 6$ | $s$ | $x = f(s)\lfloor x/6\rfloor + r - c(s)$ | $x$ after |
| --- | --- | --- | --- | --- | --- |
| 1 | 131 | 5 | `S` | $1 \cdot 21 + 5 - 5$ | **21** |
| 2 | 21 | 3 | `N` | $2 \cdot 3 + 3 - 3$ | **6** |
| 3 | 6 | 0 | `A` | $3 \cdot 1 + 0 - 0$ | **3** |
| 4 | 3 | 3 | `N` | $2 \cdot 0 + 3 - 3$ | **0** |

The four symbols are `SNAN`, and the state reaches $0$ exactly after them -- so $131$ is the complete
$\textsf{Rans-Encode}$ output of the message `SNAN`.

**(e)** With $p(\mathtt{A}) = 3/6$, $p(\mathtt{N}) = 2/6$, $p(\mathtt{S}) = 1/6$:

$$
-\log_2 \left( p(\mathtt{A})^3 p(\mathtt{N})^2 p(\mathtt{S}) \right) =
-\log_2 \left( \tfrac18 \cdot \tfrac19 \cdot \tfrac16 \right) = \log_2 432 = 4 + 3\log_2 3
\approx 8.755 \text{ bits},
$$

$$
\log_2 330 = 1 + \log_2 3 + \log_2 5 + \log_2 11 \approx 8.366 \text{ bits}.
$$

The state is slightly *smaller* than the information content only because the encoder started from
$x = 0$: the first step gave $C(\mathtt{S},0) = c(\mathtt{S}) = 5$, i.e. the state jumped to $5$
instead of about $6$, and $\log_2 x$ measures the true cost only asymptotically. What actually has to
be transmitted is the number $330$ in a whole number of bits -- $9$ bits against $8.755$ bits of
entropy, so about $0.25$ bits are lost on the whole message. This matches the `GACGU$` example of the
chapter, where $15$ bits were spent against $14.18$ bits of entropy.

**(f)** Both messages are encoded backwards, starting from $x = 0$:

| `NA`: $s$ | $x$ before | $x$ after | | `NAA`: $s$ | $x$ before | $x$ after |
| --- | --- | --- | --- | --- | --- | --- |
| `A` | 0 | $6 \cdot 0 + 0 + 0 =$ **0** | | `A` | 0 | $6 \cdot 0 + 0 + 0 =$ **0** |
| `N` | 0 | $6 \cdot 0 + 0 + 3 =$ **3** | | `A` | 0 | $6 \cdot 0 + 0 + 0 =$ **0** |
| | | | | `N` | 0 | $6 \cdot 0 + 0 + 3 =$ **3** |

Both give $x = 3$.

*Why.* In general $C(s, 0) = c(s)$, and here $c(\mathtt{A}) = 0$, so $C(\mathtt{A}, 0) = 0$: encoding
an `A` into the empty state changes nothing. This is exactly the **leading-zeros** problem of an
ordinary positional numeral system -- $\mathtt{007}$ and $\mathtt{7}$ are the same number. In ANS the
symbol with $c(s) = 0$ (the alphabetically first one) plays the role of the digit $0$, and any number
of copies of it at the *end* of the message -- which the encoder processes *first* -- disappear.

The message `ANANAS` does not have this problem, because it ends with `S` and
$c(\mathtt{S}) = 5 \neq 0$, so the very first step already moves the state away from $0$. In practice
there are two standard fixes, both mentioned in the chapter: keep the end-of-data marker `$` (because
of LIFO it is encoded first, and its $c(\$) \neq 0$), or tell the decoder the number of symbols $n$.
The streaming version $\textsf{Rans-Encode-Stream}$ solves it structurally -- it starts from $x = L$,
not from $x = 0$. $\square$

## Lempel–Ziv Algorithms

### Problem 5 (LZ77)

The input is `kakadukakadu`, $n = 12$; positions are numbered from $1$:

```text
 1 2 3 4 5 6 7 8 9 10 11 12
 k a k a d u k a k a  d  u
```

**(a)** $W = 6$, $L$ unlimited. Line 6 of $\textsf{LZ77-Encode}$ still limits the match by
$k < n - i$, so that a symbol $T[i+\ell]$ is left over for the triple.

| Cursor $i$ | Window $T[\max(1,i-6) \ldots i-1]$ | Longest match | Output $(d,\ell,x)$ | Next $i$ |
| --- | --- | --- | --- | --- |
| 1 | -- (empty) | none | $(0,0,\mathtt{k})$ | 2 |
| 2 | `k` | none (`k` $\neq$ `a`) | $(0,0,\mathtt{a})$ | 3 |
| 3 | `ka` | `ka` from position 1: $d = 2$, $\ell = 2$ | $(2,2,\mathtt{d})$ | 6 |
| 6 | `kakad` | none (`u` is not in the window) | $(0,0,\mathtt{u})$ | 7 |
| 7 | `kakadu` | `kakad` from position 1: $d = 6$, $\ell = 5$ | $(6,5,\mathtt{u})$ | 13 |

Details of the two interesting steps:

* **$i = 3$:** the scan goes $s = 2, 1$. At $s = 2$ already $T[2] = \mathtt{a} \neq \mathtt{k} = T[3]$.
  At $s = 1$: $T[1..2] = \mathtt{ka}$ matches $T[3..4] = \mathtt{ka}$, and then
  $T[3] = \mathtt{k} \neq \mathtt{d} = T[5]$. So $d = 3-1 = 2$, $\ell = 2$, and the following letter is
  $T[5] = \mathtt{d}$.
* **$i = 7$:** at $s = 3$ the match is `ka` ($\ell = 2$), but at $s = 1$ it runs
  $\mathtt{k}\mathtt{a}\mathtt{k}\mathtt{a}\mathtt{d}\mathtt{u}$ -- six letters. The loop stops at
  $k = 5$, because the condition is $k < n - i = 12 - 7 = 5$; the sixth letter $T[12] = \mathtt{u}$
  becomes the symbol $x$ of the triple. So $d = 7 - 1 = 6$ (the largest offset the window still
  reaches), $\ell = 5$.

Result: $(0,0,\mathtt{k}), (0,0,\mathtt{a}), (2,2,\mathtt{d}), (0,0,\mathtt{u}), (6,5,\mathtt{u})$ --
$12$ letters in $5$ triples.

**(b)** $W = 4$: the window is $T[\max(1,i-4) \ldots i-1]$.

| Cursor $i$ | Window | Longest match | Output $(d,\ell,x)$ | Next $i$ |
| --- | --- | --- | --- | --- |
| 1 | -- | none | $(0,0,\mathtt{k})$ | 2 |
| 2 | `k` | none | $(0,0,\mathtt{a})$ | 3 |
| 3 | `ka` | `ka` from position 1: $d = 2$, $\ell = 2$ | $(2,2,\mathtt{d})$ | 6 |
| 6 | `akad` | none | $(0,0,\mathtt{u})$ | 7 |
| 7 | `kadu` | `ka` from position 3: $d = 4$, $\ell = 2$ | $(4,2,\mathtt{k})$ | 10 |
| 10 | `ukak` | `a` from position 8: $d = 2$, $\ell = 1$ | $(2,1,\mathtt{d})$ | 12 |
| 12 | `akad` | none | $(0,0,\mathtt{u})$ | 13 |

Result: $(0,0,\mathtt{k}), (0,0,\mathtt{a}), (2,2,\mathtt{d}), (0,0,\mathtt{u}), (4,2,\mathtt{k}), (2,1,\mathtt{d}), (0,0,\mathtt{u})$
-- $7$ triples instead of $5$.

*Why there are more triples.* The string is the word `kakadu` written twice, so the ideal parsing is
"copy $6$ letters from distance $6$". With $W = 6$ the offset $d = 6$ is exactly the last one the
window reaches, and a single triple covers the whole repetition. With $W = 4$ the offset $6$ is out of
reach: at $i = 7$ the encoder no longer sees the beginning of the first `kakadu` and has to piece the
repetition together from short nearby matches ($\ell = 2$, then $\ell = 1$), spending one triple per
two or three letters. This is the general trade-off -- a short window is cheaper (fewer bits for $d$,
faster search), but it cannot exploit distant repetitions.

**(c)** $\textsf{LZ77-Decode}$ on
$(0,0,\mathtt{l}), (0,0,\mathtt{a}), (2,5,\mathtt{i}), (4,3,\mathtt{a})$. The decoder keeps $m$ -- the
number of letters already produced -- and for each triple copies $\ell$ letters **one at a time** from
$T[m+k-d]$, then appends $x$:

| Triple | $m$ before | Copied letters $T[m+k] = T[m+k-d]$ | $T$ after the triple | $m$ after |
| --- | --- | --- | --- | --- |
| $(0,0,\mathtt{l})$ | 0 | -- | `l` | 1 |
| $(0,0,\mathtt{a})$ | 1 | -- | `la` | 2 |
| $(2,5,\mathtt{i})$ | 2 | $T[3]{=}T[1]{=}\mathtt{l}$, $T[4]{=}T[2]{=}\mathtt{a}$, $T[5]{=}T[3]{=}\mathtt{l}$, $T[6]{=}T[4]{=}\mathtt{a}$, $T[7]{=}T[5]{=}\mathtt{l}$ | `lalalali` | 8 |
| $(4,3,\mathtt{a})$ | 8 | $T[9]{=}T[5]{=}\mathtt{l}$, $T[10]{=}T[6]{=}\mathtt{a}$, $T[11]{=}T[7]{=}\mathtt{l}$ | `lalalalilala` | 12 |

The decoded string is `lalalalilala`.

**The overlap happens in the third triple**, $(2,5,\mathtt{i})$, where $d = 2 < \ell = 5$: the source
region $T[1..5]$ overlaps the region being written $T[3..7]$. From $k = 3$ on, the decoder copies
letters it produced *in this same step* ($T[5]$ is written at $k = 3$ and read at $k = 5$). This is
exactly why line 4 of $\textsf{LZ77-Decode}$ copies symbol by symbol instead of doing a block move --
and it is what lets one triple encode an arbitrarily long periodic run. In the fourth triple
$d = 4 > \ell = 3$, so there is no overlap. $\square$

### Problem 6 (LZ78)

**(a)** $\textsf{LZ78-Encode}$ on `abababababa` ($n = 11$), $S = \lbrace \mathtt{a}, \mathtt{b} \rbrace$.
Initially $D[\mathtt{a}] = \mathtt{a}$, $D[\mathtt{b}] = \mathtt{b}$, $m = 0$, $w = T[1] = \mathtt{a}$.
The table shows only the steps in which line 6 fails, i.e. the phrase $w$ is output and $wk$ is added:

| Step | $i$ | Longest $w$ in $D$ | $k = T[i]$ | Output $D[w]$ | $m$ | Added: $D[wk]$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | `a` | `b` | `a` | 1 | 1: `ab` |
| 2 | 3 | `b` | `a` | `b` | 2 | 2: `ba` |
| 3 | 5 | `ab` | `a` | 1 | 3 | 3: `aba` |
| 4 | 8 | `aba` | `b` | 3 | 4 | 4: `abab` |
| 5 | 10 | `ba` | `b` | 2 | 5 | 5: `bab` |
| 6 | -- | `ba` | -- | 2 (line 13) | -- | -- |

(In the rows not shown, $wk \in D$ and the encoder only extends $w$; for instance at $i = 4$ we have
$wk = \mathtt{ab} \in D$, so $w$ becomes `ab`.)

Phrases added to the dictionary: `1: ab`, `2: ba`, `3: aba`, `4: abab`, `5: bab`. Note that phrases
$4$ and $5$ are created but never used -- each new phrase is an old one extended by exactly one letter,
which is why the phrases grow only slowly.

The code sequence is `a,b,1,3,2,2`, and the parsing is `a.b.ab.aba.ba.ba`.

**(b)** $\textsf{LZ78-Decode}(\mathtt{a},\mathtt{b},1,3,2,2)$. Line 12 adds the **previous** phrase $w$
with the first letter of the **current** phrase $v$ appended:

| $j$ | $c_j$ | In $D$? | Phrase $v$ | Output | $m$ | Added: $D[m] = w\,v[1]$ | New $w$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `a` | yes (letter) | `a` | `a` | 0 | -- | `a` |
| 2 | `b` | yes (letter) | `b` | `b` | 1 | 1: `ab` | `b` |
| 3 | 1 | yes | `ab` | `ab` | 2 | 2: `ba` | `ab` |
| 4 | 3 | **no** ($m = 2$) | $w\,w[1] = \mathtt{ab}\,\mathtt{a} = $ `aba` | `aba` | 3 | 3: `aba` | `aba` |
| 5 | 2 | yes | `ba` | `ba` | 4 | 4: `abab` | `ba` |
| 6 | 2 | yes | `ba` | `ba` | 5 | 5: `bab` | `ba` |

The decoded phrases are `a.b.ab.aba.ba.ba`, i.e. the string `abababababa`, and the dictionary is
identical to the encoder's.

**The decoder receives an unknown number in step $j = 4$**, where $c_4 = 3$ but the dictionary contains
only phrases $1$ and $2$. The encoder had already created phrase $3$ when it output it; the decoder is
one step behind, because line 12 needs the first letter of the current phrase. The special case of
lines 8--9 applies: $c_j = m+1$, so the new phrase begins with the previous phrase $w$ and ends with
its own first letter, which equals $w[1]$ -- hence
$v = w\,w[1] = \mathtt{ab} + \mathtt{a} = \mathtt{aba}$.

**(c)** $\textsf{LZ78-Decode}(\mathtt{l},\mathtt{a},1,3,2,5)$, $S = \lbrace \mathtt{a}, \mathtt{l} \rbrace$:

| $j$ | $c_j$ | In $D$? | Phrase $v$ | Output | $m$ | Added: $D[m] = w\,v[1]$ | New $w$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `l` | yes (letter) | `l` | `l` | 0 | -- | `l` |
| 2 | `a` | yes (letter) | `a` | `a` | 1 | 1: `la` | `a` |
| 3 | 1 | yes | `la` | `la` | 2 | 2: `al` | `la` |
| 4 | 3 | **no** ($m = 2$) | $w\,w[1] = \mathtt{la}\,\mathtt{l} = $ `lal` | `lal` | 3 | 3: `lal` | `lal` |
| 5 | 2 | yes | `al` | `al` | 4 | 4: `lala` | `al` |
| 6 | 5 | **no** ($m = 4$) | $w\,w[1] = \mathtt{al}\,\mathtt{a} = $ `ala` | `ala` | 5 | 5: `ala` | `ala` |

The phrases are `l.a.la.lal.al.ala`, so the string is `lalalalalala` ($12$ letters). Here the special
case of lines 8--9 occurs **twice**, at $j = 4$ and $j = 6$. (Re-encoding `lalalalalala` with
$\textsf{LZ78-Encode}$ indeed gives back `l,a,1,3,2,5`.)

**(d)** The alphabet has one letter, so $D[\mathtt{a}] = \mathtt{a}$ and the dictionary grows as
`1: aa`, `2: aaa`, `3: aaaa`, ... Every new phrase is the previous one extended by one letter, and each
phrase is used only once, so the parsing is

$$
\underbrace{\mathtt{a}}_{1} \mid \underbrace{\mathtt{aa}}_{2} \mid
\underbrace{\mathtt{aaa}}_{3} \mid \underbrace{\mathtt{aaaa}}_{4} \mid \ldots
$$

-- the $r$-th output code covers exactly $r$ letters. After $r$ codes the encoder has consumed

$$
1 + 2 + \ldots + r = \frac{r(r+1)}{2}
$$

letters. **Exact answer:** if $n = 1 + 2 + \ldots + r$, then $\textsf{LZ78-Encode}$ outputs exactly
$r$ codes, namely `a, 1, 2, ..., r-1`. (Check: $n = 1 \rightarrow 1$ code `a`; $n = 3 \rightarrow 2$
codes `a,1`; $n = 6 \rightarrow 3$ codes `a,1,2`; $n = 10 \rightarrow 4$; $n = 15 \rightarrow 5$.)

**Approximate answer:** solving $r(r+1)/2 = n$ gives

$$
r = \frac{\sqrt{8n+1} - 1}{2} \approx \sqrt{2n},
$$

and for an arbitrary $n$ the number of codes is $\left\lceil \frac{\sqrt{8n+1}-1}{2} \right\rceil$ --
the last phrase is simply cut short. So $n$ letters become about $\sqrt{2n}$ codes: the compression
ratio grows without bound. This is the extreme case of the asymptotic optimality theorem, since such a
source has entropy rate $0$. $\square$

## Burrows–Wheeler Transform

### Problem 7 (BWT)

**(a)** All cyclic rotations of `KAKAO$`, then sorted with
$\mathtt{\$} < \mathtt{A} < \mathtt{K} < \mathtt{O}$:

```text
K A K A O $              $ K A K A O
A K A O $ K              A K A O $ K
K A O $ K A    --->      A O $ K A K
A O $ K A K              K A K A O $     <- row 4
O $ K A K A              K A O $ K A
$ K A K A O              O $ K A K A
```

(Sorting details: of the two rows starting with `A` the second letters are `K` and `O`, so `AKAO$K`
comes first; of the two rows starting with `K` the third letters are `K` and `O`.)

The transform is the last column:

$$
\text{BWT}(\mathtt{KAKAO\$}) = \mathtt{OKK\$AA} .
$$

The original word `KAKAO$` is in **row 4** of the sorted matrix (rows numbered from $1$).

**(b)** $\textsf{MoveToFrontEncode}$ of `OKK$AA` with the initial alphabet `[$,A,K,O]` (positions
numbered from $0$). The alphabet shown is the one *before* the step:

| Input | Output | Alphabet before the step |
| --- | --- | --- |
| **O**, K, K, `$`, A, A | 3 | `[$,A,K,O]` |
| O, **K**, K, `$`, A, A | 3,3 | `[O,$,A,K]` |
| O, K, **K**, `$`, A, A | 3,3,0 | `[K,O,$,A]` |
| O, K, K, **`$`**, A, A | 3,3,0,2 | `[K,O,$,A]` |
| O, K, K, `$`, **A**, A | 3,3,0,2,3 | `[$,K,O,A]` |
| O, K, K, `$`, A, **A** | 3,3,0,2,3,0 | `[A,$,K,O]` |
| N/A | N/A | `[A,$,K,O]` |

The code is `3,3,0,2,3,0`. Each repeated pair produced by the BWT (`KK` and `AA`) turned into a $0$ --
exactly the effect for which *Move-to-front* is applied after a BWT.

**(c)** Given $L = \text{BWT}(w) = \mathtt{ASSAL\$}$, the first column $F$ is $L$ sorted:

| row $i$ | $F[i]$ | $L[i]$ | rank of $L[i]$ | $\textsf{LF}(i)$ |
| --- | --- | --- | --- | --- |
| 0 | `$` | `A` | 1st `A` | 1 |
| 1 | `A` | `S` | 1st `S` | 4 |
| 2 | `A` | `S` | 2nd `S` | 5 |
| 3 | `L` | `A` | 2nd `A` | 2 |
| 4 | `S` | `L` | 1st `L` | 3 |
| 5 | `S` | `$` | 1st `$` | 0 |

The Last-to-First mapping $\textsf{LF}(i)$ sends the $k$-th occurrence of a letter in $L$ to the $k$-th
occurrence of the same letter in $F$ -- identical letters keep their relative order in both columns.
Since every row is a cyclic rotation, $L[i]$ is the letter *preceding* $F[i]$ in $w$. So we start from
row $0$ -- the rotation beginning with `$`, i.e. $\mathtt{\$}w_1w_2\ldots w_5$ -- and read $w$
**backwards**:

| Step | row $i$ | $L[i]$ | position in $w$ | next row $\textsf{LF}(i)$ |
| --- | --- | --- | --- | --- |
| 1 | 0 | `A` | $w_5$ | 1 |
| 2 | 1 | `S` | $w_4$ | 4 |
| 3 | 4 | `L` | $w_3$ | 3 |
| 4 | 3 | `A` | $w_2$ | 2 |
| 5 | 2 | `S` | $w_1$ | 5 |

$$
w = \mathtt{S}\,\mathtt{A}\,\mathtt{L}\,\mathtt{S}\,\mathtt{A}\,\mathtt{\$} = \mathtt{SALSA\$} .
$$

Check by the direct definition:

```text
S A L S A $              $ S A L S A          A
A L S A $ S              A $ S A L S          S
L S A $ S A    --->      A L S A $ S          S
S A $ S A L              L S A $ S A          A
A $ S A L S              S A $ S A L          L
$ S A L S A              S A L S A $          $
```

The last column is `ASSAL$`, as required. $\square$

### Problem 8 (BWT with a suffix array)

$w = \mathtt{BARBARA\$}$, $n = 8$; positions are numbered from $0$:

```text
 0 1 2 3 4 5 6 7
 B A R B A R A $
```

**(a)** All suffixes, then sorted with $\mathtt{\$} < \mathtt{A} < \mathtt{B} < \mathtt{R}$:

| Suffix (not stored) | Suffix number |
| --- | --- |
| `$` | 7 |
| `A$` | 6 |
| `ARA$` | 4 |
| `ARBARA$` | 1 |
| `BARA$` | 3 |
| `BARBARA$` | 0 |
| `RA$` | 5 |
| `RBARA$` | 2 |

$$
A = [\,7,\; 6,\; 4,\; 1,\; 3,\; 0,\; 5,\; 2\,] .
$$

(`ARA$` comes before `ARBARA$` because of the third letters `A` < `B`; similarly `BARA$` before
`BARBARA$` and `RA$` before `RBARA$`.)

**(b)** $\textsf{efficientBWT}(w)$: for every $i$ output $w[A[i]-1]$, where $j = -1$ is replaced by
$j = n - 1 = 7$:

| $i$ | $A[i]$ | $j = A[i]-1$ | $w[j]$ |
| --- | --- | --- | --- |
| 0 | 7 | 6 | `A` |
| 1 | 6 | 5 | `R` |
| 2 | 4 | 3 | `B` |
| 3 | 1 | 0 | `B` |
| 4 | 3 | 2 | `R` |
| 5 | 0 | $-1 \rightarrow 7$ | `$` |
| 6 | 5 | 4 | `A` |
| 7 | 2 | 1 | `A` |

$$
\text{BWT}(\mathtt{BARBARA\$}) = \mathtt{ARBBR\$AA} .
$$

Check with the cyclic rotations:

```text
B A R B A R A $              $ B A R B A R A     A
A R B A R A $ B              A $ B A R B A R     R
R B A R A $ B A              A R A $ B A R B     B
B A R A $ B A R    --->      A R B A R A $ B     B
A R A $ B A R B              B A R A $ B A R     R
R A $ B A R B A              B A R B A R A $     $
A $ B A R B A R              R A $ B A R B A     A
$ B A R B A R A              R B A R A $ B A     A
```

The last column is `ARBBR$AA`, and the sorted rotations come in the same order as the sorted suffixes:
rows $0,1,\ldots,7$ start at positions $7, 6, 4, 1, 3, 0, 5, 2$, i.e. exactly at $A$. Row $5$, the one
ending with `$`, is the original word `BARBARA$`.

**(c)** Write $\text{rot}_i$ for the rotation starting at position $i$ and $\text{suf}_i$ for the
suffix starting at $i$. Then

$$
\text{rot}_i = \text{suf}_i \cdot w[0 \ldots i-1],
$$

i.e. every rotation *begins* with the corresponding suffix. Take $i \neq j$ and compare $\text{suf}_i$
with $\text{suf}_j$. The symbol `$` occurs exactly once in $w$ and only at the very end, so neither
suffix is a prefix of the other: at the position where the shorter one (say $\text{suf}_i$) has its
`$`, the longer one still has an ordinary letter, and `$` is smaller than every letter. Hence the
comparison is decided **at or before the first `$`**.

Up to that position $\text{rot}_i$ agrees letter for letter with $\text{suf}_i$ (a rotation differs
from its suffix only *after* the suffix runs out), and likewise for $j$. So the same position decides
the comparison of $\text{rot}_i$ and $\text{rot}_j$, with the same result:

$$
\text{suf}_i < \text{suf}_j \iff \text{rot}_i < \text{rot}_j .
$$

The two sorted orders therefore coincide, and $A[i]$ tells which rotation is in row $i$. Without a
unique smallest final symbol this fails -- see the `CAA` example of the chapter, where the naive BWT
gives `CAA` but $\textsf{efficientBWT}$ gives `AAC`.

**(d)** The occurrences of `BAR` are exactly the starting positions of the suffixes whose prefix is
`BAR`. Because the suffix array is sorted **lexicographically**, all strings with a common prefix $P$
form one contiguous block: if $\text{suf}_{A[i]} < \text{suf}_{A[k]} < \text{suf}_{A[j]}$ and both ends
begin with $P$, then the middle one must begin with $P$ as well -- otherwise it would be either smaller
than everything beginning with $P$ or larger than everything beginning with $P$. That is why the
answers are adjacent entries of $A$.

Two binary searches over $A$ therefore suffice:

* the *lower* bound -- the smallest $i$ with $\text{suf}_{A[i]} \geq \mathtt{BAR}$;
* the *upper* bound -- the smallest $i$ with $\text{suf}_{A[i]}$ no longer beginning with `BAR`.

For `BARBARA$`:

| $i$ | $A[i]$ | Suffix | Begins with `BAR`? |
| --- | --- | --- | --- |
| 3 | 1 | `ARBARA$` | no |
| 4 | 3 | `BARA$` | **yes** |
| 5 | 0 | `BARBARA$` | **yes** |
| 6 | 5 | `RA$` | no |

The block is $A[4 \ldots 5] = \lbrace 3,\, 0 \rbrace$: `BAR` occurs at positions $0$ and $3$, and the
number of occurrences ($2$) can be read off as the length of the block without inspecting them.

Each comparison costs $O(|P|)$ character comparisons, so the search takes $O(|P| \log n)$ time plus
$O(\textit{occ})$ for listing the answers.

**(e)**

| | Naive BWT | With a suffix array |
| --- | --- | --- |
| Building the data | write out $n$ rotations of length $n$ | build the suffix array $A$ |
| Space | $O(n^2)$ | $O(n)$ |
| Sorting | $O(n \log n)$ comparisons $\times$ $O(n)$ per comparison | $O(n)$ (linear-time construction) |
| Reading off the BWT | the last column, $O(n)$ | $n$ lookups $w[A[i]-1]$, $O(n)$ |
| **Total time** | $O(n^2 \log n)$ | $O(n)$ |

For a typical bzip2 block of $n = 900\,000$ bytes the difference is decisive:
$n^2 \log_2 n \approx 1.6 \cdot 10^{13}$ against $n \approx 10^6$ -- and the naive method would also
need about $8 \cdot 10^{11}$ bytes just to store the matrix. (Even a simple comparison-based suffix
array construction in $O(n \log^2 n)$ is entirely practical; the linear-time algorithms come in the
suffix-array chapter at the end of the course.) $\square$

## Markov Chains

### Problem 9 (Markov chain and compression)

**(a)** The graph of the chain:

```text
        1/2
       ┌───┐
       │   ↓
    ┌─────────┐   1/2    ┌─────────┐    1     ┌─────────┐
    │    A    │ ───────> │    B    │ ───────> │    C    │
    └─────────┘          └─────────┘          └─────────┘
         ↑                                         │
         └─────────────────────────────────────────┘
                            1
```

With the states in the order $(\mathtt{A}, \mathtt{B}, \mathtt{C})$ and the rows indexed by the current
state:

$$
P = \left( \begin{array}{ccc}
1/2 & 1/2 & 0 \\
0 & 0 & 1 \\
1 & 0 & 0
\end{array} \right) .
$$

The text starts with `A` with probability $1$, so for `ABCAABCA` we multiply the $7$ transition
probabilities:

$$
p = \underbrace{P_{AB}}_{1/2} \cdot \underbrace{P_{BC}}_{1} \cdot \underbrace{P_{CA}}_{1} \cdot
\underbrace{P_{AA}}_{1/2} \cdot \underbrace{P_{AB}}_{1/2} \cdot \underbrace{P_{BC}}_{1} \cdot
\underbrace{P_{CA}}_{1} = \left( \frac12 \right)^3 = \frac18 .
$$

Only the three transitions out of `A` are random; all the others are forced.

**(b)** The stationary distribution satisfies $\pi P = \pi$, i.e.

$$
\left\lbrace \begin{array}{l}
\pi_A = \tfrac12 \pi_A + \pi_C \\
\pi_B = \tfrac12 \pi_A \\
\pi_C = \pi_B
\end{array} \right.
\qquad \Longrightarrow \qquad \pi_C = \pi_B = \tfrac12 \pi_A ,
$$

after which the first equation is automatically satisfied. Normalizing,
$\pi_A + \tfrac12 \pi_A + \tfrac12 \pi_A = 2\pi_A = 1$:

$$
\pi = \left( \pi_A, \pi_B, \pi_C \right) = \left( \tfrac12,\; \tfrac14,\; \tfrac14 \right) .
$$

(Sanity check: on average half of the letters are `A`, and `B` and `C` always come in pairs, so they
must be equally frequent.)

**(c)** *Irreducible:* yes -- the cycle $\mathtt{A} \to \mathtt{B} \to \mathtt{C} \to \mathtt{A}$ makes
every state reachable from every other. In the terms of the Lempel--Ziv chapter ("Markov chains in
which every state can be reached from every other state are ergodic") the chain is **ergodic**.

*Periodic:* no. The cycle lengths are $1$ (the loop $\mathtt{A} \to \mathtt{A}$) and $3$, and
$\gcd(1,3) = 1$, so the chain is **aperiodic**. Therefore the distribution at time $n$ converges to
$\pi$ from any starting state, and the process is asymptotically stationary.

*If the transition $\mathtt{A} \to \mathtt{A}$ is removed,* the chain becomes the deterministic cycle
$\mathtt{A} \to \mathtt{B} \to \mathtt{C} \to \mathtt{A}$:

* it is still irreducible, and its stationary distribution becomes $\pi = (1/3, 1/3, 1/3)$;
* but it now has **period $3$**: starting from `A`, the letter at time $n$ is determined exactly, so
  the distribution at time $n$ never converges. As the chapter puts it, a periodic sequence cannot be
  stationary -- every probability distribution depends on the phase of the period. (In the stricter
  Markov-chain terminology, a periodic chain is also not called ergodic.)
* The text becomes `ABCABCABC...`, which contains no randomness at all: the entropy rate is $0$, and
  any reasonable compressor squeezes $n$ letters into $O(\log n)$ bits.

**(d)** *Single-letter entropy* in the stationary distribution $\pi = (1/2, 1/4, 1/4)$:

$$
H(X_1) = \tfrac12 \log_2 2 + \tfrac14 \log_2 4 + \tfrac14 \log_2 4
= \tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 = 1.5 \text{ bits}.
$$

*Entropy rate.* The entropies of the rows of $P$ are

| state $i$ | transitions | $H(\text{transitions from } i)$ |
| --- | --- | --- |
| `A` | $(1/2,\, 1/2,\, 0)$ | $1$ bit |
| `B` | $(0,\, 0,\, 1)$ | $0$ bits |
| `C` | $(1,\, 0,\, 0)$ | $0$ bits |

$$
H(X) = \sum_i \pi_i \cdot H(\text{transitions from } i)
= \tfrac12 \cdot 1 + \tfrac14 \cdot 0 + \tfrac14 \cdot 0 = 0.5 \text{ bits per letter}.
$$

*Huffman on single letters.* With probabilities $(1/2, 1/4, 1/4)$ the Huffman code is
$\mathtt{A} \to \mathtt{0}$, $\mathtt{B} \to \mathtt{10}$, $\mathtt{C} \to \mathtt{11}$, and

$$
\ell_a(C^{\ast}) = \tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 = 1.5 \text{ bits per letter}.
$$

Here the Huffman code is **exactly optimal for the single-letter model** ($\ell_a = H(X_1)$, because
all probabilities are powers of $2$) and still spends **three times** the entropy rate $0.5$. The loss
has nothing to do with Huffman's algorithm -- it comes from the model, which ignores the context.

**(e)** Cut the text after every `A`. The chain is in state `A` at the start and, by construction,
right after every `A`. From `A` there are exactly two continuations:

* with probability $1/2$ the next letter is `A` -- the piece is `A`, and we are in state `A` again;
* with probability $1/2$ the next letter is `B`, after which `C` and then `A` are forced -- the piece
  is `BCA`, and again we end in state `A`.

Both pieces end in the same state `A`, so the pieces are **independent and identically distributed**,
each with probability $1/2$. For example

$$
\mathtt{A}\,|\,\mathtt{BCA}\,|\,\mathtt{A}\,|\,\mathtt{BCA}\,|\,\mathtt{A} \ldots
$$

Encode the pieces with one bit each: $\mathtt{A} \to \mathtt{0}$, $\mathtt{BCA} \to \mathtt{1}$. (This
is the Huffman code for two equally likely messages -- optimal, and its average length equals the
entropy of one piece, which is exactly $1$ bit.) The average piece length is

$$
\mathbb{E}[\text{letters per piece}] = \tfrac12 \cdot 1 + \tfrac12 \cdot 3 = 2 \text{ letters},
$$

so the cost per letter is

$$
\frac{1 \text{ bit}}{2 \text{ letters}} = 0.5 \text{ bits per letter} = H(X) .
$$

This is exactly the entropy rate -- one third of what single-letter Huffman coding spends.

**Which algorithm finds the pieces by itself?** The **Lempel--Ziv algorithms**. $\textsf{LZ78-Encode}$
builds a dictionary of repeated phrases and quickly enters `BCA` (and `A`, `BCAB`, ...) into it, after
which every occurrence costs one code; $\textsf{LZ77-Encode}$ does the same with matches in the sliding
window. Neither is told the transition matrix -- the structure is discovered from the data itself.
This is precisely the content of the asymptotic optimality theorem of the Lempel--Ziv chapter: for a
stationary ergodic source,

$$
\limsup_n \frac{1}{n} \ell_{\text{LZW}}(X_{1:n}) \leq H(X)
$$

with probability $1$. Here $H(X) = 0.5$ bits per letter, while an entropy code built on the
single-letter distribution is stuck at $1.5$. $\square$
