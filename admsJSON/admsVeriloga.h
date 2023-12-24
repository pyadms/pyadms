/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef _admsveriloga_h
#define _admsveriloga_h

#include "adms.h"

void adms_veriloga_setint_yydebug (const int val);
void adms_veriloga_setfile_input (FILE *ifile);

void verilogaerror (const char *s);
int verilogalex ();
int verilogaparse ();

#endif /* _admsveriloga_h */
