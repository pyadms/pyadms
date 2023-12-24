/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_SIMULATOR_H
#define ADMS_SIMULATOR_H
#include "adms.h"

struct s_simulator : public s_adms {
  s_simulator(std::string name) : s_adms(admse_simulator), _name(name) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  std::string _name;
  std::string _developer;
  std::string _fullname;
  std::string _package_name;
  std::string _package_tarname;
  std::string _package_version;
  std::string _package_string;
  std::string _package_bugreport;
};
p_simulator adms_simulator_new (std::string myname);
#endif

