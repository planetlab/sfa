# this scripts tests the key conversion routines
# it converts the _pub files in test/ from openssh to openssl
# it then verifies signatures with openssl (see keytest.sh)

rm -rf testout
mkdir testout

# rsa1 keys
# these are in a different format
#./keyconvert.py test/openssh_rsa1_512.pub testout/openssl_rsa1_512.pem
#./keyconvert.py test/openssh_rsa1_1024.pub testout/openssl_rsa1_1024.pem
#./keyconvert.py test/openssh_rsa1_2048.pub testout/openssl_rsa1_2048.pem

# rsa2 keys
./keyconvert.py test/openssh_rsa_512.pub testout/openssl_rsa_512.pem
./keyconvert.py test/openssh_rsa_1024.pub testout/openssl_rsa_1024.pem
./keyconvert.py test/openssh_rsa_2048.pub testout/openssl_rsa_2048.pem

# dsa keys
./keyconvert.py test/openssh_dsa_512.pub testout/openssl_dsa_512.pem
./keyconvert.py test/openssh_dsa_1024.pub testout/openssl_dsa_1024.pem
./keyconvert.py test/openssh_dsa_2048.pub testout/openssl_dsa_2048.pem

# make a test file to encrypt
echo "this is a test to see if the key conversion routines work" > test.txt

# test the keys
./testkey.sh -sha1 rsa_512
./testkey.sh -sha1 rsa_1024
./testkey.sh -sha1 rsa_2048
./testkey.sh -dss1 dsa_512
./testkey.sh -dss1 dsa_1024
./testkey.sh -dss1 dsa_2048
