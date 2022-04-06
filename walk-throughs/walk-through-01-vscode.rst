Building C++ in VS Code
==========================

This walk-through is intended as a practical way to create small C++
programs on the Windows platform. 
*Visual Studio Code* (or *VS Code*) is a free text editor, 
it has some syntax highlighting capabilities and integrates with other build tools. 
(Using Gedit in Linux environments or XCode or Atom on Mac OS X would be similar 
starting-level tools; please let us know, if you plan to use non-Windows platforms 
to do most of your coding work.)

Objective
---------

We need to create a few single-file programs in C++, compile and run them. 
We also need to run them on plaintext input files (as standard input or ``STDIN``) 
and we also need to get plaintext output (as standard output or ``STDOUT``). 
At the end of the coding session we want to submit all the files to a GitHub repository. 

Outline of Steps

**Step 1** 
  Set up an IDE on Windows: VS Code and Microsoft C++ compiler.
  
**Step 2**
  Configure the compilation task: Create the ``.vscode\tasks.json`` configuration file.

**Step 3**  
  Write C++ code and build: If necessary, fix compiler and linker issues.
  
**Step 4** 
  Run executables from terminal: Supply input and output interactively from the terminal window.
  
**Step 5** 
  Redirect I/O streams to files: STDIN, STDOUT, STDERR, and
  also display the return value of ``main()``. 
  


Steps in Detail
----------------

Step 1: Set up an IDE on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can follow the guide `Configure VS Code for Microsoft C++ <https://code.visualstudio.com/docs/cpp/config-msvc>`_.

Visual Studio Code should have its C++ plugin enabled and Microsoft Developer Tools should be installed.
Go to some directory (can name it ``ds-workspace`` or similar). 
To create the initial directory structure, you can also check out code
from GitHub classroom's invitation (contact instructor for details). 

Open **Developer Command Prompt for VSC**. Go to the directory ``ds-workspace``. 
Create an empty subdirectory there and open **Visual Studio Code**: 

.. code-block:: text
  
  mkdir hello
  code .
  


Step 2: Configure the Compilation Task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To enable easy compilation of simple one-file projects 
directly from Visual Studio Code, 
you can configure the ``hello\.vscode\tasks.json`` file
with the following content: 

.. code-block:: javascript 

  {
    "version": "2.0.0",
    "tasks": [
      {
        "type": "shell",
        "label": "cl.exe build active file",
        "command": "cl.exe",
        "args": [
          "/Zi",
          "/EHsc",
          "/Fe:",
          "${fileDirname}\\${fileBasenameNoExtension}.exe",
          "${file}"
        ],
        "problemMatcher": ["$msCompile"],
        "group": {
          "kind": "build",
          "isDefault": true
        }
      }
    ]
  }

After this you can compile the file which is currently 
open and active in the Visual Studio Code editor by 
pressing three buttons: **Ctrl**-**Shift**-**B**. 

You can also compile larger projects with this method,
but ``"${file}"`` should be replaced by ``"*.cpp"`` in 
the configuration file like this:


.. code-block:: javascript 

        "args": [
          "/Zi",
          "/EHsc",
          "/Fe:",
          "${fileDirname}\\${fileBasenameNoExtension}.exe",
          "${file}"
        ],

This method is platform-dependent and there 
are more robust ways to compile C++ programs, but 
they will be covered in subsequent walk-throughs17. 


Step 3: Build C++ Code 
^^^^^^^^^^^^^^^^^^^^^^^

Create a minimalistic C++ program. For example, name this file ``hello.cpp``

.. code-block:: cpp

  #include <iostream>
  using namespace std;
  int main() {
    cout << "Print hello" << endl;
  }
  
Save this file in your directory ``hello``. 
Then press three buttons simultaneously: 
**Ctrl**-**Shift**-**B**. 
Select the first compiler (``cl.exe``) from the drop down list
(or just wait until your code compiles.


Run Executables from Terminal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return to the PowerShell **Developer Command Prompt for VSC**. 
Run the newly created executable: 

.. code-block:: cpp

  hello.exe
  
It should print out a greeting (``"Print hello"``). 



Redirect I/O Streams to Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To display return code (the integer value returned by the
function ``main()``) you can use the following in
a Windows terminal: 

.. code-block:: 

  hello.exe > myoutput.txt
  echo Exit Code is %errorlevel%

On Linux a similar code would look like this: 

.. code-block:: 

  echo $?

Here ``%errorcode%`` is a special variable that 
contains the value of the most recent program that ran 
in this terminal. As the name suggests, it is not used to return 
any computation results, just the indication, if the process
exited normally (``0`` means normal or successful, 
any non-zero code is some sort
of failed command).  


Save Your Work to a Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After the coding has been successfully finished, 
it has to be properly saved. All grading 
will rely on code being in a Git repository. 
The suggested of actions is the following: 

1. Create workspace for your code in appropriate directory. 
   This can be done by accepting the invite link for 
   ``ds-workspace`` and cloning the repository. 
   (In other situations you may need to check out 
   an existing project or create a new repository from scratch.)
2. Move your existing code to the new directory. 
3. Reopen Visual Studio Code, run build process and 
   tests again. 
4. Update ``.gitignore`` to ignore dependent files.
5. Add your source files to the repository. 
   Tag your commit and push. 
6. View the repository status in GitHub Webpage.




.. Use grading server
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. 
.. For some labs we can check, if they work 
.. correctly on testfiles (including private ones, which 
.. are not visible to the students before the deadline). 
.. 
.. .. note::
..    We cannot guarantee that the grading server will 
..    be available and work properly whenever you need it
..    (unlike Git repository it is not installed on a 
..    high-availability server).
..    
..    On the other hand, the grading server 
..    can clarify misunderstandings regarding the functionality
..    and shows how close is your code to being done.   
.. 
.. 1. Log into Jenkins. 
.. 2. Select the task to test. 
.. 3. Run tests and view the testing report. 
.. 4. Commit to Git some change that causes testing errors. 
.. 5. Re-test to see that only the tagged code matters for grading.

