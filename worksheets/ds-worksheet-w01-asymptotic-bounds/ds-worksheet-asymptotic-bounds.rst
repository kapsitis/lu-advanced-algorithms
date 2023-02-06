Worksheet Week 01: Asymptotic Bounds
======================================

Introduction
--------------

**Goal:**  
  The focus of this course is efficiency -- creating algorithms that can work on
  large input data and handle complex structures sufficiently fast.


**Why use Big-O Notation?** 
  It is convenient to measure speed of algorithms -- for example, to find the best algorithms for 
  a given problem. Or to find out which problems are easy (have fast algorithms) and which ones are hard 
  (have only slow or unfeasible algorithms). 
  
  * Measuring the speed should not depend on the speed of the computing hardware -- do not care about constant factors. 
  * Measuring the speed should not depend on how fast it works on very short inputs. (One can "cheat" for short inputs -- 
    just remember a large lookup table containing values for inputs of length :math:`n < n_0` with precomputed correct answers.
    Clearly, this does not tell us anything about the performance of this algorithm for arbitrary inputs.)
  * Measuring the speed should be conceptually easy, it should not take into account insignificant optimizations or count too many extra factors. 
    
**Example:** 
  Energy needed to lift a stone of mass :math:`m` to the height :math:`h` is :math:`mgh`. (Is this 
  the best-case estimate? The worst-case estimate? The exact value?)


Running Time as a Complexity Measure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**The Worst Running Time function:** 
  Given an algorithm, denote by :math:`T(n)` 
  the number of elementary steps that are needed to complete the algorithm for any input of length :math:`n`.
  (It can be called the *upper bound* of the running time.)
  
**Discussions on the Worst-Case Running Time:**

  * Is :math:`T(n)` the upper bound also for inputs shorter than :math:`n`?
  * Is :math:`T(n)` a non-decreasing function (i.e. do longer inputs always imply a longer running time)?
  * What counts as an elementary step? (Any CPU instruction? One line in a pseudocode? One comparison in a sorting algorithm?)
  * Let :math:`T(n)` be a numeric algorithm receiving single natural numbers as input. 
    Does the worst running time function change, if the input numbers are provided in binary (instead of decimal) notation? 
  * What is the worst running time to multiply two square matrices of size :math:`n \times n`? 
    What is the size of input in this case?

Sometimes it is common to have :math:`n` as some important parameter of the input data (not necessarily the exact size of its encoding). 
For matrix tasks -- the size of the matrices :math:`n`. For graph problems -- the number of vertices :math:`n` and the number of edges :math:`m`. 



Definitions
^^^^^^^^^^^^^

**Definition of Big-O:** 
  Let :math:`g \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` be a function from natural numbers (non-negative integers)
  to non-negative real numbers.
  Then :math:`O(g)` is the set of all functions :math:`f \colon \mathbb{N} \rightarrow \mathbb{R}^{0+}`
  such that there exist real constants :math:`c>0` and :math:`n_0 \in \mathbb{N}` satisfying
  
  .. math:: 
  
    0 \leq f(n) \leq c \cdot g(n)\;\; \mbox{for all}\;\; n \geq n_0.


**Definition of Big-Omega:**
  Let :math:`g \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` be a function from natural numbers to non-negative real numbers. 
  Then :math:`\Omega(g(n))` is the set of all functions :math:`f \colon \mathbb{N} \rightarrow \mathbb{R}`
  such that there exist real constants :math:`c>0` and :math:`n_0 \in \mathbb{N}` satisfying
  :math:`{\displaystyle  \forall n \in \mathbb{N}\ \big( n \geq n_0 \rightarrow f(n) \geq c \cdot g(n) \big).}`

**Definition of Big Theta:**
  Let :math:`g \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` be a function from natural numbers to non-negative real numbers. 
  Then :math:`\Theta(g)` is the set of all functions :math:`f: \mathbb{N} \to \mathbb{R}`
  such that there exist positive constants :math:`c_1, c_2 > 0` and :math:`n_0 \in \mathbb{N}` satisfying

  .. math::

    \forall n \in \mathbb{N}\ \big( n \geq n_0 \rightarrow  0 \leq   c_1 \cdot g(n) \leq  f(n) \leq c_2 \cdot g(n) \big).


Informally, the following terms are also usable:

* If :math:`f(n) \in O(g(n))`, then :math:`g(n)` is called *asymptotic upper bound* of :math:`f(n)`.
* If :math:`f(n) \in \Omega(g(n))`, then :math:`g(n)` is called *asymptotic lower bound* of :math:`f(n)`.
* If :math:`f(n) \in \Theta(g(n))`, then :math:`g(n)` is called *asymptotic growth order* of :math:`f(n)`.


