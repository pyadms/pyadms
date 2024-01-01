/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/


/* ------- code automatically created by ./mkelements.pl -------------- */

#include "adms.h"
#include "adms_math.h"
#include "adms_instance.h"
#include "adms_attribute.h"
#include "adms_admsmain.h"
#include "adms_yaccval.h"
#include "adms_lexval.h"
#include "adms_variable.h"
#include "adms_math.h"
#include "adms_source.h"
#include "adms_simulator.h"
#include "adms_module.h"
#include "adms_range.h"
#include "adms_node.h"
#include "adms_analogfunction.h"
#include "adms_analog.h"
#include "adms_block.h"
#include <cstdlib>
#include <limits>
#include <map>

#ifdef _WIN32
#include <io.h>
#define F_OK    0       /* Test for existence.  */
#define YY_NO_UNISTD_H
#else
#include <unistd.h>
#endif
#include <sys/stat.h>

void s_adms::get_reference_list(references_list_t &rlist)
{
  get_reference_list_implemented(rlist);
  if (p_math p = dynamic_cast<p_math>(this))
  {
    p->get_reference_list_math(rlist);
  }
}

void s_adms::get_attribute_list(attributes_list_t &alist)
{
  get_attribute_list_implemented(alist);
  if (p_math p = dynamic_cast<p_math>(this))
  {
    p->get_attribute_list_math(alist);
  }
}

void s_adms::get_string_list(strings_list_t &slist)
{
  get_string_list_implemented(slist);
  if (p_math p = dynamic_cast<p_math>(this))
  {
    p->get_string_list_math(slist);
  }
  const std::string &datatypename = get_admse_string(_datatypename);
}



/*-- Miscellaneous routines --*/
std::string adms_integertostring (int value)
{
  return std::to_string(value);
}


int adms_file_isregular (std::string myfilename)
{
  return((access(myfilename.c_str(),F_OK)==0));
}
int adms_file_isdirectory (std::string myfilename)
{
  struct stat s;
  return((stat(myfilename.c_str(),&s)==0)&&(s.st_mode&S_IFDIR));
}

bool is_valid_scaling_unit(const std::string &lv)
{
  return
  (lv == "E") ||
  (lv == "P") ||
  (lv == "T") ||
  (lv == "G") ||
  (lv == "M") ||
  (lv == "k") ||
  (lv == "h") ||
  (lv == "D") ||
  (lv == "d") ||
  (lv == "c") ||
  (lv == "m") ||
  (lv == "u") ||
  (lv == "n") ||
  (lv == "A") ||
  (lv == "p") ||
  (lv == "f") ||
  (lv == "a") ;
}

void push_back_attributes(attributes_list_t &alist, attribute_list &attribute)
{
  for (auto a : attribute) {
    alist.push_back(mytup2{a->_name, a->_value});
  }
}

std::string get_admse_string(admse x) {
static std::map<admse, std::string>  m= {
#define DO(a) {admse_ ## a, #a},
ADMSE_VARIABLE_LIST
#undef DO
};
  return m[x];
}

template <typename T>
void push_back_mytup1(references_list_t &rlist, std::string name, std::list<T> &list)
{
  adms_list x;
  std::copy(list.begin(), list.end(), std::back_inserter(x));
  rlist.push_back(mytup1{name, x});
}

template void push_back_mytup1(references_list_t &, std::string, std::list<s_adms *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_admsmain *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_analog *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_analogfunction *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_array *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_assignment *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_attribute *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_block *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_blockvariable *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_branch *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_branchalias *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_callfunction *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_case *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_caseitem *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_conditional *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_continuator *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_contribution *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_discipline *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_expression *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_forloop *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_function *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_instance *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_instancenode *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_instanceparameter *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_lexval *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_list *> &);
template void push_back_mytup1<s_mapply_binary *>(references_list_t &, std::string, std::list<s_mapply_binary *> &);
template void push_back_mytup1<s_mapply_ternary *>(references_list_t &, std::string, std::list<s_mapply_ternary *> &);
template void push_back_mytup1<s_mapply_unary *>(references_list_t &, std::string, std::list<s_mapply_unary *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_math *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_module *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_nature *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_nilled *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_node *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_nodealias *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_number *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_path *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_pparse *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_preprocessor *> &);
//template void push_back_mytup1<s_preprocessor_main *>(references_list_t &, std::string, std::list<s_preprocessor_main *> &);
//template void push_back_mytup1<s_preprocessor_pragma_define *>(references_list_t &, std::string, std::list<s_preprocessor_pragma_define *> &);
//template void push_back_mytup1<s_preprocessor_pragma_define_text *>(references_list_t &, std::string, std::list<s_preprocessor_pragma_define_text *> &);
//template void push_back_mytup1<s_preprocessor_substitutor *>(references_list_t &, std::string, std::list<s_preprocessor_substitutor *> &);
//template void push_back_mytup1<s_preprocessor_text *>(references_list_t &, std::string, std::list<s_preprocessor_text *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_probe *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_ptraverse *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_range *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_simulator *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_slist *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_source *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_string *> &);
//template void push_back_mytup1(references_list_t &, std::string, std::list<s_text *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_variable *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_variableprototype *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_whileloop *> &);
template void push_back_mytup1(references_list_t &, std::string, std::list<s_yaccval *> &);


template <typename T>
std::list<p_adms> create_adms_list(T x)
{
  return std::list<p_adms>{x};
}

template std::list<p_adms> create_adms_list(p_adms x);
template std::list<p_adms> create_adms_list(p_analogfunction x);
template std::list<p_adms> create_adms_list(p_assignment x);
template std::list<p_adms> create_adms_list(p_block x);
template std::list<p_adms> create_adms_list(p_branch x);
template std::list<p_adms> create_adms_list(p_branchalias x);
template std::list<p_adms> create_adms_list(p_discipline x);
template std::list<p_adms> create_adms_list(p_expression x);
template std::list<p_adms> create_adms_list(p_function x);
template std::list<p_adms> create_adms_list(p_instanceparameter x);
template std::list<p_adms> create_adms_list(p_lexval x);
template std::list<p_adms> create_adms_list(p_module x);
template std::list<p_adms> create_adms_list(p_nature x);
template std::list<p_adms> create_adms_list(p_node x);
template std::list<p_adms> create_adms_list(p_simulator x);
template std::list<p_adms> create_adms_list(p_source x);
template std::list<p_adms> create_adms_list(p_variable x);
template std::list<p_adms> create_adms_list(p_variableprototype x);
template std::list<p_adms> create_adms_list(p_analog x);
template std::list<p_adms> create_adms_list(p_number x);


