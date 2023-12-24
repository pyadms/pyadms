/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_BRANCH_H
#define ADMS_BRANCH_H
#include "adms.h"

/* ------- branch -------------- */
struct s_branch : public s_adms {
  s_branch(p_module mymodule,p_node mypnode,p_node mynnode) : s_adms(admse_branch), _module(mymodule), _pnode(mypnode), _nnode(mynnode), _discipline(nullptr) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_module _module;
  p_node _pnode;
  p_node _nnode;
  p_discipline _discipline;
  attribute_list _attribute;
};
p_branch adms_branch_new (p_module mymodule,p_node mypnode,p_node mynnode);

/* ------- branchalias -------------- */
struct s_branchalias: public s_adms {
  s_branchalias(p_module mymodule, std::string myname) : s_adms(admse_branchalias), _module(mymodule), _name(myname), _branch(nullptr) {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_module _module;
  std::string _name;
  p_branch _branch;
};
std::string adms_branchalias_uid (p_branchalias mybranchalias);
p_branchalias adms_branchalias_new (p_module mymodule,std::string myname);
void adms_branchalias_free(p_branchalias mybranchalias);
int adms_branch_cmp (p_branch mybranch,p_branch refbranch);
#endif

