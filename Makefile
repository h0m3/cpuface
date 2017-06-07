CC=gcc
CFLAGS=-Wall -O3 -g
PREFIX=/usr

all: python helper

python: cpu_get.py cpu_set.py cpuface.py main.py profiles.py
	python -m compileall -l .

helper: cpuface_helper.c python
	$(CC) -o cpuface_helper cpuface_helper.c $(CFLAGS)

clean:
	rm -f *.o cpuface_helper
	rm -rf __pycache__
	rm -f *.pyc

install:
	install -m 0755 -d $(PREFIX)/share/cpuface
	install -m 0755 -d $(PREFIX)/share/cpuface/__pycache__
	install -m 0755 -d $(PREFIX)/share/applications
	install -m 0755 -d $(PREFIX)/bin
	install -m 0755 __pycache__/* $(PREFIX)/share/cpuface/__pycache__
	install -o root -m 4755 cpuface_helper $(PREFIX)/share/cpuface/cpuface_helper
	install -m 0644 cpuface.ui $(PREFIX)/share/cpuface/cpuface.ui
	install -m 0644 LICENSE.txt $(PREFIX)/share/cpuface/LICENSE.txt
	install -m 0644 cpu_get.py $(PREFIX)/share/cpuface/cpu_get.py
	install -m 0644 cpu_set.py $(PREFIX)/share/cpuface/cpu_set.py
	install -m 0644 cpuface.py $(PREFIX)/share/cpuface/cpuface.py
	install -m 0644 profiles.py $(PREFIX)/share/cpuface/profiles.py
	install -m 0755 main.py $(PREFIX)/share/cpuface/main.py
	install -m 0755 cpuface.desktop $(PREFIX)/share/applications/cpuface.desktop
	ln -s $(PREFIX)/share/cpface/cpuface_helper $(PREFIX)/bin/cpuface_helper
	ln -s $(PREFIX)/share/cpuface/main.py $(PREFIX)/bin/cpuface

.PHONY: install clean
