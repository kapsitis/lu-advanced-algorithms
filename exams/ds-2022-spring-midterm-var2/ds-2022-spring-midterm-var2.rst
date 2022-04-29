Midterm, 2022-04-29
=========================




**Question 1:**
  Consider the following algorithm which runs on a (zero-based) array :math:`\mathtt{A[]}`. 
  The length of the array is :math:`n`; the elements of array are non-negative integers
  smaller than :math:`2^m` (i.e. ``unsigned`` type using :math:`m` bits each). 
  
  The initial call is :math:`\text{\sc ComputeSomething}(\mathtt{A[]},n)`; after that 
  the function calls itself recursively. 
  This function calls :math:`\text{\sc Gcd}(x,y)` or 
  :math:`\text{\sc Gcd}(x,y,z)` (the *greatest common divisor* of two or three numbers). 
  This function uses Euclidean algorithm; you may assume that its 
  time complexity is :math:`O(\max(|x|,|y|))` or :math:`O(\max(|x|,|y|,|z|))` respectively, 
  where :math:`|x|` denotes the length of argument :math:`x` (in bits). 
    
  | :math:`\text{\sc ComputeSomething}(\mathtt{A[]},n)`
  | :math:`\;\;\;\;\;` **if** :math:`n` ``==`` :math:`1`:  
  | :math:`\;\;\;\;\;\;\;\;\;\;` **return** :math:`A[0]`
  | :math:`\;\;\;\;\;` **else if** :math:`n` ``==`` :math:`2`:  
  | :math:`\;\;\;\;\;\;\;\;\;\;` **return** :math:`\text{\sc Gcd}(A[0],A[1])`
  | :math:`\;\;\;\;\;` **else if** :math:`n` ``==`` :math:`3`:  
  | :math:`\;\;\;\;\;\;\;\;\;\;` **return** :math:`\text{\sc Gcd}(A[0],A[1],A[2])`
  | :math:`\;\;\;\;\;` **else if** :math:`n \equiv 0\ (\text{mod} 5)`:
  | :math:`\;\;\;\;\;\;\;\;\;\;` **return** :math:`\text{\sc Gcd}(A[n-1],A[n-2],A[n-3])\ +\ \text{\sc ComputeSomething}(\mathtt{A[]},n-3)`  
  | :math:`\;\;\;\;\;` **else**:
  | :math:`\;\;\;\;\;\;\;\;\;\;` **return** :math:`\text{\sc Gcd}(A[n-1],A[n-2])\ +\ \text{\sc ComputeSomething}(\mathtt{A[]},n-2)`


  **(A)** 
    Denote by :math:`T(n,m)` the time complexity of this algorithm on an array with :math:`n` elements of size :math:`m`. 
    Express :math:`T(n,m)` 
    in terms of :math:`T(\ldots)`, where one or both arguments are smaller to reflect how the time complexity of the 
    recursive call affects the time complexity of the overall algorithm. 
        
  **(B)**
    Find some :math:`g(n,m)` such that :math:`T(n)` is in  :math:`O(g(n))` and justify your answer.
    If multiple asymptotic bounds are possible, select the smallest one among them.



.. only:: Internal 

  **Answer:** 

  TBD
    
  :math:`\square`


**Question 2:** 
  Assume that you know the degrees of some graph with :math:`6` vertices; and we need to know what kind of graph 
  can or cannot be constructed, if the degrees are like the given ones.
  
  **(A)**
    Write a sequence of six numbers that are values in the interval :math:`[1;5]` 
    such that there is **no graph** with the given degrees.
    (Or explain, why such sequence does not exist.)

  **(B)**
    Write a sequence of six numbers that are values in the interval :math:`[1;5]` 
    such that there exists a graph with such degrees, but there is **no bipartite graph** with the given vertices.
    (Or explain, why such sequence does not exist.)
    
  **(C)** 
    Write a sequence of six numbers that are values in the interval :math:`[1;5]` 
    such that there exists a graph with such degrees that there exists a bipartite graph with the given vertices, 
    but this graph does not have a perfect matching. 
    (Or explain, why such sequence does not exist.)

   
   
.. only:: Internal 

  **Answer:** 
  
  TBD
    
  :math:`\square` 
    
    


