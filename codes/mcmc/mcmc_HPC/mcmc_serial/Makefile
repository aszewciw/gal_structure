CC=gcc
CFLAGS=-Wall -03
LINKFLAGS= -lgsl -lgslcblas

mcmc: mcmc.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f mcmc