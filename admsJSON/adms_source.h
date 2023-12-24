/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_SOURCE_H
#define ADMS_SOURCE_H
#include "adms.h"
#include "adms_nature.h"
#include "adms_branch.h"

/* ------- source -------------- */
struct s_source : public s_adms {
  s_source (p_module mymodule,p_branch mybranch,p_nature mynature)
    : s_adms(admse_source), _module(mymodule), _branch(mybranch), _nature(mynature), _discipline(nullptr)
  {}

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  p_module _module;
  p_branch _branch;
  p_nature _nature;
  p_discipline _discipline;
  probe_list _probe;
  attribute_list _attribute;
};
p_source adms_source_new (p_module mymodule,p_branch mybranch,p_nature mynature);
int adms_source_cmp (p_source mysource,p_source refsource);
#endif

