/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_ANALOG_H
#define ADMS_ANALOG_H
#include "adms.h"
/* ------- analog -------------- */
struct s_analog : s_adms{
  s_analog(p_adms mycode) : s_adms(admse_analog), _code(mycode) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_adms _code;
};

p_analog adms_analog_new (p_adms mycode);

#endif

