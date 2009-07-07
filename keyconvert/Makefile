# 'make' should not install - DESTDIR might be wrong at this stage
all: keyconvert

keyconvert: 
	gcc -o keyconvert -lcrypto -ldl keyconvert.c keyconvertmain.c b64decode.c

install: keyconvert
	install -d -m 0755 $(DESTDIR)/usr/bin
	install -c -m 0755 keyconvert $(DESTDIR)/usr/bin/keyconvert

clean:
	rm -rf keyconvert
	rm -f $(DESTDIR)/usr/bin/keyconvert
