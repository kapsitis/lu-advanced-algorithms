Design Tasks
============================

This document describes the activity named *Design and Solution Description* 
from the Course Syllabus (it is worth 20% of the overall max grade). 
Some of the principles (good design, testability of the code, 
the use of object orientation) also apply to your other programming tasks, 
but for this exercise we will try to ensure that you receive some 
feedback about the design and the structure of your code 
(can discuss with others and improve it, if something is not optimal). 


**Why the need for a "Design and Solution Description"?**
  Sometimes programming tasks are submitted just in hope that they 
  will pass sufficiently many testcases and earn a good grade. 
  Still, the actual software
  creation can be more interesting and challenging than that.  
  The suggested tasks (Variants 1--10) do not require 
  very long or complex solutions, but they could encourage
  algorithmic thinking and informed choice between alternatives.

The *Technical Design* document should help the upcoming implementation, 
it should be well structured and easy to read.
Assume that you are preparing to implement this task for widespread use 
(such as a public software library), it should be well-designed, 
error-free as far as possible and also easy to understand and to 
implement by fellow programmers.


"Technical Design" Checklist
--------------------------------

Make sure to address all the points in the following checklist. 
  
**Assumptions on Input and Output:**
  Problem descriptions may leave some technical details open to interpretation. 
  Write down explicitly, which inputs your code will accept, what
  invalid arguments will you handle and what error messages will you output. 
  You do not need to process badly malformed inputs (such as binary files where
  plaintext input is expected), but your algorithm should be able to handle common mistakes 
  such as numbers outside the allowed range or missing data items.

**Underlying algorithms:**
  Write down the algorithm as a pseudocode or in a human language. 
  Analyze the algorithm regarding its asymptotic time complexity. Algorithm analysis can also 
  include space complexity, probabilistic parts in the code whenever appropriate.
  
**Object Oriented Design:**
  Which C++ classes (or, perhaps, Rust classes or traits) 
  will you use - and which part is responsible for what. 
  Write UML diagrams showing the functions -- both public and private, 
  and also class dependencies.

**Files in solution:** 
  List the compilation units (the ``*.cpp`` or ``*.rs`` files in case of Rust) and also the headers (``*.h`` files).

**Testing approach:**
  Explain your testing approach, for each functional or non-functional behavior of your solution. 
  Tests could be unit-test, system-test or performance test level. 

**Build Procedures:**
  Describe the procedures to build and to test your code.
  Prefer the simplest approach that could possibly work. For example
  a short ``Makefile`` to compile your code and run the tests. 
  Or a short Linux bash script ``build.sh``. 


Appendix: Suggest Extensions and Twists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes software developers need to evaluate their tasks critically -- 
as the existing formalizations and algorithms are not always formulated in the 
most relevant and most interesting way.

As an appendix to your "Technical Design" document add some analysis on the problem itself -- how 
could it be modified in order to create a more general and more powerful algorithm? an easier algorithm? 
apply probabilistic or amortized analysis? change the asymptotic time complexity of your algorithm? 

.. note::
  This "extension and twist" section is meant for a critical understanding of the existing problem and 
  give freedom to our imagination. Hence, all the analysis in this appendix are at conceptual (pseudocode
  and analysis) level. 
  You are **not** responsible for solving such "extended" or "twisted" algorithmic tasks; you 
  cannot replace the original task with the one modified by you.

    

Guidelines for Implementation
-------------------------------

Unlike the four programming tasks, this task is graded along with a
discussion with an instructor in an online Zoom session.
Please pay attention to the following: 
  
**Encapsulation:**
  Do not expose implementation details; if some method is not called from the outside, 
  declare it ``private``, if some parameter, class method or variable can be immutable, declare it ``const``.
 
**Separation of Concerns:**
  Single-responsibility means that each functionality except for a minimalistic ``main()`` is contained in some 
  class; each class is responsible for a single aspect of the program's functionality. 
  *A class should have only one reason to change* (R.E.Martin).
 
**Refactor to eliminate repetition:** 
  Refactoring code means improving the readability and the design of your code without 
  changing its behavior. One of the reasons to refactor is the DRY principle (*do not repeat yourself*). 
  Apply all the other modifications to make programs easier to read
  and more modular without sacrificing effectiveness.
  
**Testability:**
  Another criterion of a good design is that you can test every aspect of your algorithm separately; 
  you can easily add new testcases at different levels.

Submit your code along with the testcases to GitHub. 




Variant 1: Piles of Submitted Essays
-----------------------------------------

.. https://www.lio.lv/temp/Novads2022_Uzdevumi_vec.pdf


**Introduction:**


**Description:** 

There are :math:`N` students who have registered for a class; they are enumerated
with integers from :math:`1` to :math:`N` (inclusive). 
The instructor wants to find how many students have not submitted any essays. 
For each essay the submitted works are arranged in piles -- each pile 
containes one or more essays where the student numbers are consecutive 
integers (without any omissions). Piles of essays have been stapled together. 

