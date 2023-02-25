# Fitting Permutation

Two arrays $A$ and $B$ contain $n$ positive integers
each. Let $t$ be positive integer -- named the *threshold*. 
Arrays $A$ and $B$ are in a relation: $(A,B) \in R$ if there exists
a permutation $B'$ of the array $B$ (a way to reorder elements 
of $B$) such that $A[i] + B'[i] \geq t$ for all $i = 0,\ldots,n-1$.

Write a C++ program that reads lines from the standard input and determines, 
if for a given threshold $t$ and two arrays $A,B$, the 
pair $(A,B)$ is in relation $R$.

Lines come in groups of three: The first line in 
each group contains a threshold number $t$, 
followed by a list of $n$ space-separated positive integers 
(representing array $A$) and
then another $n$ space-separated positive integers (representing array $B$). 
After that there is another group of three lines (possibly, with different values of $t$ and 
array length $n$) and so on. Input is finished when there is a line containing just the digit ``0``.

**Constraints:** 

* At most $1000$ subproblems (groups of three lines).,
* $1 \leq n \leq 1000$,
* $1 \leq t \leq 10^9$,
* $1 \leq A[i], B[i] \leq 10^9$.

**Sample Input**

``` text  
11
5 6 3 8 9
8 2 6 5 6
23
12 14 12 7
10 11 9 20
0
```

**Sample Output:**

```
true
false
```
	
**Explanation**  
 
The first two arrays $A = \{ 5,6,3,8,9 \}$ and $B = \{ 8,2,6,5,6 \}$
are in the relation for threshold $t = 11$. 
For example, we can rearrange elements of the second array $B' = \{ 6,5,8,6,2 \}$. 
In this case $A[i] + B'[i] = \{ 11,11,11,14,11 \}$.

The second two arrays $A = \{ 12, 14, 12, 7 \}$ and $B = \{ 10, 11, 9, 20 \}$
are not in the relation for threshold $t = 23$. 
There are three numbers in $A$: $(12,12,7)$ that would need to be added with numbers at least
$11$ to add up to :math:`23`. On the other hand, there are just two 
numbers $\geq 11$ in $B$.
	
**Note:** Algorithmic tasks of this kind are widely known. 
See `HackerRank: Permuting Two Arrays [https://bit.ly/3tk8dlY>](https://bit.ly/3tk8dlY). 
  
  
 
