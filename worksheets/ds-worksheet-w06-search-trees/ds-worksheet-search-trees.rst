Worksheet, Week 06: Search Trees
=================================


Trees and Binary Trees
------------------------



**Introduction:**
  How to Encode General Tree to a Binary Tree

  Sometimes non-binary (ordered) trees should be represented in
  binary-tree data structures. See `<https://bit.ly/3khnC0p>`_ for details.
  The two rules to encode are these:


  * Every node :math:`v` in the general tree with
    its *first child* :math:`w` maps to the same node :math:`v` in the binary tree,
    where the corresponding :math:`w` is its *left child*.
  * Every node :math:`v` in the general tree having :math:`w` as its *sibling to the right*
    has the same :math:`w` in the binary tree as its *right child*.


  One can also decode: given a binary tree (if its root only has the left child),
  it is possible to restore the original general tree.

  Consider an example general tree on Figure :ref:`general-tree-no-color`.

  .. _general-tree-no-color:
  .. figure:: figs-search-trees/general-tree-no-color.png
     :width: 2in

     Multiway Tree


  **Encoding Step 1**
    Redraw edges (only connect each node with its first child and also to
    the sibling to the right). To see clearly which edges will be left-going, and
    which are right-going, can color them differently. See
    Figure :ref:`colored-binary-tree1-reordered`.


  .. _colored-binary-tree1-reordered:
  .. figure:: figs-search-trees/colored-binary-tree1-reordered.png
     :width: 2in

     Tree with Horizontal Edges



  **Encoding Step 2**
    Adjust the levels in the new binary tree so that it takes
    a more conventional look (left children to the left, right children to the right).
    See Figure :ref:`colored-binary-tree1`.


  .. _colored-binary-tree1:
  .. figure:: figs-search-trees/colored-binary-tree1.png
     :width: 1.5in

     Encoded Binary Tree



**Question 6.1.1 (Decode Binary to a Multiway Tree):**

  **(A)**
    List all the nodes in Figure :ref:`binary-tree-problem`
    using the in-order tree traversal.

  **(B)**
    Binary tree :math:`B` shown in :ref:`binary-tree-problem` has
    been obtained by encoding some general (multiway) tree :math:`T` (The
    tree :math:`T` is rooted
    and ordered, but it is not necessarily binary.)
    Restore the general tree :math:`T` by decoding the given binary tree.


  .. _binary-tree-problem:
  .. figure:: figs-search-trees/binary-tree-problem.png
     :width: 1.5in

     Binary tree for Question 6.1.1






**Question 6.1.2 (Binary Trees):**

  Define a new integer number :math:`N \in \{0,1,2,\ldots,9 \}` from the digits of your Student ID:

  .. math::

    N \;=\; (a + b) \;\text{mod}\; 10.


  **(A)**
    Redraw the binary tree in Figure;
    replace letters :math:`a,b` with your values. We denote this tree by :math:`B`.

  **(B)**
    List all the nodes of :math:`B` in their in-order DFS traversal order.

  **(C)**
    Draw a general tree (denoted by :math:`G`) that is obtained
    by decoding the tree :math:`B`.
    See `Encoding general trees as binary trees <https://en.wikipedia.org/wiki/Binary_tree#Encoding_general_trees_as_binary_trees>`_
    or `<https://bit.ly/3kdyg8n>`_.

  **(D)**
    What is the depth of the node with number :math:`N` (defined above) in the new tree :math:`G`?


  .. figure:: figs-search-trees/heptagonal-nodes.png
     :width: 3in
     :alt: Binary tree

     Binary tree :math:`B` for inorder traversal and converting to a general tree :math:`G`





BST Trees
-----------


**Definition:**
  A tree is named *Binary Search Tree* (BST) if the nodes satisfy the *order invariant*:
  Let :math:`x` be a node in a binary search tree. If :math:`y` is a node in the left subtree
  of :math:`x`, then :math:`y.key \leq x.key`. If :math:`z` is a node in the right subtree of :math:`x`, then
  :math:`z.key \geq z.key`.



