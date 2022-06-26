Worksheet, Week 12: Rolling Hash
==================================

**Objectives:**

  1. Sliding window technique with hashing.
  2. Rolling hash implementations.
  3. Naive string matching
  4. Rabin-Karp string matching
  5. Multi string matching.


Rolling Hash Functions
-----------------------

Rolling hash is an ADT: It is a data structure that accumulates some input fragment
as a sort of list/queue and supports the following operations:

* :math:`RH` ``:=`` :math:`\text{\sc RollingHash}(\mathtt{[]})` -- initialize a rolling hash to an empty list of symbols.
* :math:`RH.\text{\sc hash}()` -- return the hash value from the current list.
* :math:`RH.\text{\sc append}(val)` -- adds symbol ``val`` to the end of the list (like ``enqueue(val)`` for a queue)
* :math:`RH.\text{\sc skip}(val)` -- removes the front element from the list (like ``dequeue(val)`` for a queue).
  Parameter ``val`` is often implicit as it is stored at the front of the list stored
  in the rolling hash.

In the case of strings, the list is a list of characters. It can be a list
of anything, but elements on that list are represented as integers in some encoding.
For example if we interpret characters as ASCII codes, then
character ``'A'`` is stored as 65 and ``'B'`` is stored as 66.

We want to treat a list of items as a multidigit number :math:`u \in \mathcal{U}`
in base :math:`a` (the list in the rolling hash is interpreted as a big number).
For example, we can choose :math:`a = 256`, the alphabet size for ASCII code.

Polynomial Rolling Hash
^^^^^^^^^^^^^^^^^^^^^^^^^

This is one of the most popular implementations for rolling hashes;
it uses modular arithmetic.
Pick some prime number :math:`q` such that the number base :math:`a` is
not divisible by :math:`q`. Define the three ADT functions as follows:

* :math:`hash() = (u\,\text{mod}\,q)`
* :math:`append(val) = ((u \cdot a) + val)\,\text{mod}\,q = ((u\,\text{mod}\,q) \cdot a + val)\,\text{mod}\,q`
* :math:`skip(val) = (u - val \cdot (a^{|u|-1}\,mod\,q))\,\text{mod}\,q = \left( (u\,\text{mod}\,q) - val \cdot (a^{|u|-1}\,\text{mod}\,q)\right)\,\text{mod}\,q`

**Example:** Pick :math:`a = 100` and :math:`q = 23`.
Let ``RH`` be a rolling hash storing ``[61, 8, 19, 91, 37]``.
We can compute hash value:

.. math::

  hash([61, 8, 19, 91, 37]) = (6108199137\,\text{mod}\,23) = 12.

In general

.. math::

  hash([d_3, d_2, d_1, d_1]) = \left( d_3 \cdot a^3 + d_2 \cdot a^2 + d_1 \cdot a^1 + d_0 \cdot a^0 \right)\,\text{mod}\,q

To make it easier to compute, consider computation with a Hamming code:

.. math::

  hash([d_3, d_2, d_1, d_1]) = \left((( d_3 \cdot a + d_2) \cdot a + d_1)  \cdot a + d_0 \right) \,\text{mod}\,q

Making this faster:

  * Cache the result :math:`(u\,\text{mod}\,p)` (memorize it in the rolling hash data structure).
  * Avoid exponentiation in skip: cache :math:`a^{|u|-1}\,\text{mod}\,p`.
  * To append: multiply the cashed  :math:`(u\,\text{mod}\,p)` by base :math:`a`.
  * To skip: divide :math:`(u\,\text{mod}\,p)` by base (division is expensive, can use multicative inverse).




Cyclic Polynomial (Buzhash)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First introduce an arbitrary hash function ``h(c)`` mapping single characters to integers
from the interval :math:`{\displaystyle \left[0,2^{L}\right)}`.
Assume that there are not too many characters and the function can be defined by a lookup table.
Define the cyclical shift (bit rotation) to the left. For example, :math:`{\displaystyle s(\mathtt{1011})=\mathtt{0111}}`.
The rolling hash function for a list of characters :math:`[c_1,\ldots,c_k]` is defined by this equality:

.. math::

  H = s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) )  \oplus \ldots \oplus  s( h(c_{k-1}) ) \oplus   h(c_k).

It looks like a polynomial, but the powers are replaced by rotating binary shifts.
The result of this hash function is also a number in :math:`{\displaystyle \left[0,2^{L}\right)}`.

**Implementing rotation:**

