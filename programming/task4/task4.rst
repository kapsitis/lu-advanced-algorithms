Programming Task 4
========================

Place your files in the directory ``ds-workspace-YourName/task4``, push it to your GitHub repository.
Implement all data structures and algorithms on your own; do not use STL, Boost or similar
predefined data structures. 
The only "include" directives in your code would be "iostream", "fstream", "sstream", "string", "iomanip" 
and similar I/O libraries to ensure reading and writing formatted text to files. 

Many files may overlap with your \"task3\", but you would need to have \"task4\" as an 
independent software branch (so you can copy all the necessary files over, once your \"task3\" 
is completed). 




Description
-------------

The task is to implement the Dijkstra’s algoritm on a "network" of plane points. 
In this case there are no limitations about latitude and longitude to be angles
(any pair of two real numbers is a coordinate for a node in your algorithm). 



Implementation Details
-----------------------

Please follow the following guidelines to make your code readable and reusable: 

* Create a C++ class (or struct or similar) named ``Node`` which stores three attributes -- the string label, 
  the latitude and the longitude of a node. 
* Create a C++ class (or struct or similar) named ``NodeDistance`` which stores the node 
  along with its current distance (will serve as a key in the priority queue). 
* Create a C++ class (or struct or similar) named ``MinPriorityQueue`` which 
  is a heap-based priority queue that can store ``NodeDistance`` using the current distance number 
  as its key. 
* Use three functions ``dist(Node n1, Node n2, string metric)`` (a member function in your class ``Node`` or similar) 
  which returns the distance between the two nodes in the given metric (L2, L1, Lmax). 
* All your computations can use "double" type
  (your answers can differ from the official ones by a reasonable rounding error -- the length 
  of the path found multiplied by :math:`10^{-5}`. 



**Input representation:** 
  Each node is represented as a label followed by its coordinates. 
  
  .. code-block:: text

    <SourceLabel> <DestinationLabel> <Metric> 
    <NumberOfNodes> 
    <Label1> <X1> <Y1>
    ...
    <LabelN> <XN> <YN>
    <Label1> <AdjacentLabel1> <AdjacentLabel2> ...  <AdjacentLabelK1>
    <Label2> <AdjacentLabel1> <AdjacentLabel2> ...  <AdjacentLabelK2>
    ... 
    <LabelN> <AdjacentLabel1> <AdjacentLabel2> ...  <AdjacentLabelKN>
    
    
  * ``<SourceLabel>, <DestinationLabel>`` labels for the source and destination nodes. 
    All labels are nonempty strings up to :math:`30` characters long. They can use 
    all uppercase and lowercase letters and the underscore character. (No need to check this condition, 
    You can assume that bad characters will not be used in the labels.)
  * ``<Metric>`` is one of the following: 
  
    * ``L2`` - it is the regular Euclidean metric: :math:`d((x_1,y_1), (x_2, y_2)) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}`. 
    * ``L1`` - it is the square-city metric (how far to go, if you can go only horizontally or vertically): 
      :math:`d((x_1,y_1), (x_2, y_2)) = |x_1 - x_2| + |y_1 - y_2|`. 
    * ``Lmax`` - it is the maximum metric: 
      :math:`d((x_1,y_1), (x_2, y_2)) = \max(|x_1 - x_2|, |y_1 - y_2|)`. 

  * ``<NumberOfNodes>`` does not exceed :math:`10000`. 
  * ``<Xi>`` is a double number (precision up to :math:`10^{-5}`). 
  * ``<Yi>`` is a double number (precision up to :math:`10^{-5}`). 
  * ``<Label1> <AdjacentLabel1> <AdjacentLabel2> ...`` -- this shows the adjacent nodes to the 
    given node. Your graph is undirected; each edge appears in two adacency lists 
    (one for each endpoint). 
  

  **Sample input** ``task3.in``:

  .. code-block:: text
   
    A D L2
    5
    A 0.00000 0.00000
    B 1.00000 0.00000
    C 0.00000 1.00000
    D 1.00000 1.00000
    E 5.00000 1.00000
    A B C
    B A D
    C A D
    D B C E
    E D




**Output representation (three options):** 
  The output should be shown to the browser screen: 
  
  * Off-line approach (produce a static HTML page ``task4.out.html``). 
    It shows the distance and the path that was found. (It is similar to the previous task; 
    here you do not care about how many priority queue operations you did.)
    
    .. code-block:: text
  
      2.00000
      A B D
    
  * A text-based live integration with C++ code (showing WebAssembly integration with your C++ code producing 
    text (similar to the above). But in this case the input data can be copy-pasted into an HTML text-area. 
  * A vector-graphic live integration with C++ code (showing the points on an embedded SVG object
    or a HTML5 canvas), where the shortest path between the source and the destination is highlighted.   
    


  


