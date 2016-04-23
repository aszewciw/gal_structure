CC=gcc
CFLAGS=-Wall -O3 -ftree-vectorizer-verbose=2
LINKFLAGS= -lgsl -lgslcblas

mcmc: mcmc.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f mcmc