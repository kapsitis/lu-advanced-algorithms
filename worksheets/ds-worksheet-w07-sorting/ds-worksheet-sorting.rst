Worksheet, Week 07: Sorting
=============================

QuickSort
-----------


Pseudocode for Quicksort
^^^^^^^^^^^^^^^^^^^^^^^^^^

This variant of Quicksort
uses the leftmost element of the input area as a pivot.
It is the same as
we have in the lecture slides, but may differ from
some other Quicksort flavors (randomized etc.) that you may encouter
in other sources.

.. math::

  \begin{array}{rl}
   & \text{\textsc{Quicksort}}(A[\ell\;\ldots\;r]):\\
  1 & \text{\textbf{if\ }} l<r:\\
  2 & \hspace{.5cm} i = \ell \;\;\;\;\;\;\;\;\; \textcolor{teal}{\text{\em ($i$ increases from the left and searches elements $\geq$ than pivot)}}\\
  3 & \hspace{.5cm} j = r+1	\;\; \textcolor{teal}{\text{\em ($j$ decreases from the right and searches elements $\leq$ than pivot.)}}\\
  4 & \hspace{.5cm} v = A[\ell] \;\;\;\; \textcolor{teal}{\text{\em ($v$ is the pivot.)}}\\
  5 & \hspace{.5cm} \text{\textbf{while\ }} i<j:\\
  6 & \hspace{1.0cm} i = i+1\\
  7 & \hspace{1.0cm} \text{\textbf{while\ }} i<r \text{\textbf{\ and\ }} A[i]<v:\\
  8 & \hspace{1.5cm} i = i+1\\
  9 & \hspace{1.0cm} j = j-1\\
  10 & \hspace{1.0cm} \text{\textbf{while\ }} j>\ell \text{\textbf{\ and\ }} A[j]>v:\\
  11 & \hspace{1.5cm} j = j-1\\
  12 & \hspace{1.0cm} A[i] \leftrightarrow A[j] \;\; \textcolor{teal}{\text{\em (Undo the extra swap at the end)}}\\
  13 & \hspace{0.5cm} A[i] \leftrightarrow A[j] \;\; \textcolor{teal}{\text{\em (Undo the extra swap at the end)}}\\
  14 & \hspace{0.5cm} A[j] \leftrightarrow A[\ell] \;\; \textcolor{teal}{\text{\em (Move pivot to its proper place)}}\\
  15 & \hspace{0.5cm} \text{\textsc{Quicksort}}(A[\ell\;\ldots\;j-1])\\
  16 & \hspace{0.5cm} \text{\textsc{Quicksort}}(A[j+1\;\ldots\;r])\\
  \end{array}



**(A)**
  Run this pseudocode for one invocation :math:`\text{\textsc{QuickSort}}(A[0..11])`,
  where the table to sort is the following:

  .. math::

    13, 0, 23, 1, 8, 9, 29, 16, 8, 24, 6, 11.

  Draw the state of the array every time you swap two
  elements (i.e. execute :math:`A[k_1] \leftrightarrow A[k_2]` for any :math:`k_1,k_2`).

**(B)**
  Continue with the first recursive call of :math:`\text{\textsc{QuickSort}}()`
  (the original call :math:`\text{\textsc{QuickSort}}(A[0..11])` is assumed to be the
  :math:`0^{\text{th}}` call of this function).
  Draw the state of the array every time you swap two elements.


**(C)**
  Decide which is the second recursive call of
  :math:`\text{\textsc{QuickSort}}()` and draw the state
  of the array every time you swap two elements.
  Show the end-result
  after this second recursive call at the very end.


Solution
^^^^^^^^^^

Your answer can be simple lists of numbers (without any grid lines or additional
markings). Just try to keep the lists of numbers aligned.


**(A)**
  Swaps during the :math:`0^{\text{th}}` call:

  .. image:: figs-sorting/arrays-part1.png
     :width: 4in


**(B)**
  Since this example contains two elements equal to :math:`8`,
  we added subscripts to them (to show clearly, where every one is being swapped).
  As integer numbers they are fully identical to the Quicksort algorithm.
  (Still, the Quicksort algorithm does redundant swaps on them.)

  Swaps during the first recursive call.

  .. image:: figs-sorting/arrays-part2.png
     :width: 4in


**(C)**
  Notice that the second recursive call happens within the
  first recursive call (sorting the left side of the left half).

  Swaps during the second recursive call:

  .. image:: figs-sorting/arrays-part3.png
     :width: 4in



Problems
-----------


**Question 1:**
  You are given an array:

  .. math::

    \begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|} \hline
    a+10 & \;\;c\;\; & a+20 & \;\;a\;\; & c+5 & \;\;b\;\; & b+20 & a+15 & b+1 & b+15 & \;2\cdot c\; & b+2 \\ \hline
    \end{array}

  Here :math:`a,b,c` are the last three digits of your Student ID.
  The pseudocode (same as in the sample) is used to sort it. Pivot is the leftmost element.

  **(A)**
    Run the initial call of :math:`\text{\textsc{QuickSort}}(A[0..11])`.
    Draw the state of the array every time you swap two elements.

  **(B)**
    Draw the content of the array immediately *before* the second recursive
    call of :math:`\text{\textsc{QuickSort}}()`.
    (The original call :math:`\text{\textsc{QuickSort}}(A[0..11])` is assumed to be the
    :math:`0^{\text{th}}` call of this function).
