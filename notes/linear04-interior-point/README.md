
Sākumtuvinājuma izvēle
------------------------

Aprakstām mākslīgu mainīgo pievienošanas dažādus gadījumus. 

**Gadījums Nr.1:** 
  Dots LP uzdevums šādā formā:

  .. math::

    A\mathbf{x} \textcolor{red}{\leq} \mathbf{b},\;\;\mathbf{x} \geq 0,\;\; \mathbf{b} \geq 0.

  Var pievinināt *nokares mainīgos* (*slack variables*), 
  kas nosaka sākumstāvokli: visi vektora :math:`\mathbf{x}` mainīgie ir 0, 
  bet visi nokares mainīgie :math:`\mathbf{y}` vienādi ar attiecīgajām 
  vērtībām :math:`\mathbf{b}`.


**Gadījums Nr.2:** 
  Dots LP uzdevums, kur nevienādības vietā ir vienādība:

  .. math::

    A\mathbf{x} \textcolor{red}{\leq} \mathbf{b},\;\;\mathbf{x} \geq 0,\;\; \mathbf{b} \geq 0,

  tad pirmo tuvinājumu vispirms ir jāatrod.
  Viens no veidiem - sākt risināt nedaudz izmainītu uzdevumu.

  .. figure:: figs/adding-artificial-variables.png
     :width: 5in

     Adding Artificial Variables

  Katram mākslīgajam mainīgajam piekārtojam ļoti negatīvu :math:`c_i`, 
  lai noteikti nebūtu izdevīgi tam piešķirt nekādu pozitīvu vērtību.


**Gadījums Nr.2:** 
  Sākotnēji visi mākslīgie mainīgie ir "pamata mainīgie" (ja izmaksu 
  vektora vērtības :math:`c_i` zem tiem var pataisīt par 0, izmantojot 
  Gausa izslēgšanas metodi). Pēc tam simpleksa algoritms tos citu 
  pēc cita padara par brīvajiem mainīgajiem.

  1. Ja visi mākslīgie mainīgie kļūst brīvi, tad tiem atbilstošās kolonnas 
     var turpmāk ignorēt (aprēķini šajās kolonnās vairs neiespaidos LP atrisinājumu), 
     jo neviens no tiem nebūs pozitīvs.
  2. Ja mākslīgie mainīgie saglabājas pie pamatmainīgajiem un tos izslēgt 
     gājienu skaitā, kas sakristu ar šo mainīgo skaitu, neizdodas, tad nosacījumi ir 
     pretrunīgi.






Log Barrier Method and how to prepare or it? 
https://people.csail.mit.edu/moitra/docs/6854lec16.pdf


### 1. **Gradient Descent**

- **Relevance**: Gradient descent is a fundamental optimization technique similar to the iterative improvement process in the barrier method. Understanding how gradient descent works, particularly in unconstrained optimization, can help students grasp the iterative nature of the barrier method.
- **Focus**: Discuss concepts such as the gradient, level sets, step size, and convergence criteria.

### 2. **Newton's Method**

- **Relevance**: The barrier method often incorporates Newton's method for iteratively solving unconstrained problems derived from the barrier transformation. The quadratic convergence of Newton's method is a critical benefit.
- **Focus**: Explain how Newton's method uses second-order derivatives to find solutions to equations, emphasizing its quadratic convergence properties.

### 3. **Constrained Optimization via Lagrange Multipliers**

- **Relevance**: Although the barrier method uses a different approach, understanding Lagrange multipliers introduces students to handling constraints in optimization problems. The underlying concept of adjusting for constraints can be enlightening.
- **Focus**: Cover the theory and practice of setting up and solving optimization problems using Lagrange multipliers, comparing this to the concept of a barrier in managing constraints.
