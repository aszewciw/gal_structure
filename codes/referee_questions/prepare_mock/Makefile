CC=gcc
CFLAGS=-Wall -O3
LINKFLAGS=

make_galaxy: make_galaxy.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f make_galaxy