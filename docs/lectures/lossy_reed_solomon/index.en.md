---
layout: default
title: "Error Correction: Reed–Solomon Codes"
lang: en
permalink: /lectures/lossy_reed_solomon/
---
# 8. Error Correction: Reed–Solomon Codes

* Why correct more than one error?
* Allows correcting a large number of errors.
* The message before and after encoding is a sequence of numbers.

## Introduction to the Reed–Solomon Method

**Description of the method:** The data is split into groups of $k$ numbers. $a_1,a_2,\ldots,a_k$ is one group. Define the polynomial:

$$
f(x) = a_1x^{k-1} + a_2x^{k-2}+\ldots + a_{k-1}x + a_k.
$$

Instead of the numbers $a_1,\ldots,a_k$, the values of the polynomial are sent:

$$
f(0),f(1),\ldots,f(s-1)
$$

for a chosen $s>k$.

**Applications of Reed–Solomon codes:** Consumer technologies where reading errors can occur. See [Reed-Solomon error correction](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction).

* Audio CD, DVD, Blu-ray discs,
* QR codes,
* Data transmission with DSL and WiMAX,
* Satellite communication, DVB and ATSC,
* RAID 6.

**Fundamental theorem of algebra:** A polynomial $P(x)$ of degree $n>0$ can be written in exactly one way as

$$
P(x)=c(x-x_1)(x-x_2)\cdots(x-x_n),
$$

where $x_i$ are the (complex) roots of the polynomial $P(x)$. Representations that differ only in the order of the factors are considered equal. Here $c \neq 0$, and the complex numbers $x_1,\ldots,x_n$ are not necessarily all distinct.

**Corollary #1 of the fundamental theorem:** If $h(x)$ is a polynomial of degree at most $k$ and $h(x) \neq 0$ (not identically equal to $0$), then there are at most $k$ values of $x$ with $h(x) = 0$. In other words, $h(x)$ has at most $k$ roots.

**Proof:** This follows from the fundamental theorem of algebra: if there were more roots $x_i$, $h(x)$ could be written as the product of all $(x-x_i)$. Expanding the brackets would show that the degree of $h(x)$ exceeds $k$. A contradiction. $\blacksquare$

**Corollary #2 of the fundamental theorem:** If two polynomials $f(x)$ and $g(x)$ have degrees at most $k-1$ and their values coincide at $k$ distinct points, then they are identically equal.

**Proof:** We subtract the two polynomials and denote:

$$
h(x) = f(x)-g(x).
$$

Each point $x_i$ where $f(x)=g(x)$ is a root of the polynomial $h(x)$. The degree of $h(x)$ also does not exceed $k-1$. If there were more than $k$ roots, $h(x)$ would be identically zero. $\blacksquare$

*Examples:* Through two points one can draw only one straight line (a polynomial of degree 1) $P(x)=a_1x+a_2$. Through three points $(a_1,b_1)$, $(a_2,b_2)$, $(a_3,b_3)$, where $a_1,a_2,a_3$ are pairwise distinct, one can draw only one parabola or straight line (a polynomial of degree two or one, etc.).

### The Number of Values Sent by Reed–Solomon

**Claim:** If there are $2$ messages $a_1,\ldots,a_k$ and $b_1, \ldots, b_k$, then

$$
f(x) = a_1x^{k-1} + a_2x^{k-2}+\ldots+a_{k-1}x + a_k,
$$

$$
g(x) = b_1x^{k-1} + b_2x^{k-2}+\ldots+b_{k-1}x + b_k.
$$

* Since each of these polynomials has degree at most $k-1$, $f(x)$ and $g(x)$ coincide in at most $k-1$ positions. (This is the second corollary of the fundamental theorem of algebra.)
* If $s$ values of the polynomial are sent, they differ in the remaining $s - (k-1)$ positions.

**How many of the transmitted values may be wrong?** We saw earlier that if two encoded messages differ in at least $2c+1$ positions, then the code can correct any $c$ errors.

$$
s-(k-1) \geq 2c+1 \;\;\Rightarrow\;\; s - k \geq 2c \;\;\Rightarrow c \leq (s-k)/2
$$

* A Reed–Solomon code can correct up to $(s-k)/2$ errors.
* If $s=2k$, then $c \leq (2k-k)/2 = k/2$ errors can be corrected.
* If at most $1/4$ of a message of length $2k$ is received incorrectly, the original text can be recovered.

**Example:**

* How many errors can be corrected if $k=4$, $s=9$: then $c \leq (s-k)/2 = 2.5$. **So 2 errors can be corrected.**
* Why can't we correct $3$ errors? To correct them, any two transmitted messages must differ in $2c+1$ positions ($2\cdot 3 + 1 = 7$ positions).
* The fundamental theorem of algebra implies that $f(x)$ and $g(x)$ coincide in at most $k-1$ positions and differ in at least $s - (k-1)$ positions.
* So they may differ in exactly $s-(k-1)=6$ positions. This is a contradiction: if we tried to correct $3$ errors, $2$ codes that differ in $6$ positions could not be told apart.

**Example with polynomials:** Consider the following two different polynomials (with several common roots).

$$
f(x) = x(x-1)(x-2) = x^3 - 3x^2 + 2x + 0.
$$

$$
g(x) = 2x(x-1)(x-2) = 2x^3 - 6x^2 + 4x + 0.
$$

If the original sequences are $(1;-3;2;0)$ and $(2;-6;4;0)$, the message is transmitted for the argument values $(0,1,2,3,4,5,6,7,8)$:

$$
0,0,0,f(3),f(4),f(5),g(6),g(7),g(8).
$$

This can occur both when $f$ is transmitted (with errors in the last $3$ positions) and when $g$ is transmitted (with errors in the values $f(3),f(4),f(5)$).

## Galois Fields

**Galois fields and Reed–Solomon**

* If polynomials are computed over ordinary integers, their values quickly become large.
* Reed–Solomon codes use polynomial coefficients and values from a finite field instead of integers, for example $\text{GF}(2^{8})$ (the Galois field with $2^{8} = 256$ elements).

