Midterm, 2022-04-06
=========================




**Question 1:**
  Consider the following algorithm which can run on an array :math:`\mathtt{A[]}`; 
  we also specify the leftmost and the rightmost element of the array in every call
  of :math:`\text{\sc ComputeSomething}(\ldots)`. 
  The initial call is :math:`\text{\sc ComputeSomething}(\mathtt{A[]},0,n-1)`; after that 
  the function calls itself recursively. 
  It may also call  :math:`f(\ell)`, which runs in time :math:`O(\ell)`. 
  
  | :math:`\text{\sc ComputeSomething}(\mathtt{A[]},\ell,r)`
  | :math:`\;\;\;\;\;` *total* = :math:`0`
  | :math:`\;\;\;\;\;` **if** :math:`\ell -r \leq 2`:  
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* = *total* + :math:`f(\ell)`
  | :math:`\;\;\;\;\;` **else**:
  | :math:`\;\;\;\;\;\;\;\;\;\;` :math:`m_1 = \lfloor (2\ell + r)/3 \rfloor`
  | :math:`\;\;\;\;\;\;\;\;\;\;` :math:`m_2 = \lfloor (\ell + 2r)/3 \rfloor`
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* ``+=`` :math:`\text{\sc ComputeSomething}(\mathtt{A[]},\ell,m_1)`
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* ``+=`` :math:`\text{\sc ComputeSomething}(\mathtt{A[]}, m_1, m_2)`
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* ``+=`` :math:`\text{\sc ComputeSomething}(\mathtt{A[]},m_2,r)`
  | :math:`\;\;\;\;\;` **return** *total*


  **(A)** 
    Denote by :math:`T(n)` the time complexity of this algorithm on an array with :math:`n-1` elements. 
    Write the recurrence for the time complexity of this algorithm. Namely, express :math:`T(n)` 
    in terms of :math:`T(\ldots)` for some smaller arguments.
    
    
  **(B)**
    Apply Master Theorem to find some :math:`g(n)` such that :math:`T(n)` is in  :math:`\Theta(g(n))`. 



