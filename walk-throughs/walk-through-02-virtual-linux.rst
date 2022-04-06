Walk-Through: System Tests on Virtual Linux
=============================================

Unlike the previous walk-through (preoccupied with development environment on Windows), 
this walk-through shows a simple production environment on a Linux machine. 
The Linux guest as described in this 
walk-through is meant to be similar to the environment where your programming tasks are graded.

Unlike Java and Scala, C++ is not meant to be a platform-independent programming technology; 
it may happen that it compiles and runs on one environment (such as Windows 10 using Microsoft C++ 
compiler), but fails to run in another environment (such as Ubuntu/Debian Linux with 
makefiles and the g++ compiler). 

Run C++ projects in an environment with standardized 
operating system and its environment variables. VirtualBox and 
Xubuntu ensure some predicatability. 
Also the project files should have predictable directory layout; version control (such as GitHub) should 
be used during the submission.
It is your responsibility to ensure that it runs on Linux - since that is the only thing that
matters for the grade for programming assignments.


.. note:: 
  There may be other reasonable ways how to test your code on Linux
  converting your laptop to Linux, using dual-boot,
  or using Windows Subsystem for Linux. 
  They may be more convenient for you, if you are familiar with the technologies involved. 
  Instructors might be unable to assist with the setup. 






Objective
---------

We need to create a minimalistic Debian-style Linux machine to be used for 
building and testing C++ code - using reasonable amount of automation (to integrate
with the code repository and to run all testcases automatically). 

Overview of Steps
^^^^^^^^^^^^^^^^^

**Step 1**
  Install VirtualBox software: Install VirtualBox, create a guest machine slot named {\tt Xubuntu} there.

**Step 2** 
  Set Xubuntu guest: Install Oracle VirtualBox and initialize its guest machine with Xubuntu OS.
  
**Step 3**
  Install Basic Software on Xubuntu: C++ tools and Git.
  
**Step 4**
  Run ``git`` from the command-line: Check out the initial repository. Commit and push your changes to the 
  version control. Tag your commit. 

**Step 5**  
  Build and run C++ code manually: Use Linux command-line (but no Makefile-related tools) to 
  run executables from the command line. 

**Step 6**
  Build with a Makefile: Build and run your code on some testfiles using a ``Makefile``. 
    
**Step 7**
  Transfer files with ``WinSCP``: Use ``WinSCP``, connect to the Linux using ``Putty``.
  
**Step 8**  
  Test out the ``diff`` utility: Compare the test outputs with expected outputs, use the right switches to 
  handle Windows/Linux whitespace reasonably. 






Steps in Detail
----------------

Step 1: Install VirtualBox software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Visit `<https://www.virtualbox.org/>`_ and download the most recent 
   VirtualBox installer. 
   
   a. Click on **Download VirtualBox 6.1** banner. 
   b. Click the link {\bf Windows hosts}, if your physical machine is Windows 10 laptop 
      (or choose other operating system \textendash{} to whatever you have). 
   c. Save the instler, such as ``VirtualBox-6.1.12-139181-Win.exe``.
   
2. Double-click on the VirtualBox installer (elevate privileges
   to Admin-level, if asked to do so), and pick the default values to install it.
3. Run the newlly installed application **Oracle VM VirtualBox**.

   .. image:: figs/virtualbox1.png
      :width: 500 px

4. Click button **New** and enter the name of your new virtual guest, for example, ``xubuntu``.

..   .. image:: figs/virtualbox2.png
..      :width: 300 px

5. Leave the default RAM memory size (1024 MiB). If your laptop is powerful (16 or more GiB of RAM), 
   consider giving more RAM memory, say, 2048 MiB.
6. Leave the default option **Create a virtual hard disk now**; also leave the **VDI (VirtualBox Disk Image)**. 
7. Leave the default option **Dynamically allocated**. 
8. Confirm the location of virtual memory image.

   .. image:: figs/virtualbox7.png
      :width: 300 px





Step 2: Create Xubuntu Guest
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Download the Xubuntu installer (as an ISO file of some stable release). 
   Visit `<https://xubuntu.org/download/>`_) and pick a 64-bit ISO image.
   In our example it is {\bf xubuntu-20.04.1-desktop-amd64.iso}. 
2. Make sure that the guest machine is powered off, 
   select ``xubuntu`` machine and click button **Settings**. 
3. Under **Settings** select **Storage** > **Controller IDE** > **Empty**.

   .. image:: figs/virtualbox9.png
      :width: 3in

4. Click on the browse button (highlighted in red in the above image). Select the
   Xubuntu image that you downloaded earlier.
5. In the VirtualBox application, select the ``xubuntu`` machine
   and click on the button **Run** (the green arrow).
6. Wait about 5 minutes until Xubuntu image loads from the virtual CD-ROM drive.
   Click on the button **Install Xubuntu**.
   
   .. image:: figs/xubuntu3.png
      :width: 3in

7. Leave the default keyboard layout **English (US)** > **English (US)**.
8. Selecting the checkbox **Select third party software...** in the Xubuntu installer
   is optional (it is selected on instructor machines).
9. Leave the default radio button **Erase disk and install Xubuntu**.
10. Select **Riga** as your current location.
11. Enter an Xubuntu Linux machine name (some short name with lower-case English letters such as 
    ``miuse``), your username (e.g. ``student``) and some password (e.g. ``Bitl2!``).
	
    .. image:: figs/xubuntu7.png
       :width: 2.5in
	   
    .. note:: At this point you would need to wait about 15 minutes until VirtualBox finishes installing Xubuntu guest.
	
12. Reboot the machine. Log in as user ``student`` and enter the password.
13. Click on the upper-left corner (the mouse-like Xubuntu start button) and start 
    typing word ``terminal``. Once you see **Terminal Emulator**, right-click it and 
    select **Add to Desktop**. This would make easier to create Linux-like terminal windows
    and run command-lines.
	
    .. image:: figs/xubuntu9.png
       :width: 2.5in



Step 3: Install Basic Software on Xubuntu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


1. Set the root password to ``Bitl2!`` - same as for the user ``student``:

   .. code-block:: bash
   
      sudo passwd 
   
   First, enter ``Bitl2!`` password as student user. Secondly, type ``Bitl2!`` twice to set root's password.

2. Install all the software updates:

   .. code-block:: bash
   
      sudo apt-get update
      sudo apt-get upgrade

.. 3. Install Java JDK (prerequisite for Jenkins). First search all the ``openjdk'' related installations, 
..   then install the package ``openjdk-8-jdk``. Finally, check if your Java has the right version 1.8.
..   
..   .. code-block:: bash
..   
..      sudo apt-get search openjdk
..      sudo apt-get install openjdk-8-jdk
..      java -version

3. Install C++ compiler (named ``g++``) and also ``make`` utility:

   .. code-block:: bash
   
      sudo apt-get install build-essential

4. Install Git client:

   .. code-block:: bash
   
      sudo apt-get install git











