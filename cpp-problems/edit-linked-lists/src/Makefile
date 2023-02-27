CC=g++
CFLAGS=-std=c++17 -g
PROGRAM = edit-linked-lists
INPUT_FILES = $(wildcard test*.txt)
OUTPUT_FILES = $(patsubst test%.txt,output.test%.txt,$(INPUT_FILES))
	
all: edit-linked-lists
	
edit-linked-lists: edit-linked-lists.cpp
	$(CC) $(CFLAGS) -o edit-linked-lists edit-linked-lists.cpp

.PHONY: test
test: $(OUTPUT_FILES)

output.test%.txt: $(PROGRAM) test%.txt
	./$(PROGRAM) < $< > $@ 


.PHONY: clean
clean:
	rm -f edit-linked-lists
	rm -f $(OUTPUT_FILES)


