/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_LEXVAL_H
#define ADMS_LEXVAL_H
#include "adms.h"
/* ------- lexval -------------- */
struct s_lexval : s_adms {
  s_lexval (std::string mystring, std::string myf, int myl, int myc)
    : s_adms(admse_lexval), _string(mystring), _f(myf), _l(myl), _c(myc) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  std::string _string;
  std::string _f;
  int _l;
  int _c;
};
p_lexval adms_lexval_new (std::string mystring,std::string myf,int myl,int myc);
void adms_lexval_free(p_lexval mylexval);

#endif
