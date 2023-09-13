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



