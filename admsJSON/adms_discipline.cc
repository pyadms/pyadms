/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_discipline.h"
#if 0
#include "adms_nature.h"
#endif

int adms_discipline_cmp (p_discipline mydiscipline,p_discipline refdiscipline)
{
  return mydiscipline->_name.compare(refdiscipline->_name);
}

p_discipline adms_discipline_new (std::string myname)
{
  p_discipline mynewdiscipline = new s_discipline(myname);
  return mynewdiscipline;
}
std::string s_discipline::get_uid_implemented()
{
  return _name;
}

void s_discipline::get_reference_list_implemented(references_list_t &rlist)
{
  rlist = {
    mytup1{"flow", create_adms_list(_flow)},
    mytup1{"potential", create_adms_list(_potential)},
  };
}

void s_discipline::get_attribute_list_implemented(attributes_list_t &alist)
{
}

void s_discipline::get_string_list_implemented(strings_list_t &slist)
{
  slist = {
    mytup2{"name", _name},
    mytup2{"domain", get_admse_string(_domain)},
  };
}


