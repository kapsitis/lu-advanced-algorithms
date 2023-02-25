#!/bin/bash

#echo "Pull the submitted files from GitHub"
#Better do this command manually in the place you want - authentication is easier.
#git clone git@github.com:username/ds-workspace-username.git

# There are five CPP files in lab1-1: sample1.cpp, ... sample5.cpp (plus sample6.cpp in another directory).
declare -a programs=( "1" "2" "3" "4" "5" )

# Each CPP file has five testcases (tests with their expected results)
declare -a tsts=( "01" "02" "03" "04" "05" )

# These are the source files we expect to see:
declare -a infiles=( "lab1-1/sample1.cpp" "lab1-1/sample2.cpp" "lab1-1/sample3.cpp" "lab1-1/sample4.cpp" "lab1-1/sample5.cpp" "lab1-2/sample6.cpp" )

echo "Checking for missing source files..." 
# Boolean flag, if there were any missing *.cpp files
missingFiles=0
for i in "${infiles[@]}"
do 
  if [ ! -f ${i} ]; then
    echo "ERROR: File ${i} does not exist" 
    missingFiles=1
  fi
done
if [[ "$missingFiles" -eq "0" ]]; then
  echo "Check finished. No missing files"
else 
  echo "Check finished. Please copy the missing files in their locations."
  echo "The grading script may lead to unpredictable results, if required files are missing."
fi 


#######################################################
## Run tests in lab1-1 directory.                    ##
#######################################################

# Remove GRADES file (will append to it later on)
rm -f GRADES.txt

cd lab1-1
make clean

for tt in "${programs[@]}" 
do 
  echo "-----------------------------"
  echo "******** sample${tt}.cpp ********"
  echo "-----------------------------"
  echo "Compiling..."
  make "sample${tt}"
  # If executable exists:
  if [ -f "sample${tt}" ]
  then
    for i in "${tsts[@]}"
    do
      echo "----- test${tt}.${i}.txt -----"
      # Run the test, record output in file testN.MM.out.txt (Run for 10 seconds)
      timeout 10 ./sample${tt} < test${tt}.${i}.txt > test${tt}.${i}.out.txt
      if [ $? == "0" ]
      then      
        # Add one extra newline at the end of the file (just in case if it is missing)
        echo >> test${tt}.${i}.out.txt
        # Ignore case (-i), ignore extra whitespace (-w), ignore blank lines (-B).
        diff -i -w -B test${tt}.${i}.out.txt expected${tt}.${i}.txt
        # If the diff command found that two files are the same
        if [ $? == "0" ]
        then
          echo "Test${tt}.${i}: PASS" >> ../GRADES.txt
        else
          echo "Test${tt}.${i}: FAIL" >> ../GRADES.txt
        fi
      else
        echo "Test${tt}.${i}: TIMEOUT" >> ../GRADES.txt
      fi        
    done
  else 
    # Executable (sample1, sample2, etc.) was not created by "make" command
    echo "sample${tt}.cpp did not build"
    for i in "${tsts[@]}"
    do
      echo "Test${tt}.${i}: ERROR" >> ../GRADES.txt
    done
  fi
  echo "------------------------"
  echo 
done


#######################################################
## Run tests in another directory: just sample6.cpp. ##
#######################################################
cd ../
cd lab1-2
make clean


echo "-----------------------------"
echo "******** sample6.cpp ********"
echo "-----------------------------"
echo "Compiling..."
make sample6
if [ -f sample6 ]
then
  for i in "${tsts[@]}"
  do
    echo "----- test6.${i}.txt -----"
    ./sample6 < test6.${i}.txt > test6.${i}.out.txt
    grep -i "$(head -1 test6.${i}.out.txt)" expected6.${i}.txt    
    if [ $? == "0" ]
    then
      echo "Test6.${i}: PASS" >> ../GRADES.txt
    else
      echo "Test6.${i}: FAIL" >> ../GRADES.txt
    fi
  done
else 
  # Executable was not created by "make" command
  echo "sample6.cpp did not build"
  for i in "${tsts[@]}"
  do
    echo "Test6.${i}: ERROR" >> ../GRADES.txt
  done    
fi
echo "------------------------"
echo 





echo "Cleaning up..."
#sudo rm -fr ds-workspace-username/
echo
echo "Done!"
