SRCDIR=src
OBJDIR=build
CC=g++
CPPFLAGS=-Wall

$(SRCDIR)/%.o: $(SRCDIR)/%.cpp
	$(CC) $(CPPFLAGS) -c -o $@ $<	

circlist_main: $(SRCDIR)/CircularList.o $(SRCDIR)/CircularListMain.o
	g++ -o circlist_main $(SRCDIR)/CircularList.o $(SRCDIR)/CircularListMain.o
	mkdir -p $(OBJDIR)
	mv circlist_main $(OBJDIR)
    
tests: circlist_main test01.txt test02.txt test03.txt test04.txt test05.txt test06.txt test07.txt
	$(OBJDIR)/circlist_main < test01.txt > test01.out.txt
	$(OBJDIR)/circlist_main < test02.txt > test02.out.txt
	$(OBJDIR)/circlist_main < test03.txt > test03.out.txt
	$(OBJDIR)/circlist_main < test04.txt > test04.out.txt
	$(OBJDIR)/circlist_main < test05.txt > test05.out.txt
	$(OBJDIR)/circlist_main < test06.txt > test06.out.txt
	$(OBJDIR)/circlist_main < test07.txt > test07.out.txt

all: circlist_main
	
clean:
	rm -f $(OBJDIR)/circlist_main
	rm -f $(SRCDIR)/*.o
	rm -f *.out.txt

