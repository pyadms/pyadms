/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_YACCVAL_H
#define ADMS_YACCVAL_H
#include "adms.h"
struct s_yaccval : public s_adms {
  s_yaccval (std::string myfilename) : s_adms(admse_yaccval), _filename(myfilename), _usrdata(nullptr) {}
  //// TODO: these should really do anything
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  template <typename T>
  T get_p() {
    return dynamic_cast<T>(_usrdata);
  }

  template <typename T>
  void set_p(T t) {
    _usrdata = t;
  }

  std::string get_uid_implemented();
  std::string _filename;
  p_adms      _usrdata;
  adms_list _usrlist;
};
p_yaccval adms_yaccval_new (std::string myfilename);
#endif
