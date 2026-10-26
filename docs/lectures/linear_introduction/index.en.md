---
layout: default
title: "Introduction to Linear Programming"
lang: en
permalink: /lectures/linear_introduction/en/
---
# 9. Introduction to Linear Programming

In this chapter we learn why we need to maximize linear expressions, which is usually called *linear programming*, and why linear optimization problems are written in a particular form.

**Learning outcomes:** 

* Write optimization problems as linear programs.
* Analyze matrix (zero-sum) games. 
* Solve linear programming problems with the simplex algorithm.

## Standard Optimization Problems

**Types of optimization problems**

In optimization problems we maximize (or minimize) some expression (for example, profit or cost), either over the whole domain of the expression or subject to given conditions, also called constraints.

* Unconstrained optimization: minimize $f(x_1, x_2, \ldots, x_n)$. If $f$ is a linear function, it can take arbitrarily large (or small) values.

* Constrained optimization: minimize $f(x_1, x_2, \ldots, x_n)$ subject to

  $$
  \begin{array}{l}
  c_1(x_1, x_2, \ldots, x_n) \geq 0, \ldots, c_k(x_1, x_2, \ldots, x_n) \geq 0,\\
  d_1(x_1, x_2, \ldots, x_n) = 0, \ldots, d_{\ell}(x_1, x_2, \ldots, x_n) = 0.\\
  \end{array}
  $$

**Linear programming:** minimize $\displaystyle \sum\limits_{i=1}^{n} b_ix_i$ subject to

