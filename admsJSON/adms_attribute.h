/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_ATTRIBUTE_H
#define ADMS_ATTRIBUTE_H
#include "adms.h"
#include <string>
/* ------- attribute -------------- */
struct s_attribute : public s_adms {
s_attribute (std::string myname, std::string myvalue)
  : s_adms(admse_attribute), _name(myname), _value(myvalue) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  std::string _name;
  std::string _value;
};

p_attribute adms_attribute_new(std::string myname, std::string myvalue);
#endif

