/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_attribute.h"

/* ------- attribute -------------- */
p_attribute adms_attribute_new (std::string myname, std::string myvalue)
{
  p_attribute mynewattribute = new s_attribute(myname, myvalue);
  return mynewattribute;
}

std::string s_attribute::get_uid_implemented()
{
  std::string myuid;
  myuid += _name;
  return myuid;
}

void s_attribute::get_reference_list_implemented(references_list_t &rlist)
{
}

void s_attribute::get_attribute_list_implemented(attributes_list_t &alist)
{
}

void s_attribute::get_string_list_implemented(strings_list_t &slist)
{
  slist = {
    mytup2{"name", _name},
    mytup2{"value", _value},
  };
}

