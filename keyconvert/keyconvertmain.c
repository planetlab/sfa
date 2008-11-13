#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "keyconvert.h"
#include "b64decode.h"

int main(int argc, char **argv)
{
    FILE *fin, *fout;
    char inbytes[16384], *inptr;
    char decodedKey[16384];
    int len;

    b64decodeinit();

    if (argc != 3) {
        fprintf(stderr, "syntax: keyconvert <infile> <outfile>\n");
        exit(1);
    }

    fin = fopen(argv[1], "rt");
    if (fin == NULL) {
        fprintf(stderr, "failed to open %s\n", argv[1]);
        exit(1);
    }

    memset(inbytes, 0, sizeof(inbytes));
    len = fread(inbytes, 1, sizeof(inbytes), fin);
    fclose(fin);

 //   fprintf(stdout, "read %d bytes from openssh file\n", len);

    inptr = inbytes;

    // skip leading space
    while (isspace(*inptr)) inptr++;

    // skip the ssh-rsa or ssh-dsa part
    while (*inptr && !isspace(*inptr)) inptr++;

    // skip spaces between ssh-rsa/ssh-dsa and key
    while (isspace(*inptr)) inptr++;

    // if there is any part after the key, terminate it
    if (strchr(inptr, ' ') != NULL) {
        *strchr(inptr, ' ') = '\0';
    }

    // at this point, inptr contains the b64 encoded openssh key

    len = b64decode(inptr, decodedKey);

//    fprintf(stdout, "decoded openssh file length is %d\n", len);

    fout = fopen(argv[2], "wt");
    if (fout == NULL) {
        fprintf(stderr, "failed to open output file %s\n", argv[2]);
        exit(1);
    }

    openssh_binary_to_openssl(decodedKey, len, fout);

    fclose(fout);

    fprintf(stdout, "completed\n");
    return 0;
}
