Programming Task 2
============================

Place your files in the directory ``ds-workspace-YourName/task2``, push it to your GitHub repository.

**Implementation Details**

You can use any STL data structures for this task. 
Strict time and space limits are introduced for this task:

* Memory limit: 4 MB.
* Time limit: 0.5 seconds.




Description
-------------

**Requirements on the Data Structure**


In a large city (up to one billion inhabitants) 
there is exactly one hair studio with up to :math:`9` hairdressers, each one 
is identified by a unique number from :math:`\{1,2,3,4,5,6,7,8,9\}`).
The hair studio measures time in discrete units (time can take integer values from :math:`t=1` to 
:math:`t=10^9`). Time counting starts at the studio opening moment.
Even though the number of customers is huge, and the demand for hairdressers is high, 
every hairdresser should take mandatory breaks. The time of a mandatory break 
is when the hundreds digit in the time counter coincides with the hairdresser’s number.
For example, the hairdresser with the number :math:`5` must take a break in the time intervals 
:math:`[500,599]`, :math:`[1500,1599]`, :math:`[2500,2599]`, and so on. 
During a break, hairdresser is forbidden to serve a client. 
In addition, customer appointment cannot be interrupted, a customer can only be served 
by one hairdresser without any breaks. 
Consequently, a hairdresser cannot start to serve a client, 
if the service cannot be finished before the break starts.
The necessary service time for each customer is known in advance.

**Discrete Time Counting:** 
A customer should be served without delay if there is an unoccupied hairdresser and s/he 
does not have any limitations (required breaks, etc.). Upon finishing work with the current client, 
a hairdresser should immediately try to start serving the next one. More precisely: Let a client :math:`C_1` show up at 
the time moment :math:`T_1` and his appointment needs time (service duration) :math:`D_1`. 
Let a hairdresser :math:`H_1` be serving this customer. 
Then the appointment will take place during time interval :math:`[T_1, T_1+D_1-1]`. 
The appointment is finished at the time moment :math:`t=T_1+D_1-1`. If another customer :math:`C_2` has already shown up 
before or exactly at the time :math:`T_1+D_1`, then the hairdresser :math:`H_1` can start working with customer 
:math:`C_2` at the time moment :math:`T_1+D_1`.

**Customer Queueing:**
Customers wait in a regular queue; they must be assigned hairdressers on the first come first served basis. 
In particular, it is not allowed to "optimize" customer allocation to hairdressers -- 
if a customer :math:`C_i` arrived before :math:`C_j`, but :math:`C_i` cannot be served by any available hairdresser
because of the mandatory breaks, :math:`C_j` cannot be served either (even if :math:`C_j` has smaller service duration
and would fit before the break).

**Resolving Contentions:** 
At any time moment, no more than one customer can show up. 
Administrator immediately assigns a number in queue :math:`\{1, \ldots, 200000 \}` and an 
appointment duration (an integer number in :math:`[1,900]`).
If there is an unserved customer and there are multiple hairdressers currently available, then 
the hairdresser is assigned according to these rules:

1. The hairdresser that has spent more time without a customer 
   (counting from the end of the last appointment) has the priority.
2. If two hairdressers have spent the same time without a client, 
   the hairdresser with a smaller number has the priority. 

**The Desirable Outcome:**   
Knowing the times, when customers show up, their numbers in the queue, the durations of the 
appointments, our task is to print the appointment end time for each customer, the number of serving hairdresser 
and the customer’s number in the queue. 
The records should be in ascending order by the appointment finishing time. 
If two client appointments were finished at the same time, results should be ordered by the hairdresser number.



**Input representation:** 
  The first line has the integer number that is the number of hairdressers. 
  Then follows the information about the customers in the order of showing up (Ascending Time values).
  
  .. code-block:: text

    <Hairdressers>
    <Time> <Customer> <Duration>
    ...
    0


  * ``<Hairdressers>`` denotes the number of hairdressers (it is a number from :math:`[1,9]`). 
  * ``<Time>`` denotes the moment in time, when customer has shown up for an appointment, 
    it is an integer in :math:`[1,10^9]`.
  * ``<Customer>`` denotes the customer number in the queue, it is in :math:`[1,200000]`. 
  * ``<Duration>`` denotes the necessary length of the appointment, it is in :math:`[1,900]`.
	
  0 means the end of input data. In this case, Customer and Duration fields are not provided

  Input data is in ascending chronological order by Time.
  The input file is correct regarding the input data format and the given conditions.



**Output representation:** 
  According to the input file, each of the customer appointment end time is written in the following format:

  .. code-block:: text
  
    <Time> <Hairdresser> <Customer>
	
  * ``<Time>`` denotes the moment in time, which is the last customer appointment moment :math:`[1,10^9]`.
  * ``<Hairdresser>`` denotes the hairdresser that served the customer, i.e. the hairdresser number in :math:`[1,9]`.
  * ``<Customer>`` denotes the customer that had the appointment –- his/hernumber in the queue :math:`[1,200000]`.
  
  In the result, none of the appointment end time will not be greater than :math:`10^9`.




Input Data Samples
--------------------


**Sample input** ``task2.in``:

.. code-block:: text
  
  2
  11 1 10
  21 2 50
  31 3 20
  0



**Expected output** ``task2.out``:
  
.. code-block:: text
  
  20 1 1
  50 1 3
  70 2 2

  


