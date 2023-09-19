Please convert Reveal.js Markup into ReStructured Text. 
(1) Preserve all inline LaTeX formulas, add `:math:` prefix.
(2) For display-style math formulas `$$x$$` - drop `$$`, add `.. math::`. 
(3) Slide titles `# ...` or `## ....` become bold text. 
(4) Links are converted to `Link text <LinkURL>`_
(5) Images `![Alt text](path to PNG)` become `.. figure::` markup. 
(6) Drop tags `<hgroup>`.
(7) Convert `<blue>` or `<emblue>` into italic. 
(8) HTML-style tables converted into RST tables.

Input example: 
```md
## <lo-theory/> Kā pamatot Krafta-Makmilana teorēmu?

**Pierādījums:**  
Vispārīgiem "uniquely decodable codes" pierādīt piņķerīgi.

<emblue>Prefiksu kodiem</emblue> (*prefix-free codes*) ievērojam, ka ikviens
$k_i$-bitu kods aizpilda prefiksu kokā (sauktā arī par "kodu telpu") 
tieši `$\frac{1}{2^{k_i}}$` daļu no tilpuma.
[Kenterberijas korpuss](http://corpus.canterbury.ac.nz/)

$$\sum\limits_{s \in S} 2^{-\ell(s)}$$

![Prefiksu koks](prefix-tree.png)<!-- .element: width="400px" -->
```

converts to 
```rst
**Kā pamatot Krafta-Makmilana teorēmu?**

**Pierādījums:**  
  Vispārīgiem "uniquely decodable codes" pierādīt piņķerīgi.

  *Prefiksu kodiem* (*prefix-free codes*) ievērojam, ka ikviens
  :math:`k_i`-bitu kods aizpilda prefiksu kokā (sauktā arī par "kodu telpu") 
  tieši :math:`\frac{1}{2^{k_i}}` daļu no tilpuma.
  `Kenterberijas korpuss <http://corpus.canterbury.ac.nz/>`_

  .. math:: 

    \sum\limits_{s \in S} 2^{-\ell(s)}

.. figure:: figs/prefix-tree.png
   :width: 4in

   Prefiksu koks
```


Here is the text to convert: 







**LZ78 (biti par bitiem)**

Cits LZ78 variants (sāk ar tukšu vārdnīcu).

:math:`\mathtt{AABABBBABAABABBBABBABB}` (22 biti)  
:math:`\mathtt{A.AB.ABB.B.ABA.ABAB.BB.ABBA.BB}`

1. :math:`\mathtt{A}`
2. :math:`\mathtt{AB}`
3. :math:`\mathtt{ABB}`
4. :math:`\mathtt{B}`
5. :math:`\mathtt{ABA}`
6. :math:`\mathtt{ABAB}`
7. :math:`\mathtt{BB}`
8. :math:`\mathtt{ABBA}`
9. :math:`\mathtt{BB}`

:math:`\varnothing\mathtt{A}`

10. :math:`\mathtt{1A}`
11. :math:`\mathtt{2B}`
12. :math:`\varnothing\mathtt{B}`
13. :math:`\mathtt{2A}`
14. :math:`\mathtt{5B}`
15. :math:`\mathtt{4B}`
16. :math:`\mathtt{3A}`
17. :math:`\mathtt{7}`

LZ78 kods:  
:math:`\textcolor{blue}{\mathtt{01110100101001011100101100111}}` (29 biti)  
(Sākot no elementa :math:`2^k+1` 
viņa vārdnīcas adresi kodē ar :math:`k+1` bitiem.)
