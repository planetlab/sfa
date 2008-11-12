#include "b64decode.h"

#define UNDEF_CH -2

char s64table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
int     charmap[257];
int     *pcharmap;

void b64decodeinit()
{
   int i;
   char ch;

   pcharmap= charmap + 1;

  for (i = 0; i <= 255; i++)
    pcharmap[i] = UNDEF_CH;

  for (i = 0; i < 64; i++) {
    ch = s64table[i];
    if (pcharmap[ch] == UNDEF_CH)
      pcharmap[ch] = i;
  }
}

int b64decode(char *s, char *dest)
{
  int k,k2,i;

  i=0;
  while (*s!='\0') {
    /* byte #1 */
    if ((*s=='=') || ((k=pcharmap[(unsigned char) (*(s++))])<0))
      return -1;

    /* byte #2 */
    if ((*s=='=') || ((k2=pcharmap[(unsigned char) (*(s++))])<0))
      return -1;
    else
      dest[i++] = (k<<2) + (k2>>4);

    /* byte #3 */
    if (*s=='=')
      s++;
    else
      if ((k=pcharmap[(unsigned char) (*(s++))])<0)
	return -1;
      else
	dest[i++] = (k2<<4) + (k>>2);

    /* byte #4 */
    if (*s=='=')
      s++;
    else
      if ((k2=pcharmap[(unsigned char) (*(s++))])<0)
	-1;
      else
	dest[i++] = (k<<6) + (k2);
  }

  return i;
}