Profesora lekcijām ir reģistrējušies N studenti, kurus profesors savos pierakstos ir
sanumurējis ar naturāliem skaitļiem no 1 līdz N pēc kārtas. Pēc ilgāka pārtraukuma profesors ir
nolēmis izlabot vairākus studentu kontroldarbus un noskaidrot, vai ir tādi studenti, kuri nav
uzrakstījuši nevienu kontroldarbu. Ir zināms, ka profesors katrā kontroldarbā studentu darbus
ir sakārtojis kaudzītēs augošā secībā pēc numuriem bez izlaidumiem un, ja kaudzītē ir vairāk par
vienu darbu, tad saspraudis to ar klipsi. Ja kontroldarbu rakstījušo studentu numuri nav pēc
kārtas, tad viena kontroldarba darbi būs sagrupēti vairākās kaudzītēs. Kaudzītē var būt arī tikai
viens darbs. Diemžēl laika gaitā kaudzīšu secība ir sajukusi, tāpēc profesors uzreiz nevar pateikt,
kuram kontroldarbam konkrētā kaudzīte pieder. Ir zināms, ka katru kontroldarbu ir rakstījis
vismaz viens students.
Uzrakstiet programmu, kas nosaka to studentu skaitu, kas nav uzrakstījuši nevienu
kontroldarbu!



**Constraints:** 

  * Inequalitities... 
	
**Sample Input:**
  
  .. code-block:: text
	
    3 10 5 5 8 12 0	  
	  
**Sample Output:**

  .. code-block:: text
    
    5 8 3 
    5 10 12 

**Explanation:** 
    
  * Show why the output is correct.
	










Input Data
^^^^^^^^^^^

On the first line of the input file there are two integers separated by a single space: 

* :math:`N` (the number of students); 
* :math:`M` (the number of piles of submitted works). 

On the next :math:`M` input lines there are the 

Katrā no nākamajām M
ievaddatu rindām dots vienas darbu kaudzītes apraksts – divi naturāli skaitļi xi un yi
(1 ≤ xi ≤ yi ≤ N), kas atdalīti ar tukšumzīmi. Šis apraksts nozīmē, ka kaudzītē atrodas viena
kontroldarba visu to studentu darbi, kuru numuri ir lielāki vai vienādi ar xi un mazāki vai vienādi
ar yi.
Izvaddati
Izvaddatu vienīgajā rindā jāizvada vesels nenegatīvs skaitlis – nevienu kontroldarbu
nerakstījušo studentu skaits.




Variant 2: Primes
-----------------------





Variant 3: Pizza Hut
----------------------



Variant 4: Combination Lock
-------------------------------


http://lio.e-spiets.lv/arhivs/2018_1_uzd.pdf




Variant 5: Rectangular Arrays
-------------------------------

http://lio.e-spiets.lv/arhivs/2018_2_uzd_vec.pdf



Variant 6: Rectangular Arrays
-------------------------------

http://lio.e-spiets.lv/arhivs/2018_2_uzd_vec.pdf






Variant 7: The First Non-Substring in Shortlex Order
-------------------------------------------------------

.. http://lio.e-spiets.lv/arhivs/2018_2_uzd_vec.pdf





Variant 8: Numeric Pyramid
-----------------------------------------------

We build a numeric pyramid - first choose
three integers :math:`n`, :math:`a`, and :math:`b` 
(they may be equal or different; positive, negative or zero). 
Number :math:`n` stands at the top of the pyramid (Line 0). 
Under it there are two numbers :math:`n+a` and
:math:`n+b` (Line 1). 

After that the pyramid is being built in the following way: 
For every number on the current line :math:`s_i` 
create two children: :math:`s_i+a` and :math:`s_i+b`. 
There are :math:`2^i` numbers on Line :math:`i` 
(where :math:`i = 0,\ldots,2^i - 1`). 

After creating the children on Line :math:`i+1`, leave the
nodes 



Tālāk procesu turpina veidojot otro rindu.
Vispirms katram pirmās rindas skaitlim 𝑡 𝑗 zem tā pa
kreisi uzraksta skaitli 𝑡 𝑗 + 𝑏 un pa labi - skaitli 𝑡 𝑗 + 𝑐.
Pēc tam, neiesaistot pirmo un pēdējo no rindā
uzrakstītajiem skaitļiem, skaitļus rindā secīgi sadala
pa pāriem un katrā pārī skaitļus samaina vietām - t.i.,
otro skaitli samaina ar trešo, ceturto - ar piekto, utt.
Pēc tam tāpat veido nākamās rindas. Skaitļu tornis, kuram n=5, a=-2, b=1 parādīts 23. zīmējumā.
Uzrakstiet programmu, kas nosaka, kāds skaitlis atrodas noteiktā torņa vietā!






