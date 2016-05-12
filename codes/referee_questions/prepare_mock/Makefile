CC=gcc
CFLAGS=-Wall -O3
LINKFLAGS=-lm
OBJECTS= conversions.o

make_galaxy: make_galaxy.o $(OBJECTS)
	$(CC) $(LINKFLAGS) $^ -o $@

make_galaxy.o: make_galaxy.c
	$(CC) $(CFLAGS) $^

conversions.o: conversions.c
	$(CC) $(CFLAGS) $^

clean:
	rm -f *.o make_galaxy