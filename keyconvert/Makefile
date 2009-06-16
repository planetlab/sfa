# 'make' should not install - DESTDIR might be wrong at this stage
all: keyconvert

keyconvert: 
	gcc -o keyconvert -lcrypto -ldl keyconvert.c keyconvertmain.c b64decode.c

install: keyconvert
	install -d -m 0755 $(DESTDIR)/usr/share/keyconvert
	install -c -m 0755 keyconvert $(DESTDIR)/usr/share/keyconvert/keyconvert
 
clean:
	rm -rf keyconvert
	rm -rf $(DESTDIR)/usr/share/keyconvert/
