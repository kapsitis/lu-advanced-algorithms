CC=g++
CFLAGS=-std=c++17
PROGRAM = matrix-max
INPUT_FILES = $(wildcard test*.txt)
OUTPUT_FILES = $(patsubst test%.txt,output.test%.txt,$(INPUT_FILES))
	
all: matrix-max
	
matrix-max: matrix-max.cpp
	$(CC) $(CFLAGS) -o matrix-max matrix-max.cpp

.PHONY: test
test: $(OUTPUT_FILES)

output.test%.txt: $(PROGRAM) test%.txt
	./$(PROGRAM) < $< > $@ || echo "failure"

verify:
	diff -wB output.test01.txt expected01.txt || true
	diff -wB output.test02.txt expected02.txt || true
	diff -wB output.test03.txt expected03.txt || true
	diff -wB output.test04.txt expected04.txt || true
	diff -wB output.test05.txt expected05.txt || true

.PHONY: clean
clean:
	rm -f matrix-max
	rm -f $(OUTPUT_FILES)


