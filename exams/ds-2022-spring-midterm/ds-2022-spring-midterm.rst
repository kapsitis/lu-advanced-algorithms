Midterm, 2022-04-06
=========================




**Question 1:**
  Consider the following algorithm which can run on an array :math:`A[]`; 
  we also specify the leftmost and the right most element of the array in every call
  of :math:`\text{\sc ComputeSomething}`. 
  The initial call is :math:`\text{\sc ComputeSomething}(A[],0,n-1)`; after that 
  the function calls itself recursively. 
  It may also call  :math:`f(\ell)`, which runs in time :math:`O(\ell)`. 
  
  | :math:`\text{\sc ComputeSomething}(A[],\ell,r)`
  | :math:`\;\;\;\;\;` *total* = :math:`0`
  | :math:`\;\;\;\;\;` **if** :math:`\ell -r \leq 2`:  
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* = *total* + :math:`f(\ell)`
  | :math:`\;\;\;\;\;` **else**:
  | :math:`\;\;\;\;\;\;\;\;\;\;` :math:`m_1 = \lfloor (2\ell + r)/3 \rfloor`
  | :math:`\;\;\;\;\;\;\;\;\;\;` :math:`m_2 = \lfloor (\ell + 2r)/3 \rfloor`
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* = *total* + :math:`\text{\sc ComputeSomething}(A[\ell,m_1])`
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* = *total* + :math:`\text{\sc ComputeSomething}(A[m_1..m_2])`
  | :math:`\;\;\;\;\;\;\;\;\;\;` *total* = *total* + :math:`\text{\sc ComputeSomething}(A[m_2..r])`
  | :math:`\;\;\;\;\;` **return** *total*


  **(A)** 
    Denote by :math:`T(n)` the time complexity. 
    Write the recurrence for the time complexity of this algorithm (express :math:`T(n)` 
    in terms of :math:`T(\ldots)` for some smaller arguments). 
    
    
  **(B)**
    Apply Master Theorem to find some :math:`g(n)` such that :math:`\Theta(g(n))`. 


**Question 2:** 
  Some binary tree :math:`T` has exactly :math:`100` internal nodes.
  Other nodes in this tree are *leaves* -- they also contain information payload (keys, values, etc.), but
  they do not have non-empty children (both child pointers are :math:`\text{\sc Null}`.
  

  **(A)** 
    Can tree :math:`T` be a full binary tree? (In a full binary tree every node has either 
    two children or no children at all.)
    Can tree :math:`T` be a perfect binary tree? (In a perfect binary tree 
    all leaves have the same depth.)
	
  **(B)** 
    What is the largest and the smallest value for :math:`n` -- the total number of nodes in the 
    tree :math:`T`? Explain your estimates.
    
  **(C)**
    What is the largest and the smallest value for the :math:`\text{\sc Null}`
    pointers in this tree (such pointers do not count as internal nodes or leaves). 
	
  **(D)** 
    What is the largest and the smallest value for :math:`h` -- the height of :math:`T`? 
    Explain your estimates.
   


**Question 3:** 
  An array of :math:`10` elements are inserted into a 
  minimum heap in the order specified here:
  
  .. math::
  
    \{ 1, 7, 9, 4, 5, 3, 6, 8, 2, 10 \}


  Assume that we do not use any fast heap-building algorithms;
  we simply insert new elements and let them sift up (so that 
  any parent is always smaller than both of its children). 
  
  **(A)**
    Show the final state of the tree after all the nodes are inserted. 
    Draw this heap as a complete binary tree. 

  **(B)** 
    What is the total number of comparisons (:math:`a < b`) that is used 
    during this heap building process.

  
**Question 4:** 
  Consider the following regular 20-gon as a graph. It has :math:`20` vertices :math:`V_1,\ldots,V_{20}`, 
  it has exactly :math:`40` undirected edges -- all sides of the 20-gon, and also the diagonals that 
  connect vertices having distance exactly :math:`5`. Namely, :math:`(V_i,V_j)` exists in the
  graph iff :math:`(i - j) \equiv \pm 1 \pmod{20}` or :math:`(i - j) \equiv \pm 5 \pmod{20}`.
  
  .. image:: figs-ds-2022-spring-midterm/20gon.png
     :width: 2.5in
  

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
  
    * The current residual graph (initially -- it is simply the given graph with all flows equal to 0). 
    * The original graph with all the flows added.
    
  **(B)**
    Finally, redraw the original graph with all the maximum flows (use the same two-number labels for edges ``f/c``). 
    Show the min-cut which prevents any further augmenting paths (either highlight with 
    another color, or simply list the partition of graph's vertices into two disjoint sets that describe the cut).
  
  
  
  
  

