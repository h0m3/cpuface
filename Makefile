CC=gcc
CFLAGS=-Wall -O3

helper: cpuface_helper.c
	$(CC) -o cpuface_helper cpuface_helper.c $(CFLAGS)

clean:
	rm -f *.o cpuface_helper
