## Editing of Char Arrays

Make a C++ program that reads lines into char arrays from standard input 
(until there is an empty line -- two newline symbols in a row). 
Each line is processed and whenever there is a character ``arg[i]``
equal to some capital letter (A-Z) 
immediately preceeded by another capital letter ``arg[i-1]``
and ``arg[i-1]`` is **not** alphabetically before ``arg[i]``, 
then ``arg[i]`` is removed. 
The algorithm leaves all lower-case
letters, digits and special characters unchanged. 
(*The deletion is reapplied while there are any not-in-order 
capital letters next to each other --- the following letter is always removed. 
Ultimately, all the the sequences of 
capital letters are in strictly increasing alphabetical order.*)

The algorithm should process the C-strings (arrays of type ``char*`` and 
edit its argument in place without creating another array). 
The algorithm of deleting characters should have the following prototype:
  
``` cpp  
void eraseChars(char* arg); 
```

**Constraints:** 

* Number of non-empty lines up to :math:`1000`.
* Length of lines in the file up to :math:`1000`.
	
**Sample Input:**

``` text
ABCA-IHGxDEFD
321.ABB.AAB.BAA.ZZYWA.123
```
	  
**Sample Output:**

```
ABC-IxDEF
321.AB.AB.B.Z.123
```

**Explanation:** 

Lower-case letters (such as `x`), digits or punctuation does not change, 
but contiguous capitalized fragments such as 
`ABCA`, `IHG`, `DEFD`, `ABB`, `AAB`, `BAA`
are being filtered: All characters that do not follow alphabetically 
the earlier ones, are eliminated.

