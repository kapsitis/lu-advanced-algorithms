#!/bin/bash

rm ../../../ds-workspace/lab1-1/Makefile
rm ../../../ds-workspace/lab1-1/test*.txt
rm ../../../ds-workspace/lab1-1/expected*.txt
rm ../../../ds-workspace/lab1-2/Makefile
rm ../../../ds-workspace/lab1-2/test*.txt
rm ../../../ds-workspace/lab1-2/expected*.txt

declare -a tsts=("01" "02" "03" "04" "05")
for i in "${tsts[@]}"
do
  cp lab1-1/test1.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/expected1.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/test2.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/expected2.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/test3.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/expected3.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/test4.${i}.txt ../../../ds-workspace/lab1-1/  
  cp lab1-1/expected4.${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-1/test5.${i}.txt ../../../ds-workspace/lab1-1/  
  cp lab1-1/expected5${i}.txt ../../../ds-workspace/lab1-1/
  cp lab1-2/test6.${i}.txt ../../../ds-workspace/lab1-2/
  cp lab1-2/expected6.${i}.txt ../../../ds-workspace/lab1-2/
done

cp lab1-1/Makefile ../../../ds-workspace/lab1-1/
cp lab1-2/Makefile ../../../ds-workspace/lab1-2/

