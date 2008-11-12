#include <stdlib.h>
#include <openssl/bn.h>
#include <openssl/rsa.h>
#include <openssl/dsa.h>

#ifndef TRUE
#define TRUE 1
#define FALSE (!TRUE)
#endif

void write_rsa(FILE *fout, char *estr, int elen, char *nstr, int nlen)
{
    RSA *rsa;
    BIGNUM *r1, *r2;

    rsa = RSA_new();
    rsa->e = BN_new();
    rsa->n = BN_new();

    r1 = BN_bin2bn(estr, elen, rsa->e);
    r2 = BN_bin2bn(nstr, nlen, rsa->n);

    PEM_write_RSA_PUBKEY(fout, rsa);

    // free rsa ?
}

void write_dsa(FILE *fout, char *pstr, int plen, char *qstr, int qlen, char *gstr, int glen, char *pkstr, int pklen)
{
    DSA *dsa;

    dsa = DSA_new();
    dsa->p = BN_new();
    dsa->q = BN_new();
    dsa->g = BN_new();
    dsa->pub_key = BN_new();

    BN_bin2bn(pstr, plen, dsa->p);
    BN_bin2bn(qstr, qlen, dsa->q);
    BN_bin2bn(gstr, glen, dsa->g);
    BN_bin2bn(pkstr, pklen, dsa->pub_key);

    PEM_write_DSA_PUBKEY(fout, dsa);

    // free dsa ?
}

int get_str(char **src, int *len, char *dest)
{
   int *iptr = (int*) (*src);
   int thislen = ntohl(*iptr);

   // eat 4 bytes
   (*len) -= 4;
   (*src) = (*src) + 4;

//   fprintf(stdout, "thislen = %d\n", thislen);

   if (thislen > *len) {
       fprintf(stdout, "thislen(%d) > *len(%d)\n", thislen, *len);
       return -1;
   }

   memcpy(dest, *src, thislen);

   (*len) = (*len) - thislen;
   (*src) = (*src) + thislen;

   // null terminate it
   *(dest + thislen) = '\0';

   return thislen;
}

int openssh_binary_to_openssl(char *s, int len, FILE *fout)
{
    char keytype[1024], estr[1024], nstr[1024], pstr[1024], qstr[1024], gstr[1024], pkstr[1024];
    int elen, nlen, plen, qlen, glen, pklen;
    int result;

    result = get_str(&s, &len, keytype);
    if (result <= 0) {
        return FALSE;
    }

    fprintf(stdout, "keytype = %s\n", keytype);

    if (strcmp(keytype, "ssh-rsa") == 0) {
        elen = get_str(&s, &len, estr);
//        fprintf(stdout, "elen = %d\n", elen);
        if (elen <= 0) {
            return FALSE;
        }
        nlen = get_str(&s, &len, nstr);
//        fprintf(stdout, "nlen = %d\n", nlen);
        if (nlen <= 0) {
            return FALSE;
        }
        write_rsa(fout, estr, elen, nstr, nlen);
    } else if (strcmp(keytype, "ssh-dss") == 0) {
        plen = get_str(&s, &len, pstr);
//        fprintf(stdout, "plen = %d\n", plen);
        if (plen <= 0) {
            return FALSE;
        }
        qlen = get_str(&s, &len, qstr);
//        fprintf(stdout, "qlen = %d\n", qlen);
        if (qlen <= 0) {
            return FALSE;
        }
        glen = get_str(&s, &len, gstr);
//        fprintf(stdout, "glen = %d\n", glen);
        if (glen <= 0) {
            return FALSE;
        }
        pklen = get_str(&s, &len, pkstr);
//        fprintf(stdout, "pklen = %d\n", pklen);
        if (pklen <= 0) {
            return FALSE;
        }
        write_dsa(fout, pstr, plen, qstr, qlen, gstr, glen, pkstr, pklen);
    } else {
        return FALSE;
    }
}

