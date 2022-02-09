Worksheet 1, 2022-02-09
=========================



**Definition:** 
  Let :math:`g \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` be a function from natural numbers (non-negative integers)
  to non-negative real numbers. 
  Then :math:`O(g)` is the set of all functions :math:`f \colon \mathbb{N} \rightarrow \mathbb{R}`
  such that there exist real constants :math:`c>0` and :math:`n_0 \in \mathbb{N}` satisfying
  :math:`{\displaystyle \forall n \in \mathbb{N}\ \big( n \geq n_0 \rightarrow | f(n) | \leq c \cdot g(n) \big).}`
    
**Definition:**
  Let :math:`g \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` be a function. 
  Then :math:`\Omega(g)` is the set of all functions :math:`f \colon \mathbb{N} \rightarrow \mathbb{R}` 
  such that there exist real constants :math:`c>0` and :math:`n_0 \in \mathbb{N}` satisfying 
  :math:`{\displaystyle  \forall n \in \mathbb{N}\ \big( n \geq n_0 \rightarrow | f(n) | \geq c \cdot g(n) \big).}`
    
**Definition:** 
  Define :math:`\Theta(g)` to be the intersection of :math:`O(g)` and :math:`\Omega(g)`. 
  
  Formally, let :math:`g \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` be a function.
  Then :math:`\Theta(g)` is the set of all functions :math:`f: \mathbb{N} \to \mathbb{R}` 
  such that there exist real constants :math:`c_1, c_2 > 0` and :math:`n_0 \in \mathbb{N}` satisfying 

  .. math::
  
    \forall n \in \mathbb{N}\ \big( n \geq n_0 \rightarrow   c_1 \cdot g(n) \leq  | f(n) | \leq c_2 \cdot g(n) \big).


In spoken language we often use descriptive concepts:

* If :math:`f \in O(g)`, then :math:`g(n)` is called *asymptotic upper bound* of :math:`f(n)`. 
* If :math:`f \in \Omega(g)`, then :math:`g(n)` is called *asymptotic lower bound* of :math:`f(n)`.
* If :math:`f \in \Theta(g)`, then :math:`g(n)` is called *asymptotic growth order* of :math:`f(n)`.

**Definition:**
  The *time complexity* of an algorithm is described by a function :math:`f(n)`, 
  if for **any** input of length :math:`n` bytes, the time spent running the algorithm is bound
  from above by :math:`f(n)`. 


Changing the base of a logarithm: :math:`{\displaystyle \forall a,b,m > 1 \left( \log_a b = \frac{ \log_m b }{ \log_m a } \right)}`



Binomial coefficients: :math:`{\displaystyle \binom{n}{k} = \frac{n!}{(n-k)!k!}}`.
Stirling's formula: :math:`{\displaystyle n! \sim \sqrt{2 \pi n}\left(\frac{n}{e}\right)^n}`.

**Definition:**
  Two functions :math:`f,g \colon \mathbb{N} \to \mathbb{R}` are *asymptotically equivalent* (write :math:`f(n) \sim g(n)`) iff
  :math:`{\displaystyle  \lim\limits_{n \rightarrow \infty} \frac{f(n)}{g(n)} = 1. }`

---------

**Question 1 (Warm up):**

  * Every function :math:`f(n)` is both :math:`\Omega(1)` and :math:`O(e^n)`.
  * If a function is :math:`O(1)`, then it must be a constant function: :math:`f(n) = C` for some :math:`C \in \mathbb{R}`. 
  * Define a function :math:`f \colon \mathbb{N} \rightarrow \mathbb{R}_{0+}` which equals :math:`n^2` for infinitely many :math:`n`
    and equals :math:`n^3` for infinitely many :math:`n`.



**Question 2:** 
  You are given Algorithm1, which is :math:`O(n^a)`, and Algorithm2, which is :math:`O(n^b)`, 
  for :math:`a,b \in \mathbb{N}`.
  
  * Give another function :math:`f(n) \neq n^a`, so that Algorithm1 is in :math:`O(f(n))`.
  * What is asymptotic upper bound of the runtime, if a program first executes Algorithm1, then Algorithm2?
  * What is the closest upper bound on the algorithm that runs Algorithm1, which calls 
    Algorithm2 :math:`n` times? 


**Question 3:** 
  Suppose that Algorithm3 has asymptotic time complexity in :math:`O(2^{n+1})` 
  and Algorithm4 has asymptotic time complexity in :math:`O(2^{2n})`. 
  Are any of these algorithms (Algorithm3 or Algorithm4) in :math:`O(2^n)`?


  
**Question 4:** 
  Prove or disprove the following statement:
  If :math:`f(n)` is in :math:`O(g(n))` and also :math:`g(n)` is in :math:`O(f(n))`, 
  then :math:`f(n)` is also in :math:`\Theta(g(n))` (and :math:`g(n)` is in :math:`\Theta(f(n))`.   
  (You can assume that :math:`f(n)` and :math:`g(n)` always take positive values.) 


**Question 5:** 
  Order these functions in increasing order regarding Big-O complexity 
  (:math:`f_i` is considered "not larger" than :math:`f_j` iff :math:`f_i \in O(f_j)`. 

  * :math:`f_1(n) = n^{0.9999} \log_2 n`
  * :math:`f_2(n) = 10000n`
  * :math:`f_3(n) = 1.0001^n`
  * :math:`f_4(n) = n^2`
  
  
**Question 6:**
  Order these functions in increasing order regarding Big-O complexity: 
  
  * :math:`f_1(n) = 2^{2^{10000}}`
  * :math:`f_2(n) = 2^{10000n}`
  * :math:`f_3(n) = \binom{n}{2} = C_n^2`
  * :math:`f_4(n) = \binom{n}{\lfloor n/2 \rfloor}`
  * :math:`f_5(n) = \binom{n}{n-2}`
  * :math:`f_6(n) = n!`
  * :math:`f_7(n) = n\sqrt{n}`

**Question 7:**
  Order these functions in increasing order regarding Big-O complexity: 

  * :math:`f_1(n) = n^{\sqrt{n}}`
  * :math:`f_2(n) = 2^n`
  * :math:`f_3(n) = n^{10} \cdot 2^{n/2}`
  * :math:`{\displaystyle \sum\limits_{i = 1}^{n} (i + 1)}`. 


**Question 8:**
  Select the correct asymptotic complexity of an algorithm with runtime
  :math:`T(n, n)` where

  .. math:: 
  
    \left\{ \begin{array}{l}
    T(x, c) = \Theta(x)\;\mbox{for $c \leq 2$},\\    
    T(c, y) = \Theta(y)\;\mbox{for $c \leq 2$, and},\\    
    T(x, y) = \Theta(x + y) + T(\lfloor x/2 \rfloor, \lfloor y/2 \rfloor)\;\mbox{otherwise}.\\
    \end{array} \right.
    
  a. :math:`\Theta(\log n)`. 
  b. :math:`\Theta(n)`.
  c. :math:`\Theta(n \log n)`. 
  d. :math:`\Theta(n log^2 n)`.
  e. :math:`\Theta(n^2)`.
  f. :math:`\Theta(2^n)`.


