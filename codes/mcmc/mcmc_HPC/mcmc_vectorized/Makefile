CC=icc
CFLAGS=-Iicc -Wall
LINKFLAGS= -lgsl -lgslcblas

mcmc: mcmc.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f mcmc