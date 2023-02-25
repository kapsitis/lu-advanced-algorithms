# Finding Closest Pairs

There is an array $A$ of length $2n$. 
We build two new arrays $B$ and $C$ (both of length $n$) from the elements of $A$.
We repeat the following step $n$ times:

**Step Description:** 
  Among the elements of $A$ that are still unused in either $B$ or $C$
  find those $A[i]$ and $A[j]$ which are the "closest". 
  Namely, find two indices for which the absolute value
  ${\displaystyle \left| A[i] - A[j] \right|}$ is minimal. If there are multiple
  pairs $i,j$ where $A[i],A[j]$ are closest, select the pair with the
  smallest $i$ (and, if the same $i$ participates in multiple closest pairs, then 
  also pick the smallest $j$). 
	
  Once you have the "closest" $A[i]$ and $A[j]$,
  insert the smallest one into $B$ and the largest one into
  $C$ (or append the same number to both arrays, if they 
  were equal). Both $B$ and $C$ are filled from the left
  to the right.	

  Create a C++ program that reads an an array $A$ of even length
  (All its $2n$ elements are space separated positive integers. 
  It terminates with a single $0$.)
  Output arrays $B$ and $C$ as two lines of
  integers.
  
**Constraints:** 

  * $n \leq 1000$,
  * $1 \leq A[i] \leq 10^9$ for all $i \in \{ 0,\ldots,2n-1\}$.
	
**Sample Input:**
  
  .. code-block:: text
	
    3 10 5 5 8 12 0	  
	  
**Sample Output:**

  .. code-block:: text
    
    5 8 3 
    5 10 12 

**Explanation:** 
    
  * During the first step we remove $A[2]=5$ and $A[3]=5$. 
  * During the second step we remove $A[1]=10$ and $A[4]=8$. 
  * During the third step we remove $A[0]=3$ and $A[5]=12$.
	