$$
\left\{ \begin{array}{l}
c_{11} x_1 + c_{12} x_2 + \ldots + c_{1n} x_n \leq d_1,\\
\ldots,\\
c_{m1} x_1 + c_{m2} x_2 + \ldots + c_{mn} x_n \leq d_m,
\end{array} \right.
$$

> *Note:* The word "programming" is used in the sense of "planning". Some types of optimization problems have been called programming since the 1920s.

**Quadratic programming** (*Not covered in this course, but also important in practice.*)

Minimize the expression

$$
\sum\limits_{i,j=1}^{n} a_{ij}x_ix_j +  \sum\limits_{i=1}^{n} b_ix_i
$$

subject to

$$
\left\{
\begin{array}{l}
c_{11} x_1 + c_{12} x_2 + \ldots + c_{1n} x_n \leq d_1,\\
\ldots,\\
c_{m1} x_1 + c_{m2} x_2 + \ldots + c_{mn} x_n \leq d_m,
\end{array} \right.
$$

Here the function to minimize is quadratic, but the constraints are linear.

**Integer programming** (linear programming over the integers): the problem is the same as in linear programming, with the extra condition that all $x_1, x_2, \ldots, x_n$ are integers.

Integer linear programs can describe many interesting and practically important problems, but no algorithm is known that solves an arbitrary integer program fast (in polynomial time).


## Graphical Interpretation of Linear Programs

**The general LP problem:** Linear programming describes many practical problems, and efficient algorithms exist for it.

The general LP problem: find $\textcolor{blue}{\max\left(c_1x_1 + \ldots + c_nx_n\right)}$ subject to the constraints

$$
\left\{
\begin{array}{l}
a_{11}x_1 + a_{12}x_2 + \ldots + a_{1n}x_n \leq b_1\\
\ldots\\
a_{m1}x_1 + a_{m2}x_2 + \ldots + a_{mn}x_n \leq b_m
\end{array} \right.
$$

**A two-dimensional example:** find $\textcolor{blue}{\max(2x_1 + 3x_2)}$, where

$$
\left\{ \begin{array}{l}
x_1 - 2x_2 \leq 4,\\
x_1 + x_2 \leq 18,\\
x_2 \leq 10,\\
x_1,x_2 \geq 0.
\end{array} \right.
$$

> *Note:* Every maximization problem is equivalent to some minimization problem (and vice versa). For example: $\max(2x_1 + 3x_2) = -\min(-2x_1 - 3x_2).$ From now on we consider only maximization problems.

**Graphical interpretation of the example:** find $\textcolor{blue}{\max(2x_1 + 3x_2)}$, where

$$
\left\{ \begin{array}{l}
x_1 - 2x_2 \leq 4,\\
x_1 + x_2 \leq 18,\\
x_2 \leq 10,\\
x_1,x_2 \geq 0.
\end{array} \right.
$$

![Graphical interpretation of the LP problem](figs/graphical-interpretation.png)

The figure makes the solution easy to see: it is the point $(8,10)$. In higher dimensions such a picture can be hard to draw. In typical LP problems the *feasible region* is bounded. Otherwise the maximum may not exist at all: the expression can take arbitrarily large values. Before solving an LP, one often checks whether the feasible region is bounded.

**Where the optimum lies:** The figures show two important facts:

* **Fact 1:** The objective function reaches its maximum at a corner of the feasible region.
* **Fact 2:** If $a_1x_1 + \ldots + a_nx_n$ does not reach its maximum at some corner, then at one of the adjacent corners $a_1x_1 + \ldots + a_nx_n$ has a larger value.

In two dimensions, for example, Fact 2 can be checked with the geometric interpretation by considering
cases:

* **(a)** If the objective function is smaller at all neighboring corners, $c_1x_1 + c_2x_2 \leq c$, then the corner is a maximum.
* **(b)** If the objective function is larger at all neighboring corners, $c_1x_1+c_2x_2 \geq c$, then the corner is a minimum.
* **(c)** Otherwise the corner is neither a maximum nor a minimum; then there is both a neighboring corner with a larger value of the objective function $c_1x_1+c_2x_2$ and one with a smaller value.

![The maximum is located at corners of the feasible region](figs/locate-maximum.png)

In higher dimensions, too, the maximum or minimum is always located at some "corner" of the region,
because a region defined by a system of linear inequalities is always *closed* and *convex*.

**Definition:** (1) A geometric figure is called closed if, together with every convergent sequence of points $(\mathbf{a}^{(n)})$, 
it also contains the limit $\mathbf{a}^{\ast}$ of this sequence (in other words, it contains the region together with its whole boundary).  
(2) A geometric figure is called convex if, together with any two points $\mathbf{a}$ and $\mathbf{b}$, it 
also contains the whole segment with points $\mathbf{x}(t) = (1-t)\mathbf{a} + t\mathbf{b}$, where $t \in [0;1]$. 



## Examples of Linear Programs

### The Diet Problem

We are given constraints (human nutritional requirements) and must decide which food products to buy.

* **Goal:** Minimize the cost of a diet that satisfies all nutritional requirements.
* **Variables:** $x_1, x_2, \ldots, x_n$ denote the amounts of different food products included in the diet.
* **Objective function:** $\textcolor{blue}{\min\left( z = c_1x_1 + c_2x_2 + \ldots + c_nx_n \right)}$, where $c_i$ is the cost of one unit of the $i$-th food product.
* **Constraints:** Reach the required amount of nutrients, for example calories, protein, vitamins.

  $$
  \begin{array}{ll}
  a_{11}x_1 + a_{12}x_2 + \ldots + a_{1n}x_n \geq d_1 & (\text{Nutrient 1}) \\
  a_{21}x_1 + a_{22}x_2 + \ldots + a_{2n}x_n \geq d_2 & (\text{Nutrient 2}) \\
  &\vdots \\
  a_{m1}x_1 + a_{m2}x_2 + \ldots + a_{mn}x_n \geq d_m & (\text{Nutrient m}) \\
  x_i \geq 0 & (\text{One cannot eat a negative amount of food})\\
  \end{array}
  $$

> *Note:* If the amounts of products are measured in integers (for example, a whole number of packages), we get integer linear programming. If some variables must be integers while others may be arbitrary real numbers, it is mixed integer programming.

**Leonid Kantorovich (1912-1986):** Optimal use of raw materials in the plywood industry (1939). Early optimization problems were often related to production planning.





### Maximum Flow in a Directed Graph

Flow maximization problems are a special case of linear programming problems. 
They have specialized algorithms (the Ford–Fulkerson or Edmonds–Karp algorithms), 
but they can also be solved with linear programming tools and 
used to illustrate the theory of linear programming (including the dual problem).


**Concepts of the maximum flow problem:**

* We are given a directed flow network $N = (V, E)$ with two vertices $s, t \in V$, called the *source* and the *sink*, respectively.
* Various functions can be defined on the edges $(u,v)$ of the graph; they are denoted $g(u,v)$ or $g_{uv}$.

**Definition:** The *capacity* of an edge is the maximum flow that can be assigned to that 
edge. Capacity is denoted $c: E \to \mathbb{R}^+$.

**Definition:** A *flow* is a function $f : E \to \mathbb{R}$ that satisfies the following conditions:

* *Capacity constraint:* the flow on every edge is non-negative and does not exceed its capacity, i.e., $0 \leq f_{uv} \leq c_{uv}$ for all $(u, v) \in E$.
* *Flow conservation:* at every vertex except the source and the sink, the sum of incoming flows equals the sum of outgoing flows:

  $$
  \forall v \in V \setminus \{s, t\} \quad
  \sum_{u:\ (u, v) \in E} f_{uv} = \sum_{u:\ (v, u) \in E} f_{vu}.
  $$

**Definition:** The *value of a flow* is the amount of flow that moves from the source to the sink: the flow leaving the source minus the flow entering the source. If no edge enters the source and no edge leaves the sink (as in the example below), then

$$
|f| = \sum_{v:\ (s,v) \in E} f_{sv} = \sum_{u:\ (u,t) \in E} f_{ut}.
$$

**Definition:** The *maximum flow problem* is to find a flow (the flow value on every edge of the graph) that carries as much as possible from the source to the sink, i.e., to find a flow $f_\textrm{max}$ with the maximum value $|f|$.

> *Note:* Between two vertices $u, v$ there may be edges in both directions, $(u,v)$ and $(v,u)$, with different capacities. If both carry a nonzero flow, both flows can be reduced by the smaller of them (the flow from $u$ to $v$ and back cancels out), so we may assume that the flow is $0$ in at least one direction. In an undirected graph each edge $\lbrace u, v \rbrace$ is replaced by two directed edges $(u,v)$ and $(v,u)$ with the same capacity. Some books define flow antisymmetrically ($f_{uv} = -f_{vu}$); this is a different notation for the same concept.

**Example:** Find the maximum flow from $S$ to $T$ in the graph where each edge is labeled with its capacity:

![Directed graph with edge capacities](figs/graph-capacities.png)

To each edge $(u,v)$ we assign a variable $f_{uv}$, the flow along this edge. We maximize the flow leaving $S$; the constraints are flow conservation at each intermediate vertex $A, B, C, D$ and the capacity constraints:

$$
\textcolor{blue}{\max \left( f_{SA} + f_{SC} \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{ll}
f_{SA} + f_{CA} = f_{AB} & (A),\\
f_{AB} + f_{CB} = f_{BT} + f_{BD} & (B),\\
f_{SC} = f_{CA} + f_{CB} + f_{CD} & (C),\\
f_{CD} + f_{BD} = f_{DT} & (D),\\
0 \leq f_{SA} \leq 11,\;\; 0 \leq f_{SC} \leq 14,\;\; 0 \leq f_{AB} \leq 15, & \\
0 \leq f_{CA} \leq 3,\;\; 0 \leq f_{CB} \leq 3,\;\; 0 \leq f_{CD} \leq 7, & \\
0 \leq f_{BT} \leq 12,\;\; 0 \leq f_{BD} \leq 2,\;\; 0 \leq f_{DT} \leq 15. & \\
\end{array} \right.
$$

The program [figs/max-flow-lp.py](figs/max-flow-lp.py) finds the maximum flow $|f| = 21$, for example:

| Edge | $SA$ | $SC$ | $AB$ | $CA$ | $CB$ | $CD$ | $BT$ | $BD$ | $DT$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Flow $f_{uv}$ | 11 | 10 | 14 | 3 | 0 | 7 | 12 | 2 | 9 |
| Capacity $c_{uv}$ | 11 | 14 | 15 | 3 | 3 | 7 | 12 | 2 | 15 |

The optimal flow is not unique: for example, one can take $f_{CA} = 0$, $f_{CB} = 3$, $f_{AB} = 11$. A larger flow is impossible: if the vertex set is split into $\lbrace S, A, B, C \rbrace$ and $\lbrace D, T \rbrace$, then the only edges from the first part to the second are $BT$, $BD$ and $CD$ with total capacity $12 + 2 + 7 = 21$. Such a partition is a *minimum cut*; it is the solution of the dual of the maximum flow problem.




### The Single-Source Shortest Path Problem

We are given a graph with non-negative edge lengths $w_{uv}$ and a start vertex $s$. We must find the lengths of the shortest paths from $s$ to all other vertices.

To each vertex $v$ we assign a variable $x_{v}$, the distance from the start vertex $s$ (it is also called the *potential* of the vertex).

**Objective function:**
Maximize the sum of all variables $\sum_{v} x_{v}$. (If only one target vertex $t$ is needed, we can maximize $x_t$; then $x_t$ will be the distance to $t$, but the other $x_v$ may be smaller than the distances.)

**Constraints:**

* At the start vertex, $x_s = 0$.
* For each directed edge $(u,v)$: $x_{v}-x_{u} \leq w_{uv}$ (the *triangle inequality*: $v$ cannot be farther away than $u$ plus the length of edge $(u,v)$). In an undirected graph each edge $\lbrace u,v \rbrace$ gives two inequalities: $x_v - x_u \leq w_{uv}$ and $x_u - x_v \leq w_{uv}$.

It seems strange that shortest paths are found by *maximization*. However, the constraints do not allow any $x_v$ to exceed the distance $d(s,v)$: adding up the inequalities along the edges of a shortest path $s = v_0, v_1, \ldots, v_k = v$ gives $x_v - x_s \leq d(s,v)$. On the other hand, $x_v = d(s,v)$ satisfies all inequalities. Hence the maximum is reached when every $x_v$ is exactly the distance. (If some vertex is not reachable from $s$, the LP is unbounded.)

**Example:** Find the lengths of the shortest paths from vertex $A$ to all other vertices in this undirected graph:

![Graph for finding shortest paths from vertex A](figs/shortest-paths-example.svg)

$$
\textcolor{blue}{\max \left( x_A + x_B + x_C + x_D + x_E + x_F \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{ll}
x_A = 0, & \\
\lvert x_B - x_A \rvert \leq 7, & \lvert x_C - x_A \rvert \leq 9,\\
\lvert x_F - x_A \rvert \leq 14, & \lvert x_C - x_B \rvert \leq 10,\\
\lvert x_D - x_B \rvert \leq 15, & \lvert x_D - x_C \rvert \leq 11,\\
\lvert x_F - x_C \rvert \leq 2, & \lvert x_E - x_D \rvert \leq 6,\\
\lvert x_E - x_F \rvert \leq 9. & \\
\end{array} \right.
$$

Here $\lvert x_v - x_u \rvert \leq w$ is shorthand for the two linear inequalities $x_v - x_u \leq w$ and $x_u - x_v \leq w$.

The program [figs/shortest-paths-lp.py](figs/shortest-paths-lp.py) reads the graph from the file [figs/shortest-paths-example.json](figs/shortest-paths-example.json) (the same file from which [figs/shortest-paths-example.py](figs/shortest-paths-example.py) draws the figure) and finds:

| Vertex $v$ | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ |
| --- | --- | --- | --- | --- | --- | --- |
| Distance $x_v = d(A,v)$ | 0 | 7 | 9 | 20 | 20 | 11 |
| Previous vertex on the path | -- | $A$ | $A$ | $C$ | $F$ | $C$ |

The value of the objective function is $0 + 7 + 9 + 20 + 20 + 11 = 67$. The shortest path tree consists of the edges on which the inequality becomes an equality; for example, the shortest path to $E$ is $A \to C \to F \to E$ with length $9 + 2 + 9 = 20$.

> *Note:* In practice, single-source shortest paths are found with Dijkstra's algorithm, not with LP: with a binary heap it runs in $O((\lvert V \rvert + \lvert E \rvert) \log \lvert V \rvert)$ time and is simple, while a general LP solver is much slower and uses more memory. If edges may have negative lengths, the Bellman–Ford algorithm is used. The LP formulation is useful for theory: its dual is a minimum-cost flow that sends one unit from $s$ to every other vertex, and additional linear constraints are easy to add to the LP formulation.




### Optimal Prefix Code Lengths

Huffman's algorithm (see the lecture [Entropy and Huffman Trees]({{ '/lectures/lossless_entropy_and_huffman/' | relative_url }})) also solves an optimization problem. We are given messages with probabilities $p_1, \ldots, p_n$ and must choose codeword lengths $\ell_1, \ldots, \ell_n$ so that the average code length is minimal. By the Kraft–McMillan inequality, a prefix code with lengths $\ell_i$ exists if and only if $\sum_i 2^{-\ell_i} \leq 1$. So the *optimal prefix code problem* is:

$$
\textcolor{blue}{\min \left( \sum_{i=1}^n p_i \ell_i \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
\sum\limits_{i=1}^n 2^{-\ell_i} \leq 1,\\
\ell_i \in \lbrace 1, 2, 3, \ldots \rbrace.\\
\end{array} \right.
$$

The objective function is linear, but the Kraft inequality is not linear in $\ell_i$, and the variables must be integers.

**Relaxation:** If the integrality condition is dropped (real $\ell_i > 0$ are allowed), the optimum is $\ell_i = -\log_2 p_i$, and the minimum value is the entropy:

$$
\sum_{i=1}^n p_i \ell_i = -\sum_{i=1}^n p_i \log_2 p_i = H(p).
$$

(This can be checked with Lagrange multipliers; the Kraft inequality holds with equality because $\sum_i 2^{\log_2 p_i} = \sum_i p_i = 1$.) So the entropy is the optimum of the relaxation of this optimization problem, while the Huffman code is the optimum of the integer problem. The relaxation gives the lower bound $H(p) \leq L_{\text{Huffman}}$. On the other hand, the rounded lengths $\ell_i = \lceil -\log_2 p_i \rceil$ satisfy the Kraft inequality and give an average length less than $H(p) + 1$, so $L_{\text{Huffman}} < H(p) + 1$. The gap between the relaxation and the integer solution is less than $1$ bit -- this is exactly the "$+1$" in Shannon's theorem.

**Integer linear program:** The problem can be rewritten with linear constraints by introducing binary variables $y_{i\ell} \in \lbrace 0,1 \rbrace$: $y_{i\ell} = 1$ means that the codeword of the $i$-th message has length $\ell$ (it suffices to take $\ell = 1, \ldots, n-1$):

$$
\textcolor{blue}{\min \left( \sum_{i=1}^n \sum_{\ell=1}^{n-1} \ell\, p_i\, y_{i\ell} \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{ll}
\sum\limits_{\ell=1}^{n-1} y_{i\ell} = 1 & \text{for each}\ i \;\;(\text{one length per message}),\\
\sum\limits_{i=1}^n \sum\limits_{\ell=1}^{n-1} 2^{-\ell}\, y_{i\ell} \leq 1 & (\text{Kraft inequality}),\\
y_{i\ell} \in \lbrace 0, 1 \rbrace. & \\
\end{array} \right.
$$

The numbers $2^{-\ell}$ are constants here, so all constraints are linear.

**Example:** Probabilities $p = (0.4;\ 0.3;\ 0.2;\ 0.1)$. The program [figs/prefix-code-lengths.py](figs/prefix-code-lengths.py) solves the integer LP and compares it with the Huffman code:

| | $\ell_1$ | $\ell_2$ | $\ell_3$ | $\ell_4$ | Average length |
| --- | --- | --- | --- | --- | --- |
| Relaxation $-\log_2 p_i$ | $1.322$ | $1.737$ | $2.322$ | $3.322$ | $H(p) \approx 1.846$ |
| Integer LP | $1$ | $2$ | $3$ | $3$ | $1.9$ |
| Huffman code | $1$ | $2$ | $3$ | $3$ | $1.9$ |
| $\lceil -\log_2 p_i \rceil$ | $2$ | $2$ | $3$ | $4$ | $2.4$ |

The integer LP finds the same lengths as Huffman's algorithm, and $1.846 \leq 1.9 < 2.846$. Rounding up gives a valid but non-optimal code ($2.4$); it also stays within Shannon's bound $H(p) + 1$.

In practice, of course, the optimal lengths are found with Huffman's algorithm in $O(n \log n)$ time; integer LP is NP-hard in general. The example shows how the same problem looks in the language of optimization: the entropy is the optimum of the relaxation, the Huffman code is the integer optimum.




### The Resource Allocation Problem

A popular approximation of a well-known problem in economics (the *resource allocation problem*). Being able to solve it efficiently may answer a philosophical question: do we need a market?

* **Goal:** Maximize profit by choosing the optimal production volumes of different products while respecting the existing constraints.
* **Variables:** $x_1, x_2, \ldots, x_n$ are the production volumes of the products.
* **Objective function:** $\textcolor{blue}{\max \left( z = c_1x_1 + c_2x_2 + \ldots + c_nx_n \right)}$, where $c_i$ is the profit from producing one unit of the $i$-th product.
* **Constraints:** Availability of resources -- labor, raw materials, capital.

  $$
  \begin{array}{ll}
  a_{11}x_1 + a_{12}x_2 + \ldots + a_{1n}x_n \leq b_1 & (\text{Resource 1}) \\
  a_{21}x_1 + a_{22}x_2 + \ldots + a_{2n}x_n \leq b_2 & (\text{Resource 2}) \\
  &\vdots \\
  a_{m1}x_1 + a_{m2}x_2 + \ldots + a_{mn}x_n \leq b_m & (\text{Resource m}) \\
  x_i \geq 0 & (\text{Negative amounts cannot be produced})\\
  \end{array}
  $$

**Numerical example:**

* There are enough cabbage seeds to sow 3 hectares.
* There are enough carrot seeds to sow 4 hectares.
* 5 free hectares are available.
* The profit is 1200 EUR per hectare of cabbage and 1700 EUR per hectare of carrots. The task is to maximize profit.

**Formalized problem:** $\textcolor{blue}{\max \left( 1200x_k + 1700x_b \right)}$, where

$$
\left\{ \begin{array}{l}
x_k \leq 3,\\
x_b \leq 4\\
x_k + x_b \leq 5,\\
x_k,x_b \geq 0.
\end{array} \right.
$$

1. Draw the feasible region; put cabbage on the horizontal axis and carrots on the vertical axis.
2. Find and mark the corners of the feasible region -- the points of the 2D plane where at least 2 of the given inequalities become equalities.
3. Draw the profit gradient vector $(1200, 1700)$ in the plane.
4. Find the corner of the feasible region that is farthest in the direction of this gradient vector.

**Definition:** A *scalar field* is a real-valued function defined at every point of space. For example, in two dimensions each $(x_1,x_2)$ has a value $f(x_1,x_2)$. For example, for each choice of cabbage and carrot areas one can compute the profit: $f(x_k,x_b) = 1200x_k + 1700 x_b$.

> *Note:* Scalar fields have nothing to do with finite fields (the algebraic structure that appeared in Reed–Solomon codes).

**Definition:** The *gradient* of a scalar field $f$ is the vector $\nabla f(x_1, x_2)$ defined for each $(x_1,x_2) \in \mathbb{R}^2$ as follows:

$$
\nabla f(x_1, x_2) = \left( \frac{\partial f}{\partial x_1}(x_1, x_2), \frac{\partial f}{\partial x_2}(x_1, x_2) \right)
$$

In our example the partial derivatives of the profit function are $1200$ and $1700$ (constant values). So the profit function grows uniformly in the direction of the gradient vector.




## Two-Player Matrix Games

Two players $X$ and $Y$ simultaneously choose one of their moves each: player $X$
chooses one of $n$ rows, player $Y$ chooses one of $m$ columns. The game is described by the
*payoff matrix* $A = (a_{ij})$ of size $n \times m$: if $X$ chooses the $i$-th row and $Y$ chooses
the $j$-th column, then $X$ pays player $Y$ the amount $a_{ij}$. Player $X$ minimizes this
payment, player $Y$ maximizes it.

> *Note:* These are *zero-sum games*: everything $X$ pays goes to $Y$, so the
> sum of both players' gains is $0$. If $a_{ij} < 0$, then in fact $Y$ pays player $X$.
> Games where this is not the case (for example, the prisoner's dilemma) are discussed at the end of this section.

### Pure Strategies and Saddle Points

A *pure strategy* means always choosing the same move.

**Example:** Consider the game with the payoff matrix

$$
A = \left( \begin{array}{cc}
1 & 2 \\
4 & 8 \\
\end{array} \right).
$$

For player $Y$, column 2 is better than column 1 whatever $X$ chooses ($2 > 1$ and
$8 > 4$); we say that column 2 *dominates* column 1. Similarly, for player $X$ row 1 dominates
row 2 ($1 < 4$ and $2 < 8$). So $X$ chooses row 1, $Y$ chooses column 2, and $X$ pays
$a_{12} = 2$. Neither player gains by changing their choice unilaterally.

**Definition:** A matrix element $a_{rs}$ is a *saddle point* if it is the largest in its row and
the smallest in its column.

If $a_{rs}$ is a saddle point, then by choosing row $r$ player $X$ pays at most $a_{rs}$
(it is the row maximum), while by choosing column $s$ player $Y$ receives at least $a_{rs}$
(it is the column minimum). So the optimal strategies of both players are pure, and the
outcome of the game is $a_{rs}$. In the previous example the saddle point is $a_{12} = 2$.

**Example:** In the game "rock, paper, scissors" both players have three moves: rock (R),
paper (P) and scissors (S). The winner receives $1$ from the loser; in a draw nobody
pays. With rows and columns in the order R, P, S, the payoff matrix is

$$
A = \left( \begin{array}{ccc}
0 & 1 & -1 \\
-1 & 0 & 1 \\
1 & -1 & 0 \\
\end{array} \right).
$$

This matrix has no saddle point: the largest element in every row is $1$, while the
smallest element in every column is $-1$. Against any pure strategy the opponent has a best
response that always wins. Therefore in such games the moves must be chosen at random.

### Mixed Strategies

A *mixed strategy* chooses each move with a certain probability. A mixed strategy of player
$X$ is described by a probability vector $\mathbf{x} = (x_1,\ldots,x_n)^T$, and one of player $Y$ by
a probability vector $\mathbf{y} = (y_1,\ldots,y_m)^T$, where

$$
x_1 + \ldots + x_n = 1,\quad y_1 + \ldots + y_m = 1,\quad x_i \geq 0,\; y_j \geq 0.
$$

(Such vectors are also called *stochastic vectors*.) A pure strategy is a special case of a
mixed strategy: a vector with a single one and zeros elsewhere.

If the players choose their moves independently, the average payment (the expected value) that
$X$ pays player $Y$ is

$$
\mathbf{x}^T A \mathbf{y} = \sum_{i=1}^{n}\sum_{j=1}^{m} x_i\,a_{ij}\,y_j.
$$

**Example:** In "rock, paper, scissors" player $X$ chooses $\mathbf{x}^T = (1/2, 0, 1/2)$,
and player $Y$ chooses $\mathbf{y}^T = (1/2, 1/3, 1/6)$. The average payment is

$$
\mathbf{x}^T A \mathbf{y} =
\left( \begin{array}{ccc}
\frac{1}{2} & 0 & \frac{1}{2} \end{array} \right) \cdot
\left( \begin{array}{ccc}
0 & 1 & -1 \\
-1 & 0 & 1 \\
1 & -1 & 0 \\
\end{array} \right) \cdot
\left(
\begin{array}{c}
\frac{1}{2}\\
\frac{1}{3}\\
\frac{1}{6}
\end{array} \right) =
\left( \begin{array}{ccc}
\frac{1}{2} & 0 & -\frac{1}{2} \end{array} \right) \cdot
\left(
\begin{array}{c}
\frac{1}{2}\\
\frac{1}{3}\\
\frac{1}{6}
\end{array} \right) = \frac{1}{4} - \frac{1}{12} = \frac{1}{6}.
$$

The coordinates of the vector $\mathbf{x}^T A = (1/2,\, 0,\, -1/2)$ are the average payments when $Y$ chooses
R, P or S, respectively. If $Y$ knows $\mathbf{x}$, it is better for $Y$ to always choose R
(the largest coordinate), and $X$ will pay $1/2$ on average. In contrast, with $\mathbf{x}^T = (1/3, 1/3, 1/3)$
we get $\mathbf{x}^T A = (0, 0, 0)$, so on average $X$ loses nothing, whatever $Y$ does.
Therefore the strategy $(1/2, 0, 1/2)$ is not optimal.

This example shows a general property. If $Y$ knows player $X$'s strategy $\mathbf{x}$, then
$Y$'s *best response* is a pure strategy: the column with the largest coordinate of the vector
$\mathbf{x}^T A$. Since $\mathbf{x}^T A \mathbf{y}$ is the average of the coordinates of this vector with
weights $y_j$, it cannot exceed the largest coordinate:

$$
\max_{\mathbf{y}} \mathbf{x}^T A \mathbf{y} = \max_{j} \left(\mathbf{x}^T A\right)_j.
$$

Similarly, player $X$'s best response to $\mathbf{y}$ is the row with the smallest coordinate of the vector $A\mathbf{y}$:
$\min_{\mathbf{x}} \mathbf{x}^T A \mathbf{y} = \min_i \left(A\mathbf{y}\right)_i$.

**Example:** If player $X$ chooses $\mathbf{x}^T = (0.7, 0.2, 0.1)$ (rock with probability $70\%$,
paper with $20\%$, scissors with $10\%$), then $\mathbf{x}^T A = (-0.1,\, 0.6,\, -0.5)$, and player $Y$'s
best response is $\mathbf{y}^T = (0, 1, 0)$ -- always choose paper.

**Definition:** The *value* of a matrix game is the smallest average payment that player $X$ can
guarantee if $Y$ knows $X$'s mixed strategy and responds to it in the best possible way:

$$
v(A) = \min_{\mathbf{x}} \max_{\mathbf{y}} \mathbf{x}^T A \mathbf{y}
= \min_{\mathbf{x}} \max_{j} \left(\mathbf{x}^T A\right)_j.
$$

Here the minimum is taken over all probability vectors $\mathbf{x}$, the maximum over all $\mathbf{y}$.
A strategy $\mathbf{x}^{\ast}$ at which this minimum is reached is an *optimal strategy* of player $X$.

### Optimal Strategy with a Linear Program

<!-- https://www.matem.unam.mx/~omar/math340/matrix-games.html -->

The expression $\min_{\mathbf{x}} \max_j (\mathbf{x}^T A)_j$ is not linear, but it can be turned into a linear
program (see *Matrix Games* [Cam16]({{ '/lectures/linear_algorithms/' | relative_url }}#Cam16)).
We introduce an extra variable $z$ that is not smaller than any coordinate of the vector $\mathbf{x}^T A$, and
minimize it. At the optimum, $z$ equals the largest coordinate. Player $X$'s linear program
(variables $x_1,\ldots,x_n$ and $z$):

$$
\textcolor{blue}{\min(z)},\;\text{where}
\left\{ \begin{array}{l}
z \geq a_{1j}x_1 + a_{2j}x_2 + \ldots + a_{nj}x_n \quad (j = 1,\ldots,m), \\
x_1 + x_2 + \ldots + x_n  = 1,\\
x_1, x_2, \ldots, x_n \geq 0.
\end{array} \right.
$$

Player $Y$ reasons symmetrically: whatever $\mathbf{y}$ $Y$ chooses, $X$ will respond with the row where the
coordinate of $A\mathbf{y}$ is the smallest. So $Y$ maximizes $\min_i (A\mathbf{y})_i$; this is a linear
program with variables $y_1,\ldots,y_m$ and $w$:

$$
\textcolor{blue}{\max(w)},\;\text{where}
\left\{ \begin{array}{l}
w \leq a_{i1}y_1 + a_{i2}y_2 + \ldots + a_{im}y_m \quad (i = 1,\ldots,n), \\
y_1 + y_2 + \ldots + y_m  = 1,\\
y_1, y_2, \ldots, y_m \geq 0.
\end{array} \right.
$$

Both programs have feasible solutions, and their objective functions are bounded
($z \geq \min_{i,j} a_{ij}$ and $w \leq \max_{i,j} a_{ij}$), so both have an optimum. Moreover,
these programs are *dual* to each other (see the section on duality below), so by the strong
duality theorem their optimal values coincide. This is one way to prove
von Neumann's minimax theorem (1928).

**Theorem (minimax theorem):** For every matrix $A$ both players have optimal
mixed strategies $\mathbf{x}^{\ast}$, $\mathbf{y}^{\ast}$, and

$$
v(A) = \min_{\mathbf{x}} \max_{\mathbf{y}} \mathbf{x}^T A \mathbf{y}
= \max_{\mathbf{y}} \min_{\mathbf{x}} \mathbf{x}^T A \mathbf{y}.
$$

So it does not matter which player "reveals" their strategy first: player $X$ can
guarantee to pay at most $v(A)$, and $Y$ can guarantee to receive at least $v(A)$.

**Corollary (optimality check):** For any probability vectors $\mathbf{x}$, $\mathbf{y}$

$$
\min_i \left(A\mathbf{y}\right)_i \leq \mathbf{x}^T A \mathbf{y} \leq \max_j \left(\mathbf{x}^T A\right)_j,
$$

so $\min_i (A\mathbf{y})_i \leq v(A) \leq \max_j (\mathbf{x}^T A)_j$. Hence the strategies
$\mathbf{x}^{\ast}$ and $\mathbf{y}^{\ast}$ are optimal if and only if

$$
\max_j \left((\mathbf{x}^{\ast})^T A\right)_j = \min_i \left(A \mathbf{y}^{\ast}\right)_i,
$$

and this common value is $v(A)$.

### A Numerical Example of a Game

<!-- https://youtu.be/feb9j65Iz4w?si=tGIUByy4Hc5fwr_b -->

Consider the game with the payoff matrix (see [Str18]({{ '/lectures/linear_algorithms/' | relative_url }}#Str18))

$$
A = \left( \begin{array}{cc}
1 & 8 \\
4 & 2 \\
\end{array} \right).
$$

There is no saddle point (the row maxima are $8$ and $4$, the column minima are $1$ and $2$).
We solve both linear programs with the Python library `pulp`.
Player $X$'s program ($\min z$, where $z \geq x_1 + 4x_2$ and $z \geq 8x_1 + 2x_2$):

```python
from pulp import *

model = LpProblem(sense=LpMinimize)

x1 = LpVariable(name="x1", lowBound=0)
x2 = LpVariable(name="x2", lowBound=0)
z = LpVariable(name="z")

model += z - 1*x1 - 4*x2 >= 0
model += z - 8*x1 - 2*x2 >= 0
model += x1 + x2 == 1 
model += z  # Objective function

status = model.solve(PULP_CBC_CMD(msg=False))
print(f"(x1,x2) = {x1.value(), x2.value()}")
print(f"Value of the game = {model.objective.value()}")
```

The optimal strategy is $(\mathbf{x}^{\ast})^T = (2/9, 7/9)$, and $z = 3\frac{1}{3}$.

Player $Y$'s program ($\max w$, where $w \leq y_1 + 8y_2$ and $w \leq 4y_1 + 2y_2$):

```python
from pulp import *

model = LpProblem(sense=LpMaximize)

y1 = LpVariable(name="y1", lowBound=0)
y2 = LpVariable(name="y2", lowBound=0)
w = LpVariable(name="w")

model += 1*y1 + 8*y2 - w >= 0
model += 4*y1 + 2*y2 - w >= 0
model += y1 + y2 == 1 
model += w  # Objective function

status = model.solve(PULP_CBC_CMD(msg=False))
print(f"(y1,y2) = {y1.value(), y2.value()}")
print(f"Value of the game = {model.objective.value()}")
```

The optimal strategy is $(\mathbf{y}^{\ast})^T = (2/3, 1/3)$, and $w = 3\frac{1}{3}$ -- the same as $z$,
as the minimax theorem predicts.

We check optimality with the corollary of the minimax theorem:

$$
(\mathbf{x}^{\ast})^T A = \left(\frac{2}{9}, \frac{7}{9}\right) \cdot \left( \begin{array}{cc}
1 & 8 \\
4 & 2 \\
\end{array} \right) =
\left( \frac{2}{9} \cdot 1 + \frac{7}{9} \cdot 4,\; \frac{2}{9} \cdot 8  + \frac{7}{9} \cdot 2 \right) =
\left( \frac{10}{3}, \frac{10}{3} \right),
$$

$$
A \mathbf{y}^{\ast} = \left( \begin{array}{cc}
1 & 8 \\
4 & 2 \\
\end{array} \right) \cdot \left( \begin{array}{c}
2/3\\
1/3\\
\end{array} \right) = \left( \begin{array}{c}
10/3\\
10/3\\
\end{array} \right).
$$

So $\max_j ((\mathbf{x}^{\ast})^T A)_j = \min_i (A\mathbf{y}^{\ast})_i = 10/3$, and the value of the game is
$v(A) = 3\frac{1}{3}$: on average $X$ pays player $Y$ $3\frac{1}{3}$ units.

In both vectors all coordinates are equal. This is not a coincidence but the *indifference principle*:
if the optimal strategy $\mathbf{x}^{\ast}$ chooses the $i$-th row with
positive probability, then $(A\mathbf{y}^{\ast})_i = v(A)$, and if $\mathbf{y}^{\ast}$ chooses the $j$-th column with
positive probability, then $((\mathbf{x}^{\ast})^T A)_j = v(A)$. In other words, against the opponent's
optimal strategy all moves that a player uses give the same average result. (These are the
complementary slackness conditions for the two linear programs.)

For small games the indifference principle lets us find the optimal strategies without LP. In this example both
players use both moves, so

$$
x_1 + 4x_2 = 8x_1 + 2x_2,\;\; x_1 + x_2 = 1 \;\Rightarrow\; x_1 = \frac{2}{9};\qquad
y_1 + 8y_2 = 4y_1 + 2y_2,\;\; y_1 + y_2 = 1 \;\Rightarrow\; y_1 = \frac{2}{3}.
$$

### Non-Zero-Sum Games

If the sum of both players' gains is not constant (for example, both can gain or both can lose at the same time),
the game is described by two matrices, or by a table of pairs (player $X$'s gain, player
$Y$'s gain), and *both* players maximize their own gain. (A gain can also be negative,
for example years of prison with a minus sign.)

For such games linear programming is less useful. With LP one can find a player's
*maximin strategy* -- the one that maximizes the guaranteed gain, assuming that the other player
acts in the way that is worst for us. In a zero-sum game this is the optimal strategy, but in a non-zero-sum
game the other player has no goal of harming us: they maximize their own gain. Therefore the
central concept here is the *Nash equilibrium* -- a pair of strategies in which no
player gains by changing their strategy unilaterally. Finding a Nash equilibrium in a two-player
game is not a linear programming problem (it is solved, for example, with the Lemke–Howson algorithm).

**Example (prisoner's dilemma):**

|     | $Y$: cooperates | $Y$: defects |
| --- | --- | --- |
| $X$: cooperates | $(3,3)$ | $(0,5)$ |
| $X$: defects | $(5,0)$ | $(1,1)$ |

For each player "defects" dominates "cooperates" ($5 > 3$ and $1 > 0$), so the only Nash
equilibrium is (defects, defects) with gains $(1,1)$, although (cooperates, cooperates) would give both
more. Here the maximin strategy ("defects" guarantees $1$, "cooperates" only $0$) coincides with the
equilibrium.

**Example (the maximin strategy is not a Nash equilibrium):**

|     | $Y$: left | $Y$: right |
| --- | --- | --- |
| $X$: top | $(3,2)$ | $(0,1)$ |
| $X$: bottom | $(1,2)$ | $(1,1)$ |

Player $X$'s maximin strategy is "bottom": it guarantees a gain of $1$, while "top" may give $0$
if $Y$ chooses "right". But for player $Y$ "left" always gives more ($2 > 1$), so
$Y$ will not choose "right". The only Nash equilibrium is (top, left) with gains
$(3,2)$: $X$ knows this and chooses "top".


## The Cabbage–Carrot Problem and Its Dual

**Example:** A farmer has $5$ hectares of land. There are cabbage seeds for at most $3$ ha, 
and carrot seeds for at most $4$ ha. One hectare of cabbage gives $1200$ euros of profit, 
one hectare of carrots gives $1700$ euros. Let $x_k$ and $x_b$ denote the areas of cabbage and carrots 
in hectares:

$$
\textcolor{blue}{\max \left( 1200x_k + 1700x_b \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
x_k \leq 3,\\
x_b \leq 4,\\
x_k + x_b \leq 5,\\
x_k,x_b \geq 0.
\end{array} \right.
$$

Solution: $(x_k, x_b) = (1,4)$. Objective function: $1200 \cdot 1 + 1700 \cdot 4 = 8000$.

The feasible region is a pentagon with vertices $(0,0)$, $(3,0)$, $(3,2)$, $(1,4)$, $(0,4)$. 
The profit level lines $1200x_k + 1700x_b = z$ are parallel lines; as $z$ increases, they 
move in the direction of the gradient $\mathbf{c} = (1200, 1700)$. The last level line that 
still has a common point with the feasible region passes through the vertex $(1,4)$:

![Feasible region of the cabbage–carrot problem and the line of optimal profit](figs/cabbage-carrots-feasible.png)

*The feasible region (blue) and profit level lines; the optimal line $1200x_k + 1700x_b = 8000$ touches the region at the vertex $(1,4)$.*

**The dual problem:** How can we be sure that the point $(1,4)$ found by the program is really optimal 
(and nothing better is possible)? All three inequalities can be multiplied by non-negative numbers 
$y_1, y_2, y_3$ and added up:

$$
y_1 x_k + y_2 x_b + y_3 (x_k + x_b) = (y_1 + y_3)\,x_k + (y_2 + y_3)\,x_b \leq 3y_1 + 4y_2 + 5y_3.
$$

If $y_1 + y_3 \geq 1200$ and $y_2 + y_3 \geq 1700$, then (since $x_k, x_b \geq 0$) the left-hand side 
is not smaller than the profit $1200x_k + 1700x_b$, so $3y_1 + 4y_2 + 5y_3$ is an upper 
bound on the profit. The best (smallest) bound is sought by the *dual problem*:

$$
\textcolor{blue}{\min \left( 3y_1 + 4y_2 + 5y_3 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
y_1 + y_3 \geq 1200,\\
y_2 + y_3 \geq 1700,\\
y_1,y_2,y_3 \geq 0.
\end{array} \right.
$$

Solution: $(y_1, y_2, y_3) = (0, 500, 1200)$. Objective function: $3 \cdot 0 + 4 \cdot 500 + 5 \cdot 1200 = 8000$. 
Since the upper bound equals the profit found, $(x_k, x_b) = (1,4)$ is optimal.

**The primal and dual LP problems in matrix notation:** Let

$$
\mathbf{x} = \left( \begin{array}{c}
x_k \\
x_b \\
\end{array} \right),\;\;
\mathbf{y} = \left( \begin{array}{c}
y_1 \\
y_2 \\
y_3 \\
\end{array} \right),\;\;
\mathbf{c} = \left( \begin{array}{c}
1200 \\
1700 \\
\end{array} \right),\;\;
A = \left( \begin{array}{cc}
1 & 0 \\
0 & 1 \\
1 & 1 \\
\end{array} \right),\;\;
\mathbf{b} = \left( \begin{array}{c}
3 \\
4 \\
5 \\
\end{array} \right).
$$

$$
(P): \textcolor{blue}{\max \left( \mathbf{c}^T \mathbf{x} \right)},\;\;\text{where}\;\;
A\mathbf{x} = \left( \begin{array}{cc}
1 & 0 \\
0 & 1 \\
1 & 1 \\
\end{array} \right) \left( \begin{array}{c}
x_k \\
x_b \\
\end{array} \right) \leq \left( \begin{array}{c}
3 \\
4 \\
5 \\
\end{array} \right),\;\; \mathbf{x} \geq \mathbf{0}.
$$

$$
(D): \textcolor{blue}{\min \left( \mathbf{b}^T \mathbf{y} \right)},\;\;\text{where}\;\;
A^T\mathbf{y} = \left( \begin{array}{ccc}
1 & 0 & 1 \\
0 & 1 & 1 \\
\end{array} \right) \left( \begin{array}{c}
y_1 \\
y_2 \\
y_3 \\
\end{array} \right) \geq \left( \begin{array}{c}
1200 \\
1700 \\
\end{array} \right),\;\; \mathbf{y} \geq \mathbf{0}.
$$

Each inequality of the primal problem (row of the matrix $A$) corresponds to one dual variable $y_i$, 
and each primal variable (column of the matrix $A$) corresponds to one inequality of the dual problem.

### Interpretations of the Dual Problem

**Upper bounds.** Every feasible point $\mathbf{y}$ of the dual problem gives an upper bound 
$\mathbf{b}^T \mathbf{y}$ on the profit, even if it is not optimal. In this problem 
all three points $\mathbf{y}$ considered have $y_1 + y_3 = 1200$ and $y_2 + y_3 = 1700$, so 
the left-hand side of the summed inequality is exactly the profit:

| $(y_1, y_2, y_3)$ | Summed inequality | Bound |
| --- | --- | --- |
| $(1200, 1700, 0)$ | $1200 x_k + 1700 x_b \leq 1200 \cdot 3 + 1700 \cdot 4$ | $10400$ |
| $(200, 700, 1000)$ | $200 x_k + 700 x_b + 1000 (x_k + x_b) \leq 200 \cdot 3 + 700 \cdot 4 + 1000 \cdot 5$ | $8400$ |
| $(0, 500, 1200)$ | $500 x_b + 1200 (x_k + x_b) \leq 500 \cdot 4 + 1200 \cdot 5$ | $8000$ |

The first bound uses only the seed constraints: it would be reached at the point $(3,4)$, which 
violates the land constraint. The last bound, given by the optimal solution of the dual problem 
$\mathbf{y}^{\ast} = (0, 500, 1200)$, is $8000$ and is reached at the point $(1,4)$, 
so it cannot be improved.

In the $(x_k, x_b)$ plane each summed inequality is a half-plane that contains the whole feasible 
region. The better the dual solution, the closer the boundary of the half-plane is to the region:

![Upper bounds from dual solutions in the cabbage–carrot problem](figs/cabbage-carrots-dual-bounds.png)

*Three feasible points $\mathbf{y}$ of the dual problem and the corresponding lines $1200x_k + 1700x_b = \mathbf{b}^T\mathbf{y}$. In all cases the feasible region lies below the line; the line of the optimal $\mathbf{y}^{\ast}$ touches it at the vertex $(1,4)$.*

In general (*weak duality*, see below): for any feasible $\mathbf{x}$ of the primal problem 
and any feasible $\mathbf{y}$ of the dual problem, $\mathbf{c}^T \mathbf{x} \leq \mathbf{b}^T \mathbf{y}$; 
equality is possible only if both are optimal.

**Shadow prices.** The component $y_i$ of the dual solution shows by how much the optimal 
profit would increase if the right-hand side of the $i$-th constraint were increased by $1$:

* $y_1 = 0$: extra cabbage seeds do not increase the profit -- cabbage already occupies only $1$ ha of the possible $3$.
* $y_2 = 500$: one hectare's worth of extra carrot seeds gives $+500$ euros -- one hectare of cabbage is replaced by carrots ($1700 - 1200 = 500$).
* $y_3 = 1200$: an extra hectare of land gives $+1200$ euros -- the unused cabbage seeds can be sown on it.

The shadow price is the highest price at which it pays to buy an extra unit of the resource; it is not 
the market price of the resource. Shadow prices hold only for small changes, as long as the optimum stays 
at the same vertex with the same active constraints. For example, $y_3 = 1200$ holds 
when the land area is between $4$ and $7$ ha. If there is more than $7$ ha of land, the optimum 
is $(3,4)$, the shadow price of land becomes $0$, and the shadow prices of the seeds become $1200$ and $1700$.

**A physical model.** Imagine that the feasible region is a container in which a small ball rolls, 
and a "gravitational force" $\mathbf{c} = (1200, 1700)$ pulls it in the direction in which the objective function increases. 
The ball stops at the optimal vertex $(1,4)$, resting against both "walls" 
$x_b = 4$ and $x_k + x_b = 5$. The reaction forces of the walls point along their normals 
$(0,1)$ and $(1,1)$, and their magnitudes are exactly the dual variables: 
$y_2 (0,1) + y_3 (1,1) = 500 \cdot (0,1) + 1200 \cdot (1,1) = (1200, 1700) = \mathbf{c}$. 
The wall $x_k = 3$ does not touch the ball, so its reaction is $y_1 = 0$.

**General case:** In the cabbage–carrot problem the objective function is maximized, all constraints 
are $\leq$ and all variables are non-negative. For such a primal problem (P) the dual (D) is:

$$
(P): \textcolor{blue}{\max\left( \mathbf{c}^T \mathbf{x} \right)},\;\;\text{where}\;\;
A \mathbf{x} \leq \mathbf{b},\;\; \mathbf{x} \geq \mathbf{0}.
$$

$$
(D): \textcolor{blue}{\min\left( \mathbf{b}^T \mathbf{y} \right)},\;\;\text{where}\;\;
A^T \mathbf{y} \geq \mathbf{c},\;\; \mathbf{y} \geq \mathbf{0}.
$$

The dual of the dual problem is again the primal problem. So one can equally well start with the 
minimization problem $\min \mathbf{c}^T \mathbf{x}$, where $A\mathbf{x} \geq \mathbf{b}$, $\mathbf{x} \geq \mathbf{0}$; 
its dual is $\max \mathbf{b}^T \mathbf{y}$, where $A^T\mathbf{y} \leq \mathbf{c}$, $\mathbf{y} \geq \mathbf{0}$.




## The Dual of a General LP Problem

Duals are also written for LP problems that are not in standard form. In the primal problem the objective function may have to be minimized or maximized, the constraints may be inequalities in either direction or equalities, and the variables $x_i$ are sometimes non-negative and sometimes unrestricted. All such problems have duals.

**Primal linear program:** Let us define a linear program $(P)$, which we call the *primal LP*:

$$
(P): \textcolor{blue}{\min \left( c_1 x_1 + c_2 x_2 + \ldots + c_n x_n \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
a_{11} x_1 + a_{12} x_2 + \ldots + a_{1n} x_n  \;\;\textcolor{red}{?}\;\; b_1,\\
\ldots\\
a_{k1} x_1 + a_{k2} x_2 + \ldots + a_{kn} x_n \;\;\textcolor{red}{?}\;\; b_k,\\
x_1 \textcolor{red}{?} 0,\; x_2 \textcolor{red}{?} 0,\;\ldots\;  x_n \textcolor{red}{?} 0.\\
\end{array} \right.
$$

Here the LP need not be in standard form:

* In the constraints $a_{i1} x_1 + a_{i2} x_2 + \ldots + a_{in} x_n \;\;\textcolor{red}{?}\;\; b_i$ the question mark may be any relation ($\geq$, $\leq$, $=$).
* The variables $x_i$ may have the condition $x_i \geq 0$, $x_i \leq 0$, or no condition at all.

**Definition:** The *dual program* is the linear program:

$$
(D): \textcolor{blue}{\max \left( b_1 y_1 + b_2 y_2 + \ldots + b_k y_k \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
a_{11} y_1 + a_{21} y_2 + \ldots + a_{k1} y_k  \;\;\textcolor{red}{?}\;\; c_1,\\
a_{12} y_1 + a_{22} y_2 + \ldots + a_{k2} y_k  \;\;\textcolor{red}{?}\;\; c_2,\\
\ldots\\
a_{1n} y_1 + a_{2n} y_2 + \ldots + a_{kn} y_k \;\;\textcolor{red}{?}\;\; c_n,\\
y_1 \textcolor{blue}{?} 0,\; y_2 \textcolor{blue}{?} 0,\;\ldots\; y_k \textcolor{blue}{?} 0 \\
\end{array} \right.
$$

The symbols in place of the blue question marks $\textcolor{blue}{?}$ are determined as follows:

| Primal constraint $i$ | Corresponding dual variable |
| --- | --- |
| ${\displaystyle \sum_{j=1}^n a_{ij}x_j \textcolor{blue}{\geq} b_i}$ |	$y_i \textcolor{blue}{\geq} 0$ |
| ${\displaystyle \sum_{j=1}^n a_{ij}x_j \textcolor{blue}{\leq} b_i}$ |	$y_i \textcolor{blue}{\leq} 0$ |
| ${\displaystyle \sum_{j=1}^n a_{ij}x_j \textcolor{blue}{=} b_i}$ | $y_i\;\;\textcolor{blue}{\text{unrestricted}}$ |

The symbols in place of the red question marks $\textcolor{red}{?}$ are determined as follows:

| Primal variable $x_j$ | Corresponding dual constraint |
| --- | --- |
| $x_j \textcolor{red}{\geq} 0$ | ${\displaystyle \sum_{i=1}^k  a_{ij} y_i \;\;\textcolor{red}{\leq}\;\; c_j}$ |
| $x_j \textcolor{red}{\leq} 0$ | ${\displaystyle \sum_{i=1}^k  a_{ij} y_i \;\;\textcolor{red}{\geq}\;\; c_j}$ |
| $x_j\;\;\textcolor{red}{\text{unrestricted}}$ | ${\displaystyle \sum_{i=1}^k a_{ij} y_i \;\;\textcolor{red}{=}\;\; c_j}$ |




**Example:** Consider a primal LP problem whose constraints contain all kinds of inequalities:

$$
\textcolor{blue}{\max \left( 4x_1 + 2x_2 - x_3 \right)},\;\; \text{where}\;\;
\left\{
\begin{array}{l}
x_1 + x_2 + x_3 = 20\\
2x_1 - x_2 \geq 6\\
3x_1 + 2x_2 + x_3 \leq 40\\
x_1,x_2 \geq 0
\end{array} \right.
$$

The same in matrix notation, where $\mathbf{x}$ is a column vector with 3 coordinates $x_1,x_2,x_3$:

$$
(P): \textcolor{blue}{\max \left( (4, 2, -1) \cdot \mathbf{x} \right)},\;\;\text{where}\;\;
\left(
\begin{array}{ccc}
1 & 1 & 1\\
2 & -1 & 0\\
3 & 2 & 1
\end{array} \right) \left(
\begin{array}{c}
x_1\\
x_2\\
x_3 \end{array} \right)
\begin{array}{c}
=^{\textcolor{blue}{(a)}}\\
\geq^{\textcolor{blue}{(b)}} \\
\leq^{\textcolor{blue}{(c)}}
\end{array}
\left(
\begin{array}{c}
20\\
6 \\
40
\end{array} \right)\;\;\text{and}
$$

$$
x_1 \geq^{\textcolor{blue}{(d)}} 0,\; x_2 \geq^{\textcolor{blue}{(e)}} 0,
x_3\;\text{unrestr.}^{\textcolor{blue}{(f)}}
$$

**The corresponding dual LP problem:** Let $\mathbf{y}$ be a column vector with 3 coordinates: $y_1, y_2, y_3$. Then

$$
(D): \textcolor{blue}{ \min \left(  (20,6,40) \cdot \mathbf{y}  \right) },\;\;\text{where}\;\;
\left(
\begin{array}{ccc}
1 & 2 & 3\\
1 & -1 & 2\\
1 & 0 & 1
\end{array} \right) \left(
\begin{array}{c}
y_1\\
y_2\\
y_3 \end{array} \right)
\begin{array}{c}
\geq^{\textcolor{blue}{(d)}}\\
\geq^{\textcolor{blue}{(e)}} \\
=^{\textcolor{blue}{(f)}}
\end{array}
\left(
\begin{array}{c}
4\\
2 \\
-1
\end{array} \right)\;\;\text{and}
$$

$$
y_1\;\text{unrestr.}^{\textcolor{blue}{(a)}},\;
y_2 \leq^{\textcolor{blue}{(b)}} 0,\;
y_3 \geq^{\textcolor{blue}{(c)}} 0.
$$

The coefficients of the dual problem are obtained by transposing the matrix $A$. The tables above are for a primal problem with $\min$; if the primal problem has $\max$ (as in this example), then all signs in both tables are reversed: a $\leq$ constraint corresponds to $y_i \geq 0$, a $\geq$ constraint corresponds to $y_i \leq 0$, and a variable $x_j \geq 0$ corresponds to a dual constraint with $\geq$. For example, since $x_1 \geq 0$, the dual constraint corresponding to the variable $x_1$ is $y_1 + 2y_2 + 3y_3 \geq 4$. The optimal value of both problems is $33.5$: for the primal at $\mathbf{x}^{\ast} = (6.5;\ 7;\ 6.5)$, for the dual at $\mathbf{y}^{\ast} = (-3.75;\ -0.25;\ 2.75)$.



## Duality Theorems: A Summary for Algorithms

The LP algorithms discussed in the next lecture -- the ellipsoid algorithm, the affine scaling method and especially the primal-dual path-following method -- use several facts from duality theory. Here they are collected in a unified notation, without proofs (except the simplest ones).

### The Primal and Dual Problems in Standard Form

Interior point methods formulate LP in *standard form*: all constraints are equalities and all variables are non-negative. Inequalities are turned into equalities with slack variables: $\mathbf{a}_i^T\mathbf{x} \leq b_i$ is replaced by $\mathbf{a}_i^T\mathbf{x} + x'_i = b_i$, $x'_i \geq 0$. If $A$ is an $m \times n$ matrix, then

$$
(P): \textcolor{blue}{\min \left( \mathbf{c}^T \mathbf{x} \right)},\;\;\text{where}\;\;
A\mathbf{x} = \mathbf{b},\;\; \mathbf{x} \geq \mathbf{0};
$$

$$
(D): \textcolor{blue}{\max \left( \mathbf{b}^T \mathbf{y} \right)},\;\;\text{where}\;\;
A^T\mathbf{y} + \mathbf{s} = \mathbf{c},\;\; \mathbf{s} \geq \mathbf{0}.
$$

Here $\mathbf{x}, \mathbf{s} \in \mathbb{R}^n$ and $\mathbf{y} \in \mathbb{R}^m$. According to the table in the previous section, the equalities $A\mathbf{x} = \mathbf{b}$ correspond to unrestricted dual variables $y_i$, and the variables $x_j \geq 0$ correspond to the dual inequalities $(A^T\mathbf{y})_j \leq c_j$. The differences $\mathbf{s} = \mathbf{c} - A^T\mathbf{y} \geq \mathbf{0}$ are called *dual slacks* (in the simplex algorithm they are the *reduced costs*). So each primal variable $x_j$ corresponds to one dual slack $s_j$.

### Weak Duality and the Duality Gap

If $\mathbf{x}$ is feasible for (P) and $(\mathbf{y}, \mathbf{s})$ is feasible for (D), then

$$
\mathbf{c}^T\mathbf{x} - \mathbf{b}^T\mathbf{y}
= (A^T\mathbf{y} + \mathbf{s})^T\mathbf{x} - (A\mathbf{x})^T\mathbf{y}
= \mathbf{s}^T\mathbf{x} = \sum_{j=1}^n x_j s_j \geq 0.
$$

The difference $\mathbf{c}^T\mathbf{x} - \mathbf{b}^T\mathbf{y} = \mathbf{x}^T\mathbf{s}$ is called the *duality gap*. This equality implies:

* Every dual feasible $\mathbf{y}$ gives a lower bound $\mathbf{b}^T\mathbf{y} \leq \mathbf{c}^T\mathbf{x}$ for all primal feasible $\mathbf{x}$ (*weak duality*).
* If $\mathbf{x}^T\mathbf{s} = 0$, then $\mathbf{x}$ and $(\mathbf{y}, \mathbf{s})$ are both optimal -- this is a *certificate of optimality*.
* If $\mathbf{x}^T\mathbf{s} \leq \varepsilon$, then $\mathbf{c}^T\mathbf{x}$ differs from the optimum by at most $\varepsilon$, even if the optimum is not known. Interior point methods use this as a stopping criterion.
* If (P) is unbounded (the objective function can be arbitrarily small), then (D) has no feasible points, and vice versa.

### Strong Duality

**Theorem (strong duality):** If (P) has an optimal solution $\mathbf{x}^{\ast}$, then (D) also has an optimal solution $(\mathbf{y}^{\ast}, \mathbf{s}^{\ast})$, and $\mathbf{c}^T\mathbf{x}^{\ast} = \mathbf{b}^T\mathbf{y}^{\ast}$.

(The proof is usually derived from Farkas' lemma or from the simplex algorithm: when it stops, the reduced costs give a dual solution.) Together with weak duality this means that only the following combinations are possible for the primal and dual problems:

| | (D) has an optimum | (D) unbounded | (D) infeasible |
| --- | --- | --- | --- |
| (P) has an optimum | possible, $\mathbf{c}^T\mathbf{x}^{\ast} = \mathbf{b}^T\mathbf{y}^{\ast}$ | impossible | impossible |
| (P) unbounded | impossible | impossible | possible |
| (P) infeasible | impossible | possible | possible |

**Corollary (optimization $\to$ feasibility):** $\mathbf{x}$ and $(\mathbf{y}, \mathbf{s})$ are optimal if and only if they satisfy the following system of linear equalities and inequalities:

$$
A\mathbf{x} = \mathbf{b},\;\; \mathbf{x} \geq \mathbf{0},\;\;
A^T\mathbf{y} + \mathbf{s} = \mathbf{c},\;\; \mathbf{s} \geq \mathbf{0},\;\;
\mathbf{c}^T\mathbf{x} \leq \mathbf{b}^T\mathbf{y}.
$$

So an algorithm that finds *at least one* point satisfying a system of linear inequalities is enough. The ellipsoid algorithm uses this.

### Complementary Slackness

The duality gap $\sum_j x_j s_j$ is a sum of non-negative terms. It is $0$ only if every term is $0$:

**Theorem (complementary slackness):** Feasible $\mathbf{x}$ and $(\mathbf{y}, \mathbf{s})$ are optimal if and only if

$$
x_j s_j = 0\;\;\text{for all}\;\; j = 1, \ldots, n,
$$

i.e., for each $j$ either $x_j = 0$ or the $j$-th dual inequality holds with equality ($s_j = 0$).

**Example:** In the cabbage–carrot problem (see above; it is a maximization problem with $\leq$ inequalities) the complementary slackness conditions are of two kinds: $y_i = 0$ if the $i$-th primal constraint is not active, and the $j$-th dual inequality is an equality if $x_j > 0$. At the optimal point $(x_k, x_b) = (1, 4)$:

* $x_k = 1 < 3$, so the first constraint is not active, and $y_1 = 0$;
* $x_k > 0$ and $x_b > 0$, so $y_1 + y_3 = 1200$ and $y_2 + y_3 = 1700$.

Hence $y_3 = 1200$ and $y_2 = 500$ -- exactly the dual optimum $(0, 500, 1200)$. Knowing the primal optimum, the dual one can be found by solving a system of linear equations.

### Optimality Conditions and the Central Path

Combining feasibility and complementary slackness, $\mathbf{x}$ is optimal for (P) and $(\mathbf{y}, \mathbf{s})$ is optimal for (D) if and only if

$$
\left\{ \begin{array}{ll}
A\mathbf{x} = \mathbf{b} & (\text{primal feasibility}),\\
A^T\mathbf{y} + \mathbf{s} = \mathbf{c} & (\text{dual feasibility}),\\
X S \mathbf{e} = \mathbf{0} & (\text{complementary slackness}),\\
\mathbf{x} \geq \mathbf{0},\;\; \mathbf{s} \geq \mathbf{0}. &
\end{array} \right.
$$

Here $X = \operatorname{diag}(x_1, \ldots, x_n)$ and $S = \operatorname{diag}(s_1, \ldots, s_n)$ are diagonal matrices, and $\mathbf{e} = (1, \ldots, 1)^T$; so $X S \mathbf{e} = (x_1 s_1, \ldots, x_n s_n)^T$. These conditions are also called the *KKT conditions* (Karush–Kuhn–Tucker). The first two blocks are linear, but complementary slackness is not (it contains the products $x_j s_j$). Different algorithms handle these conditions differently:

* The *simplex algorithm* always maintains $A\mathbf{x} = \mathbf{b}$, $\mathbf{x} \geq \mathbf{0}$ and complementary slackness (non-basic variables $x_j = 0$, basic variables have $s_j = 0$) and moves along vertices until also $\mathbf{s} \geq \mathbf{0}$.
* *Interior point methods* maintain $\mathbf{x} > \mathbf{0}$ and $\mathbf{s} > \mathbf{0}$ (strictly positive) and gradually drive the products $x_j s_j$ to zero.

**The central path:** The complementary slackness condition $x_j s_j = 0$ is replaced by $x_j s_j = \mu$ for all $j$, where $\mu > 0$ is a parameter:

$$
A\mathbf{x} = \mathbf{b},\;\;
A^T\mathbf{y} + \mathbf{s} = \mathbf{c},\;\;
X S \mathbf{e} = \mu \mathbf{e},\;\;
\mathbf{x} > \mathbf{0},\;\; \mathbf{s} > \mathbf{0}.
$$

If both problems have strictly feasible points ($\mathbf{x} > \mathbf{0}$, $\mathbf{s} > \mathbf{0}$) and the rows of the matrix $A$ are linearly independent, then for each $\mu > 0$ this system has exactly one solution $(\mathbf{x}(\mu), \mathbf{y}(\mu), \mathbf{s}(\mu))$. This curve of points is called the *central path*. Its properties:

* On the central path the duality gap is $\mathbf{x}(\mu)^T\mathbf{s}(\mu) = n\mu$; so $\mu$ directly determines how far we are from the optimum.
* As $\mu \to 0$, the central path tends to the optimal solutions of (P) and (D).
* As $\mu \to \infty$ (and the feasible region is bounded), $\mathbf{x}(\mu)$ tends to the *analytic center* of the feasible region -- the point where $\sum_j \ln x_j$ is maximal.
* $\mathbf{x}(\mu)$ is the solution of the *barrier problem* $\min \left( \mathbf{c}^T\mathbf{x} - \mu \sum_j \ln x_j \right)$, where $A\mathbf{x} = \mathbf{b}$: its optimality condition is $\mathbf{c} - \mu X^{-1}\mathbf{e} = A^T\mathbf{y}$, and writing $s_j = \mu / x_j$ gives exactly $x_j s_j = \mu$. So the central path connects the idea of a barrier function with duality.

**Example:** $\min x_1$, where $x_1 + x_2 = 1$, $x_1, x_2 \geq 0$ (optimum $\mathbf{x}^{\ast} = (0, 1)$). The dual problem: $\max y$, where $y + s_1 = 1$, $y + s_2 = 0$, $s_1, s_2 \geq 0$ (optimum $y^{\ast} = 0$). The central path equations $x_1(1 - y) = \mu$, $x_2 \cdot (-y) = \mu$, $x_1 + x_2 = 1$ give:

| $\mu$ | $x_1(\mu)$ | $x_2(\mu)$ | $y(\mu)$ | Gap $x_1 s_1 + x_2 s_2 = 2\mu$ |
| --- | --- | --- | --- | --- |
| $10$ | $0.4875$ | $0.5125$ | $-19.5125$ | $20$ |
| $1$ | $0.3820$ | $0.6180$ | $-1.6180$ | $2$ |
| $0.1$ | $0.0901$ | $0.9099$ | $-0.1099$ | $0.2$ |
| $0.01$ | $0.0099$ | $0.9901$ | $-0.0101$ | $0.02$ |

For large $\mu$ the point is close to the analytic center $(1/2, 1/2)$, and as $\mu$ decreases it approaches the optimum $(0, 1)$ from the interior of the feasible region.

**What each algorithm uses:**

| Algorithm | Duality result used |
| --- | --- |
| Ellipsoid algorithm | Strong duality: optimization reduces to finding a feasible point |
| Affine scaling method | Dual estimate $\mathbf{y}$ and the duality gap for the stopping criterion |
| Primal-dual path-following method | Optimality conditions, central path, gap $\mathbf{x}^T\mathbf{s} = n\mu$ |




## Problems

**Problem 9.1:** We are given a directed graph with source $s$, sink $t$ and edge capacities:

![Directed graph with edge capacities](figs/edmonds-karp-graph.png)

Write a linear program whose solution is the maximum flow from $s$ to $t$: state the variables, the objective function and all constraints. (The linear program need not be solved.)

**Answer:** For each edge $(u,v)$ we introduce a variable $f_{uv}$, the flow along this edge (in the subscripts the vertices $v_i$ are denoted by $i$). The graph has $12$ edges, so there are $12$ variables.

*Objective function:* maximize the flow leaving the source (no edge enters the source):

$$
\textcolor{blue}{\max \left( f_{s1} + f_{s3} + f_{s5} \right)}.
$$

*Flow conservation* at each intermediate vertex $v_1, \ldots, v_6$ (incoming flow = outgoing flow):

$$
\left\{ \begin{array}{ll}
f_{s1} + f_{31} = f_{12} & (v_1),\\
f_{12} + f_{42} = f_{2t} & (v_2),\\
f_{s3} = f_{31} + f_{36} & (v_3),\\
f_{54} = f_{42} + f_{4t} & (v_4),\\
f_{s5} = f_{54} + f_{56} & (v_5),\\
f_{36} + f_{56} = f_{6t} & (v_6).
\end{array} \right.
$$

*Capacity constraints* (the flow is non-negative and does not exceed the capacity):

$$
\begin{array}{llll}
0 \leq f_{s1} \leq 3, & 0 \leq f_{s3} \leq 1, & 0 \leq f_{s5} \leq 3, & 0 \leq f_{31} \leq 5,\\
0 \leq f_{12} \leq 4, & 0 \leq f_{42} \leq 2, & 0 \leq f_{2t} \leq 2, & 0 \leq f_{4t} \leq 3,\\
0 \leq f_{36} \leq 2, & 0 \leq f_{54} \leq 2, & 0 \leq f_{56} \leq 5, & 0 \leq f_{6t} \leq 1.
\end{array}
$$

In total there are $12$ variables, $6$ equalities and $24$ simple inequalities (lower and upper bounds). Instead of this objective function one can also maximize the flow entering the sink, $f_{2t} + f_{4t} + f_{6t}$ -- by flow conservation both expressions are equal.

*Note:* Solving this linear program (for example, with `pulp`) gives the maximum flow $5$. It cannot be larger, because the edges $v_2 \to t$, $v_5 \to v_4$ and $v_6 \to t$ separate $\lbrace s, v_1, v_2, v_3, v_5, v_6 \rbrace$ from $\lbrace v_4, t \rbrace$, and their total capacity is $2 + 2 + 1 = 5$. $\square$

**Problem 9.2 (information asymmetry):** A software company sells annual licenses. There are two types of customers: *small* companies value a license at $4$ thousand EUR, *large* ones at $10$ thousand EUR. Large companies make up $50\%$ of all customers, but the seller does not know the type of a particular customer (the customer knows it; this is *information asymmetry*). The cost of distributing a license can be ignored.

The seller offers a *menu of contracts* -- two versions of the license $(q_M, t_M)$ and $(q_L, t_L)$, where $q \in [0;1]$ is the share of functionality (the full version has $q = 1$, while $q = 0$ means not buying a license), and $t$ is the price. A customer with valuation $v$ who chooses version $(q, t)$ gets the benefit $v q - t$, and every customer chooses the version that is best for them or buys nothing.

1. What revenue per customer would the seller get if they *knew* the type of each customer?
2. Write a linear program that maximizes the seller's expected revenue per customer when the customer type is unknown. Explain why the constraints are linear.
3. Solve this linear program. Which group of customers gets an *information rent* (a benefit greater than $0$), and why?
4. How does the answer change if the share of large companies is only $30\%$?

**Answer:**

1. Knowing the customer type, the seller sells each customer the full version at their valuation: small ones for $4$, large ones for $10$. Expected revenue: $0.5 \cdot 4 + 0.5 \cdot 10 = 7$ thousand EUR.
2. Variables: $q_M, q_L \in [0;1]$, $t_M, t_L$. The linear program:

   $$
   \textcolor{blue}{\max \left( 0.5\, t_M + 0.5\, t_L \right)},\;\;\text{where}\;\;
   \left\{ \begin{array}{ll}
   4 q_M - t_M \geq 0 & (\text{IR}_M),\\
   10 q_L - t_L \geq 0 & (\text{IR}_L),\\
   10 q_L - t_L \geq 10 q_M - t_M & (\text{IC}_L),\\
   4 q_M - t_M \geq 4 q_L - t_L & (\text{IC}_M),\\
   0 \leq q_M \leq 1,\;\; 0 \leq q_L \leq 1. &
   \end{array} \right.
   $$

   *Participation constraints* (IR, *individual rationality*): for every customer, buying their version is not worse than buying nothing. *Incentive compatibility constraints* (IC): for every customer, their own version is not worse than the one intended for the other type -- otherwise a large company would pretend to be a small one. All constraints are linear, because the valuations $4$ and $10$ are constants and the benefit $v q - t$ is linear in $q$ and $t$.
3. At the optimum the active constraints are $\text{IR}_M$ and $\text{IC}_L$, and $q_L = 1$. Then $t_M = 4 q_M$ and $t_L = 10 - 6 q_M$, so the revenue is

   $$
   0.5 \cdot 4 q_M + 0.5 \cdot (10 - 6 q_M) = 5 - q_M.
   $$

   It is maximal at $q_M = 0$: the optimal menu is $(q_M, t_M) = (0, 0)$ and $(q_L, t_L) = (1, 10)$, with revenue $5$ thousand EUR (solving the LP on a computer gives the same). The seller sells nothing to small companies, although they value the license positively -- this is an efficiency loss caused by information asymmetry. If small companies were sold a part of the functionality $q_M > 0$, large companies could buy this cheaper version and get the benefit $10 q_M - 4 q_M = 6 q_M$. So their price for the full version would have to be reduced by $6 q_M$ -- this discount is the large companies' *information rent*. At $q_M = 0$ the rent is $0$; if both were sold the full version at price $4$, the large companies' rent would be $6$.
4. If $30\%$ of the companies are large, the revenue is $0.7 \cdot 4 q_M + 0.3 \cdot (10 - 6 q_M) = 3 + q_M$, and the optimum is $q_M = 1$: both customer types are sold the full version at price $4$, the revenue is $4$ thousand EUR, and the large companies get an information rent of $6$. The seller always has to choose between efficiency (serving everyone) and limiting the rent (not selling to small companies).

*Note:* Problems in which a contracting party does not know the other party's *hidden information* are called *adverse selection* or *screening* problems in microeconomics. A classic example is Akerlof's "market for lemons" (1970): buyers of used cars do not know the quality of a car, so they are willing to pay only the average price, and owners of good cars leave the market. $\square$

**Problem 9.3:** Two players play a matrix game with the payoff matrix

$$
A = \left( \begin{array}{rrr}
3 & -1 & 2 \\
-2 & 4 & 1 \\
4 & 0 & 3 \\
\end{array} \right).
$$

As in this lecture, player $X$ chooses a row, player $Y$ chooses a column, and $X$ pays player $Y$ the amount $a_{ij}$ ($X$ minimizes it, $Y$ maximizes it).

1. Does the game have a saddle point?
2. Can any row or column be eliminated because it is worse than another one (*dominated*)?
3. Find the optimal mixed strategies of both players and the value of the game.
4. Write a linear program whose solution is player $X$'s optimal strategy.

**Answer:**

1. In each row $X$ must reckon with the worst case -- the largest element: $3$, $4$, $4$; the best is $\min = 3$ (row 1). In each column $Y$ is guaranteed the smallest element: $-2$, $-1$, $1$; the best is $\max = 1$ (column 3). Since $1 < 3$, there is no saddle point, and the optimal strategies are mixed.
2. Row 3 $(4, 0, 3)$ is larger than row 1 $(3, -1, 2)$ in every column, so the minimizing player $X$ never chooses row 3. In the remaining $2 \times 3$ matrix no column is dominated.
3. Let $X$ choose row 1 with probability $p$ and row 2 with probability $1 - p$. Player $Y$'s average gain for each column:

   $$
   \text{column 1: } 3p - 2(1-p) = 5p - 2,\quad
   \text{column 2: } -p + 4(1-p) = 4 - 5p,\quad
   \text{column 3: } 2p + (1-p) = 1 + p.
   $$

   Player $X$ minimizes the maximum of these three lines (the upper envelope). It is $4 - 5p$ if $p \leq 1/2$; $1 + p$ if $1/2 \leq p \leq 3/4$; $5p - 2$ if $p \geq 3/4$. The smallest value is at $p = 1/2$, where the lines of columns 2 and 3 intersect: $v = 3/2$. So $\mathbf{x}^{\ast} = (1/2, 1/2, 0)$.

   Player $Y$ uses only columns 2 and 3 (at $p = 1/2$ column 1 gives only $1/2 < 3/2$). If column 2 is chosen with probability $q$, then by the indifference principle rows 1 and 2 must give the same result: $-q + 2(1-q) = 4q + (1-q)$, hence $q = 1/6$. So $\mathbf{y}^{\ast} = (0, 1/6, 5/6)$.

   Check (see the corollary of the minimax theorem):

   $$
   (\mathbf{x}^{\ast})^T A = \left( \tfrac{1}{2}, \tfrac{3}{2}, \tfrac{3}{2} \right),\;\;
   \max = \tfrac{3}{2};\qquad
   A\mathbf{y}^{\ast} = \left( \tfrac{3}{2}, \tfrac{3}{2}, \tfrac{5}{2} \right)^T,\;\;
   \min = \tfrac{3}{2}.
   $$

   Both values coincide, so both strategies are optimal, and the value of the game is $v(A) = 3/2$ (on average $X$ pays player $Y$ $1.5$ units).
4. Player $X$'s linear program (variables $x_1, x_2, x_3, z$):

   $$
   \textcolor{blue}{\min(z)},\;\;\text{where}\;\;
   \left\{ \begin{array}{l}
   3x_1 - 2x_2 + 4x_3 \leq z,\\
   -x_1 + 4x_2 \leq z,\\
   2x_1 + x_2 + 3x_3 \leq z,\\
   x_1 + x_2 + x_3 = 1,\\
   x_1, x_2, x_3 \geq 0.
   \end{array} \right.
   $$

   Its solution is $\mathbf{x}^{\ast} = (1/2, 1/2, 0)$, $z = 3/2$. $\square$

**Problem 9.4:** We are given the linear program

$$
\textcolor{blue}{\max \left( 3x_1 + 2x_2 \right)},\;\;\text{where}\;\;
\left\{ \begin{array}{l}
x_1 + x_2 \leq 5,\\
x_1 + 3x_2 \leq 12,\\
2x_1 + x_2 \leq 8,\\
x_1, x_2 \geq 0.
\end{array} \right.
$$

1. Write the dual linear program.
2. Using only weak duality, show that the value of the objective function cannot exceed $15$.
3. It is claimed that $\mathbf{x}^{\ast} = (3, 2)$ is an optimal solution. Use the complementary slackness conditions to find the dual solution $\mathbf{y}^{\ast}$ and check that $\mathbf{x}^{\ast}$ is indeed optimal.
4. Approximately how much will the optimal value change if the right-hand side of the first constraint is increased from $5$ to $5.1$? And if the right-hand side of the second constraint is decreased from $12$ to $11$?
5. Can the dual program be unbounded (i.e., can its objective function be arbitrarily small)?

**Answer:**

1. Each constraint corresponds to a dual variable $y_1, y_2, y_3 \geq 0$, and each variable $x_j \geq 0$ corresponds to a dual inequality:

   $$
   \textcolor{blue}{\min \left( 5y_1 + 12y_2 + 8y_3 \right)},\;\;\text{where}\;\;
   \left\{ \begin{array}{l}
   y_1 + y_2 + 2y_3 \geq 3,\\
   y_1 + 3y_2 + y_3 \geq 2,\\
   y_1, y_2, y_3 \geq 0.
   \end{array} \right.
   $$

2. The point $\mathbf{y} = (3, 0, 0)$ is dual feasible: $3 \geq 3$ and $3 \geq 2$. Its value is $5 \cdot 3 = 15$, so by weak duality $3x_1 + 2x_2 \leq 15$ for every feasible $\mathbf{x}$. (Directly: $3x_1 + 2x_2 \leq 3x_1 + 3x_2 = 3(x_1 + x_2) \leq 15$.)
3. $\mathbf{x}^{\ast} = (3, 2)$ is feasible: $3 + 2 = 5 \leq 5$, $3 + 6 = 9 \leq 12$, $6 + 2 = 8 \leq 8$. The second constraint is not active ($9 < 12$), so $y_2 = 0$. Since $x_1 > 0$ and $x_2 > 0$, both dual inequalities are equalities: $y_1 + 2y_3 = 3$ and $y_1 + y_3 = 2$. Hence $y_3 = 1$, $y_1 = 1$, so $\mathbf{y}^{\ast} = (1, 0, 1) \geq \mathbf{0}$ -- dual feasible. The values of the objective functions: $3 \cdot 3 + 2 \cdot 2 = 13$ and $5 \cdot 1 + 12 \cdot 0 + 8 \cdot 1 = 13$. They coincide, so both solutions are optimal.
4. The shadow price is $y_1^{\ast} = 1$, so the optimal value increases by approximately $1 \cdot 0.1 = 0.1$, to $13.1$. (Check: the new optimum is $(2.9;\ 2.2)$ with value $8.7 + 4.4 = 13.1$.) The shadow price of the second constraint is $y_2^{\ast} = 0$: decreasing the right-hand side to $11$ does not change the optimum, because $\mathbf{x}^{\ast}$ still satisfies this constraint ($9 \leq 11$).
5. No. The primal program has a feasible point (for example, $\mathbf{x} = (0, 0)$ or $\mathbf{x}^{\ast}$), and by weak duality every dual value is at least $3x_1 + 2x_2$ at this point. So the values of the dual objective function are bounded from below. $\square$