.. only:: Internal 

  **Answer:** 
  
  **(A)**
    Let us compute the array size in the call of this function by :math:`r - \ell + 1` 
    (:math:`1` is added, since both endpoints are included). Thus, the first call 
    on array :math:`[0;n-1]` uses array length equal to :math:`(n-1) - 0 + 1 = n`. 
  
    The recurrence should reflect the three recursive calls of this function. Take into
    account that the recursive calls are now on shorter fragments of the input array -- 
    all the new array lengths are 
    :math:`m_1 - \ell + 1`, :math:`m_2 - m_1 + 1`, :math:`r - m_2 + 1`. They are all less or equal than 
    :math:`\lceil n/3 \rceil`. 
    Computing the :math:`m_1` and :math:`m_2` takes :math:`O(1)` time. 
            
    So the recurrence relation describing the time complexity is 
    
    .. math::
      
      \begin{array}{l}
      T(k) = 3T(\lceil k/3 \rceil) + O(1),\ \mbox{if $k>4$}\\
      T(k) = O(n),\ \mbox{if $k < \leq 3$}\\
      \end{array}
      
    Observe that the last line contains the only expression that is :math:`O(n)` (does not depend on 
    the current length of the array being processed (the variable :math:`k`), but rather on
    the length of the original array :math:`n` (more precisely, it depends on :math:`\ell`, the numeric value 
    of the left endpoint of the input, which does not decrease as the size of the processed array decreases). 
    
    We replace :math:`O(\ell)` by :math:`O(n)`, because :math:`\ell` changes every time, but :math:`n` is the
    upper bound of all values :math:`\ell`. 
   
  **(B)**
    By Master's theorem the number of recursive calls of :math:`\text{\sc ComputeSomething}(\ldots)` 
    is in :math:`O(n \log n)`. 
    Since the recursion every time ends with a call that costs :math:`O(n)`, we need to multiply this 
    estimate from the Master's theorem by :math:`O(n)` to get the overall complexity :math:`O(n^2 \log n)`. 
    
  :math:`\square`


**Question 2:** 
  Some binary tree :math:`T` has exactly :math:`100` *internal nodes*.
  Other nodes in this tree are *leaves* -- they also contain information payload (keys, values, etc.), but
  they do not have non-empty children (both child pointers are :math:`\text{\sc Null}`).
  

  **(A)** 
    Can tree :math:`T` be a full binary tree? 
    Can tree :math:`T` be a complete binary tree? 
    Can tree :math:`T` be a perfect binary tree?

    *To remind the tree terminology: In a full binary tree every node has either 
    two children or no children at all. Complete trees are used to implement heaps (nodes are 
    filled in level by level). In perfect binary trees 
    all leaves have the same depth.*
	
  **(B)** 
    What is the largest and the smallest value for :math:`n` -- the total number of nodes in the 
    tree :math:`T`? Explain your estimates.
    
  **(C)**
    What is the largest and the smallest value for the :math:`\text{\sc Null}`
    pointers in this tree (such pointers do not count as internal nodes or leaves). 
	
  **(D)** 
    What is the largest and the smallest value for :math:`h` -- the height of :math:`T`? 
    Explain your estimates.
   
   
.. only:: Internal 

  **Answer:** 
  
  **(A)**
    The tree :math:`T` can be full (every time you need a new internal node, add to it two children -- until you reach the
    necessary number of children). 
    
    The tree can be complete (you build a perfect binary tree containing all the nodes, but leave the last level 
    incomplete -- fill it in from the left side). 
    
    The tree cannot be perfect, because the only perfect trees (containing all levels filled in up to the maximum) 
    may contain :math:`0,1,3,7,15,31,63,127,\ldots` internal nodes; in general it must be :math:`2^k - 1`. 
    The number :math:`100` is not in this list. 
   
  **(B)**
    The smallest number of nodes is :math:`100 + 1` (we just build a long skinny path and add one leaf at the very bottom). 
    
    The largest number of nodes is :math:`100 + 101` (for every internal node add two children; then the count of leaves are always 
    one more than the count of the internal nodes). 
    
   

  **(C)**
    The count of :math:`\mathtt{Null}` pointers in a binary tree is always one more than the number of nodes.
    
    * If the total number of nodes is :math:`101` (the smallest one), then the number of 
      :math:`\mathtt{Null}` pointers is :math:`102`. 
      
    * If the total number of nodes is :math:`201` (the largest one), then the number of 
      :math:`\mathtt{Null}` pointers is :math:`202`. 
   
  **(D)**
    The largest height is for the skinny tree (with :math:`101` nodes). The height is :math:`100`. 
    
    The smallest height is for the tree which is complete. It is easy to figure out its height inductively: 
    
    * If there are up to :math:`3` inner nodes, the complete binary tree has height :math:`2`
    * If there are up to :math:`7` inner nodes, the complete binary tree has height :math:`3`
    * If there are up to :math:`2^k - 1` inner nodes, the complete binary tree has height :math:`k`
    
    In our case there are up to :math:`127 = 2^7 -1` inner nodes, so the height must be :math:`7`. 
    

    
  :math:`\square` 
    
    


**Question 3:** 
  An array of :math:`10` elements are inserted into a 
  minimum heap in the order specified here:
  
  .. math::
  
    1, 7, 9, 4, 5, 3, 6, 8, 2, 10.


  Assume that we do not use any fast heap-building algorithms;
  we just insert new elements and let them sift up. 
  
  **(A)**
    Show the final state of the tree after all the nodes are inserted in this way. 
    Draw this heap as a complete binary tree. (You can also show intermediate results 
    to show your approach.)

  **(B)** 
    What is the total number of comparisons (:math:`a <^{?} b`) that is used 
    during this heap building process.


.. only:: Internal 

  **Answer:** 

  **(A)**
    The stages of building the heap are shown in the image: 
    
    .. image:: figs-ds-2022-spring-midterm/heap-solution.png
       :width: 3in
    
    For each heap insert operation we also write the number of comparisons (C, 2C etc.) 
    needed to complete that operation.
    
   
  **(B)**
    It needs about :math:`13` comparisons (typically, :math:`1` comparison 
    per one heap insert; sometimes :math:`2` comparisons). 
    In larger trees the cost per one heap insert is :math:`O(n \log n)`. 
    
    (In fact, it is possible to do cheaper heap inserts if we need to 
    build a heap from the predefined list of nodes. If you proceed by layers
    bottom up, it takes :math:`O(n \log n)` steps.)

  :math:`\square`






  
**Question 4:** 
  Consider the following regular 20-gon as a graph. It has :math:`20` vertices :math:`V_1,\ldots,V_{20}`, 
  it has exactly :math:`40` undirected edges -- all sides of the 20-gon, and also the diagonals that 
  connect vertices having distance exactly :math:`5`. Namely, :math:`(V_i,V_j)` exists in the
  graph iff :math:`(i - j) \equiv \pm 1 \pmod{20}` or :math:`(i - j) \equiv \pm 5 \pmod{20}`.
  
  .. image:: figs-ds-2022-spring-midterm/20gon.png
     :width: 2in
  

  **(A)**
    Draw the BFS tree that is created if this graph is traversed in the BFS order, and vertex :math:`V_1` is 
    the root. 
    Make sure to show the labels of all vertices. Assume that the children for each internal node in the BFS tree are visited 
    in the order of increasing numbers (namely, if a parent node :math:`V_i` discovers two neighbors :math:`V_j` and :math:`V_k`
    where :math:`k>j`, then :math:`V_k` is a sibling drawn to the right of :math:`V_j`). 
    
  **(B)**
    What is the number of internal nodes in this BFS tree? What is the number of leaves? 
    What is the height of the BFS tree (the number of edges leading from its root to the deepest leaf)?
  
  **(C)**
    Consider a graph -- regular 100-gon with edges that are all its sides
    and also those diagonals that connect vertices with distance exactly :math:`5`. 
    What is the height of the BFS tree created from this graph?


.. only:: Internal

  **Answer:**
  
  **(A)**
    The BFS tree is shown in the picture below:
    
    .. image:: figs-ds-2022-spring-midterm/20gon-bfs.png
       :width: 4in
    
  **(B)**
    The number of internal nodes is :math:`11`, 
    the number of leaves is :math:`9`. 
    The height of the tree is :math:`4` -- the shortest paths from :math:`v_1` to the 
    "worst" vertices (either :math:`v_{9}` or :math:`v_{13}`) have length :math:`4`. 

  **(C)**
    In case of a regular 100-gon, we need to find the "worst" vertices -- the ones which 
    are furthest away from :math:`v_1`, if we are only allowed to jump :math:`1` or :math:`5`
    units back or forth. 
    
    Consider vertices :math:`v_{49}` and :math:`v_{53}`. 
    Both of them can be reached within ... steps:
    
    .. math::
    
      \begin{array}{l}
      v_1 \rightarrow v_2 \rightarrow v_3 \rightarrow v_4 \rightarrow v_9 \rightarrow v_{14} \rightarrow v_{19} \rightarrow v_{24}
      \rightarrow v_{29} \rightarrow v_{34} \rightarrow v_{39} \rightarrow v_{44} \rightarrow v_{49}.\\
      v_1 \rightarrow v_2 \rightarrow v_3 \rightarrow v_8 \rightarrow v_{13} \rightarrow v_{18} \rightarrow v_{23}
      \rightarrow v_{28} \rightarrow v_{33} \rightarrow v_{38} \rightarrow v_{43} \rightarrow v_{48} \rightarrow v_{53}.\\
      \end{array}
      
    In both cases the paths are of length :math:`12`, so the BFS tree height must also be :math:`12`. 
    There can be **no** vertices that need longer paths. You can classify all the vertices in this 
    graph accordingly to the remainder when dividing by :math:`5`.
      
    * Among all the vertices :math:`v_{i}` such that :math:`i \equiv 4 \pmod {5}` the 
      vertex :math:`v_{49}` is the furthest away from :math:`v_1`. All the others need
      fewer jumps of length :math:`5` (either clockwise or counter-clockwise). 
    * Among all the vertices :math:`v_{i}` such that :math:`i \equiv 3 \pmod {5}` the
      vertex :math:`v_{53}` is the furthest away from :math:`v_1`. Verification is 
      similar to the previous case.

            

  :math:`\square`





**Question 5:** 
  Run the Edmonds-Karp maximum flow algorithm on the graph provided. 
  
  .. image:: figs-ds-2022-spring-midterm/flow-graph.png
     :width: 2in
     
  **(A)**
    Run Edmonds-Karp algorithm on the graph shown above. 
    For every phase highlight the the augmenting path (or simply list its vertices), 
    find the *residual flow* of this augmenting graph. 
    Next to it draw a copy of the flow graph where 
    every age is labeled by two numbers ``f/c`` -- the actual flow ``f`` 
    and also the capacity ``c`` of the edge.  
    Thus, every phase shows two oriented graphs: 
    First: The current residual graph (initially -- it is simply the given graph with all flows equal to 0). 
    Second: The original graph with edge capacities and new flows.
    
  **(B)**
    Finally, redraw the original graph with all the maximum flows (use the same two-number labels for edges ``f/c``). 
    Show the min-cut which prevents any further augmenting paths (either highlight with 
    another color, or simply list the partition of graph's vertices into two disjoint sets that describe the cut).
  
  

.. only:: Internal 

  **Answer:**
   
  See \"Max Flow Handout\" under Week9 in E-Studijas. It contains examples how to write down such solutions.
     
  :math:`\square`
  
  