All these concepts (Big-O, Big-Omega, Big-Theta) are related to calculus (real analysis); it is functional behavior as :math:`n \rightarrow \infty`.
Predicting the speed of an algorithm for short input lengths :math:`n`, the dependence on :math:`n` is typically
quite complex (and we cannot ignore "lower order"  terms). As :math:`n` becomes very large,
only the "dominant parts" in the expression :math:`f(n)` matter.


Properties of Big-O, Big-Omega, Big-Theta
--------------------------------------------

**Big-O and Limit of the Ratio:**
  If the following limit exists and is finite:

  .. math::

    \lim\limits_{n \rightarrow \infty} \frac{f(n)}{g(n)} = C < + \infty,

  then :math:`f(n)` is in :math:`O(g(n))`.


**Big-O is transitive:**
  If :math:`f(n) \in O(g(n))` and :math:`g(n) \in O(h(n))`, then :math:`f(n) \in O(h(n))`.

**Sum of two functions:**
  If :math:`f(n) \in O(h(n))` and :math:`g(n) \in O(h(n))`, then :math:`f(n) + g(n) = O(h(n))`.

**All polynomials:**
  Any :math:`k`-th degree polynomial :math:`P(n) = a_k n^k + a_{k-1} n^{k-1} + \ldots + a_1 n + a_0` is in :math:`O(n^k)`.

**Logarithms of any base:**
  If :math:`a,b > 1` are any real numbers, then :math:`\log_a n = O(log_b n)`. Typically use just one base (usually, it is base :math:`2` or
  base :math:`e` of the natural logarithm, if you prefer that), and write just :math:`O(\log n)` without specifying base at all.

The last result directly follows from the formula to change the base of a logarithm: :math:`{\displaystyle \forall a,b,m > 1 \left( \log_a b = \frac{ \log_m b }{ \log_m a } \right)}`.





Problems
------------

**Problem 1:**
  Show using the above definition of :math:`O(g)` the following facts:

  **(A)**
    :math:`f(n) = 13n + 7` is in :math:`O(n)`. (Formally, :math:`f \in O(g)`, where :math:`g(n) = n`.)

  **(B)**
    :math:`f(n) = 3n^2 - 100n + 6` is in :math:`O(n^2)`.

  **(C)**
    :math:`f(n) = 3n^2 - 100n + 6` is in :math:`O(n^3)`.

  **(D)**
    :math:`f(n) = 3n^2 - 100n + 6` is **not** in :math:`O(n)`.


**Problem 2:**
  Let us have a zero-based dictionary :math:`D` with :math:`n` items
  from :math:`D[0]` to :math:`D[n-1]`.

  | :math:`\text{\sc LinearSearch}(D,w)`
  | 1. :math:`\;\;\;\;\;` **for** :math:`i` **in** :math:`\text{\sc range}(0,n)`:
  | 2. :math:`\;\;\;\;\;\;\;\;\;\;` **if** :math:`w` ``==`` :math:`D[i]`:
  | 3. :math:`\;\;\;\;\;\;\;\;\;\;\;\;\;\;\;` **return** :math:`\text{\sc found}` :math:`w` at location :math:`i`
  | 4. :math:`\;\;\;\;\;` **return** :math:`\text{\sc not found}`



**Problem 3:**
  What is the worst running time to find, if the given input :math:`m` is a prime number? 
  (Primality testing is done by dividing the input with all 
  numbers :math:`2,3,\ldots,\lfloor \sqrt{m} \rfloor` until :math:`m` is found to be divisible by some number.)
  

