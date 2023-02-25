#!/bin/bash
#must have sudo rights

#echo "Pulling from git..."
#echo "-----------------------------"
#git clone git@github.com:jekabssolo/workspace-cpp.git
#cd workspace-cpp
#git checkout ex03-alice
echo "Change directory"
cd lab1-1
echo
echo "Compiling..."
echo "-----------------------------"
#make clean
#make all
 "/c/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe" sample1.cpp

echo "-----------------------------"
echo "Compiled!"
exit 0

echo
echo
echo
echo "Starting tests..."
echo
echo
echo "-----------------------------"
echo "Starting test No. 1"
time ./ex03alice < tests/test01in.txt > tests/test01out.txt
echo
diff -s -B tests/test01out.txt tests/test01expected.txt
echo "-----------------------------"
echo
echo "-----------------------------"
echo "Starting test No. 2"
time ./ex03alice < tests/test02in.txt > tests/test02out.txt
echo
diff -s -B tests/test02out.txt tests/test02expected.txt
echo "-----------------------------"
echo
echo "-----------------------------"
echo "Starting test No. 3"
time ./ex03alice < tests/test003in.txt > tests/test03out.txt
echo
diff -s -B tests/test03out.txt tests/test03expected.txt
echo "-----------------------------"
echo
echo "-----------------------------"
echo "Starting test No. 4"
time ./ex03alice < tests/test04in.txt > tests/test04out.txt
echo
diff -s -B tests/test04out.txt tests/test04expected.txt
echo "-----------------------------"
echo
echo "Cleaning up..."
rm ./ex03alice & rm ./Node.o & rm ./AliceMain.o
rm ./tests/test01out.txt ./tests/test02out.txt ./tests/test03out.txt ./tests/test04out.txt
cd ../../
sudo rm -r workspace-cpp
echo
echo "Done!"
