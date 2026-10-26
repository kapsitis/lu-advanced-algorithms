https://youtu.be/WwMz2fJwUCg?si=3F-QEHx36ij58Rhe
https://youtu.be/fpwsw7SdkyY?si=HzQBi7CBnPhfXA-J


P2.
Simpleksu metodes atkārtojums
Dualitāte
Simpleksu sarežģītība
Elipsoīdu  metode

P3.
Visādas iekšējo punktu metodes

https://www.abacademies.org/articles/an-application-of-linear-programming-in-performance-evaluation-6723.html




Rate-distortion theory
provides a framework for optimally trading off a signal's distortion (a measure of fidelity) 
and the rate (the amount of data) necessary to represent it. 
For lossy compression, especially in multimedia data like images and videos, 
this balance between the rate of information and the distortion in the recovered data is crucial. 

In the context of linear programming, the rate-distortion problem can be formulated as follows:

Objective: Minimize the total distortion + λ * rate

The "total distortion" is a measure of the difference between the original signal 
and the signal after compression and decompression. 
This is typically computed as the sum of squared differences 
(in case of images, for pixels; for audio, signal amplitude etc.), 
but other measures can be used depending on the application. 

The "rate" is the size of the compressed data. This could be measured in bits, 
bytes, or any other unit of digital information.

λ is a parameter that controls the trade-off between the distortion and the rate. 
When λ is large, the optimization will prioritize minimizing the rate 
(getting the smallest possible compressed data size), leading to more distortion. 
When λ is small, the optimization will prioritize minimizing the distortion, 
leading to a larger compressed data size. 

The variables in this objective function could be the different elements 
(e.g., pixels in an image or signal amplitudes in an audio file) in the data to be compressed. 

The linear programming problem could then be built upon this objective function:

minimize: 
    total distortion + λ * rate

Subject to: 
    (1) constraints imposed by the compression algorithm itself
    (2) constraints imposed by the storage or transmission capabilities

Note: Rate distortion theory and its applications in real world problems can 
get quite complex and dive deep into some advanced mathematics. 
Depending on the level of detail you wish to teach, 
some parts might be more applicable than others.





Resource Allocation Problem


#### Dual Problem:
- **Objective:** Minimize the total cost of acquiring resources.
- **Variables:** Let \( y_1, y_2, \ldots, y_m \) represent the shadow prices of each resource.
- **Objective Function:** Minimize \( w = b_1y_1 + b_2y_2 + \ldots + b_my_m \).
- **Constraints:** Ensure that the cost does not exceed the profit coefficient for each product:
  \[
  \begin{align*}
  a_{11}y_1 + a_{21}y_2 + \ldots + a_{m1}y_m &\geq c_1 \\
  a_{12}y_1 + a_{22}y_2 + \ldots + a_{m2}y_m &\geq c_2 \\
  &\vdots \\
  a_{1n}y_1 + a_{2n}y_2 + \ldots + a_{mn}y_m &\geq c_n \\
  y_i &\geq 0 \, (\text{Non-negativity})
  \end{align*}
  \]

**Interpretation:** The dual prices \( y_i \) indicate how much the overall profit would increase if the availability of resource \( i \) were increased by one unit.




Diet problem 

#### Dual Problem:
- **Objective:** Maximize the nutritional utility gained for the budget spent.
- **Variables:** Let \( y_1, y_2, \ldots, y_m \) represent the utility (value) coefficients of each nutrient.
- **Objective Function:** Maximize \( w = d_1y_1 + d_2y_2 + \ldots + d_my_m \).
- **Constraints:** Ensure that the value assigned to the nutrients justifies the cost:
  \[
  \begin{align*}
  a_{11}y_1 + a_{21}y_2 + \ldots + a_{m1}y_m &\leq c_1 \\
  a_{12}y_1 + a_{22}y_2 + \ldots + a_{m2}y_m &\leq c_2 \\
  &\vdots \\
  a_{1n}y_1 + a_{2n}y_2 + \ldots + a_{mn}y_m &\leq c_n \\
  y_i &\geq 0 \, (\text{Non-negativity})
  \end{align*}
  \]

**Interpretation:** The dual variables \( y_i \) represent the marginal value of increasing each nutrient's requirement, providing insights into which nutrients are binding in terms of cost.







### 3. Transportation Problem

#### Primal Problem:
- **Objective:** Minimize the cost of shipping goods from multiple suppliers to multiple consumers.
- **Variables:** Let \( x_{ij} \) represent the amount shipped from supply point \( i \) to demand point \( j \).
- **Objective Function:** Minimize \( z = \sum_{i=1}^m \sum_{j=1}^n c_{ij}x_{ij} \), where \( c_{ij} \) is the cost per unit shipped from \( i \) to \( j \).
- **Constraints:** Satisfy supply and demand constraints:
  \[
  \begin{align*}
  \sum_{j=1}^n x_{ij} &\leq s_i \, (\text{Supply at } i) \\
  \sum_{i=1}^m x_{ij} &\geq d_j \, (\text{Demand at } j) \\
  x_{ij} &\geq 0 \, (\text{Non-negativity})
  \end{align*}
  \]

#### Dual Problem:
- **Objective:** Maximize the total value assigned to supply and demand points under cost constraints.
- **Variables:** Let \( u_i \) and \( v_j \) be the dual variables representing the values of supply and demand points, respectively.
- **Objective Function:** Maximize \( w = \sum_{i=1}^m s_iu_i + \sum_{j=1}^n d_jv_j \).
- **Constraints:** Ensure the sum of the values at supply and demand points does not exceed shipment costs:
  \[
  u_i + v_j \leq c_{ij} \quad \text{for all } i \text{ and } j
  \]

**Interpretation:** The dual variables \( u_i \) and \( v_j \) can be seen as effective prices for the supply and demand locations. They indicate how much cost can be reduced if supply or demand restrictions at a particular node are relaxed.

These tasks and their respective duals illustrate how linear programming can be applied to solve real-world economic and logistical problems while providing meaningful insights through their dual interpretations.