**Problem 4:** 
  Answer the following Yes/No questions: 

  **(A)**
    For any :math:`g(n)`, is the set of functions :math:`\Theta(g(n))` the intersection of :math:`O(g(n))` and :math:`\Omega(g(n))`? 
	
  **(B)**
    Does every function :math:`f(n)` belong to the set :math:`Omega(1)`?
	
  **(C)** 
    Let :math:`f(n), g(n)` be two functions from natural numbers to non-negative real numbers. 
    Is it true that we have either :math:`f(n)` in :math:`O(g(n))` or :math:`g(n)` in :math:`f(n)` (or both)? 

  **(D)**
    Does the definition of :math:`f(n)` in :math:`O(g(n))` make sense, if :math:`f(n)` and :math:`g(n)` can take negative values? 
	
  **(E)** 
    Let :math:`f(n)` be a function from natural numbers to non-negative real numbers. 
	Do we always have that :math:`f(n)` is in :math:`O(f(n))`, and :math:`f(n)` is in :math:`\Omega(f(n))` and :math:`f(n)` is in :math:`\Theta(f(n))`? 
	(In other words, is being in Big-O, in Big-Omega and in Big-Theta a reflexive relation?)
	
  **(F)** 
    Let :math:`f(n),g(n),h(n)` be functions from natural numbers to non-negative real numbers. 
	It is known that :math:`f(n)` is in :math:`O(g(n))` and also :math:`g(n)` is in :math:`h(n)`. 
	Can we always imply that :math:`f(n)` is in :math:`O(h(n))`. 
	(In other words, is being in Big-O, in Big-Omega and in Big-Theta a transitive relation?)
	
  **(H)** 
    Let :math:`f(n),g(n)` be functions from natural numbers to non-negative real numbers. 
	It is known that :math:`f(n)` is in :math:`\Theta(g(n))`. 
	Can we always imply that :math:`g(n)` is in :math:`\Theta(f(n))`? 
	(In other words, is being in Big-Theta an equivalence relation?)
	
  **(I)**
    A function :math:`f(n)` is defined for natural arguments and takes natural values. 
	It is known that :math:`f(n)` is in :math:`O(1)`. Is it true that :math:`f(n)` is a constant function: :math:`f(n) = C` for all :math:`n \in \mathbf{N}`.





**Problem 5:** 
  Given a sequence :math:`a_i` (:math:`i = 0,\ldots,n-1`) we call its element :math:`a_i` a *peak*
  iff it is a local maximum (at least as big as any of its neighbors):

  .. math::

    a_i \geq a_{i-1}\;\;\text{\bf and}\;\; a_i \geq a_{i+1}

  (In case if :math:`i=0` or :math:`i = n-1`, one of these neighbors does not exist; and in such cases we
  only compare :math:`a_i` with neighbors that do exist.)
  
  **(A)**
    Suggest an algorithm to find some peak in the given array :math:`A[0],\ldots,A[n-1]` and find its worst-case running time. 
  
  **(B)**
    Suggest an algorithm that is faster than linear time to find peaks in an array. Namely, its worst-case running time should satisfy the limit: 
	
	.. math::
	
	  \lim_{n \rightarrow \infty} \frac{T(n)}{n} = 0. 
	  



**Problem 6:**
  Order these functions in increasing order regarding Big-O complexity
  (:math:`f_i` is considered "not larger" than :math:`f_j` iff :math:`f_i \in O(f_j)`.

  * :math:`f_1(n) = n^{0.9999} \log_2 n`
  * :math:`f_2(n) = 10000n`
  * :math:`f_3(n) = 1.0001^n`
  * :math:`f_4(n) = n^2`


**Problem 7:**
  Order these functions in increasing order regarding Big-O complexity:

  * :math:`f_1(n) = 2^{2^{10000}}`
  * :math:`f_2(n) = 2^{10000n}`
  * :math:`f_3(n) = \binom{n}{2} = C_n^2`
  * :math:`f_4(n) = \binom{n}{\lfloor n/2 \rfloor}`
  * :math:`f_5(n) = \binom{n}{n-2}`
  * :math:`f_6(n) = n!`
  * :math:`f_7(n) = n\sqrt{n}`

**Problem 8:**
  Order these functions in increasing order regarding Big-O complexity:

  * :math:`f_1(n) = n^{\sqrt{n}}`
  * :math:`f_2(n) = 2^n`
  * :math:`f_3(n) = n^{10} \cdot 2^{n/2}`
  * :math:`{\displaystyle \sum\limits_{i = 1}^{n} (i + 1)}`.
	
	
  
	

**Problem 9:**
  A black box :math:`\mathcal{B}` receives two numbers :math:`k_1,k_2 \in \{ 1,\ldots,n \}` as inputs and returns a value :math:`v = \mathcal{B}(k_1,k_2)`. 
  What is the worst-case time complexity to find the maximum possible value :math:`v = \mathcal{B}(k_1,k_2)` for any two inputs.
  
  What if the black box receives permutations of :math:`n` elements as its inputs?


	
**Problem 10:**
  Prove or disprove the following statement:
  If :math:`f(n)` is in :math:`O(g(n))` and also :math:`g(n)` is in :math:`O(f(n))`,
  then :math:`f(n)` is also in :math:`\Theta(g(n))` (and :math:`g(n)` is in :math:`\Theta(f(n))`.
  (You can assume that :math:`f(n)` and :math:`g(n)` always take positive values.)

