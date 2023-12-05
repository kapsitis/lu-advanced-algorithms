Handout 14: MST and Maximum Flow Problems
===========================================



Minimum Spanning Trees
-----------------------

Prim's algorithm finds a minimum spanning
tree in an undirected graph with given edge weights.
See also `<https://bit.ly/2VLz3DK>`_.
It is an efficient algorithm; it requires :math:`O((m+n)\log_2 n)` time, if
we use priority queues.
In this exercise you do not need to implement a priority queue;
assume that you can always compute the minimums in your head and
grow the MST accordingly.


Problem
^^^^^^^^^

**Question 4 (Prim's algorithm):**
  Prim's algorithm for the graph shown in Figure:

  .. figure:: figs/problem-graph.png
     :width: 3in
     :alt: Graph diagram

     Graph Diagram for Prim's Algorithm.


  **(A)**
    Vertex :math:`A` will be your source vertex.
    It is the first vertex added to the MST vertice set :math:`S`.
    At every step you find the lightest edge that connects
    some vertex in :math:`S` to some vertex not in :math:`S`.
    Add this new vertex to a graph and remember the edge you added.
    Show how the Prim's MST (Minimum Spanning Tree grows) one edge at a time.

    .. note::
      In cases when there is a choice between multiple lightest edges of the same
      weight, pick the edge :math:`(v,w)` with :math:`v \in S` and
      :math:`w \not\in S` such that :math:`(v,w)` lexicographically precedes
      any other lightest edge.


  **(B)**
    Redraw the graph,
    highlight the edges selected for MST (make them bold or color them differently).
    Add up the total weight of the obtained MST and
    write this in your answer (it should be the minimum value among all the
    possible spanning trees in this graph).



**Question 5 (Prim's algorithm):**
  Denote the last three digits of your Student ID by :math:`a,b,c`.
  Student ID often looks like this: :math:`\mathtt{201RDBabc}`, where
  :math:`a,b,c` are digits.
  Compute three more digits :math:`x,y,z`:

  .. math::

    \left\{ \begin{array}{l}
    x = (b + 4)\ \text{mod}\ 10\\
    y = (c + 4)\ \text{mod}\ 10\\
    z = (a + b + c)\ \text{mod}\ 10\\
    \end{array} \right.

  In this task the input graph :math:`G = (V,E)` is given by its adjacency matrix:

  .. math::

    M_G = \left( \begin{array}{cccccccc}
    0 & 0 & 5 & 8 & y & 0 & 0 & 0 \\
    0 & 0 & 3 & 7 & 0 & z & 0 & 0 \\
    5 & 3 & 0 & 3 & 0 & 0 & 0 & 0 \\
    8 & 7 & 3 & 0 & 1 & 7 & 0 & 0 \\
    y & 0 & 0 & 1 & 0 & 6 & 9 & 6 \\
    0 & z & 0 & 7 & 6 & 0 & x & 2 \\
    0 & 0 & 0 & 0 & 9 & x & 0 & 7 \\
    0 & 0 & 0 & 0 & 6 & 2 & 7 & 0 \\
    \end{array} \right).

  **(A)**
    Draw the graph as a diagram with nodes and edges.
    Replace :math:`x,y,z` with values
    calculated from your Student ID.
    Label the vertices with letters
    :math:`A,B,C,D,E,F,G,H` (they correspond
    to the consecutive rows and columns in the matrix).

    If you wish, you can use the following layout
    (edges are not shown, but the vertice positions allow
    to draw the edges without much intersection).
    But you can use any other layout as well.

    .. image:: figs/mst-vertices.png
       :width: 3in


  **(B)**
    Run Prim's algorithm to find MST using
    :math:`r = A` as the root.
    If you do not have time to redraw the graph many times,
    just show the table with :math:`v.key`
    values after each phase.
    (No need to show :math:`v.p`, as the parents do not change
    and they are easy to find once you have the final rooted tree drawn.)
    The top of the table would look like this (it shows Phase 0 --
    the initial state before any edges have been added).

    =====================  ==============  ==============  ==============  ==============  ==============  ==============  ==============  ==============
    Phase                               A               B               C               D               E               F               G               H
    0 (initial state)           :math:`0`  :math:`\infty`  :math:`\infty`  :math:`\infty`  :math:`\infty`  :math:`\infty`  :math:`\infty`  :math:`\infty`
    =====================  ==============  ==============  ==============  ==============  ==============  ==============  ==============  ==============


  **(C)**
    Summarize the result: Draw the MST obtained as the
    result of Prim's algorithm, find its total weight.




**Question 6:**
  Run Kruskal's algorithm on the same graph as in the Question 4.



  **(A)**
    After each step when there is an edge connecting two sets of vertices,
    write that edge and show the partition where that edge connects two previously disjoined pieces
    in the forest of trees.

    .. note::
      If there are multiple lightest edges that can be used to connect two disjoined pieces, pick edge :math:`(v,w)`
      which lexicographically precedes any other.

  **(B)**
    Redraw the given graph (show the order how you added the edges in parentheses).
    Also compute the total weight of this MST.





Maximum Flow Problem
-----------------------





Ford-Fulkerson algorithm finds 
mazimum flow in a directed graph with edge capacities.
Ford-Fulkerson algorithm does not specify, how to pick augmenting paths.
In some cases they can be picked in a very inefficient way resulting 
in running time that is equal to the numeric integer value of the flow
(and does not depend on the size of the graph). 

So there is a popular variation of it named *Edmonds-Karp algorithm*, 
see `<https://bit.ly/2YMhkkC>`_; it picks the augmenting paths
from the source :math:`s` to the sink :math:`t` using BFS traversal 
(using the residual graph :math:`G_f` for the flow :math:`f` assigned
so far). 
It is an efficient algorithm; it requires :math:`O(n^2 m)` time, 
where :math:`n = |V|` denotes the number of vertices, but :math:`m =|E|`
denotes the number of edges.



Edmonds-Karp Algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a fast version of Ford-Fulkerson; was first proposed
by Yefim Dinitz in 1970 and later independently published
by Edmonds and Karp (1972).


.. figure:: figs/edmonds-karp-graph.png
   :width: 2.5in
   :alt: Graph diagram
   
   Flow graph for the Edmonds-Karp Algorithm


Problem
^^^^^^^^^

**(A)**
  Run Edmonds-Karp algorithm on the graph shown above. 
  For every phase highlight the the augmenting path (or simply list its vertices), 
  find the *residual flow* of this augmenting graph. 
  Draw a copy of the original graph where the residual flow is added.
  Namely, every age is labeled by two numbers ``f/c`` -- the actual flow ``f`` (after adding
  the residual flow obtained in this step) and also the capacity ``c`` of the edge (it never changes).
  
  During the next phase, show the next residual graph, highlight the augmenting path, find the residual flow. 
  And next to that residual graph show a new copy of the original graph with updated flow numbers. 
  Thus, every phase shows two oriented graphs: 
  
  * The current residual graph (initially -- it is simply the given graph with all flows equal to 0). 
  * The original graph with all the flows added.
  
  .. note:: 
    In Edmonds-Karp algorithm visiting the successors of the source vertex :math:`s` in the BFS order
    needs to know the ordering. Assume that all the vertices are arranged in growing order of their indices
    (namely, :math:`v_1` is visited before :math:`v_2` and so on).
  
**(B)**
  Redraw the original graph with all the maximum flows (use the same two-number labels for edges ``f/c``). 
  Show the min-cut which prevents any further augmenting paths (either highlight with 
  another color, or simply list the partition of graph's vertices into two disjoint sets that describe the cut).
  
  


Solution
^^^^^^^^^^

**(A)**

  **Phase 1:**
    Augmenting path: :math:`p = \left\langle s,v_1,v_2,t \right\rangle`, the added flow is 
    :math:`f_p = \min(3,4,2) = 2`. 
  
    .. image:: figs/edmonds-karp-solution-1.png
       :width: 4in
   
  **Phase 2:**
    Augmenting path: :math:`p = \left\langle s,v_3,v_6,t \right\rangle`, the added flow is 
    :math:`f_p = \min(1,2,1) = 1`.
  
    .. image:: figs/edmonds-karp-solution-2.png
       :width: 4in
  
  **Phase 3:**
    Augmenting path: :math:`p = \left\langle s,v_5,v_4,t \right\rangle`, the added flow is 
    :math:`f_p = \min(3,2,3) = 2`.
  
    .. image:: figs/edmonds-karp-solution-3.png
       :width: 4in

  **Phase 4:**
    Finally, the residual graph looks like shown below. There are no further 
    augmenting paths going from :math:`s` to :math:`t` with some positive capacity.

    .. image:: figs/edmonds-karp-solution-4.png
       :width: 2in

  
**(B)**
  The flow obtained during the previous three phases is shown in the picture below. 
  The minimum cut (that is equal to the max flow) is given by two 
  disjoints sets of vertices: 
  
  .. math::
  
    V_1 = \{ s,v_1,v_2,v_3,v_5,v_6 \}\;\;\text{and}\;\;V_2 = \{ v_4, t \}.
  
  The capacity of this min-cut is :math:`w(v_2,t) + w(v_5,v_4) + w(v_6,t) = 2 + 2 + 1 = 5`.
  It is the sum of the weights of edges connecting something in :math:`V_1` with something in :math:`V_2`. 

  .. image:: figs/edmonds-karp-min-cut.png
     :width: 2.5in
	 



**(A)**
  Run Edmonds-Karp algorithm on the graph shown above. 
  Every edge in the picture is labeled with a number showing the *capacity* of that edge.
  
  For every phase highlight the the augmenting path (or simply list its vertices), 
  find the *residual flow* of this augmenting graph. 
  Draw a copy of the original graph where the residual flow is added.
  Namely, every age is labeled by two numbers ``f/c`` -- the actual flow ``f`` (after adding
  the residual flow obtained in this step) and also the capacity ``c`` of the edge (it never changes).
  
  During the next phase, show the next residual graph, highlight the augmenting path, find the residual flow. 
  And next to that residual graph show a new copy of the original graph with updated flow numbers. 
  Thus, every phase shows two oriented graphs: 
  
  * The current residual graph (initially -- it is simply the given graph with all flows equal to 0). 
    It only displays edge capacities and **not** flows (but it may include *reversed edges*).
    In this graph you can search (in BFS order) and highlight the augmenting path.
  * The original graph with all the flows added. In this graph you must also show the flows
    using the notation with two numbers ``f/c``.
  
  .. note:: 
    In Edmonds-Karp algorithm visiting the successors of the source vertex :math:`s` in the BFS order
    needs to know the ordering. Assume that all the vertices are arranged in alphabetical order.
  
**(B)**
  Redraw the original graph with all the maximum flows (use the same two-number labels for edges ``f/c``). 
  Show the min-cut which prevents any further augmenting paths (either highlight with 
  another color, or simply list the partition of graph's vertices into two disjoint sets that describe the cut).
  
  
.. only:: Internal

  **Answer:** 
  
  **(A)**
    Following Edmonds-Karp algorithm, we successfully select augmenting paths 
    starting from the shortest ones (and lexicographically first -- if there are multiple
    paths of the same length). 
    
    Phase 1: Push :math:`11` units of flow over the augmenting path :math:`S \rightarrow A \rightarrow B \rightarrow T` highlighted in orange.
    
    .. image:: figs/ford-fulkerson-phases-1.png
       :width: 4in
    
    Phase 2: Push :math:`1` unit of flow over the augmenting path :math:`S \rightarrow C \rightarrow B \rightarrow T`. 
    
    .. image:: figs/ford-fulkerson-phases-2.png
       :width: 4in
       
    Phase 3: Push :math:`7` units of flow over the augmenting path :math:`S \rightarrow C \rightarrow D \rightarrow T`.     

    .. image:: figs/ford-fulkerson-phases-3.png
       :width: 4in
       
    Phase 4: Push :math:`2` units of flow over the augmenting path :math:`S \rightarrow C \rightarrow B \rightarrow D \rightarrow T`.            

    .. image:: figs/ford-fulkerson-phases-4.png
       :width: 4in

    The last residual graph does not contain any augmenting path from :math:`S` to 
    :math:`T`, so the algorithm stops here.
    Overall, we have pushed :math:`11 + 1 + 7 + 2 = 21` units of flow.

    .. image:: figs/ford-fulkerson-phases-5.png
       :width: 2in
    
    
  **(B)**
    We redraw the flow graph (showing actual flows and capacities for each edge). 
    The minimum cut is shown as red dashed line. 
    It splits vertices into two disjoint groups: :math:`S,A,B,C` and :math:`D,T`; 
    all the edges between them are saturated -- the flow reaches capacity. 
    As we know the capacity of a minimum cut must equal the maximum flow. 
    This maximum flow (equalling the min cut capacity) is :math:`7+2 + 12 = 21`. 

    .. image:: figs/ford-fulkerson-min-cut.png
       :width: 2in

      
  :math:`\square`
