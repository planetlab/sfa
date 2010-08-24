# do not execute this script directly; it is run by test.sh

rm -rf signature.bin
openssl dgst $1 -sign test/openssh_$2 test.txt > signature.bin
openssl dgst $1 -signature signature.bin -verify testout/openssl_$2.pem test.txt
rm -rf signature.bin
