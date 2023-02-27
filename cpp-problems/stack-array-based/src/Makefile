CC=g++
CFLAGS=-std=c++17 -g
SRCDIR=.
OBJDIR=.
SRC=$(wildcard $(SCRCDIR)/*.cpp)
OBJ1=$(OBJDIR)/Stack.o $(OBJDIR)/StackMain.o
OBJ2=$(OBJDIR)/Stack.o $(OBJDIR)/TestStack.o
EXECMAIN=$(SRCDIR)/stack-main
EXECTEST=$(SRCDIR)/stack-test
	
all: $(EXECMAIN)
test: $(EXECTEST)
	
$(EXECMAIN): $(OBJ1)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.cpp
	$(CC) $(CFLAGS) -c -o $@ $<

$(EXECTEST): $(OBJ2)
	$(CC) $(CFLAGS) -o $@ $^


.PHONY: clean
clean:
	rm -f $(SRCDIR)/*.o $(EXEC1) $(EXEC2)
