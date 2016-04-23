CC=mpicc
CFLAGS=-cc=icc -Wall -xHost -O3 -vec_report2
LINKFLAGS= -limf -lgsl -lgslcblas

mcmc: mcmc.c
	$(CC) $(LINKFLAGS) -o $@ $< $(CFLAGS)

clean:
	rm -f mcmc