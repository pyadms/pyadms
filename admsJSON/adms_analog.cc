/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_analog.h"

p_analog adms_analog_new (p_adms mycode)
{
  p_analog mynewanalog = new s_analog(mycode);
  return mynewanalog;
}
std::string s_analog::get_uid_implemented()
{
  std::string myuid="analog ";
  myuid += _code->get_uid();
  return myuid;
}

void s_analog::get_reference_list_implemented(references_list_t &rlist)
{
  rlist = {
    mytup1{"code", adms_list{_code}},
  };
}

void s_analog::get_attribute_list_implemented(attributes_list_t &alist)
{
}

void s_analog::get_string_list_implemented(strings_list_t &slist)
{
}