**Question 3:** 
  Assume there is a queue implemented as a cyclical array. 
  A queue is implemented as an array with :math:`size=15` elements; it has two extra variables 
  :math:`front` (pointer to the first element) and :math:`length` (the current number of
  elements in the queue). 
  Enumeration of array elements starts with 0. The array is filled in a circular fashion. The command
  ``enqueue(elt)`` inserts a new element at
  :math:`(front + length)\ \text{mod}\ size`.  
  The ``enqueue(elt)`` command also increments the ``length``.
  
  The command ``dequeue()`` does not change anything in the ``array``, 
  but increments ``front`` by :math:`1` and decreases
  ``length`` by 1. Thus the queue becomes shorter by 1.
  
  
  The initial state of the queue is the following: 
  
  .. code-block:: text
  
    size = 15
    front = 0
    length = 0
    array[] = 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 
    
  The following list of size :math:`25` contains all prime numbers from :math:`[1;100]`. 
  After that we enqueue five elements, dequeue three elements (and repeat these actions five times). 
      
  .. code-block:: cpp
  
    list<int> L = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};
    for (int i = 0; i < 5; i++) {
        queue.enqueue(L[5*i]); 
        queue.enqueue(L[5*i+1]); 
        queue.enqueue(L[5*i+2]); 
        queue.enqueue(L[5*i+3]); 
        queue.enqueue(L[5*i+4]); 
        queue.dequeue();
        queue.dequeue();
        queue.dequeue();
    }
        



.. only:: Internal 

  **Answer:** 

  TBD

  :math:`\square`






  
**Question 4:** 
  We build a ternary tree as follows: Add node :math:`v_0`. 
  Then :math:`33` times pick the rightmost leaf on the last level and add three children to it. 
  You will end up with a tree with :math:`100` nodes (see figure): 
  
  .. image:: figs-ds-2022-spring-midterm-var2/ternary-tree.png
     :width: 2in
     
  **(A)** 
    Run the post-order traversal of this tree; find the four \"middle\" vertices :math:`a_{48}`, 
    :math:`a_{49}`, :math:`a_{50}`, :math:`a_{51}`. 
    
  **(B)** 
    Run the in-order traversal of this tree; find the four \"middle\" vertices :math:`b_{48}`, 
    :math:`b_{49}`, :math:`b_{50}`, :math:`b_{51}`. 
    (In-order traversal of a ternary tree -- visit the leftmost subtree, then the parent, then the two 
    remaining subtrees). 
    


**Question 5:** 
  Run the Bellman-Ford algorithm to find the minimum distance 
  from the source :math:`v_0` to all the other vertices. 
  
  .. image:: figs-ds-2022-spring-midterm-var2/bellman-ford.png
     :width: 2in
  
  The pseudocode of Bellman-Ford algorithm is this: 
  
  | :math:`\text{\sc BellmanFord}(G,w,s)`:
  |     **for** **each** vertex :math:`v \in V`: :math:`\;\;\;\;\;` *(initialize vertices to run shortest paths)*
  |         :math:`v.d = \infty`
  |         :math:`v.p = \text{\sc Null}`
  |     :math:`s.d = 0` :math:`\;\;\;\;\;` *(the distance from source vertex to itself is 0)*
  |     **for** :math:`i=1` **to** :math:`|V|-1` :math:`\;\;\;\;\;` *(repeat* :math:`|V|-1` *times)*
  |         **for** **each** edge :math:`(u,v) \in E`
  |             **if** :math:`v.d > u.d + w(u,v)`: :math:`\;\;\;\;\;` *(relax an edge, if necessary)*
  |                 :math:`v.d = u.d + w(u,v)`
  |                 :math:`v.p = u`

  As you run the algorithm, build a table (current distances from the source :math:`v_0` to all the other vertices)
  every time when some distances change (due to edge relaxing). 
  The table looks something like this (but at each stage you specify actual edge that was 
  relaxed -- instead of :math:`(v_i,v_j)`; and also the actual distances). 
  
    =======================  ==============  ==============  ==============  ==============  ==============  ==============  
    Vertices                    :math:`v_0`     :math:`v_1`     :math:`v_2`     :math:`v_3`     :math:`v_4`     :math:`v_5`
    Initial distances                     0  :math:`\infty`  :math:`\infty`  :math:`\infty`  :math:`\infty`  :math:`\infty`
    Relax :math:`(v_i,v_j)`               ?               ?               ?               ?               ?               ?
    :math:`\ldots`           :math:`\ldots`
    =======================  ==============  ==============  ==============  ==============  ==============  ==============  
  
  Make sure that in the **for each** loop you visit all the edges in their lexicographical order. 
  Show all the the relaxed edges in this table, but
  in case some edge does not result in changes of any distances, do not enter it into the table. 
  
  

.. only:: Internal 

  **Answer:**
   

     
  :math:`\square`
  
  

