/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_yaccval.h"

/* ------- yaccval -------------- */
p_yaccval adms_yaccval_new (std::string myfilename)
{
  p_yaccval mynewyaccval = new s_yaccval(myfilename);
  return mynewyaccval;
}

std::string s_yaccval::get_uid_implemented ()
{
  return _filename;
}


void s_yaccval::get_reference_list_implemented(references_list_t &rlist)
{
}

void s_yaccval::get_attribute_list_implemented(attributes_list_t &alist)
{
}

void s_yaccval::get_string_list_implemented(strings_list_t &slist)
{
}

