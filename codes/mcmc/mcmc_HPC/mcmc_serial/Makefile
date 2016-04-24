CC=gcc
CFLAGS=-Wall -O3
LINKFLAGS= -lgsl -lgslcblas

mcmc: mcmc.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f mcmc