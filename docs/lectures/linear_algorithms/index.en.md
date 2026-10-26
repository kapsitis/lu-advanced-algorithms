---
layout: default
title: "Linear Programming Algorithms"
lang: en
permalink: /lectures/linear_algorithms/en/
---
# 10. Linear Programming Algorithms



## The Simplex Algorithm

The basic idea of the simplex algorithm:

1. Start at some corner $v$ of the feasible region.
2. If corner $v$ has an adjacent corner $u$ where the value of the objective function
   $c_1x_1+\ldots+c_nx_n$ is larger, replace $v$ with $u$ and repeat this step.

If no adjacent corner gives a larger value, the objective function has already reached its maximum
over the whole feasible region (since the region is convex and the objective function is linear,
a local maximum is also a global one).


### Converting the Problem to Standard Form

The *standard form* of a problem is a formulation in which all constraints are equalities,
except the non-negativity constraints $x_i \geq 0$.
An inequality $\leq$ is turned into an equality by introducing a slack variable
(*slack variable*) that is non-negative. For example:

$$
x_1-2x_2 \leq 4\;\; \Leftrightarrow \;\; x_1-2x_2+x_3=4,\;x_3 \geq 0.
$$

Each inequality needs its own slack variable.

**Example:** $\textcolor{blue}{\max \left( 2x_1 + 3x_2 \right)}$, where

