/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_H
#define ADMS_H
#include <string>
#include <list>
#include <algorithm>
#include <iterator>
#include <limits>

#define ADMS_PATH_SEPARATOR "/"
#define PACKAGE_NAME "adms"
#define PACKAGE_VERSION "2.3.0"
#define PACKAGE_BUGREPORT "lutherthecat@github"
#define ADMS_COMPILER "N/A" 
#define ADMS_OS "N/A" 

#define ADMSE_VARIABLE_LIST \
DO(simulator) \
DO(admsmain) \
DO(list) \
DO(nature) \
DO(discipline) \
DO(module) \
DO(analogfunction) \
DO(nodealias) \
DO(node) \
DO(branchalias) \
DO(branch) \
DO(variableprototype) \
DO(source) \
DO(range) \
DO(analog) \
DO(string) \
DO(mapply_unary) \
DO(mapply_binary) \
DO(mapply_ternary) \
DO(number) \
DO(function) \
DO(variable) \
DO(array) \
DO(probe) \
DO(expression) \
DO(instance) \
DO(instanceparameter) \
DO(instancenode) \
DO(nilled) \
DO(assignment) \
DO(contribution) \
DO(conditional) \
DO(forloop) \
DO(whileloop) \
DO(case) \
DO(caseitem) \
DO(blockvariable) \
DO(block) \
DO(callfunction) \
DO(attribute) \
DO(lexval) \
DO(yaccval) \
DO(input) \
DO(output) \
DO(yes) \
DO(no) \
DO(continuous) \
DO(discrete) \
DO(real) \
DO(integer) \
DO(inout) \
DO(internal) \
DO(ground) \
DO(external) \
DO(scalar) \
DO(model) \
DO(range_bound_include) \
DO(range_bound_exclude) \
DO(range_bound_value) \
DO(include) \
DO(include_value) \
DO(exclude) \
DO(exclude_value) \
DO(plus) \
DO(minus)

// update for get_admse_string
enum admse {
#define DO(a) admse_ ## a,
ADMSE_VARIABLE_LIST
#undef DO
};


/*
struct        s_adms;
typedef       s_adms *p_adms;
typedef std::list<p_adms> adms_list;
*/

#define LIST_OF_VARIABLES \
DO2(admsmain) \
DO2(analog) \
DO2(lexval) \
DO2(simulator) \
DO2(yaccval) \
DO4(adms) \
DO4(analogfunction) \
DO4(attribute) \
DO4(branch) \
DO4(branchalias) \
DO4(discipline) \
DO4(module) \
DO4(nature) \
DO4(node) \
DO4(nodealias) \
DO4(range) \
DO4(source) \
DO4(variableprototype) \
/* math */ \
DO2(array) \
DO2(caseitem) \
DO2(function) \
DO2(mapply_binary) \
DO2(mapply_ternary) \
DO2(mapply_unary) \
DO2(math) \
DO2(nilled) \
DO2(number) \
DO4(assignment) \
DO4(block) \
DO4(blockvariable) \
DO4(callfunction) \
DO4(case) \
DO4(conditional) \
DO4(contribution) \
DO4(expression) \
DO4(forloop) \
DO4(instance) \
DO4(instancenode) \
DO4(instanceparameter) \
DO4(probe) \
DO4(string) \
DO4(variable) \
DO4(whileloop)


#define DO2(a) \
struct s_ ## a; \
typedef s_ ## a *p_ ## a;
#define DO3(a) DO2(a) \
typedef std::list<p_ ## a> p_ ## a ## _list;
#define DO4(a) DO2(a) \
typedef std::list<p_ ## a> a ## _list;
LIST_OF_VARIABLES
#undef DO2
#undef DO3
#undef NLINE
#undef LIST_OF_VARIABLES

int admsmain(std::string xcode,std::string xflag,std::string vacode);


/*-- Miscellaneous routines --*/
std::string adms_integertostring(int value);
int adms_file_isdirectory(std::string myfilename);
int adms_file_isregular(std::string myfilename);


typedef std::tuple<std::string, std::list<p_adms> > mytup1;
typedef std::tuple<std::string, std::string > mytup2;
typedef std::list <mytup1> references_list_t;
typedef std::list <mytup2> attributes_list_t;
typedef attributes_list_t strings_list_t;

/* ------- adms -------------- */
struct s_adms {
  s_adms(admse datatypename) : _datatypename(datatypename) {}
  virtual ~s_adms() {}

  std::string get_uid() {
    return this->get_uid_implemented();
  }

  void get_reference_list(references_list_t &rlist);
  void get_attribute_list(attributes_list_t &alist);
  void get_string_list(strings_list_t &slist);



  virtual std::string get_uid_implemented() = 0;
  virtual void get_reference_list_implemented(references_list_t &rlist) = 0;
  virtual void get_attribute_list_implemented(attributes_list_t &alist) = 0;
  virtual void get_string_list_implemented(strings_list_t &slist) = 0;

  admse _datatypename;
};






template <typename T>
T* myprepend_or_fail(std::list<T*> &mylist, std::function<bool(T*)> myfunc, std::function<void()> myfail, std::function<T*()> mycreate)
{
  T *ret = mylookup_by_id(mylist, myfunc);

  if (ret)
  {
    myfail();
  }
  else
  {
    ret = mycreate();
    mylist.push_back(ret);
  }
  
  return ret;
}

template <typename T>
T* myprepend_or_ignore(T *new_elem, std::list<T*> &mylist, std::function<bool(T*)> myfunc)
{
  T *ret = new_elem;
  auto it = std::find_if(mylist.begin(), mylist.end(), myfunc);
  if (it != mylist.end())
  {
    ret = *it;
  }
  else
  {
    mylist.push_back(new_elem);
  }
  return ret;
}

template <typename T>
T* mylookup_by_id(std::list<T*> &mylist, std::function<bool(T*)> myfunc)
{
  T *ret = nullptr;
  auto it = std::find_if(mylist.begin(), mylist.end(), myfunc);
  if (it != mylist.end())
  {
    ret = *it; 
  }
  return ret;
}

const double adms_dzero=0.0;
const double adms_NAN = std::numeric_limits<double>::quiet_NaN();

bool is_valid_scaling_unit(const std::string &);

std::string get_admse_string(admse x);

void push_back_attributes(attributes_list_t &, attribute_list &);

template <typename T>
void push_back_mytup1(references_list_t &rlist, std::string name, std::list<T> &list);

template <typename T>
std::list<p_adms> create_adms_list(T);

#endif /* adms_h */

