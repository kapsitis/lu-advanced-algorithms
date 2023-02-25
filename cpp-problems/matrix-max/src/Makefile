CPPFLAGS = 
SRC_DIR := .
OBJ_DIR := .

all: matrix-max

matrix-max: matrix-max.o
	g++ -o sample1 sample1.o

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	g++ $(CPPFLAGS) -c -o $@ $<

clean:
	rm -f matrix-max
	rm -f matrix-max.o
	rm -f matrix-max.out.txt

