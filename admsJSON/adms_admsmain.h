/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_MAIN_H
#define ADMS_MAIN_H
#include "adms.h"

struct s_admsmain : public s_adms {
  s_admsmain(std::string name) : s_adms(admse_admsmain), _name(name),
  _curline(-1),
  _fpos(-1),
  _simulator(nullptr),
  _info(admse_yes),
  _usage(admse_yes),
  _verbose(admse_no),
  _warning(admse_yes),
  _dbg_vla(admse_no),
  _fatal(admse_yes)
 {}

  ~s_admsmain() {
  }

  std::string get_uid_implemented();
  void get_reference_list_implemented(references_list_t &rlist);
  void get_attribute_list_implemented(attributes_list_t &alist);
  void get_string_list_implemented(strings_list_t &slist);

  std::string _name;
  std::string _fullfilename;
  std::string _filename;
  std::string _curfilename;
  int _curline;
  int _fpos;

  p_simulator _simulator;
  admse _info;
  admse _usage;
  admse _verbose;
  admse _warning;
  admse _dbg_vla;
  admse _fatal;

  module_list     _module;
  discipline_list _discipline;
  nature_list     _nature;
};

p_admsmain adms_admsmain_new (std::string myname);
p_module adms_admsmain_list_module_prepend_by_id_once_or_abort (p_admsmain mymyadmsmain,std::string myname);
p_module adms_admsmain_list_module_lookup_by_id (p_admsmain mymyadmsmain,std::string myname);
void adms_admsmain_list_discipline_prepend_once_or_abort (p_admsmain mymyadmsmain,p_discipline mydiscipline);
p_discipline adms_admsmain_list_discipline_lookup_by_id (p_admsmain mymyadmsmain,std::string myname);

p_nature adms_admsmain_list_nature_prepend_by_id_once_or_abort (p_admsmain mymyadmsmain,std::string myaccess);
p_nature adms_admsmain_list_nature_lookup_by_id (p_admsmain mymyadmsmain,std::string myaccess);

p_admsmain root(void);
void rootnew(p_admsmain myglobaladmsmain);
#endif
