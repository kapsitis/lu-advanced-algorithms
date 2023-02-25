# Fitting Permutation

Two arrays :math:`A` and :math:`B` contain :math:`n` positive integers
each. Let :math:`t` be positive integer -- named the *threshold*. 
Arrays :math:`A` and :math:`B` are in a relation: :math:`(A,B) \in R` if there exists
a permutation :math:`B'` of the array :math:`B` (a way to reorder elements 
of :math:`B`) such that :math:`A[i] + B'[i] \geq t` for all :math:`i = 0,\ldots,n-1`.

Write a C++ program that reads lines from the standard input and determines, 
if for a given thershold :math:`t` and two arrays :math:`A,B`, the 
pair :math:`(A,B)` is in relation :math:`R`.

Lines come in groups of three: The first line in 
each group contains a threshold number :math:`t`, 
followed by a list :math:`n` space-separated positive integers 
(representing array :math:`A`) and
then another :math:`n` space-separated positive integers (representing array :math:`B`). 
After that there is another group of three lines (possibly, with different values of :math:`t` and 
array length :math:`n`) and so on. Input is finished when there is a line containing just the digit ``0``.

**Constraints:** 

  * At most :math:`1000` subproblems (groups of three lines).,
  * :math:`1 \leq n \leq 1000`,
  * :math:`1 \leq t \leq 10^9`,
  * :math:`1 \leq A[i], B[i] \leq 10^9`.

**Sample Input**

.. code-block:: text

  11
  5 6 3 8 9
  8 2 6 5 6
  23
  12 14 12 7
  10 11 9 20
  0

**Sample Output:**
  
.. code-block:: text

  true
  false
	
**Explanation**  
  The first two arrays :math:`A = \{ 5,6,3,8,9 \}` and :math:`B = \{ 8,2,6,5,6 \}`
  are in the relation for threshold :math:`t = 11`. 
  For example, we can rearrange elements of the second array :math:`B' = \{ 6,5,8,6,2 \}`. 
  In this case :math:`A[i] + B'[i] = \{ 11,11,11,14,11 \}`

  The second two arrays  :math:`A = \{ 12, 14, 12, 7 \}` and :math:`B = \{ 10, 11, 9, 20 \}`
  are not in the relation for threshold :math:`t = 23`. 
  There are three numbers in :math:`A` (12,12,7) that would need to be added with numbers at least
  :math:`11` to add up to :math:`23`. On the other hand, there are just two 
  numbers :math:`\geq 11` in :math:`B`.
	

..  .. note:: 
..    Algorithmic tasks of this kind are known from other sources as well. 
..    See `HackerRank: Permuting Two Arrays <https://bit.ly/3tk8dlY>`_. 
  
  
 
