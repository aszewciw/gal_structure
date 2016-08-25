CC=gcc
CFLAGS= -Wall -O3 -c -fopenmp -I/usr/local/gsl/latest/opteron/intel/nonet/include
LINKFLAGS= -L/usr/local/gsl/latest/opteron/gcc/nonet/lib -lgsl -lgslcblas -lm -fopenmp
#CFLAGS= -Wall -O3 -c -fopenmp
#LINKFLAGS= -lgsl -lgslcblas -lm -fopenmp
OBJECTS= io.o functions.o model.o correlation.o mcmc.o


all: gal_mcmc test_correlation test_chi2

gal_mcmc: main.o $(OBJECTS) 
	$(CC) $(LINKFLAGS) $^ -o $@

test_correlation: test_correlation.o $(OBJECTS)
	$(CC) $(LINKFLAGS) $^ -o $@

test_chi2: test_chi2.o $(OBJECTS)
	$(CC) $(LINKFLAGS) $^ -o $@

main.o: main.c
	$(CC) $(CFLAGS) $^

test_correlation.o: test_correlation.c
	$(CC) $(CFLAGS) $^

test_chi2.o: test_chi2.c
	$(CC) $(CFLAGS) $^

io.o: io.c
	$(CC) $(CFLAGS) $^

model.o: model.c
	$(CC) $(CFLAGS) $^

functions.o: functions.c
	$(CC) $(CFLAGS) $^

correlation.o: correlation.c
	$(CC) $(CFLAGS) $^

mcmc.o: mcmc.c
	$(CC) $(CFLAGS) $^


clean:
	rm -f *.o gal_mcmc test_correlation test_chi2


