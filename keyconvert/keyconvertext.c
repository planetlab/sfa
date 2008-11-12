#include <python2.3/Python.h>

#include "keyconvert.h"

static PyObject *keyconvert_opensshtoopenssl(PyObject *self, PyObject *args)
{
    const char *fn;
    const char *s;
    int len;
    FILE *fout;

    PyArg_ParseTuple(args, "ss#", &fn, &s, &len);

    fout = fopen(fn, "wt");
    if (fout == NULL) {
        return Py_BuildValue("i", 0);
    } else {
        fprintf(stdout, "len = %d\n", len);
        openssh_binary_to_openssl(s, len, fout);
        fclose(fout);
    }

    return Py_BuildValue("i", 1);
}

static PyMethodDef KeyConvertMethods[] = {
    {"opensshtoopenssl", keyconvert_opensshtoopenssl, METH_VARARGS, "convert an openssh key to an openssl key"},
    {NULL, NULL, 0, NULL}};

PyMODINIT_FUNC initkeyconvert(void)
{
    (void) Py_InitModule("keyconvert", KeyConvertMethods);
}