**Question 6.2.1 (Recurrences to count BSTs):**
  Let :math:`B_n` denote how many different BSTs for :math:`n` different keys there exist (all the trees should have correct order invariant).
  We have :math:`B_1 = 1` (one node only makes one tree). And :math:`B_2 = 2` (in the case of two


**Question 6.2.2 (Search Random Keys in BST):**
  Consider the binary tree shown below.

  .. image:: figs-search-trees/bst-search.png
     :width: 2in

  Every key in this tree is being searched with the same probability.
  Find the expected number of pointers that are followed as we search for a random key in this tree.
  (For example, searching the key at the root means following :math:`1` pointer, searching the key that is a child
  of the root means following :math:`2` pointers and so on.)







Prefix Codes and Huffman Algorithm
------------------------------------

Let :math:`C` be the collection of letters to be encoded; each letter
has its frequency :math:`c.freq` (frequencies are numbers describing the probability
of each letter).


| :math:`\text{\sc Huffman}(C)`:
| :math:`\;\;\;\;` :math:`n = |C|`
| :math:`\;\;\;\;` :math:`Q = \text{\sc PriorityQueue}(C)` :math:`\;\;\;\;` (*Minimum heap by "c.freq"*)
| :math:`\;\;\;\;` **for** :math:`i = 1` to :math:`n - 1` :math:`\;\;\;\;` (*Repeat n-1 times*)
| :math:`\;\;\;\;\;\;\;\;` :math:`z = \text{\sc Node}()`
| :math:`\;\;\;\;\;\;\;\;` :math:`z.left = x = \text{\sc ExtractMin(Q)}`
| :math:`\;\;\;\;\;\;\;\;` :math:`z.right = y = \text{\sc ExtractMin(Q)}`
| :math:`\;\;\;\;\;\;\;\;` :math:`z.freq = x.freq + y.freq`
| :math:`\;\;\;\;\;\;\;\;` :math:`\text{\sc Insert}(Q,z)`
| :math:`\;\;\;\;` **return** :math:`\text{\sc ExtractMin(Q)}`  :math:`\;\;\;\;` (*Return the root of the tree*)


**Question 6.3.1 (Decrypt/Encrypt Prefix Code):**
  Consider the following Prefix Tree to encode letters in alphabet
  :math:`\mathcal{A} = \{ S, I, E, N, T, A \}`.

  .. image:: figs-search-trees/prefix-tree.png
     :width: 2in

  Every letter is encoded as a sequence of 0s and 1s (the path from the root to the respective letter).

  **(A)**
    Decode the following sequences:

    * ``11100110100``
    * ``0001100101111``

  **(B)**
    Explain, if there are sequences of bits that are *ambiguous* (can be decoded in more than one way).

  **(C)**
    Explain, if there are sequences of bits that are *impossible* (do not represent any word in the alphabet :math:`\mathcal{A}`).







**Question 6.3.2 (Huffman Code):**
  Let the alphabet be :math:`\mathcal{A} = \{ A, B, C, D, E, F \}` and
  their probabilities are shown in the table.

  ====  ====  ====  ====  ====  ====
  A     B     C     D     E     F
  27%   9%    11%   15%   30%   8%
  ====  ====  ====  ====  ====  ====



**Question 6.3.3 (Entropy and average code length):**

  **(A)**
    For the alphabet (and letter frequencies)
    taken from the previous question compute the Shannon entropy:

    .. math::

      H(\mathcal{A}) = \sum\limits_{c \in \mathcal{A}} (- \log_2 P(c)) \cdot P(c),

    where :math:`P(c)` denotes the probability of the character :math:`c` in the alphabet.

  **(B)**
    Also compute the expected number of bits needed to encode one random letter
    by the Huffman code you created in the previous question.  (Assume that letters arrive with
    the probabilities shown in the table.)


  Theory (not in the scope of our course) tells that nobody can encode the alphabet
  :math:`\mathcal{A}` better than the Shannon's entropy.
  On the other hand, Huffman code is an optimal prefix code; the expected number of bits spent
  per one letter does not exceed :math:`H(\mathcal{A}) + 1`.





Inserting and Deleting from BSTs
---------------------------------


**Question 6.4.1 (Insert new nodes):**
  Generate a random sequence of :math:`10` different
  integer numbers and build a BST tree out of these numbers.
  What is the average depth of a node in this tree?


**Question 6.4.2 (Delete nodes from BST):**
  From the tree build in the previous question delete the following:

  * Any leaf
  * Any inner node with just one child (at best, pick an innder node that has another inner node as a child)
  * Any inner node with two children.



Inserting and Deleting from an AVL Tree
-----------------------------------------


**Question 6.5.1 (AVL tree with min nodes):**
  Let :math:`T_n` be an AVL tree of height :math:`n` with the
  smallest possible number of nodes. For example :math:`|T_0| = 1`
  (just one node is an AVL tree of height :math:`0`); :math:`|T_1| = 2`
  (a root with one child only is an AVL tree of height :math:`1`) and so on.

  **(A)**
    Draw AVL trees :math:`T_2`, :math:`T_3`, :math:`T_4` and :math:`T_5`.

  **(B)**
    Write a recurrence to find the number of nodes :math:`|T_n|`
    (recurrent formula expresses the number :math:`|T_n|` using
    the previous numbers :math:`|T_k|` with :math:`k < n`).


**Question 6.5.1 (AVL and Rotations):**
  Let :math:`T` be some (unknown) BST tree that also satisfied the AVL balancing requirement.
  After :math:`k` nodes were inserted (without any re-balancing actions) the tree :math:`T'` now looks as
  in the image below.

  .. image:: figs-search-trees/tree-for-rotations.png
     :width: 3in


  **(A)**
    Find the smallest value of :math:`k` -- the nodes that were inserted into the original :math:`T`
    to get :math:`T'`.

  **(B)**
    Show the tree after :math:`\text{\sc LeftRotate}(T',x)` -- the left rotation around the node :math:`x`.
    Is the resulting tree an AVL tree now?




(2,4) and Red-Black Trees
----------------------------

**Definition:**
  A tree is named a *Red-Black Tree*, if it is a Binary Search Tree,
  every node is either red or black (extra boolean flag stores this color) and
  it satisfies these *red-black invariants*:

  Root property
    The root is black.

  External property
    Every leaf (a node with NULL key) is also black.

  Internal property
    If a node is red, then both its children are black.

  Depth property
    For each node, all simple paths from the node to descendant leaves contain the
    same number of black nodes.


  .. note::
    See Figure :ref:`red-black-tree`; leaves with NIL keys have
    black-height equal to :math:`0`. As we move to the root, we increment
    the black-height :math:`h_\text{black}` whenever the path crosses some black node.
    The Depth property guarantees that each internal node gets the same black-height, no matter
    which path from a leaf to a root we choose.



**Question 6.6.1 (Insert Nodes in a Red-Black Tree):**

  .. _red-black-tree:
  .. figure:: figs-search-trees/red-black-tree.png
     :width: 5in

     Sample Red-Black Tree


  **(A)**
    Compute the following three key values (:math:`u`, :math:`v`, and :math:`w`):

    .. math::

      \left\{ \begin{array}{l}
      u = 3(a+b)+2\\
      v = 3(b+c)+1\\
      w = 3(c+a)\\
      \end{array} \right.

    Here :math:`a,b,c` are the last :math:`3` digits of your Student ID.

    Verify the "black height" of every node in the graph -- all NULL leaves have black height equal to zero.
    Any other node has black height equal to the number of black nodes that are on some descendant path.
    (According to the depth property -- the black height of any node should not depend on the path to the leaf
    we chose.)


  **(B)**
    Show how the tree looks after the nodes :math:`u`, :math:`v` and :math:`w` (in this order)
    are inserted in the Red-Black Tree shown in Figure :ref:`red-black-tree`.

    If any of the values :math:`u,v,w` coincide with existing nodes, they
    should not be inserted. (Red-Black trees and BSTs in general can handle duplicates; but here
    we assume that it stores a map/set with unique keys.)

    Show the intermediate steps -- the tree after each successive inserted node.
    Clearly show, which are the red/black vertices in the submitted answers.


  .. note::

    Check that your inserts preserve the BST order invariant (along with all the Red-Black
    tree invariants). Secondly, try to follow the standard algorithm when inserting new nodes
    (still, preserving the invariants is more important).