[See the list of primitive polynomials](https://www.partow.net/programming/polynomials/index.html) to construct $\text{GF}(2^n)$ for powers up to $2^{32}$.

**Definition:** A *field* is a set $L$ with operations $+$ and $\ast$ that have the following properties:

* Closure: for any $a$ and $b$ both $a+b$ and $a \ast b$ are defined.
* Commutativity: $a + b = b + a$, $a \ast b = b \ast a$
* Associativity: $(a + b) + c = a + (b + c)$, $(a \ast b) \ast c = a \ast (b \ast c)$.
* Distributivity: $a \ast (b + c) = a \ast b + a \ast c$.
* Element $0$: there is an element $0$ such that $0 + a = a$ for any $a$.
* Element $1$: there is an element $1$ such that $1 \ast a = a$ for any $a$.
* Additive inverse: for each $a$ there is $-a$ such that $a + (-a) = 0$,
* Multiplicative inverse: if $a \neq 0$, there is $a^{-1}$ such that $a \ast a^{-1} = 1$.

### Infinite Fields

A field is any set of numbers or other objects in which all four arithmetic operations can be performed according to the usual rules.

* The set of rational numbers $\mathbb{Q}$ is a field (for each rational fraction $a/b$ there is an additive inverse $-a/b$ and a reciprocal $b/a$).
* The set of real numbers $\mathbb{R}$ is a field
* The set of complex numbers $\mathbb{C}$ (or also the set of only those complex numbers $a+bi$ with $a,b \in \mathbb{Q}$) is a field.
* The set of ratios of all segment lengths that can be constructed with compass and straightedge (the square root operation is added, but not roots of higher degrees).
* The set of all rational fractions $\frac{P(x)}{Q(x)}$ is a field.

**Claim:**

1. A finite field with $q$ elements exists if and only if $q$ can be written as a power $p^k$, where $p$ is prime and $k=1,2,3,\ldots$. This number is also called the *order*.
2. If ${\displaystyle q=p^{k}}$, then all fields of order $q$ are *isomorphic* -- their structure with respect to addition and multiplication is the same; only the names of the elements differ.

**Definition:** A finite field with $q = p^k$ elements is called a *Galois field*; it is denoted $\text{GF}(q)$ or $\text{GF}(p^k)$.

### GF for Primes

Addition and multiplication tables for $p = 2$.

| $a+b$ | 0 | 1 |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 1 | 0 |

| $a \ast b$ | 0 | 1 |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0 | 1 |


Addition and multiplication tables for $p = 3$.

| $a+b$ | 0 | 1 | 2 |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 2 |
| 1 | 1 | 2 | 0 |
| 2 | 2 | 0 | 1 |

| $a \ast b$ | 0 | 1 | 2 |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 2 |
| 2 | 0 | 2 | 1 |

### If $q$ Is Not Prime

* Consider $\text{GF}(8)$. We cannot use addition and multiplication modulo $8$, because $2 \cdot 0 = 2 \cdot 4 = 0$ and $2 \cdot 1 = 2 \cdot 5 = 2$.
* $2^{-1}$ would not exist, because the number $2 \neq 0$ merges results under multiplication $(\text{mod}\,8)$: it can happen that $a \neq b$ but $2a = 2b$.
* Remainders modulo a $q$ that is **not** prime can be studied (for example, keeping only those coprime to $q$), but they form only a multiplicative group, not a field.

*Important note:* Modular arithmetic $(\text{mod}\,q)$ forms a field if and only if $q$ is prime. If $q = p^k$ $(k > 1)$, $\text{GF}(q)$ has to be constructed in a different way.

* [Multiplicative groups modulo any number](https://en.wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n)
* [Finite fields](https://en.wikipedia.org/wiki/Finite_field)

**Example ($\text{GF}(8)$):**

* $p(x) = x^3 + x + 1$ is an *irreducible* polynomial; in other words, it cannot be factored so that the coefficients of the factors are elements of $\text{GF}(2)$.
* We form all possible "remainders" of division by the polynomial $p(x)$, and the coefficients of these polynomials are always added and multiplied modulo $2$.
* Then all $8$ possible remainders form the Galois field $\text{GF}(2^3)$: $0,\;1,\;x,\;x+1,\;x^2,\;x^2+1,\;x^2+x,\;x^2+x+1.$

**Addition and multiplication in $\text{GF}(8)$**

| $P(x)+Q(x)$ | $0$ | $1$ | $x$ | $x+1$ | $x^2$ | $x^2+1$ | $x^2+x$ | $x^2+x+1$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $0$ | $0$ | $1$ | $x$ | $x+1$ | $x^2$ | $x^2+1$ | $x^2+x$ | $x^2+x+1$ |
| $1$ | $1$ | $0$ | $x+1$ | $x$ | $x^2+1$ | $x^2$ | $x^2+x+1$ | $x^2+x$ |
| $x$ | $x$ | $x+1$ | $0$ | $1$ | $x^2+x$ | $x^2+x+1$ | $x^2$ | $x^2+1$ |
| $x+1$ | $x+1$ | $x$ | $1$ | $0$ | $x^2+x+1$ | $x^2+x$ | $x^2+1$ | $x^2$ |
| $x^2$ | $x^2$ | $x^2+1$ | $x^2+x$ | $x^2+x+1$ | $0$ | $1$ | $x$ | $x+1$ |
| $x^2+1$ | $x^2+1$ | $x^2$ | $x^2+x+1$ | $x^2+x$ | $1$ | $0$ | $x+1$ | $x$ |
| $x^2+x$ | $x^2+x$ | $x^2+x+1$ | $x^2$ | $x^2+1$ | $x$ | $x+1$ | $0$ | $1$ |
| $x^2+x+1$ | $x^2+x+1$ | $x^2+x$ | $x^2+1$ | $x^2$ | $x+1$ | $x$ | $1$ | $0$ |

| $P(x) \ast Q(x)$ | $0$ | $1$ | $x$ | $x+1$ | $x^2$ | $x^2+1$ | $x^2+x$ | $x^2+x+1$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ | $x$ | $x+1$ | $x^2$ | $x^2+1$ | $x^2+x$ | $x^2+x+1$ |
| $x$ | $0$ | $x$ | $x^2$ | $x^2+x$ | $x+1$ | $1$ | $x^2+x+1$ | $x^2+1$ |
| $x+1$ | $0$ | $x+1$ | $x^2+x$ | $x^2+1$ | $x^2+x+1$ | $x^2$ | $1$ | $x$ |
| $x^2$ | $0$ | $x^2$ | $x+1$ | $x^2+x+1$ | $x^2+x$ | $x$ | $x^2+1$ | $1$ |
| $x^2+1$ | $0$ | $x^2+1$ | $1$ | $x^2$ | $x$ | $x^2+x+1$ | $x+1$ | $x^2+x$ |
| $x^2+x$ | $0$ | $x^2+x$ | $x^2+x+1$ | $1$ | $x^2+1$ | $x+1$ | $x$ | $x^2$ |
| $x^2+x+1$ | $0$ | $x^2+x+1$ | $x^2+1$ | $x$ | $1$ | $x^2+x$ | $x^2$ | $x+1$ |

## Decoding Reed–Solomon Codes

**Finite fields in R-S codes**

In a Reed–Solomon code all numbers -- the message elements, the arguments and the values of the polynomial -- are elements of a finite field $\text{GF}(q)$, and all operations ($+$ and $\ast$) are performed in this field. The data is converted into a sequence of field elements and split into blocks of length $k$.

**Notation** (the same throughout the chapter and in the problems):

* $a_1, a_2, \ldots, a_k$ -- one message block; $f(x) = a_1 x^{k-1} + a_2 x^{k-2} + \ldots + a_{k-1} x + a_k$ -- the message polynomial (of degree at most $k-1$).
* $s$ values $f(0), f(1), \ldots, f(s-1)$ are sent. The arguments $0, 1, \ldots, s-1$ must be distinct field elements, so $k < s \leq q$.
* $r_0, r_1, \ldots, r_{s-1}$ -- the received values: $r_i$ is received in place of the value $f(i)$.
* $c$ -- the largest number of errors the code is guaranteed to correct: $c \leq (s-k)/2$, i.e., $s \geq k + 2c$.

The decoding algorithm and the number of correctable errors do not change, because the proof of the error-correcting capability uses nothing that fails in an arbitrary field. Finite fields, however, make it possible to avoid computations with large numbers.

**Examples with $\text{GF}(5)$:** In Problems 8.1-8.4 (see the section "Problems") we use the finite field

$$
\text{GF}(5) = \lbrace 0, 1, 2, 3, 4 \rbrace,
$$

where arithmetic is done modulo $5$. A message block has $k = 3$ numbers, so the polynomial is $f(x) = a_1 x^2 + a_2 x + a_3$, and $s = 5$ values $f(0), f(1), f(2), f(3), f(4)$ are sent. This code can recover up to $s - k = 2$ lost values (Problems 8.2 and 8.3) or correct $c = (5-3)/2 = 1$ error (Problem 8.4).

### Lagrange Interpolation

If there are no errors but some values are lost, any $k$ received values are enough: by the second corollary of the fundamental theorem of algebra there is exactly one polynomial of degree at most $k-1$ that passes through $k$ given points. It can be found with a system of equations (as in Problems 8.2 and 8.3) or by interpolation (works well for small $k$).

Suppose the correct values are known at $k$ distinct points $x_1, \ldots, x_k$ (these are some of the arguments $0, \ldots, s-1$):

$$
f(x_1)=w_1;\;\;f(x_2)=w_2;\;\;\ldots,\;\;f(x_k)=w_k.
$$

We define the *Lagrange basis polynomials*:

$$
L_i (x) = \frac{(x-x_1)\cdot\ldots\cdot(x-x_{i-1})\cdot(x-x_{i+1})\cdot\ldots\cdot(x-x_k)}
{(x_i-x_1)\cdot\ldots\cdot(x_i-x_{i-1})\cdot(x_i-x_{i+1})\cdot\ldots\cdot(x_i-x_k)}.
$$

(In a finite field, division means multiplication by the inverse element; the denominator is not $0$, because the points are distinct.) These polynomials have the following properties:

1. If $x=x_i$, then $L_i(x) = 1$, because the numerator and the denominator coincide.
2. If $x=x_j$ ($i \neq j$), then $L_i(x)=0$, because the numerator contains the factor $(x-x_j)=0$.

**Using interpolation for decoding**

The polynomial we are looking for is:

$$
f(x) = w_1 \cdot L_1(x) + w_2 \cdot L_2 (x) + \ldots + w_k \cdot L_k (x).
$$

Why does this polynomial give the right result? If $x = x_i$, then all $L_j(x_i)$ ($j \neq i$) are equal to $0$, and only $L_i(x_i) = 1$. So $f(x_i) = w_i \cdot L_i(x_i) = w_i$. Each $L_i$ has degree $k-1$, so the degree of $f$ also does not exceed $k-1$, and it is exactly the polynomial that was sent. If the only kind of error is that some values are lost, this approach is enough.

**Interpolation when other errors are possible**

If there are errors where another value is received in place of the correct one, things are harder:

* $k$ -- the number of message elements;
* $s$ -- the number of transmitted values: $f(0), f(1), \ldots, f(s-1)$;
* $c \leq (s-k)/2$ -- the maximum allowed number of errors;
* at least $s-c$ values are correct.

There are enough correct values, but we do not know which ones exactly are correct: if we chose $k$ points for interpolation that include even one error, we would get a wrong polynomial.

## Berlekamp–Welch Decoding

**The polynomial $Y(x)$ -- the error locator**

The Berlekamp–Welch algorithm is a Reed–Solomon decoding method used when not only data loss is possible, but also receiving wrong data in place of the correct data. We use the notation of the section "Decoding Reed–Solomon Codes" ($f$, $k$, $s$, $r_i$, $c$) and in addition:

* $e_1, e_2, \ldots, e_c$ -- the arguments at which the received value is wrong: $r_{e_j} \neq f(e_j)$ (unknown for now). If there are fewer than $c$ errors, the remaining $e_j$ can be chosen arbitrarily.
* At all other arguments $i$ the value is correct: $r_i = f(i)$.

We define the *error locator*:

$$
Y(x) = (x-e_1)(x-e_2) \ldots (x-e_c).
$$

It is a polynomial of degree $c$ with leading coefficient $1$ that is $0$ at all erroneous arguments.

**The polynomial $Z(x)$: the product of $Y(x)$ and $f(x)$**

We define the polynomial $Z(x)$ as the product of the error locator and the polynomial that was sent:

$$
Z(x) = Y(x) \cdot f(x).
$$

Its degree is $\deg Z = \deg Y + \deg f \leq c+(k-1) = k + c - 1$.

If we can find $Y$ and $Z$, the polynomial that was sent is obtained by division: $f(x) = Z(x) / Y(x)$. To find them, we use the fact that at each transmitted argument $i = 0, 1, \ldots, s-1$

$$
Z(i) = Y(i) \cdot r_i ,
$$

because

1. if $r_i = f(i)$ (a correct value), then $Z(i) = Y(i) \cdot f(i) = Y(i) \cdot r_i$;
2. if $r_i \neq f(i)$ (an error), then $i$ is one of the $e_j$, so $Y(i) = 0$ and $Z(i) = 0 = Y(i) \cdot r_i$.

The equations $Z(i) = Y(i) \cdot r_i$ do not contain the unknown $f$ -- they contain only the received values $r_i$.

**Finding $Y$, $Z$**

We write the unknown polynomials with unknown coefficients:

$$
Y(x) = x^c + y_{c-1} x^{c-1} + \ldots + y_1 x + y_0,
$$

$$
Z(x) = z_{k+c-1} x^{k+c-1} + z_{k+c-2} x^{k+c-2} + \ldots + z_1 x + z_0.
$$

Each received $r_i$ gives one equation:

$$
\left\{ \begin{array}{l}
Z(0) = Y(0) \cdot r_0\\
Z(1) = Y(1) \cdot r_1\\
\ldots\\
Z(s-1) = Y(s-1) \cdot r_{s-1}
\end{array} \right.
$$

After substituting the specific $i$ and $r_i$, each of them is a linear equation in the unknowns $z_0, \ldots, z_{k+c-1}$ and $y_0, \ldots, y_{c-1}$. This is a system of $s$ equations with $(k + c) + c = k + 2c$ unknowns; since $s \geq k + 2c$, there are enough equations. We solve it, find $Z(x)$ and $Y(x)$ and compute $f(x) = Z(x)/Y(x)$. A numerical example is in Problem 8.4.

(The leading coefficient of $Y$ is $1$ in order to exclude the trivial solution $Y = Z = 0$: without this condition the system would be homogeneous.)

**Questions about Berlekamp–Welch:**

1. Does the system of equations have a solution?
2. Could the system of equations have several solutions?
3. Can we find an algorithmic way to solve the system of equations?

**Answers:**

1. Yes: if there are at most $c$ errors, the true error locator $Y(x)$ and $Z(x) = Y(x) f(x)$ satisfy all the equations.
2. There may be several solutions (e.g., if there are fewer than $c$ errors, some $e_j$ can be chosen arbitrarily), but the ratio $Z(x)/Y(x)$ is the same for all solutions (see the claim below). So any solution gives the correct $f(x)$.
3. Yes; it is a system of linear equations that can be solved by Gaussian elimination (see below).

### Solvability of Berlekamp–Welch

**Claim:** Suppose $s \geq k + 2c$ and the polynomial pairs $(Y, Z)$ and $(Y', Z')$ both satisfy the following conditions:

1. $\deg Y \leq c$ and $Y \neq 0$,
2. $\deg Z \leq k + c - 1$,
3. for all $i = 0, 1, \ldots, s-1$: $Z(i) = Y(i) \cdot r_i$.

Then $Z(x)/Y(x) = Z'(x)/Y'(x)$.

**Proof:** For each $i$ we have $Z(i) = Y(i) \cdot r_i$ and $Z'(i) = Y'(i) \cdot r_i$. Hence

$$
Z(i) \cdot Y'(i) = Y(i) \cdot r_i \cdot Y'(i) = Y(i) \cdot Z'(i)
$$

(we do not divide by $r_i$, since it may be $0$). The degrees of the polynomials $Z \cdot Y'$ and $Z' \cdot Y$ do not exceed $(k + c - 1) + c = k + 2c - 1$, and they coincide at $s \geq k + 2c$ distinct points $i = 0, 1, \ldots, s-1$.

> *Note (the second corollary of the fundamental theorem of algebra):* if two polynomials have degrees at most $m$ and their values coincide at more than $m$ distinct points, then they are equal.

So $Z(x) \cdot Y'(x) = Z'(x) \cdot Y(x)$ as polynomials. Dividing both sides by $Y(x) \cdot Y'(x)$ (neither is the zero polynomial), we get

$$
Z(x) / Y(x) = Z'(x) / Y'(x).
$$

$\blacksquare$

### Solving Berlekamp–Welch Algorithmically

Substituting the polynomial coefficients into the equation $Z(i) = Y(i) \cdot r_i$ and moving the unknowns to the left-hand side gives

$$
z_0 + z_1 i + z_2 i^2 + \ldots + z_{k+c-1} i^{k+c-1} - r_i \left( y_0 + y_1 i + \ldots + y_{c-1} i^{c-1} \right) = r_i \, i^c .
$$

The coefficients of the unknowns are powers of the argument $i$ (and these powers multiplied by $-r_i$), and the right-hand side is a known number. All $s$ equations together form a linear system with $k + 2c$ unknowns, which is solved by Gaussian elimination: eliminating the variables one by one, with all operations performed in the field $\text{GF}(q)$ (division is multiplication by the inverse element). This takes $O(s^3)$ field operations. Then $Z(x)$ is divided by $Y(x)$:

* if the remainder is $0$, the quotient is the polynomial $f(x)$ that was sent, and the roots of $Y(x)$ show where the errors are;
* if the remainder is not $0$ (or the system has no solution), there were more than $c$ errors -- the decoder detects this but cannot correct them.

If there are more than $c$ errors, it can also happen that the division succeeds but the result is a different (wrong) codeword: the guarantee applies only to at most $c$ errors.

## LDPC Codes

*LDPC codes* (*low-density parity-check codes*, codes with a sparse parity-check matrix) are linear binary codes given by a *parity-check matrix* $H$. A bit string $c$ is a codeword if and only if

$$
H c = 0 \pmod{2},
$$

i.e., each row of the matrix $H$ is one parity check: the XOR of the bits that have a one in this row must be $0$. The Hamming code is like this too (see the section "Other Linear Codes" of the Hamming code lecture). The characteristic property of an LDPC code is that $H$ is *sparse*: a code may have thousands of bits, but each bit takes part in only a few (usually $3$--$6$) checks, and each check contains only a few dozen bits. Therefore the decoding work grows linearly with the code length.

**History.** LDPC codes were invented by Robert Gallager in his doctoral thesis at MIT in 1960 (the book appeared in 1963). Decoding them was too demanding for the computers of that time, and the codes were almost forgotten. In 1981 Michael Tanner introduced their representation as a bipartite graph. After the similarly decoded turbo codes appeared in 1993, LDPC codes were rediscovered in 1995-1996 by David MacKay and Radford Neal. It turned out that long LDPC codes with iterative soft decoding almost reach the Shannon limit -- the highest data rate that can be reliably achieved at all on a channel with a given noise level.

**Applications.** Satellite television DVB-S2 (2005), 10 Gigabit Ethernet over twisted pair (10GBASE-T), Wi-Fi (IEEE 802.11n/ac/ax), WiMAX, 5G mobile communication (data channels), digital television ATSC 3.0, space communication (CCSDS standards) and SSD controllers (error correction for NAND flash memory).

### Tanner Graph

An LDPC code is conveniently represented by a *Tanner graph* -- a bipartite graph with *bit nodes* (the columns of the matrix $H$) on one side and *check nodes* (the rows of the matrix $H$) on the other. Check $i$ and bit $j$ are joined by an edge if and only if $H_{i,j} = 1$. In a codeword, the XOR of the neighboring bits of each check is $0$.

For example, the Hamming code $[7,4,1]$, where the check bits are defined as

$$
\left\{
\begin{array}{l}
y_1 = x_1 \oplus x_2 \oplus x_3\\
y_2 = x_1 \oplus x_2 \oplus x_4\\
y_3 = x_1 \oplus x_3 \oplus x_4\\
\end{array} \right.
$$

corresponds to the following graph (here each check bit $y_i$ is at the same time the check "$y_i \oplus$ the connected $x_j = 0$"):

<img
  id="heminga_tanera_grafs"
  alt="Tanner graph of the Hamming code"
  src="{{ '/lectures/lossy_reed_solomon/figs/hamming-tanner.en.svg' | relative_url }}"
  style="width: 100%; max-width: 316px; border:none; background-color:#FFFFFF;"
/>

Below we use a small "toy" LDPC code with $n = 12$ bits and $6$ checks; each bit takes part in $2$ checks, and each check contains $4$ bits. The dimension of the code is $k = 12 - \operatorname{rank}(H) = 7$, and the minimum distance is $d = 3$ -- so, just like the Hamming code, it is guaranteed to correct only one error. (Real LDPC codes are much longer, but the algorithms are the same.)

<img
  id="ldpc_tanera_grafs"
  alt="Parity-check matrix and Tanner graph of an LDPC code"
  src="{{ '/lectures/lossy_reed_solomon/figs/ldpc-tanner.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

### Hard and Soft Information

The receiver does not get the bits themselves but a noisy signal. For example, bit $0$ is sent as $+1$, bit $1$ as $-1$, and $r_j = 0.9$ or $r_j = -0.2$ is received. A *hard decision* is only the sign: $r_j < 0 \Rightarrow 1$, otherwise $0$. *Soft information* is the number $r_j$ itself: the sign shows the most likely bit, and $\lvert r_j \rvert$ shows how reliable it is. (In practice the *log-likelihood ratio*, LLR, is used; for a channel with Gaussian noise it is proportional to $r_j$.) The value $-0.2$ means "rather $1$, but very unreliable", the value $-1.3$ means "almost certainly $1$".

### Decoding by Message Passing

LDPC decoders work iteratively: bit nodes and check nodes send each other messages along the edges of the Tanner graph about what the value of each bit should be. Each node sees only its neighbors, so each iteration takes only as much work as there are edges in the graph.

**Bit flipping** (R. Gallager) uses only the hard decisions $y$:

1. Compute the syndrome $s = H y \pmod 2$. If $s = 0$, then $y$ is a codeword -- stop.
2. For each bit, count in how many unsatisfied checks ($s_i = 1$) it takes part.
3. Flip ($0 \leftrightarrow 1$) the bits with the largest count and return to step 1.

**The min–sum decoder** uses the soft information $r_j$. It is a simplified variant of the *belief propagation* (*sum–product*) algorithm:

1. Each bit $j$ sends its current value (initially $r_j$) to each of its checks.
2. Each check $i$ replies to each of its bits $j$ what the value of this bit should be for the check to be satisfied, given that the other bits of the check are as they report. The sign is the product (XOR) of the signs of the other bits' values, and the reliability is the smallest of the other bits' reliabilities: a check is no more reliable than its weakest link.
3. Each bit adds its received value $r_j$ and the replies of all its checks. The sign of the sum is the new decision. If all decisions together satisfy all checks, stop; otherwise repeat from step 1 (a bit sends each check the sum without that check's own reply).

<img
  id="ldpc_atkodesana"
  alt="Hard and soft LDPC decoding"
  src="{{ '/lectures/lossy_reed_solomon/figs/ldpc-decoding.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

*The codeword $101000001000$ was sent; the noise flipped the sign of bits 1 and 3, but these values are very unreliable ($0.1$ and $0.3$). Bit flipping gets a wrong codeword, min–sum gets the correct one (see Problem 8.6). The figures and the course of the algorithms are printed by the Python script [ldpc_toy.py]({{ '/lectures/lossy_reed_solomon/figs/ldpc_toy.py' | relative_url }}).*

### Guaranteed and Soft Error Correction

* A **Reed–Solomon code** with algebraic decoding (e.g., the Berlekamp–Welch algorithm) is a *bounded-distance decoder*: it is **guaranteed** to correct any at most $(s-k)/2$ wrong symbols, no matter which ones they are. If there are more errors, it fails or finds a wrong codeword. The decoder uses only hard symbols -- each received value is equally "important".
* **Hard decoding** (bit flipping as well) looks for the codeword that is closest in Hamming distance. In the example, the closest codeword to the received $000000001000$ is $000000000000$ (distance $1$), while the sent $101000001000$ is at distance $2$ -- more than the code ($d = 3$) is guaranteed to correct. Therefore the hard decoder "corrects" the correctly received bit 9 and makes a mistake, and it cannot notice this itself: the result is a valid codeword.
* **Soft decoding** measures distance taking reliability into account: an error in an unreliable bit "costs" little, an error in a reliable bit costs a lot. In the example, the sent codeword agrees with the received values better than the all-zero word (see Problem 8.6), and min–sum finds it. Soft decoding has no simple guarantee like "any $t$ errors", and it can fail for some error patterns. Its quality is measured statistically -- by the error probability at a given noise level --, and for long LDPC codes it is much better than guaranteed correction: they correct most error patterns with many more errors than the minimum distance allows.
* A Reed–Solomon decoder can also partly use soft information: the least reliable symbols can be marked as *erased* (see Problems 8.2 and 8.3). An erasure whose position is known "costs" half as much as an error: with $s - k$ redundant values one can recover up to $s - k$ erasures, but only up to $(s-k)/2$ errors.

### Erasure Decoding

In some channels bits are not corrupted but lost: for example, if a data packet is received, its data is correct, but some packets are lost. Then an LDPC code is decoded with a simple "peeling" algorithm that uses only XOR:

1. Find a check in which exactly one bit is unknown.
2. This bit is the XOR of the other bits of the check (because the XOR of all bits of the check is $0$).
3. If there are still unknown bits, return to step 1.

This idea was the basis of the *Tornado codes* (M. Luby et al.) at the end of the 1990s -- early LDPC-type erasure codes that recover lost data in a similar amount as Reed–Solomon codes, but with much faster decoding. They gave rise to the *fountain codes* (LT, Raptor), which are used to distribute data to many receivers at once (e.g., in mobile television). An example is in Problem 8.5.

## Summary

* We encoded and decoded Hamming codes
* We defined Reed–Solomon codes
* We added and multiplied elements of finite fields
* We studied some decoding methods for Reed–Solomon codes, including the Berlekamp–Welch algorithm.
* We studied LDPC codes, Tanner graphs and their hard (bit flipping) and soft (min–sum) decoding.

## Problems

**Problem 8.1:** Encode the message $3, 2, 1$ with a Reed–Solomon code over the field $\text{GF}(5)$ ($k = 3$, $s = 5$).

**Answer:** The message polynomial is $f(x) = a_1 x^2 + a_2 x + a_3 = 3x^2 + 2x + 1$. We compute the values

$$
\begin{array}{rl}
f(0) & = 3\cdot{}0^2 + 2\cdot{}0 + 1 = 1,\\
f(1) & = (3\cdot{}1^2 + 2\cdot{}1 + 1)\;\text{mod}\;5 = 6\;\text{mod}\;5 = 1,\\
f(2) & = (3\cdot{}2^2 + 2\cdot{}2 + 1)\;\text{mod}\;5 = 17\;\text{mod}\;5 = 2,\\
f(3) & = (3\cdot{}3^2 + 2\cdot{}3 + 1)\;\text{mod}\;5 = 34\;\text{mod}\;5 = 4,\\
f(4) & = (3\cdot{}4^2 + 2\cdot{}4 + 1)\;\text{mod}\;5 = 57\;\text{mod}\;5 = 2.
\end{array}
$$

So the values $1, 1, 2, 4, 2$ are transmitted. $\square$

**Problem 8.2:** The received values are $r = (1, 1, \ast, 4, \ast)$, where $\ast$ is a lost value (all received values are correct). Recover the message $a_1, a_2, a_3$ (field $\text{GF}(5)$, $k = 3$, $s = 5$).

**Answer:** We know $f(0) = 1$, $f(1) = 1$, $f(3) = 4$. Since $3^2 = 9 \equiv 4\;(\text{mod}\,5)$, we get the system of equations (mod 5):

$$
\left\{ \begin{array}{rcl}
a_3 & \equiv & 1,\\
a_1 + a_2 + a_3 & \equiv & 1,\\
4 a_1 + 3 a_2 + a_3 & \equiv & 4.
\end{array} \right.
$$

Substituting $a_3 = 1$ into the second and third equations:

$$
\left\{ \begin{array}{rcl}
a_1 + a_2 & \equiv & 1 - 1 = 0,\\
4 a_1 + 3 a_2 & \equiv & 4 - 1 = 3.
\end{array} \right.
$$

Multiplying the first equation by $3$ and subtracting it from the second gives

$$
(4a_1 + 3a_2) - 3(a_1 + a_2) = a_1 \equiv 3 - 3\cdot{}0 = 3.
$$

From $a_1 + a_2 \equiv 0$ we get $a_2 \equiv -3 \equiv 2$. So $f(x) = 3x^2 + 2x + 1$, and the message is $3, 2, 1$ -- the same one we encoded in Problem 8.1. $\square$

**Problem 8.3:** The received values are $r = (2, 3, \ast, \ast, 2)$, where $\ast$ is a lost value (all received values are correct). Recover the message $a_1, a_2, a_3$ (field $\text{GF}(5)$, $k = 3$, $s = 5$).

**Answer:** We know $f(0) = 2$, $f(1) = 3$, $f(4) = 2$. Since $4^2 = 16 \equiv 1\;(\text{mod}\,5)$, we get the system (mod 5):

$$
\left\{ \begin{array}{rcl}
a_3 & \equiv & 2,\\
a_1 + a_2 + a_3 & \equiv & 3,\\
a_1 + 4 a_2 + a_3 & \equiv & 2.
\end{array} \right.
$$

Substituting $a_3 = 2$:

$$
\left\{ \begin{array}{rcl}
a_1 + a_2 & \equiv & 1,\\
a_1 + 4 a_2 & \equiv & 0.
\end{array} \right.
$$

Subtracting the first equation from the second: $3a_2 \equiv 0 - 1 \equiv 4$.

> *Note:* The solution is not the fraction $4/3$, because it is not a field element! We have to multiply by $3^{-1}$: since $3 \cdot 2 = 6 \equiv 1$, $3^{-1} = 2$, and $a_2 \equiv 4 \cdot 2 = 8 \equiv 3$. (Check: $3 \cdot 3 = 9 \equiv 4$.)
>
> There are algorithms for finding the inverse element without exhaustive search (the extended Euclidean algorithm). But $(\text{mod}\,5)$ has so few possible values that exhaustive search is faster.

From $a_1 + a_2 \equiv 1$ we get $a_1 \equiv 1 - 3 = -2 \equiv 3$. So $f(x) = 3x^2 + 3x + 2$, and the message is $3, 3, 2$. $\square$

**Problem 8.4 (Berlekamp–Welch decoding):** In Problem 8.1 we encoded the message $3, 2, 1$ as $1, 1, 2, 4, 2$. One value was corrupted during transmission, and the received values are

$$
r = (r_0, r_1, r_2, r_3, r_4) = (1, 1, 2, 0, 2).
$$

The decoder does not know which value is wrong. Use the Berlekamp–Welch method to find the position of the error and the message that was sent (field $\text{GF}(5)$).

**Answer:** Here $k = 3$, $s = 5$, so $c = (5 - 3)/2 = 1$ error can be corrected. We look for

$$
Y(x) = x + y_0, \qquad Z(x) = z_3 x^3 + z_2 x^2 + z_1 x + z_0
$$

($\deg Z \leq k + c - 1 = 3$). There are $k + 2c = 5$ unknowns, as many as there are equations. The equations $Z(i) = (i + y_0) \cdot r_i$ modulo 5, using $2^3 = 8 \equiv 3$, $3^2 \equiv 4$, $3^3 = 27 \equiv 2$, $4^2 \equiv 1$, $4^3 = 64 \equiv 4$:

$$
\begin{array}{lrcl}
i = 0: & z_0 & \equiv & 1 \cdot (0 + y_0) = y_0,\\
i = 1: & z_3 + z_2 + z_1 + z_0 & \equiv & 1 \cdot (1 + y_0),\\
i = 2: & 3 z_3 + 4 z_2 + 2 z_1 + z_0 & \equiv & 2 \cdot (2 + y_0) = 4 + 2 y_0,\\
i = 3: & 2 z_3 + 4 z_2 + 3 z_1 + z_0 & \equiv & 0 \cdot (3 + y_0) = 0,\\
i = 4: & 4 z_3 + z_2 + 4 z_1 + z_0 & \equiv & 2 \cdot (4 + y_0) = 3 + 2 y_0.
\end{array}
$$

We substitute $z_0 = y_0$ into the other equations:

$$
\left\{ \begin{array}{lrcl}
(1) & z_3 + z_2 + z_1 & \equiv & 1,\\
(2) & 3 z_3 + 4 z_2 + 2 z_1 - y_0 & \equiv & 4,\\
(3) & 2 z_3 + 4 z_2 + 3 z_1 + y_0 & \equiv & 0,\\
(4) & 4 z_3 + z_2 + 4 z_1 - y_0 & \equiv & 3.
\end{array} \right.
$$

From (1) we express $z_1 = 1 - z_3 - z_2$ and substitute:

$$
\left\{ \begin{array}{lrcl}
(2) & z_3 + 2 z_2 - y_0 & \equiv & 2,\\
(3) & -z_3 + z_2 + y_0 & \equiv & -3 \equiv 2,\\
(4) & -3 z_2 - y_0 & \equiv & -1.
\end{array} \right.
$$

Adding (2) and (3): $3 z_2 \equiv 4$, so $z_2 \equiv 4 \cdot 3^{-1} = 4 \cdot 2 = 8 \equiv 3$. From (4): $y_0 \equiv 1 - 3 z_2 = 1 - 9 \equiv 2$. From (3): $z_3 \equiv z_2 + y_0 - 2 = 3$. From (1): $z_1 \equiv 1 - 3 - 3 = -5 \equiv 0$. And $z_0 = y_0 = 2$.

So $Y(x) = x + 2$ and $Z(x) = 3x^3 + 3x^2 + 2$. The root of $Y(x)$ is $x = 3$ (because $3 + 2 = 5 \equiv 0$), so the value $r_3$ is wrong. The polynomial that was sent is obtained by dividing $Z(x)$ by $Y(x)$ (mod 5):

$$
\begin{array}{rcl}
3x^3 + 3x^2 + 0x + 2 - 3x^2 (x + 2) & = & -3x^2 + 0x + 2 \;\equiv\; 2x^2 + 0x + 2,\\
2x^2 + 0x + 2 - 2x (x + 2) & = & -4x + 2 \;\equiv\; x + 2,\\
x + 2 - 1 \cdot (x + 2) & = & 0.
\end{array}
$$

The quotient is $f(x) = 3x^2 + 2x + 1$ with no remainder, so the message is $3, 2, 1$, and the correct value at position $3$ is $f(3) = 4$. (Check: $Z(3) = 3 \cdot 27 + 3 \cdot 9 + 2 = 110 \equiv 0$ -- at the error position both $Z$ and $Y$ are $0$.) If the error position were known in advance (an erasure), the method of Problem 8.2 would suffice; the Berlekamp–Welch method finds this position itself as a root of the polynomial $Y(x)$. $\square$

**Problem 8.5:** A code is given by the Tanner graph in the figure: each check bit $y_i$ is the XOR of the message bits $x_j$ connected to it. Some bits were lost during transmission, but the received ones are correct (an erasure channel): $x_1 = 1$, $x_2 = 0$, $x_5 = 1$, $y_1 = 0$, $y_2 = 1$, $y_3 = 1$, $y_4 = 0$. Use erasure decoding (see "Erasure Decoding") to determine the lost message bits $x_3$, $x_4$, $x_6$.

<img
  id="dzesumu_uzdevuma_grafs"
  alt="Tanner graph for Problem 8.5"
  src="{{ '/lectures/lossy_reed_solomon/figs/erasure-problem.en.svg' | relative_url }}"
  style="width: 100%; max-width: 444px; border:none; background-color:#FFFFFF;"
/>

**Answer:** $(x_1,x_2,x_3,x_4,x_5,x_6) = (1,0,\textcolor{red}{x_3},\textcolor{red}{x_4},1,x_6)$, $(y_1,y_2,y_3,y_4) = (0,1,1,0)$.

* From $y_1 = x_1 \oplus x_2 \oplus x_3$ we get $0 = 1 \oplus 0 \oplus x_3$, which means that $x_3 = 1$.
* From $y_2 = x_1 \oplus x_4 \oplus x_5$ we get $1 = 1 \oplus x_4 \oplus 1$, which means that $x_4 = 1$.
* From $y_4 = x_3 \oplus x_5 \oplus x_6$ we get $0 = 1 \oplus 1 \oplus x_6$, which means that $x_6 = 0$.

Check: $y_3 = x_2 \oplus x_4 \oplus x_6 = 0 \oplus 1 \oplus 0 = 1$. $\square$

**Problem 8.6:** Consider the LDPC code with the parity-check matrix $H$ from the section "Tanner Graph" (checks $p_1, \ldots, p_6$; check $p_1$ contains bits $1, 2, 3, 4$, check $p_2$ -- $5, 6, 7, 8$, $p_3$ -- $1, 5, 9, 10$, $p_4$ -- $2, 6, 11, 12$, $p_5$ -- $3, 7, 9, 11$, $p_6$ -- $4, 8, 10, 12$). The codeword $c = 101000001000$ is sent (bit $0$ is sent as $+1$, bit $1$ as $-1$), and the received values are

$$
r = (0.1,\; 0.8,\; 0.3,\; 1.3,\; 0.8,\; 0.9,\; 0.6,\; 1.1,\; -1.3,\; 1.4,\; 0.9,\; 1.2).
$$

* **(a)** Check that $c$ is a codeword.
* **(b)** Find the hard decisions $y$ and the syndrome $H y$. What will the bit-flipping decoder do?
* **(c)** Perform one min–sum iteration: compute the messages of each check to its bits and the new value of each bit $L_j = r_j + (\text{the sum of its checks' messages})$. What are the new decisions?
* **(d)** Which codeword -- $c$ or $000000000000$ -- agrees better with the received values? Compare the correlation $\sum_j r_j \cdot (1 - 2 c_j)$ (the larger, the better).

**Answer:**

**(a)** The ones in the word $c$ are in bits $1, 3, 9$. Check $p_1$ contains bits $1$ and $3$, check $p_3$ -- bits $1$ and $9$, check $p_5$ -- bits $3$ and $9$, and the other checks contain no ones. Each check contains an even number of ones, so $H c = 0$.

**(b)** Only $r_9$ is negative, so $y = 000000001000$ (errors in bits 1 and 3). Bit 9 is in checks $p_3$ and $p_5$, so the syndrome is $(0, 0, 1, 0, 1, 0)$. The number of unsatisfied checks is $2$ for bit 9, $1$ for bits $1, 3, 5, 7, 10, 11$ and $0$ for the others. The decoder flips bit 9 and gets $000000000000$; the syndrome is $0$, so it stops. The result is a valid but wrong codeword (it differs from $c$ in three bits).

**(c)** A check sends its bit the product of the signs of the other three bits' values, multiplied by the smallest of their absolute values. For example, $p_3$ to bit $1$: the other bits $5, 9, 10$ report $0.8$, $-1.3$, $1.4$, so the sign is "$-$" and the reliability is $\min(0.8, 1.3, 1.4) = 0.8$, i.e., the message is $-0.8$ ("you must be $1$").

| Check | Bits | Messages to the bits |
| --- | --- | --- |
| $p_1$ | $1, 2, 3, 4$ | $0.3,\; 0.1,\; 0.1,\; 0.1$ |
| $p_2$ | $5, 6, 7, 8$ | $0.6,\; 0.6,\; 0.8,\; 0.6$ |
| $p_3$ | $1, 5, 9, 10$ | $-0.8,\; -0.1,\; 0.1,\; -0.1$ |
| $p_4$ | $2, 6, 11, 12$ | $0.9,\; 0.8,\; 0.8,\; 0.8$ |
| $p_5$ | $3, 7, 9, 11$ | $-0.6,\; -0.3,\; 0.3,\; -0.3$ |
| $p_6$ | $4, 8, 10, 12$ | $1.1,\; 1.2,\; 1.1,\; 1.1$ |

The new values: $L_1 = 0.1 + 0.3 - 0.8 = -0.4$, $L_3 = 0.3 + 0.1 - 0.6 = -0.2$, $L_9 = -1.3 + 0.1 + 0.3 = -0.9$; the other bits stay positive: $L = (-0.4,\; 1.8,\; -0.2,\; 2.5,\; 1.3,\; 2.3,\; 1.1,\; 2.9,\; -0.9,\; 2.4,\; 1.4,\; 3.1)$. The decisions are $101000001000 = c$, all checks are satisfied, so decoding stops after one iteration with the correct result. Bits 1 and 3 are corrected by the checks $p_3$ and $p_5$, which contain the reliable bit 9; the check $p_1$ hardly affects them, because both of them are unreliable in it.

**(d)** For the all-zero word the correlation is the sum of all $r_j$, which is $8.1$. For the word $c$ the signs of bits $1, 3, 9$ must be flipped: $8.1 - 2 \cdot 0.1 - 2 \cdot 0.3 + 2 \cdot 1.3 = 9.9$. So $c$ agrees better (it is also the best of all $128$ codewords -- the *maximum likelihood* answer), although in Hamming distance the all-zero word is closer to the hard decisions $y$. $\square$


## References

* [Tanner graphs](https://en.wikipedia.org/wiki/Tanner_graph).
* [Low-density parity-check code](https://en.wikipedia.org/wiki/Low-density_parity-check_code).
* R. G. Gallager, *Low-density parity-check codes*, IRE Transactions on Information Theory, 8(1), 1962, 21--28.
* D. J. C. MacKay, R. M. Neal, *Near Shannon limit performance of low density parity check codes*, Electronics Letters, 32(18), 1996.
* T. Richardson, R. Urbanke, *Modern Coding Theory*, Cambridge University Press, 2008.
