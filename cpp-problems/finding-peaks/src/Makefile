CPPFLAGS = 
SRC_DIR := .
OBJ_DIR := .

all: sample6

sample6: sample6.o
	g++ -o sample6 sample6.o

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	g++ $(CPPFLAGS) -c -o $@ $<

clean:
	rm -f sample6
	rm -f *.o
	rm -f *.out.txt
	
