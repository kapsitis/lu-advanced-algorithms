Programming Task 1
============================

When doing the exercises follow the following guidelines: 

  * Clone the GitHub repository
  * Create all your C++ files with lower-case names 
    in the subdirectory ``ds-workspace-YourName/task1``
  * Commit and push your repository to GitHub.
  * Tag this programming task as ``submit-task1``. 


**Introduction:**
  The input for this program is an array :math:`A` of length :math:`2n`. 
  We build two new arrays :math:`B` and :math:`C` (both of length :math:`n`) from the elements of :math:`A`; 
  every element from :math:`A` is used exactly once -- it goes either to the array :math:`B` or to the array :math:`C`.
  We repeat the following step :math:`n` times:

**Step Description:** 
  Among the elements of :math:`A` that are still unused in either :math:`B` or :math:`C`
  find those :math:`A[i]` and :math:`A[j]` which are the "closest". 
  Namely, find two indices for which the absolute value
  :math:`{\displaystyle \left| A[i] - A[j] \right|}` is minimal. If there are multiple
  pairs :math:`i,j` where :math:`A[i],A[j]` are closest, select the pair with the
  smallest :math:`i` (and, if the same :math:`i` participates in multiple closest pairs, then 
  also pick the smallest :math:`j`). 
	
  Once you have the "closest" :math:`A[i]` and :math:`A[j]`,
  insert the smallest one into :math:`B` and the largest one into
  :math:`C` (or append the same number to both arrays, if they 
  were equal). Both :math:`B` and :math:`C` are filled from the left
  to the right.	

  Create a C++ program that reads an an array :math:`A` of even length
  (All its :math:`2n` elements are space separated positive integers. 
  It terminates with a single :math:`0`.)
  Output arrays :math:`B` and :math:`C` as two lines of
  integers.
  
**Constraints:** 

  * :math:`n \leq 100000`,
  * :math:`1 \leq A[i] \leq 10^9` for all :math:`i \in \{ 0,\ldots,2n-1\}`.
	
**Sample Input:**
  
  .. code-block:: text
	
    3 10 5 5 8 12 0	  
	  
**Sample Output:**

  .. code-block:: text
    
    5 8 3 
    5 10 12 

**Explanation:** 
    
  * During the first step we remove :math:`A[2]=5` and :math:`A[3]=5`. 
  * During the second step we remove :math:`A[1]=10` and :math:`A[4]=8`. 
  * During the third step we remove :math:`A[0]=3` and :math:`A[5]=12`.
	
