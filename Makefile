PROG = ising
CC = g++
CPPFLAGS = -I /usr/local/include/eigen3
OBJS = ising.o

$(PROG): $(OBJS)
	$(CC) -o $(PROG) $(OBJS)

$(OBJS): ising.cpp
	$(CC) $(CPPFLAGS) -c ising.cpp

clean:
	rm -f ising ising.o