$$
\left\{ \begin{array}{l}
x_1-2x_2 \leq 4,\\
x_1+x_2 \leq 18,\\
x_2 \leq 10,\\
x_1,x_2 \geq 0.
\end{array} \right.
$$

In standard form: $\textcolor{blue}{\max \left( 2x_1 + 3x_2 \right)}$, where

$$
\left\{ \begin{array}{l}
x_1-2x_2+x_3=4,\\
x_1+x_2+x_4=18,\\
x_2+x_5=10,\\
x_1,x_2,x_3,x_4,x_5 \geq 0.
\end{array} \right.
$$

### The Feasible Region

![Feasible region](figs/feasible-region.png)

Each edge of the feasible region lies on a line where one of the variables
$x_1,\ldots,x_5$ is $0$ (for example, on the line $x_2+x_5=10$ we have $x_5=0$).
A corner is the intersection of two edges, i.e., a point where two of the variables are equal to $0$:

![Polygon of the feasible region with its corners](figs/lp-polygon.png)

In higher dimensions it is similar. If the original problem has $k$ variables and $m$
inequalities, then the standard form has $n = k+m$ variables, and a corner is a point where
$k$ hyperplanes intersect, i.e., $k$ of the $n$ variables are equal to $0$.

### The Simplex Tableau

The steps of the simplex algorithm are conveniently written in a tableau. The rows of the tableau
contain the coefficients of the equalities and the right-hand sides $b_i$, and the last row contains
the coefficients of the objective function.
The $b_i$ cell of the last row holds the current value of the objective function with a minus sign
(initially it is $0$).

<table>
<thead>
<tr><th style="background-color:#e6e6e6;">$x_1$</th><th style="background-color:#e6e6e6;">$x_2$</th><th>$x_3$</th><th>$x_4$</th><th>$x_5$</th><th>$b_i$</th><th>Corresponding expression</th></tr>
</thead>
<tbody>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$-2$</td><td>$1$</td><td>$0$</td><td>$0$</td><td>$4$</td><td>$x_1 - 2x_2 + x_3 = 4$</td></tr>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$1$</td><td>$0$</td><td>$1$</td><td>$0$</td><td>$18$</td><td>$x_1 + x_2 + x_4 = 18$</td></tr>
<tr><td style="background-color:#e6e6e6;">$0$</td><td style="background-color:#e6e6e6;">$1$</td><td>$0$</td><td>$0$</td><td>$1$</td><td>$10$</td><td>$x_2 + x_5 = 10$</td></tr>
<tr><td style="background-color:#e6e6e6;"><b>2</b></td><td style="background-color:#e6e6e6;"><b>3</b></td><td><b>0</b></td><td><b>0</b></td><td><b>0</b></td><td><b>0</b></td><td>$z = 2x_1+3x_2$</td></tr>
</tbody>
</table>

The tableau corresponds to the corner $(x_1,x_2) = (0,0)$:

* The gray columns are the *non-basic variables* (*tight variables*);
  at the corner they are equal to $0$.
* The other columns are the *basic variables* (*loose variables*). Their columns form the
  identity matrix, so their values can be read from the $b_i$ column: $x_3 = 4$, $x_4 = 18$, $x_5 = 10$.
  The last row has zeros under the basic variables, so the objective function is expressed only
  in terms of the non-basic variables.

We call such a tableau *canonical*. In a step of the simplex algorithm one non-basic variable becomes
basic and one basic variable becomes non-basic; then the tableau is brought into canonical form again.

> *Note:* At the starting corner $(x_1, x_2) = (0,0)$ the non-basic variables are the original variables
> of the problem $x_1, x_2$, and the basic variables are the slack variables $x_3,x_4,x_5$. In the following steps
> non-basic and basic variables swap places; they depend on the corner where we are.

### The First Step of the Simplex Algorithm

A step of the simplex algorithm consists of three parts:

1. **Entering variable.** Choose a non-basic variable with a positive coefficient in the last row;
   increasing it increases the objective function. Usually the largest coefficient is taken (*Dantzig's rule*), but
   any positive one will do. If there are no positive coefficients, the corner is optimal.
2. **Leaving variable.** Increase the chosen variable by $d$, keeping the other non-basic variables at $0$,
   and change the basic variables so that the equalities still hold. Stop increasing when some
   basic variable becomes $0$; it becomes a non-basic variable.
3. **Pivoting.** Swap the columns of the two variables and restore the canonical
   form with row operations.

In the objective function $2x_1+3x_2$ the largest coefficient belongs to $x_2$, so we increase $x_2$
(increasing $x_1$ would also work). If $x_2 = d$ and $x_1 = 0$, then from the equalities:

$$
x_3 = 4 + 2d \geq 0,\quad x_4 = 18 - d \geq 0,\quad x_5 = 10 - d \geq 0.
$$

The first condition holds for any $d \geq 0$, the second requires $d \leq 18$, the third $d \leq 10$.
So the largest possible value is $d = 10$ (the smallest of the ratios $b_i/a_{i2}$ over rows with
$a_{i2} > 0$), and then $x_5 = 0$. We move from the corner $x_1 = x_2 = 0$ to the corner $x_1 = x_5 = 0$:
$x_2$ becomes basic, $x_5$ becomes non-basic. We swap the columns $x_2$ and $x_5$.
The pivot element is the coefficient of $x_2$ in row 3 (yellow cell); the blue cells
must be made zero:

<table>
<thead>
<tr><th style="background-color:#e6e6e6;">$x_1$</th><th style="background-color:#e6e6e6;">$x_5$</th><th>$x_3$</th><th>$x_4$</th><th>$x_2$</th><th>$b_i$</th><th>Corresponding expression</th></tr>
</thead>
<tbody>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$0$</td><td>$1$</td><td>$0$</td><td style="background-color:#b3ccff;">$-2$</td><td>$4$</td><td>$x_1 + x_3 - 2x_2 = 4$</td></tr>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$0$</td><td>$0$</td><td>$1$</td><td style="background-color:#b3ccff;">$1$</td><td>$18$</td><td>$x_1 + x_4 + x_2 = 18$</td></tr>
<tr><td style="background-color:#e6e6e6;">$0$</td><td style="background-color:#e6e6e6;">$1$</td><td>$0$</td><td>$0$</td><td style="background-color:#ffe08a;">$1$</td><td>$10$</td><td>$x_5 + x_2 = 10$</td></tr>
<tr><td style="background-color:#e6e6e6;"><b>2</b></td><td style="background-color:#e6e6e6;"><b>0</b></td><td><b>0</b></td><td><b>0</b></td><td style="background-color:#b3ccff;"><b>3</b></td><td><b>0</b></td><td>$z = 2x_1+3x_2$</td></tr>
</tbody>
</table>

Row operations (the pivot element is already $1$, so row 3 is not divided):

* Add twice row 3 to row 1: $(x_1 + x_3 - 2x_2) + 2(x_5 + x_2) = 4 + 2 \cdot 10$.
* Subtract row 3 from row 2: $(x_1 + x_4 + x_2) - (x_5 + x_2) = 18 - 10$.
* Subtract three times row 3 from the last row: $z = 2x_1 + 3(10 - x_5) = 30 + 2x_1 - 3x_5$.

<table>
<thead>
<tr><th style="background-color:#e6e6e6;">$x_1$</th><th style="background-color:#e6e6e6;">$x_5$</th><th>$x_3$</th><th>$x_4$</th><th>$x_2$</th><th>$b_i$</th><th>Corresponding expression</th></tr>
</thead>
<tbody>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$2$</td><td>$1$</td><td>$0$</td><td>$0$</td><td>$24$</td><td>$x_1 + 2x_5 + x_3 = 24$</td></tr>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$-1$</td><td>$0$</td><td>$1$</td><td>$0$</td><td>$8$</td><td>$x_1 - x_5 + x_4 = 8$</td></tr>
<tr><td style="background-color:#e6e6e6;">$0$</td><td style="background-color:#e6e6e6;">$1$</td><td>$0$</td><td>$0$</td><td>$1$</td><td>$10$</td><td>$x_5 + x_2 = 10$</td></tr>
<tr><td style="background-color:#e6e6e6;"><b>2</b></td><td style="background-color:#e6e6e6;"><b>-3</b></td><td><b>0</b></td><td><b>0</b></td><td><b>0</b></td><td><b>-30</b></td><td>$z = 30 + 2x_1-3x_5$</td></tr>
</tbody>
</table>

The tableau is canonical again. It corresponds to the corner $(x_1, x_2) = (0, 10)$, where
$x_3 = 24$, $x_4 = 8$, $x_2 = 10$ and $z = 30$.

### The Second Step of the Simplex Algorithm

In the last row the only positive coefficient belongs to $x_1$ (increasing $x_5$ would decrease
the objective function), so we increase $x_1$. If $x_1 = d$ and $x_5 = 0$, then

$$
x_3 = 24 - d \geq 0,\quad x_4 = 8 - d \geq 0,\quad x_2 = 10 \geq 0.
$$

The largest possible value is $d = \min(24/1,\, 8/1) = 8$, and then $x_4 = 0$. We swap
the columns $x_1$ and $x_4$; the pivot element is the coefficient of $x_1$ in row 2:

<table>
<thead>
<tr><th style="background-color:#e6e6e6;">$x_4$</th><th style="background-color:#e6e6e6;">$x_5$</th><th>$x_3$</th><th>$x_1$</th><th>$x_2$</th><th>$b_i$</th><th>Corresponding expression</th></tr>
</thead>
<tbody>
<tr><td style="background-color:#e6e6e6;">$0$</td><td style="background-color:#e6e6e6;">$2$</td><td>$1$</td><td style="background-color:#b3ccff;">$1$</td><td>$0$</td><td>$24$</td><td>$x_1 + 2x_5 + x_3 = 24$</td></tr>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$-1$</td><td>$0$</td><td style="background-color:#ffe08a;">$1$</td><td>$0$</td><td>$8$</td><td>$x_1 - x_5 + x_4 = 8$</td></tr>
<tr><td style="background-color:#e6e6e6;">$0$</td><td style="background-color:#e6e6e6;">$1$</td><td>$0$</td><td>$0$</td><td>$1$</td><td>$10$</td><td>$x_5 + x_2 = 10$</td></tr>
<tr><td style="background-color:#e6e6e6;"><b>0</b></td><td style="background-color:#e6e6e6;"><b>-3</b></td><td><b>0</b></td><td style="background-color:#b3ccff;"><b>2</b></td><td><b>0</b></td><td><b>-30</b></td><td>$z = 30 + 2x_1-3x_5$</td></tr>
</tbody>
</table>

Row operations:

* Subtract row 2 from row 1: $(x_1 + 2x_5 + x_3) - (x_1 - x_5 + x_4) = 24 - 8$.
* Subtract twice row 2 from the last row: $z = 30 + 2(8 + x_5 - x_4) - 3x_5 = 46 - 2x_4 - x_5$.

<table>
<thead>
<tr><th style="background-color:#e6e6e6;">$x_4$</th><th style="background-color:#e6e6e6;">$x_5$</th><th>$x_3$</th><th>$x_1$</th><th>$x_2$</th><th>$b_i$</th><th>Corresponding expression</th></tr>
</thead>
<tbody>
<tr><td style="background-color:#e6e6e6;">$-1$</td><td style="background-color:#e6e6e6;">$3$</td><td>$1$</td><td>$0$</td><td>$0$</td><td>$16$</td><td>$-x_4 + 3x_5 + x_3 = 16$</td></tr>
<tr><td style="background-color:#e6e6e6;">$1$</td><td style="background-color:#e6e6e6;">$-1$</td><td>$0$</td><td>$1$</td><td>$0$</td><td>$8$</td><td>$x_4 - x_5 + x_1 = 8$</td></tr>
<tr><td style="background-color:#e6e6e6;">$0$</td><td style="background-color:#e6e6e6;">$1$</td><td>$0$</td><td>$0$</td><td>$1$</td><td>$10$</td><td>$x_5 + x_2 = 10$</td></tr>
<tr><td style="background-color:#e6e6e6;"><b>-2</b></td><td style="background-color:#e6e6e6;"><b>-1</b></td><td><b>0</b></td><td><b>0</b></td><td><b>0</b></td><td><b>-46</b></td><td>$z = 46 - 2x_4 - x_5$</td></tr>
</tbody>
</table>

All coefficients of the non-basic variables in the last row are negative. Since $x_4, x_5 \geq 0$,
$z = 46 - 2x_4 - x_5$ implies $z \leq 46$ over the whole feasible region. The maximum is reached.

### Reading Off the Solution

In the last tableau the non-basic variables are $x_4 = x_5 = 0$, and the values of the basic variables are read from the $b_i$ column:

$$
x_3 = 16,\quad x_1 = 8,\quad x_2 = 10.
$$

So $(x_1,x_2) = (8, 10)$ and $(x_3,x_4,x_5) = (16,0,0)$. Check in the original constraints:
$8 - 2 \cdot 10 + 16 = 4$, $8 + 10 + 0 = 18$, $10 + 0 = 10$. The value of the objective function:

$$
2x_1 + 3x_2 = 2 \cdot 8 + 3 \cdot 10 = 46,
$$

which matches the $-46$ written in the $b_i$ column of the last tableau (with the opposite sign). So the largest value of $2x_1 + 3x_2$ under the given
constraints is $46$, and it is reached at the point $(x_1, x_2) = (8, 10)$. The simplex algorithm went along the
corners of the polygon $(0,0) \to (0,10) \to (8,10)$.

## The Simplex Algorithm in General Form

**An LP problem in standard form:** find $\textcolor{blue}{\max(c_1x_1 + \ldots + c_nx_n)}$ subject to
$k$ equalities and $n$ non-negativity constraints:

$$
\left\{
\begin{array}{l}
a_{11}x_1 + a_{12}x_2 + \ldots + a_{1n}x_n = b_1\\
\ldots\\
a_{k1}x_1 + a_{k2}x_2 + \ldots + a_{kn}x_n = b_k\\
x_1,x_2,\ldots,x_n \geq 0
\end{array} \right.
$$

In matrix notation: $\max \mathbf{c}^T\mathbf{x}$, where $A\mathbf{x} = \mathbf{b}$, $\mathbf{x} \geq \mathbf{0}$,
and $A$ is a $k \times n$ matrix ($k < n$). We assume that the equalities are linearly independent
(otherwise the redundant ones can be dropped).

The *simplex tableau* is the $(k+1) \times (n+1)$ matrix whose
first $k$ rows contain the coefficients and right-hand sides of the equalities, and whose last row contains
the coefficients of the objective function and the current value of the objective function with a minus sign:

| $x_1$ | $x_2$ | $\ldots$ | $x_n$ | $b_i$ |
| --- | --- | --- | --- | --- |
| $a_{11}$ | $a_{12}$ | $\ldots$ | $a_{1n}$ | $b_1$ |
| $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ |
| $a_{k1}$ | $a_{k2}$ | $\ldots$ | $a_{kn}$ | $b_k$ |
| $c_1$ | $c_2$ | $\ldots$ | $c_n$ | $0$ |

Row operations (multiplying a row by a number $\neq 0$ and adding a multiple of another row)
change neither the feasible region nor the objective function; only the notation changes.

### The Canonical Tableau

The simplex algorithm is always at some corner. The corner corresponds to $k$ *basic variables*; the other
$n-k$ are *non-basic variables*, and at the corner they are equal to $0$. Let us renumber the variables so that
the basic variables come last: $x_{n-k+1},\ldots,x_n$. The tableau is *canonical* if

* the columns of the basic variables form the identity matrix;
* the last row has zeros under the basic variables;
* the right-hand sides are non-negative: $\bar{b}_1,\ldots,\bar{b}_k \geq 0$.

| $x_1$ | $\ldots$ | $x_{n-k}$ | $x_{n-k+1}$ | $x_{n-k+2}$ | $\ldots$ | $x_n$ | $b_i$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $\bar{a}_{11}$ | $\ldots$ | $\bar{a}_{1,n-k}$ | $1$ | $0$ | $\ldots$ | $0$ | $\bar{b}_1$ |
| $\bar{a}_{21}$ | $\ldots$ | $\bar{a}_{2,n-k}$ | $0$ | $1$ | $\ldots$ | $0$ | $\bar{b}_2$ |
| $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ | $\ldots$ |
| $\bar{a}_{k1}$ | $\ldots$ | $\bar{a}_{k,n-k}$ | $0$ | $0$ | $\ldots$ | $1$ | $\bar{b}_k$ |
| $\bar{c}_1$ | $\ldots$ | $\bar{c}_{n-k}$ | $0$ | $0$ | $\ldots$ | $0$ | $-z_0$ |

From the canonical tableau one can read off directly:

* **the corner:** $x_1 = \ldots = x_{n-k} = 0$ (non-basic) and $x_{n-k+i} = \bar{b}_i$ (basic);
* **the objective function**, expressed in terms of the non-basic variables:
  $z = z_0 + \bar{c}_1x_1 + \ldots + \bar{c}_{n-k}x_{n-k}$; at the corner its value is $z_0$.

The coefficients $\bar{c}_j$ are called *reduced costs*: they show how much
$z$ changes if the non-basic variable $x_j$ is increased by $1$.

### A Step of the Simplex Algorithm

In the general case one step on a canonical tableau looks like this:

1. **Optimality check.** If all $\bar{c}_j \leq 0$, then $z \leq z_0$ over the whole feasible
   region, and the current corner is optimal.
2. **Entering variable.** Choose a non-basic variable $x_j$ with $\bar{c}_j > 0$ (for example, the one with
   the largest $\bar{c}_j$).
3. **Leaving variable.** If $x_j = d$, then the value of the $i$-th basic variable is $\bar{b}_i - \bar{a}_{ij}d$.
   Rows with $\bar{a}_{ij} \leq 0$ do not limit the increase. If all $\bar{a}_{ij} \leq 0$, then
   $x_j$ can be increased indefinitely, and the objective function is unbounded. Otherwise choose the row $r$
   with the smallest ratio (*minimum ratio test*):
   $$
   d = \frac{\bar{b}_r}{\bar{a}_{rj}} = \min_{i:\;\bar{a}_{ij} > 0} \frac{\bar{b}_i}{\bar{a}_{ij}}.
   $$
   The basic variable of row $r$ becomes $0$ and leaves the set of basic variables.
4. **Pivoting.** Divide row $r$ by the pivot element $\bar{a}_{rj}$, then from
   every other row (including the last one) subtract the multiple of row $r$ that makes column $j$
   zero. The tableau is canonical again, $x_j$ is a basic variable, and $z_0$ increases by
   $\bar{c}_j d \geq 0$.

In pseudocode (tableau $T$, set $B$ of the indices of the basic variables):

$\textsf{Simplex}(T, B)$
1. **while** the last row has $\bar{c}_j > 0$ for some $j \notin B$ $\quad$ *// otherwise the corner is optimal*
2. $\quad$ choose $j \notin B$ with $\bar{c}_j > 0$ $\quad$ *// entering variable*
3. $\quad$ **if** all $\bar{a}_{ij} \leq 0$
4. $\quad\quad$ **return** "unbounded"
5. $\quad$ choose $r$ with the smallest $\bar{b}_r / \bar{a}_{rj}$ among $\bar{a}_{rj} > 0$ $\quad$ *// leaving variable*
6. $\quad \textsf{Pivot}(T, r, j)$ $\quad$ *// row operations, unit vector in column $j$*
7. $\quad$ in $B$ replace the basic variable of row $r$ with $j$
8. **return** the corner $x_{B} = \bar{\mathbf{b}}$, all other $x_j = 0$

In the previous example both steps went exactly like this; there the columns were also swapped so that
the basic variables always stayed in the last columns.

### Starting Corner and Degeneracy

* **Starting corner.** If all original constraints are $\leq$ with $b_i \geq 0$, then
  the very first tableau is already canonical: the basic variables are the slack variables, and the corner is $\mathbf{x} = \mathbf{0}$
  (as in the example). Otherwise the starting corner is found with the *two-phase method*: first the simplex algorithm
  minimizes the sum of artificial auxiliary variables; if it reaches $0$, a feasible corner has been found, otherwise
  the problem has no feasible solutions.
* **Degeneracy.** If some $\bar{b}_r = 0$, a step can happen with $d = 0$: the set of
  basic variables changes, but neither the corner nor $z_0$ does. With an unlucky choice of entering variables
  the algorithm can cycle back to the same tableau. Cycling is prevented, for example, by
  *Bland's rule*: as the entering and leaving variable take the eligible one with the smallest index.
  Then the simplex algorithm always terminates, because the number of corners is finite (at most
  $\binom{n}{k}$).

## Algorithms for Solving LP

* (Real-valued) LP is the first step towards solving integer problems (*Integer Programming, IP*) and mixed integer problems (*Mixed Integer Linear Programs, MIP*).
* How to choose an optimal combination (raw materials, stock portfolios), how best to allocate some resource.
* Maximizing a flow in a graph (see the previous lecture).

Integer unknowns (*Integer Programming*) model yes/no decisions better (values 0 and 1), but such problems are harder to solve.

The following algorithms are known:

* The simplex algorithm (Kantorovich, 1939; Dantzig, 1947).
* The ellipsoid algorithm (Khachian, 1979); the first provably efficient algorithm.
* Interior point methods.
  - The projective method (Karmarkar, 1984).
  - The affine method (Dikin, 1967).
  - Log Barrier Method.
  - The primal-dual path-following method (Kojima, Mizuno, Yoshise, 1989; Mehrotra, 1992).

The simplex algorithm is usually efficient, but specially constructed examples can be very slow. Matrices can have about 100 thousand rows/columns; about a million numbers in these matrices are nonzero.


### A Counterexample for the Simplex Algorithm

Maximize an expression with $D$ variables: $2^{D-1}x_1+2^{D-2}x_2+ \dots + 2x_{D-1}+x_D$

The inequalities are:

$$
\left\{ \begin{array}{l}
x_1 \leq 5\\
4x_1+x_2 \leq 25\\
8x_1+4x_2+x_3 \leq 125 \\
\vdots\\
2^Dx_1+2^{D-1}x_2+ \dots +4x_{D-1}+x_D \leq 5^D \\
x_1 \geq 0, \, \, \dots , \, \, x_D \geq 0.
\end{array} \right.
$$

**The Klee–Minty squashed hypercube:**

* A deterministic simplex algorithm visits all $2^D$ vertices of the hypercube before it finds the optimal solution $x_D = 5^D$ (all others are zero).
* If the simplex algorithm chooses the next step with a randomized (rather than deterministic) method, polynomial time suffices.
* The example is unstable; real-number arithmetic and rounding also usually make the algorithm terminate after polynomially many steps.

[Performance of real LP algorithms](https://cstheory.stackexchange.com/questions/2373/complexity-of-the-simplex-algorithm)

### The Ellipsoid Algorithm

This algorithm was invented by Khachiyan in 1979. The ellipsoid algorithm is known as 
the first linear programming algorithm that was proven to find a solution 
in polynomial time ($O(n^4L)$), where $n$ is the number of dimensions and $L$ is the number of bits of precision 
to which the solution must be found.

Although its running time is polynomial in theory, in practice the algorithm is slow and is not used. 
Therefore in this course we restrict ourselves to a short description of this algorithm.

**Summary of the ellipsoid algorithm:** Because of the duality theorems (and the reduction to primal+dual), 
an algorithm that finds a point where all constraints hold is enough. Such a point is sought as follows:

Start with an ellipsoid $E_0$ that certainly contains the LP feasible region. Perform the following steps 
until the required precision is reached:

1. Take the center $c_i$ of the previous ellipsoid $E_i$.
2. If $c_i$ does not satisfy all LP constraints, find the constraint $a_k$ that is violated 
   the most.
3. The plane consisting of all points where the expression of constraint $a_k$ has the same value 
   $c$ (where $c$ is between the value at the point $c_i$ and the feasible values of the expression) 
   splits the space into two parts. Let $R_1$ denote the part containing $c_i$, and $R_2$ the 
   part containing the feasible region.
4. Construct a new ellipsoid $E_{i+1}$ such that $E_i \cap R_2 \subseteq E_{i+1}$.

![The ellipsoid algorithm](figs/ellipsoid-algorithm.png)

We look for a point in a convex region of $n$-dimensional space. Khachiyan's construction 
(*barycentric coordinate descent*) builds a sequence of ellipsoids for which

$$
\frac{\text{Volume}(E_{k+1})}{\text{Volume}(E_{k})} = e^{-\frac{1}{2n+1}}
$$

i.e., the ratio of volumes is strictly less than $1$ (and depends only on the number of dimensions $n$).

Cf. [Ellipsoid algorithm lecture 6-854J.L12](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-854j-advanced-algorithms-fall-2008/lecture-notes/lec12.pdf).

### Overview of Interior Point Methods

Common ideas of interior point methods:

* The region where the solution is sought can be replaced by a **barrier function** that grows rapidly when approaching the boundary of the feasible region.
* Unlike the simplex method, which searches through the corners of the feasible region, interior point methods look for better and better solutions inside the feasible region. The steps of the algorithm approach a corner only at the end of the algorithm.

Iterations in the interior are usually implemented in one of the following two ways:

**Interior point methods, type 1:** Modify the objective function so that its value gets worse near the edges of the feasible region. For example, the objective function $\max (c_1 x_1 + c_2 x_2 + \ldots + c_n x_n)$ can be replaced by

$$
\max \left( c_1 x_1 + c_2 x_2 + \ldots + c_n x_n + \ln x_1 + \ldots + \ln x_n \right).
$$

Then, when approaching the planes $x_i=0$ that bound the feasible region, $\ln x_i$ tends to $-\infty$, and the objective function also tends to $-\infty$.

**Interior point methods, type 2:** Introduce additional constraints that keep the iterates away from the edges of the feasible region. With each step the additional constraints are weakened, allowing the algorithm to approach the corner where the original objective function has its maximum value. The goal is for the algorithm to first find the optimal value inside the feasible region and then to arrive at the optimal corner.

### The Affine Scaling Method

This method was published by I.Dikin in 1967, but it became widely known only after 1984, 
when, following Karmarkar's projective method, several authors (E.Barnes; R.Vanderbei, M.Meketon, B.Freedman) 
rediscovered it as a simpler alternative. It is the simplest interior point method: it uses only 
the primal problem and does not use a barrier function. No polynomial running time has been proven for this method, 
and in practice it has been replaced by primal-dual methods (see the next section). Therefore in this course we restrict ourselves 
to a short description.

**Problem:** $\max \mathbf{c}^T\mathbf{x}$, where $A\mathbf{x} = \mathbf{b}$, $\mathbf{x} \geq \mathbf{0}$. 
A starting point $\mathbf{x} > \mathbf{0}$ with $A\mathbf{x} = \mathbf{b}$ (inside the feasible region) is known.

**Summary of affine scaling:** If $\mathbf{x}$ is close to some boundary $x_j = 0$, then only a short step 
can be taken in the gradient direction. Therefore in each iteration the coordinates are first *scaled* so 
that the current point is at the same distance from all boundaries:

1. Let $X = \operatorname{diag}(x_1, \ldots, x_n)$ denote the diagonal matrix. In the coordinates $\tilde{\mathbf{x}} = X^{-1}\mathbf{x}$ 
   the current point is $\mathbf{e} = (1, \ldots, 1)$, and the unit ball around it lies in the region $\tilde{\mathbf{x}} \geq \mathbf{0}$. 
   In the original coordinates this ball corresponds to the ellipsoid $\sum_j (\Delta x_j / x_j)^2 \leq 1$ (the *Dikin ellipsoid*), 
   which touches the planes $x_j = 0$.
2. In the scaled coordinates the gradient of the objective function $X\mathbf{c}$ is projected onto the subspace where $AX\tilde{\mathbf{x}} = \mathbf{b}$ 
   still holds. Returning to the original coordinates gives the direction
   
   $$
   \mathbf{y} = (A X^2 A^T)^{-1} A X^2 \mathbf{c},\qquad
   \mathbf{r} = \mathbf{c} - A^T\mathbf{y},\qquad
   \Delta\mathbf{x} = X^2 \mathbf{r}.
   $$
   
   Then $A\Delta\mathbf{x} = \mathbf{0}$, and $\mathbf{c}^T\Delta\mathbf{x} = \lVert X\mathbf{r} \rVert^2 \geq 0$.
3. Find the longest step $\alpha_{\max} = \min_{j:\, \Delta x_j < 0} x_j / (-\Delta x_j)$ for which $\mathbf{x} + \alpha\Delta\mathbf{x} \geq \mathbf{0}$ still holds, 
   and move only a fraction of it: $\mathbf{x} \leftarrow \mathbf{x} + \beta\,\alpha_{\max}\Delta\mathbf{x}$, where, for example, $\beta = 0.96$. 
   (If $\Delta\mathbf{x} \geq \mathbf{0}$ and $\Delta\mathbf{x} \neq \mathbf{0}$, the problem is unbounded.)
4. The vector $\mathbf{y}$ is an estimate of the dual solution. When $\mathbf{r} \leq \mathbf{0}$ (i.e., $\mathbf{y}$ is dual feasible) 
   and the duality gap $\mathbf{b}^T\mathbf{y} - \mathbf{c}^T\mathbf{x} = -\mathbf{x}^T\mathbf{r}$ is small enough, the algorithm stops.

**Example:** For the problem $\max \left( -\frac{x_1}{3} + x_2 \right)$, where $x_1 + x_2 \leq 4$, $2x_1 - x_2 \leq 3$, $x_1, x_2 \geq 0$ 
(in standard form with slack variables $x_3, x_4$), one iteration with $\beta = 0.96$ from the starting point $\mathbf{x} = (1, 1, 2, 2)$ 
gives $\mathbf{x} = (0.74957;\ 3.17043;\ 0.08000;\ 4.67130)$. This step is limited by the slack variable $x_3$, which is close to zero, 
i.e., the point is already close to the boundary $x_1 + x_2 = 4$. The optimum is $(x_1, x_2) = (0, 4)$.

![Result of affine scaling](figs/affine-scaling-sample-result.png)

*The first iteration of affine scaling from the point $(1,1)$.*

**Drawbacks:** With a long step ($\beta$ close to $1$) the iterates come close to the boundary, and then the next steps become very short, because 
the Dikin ellipsoid is narrow. Convergence to the optimum has been proven for $\beta \leq 2/3$, but counterexamples are known 
in which with $\beta = 0.999$ the method converges to a non-optimal point. The primal-dual method (see below) 
solves this problem by keeping the iterates close to the *central path*; there the matrix $X^2$ is replaced by $X S^{-1}$.

### The Primal-Dual Path-Following Method

Primal-dual path-following methods are today 
the most widely used interior point methods. The central path was described by N.Megiddo (1989), 
a polynomial-time primal-dual algorithm by M.Kojima, S.Mizuno and A.Yoshise (1989), 
and the practical *predictor-corrector* variant by S.Mehrotra (1992). These methods underlie the interior point (*barrier*) algorithms of most 
commercial and open-source LP solvers; they usually 
find a solution after a few dozen iterations, almost independently of the size of the problem.

The method uses the duality results from the [previous lecture]({{ '/lectures/linear_introduction/' | relative_url }}) 
(section "Duality Theorems: A Summary for Algorithms"). A more detailed exposition is in the book [[Wri97]](#Wri97).

**Problem:** The primal and dual problems in standard form, where $A$ is an $m \times n$ matrix:

$$
(P): \textcolor{blue}{\min \left( \mathbf{c}^T \mathbf{x} \right)},\;\;\text{where}\;\;
A\mathbf{x} = \mathbf{b},\;\; \mathbf{x} \geq \mathbf{0};
\qquad
(D): \textcolor{blue}{\max \left( \mathbf{b}^T \mathbf{y} \right)},\;\;\text{where}\;\;
A^T\mathbf{y} + \mathbf{s} = \mathbf{c},\;\; \mathbf{s} \geq \mathbf{0}.
$$

Let $X = \operatorname{diag}(\mathbf{x})$, $S = \operatorname{diag}(\mathbf{s})$, $\mathbf{e} = (1, \ldots, 1)^T$.

**Basic idea:** The optimal $\mathbf{x}$ and $(\mathbf{y}, \mathbf{s})$ are the solution of the system

$$
A\mathbf{x} = \mathbf{b},\;\;
A^T\mathbf{y} + \mathbf{s} = \mathbf{c},\;\;
X S \mathbf{e} = \mathbf{0},\;\;
\mathbf{x} \geq \mathbf{0},\;\; \mathbf{s} \geq \mathbf{0}.
$$

This system is hard to solve directly, because $x_j s_j = 0$ means a combinatorial choice -- which 
$x_j$ will be zero. Therefore the algorithm maintains strictly positive $\mathbf{x} > \mathbf{0}$ and $\mathbf{s} > \mathbf{0}$, and in each iteration it:

* computes $\mu = \mathbf{x}^T\mathbf{s} / n$ -- the average product $x_j s_j$ (the duality gap is $n\mu$);
* chooses a target on the central path with a smaller parameter $\sigma\mu$, where $0 < \sigma < 1$ (the *centering parameter*);
* makes one step of *Newton's method* for the system $A\mathbf{x} = \mathbf{b}$, $A^T\mathbf{y} + \mathbf{s} = \mathbf{c}$, $X S \mathbf{e} = \sigma\mu\mathbf{e}$;
* shortens the step so that $\mathbf{x}$ and $\mathbf{s}$ stay positive.

Its iterates follow the central path, and the duality gap decreases by a factor of about $1/\sigma$ in each iteration.

**The Newton step:** The first two equations are linear, but in the third, $(x_j + \Delta x_j)(s_j + \Delta s_j) = \sigma\mu$, 
the small term $\Delta x_j \Delta s_j$ is dropped. This gives a linear system for the direction $(\Delta\mathbf{x}, \Delta\mathbf{y}, \Delta\mathbf{s})$:

$$
\left( \begin{array}{ccc}
A & 0 & 0\\
0 & A^T & I\\
S & 0 & X
\end{array} \right)
\left( \begin{array}{c}
\Delta\mathbf{x}\\
\Delta\mathbf{y}\\
\Delta\mathbf{s}
\end{array} \right)
=
\left( \begin{array}{c}
\mathbf{r}_P\\
\mathbf{r}_D\\
\mathbf{r}_C
\end{array} \right),
\;\;\text{where}\;\;
\left\{ \begin{array}{l}
\mathbf{r}_P = \mathbf{b} - A\mathbf{x},\\
\mathbf{r}_D = \mathbf{c} - A^T\mathbf{y} - \mathbf{s},\\
\mathbf{r}_C = \sigma\mu\mathbf{e} - X S\mathbf{e}.
\end{array} \right.
$$

Eliminating $\Delta\mathbf{s}$ and $\Delta\mathbf{x}$ leaves only an $m \times m$ system (the *normal equations*) with the symmetric 
positive definite matrix $A D A^T$, where $D = X S^{-1}$:

$$
(A D A^T)\,\Delta\mathbf{y} = \mathbf{r}_P + A S^{-1}(X\mathbf{r}_D - \mathbf{r}_C),\qquad
\Delta\mathbf{s} = \mathbf{r}_D - A^T\Delta\mathbf{y},\qquad
\Delta\mathbf{x} = S^{-1}(\mathbf{r}_C - X\Delta\mathbf{s}).
$$

If the starting point is feasible ($\mathbf{r}_P = \mathbf{0}$, $\mathbf{r}_D = \mathbf{0}$), it stays feasible afterwards, 
because $A\Delta\mathbf{x} = \mathbf{0}$ and $A^T\Delta\mathbf{y} + \Delta\mathbf{s} = \mathbf{0}$.

**Pseudocode of the primal-dual method**

*Input:* Matrix $A$, vectors $\mathbf{b}$, $\mathbf{c}$; a starting point $\mathbf{x} > \mathbf{0}$, $\mathbf{y}$, $\mathbf{s} > \mathbf{0}$; 
precision $\varepsilon > 0$; parameters $\sigma \in (0;1)$ (for example, $0.1$) and $\eta \in (0;1)$ (for example, $0.9$--$0.99$).  
*Output:* Approximately optimal $\mathbf{x}$ and $(\mathbf{y}, \mathbf{s})$.

$\textsf{Primal-Dual-Path-Following}(A, \mathbf{b}, \mathbf{c}, \mathbf{x}, \mathbf{y}, \mathbf{s})$
1. **while** $\mathbf{x}^T\mathbf{s} > \varepsilon$ **or** $\lVert \mathbf{b} - A\mathbf{x} \rVert > \varepsilon$ **or** $\lVert \mathbf{c} - A^T\mathbf{y} - \mathbf{s} \rVert > \varepsilon$
2. $\quad \mu = \mathbf{x}^T\mathbf{s} / n$ $\quad$ *// the duality gap is $n\mu$*
3. $\quad \mathbf{r}_P = \mathbf{b} - A\mathbf{x}$; $\;\;\mathbf{r}_D = \mathbf{c} - A^T\mathbf{y} - \mathbf{s}$; $\;\;\mathbf{r}_C = \sigma\mu\mathbf{e} - X S\mathbf{e}$
4. $\quad D = X S^{-1}$
5. $\quad \Delta\mathbf{y} = \textsf{Solve}\left(A D A^T,\; \mathbf{r}_P + A S^{-1}(X\mathbf{r}_D - \mathbf{r}_C)\right)$ $\quad$ *// normal equations*
6. $\quad \Delta\mathbf{s} = \mathbf{r}_D - A^T\Delta\mathbf{y}$
7. $\quad \Delta\mathbf{x} = S^{-1}(\mathbf{r}_C - X\Delta\mathbf{s})$
8. $\quad \alpha_P = \min\left(1,\; \eta \cdot \min_{j:\, \Delta x_j < 0} x_j / (-\Delta x_j)\right)$ $\quad$ *// $\mathbf{x}$ stays positive*
9. $\quad \alpha_D = \min\left(1,\; \eta \cdot \min_{j:\, \Delta s_j < 0} s_j / (-\Delta s_j)\right)$ $\quad$ *// $\mathbf{s}$ stays positive*
10. $\quad \mathbf{x} = \mathbf{x} + \alpha_P \Delta\mathbf{x}$
11. $\quad \mathbf{y} = \mathbf{y} + \alpha_D \Delta\mathbf{y}$; $\;\;\mathbf{s} = \mathbf{s} + \alpha_D \Delta\mathbf{s}$
12. **return** $(\mathbf{x}, \mathbf{y}, \mathbf{s})$

The main work in each iteration is line 5: solving an $m \times m$ system (in large problems, with a sparse 
Cholesky factorization). The matrix $A D A^T$ changes in every iteration, but the pattern of its nonzero elements stays 
the same, so the structure of the factorization can be computed once.

**Running time:** If the iterates are kept close enough to the central path (the *short-step* variant with $\sigma = 1 - 0.4/\sqrt{n}$ 
and a full step), then $O(\sqrt{n}\, L)$ iterations suffice, where $L$ is the number of input bits; this is the best known 
bound on the number of iterations for interior point methods. In practice longer steps are used ($\sigma \approx 0.1$ or an adaptive $\sigma$) 
together with Mehrotra's predictor-corrector scheme: first a direction with $\sigma = 0$ is computed (the *predictor*), based on it $\sigma$ is chosen, 
and a correction is added that accounts for the dropped term $\Delta x_j \Delta s_j$ (the *corrector*). Both directions use the same 
factorization of the matrix $A D A^T$.

#### An Example of the Primal-Dual Method

Let us solve the same problem as for the affine scaling method: $\max \left( -\frac{x_1}{3} + x_2 \right)$, where 
$x_1 + x_2 \leq 4$, $2x_1 - x_2 \leq 3$, $x_1, x_2 \geq 0$. With slack variables $x_3, x_4$ and switching to minimization:

$$
\textcolor{blue}{\min \left( \frac{x_1}{3} - x_2 \right)},\;\;\text{where}\;\;
A = \left( \begin{array}{cccc}
1 & 1 & 1 & 0\\
2 & -1 & 0 & 1
\end{array} \right),\;\;
\mathbf{b} = \left( \begin{array}{c}
4\\
3
\end{array} \right),\;\;
\mathbf{c} = \left( \begin{array}{c}
1/3\\
-1\\
0\\
0
\end{array} \right),\;\;
\mathbf{x} \geq \mathbf{0}.
$$

The dual problem: $\max (4y_1 + 3y_2)$, where $y_1 + 2y_2 + s_1 = 1/3$, $y_1 - y_2 + s_2 = -1$, $y_1 + s_3 = 0$, $y_2 + s_4 = 0$, 
$\mathbf{s} \geq \mathbf{0}$.

**Starting point:** $\mathbf{x}^{(0)} = (1, 1, 2, 2)$ (primal feasible) and $\mathbf{y}^{(0)} = (-2, -1/2)$, which gives 
$\mathbf{s}^{(0)} = \mathbf{c} - A^T\mathbf{y}^{(0)} = (10/3,\ 1/2,\ 2,\ 1/2) > \mathbf{0}$ (dual feasible). 
The duality gap is $\mathbf{x}^T\mathbf{s} = 10/3 + 1/2 + 4 + 1 = 8.8333$, so $\mu = 8.8333/4 = 2.2083$. 
Parameters: $\sigma = 0.1$, $\eta = 0.9$.

**The first iteration:**

* Target on the central path: $\sigma\mu = 0.22083$. Since the starting point is feasible, $\mathbf{r}_P = \mathbf{0}$ and $\mathbf{r}_D = \mathbf{0}$, while 
  $\mathbf{r}_C = \sigma\mu\mathbf{e} - X S\mathbf{e} = 0.22083 - (3.33333,\ 0.5,\ 4,\ 1) = (-3.11250,\ -0.27917,\ -3.77917,\ -0.77917)$.
* $D = X S^{-1} = \operatorname{diag}(0.3,\ 2,\ 1,\ 4)$, and the matrix of the normal equations is

  $$
  A D A^T = \left( \begin{array}{cc}
  0.3 + 2 + 1 & 0.6 - 2\\
  0.6 - 2 & 1.2 + 2 + 4
  \end{array} \right)
  = \left( \begin{array}{cc}
  3.3 & -1.4\\
  -1.4 & 7.2
  \end{array} \right).
  $$

* Right-hand side $-A S^{-1}\mathbf{r}_C = (3.38167,\ 2.86750)$; solving the system gives $\Delta\mathbf{y} = (1.30103,\ 0.65124)$.
* $\Delta\mathbf{s} = -A^T\Delta\mathbf{y} = (-2.60352,\ -0.64979,\ -1.30103,\ -0.65124)$ and 
  $\Delta\mathbf{x} = S^{-1}(\mathbf{r}_C - X\Delta\mathbf{s}) = (-0.15269,\ 0.74125,\ -0.58855,\ 1.04664)$.
* Step lengths: primal $\alpha_P = \min(1;\ 0.9 \cdot 1/0.15269;\ 0.9 \cdot 2/0.58855) = 1$; dual 
  $\alpha_D = 0.9 \cdot 0.5 / 0.65124 = 0.69099$ (limited by $s_4$).
* The new point: $\mathbf{x}^{(1)} = (0.84731,\ 1.74125,\ 1.41145,\ 3.04664)$, $\mathbf{y}^{(1)} = (-1.10100,\ -0.05000)$, 
  duality gap $\mathbf{x}^T\mathbf{s} = 3.09520$.

**Further iterations** (computed with the program [figs/primal-dual-path.py](figs/primal-dual-path.py)):

| $k$ | $x_1$ | $x_2$ | $\mu = \mathbf{x}^T\mathbf{s}/4$ | Gap $\mathbf{x}^T\mathbf{s}$ | $\alpha_P$ | $\alpha_D$ |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.00000 | 1.00000 | 2.20833 | 8.83333 | -- | -- |
| 1 | 0.84731 | 1.74125 | 0.77380 | 3.09520 | 1.0000 | 0.6910 |
| 2 | 0.20797 | 3.54898 | 0.15425 | 0.61701 | 1.0000 | 0.5980 |
| 3 | 0.02080 | 3.95321 | 0.01922 | 0.07687 | 0.9685 | 1.0000 |
| 4 | 0.00208 | 3.99524 | 0.00227 | 0.00908 | 0.9719 | 1.0000 |
| 5 | 0.00021 | 3.99952 | 0.00025 | 0.00100 | 0.9810 | 1.0000 |
| 6 | 0.00002 | 3.99995 | 0.00003 | 0.00011 | 0.9896 | 1.0000 |

When the steps are almost full, the gap decreases by a factor of about $1/\sigma = 10$ in each iteration. The iterates approach 
$\mathbf{x}^{\ast} = (0, 4, 0, 7)$, $\mathbf{y}^{\ast} = (-1, 0)$, $\mathbf{s}^{\ast} = (4/3, 0, 1, 0)$ -- all products $x_j s_j$ tend to $0$, 
and the maximum of the objective function is $-0/3 + 4 = 4$. For the original maximization problem the shadow prices are $-\mathbf{y}^{\ast} = (1, 0)$: 
only the constraint $x_1 + x_2 \leq 4$ is active.

![Iterations of the primal-dual method and the central path](figs/primal-dual-path.png)

*The central path (green) starts at the analytic center of the feasible region and ends at the optimum $(0,4)$. The starting point $\mathbf{x}^{(0)}$ is not on the central path, but the very first iterations come close to it and then follow it to the optimum.*



## Integer Programming

**Claim:** The integer programming problem is NP-complete: it belongs to a well-known 
family of problems that can all be reduced to one another. No efficient algorithm is known for NP-complete problems. 
If such an algorithm were found for one of these problems, then one could also efficiently solve 
all the other NP-complete problems from the famous [list of Richard Karp](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems) and hundreds of other problems that are also NP-complete (i.e., efficiently reducible 
to each other in terms of algorithmic complexity).

Linear programs over the real numbers have efficient polynomial algorithms, but 
for the integer programming problem (except some special cases) no efficient algorithm is known. 

**The decision problem:**  
Given an integer matrix $A$, integer vectors $\mathbf{b}$ and $\mathbf{c}$ and 
an integer $K$, determine whether there exists $\mathbf{x} \in \mathbb{Z}_{\geq 0}^n$ such that 
$$A\mathbf{x}\leq \mathbf{b}\;\;\mbox{and}\;\;\mathbf{c}^\top \mathbf{x}\leq K?$$

The decision problem is NP-complete: 

* The decision problem is NP-hard even if the allowed values of the variables are $x_i \in \{0,1\}$. 
  Vertex cover, 3SAT and several other NP-hard problems can be reduced to it.
* The decision problem belongs to NP: if the answer is "yes", an $\mathbf{x}$ certifying it can be checked
  in polynomial time (although finding it may be impossible in polynomial time).

**The optimization problem:**  
$$\min \lbrace \mathbf{c}^\top \mathbf{x} : A\mathbf{x}\le \mathbf{b},\ \mathbf{x}\in\mathbb Z_{\ge0}^n \rbrace$$

The integer optimization problem is NP-hard (other NP-hard problems can be reduced to it). 
It cannot be considered NP-complete, because it is not a decision problem.




### Vertex Cover

**Definition:** In an undirected graph $G = (V,E)$ a *vertex cover* is a subset of vertices $V' \subseteq V$ 
that contains at least one endpoint ($v_i$ or $v_j$) of every edge $(v_i,v_j) \in E$. 

Richard Karp showed that it is NP-complete to determine whether a given graph $G = (V,E)$ has a vertex cover $V'$ with at most $\lvert V' \rvert = k$ vertices. This is a *decision problem*.

There is also a related *optimization problem*: for a given graph find the smallest $k$ for which a vertex cover with $\lvert V' \rvert=k$ exists.

In both cases one may want not only to find the answer Yes/No (or the number $k$), but also to construct the vertex cover itself.

**Reduction of vertex cover to integer programming**

![Reduction of vertex cover to integer programming](figs/vertex-cover.png)

The number of vertices corresponds to the number of variables, and the number of constraints corresponds to the number of edges. If vertex $v_i$ is put in the cover, the corresponding variable is $x_i = 1$; otherwise $x_i = 0$.

This example shows that integer programming most likely has no simple algorithm that solves it in polynomial time, because otherwise the vertex cover problem (one of the NP-complete problems) could also be solved in polynomial time.




### The Knapsack Problem

We are given $N$ objects. Each of them has a price $c_i$ and a weight $w_i$.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $c_i$ | 19 | 17 | 30 | 13 | 25 | 29 | 23 | 10 |
| $w_i$ | 4 | 2 | 8 | 3 | 7 | 5 | 9 | 6 |

The knapsack can hold objects with a total weight of at most 17 kilograms. 
What is the largest value that can be put into the knapsack?


**Variables:**
$$
1 \ge b_1,b_2,b_3,b_4,b_5,b_6,b_7,b_8 \ge 0,
\qquad b_i\in\mathbb{Z}.
$$

**Constraint:**
$$
4b_1+2b_2+8b_3+3b_4+7b_5+5b_6+9b_7+6b_8\le17.
$$

**Objective function:**
$$
\max\; 19b_1+17b_2+30b_3+13b_4+25b_5+29b_6+23b_7+10b_8.
$$


Turn the knapsack problem into a linear/integer programming problem. 
Solve it in Python using the library `pulp`.

<!-- https://youtu.be/E72DWgKP_1Y?si=hcea7o5EMqtuY0OS -->



### Hamiltonian Cycle

**Definition:** In an undirected graph $G = (V,E)$ a *Hamiltonian cycle* is a cycle that passes through 
every vertex of the graph exactly once. A graph that has a Hamiltonian cycle is called a *Hamiltonian graph*.

The problem of determining whether a given graph has a Hamiltonian cycle is also NP-complete (it is on Richard Karp's list).

![Hamiltonian cycle in the dodecahedron graph](figs/hamiltonian-paths.png)

*A Hamiltonian cycle in the dodecahedron graph: the edges of the cycle are red, the other edges of the graph are dotted.*

**Reduction of the Hamiltonian cycle to integer programming**

To each edge $e \in E$ we assign a variable $x_e \in \lbrace 0,1 \rbrace$: $x_e = 1$ if edge $e$ belongs to the Hamiltonian cycle, and $x_e = 0$ otherwise. For a subset of vertices $S \subseteq V$, $\delta(S)$ denotes the set of edges with one endpoint in $S$ and the other outside $S$. For a vertex $v$ we write $\delta(v) = \delta(\lbrace v \rbrace)$ -- these are all edges with endpoint $v$.

*Vertex constraints:* In a Hamiltonian cycle each vertex is incident to exactly two edges of the cycle (the cycle enters the vertex along one and leaves along the other):

$$
\sum_{e\in\delta(v)}x_e=2
\qquad \forall v\in V.
$$

These constraints alone are not enough: they are also satisfied by several disjoint cycles (*subtours*) that together contain all vertices.

*Cut constraints:* For each partition of the vertex set $V$ into two nonempty subsets $S$ and $V \setminus S$, a Hamiltonian cycle crosses the boundary between them at least twice (if the cycle leaves $S$, it must come back):

$$
\sum_{e\in\delta(S)}x_e\ge2
\qquad
\forall\,\varnothing\ne S\subsetneq V.
$$

If $\mathbf{x}$ describes several subtours, then choosing the vertices of one subtour as $S$ gives $\sum_{e\in\delta(S)}x_e = 0$, so this constraint is violated. Therefore the integer solutions that satisfy both kinds of constraints are exactly the Hamiltonian cycles. This decision problem needs no objective function; if the edges are given lengths $c_e$ and $\sum_{e \in E} c_e x_e$ is minimized, we get the traveling salesman problem.



### The Branch and Bound Method

**The knapsack problem (*0-1 Knapsack Problem*):** We are given $n$ items; for each the 
weight $w_i$ and the value $c_i$ are known. We must find which of them to put into a collection 
("knapsack") so that the total weight does not exceed the given limit $W$ and the total value 
is as large as possible. (For example, resource allocation problems where one must choose from 
many indivisible projects under a fixed budget or time constraint.)

$$
\textcolor{blue}{\max \left( \sum\limits_{i=1}^n c_i x_i \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
\sum\limits_{i=1}^n w_i x_i \leq W,\\
x_i \in \{0,1\}.\\
\end{array} \right.
$$

There are also other variants of this problem: the *bounded knapsack problem* allows taking several 
identical items (up to $d$ copies of each item), and the *unbounded knapsack problem* 
allows taking any integer number of copies of each item.

The solution can be sought by exhaustive search. This gives a *decision tree* 
for the variables $x_1,x_2,x_3,\ldots$: at each level one variable is fixed as $0$ or $1$.

![Decision tree for the variables](figs/binary-search-tree1.png)

* The variables are integers that satisfy the inequalities $0 \leq x_i \leq 1$ for all 
  $i = 1,\ldots,n$, i.e., $x_i \in \lbrace 0,1 \rbrace$. The tree has $2^n$ leaves.
* Exhaustive search always finds the optimum, and for small problems (for example, $4$ variables 
  give only $2^4 = 16$ cases) it is perfectly sufficient, but for larger problems 
  the time of exhaustive search grows exponentially.

**The basic idea of the Branch and Bound algorithm:**

* *Branching* (*branch*): the problem is split into subproblems by fixing the value of some variable 
  ($x_k = 0$ or $x_k = 1$); these are the children of a node of the decision tree.
* *Bounding* (*bound*): at each node the *LP relaxation* is solved -- the same problem, 
  but with real $x_i \in [0;1]$. The relaxed problem has more feasible solutions, 
  so its maximum is an upper bound for all integer solutions 
  in the subtree of this node.
* The best integer solution found so far is called the *incumbent solution*. 
  If the maximum of the relaxed LP is not larger than the incumbent 
  solution, there is no better solution in this subtree, and the whole branch is *pruned*.
* A branch is also pruned if the solution of the relaxed LP is already integer (it is 
  the best one in this subtree), or if the LP is infeasible.

In practical problems this usually prunes most nodes of the decision tree 
(although in the worst case the amount of work still grows exponentially). The possibility 
of considerably reducing exhaustive search pays off -- even though at each node an additional 
relaxed LP subproblem has to be solved.

**Notation:**

* The *nodes* of the decision tree are numbered in the order of their creation $v_1, v_2, \ldots$. 
  Each node corresponds to a subproblem in which some of the variables are fixed as $0$ or $1$:
  - at the root $v_1$ no variable is fixed;
  - in the children of $v_1$ the branching variable is fixed, for example, $v_2$: $x_1 = 0$ and $v_3$: $x_1 = 1$ 
    (the other variables are not fixed);
  - further numbers are assigned only to the nodes that the algorithm actually creates 
    (children of pruned nodes are not created).
* $\mathbf{x}_{LP}(j)$ -- the optimal real values $x_i \in [0;1]$ of the relaxed LP at node $v_j$; 
  $z_{LP}(j)$ -- the corresponding maximum of the objective function.
* $\mathbf{x}^{\ast}$ and $z^{\ast}$ -- the incumbent solution and its objective function value.

**Branch and Bound pseudocode**

*Input:* An integer programming problem $\max \mathbf{c}^T \mathbf{x}$, where 
$A\mathbf{x} \leq \mathbf{b}$, $x_i \in \lbrace 0,1 \rbrace$ (objective function coefficients 
$\mathbf{c}$, constraint matrix $A$ and right-hand sides $\mathbf{b}$).  
*Output:* The optimal solution $\mathbf{x}^{\ast} \in \lbrace 0,1 \rbrace^n$.

$\textsf{Branch-And-Bound}(\mathbf{c}, A, \mathbf{b})$
1. $Q = \lbrace v_1 \rbrace$ $\quad$ *// active nodes; at the root $v_1$ no $x_i$ is fixed*
2. $\mathbf{x}^{\ast} = (0,\ldots,0)$; $\;\;z^{\ast} = 0$ $\quad$ *// incumbent solution (valid if $\mathbf{b} \geq \mathbf{0}$)*
3. **while** $Q \neq \varnothing$
4. $\quad$ remove some node $v_j$ from $Q$
5. $\quad (\mathbf{x}_{LP}(j), z_{LP}(j)) = \textsf{Solve-LP-Relaxation}(\mathbf{c}, A, \mathbf{b}, v_j)$ $\quad$ *// if the LP is infeasible, $z_{LP}(j) = -\infty$*
6. $\quad$ **if** $z_{LP}(j) \leq z^{\ast}$ $\quad$ *// even the relaxed LP is not better than the incumbent*
7. $\quad\quad$ prune $v_j$
8. $\quad$ **elseif** all coordinates of $\mathbf{x}_{LP}(j)$ are integers $\quad$ *// better than the incumbent solution*
9. $\quad\quad \mathbf{x}^{\ast} = \mathbf{x}_{LP}(j)$; $\;\;z^{\ast} = z_{LP}(j)$
10. $\quad\quad$ prune $v_j$
11. $\quad$ **else** $\quad$ *// maybe the incumbent can be improved in the subtree?*
12. $\quad\quad$ choose a variable $x_k$ whose value in $\mathbf{x}_{LP}(j)$ is not an integer
13. $\quad\quad$ insert into $Q$ the two children of $v_j$: with the extra constraint $x_k = 0$ and with $x_k = 1$
14. **return** $\mathbf{x}^{\ast}$

In line 4 the node can be chosen in different ways. If $Q$ is a queue (FIFO), the tree is traversed breadth-first (BFS) -- as in the example below; if $Q$ is a stack, the tree is traversed depth-first (DFS), and then the first integer solution is found sooner. In line 2 the initial solution $\mathbf{x}^{\ast} = \mathbf{0}$ is feasible if $\mathbf{b} \geq \mathbf{0}$ (for example, in the knapsack problem); in the general case one starts with $z^{\ast} = -\infty$.

### An Example of an Integer Problem

We look for variables $x_i \in \lbrace 0,1 \rbrace$. The integer programming problem:

$$
\textcolor{blue}{\max \left( 15x_1 + 12x_2 + 4x_3 + 2x_4 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
8x_1 + 5x_2 + 3x_3 + 2x_4 \leq 10,\\
x_k \in \{0,1\}\;\;\text{for}\;\;k=1,2,3,4.\\
\end{array} \right.
$$

This is a knapsack problem with $4$ items and the weight limit $W = 10$. (In the library `pulp` such 
variables are defined with `cat=LpBinary`; the solver usually finds them quickly, although in the general 
case integer programming is NP-hard.)

The same problem in matrix notation:

$$
\textcolor{blue}{\max \left( \mathbf{c}^T \cdot \mathbf{x} \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
A\mathbf{x} \leq \mathbf{b},\\
x_i \in \{ 0, 1 \}.
\end{array} \right.
$$

$$
\mathbf{x} = \left(
\begin{array}{c}
x_1 \\
x_2 \\
x_3 \\
x_4 \\
\end{array} \right),\;\;\mathbf{c} = \left(
\begin{array}{c}
15 \\
12 \\
4 \\
2 \\
\end{array} \right),
$$

$$
A = \left(
\begin{array}{cccc}
8 & 5 & 3 & 2 \\
\end{array} \right),\;\;\;\mathbf{b} = \left(
\begin{array}{c}
10 \\
\end{array} \right)
$$

In this problem the relaxed LP can be solved without the simplex algorithm: sort the items by 
the ratio of value to weight ($c_2/w_2 = 12/5 = 2.4$; $c_1/w_1 = 15/8 = 1.875$; 
$c_3/w_3 = 4/3 \approx 1.33$; $c_4/w_4 = 2/2 = 1$) and take them greedily in this order while 
there is room; the last item that no longer fits completely is taken partially. 
We process the nodes in the order of their creation (BFS).

#### Step 1

At node $v_1$ (none of the $x_i$ is fixed) the relaxed LP problem is:

$$
\textcolor{blue}{\max \left( 15x_1 + 12x_2 + 4x_3 + 2x_4 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
8x_1 + 5x_2 + 3x_3 + 2x_4 \leq 10,\\
x_k \leq 1,\;\;k=1,2,3,4,\\
x_k \geq 0,\;\;k=1,2,3,4.\\
\end{array} \right.
$$

![Root v1 of the decision tree](figs/binary-search-tree2.png)

Incumbent solution: $\mathbf{x}^{\ast} = (0, 0, 0, 0)$, $z^{\ast} = 0$.

Solution of the relaxed LP: $\mathbf{x}_{LP}(1) = (5/8, 1, 0, 0)$, $z_{LP}(1) = 12 + 15 \cdot 5/8 = 21\frac{3}{8}$.

Since $z_{LP}(1) = 21\frac{3}{8} > z^{\ast} = 0$, but $x_1 = 5/8$ is not an integer, we branch on $x_1$: both children of $v_1$ are added to the tree -- $v_2$ ($x_1 = 0$) and $v_3$ ($x_1 = 1$).

![Decision tree with the children of v1](figs/binary-search-tree3.png)

#### Step 2

At node $v_2$ (fixed $x_1 = 0$) the relaxed LP problem is:

$$
\textcolor{blue}{\max \left( 15x_1 + 12x_2 + 4x_3 + 2x_4 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
8x_1 + 5x_2 + 3x_3 + 2x_4 \leq 10,\\
x_1 = 0,\\
x_k \leq 1,\;\;k=1,2,3,4,\\
x_k \geq 0,\;\;k=1,2,3,4.\\
\end{array} \right.
$$

Incumbent solution: $\mathbf{x}^{\ast} = (0, 0, 0, 0)$, $z^{\ast} = 0$.

Solution of the relaxed LP: $\mathbf{x}_{LP}(2) = (0, 1, 1, 1)$, $z_{LP}(2) = 12 + 4 + 2 = 18$ (all three items fit: $5 + 3 + 2 = 10$).

Since $z_{LP}(2) = 18 > z^{\ast} = 0$ and all coordinates of $\mathbf{x}_{LP}(2)$ are integers, it becomes the new incumbent solution: $\mathbf{x}^{\ast} = (0, 1, 1, 1)$, $z^{\ast} = 18$. Node $v_2$ is pruned (its subtree has no better solution).

![Decision tree after processing node v2](figs/binary-search-tree4.png)

#### Step 3

At node $v_3$ (fixed $x_1 = 1$) the relaxed LP problem is:

$$
\textcolor{blue}{\max \left( 15x_1 + 12x_2 + 4x_3 + 2x_4 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
8x_1 + 5x_2 + 3x_3 + 2x_4 \leq 10,\\
x_1 = 1,\\
x_k \leq 1,\;\;k=1,2,3,4,\\
x_k \geq 0,\;\;k=1,2,3,4.\\
\end{array} \right.
$$

Incumbent solution: $\mathbf{x}^{\ast} = (0, 1, 1, 1)$, $z^{\ast} = 18$.

Solution of the relaxed LP: $\mathbf{x}_{LP}(3) = (1, 2/5, 0, 0)$, $z_{LP}(3) = 15 + 12 \cdot 2/5 = 19\frac{4}{5}$ (after $x_1$, the remaining room $10 - 8 = 2$ holds $2/5$ of the second item).

Since $z_{LP}(3) = 19\frac{4}{5} > z^{\ast} = 18$, but $x_2 = 2/5$ is not an integer, we branch on $x_2$: both children of $v_3$ are added to the tree -- $v_4$ ($x_1 = 1$, $x_2 = 0$) and $v_5$ ($x_1 = 1$, $x_2 = 1$).

![Decision tree after processing node v3](figs/binary-search-tree5.png)

#### Step 4

At node $v_4$ (fixed $x_1 = 1$ and $x_2 = 0$) the relaxed LP problem is:

$$
\textcolor{blue}{\max \left( 15x_1 + 12x_2 + 4x_3 + 2x_4 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
8x_1 + 5x_2 + 3x_3 + 2x_4 \leq 10,\\
x_1 = 1,\;\;x_2 = 0,\\
x_k \leq 1,\;\;k=1,2,3,4,\\
x_k \geq 0,\;\;k=1,2,3,4.\\
\end{array} \right.
$$

Incumbent solution: $\mathbf{x}^{\ast} = (0, 1, 1, 1)$, $z^{\ast} = 18$.

Solution of the relaxed LP: $\mathbf{x}_{LP}(4) = (1, 0, 2/3, 0)$, $z_{LP}(4) = 15 + 4 \cdot 2/3 = 17\frac{2}{3}$.

Since $z_{LP}(4) = 17\frac{2}{3} \leq z^{\ast} = 18$, even the relaxed LP is not better than the incumbent solution. Node $v_4$ is pruned (even though $x_3 = 2/3$ is not an integer).

#### Step 5

At node $v_5$ (fixed $x_1 = 1$ and $x_2 = 1$) the relaxed LP problem is:

$$
\textcolor{blue}{\max \left( 15x_1 + 12x_2 + 4x_3 + 2x_4 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
8x_1 + 5x_2 + 3x_3 + 2x_4 \leq 10,\\
x_1 = 1,\;\;x_2 = 1,\\
x_k \leq 1,\;\;k=1,2,3,4,\\
x_k \geq 0,\;\;k=1,2,3,4.\\
\end{array} \right.
$$

Incumbent solution: $\mathbf{x}^{\ast} = (0, 1, 1, 1)$, $z^{\ast} = 18$.

The relaxed LP is infeasible: already $8 \cdot 1 + 5 \cdot 1 = 13 > 10$. So $z_{LP}(5) = -\infty \leq z^{\ast}$, and node $v_5$ is pruned.

![Decision tree after processing nodes v4 and v5](figs/binary-search-tree6.png)

#### Result

There are no more active nodes, so the incumbent solution is optimal: $\mathbf{x}^{\ast} = (0, 1, 1, 1)$, $z^{\ast} = 18$ -- items 2, 3 and 4 must be taken (total weight $10$). The algorithm solved $5$ relaxed LP problems, whereas exhaustive search would have to check $2^4 = 16$ cases.



## Problems

**Problem 10.1:** The search for a Hamiltonian cycle in the dodecahedron graph (see the figure in the section "Hamiltonian Cycle") is written as an integer programming problem with vertex constraints and cut constraints. How many variables, equalities and inequalities does this problem have?

**Answer:** The dodecahedron has $12$ pentagonal faces, and $3$ faces meet at each vertex, so the number of vertices is $\lvert V \rvert = 12 \cdot 5/3 = 20$. Each vertex has degree $3$, so the number of edges is $\lvert E \rvert = 20 \cdot 3/2 = 30$.

* *Variables:* one for each edge, i.e., $30$ variables $x_e \in \lbrace 0,1 \rbrace$.
* *Equalities:* one for each vertex, i.e., $20$ equalities $\sum_{e\in\delta(v)}x_e=2$.
* *Inequalities:* there are $2^{20}-2 = 1\,048\,574$ nonempty subsets $S \subsetneq V$. But $S$ and $V \setminus S$ give the same partition, and $\delta(S) = \delta(V \setminus S)$, so the number of different inequalities is $(2^{20}-2)/2 = 2^{19}-1 = 524\,287$.

In total there are $20 + 524\,287 = 524\,307$ constraints (not counting $0 \leq x_e \leq 1$).

*Note:* Many cut constraints follow from the vertex constraints. Adding the vertex equalities for all $v \in S$ gives $2\lvert S \rvert = 2 k + \sum_{e\in\delta(S)}x_e$, where $k$ is the number of chosen edges with both endpoints in $S$. The shortest cycle in the dodecahedron is a pentagon, so for $\lvert S \rvert \leq 4$ the edges inside $S$ form no cycle and $k \leq \lvert S \rvert - 1$, hence $\sum_{e\in\delta(S)}x_e \geq 2$ holds automatically. Only the partitions with $5 \leq \lvert S \rvert \leq 15$ need to be checked; their number is ${\displaystyle \frac{1}{2}\sum_{k=5}^{15} \binom{20}{k} = 518\,092}$. In practice such constraints are not all written down at once, but added only when the current solution violates one of them. $\square$




## References

<a id="Ber2009"></a>**[Ber2009]** D.Bertsimas, *Introduction to Mathematical Programming*, MIT OpenCourseWare, Massachusetts Institute of Technology, Fall 2009. Available at [https://bit.ly/493SnRh](https://bit.ly/493SnRh), [Archived](https://web.archive.org/web/20221007151158/https://ocw.mit.edu/courses/6-251j-introduction-to-mathematical-programming-fall-2009/).

<a id="Cam16"></a>**[Cam16]** O.A.Camarena, *Math 340: Linear Programming*, National Autonomous University of Mexico, Fall 2016. Available at [https://bit.ly/4fmrfzp](https://bit.ly/4fmrfzp), [Archived:Cam16](https://web.archive.org/web/20201022041337/https://www.matem.unam.mx/~omar/math340/index.html).

<a id="Goe08"></a>**[Goe08]** M. Goemans, *Advanced Algorithms*, MIT OpenCourseWare, Massachusetts Institute of Technology, Spring 2008. Available at [https://bit.ly/40IoKmh](https://bit.ly/40IoKmh), [Archived:Goe08](https://web.archive.org/web/20220531183759/https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2008/).

<a id="Lee2023"></a>**[Lee2023]** J.Lee, *A First Course in Linear Optimization*, 4th ed., Ann Arbor, Michigan, 2024. Available at [https://github.com/jon77lee/JLee_LinearOptimizationBook](https://github.com/jon77lee/JLee_LinearOptimizationBook).

<a id="Str18"></a>**[Str18]** G.Strang, *MIT 18.065 Matrix Methods in Data Analysis*, MIT OpenCourseWare, Massachusetts Institute of Technology, Spring 2018. Available at [https://bit.ly/40H8H8z](https://bit.ly/40H8H8z), [YouTube](https://youtu.be/feb9j65Iz4w?si=mtQZZxM6jex8zCAp).

<a id="Wri97"></a>**[Wri97]** S.J.Wright, *Primal-Dual Interior-Point Methods*, SIAM, Philadelphia, 1997.

<!--
[https://ocw.mit.edu/courses/mathematics/18-086-mathematical-methods-for-engineers-ii-spring-2006/video-lectures/lecture-28-linear-programming-and-duality/](https://ocw.mit.edu/courses/mathematics/18-086-mathematical-methods-for-engineers-ii-spring-2006/video-lectures/lecture-28-linear-programming-and-duality/) -- MIT lecture
[Max Flow to Linear Programming](http://www.cs.cmu.edu/~odonnell/toolkit13/lecture14.pdf) -- Duality in graph problems, including maximum flow.
[Shadow Price](https://economics.stackexchange.com/questions/21796/linear-programming-shadow-price-range) -- An explanation of what a "shadow price" is.
-->
