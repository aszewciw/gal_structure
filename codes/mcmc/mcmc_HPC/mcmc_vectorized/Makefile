CC=icc
CFLAGS=-Iicc -Wall -xHost -O3 -vec_report2
LINKFLAGS= -lgsl -lgslcblas

mcmc: mcmc.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f mcmc