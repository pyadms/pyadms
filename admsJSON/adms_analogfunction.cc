/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_analogfunction.h"
#include "adms_message.h"
#include "adms_variable.h"
#include "adms_admsmain.h"
#include "adms_module.h"

int adms_analogfunction_cmp (p_analogfunction myanalogfunction,p_analogfunction refanalogfunction)
{
  return
  (
    (myanalogfunction->_module != refanalogfunction->_module)
    ||
    myanalogfunction->_lexval->_string.compare(refanalogfunction->_lexval->_string)
  );
}

void adms_analogfunction_list_variable_prepend_once_or_abort (p_analogfunction mymyanalogfunction,p_variableprototype myvariable)
{
  myprepend_or_fail<s_variableprototype>(mymyanalogfunction->_variableprototype,
    [&](p_variableprototype m)->bool {return !adms_variableprototype_cmp(m, myvariable);},
    [&](void)->void {
      adms_message_fatal("analogfunction=[%s] variable=[%s] already defined\n",
        mymyanalogfunction->get_uid().c_str(),myvariable->get_uid().c_str());},
    [&](void)->p_variableprototype {return myvariable;}
    );
}

p_variableprototype adms_analogfunction_list_variable_lookup_by_id (p_analogfunction mymyanalogfunction,p_module mymodule,p_lexval mylexval,p_adms myblock)
{
  p_variableprototype ret = nullptr;
  if (mymyanalogfunction)
  {
    return mylookup_by_id<s_variableprototype>( mymyanalogfunction->_variableprototype,
      [&](p_variableprototype m)->bool {
        return (m->_module==mymodule)&&
           !m->_lexval->_string.compare(mylexval->_string)&&
           (m->_block==myblock);
      });
  }
  return ret;
}

p_analogfunction adms_analogfunction_new (p_module mymodule,p_lexval mylexval)
{
  p_analogfunction mynewanalogfunction = new s_analogfunction(mymodule, mylexval);
  return mynewanalogfunction;
}

std::string s_analogfunction::get_uid_implemented()
{
  std::string myuid = _module->get_uid();
  myuid += ":";
  myuid += _lexval->get_uid();
  return myuid;
}

void s_analogfunction::get_reference_list_implemented(references_list_t &rlist)
{
  rlist = {
    mytup1{"module", adms_list{_module}},
    mytup1{"lexval", adms_list{_lexval}},
    mytup1{"tree", adms_list{_tree}},
  };

  push_back_mytup1(rlist, "variableprototype", _variableprototype);
}

void s_analogfunction::get_attribute_list_implemented(attributes_list_t &alist)
{
  push_back_attributes(alist, _attribute);
}

void s_analogfunction::get_string_list_implemented(strings_list_t &slist)
{
  slist = {
    mytup2{"type", get_admse_string(_type)},
  };
}

