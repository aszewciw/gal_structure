CC=icc
CFLAGS=-I. -Wall -xHost -O3 -vec_report2

# Linker Flags and Libraries
LDFLAGS=
LDLIBS=

# Name of final Executable
TARGET=separate_gal

# inc files and object files
SOURCES := $(wildcard *.c)
INCLUDES := $(wildcard *.h)
OBJECTS := $(SOURCES:%.c=%.o)

# Notes: $@ refers to the file name of the target of the rule
#        $< refers to the name of the first prerequisite
$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) $(LDLIBS) $(OBJECTS) -o $@

# This is a poor way to do this, actually, because an object
# file depends on all header files. I suppose we don't expect
# the headers to change very often. It would be cleaner to build
# a list of header files that each source file depends on, especially
# since this will be a relatively small project.
%.o: %.c $(INCLUDES)
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean cleanall

clean:
	rm -f $(TARGET)

cleanall: clean
	rm -f $(OBJECTS)