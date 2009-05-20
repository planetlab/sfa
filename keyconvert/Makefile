
all: install

keyconvert: 
	gcc -o keyconvert -lcrypto -ldl keyconvert.c keyconvertmain.c b64decode.c

install: keyconvert
	install -cD -m 0755 keyconvert $(DESTDIR)/usr/share/keyconvert/keyconvert
 
clean:
	rm -rf keyconvert
	rm -rf $(DESTDIR)/usr/share/keyconvert/
