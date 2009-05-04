keyconvert:
	gcc -o keyconvert -lcrypto -ldl keyconvert.c keyconvertmain.c b64decode.c
	install -cD -m 0755 keyconvert /usr/share/keyconvert/keyconvert

clean:
	rm -rf keyconvert
	rm -rf /usr/share/keyconvert/