Assume that we want to skip the first character: :math:`c_1` (and simultaneously add a new character :math:`c_{k+1}`.
Now the rolling hash covers the list :math:`[c_2,\ldots,c_k,c_{k+1}]` In this case do the following assignment
to the new hash value :math:`H`.

.. math::

  H := s(H) \oplus s^{k}(h( c_1 )) \oplus h(c_{k+1}),






Naive String Matching Algorithm
--------------------------------

**String Matching Problem:**
We have a text :math:`T` and a pattern :math:`P`.
We need to find all the offsets where the pattern :math:`P` occurs in the text.
Here is a straightforward solution that tries all the possible offsets:

| :math:`\text{\sc NaiveStringMatching}(T,P)`:
|     :math:`n = len(T)`
|     :math:`m = len(P)`
|     **for** :math:`s = 0` **to** :math:`n-m`:
|         **if** :math:`P[0:m-1]` ``==`` :math:`T[s:(s+m-1)]`:
|             **output** "Pattern found at offset", :math:`s`


**Worst-case behavior:** Pick some values for the length of pattern and the
text itself. For example, :math:`m = 4`, :math:`n = 14`.
Select the alphabet of just two letters: :math:`\mathcal{A} = \{ \mathtt{a}, \mathtt{b} \}`.
Consider the following pattern and text:

.. math::

  \left\{ \begin{array}{l}
  P = \mathtt{aaab} \\
  T = \mathtt{aaaaaaaaaaaaaa}\\
  \end{array} \right.

You will end up comparing all four times for any offset :math:`s = 0,\ldots,10`.
The total number of comparisons is :math:`4 \cdot 11 = 44`.
In general the worst-case complexity of the Naive String matching
is :math:`O(m \cdot (n-m+1)) = O(m \cdot n)`.





Rabin-Karp Algorithm
----------------------

| :math:`\text{\sc RabinKarpStringMatching}(T,P,a,q)`
|     :math:`rP = \text{\sc RollingHash}(\mathtt{[]})`
|     :math:`rT = \text{\sc RollingHash}(\mathtt{[]})`
|     **for** :math:`i` **in** :math:`\text{\sc range}(0,len(P))`:
|         :math:`rP.\text{\sc append}(P[i])`
|         :math:`rT.\text{\sc append}(T[i])`
|     **for** :math:`i` **in** :math:`\text{\sc range}(len(P),len(T))`:
|         **if** :math:`rP.\text{\sc hash}()` ``==`` :math:`rT.\text{\sc hash}()`:
|             (*Here we need to double-check as collisions are possible*)
|             **if** :math:`P` ``==`` :math:`T[i - len(P) + 1: i+1]`
|                 **output** "Pattern found at offset", :math:`i - len(P)+1`
|         :math:`rT.\text{\sc skip}(T[i - len(P)])`
|         :math:`rT.\text{\sc append}(T[i])`


**Worst-case behavior:** Can we ensure that false matches (hash collisions)
do not happen more frequently than with the probability :math:`1/len(P)`?


Rabin-Karp Multi-String Matching Algorithm
---------------------------------------------

**Problem:** We have a text :math:`T` of length :math:`n` as before.
But now we have not just one pattern to search, but a
set of :math:`k` patterns :math:`\mathcal{P} = \{ P_0, P_1, \ldots, P_{k-1} \}`;
each pattern has the same length :math:`m`.

| :math:`\text{\sc RabinKarpMultiString}(T, \mathcal{P}, m)`:
|     :math:`hashes` ``:=`` :math:`Set.\text{\sc Empty}()`
|     **foreach** :math:`P_i \in \mathcal{P}`:
|         :math:`rP_i = \text{\sc RollingHash}(\mathtt{[]})`
|         **for** :math:`j` **in** :math:`\text{\sc range}(0,m)`:
|             :math:`rP_i.\text{\sc append}(P[j])`
|         :math:`hashes.\text{\sc insert}(rP_i.\text{\sc hash}())`
|     :math:`rT = \text{\sc RollingHash}(\mathtt{[]})`
|     **for** :math:`j` **in** :math:`\text{\sc range}(0,m)`:
|         :math:`rT.\text{\sc append}(T[i])`
|     **for** :math:`j` **in** :math:`\text{\sc range}(1,n-m+1)`
|         **if** :math:`rT.\text{\sc hash}() \in hashes` **and** :math:`T[j:j+m-1] \in \mathcal{P}`
|             **output** "Pattern found at offset", :math:`j`
|         :math:`rT.\text{\sc skip}(T[j])`
|         :math:`rT.\text{\sc append}(T[j+m])`

This algorithm would take :math:`O(n + km)` running time.
Naive string matching could take :math:`O(nmk)` running time, if
we probe all the :math:`k` patterns one by one.



Bloom Filters
---------------

Often we have to find patterns in a very large collection of documents.
Optimal hashtables that use linear probing to resolve collisions typically
have load factors (number of keys stored divided by the size of the hashtable)
around :math:`\ln 2 \approx 0.7`. Namely, if the expected load for a hashtable
is expected to fluctuate around :math:`1000` items, then the optimal hashtable
would have about :math:`1400` slots.
Consequently, very large text documents (multiple megabytes) would require many
millions of slots in the hashtable.
This is not practical, so there is a useful optimization called *Bloom Filter*.

*Bloom Filter* creates a single set-like data structure
that supports two operations:

* Add a new item to a set: ``BF.add(item)``.
* Tests, if an item belongs to a set: ``BF.contains(item)`` (return Boolean true/false).

.. note::
  Unlike regular hashtables Bloom Filters often do not support remove
  operations. They are useful in contexts where we need to
  check membership of a comparatively large set, but we have limited space to store
  that set.

It can be implemented  by creating :math:`k` hash functions -- each one randomly
and independently from other hash functions maps an item to one of :math:`m` bits.
Assume that we have inserted :math:`n` elements, the probability that a certain
bit is still :math:`0` is:

.. math::

  p = \left(1-\frac{1}{m}\right)^{kn} \approx e^{-kn/m};

Now test membership of an element that is not in the set.
Each of the :math:`k` array positions computed by the hash functions is :math:`1` with a probability :math:`(1-p)`.
The probability of all of them being :math:`1`, which would cause the Bloom filter to erroneously claim
that the element is in the set, is the following:


.. math::

  \varepsilon = \left(1-\left[1-\frac{1}{m}\right]^{kn}\right)^k \approx \left( 1-e^{-kn/m} \right)^k.

Given the size of the bit-array :math:`m` and the number of items to be inserted :math:`n`, we can find
the optimal number :math:`k`:

.. math::

  k = \frac{m}{n} \ln 2

If we know the maximum tolerance of false positives :math:`\varepsilon`, then we can adjust the value :math:`m` accordingly
so that we have limited number of false positives.


Questions
----------

**Question 1 (Computing Rolling Hash -- Polynomial Method):**
  Assume that we have an alphabet of :math:`100` symbols.
  They are denoted by pairs of digits: :math:`\{ 00, 01, \ldots, 99 \}`.
  Select the sliding window size :math:`m = 5` and the prime number for modulo :math:`q = 23`.

  Let the input be ``[3, 14, 15, 92, 65, 35, 89, 79, 31]``.

  * Initialize an empty rolling hash ``rH`` and add the first five numbers using ``append()`` function
    defined as follows:

    .. math::

      append(val) = ((u \cdot a) + val)\,\text{mod}\,q = ((u\,\text{mod}\,q) \cdot a + val)\,\text{mod}\,q.

  * Show how the rolling hash can "roll" from the list ``[3, 14, 15, 92, 65]`` to ``[14, 15, 92, 65, 35]`` (first skip value ``3``,
    then append value ``35``.

**Question 2 (Computing Rolling Hash -- Cyclic Polynomial):**
  Consider :math:`16` Latin letters with randomly assigned 4-bit codes (i.e. :math:`L=4`):

  ==========  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====
  Letter         A     B     C     D     E     F     G     H     I     J     K     L     M     N     O     P
  h(x)        1100  0100  0010  0110  0111  0000  1001  1111  0101  1101  1110  1011  0011  1010  1000  0001
  ==========  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====  ====

  Also assume that the sliding window has size :math:`k=5`.
  Find the hash value for :math:`ABIDE` and then rotate it over to :math:`BIDEN`.
  Please recall that the rolling hash uses the following formula:

  .. math::

    H = s^{k-1}(h( c_1 )) \oplus s^{k-2}( h(c_2) )  \oplus \ldots \oplus  s( h(c_{k-1}) ) \oplus   h(c_k),


**Question 3 (Rolling Hash ADT with Cyclic Polynomial):**
  Write formulas for the Rolling Hash functions (when using Cyclic Polynomial or Buzhash):

  * Formula to initialize ``RH`` to an empty list.
  * Formula to append a new character :math:`c_i` to the existing list (without skipping anything).
  * Formula to skip the head of the existing list :math:`c_j` (without appending anything).

**Question 4 (Average Complexity of Naive String Matching)**
  Suppose that pattern :math:`P` and text :math:`T` are randomly chosen strings of length :math:`m` and :math:`n`,
  respectively, from an alaphabet with :math:`a` letters (:math:`a \geq 2`).
  What is the expected character to character comparisons in the naive algorithm,
  if any single comparison has a chance :math:`1/a` to succeed?
