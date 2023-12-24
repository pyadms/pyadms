/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_VARIABLE_H
#define ADMS_VARIABLE_H
#include "adms.h"

/* ------- variableprototype -------------- */
struct s_variableprototype : public s_adms {
  s_variableprototype(p_module mymodule,p_lexval mylexval,p_adms myblock)
    : s_adms(admse_variableprototype), _module(mymodule), _lexval(mylexval), _block(myblock),
      _maxsize(nullptr),
      _minsize(nullptr),
      _default(nullptr),
      _vlast(nullptr),
      _sizetype(admse_scalar),
      _parametertype(admse_model),
      _type(admse_real),
      _input(admse_no),
      _output(admse_no),
      _vcount(0)
   {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_module _module;
  p_lexval _lexval;
  p_adms _block;
  admse _sizetype;
  admse _parametertype;
  admse _type;
  p_number _maxsize;
  p_number _minsize;
  admse _input;
  admse _output;
  p_expression _default;
  int _vcount;
  p_assignment _vlast;
  p_adms_list    _arraydefault;
  attribute_list _attribute;
  string_list _alias;
  range_list _range;
  variable_list _instance;
};

p_variableprototype adms_variableprototype_new (p_module mymodule,p_lexval mylexval,p_adms myblock);

void adms_variableprototype_list_alias_prepend_once_or_abort (p_variableprototype mymyvariableprototype,std::string myalias);

int adms_variableprototype_cmp (p_variableprototype myvariableprototype,p_variableprototype refvariableprototype);
#endif

