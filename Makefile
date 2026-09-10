# Makefile for KTP (KGP Transport Protocol)
# CS39006: Networks Laboratory | IIT Kharagpur

CC = gcc
CFLAGS = -Wall -Wextra -O2
AR = ar
ARFLAGS = rcs
LDFLAGS = -L. -lksocket -lpthread

# Targets
LIB = libksocket.a
DAEMON = ktp_main
USERS = user1 user2

all: $(LIB) $(DAEMON) $(USERS)

# Static Library Target
$(LIB): ktp.o ktp_util.o queue.o
	$(AR) $(ARFLAGS) $@ $^

ktp.o: ktp.c ktp.h queue.h
	$(CC) $(CFLAGS) -c ktp.c

ktp_util.o: ktp_util.c ktp_util.h ktp.h queue.h
	$(CC) $(CFLAGS) -c ktp_util.c

queue.o: queue.c queue.h
	$(CC) $(CFLAGS) -c queue.c

# Daemon Executable
$(DAEMON): ktp_main.c $(LIB)
	$(CC) $(CFLAGS) ktp_main.c $(LDFLAGS) -o $@

# User Applications
user1: user1.c $(LIB)
	$(CC) $(CFLAGS) user1.c $(LDFLAGS) -o $@

user2: user2.c $(LIB)
	$(CC) $(CFLAGS) user2.c $(LDFLAGS) -o $@

# Convenience aliases
library: $(LIB)
daemon: $(DAEMON)
users: $(USERS)

# Clean Build Artifacts
clean:
	rm -f *.o $(LIB) $(DAEMON) $(USERS)

.PHONY: all clean library daemon users
