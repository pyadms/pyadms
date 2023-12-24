/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_INSTANCE_H
#define ADMS_INSTANCE_H
#include "adms.h"
#include "adms_math.h"

/* ------- instance -------------- */
struct s_instance : public s_math {
  s_instance (p_module myinstantiator,p_module mymodule, std::string myname)
   : s_math(admse_instance) , _instantiator(myinstantiator), _module(mymodule), _name(myname) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_module _instantiator;
  p_module _module;
  std::string _name;
  instancenode_list _terminal;
  instanceparameter_list _parameterset;
};
p_instance adms_instance_new (p_module myinstantiator,p_module mymodule, std::string myname);
void adms_instance_list_terminal_prepend_once_or_abort (p_instance mymyinstance,p_instancenode myterminal);
void adms_instance_list_parameterset_prepend_once_or_abort (p_instance mymyinstance,p_instanceparameter myparameterset);

/* ------- instanceparameter -------------- */
struct s_instanceparameter : public s_math {
  s_instanceparameter (p_variableprototype myparameter) :
    s_math(admse_instanceparameter), _parameter(myparameter), _value(nullptr) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_variableprototype _parameter;
  p_expression _value;
};
p_instanceparameter adms_instanceparameter_new (p_variableprototype myparameter);

/* ------- instancenode -------------- */
struct s_instancenode : public s_math {
  s_instancenode (p_node mynodefrominstantiator,p_node mynodefrommodule)
  : s_math(admse_instancenode), _nodefrominstantiator(mynodefrominstantiator), _nodefrommodule(mynodefrommodule) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_node _nodefrominstantiator;
  p_node _nodefrommodule;
};
p_instancenode adms_instancenode_new (p_node mynodefrominstantiator,p_node mynodefrommodule);

int adms_instance_cmp (p_instance myinstance,p_instance refinstance);
int adms_instanceparameter_cmp (p_instanceparameter myinstanceparameter,p_instanceparameter refinstanceparameter);
int adms_instancenode_cmp (p_instancenode myinstancenode,p_instancenode refinstancenode);
#endif
