# Editing Linked Lists

There is a list of $n$ integer numbers $a_i$, $i=0,\ldots,n-1$ 
implemented as a linked list of ``Node`` objects. 
``Node`` has the following type: 
  
``` text
struct Node { int info; Node* next; }; 
```

Each number in the list is stored in the ``info`` attribute.
Assume that the first node is pointed to by variable ``Node* listHead``. 
Implement a procedure with the following prototype: 

```
void changeList(Node* listHead);
```

It swaps the fist element of the list with the last one. Then it 
deletes all nodes with ``info`` field equal to ``0``. 

**Note:** In order to use the linked list for processing the elements, you 
should avoid storing intermediate results in arrays (as well as vectors or similar data structures).
Just a few extra variables taking a constant amount of memory should be enough.
Also, the more appropriate way to rearrange a linked list is
to redraw the pointers (rather to modify ``info`` fields of ``Node``
objects).


**Constraints:** 

* $n < 10000$,
* $0 \leq a_i \leq 10^9$, where $i=0,\ldots,n-1$.

**Sample Input:**

``` text
9
1 2 0 3 0 0 4 0 5
```

**Sample Output:**

``` text
5 2 3 4 1
```
	
**Explanation:** The first line of the input contains the number of integers to read ($n=9$ in this case).
After exchanging the first and the last elements, we get the list $\{5,2,0,3,0,0,4,0,1\}$.
After removing all zeroes we get the final list $\{5,2,3,4,1\}$.
  
If the input list starts or ends with a zero, these are removed as well. 
For example $\{1,0,2,3,0\}$
would at first become $\{0,0,2,3,1\}$, and then $\{2,3,1\}$.



