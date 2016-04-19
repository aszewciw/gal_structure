CC=gcc
CFLAGS=-Wall
LINKFLAGS= -lgsl -lgslcblas

io_test: io_test.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f io_test