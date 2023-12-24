/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_lexval.h"

p_lexval adms_lexval_new (std::string mystring,std::string myf,int myl,int myc)
{
  p_lexval mynewlexval = new s_lexval(mystring, myf, myl, myc);
  return mynewlexval;
}

std::string s_lexval::get_uid_implemented()
{
  std::string myuid;
  myuid += _string;
  return myuid;
}

void s_lexval::get_reference_list_implemented(references_list_t &rlist)
{
}

void s_lexval::get_attribute_list_implemented(attributes_list_t &alist)
{
}

void s_lexval::get_string_list_implemented(strings_list_t &slist)
{
  slist = {
    mytup2{"string", _string},
    mytup2{"f", _f},
    mytup2{"l", std::to_string(_l)},
    mytup2{"c", std::to_string(_c)},
  };
}
