/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_block.h"
#include "adms_message.h"
#include "adms_lexval.h"
#include "adms_variable.h"
#include "adms_admsmain.h"

/* ------- blockvariable -------------- */
p_blockvariable adms_blockvariable_new (p_block myblock)
{
  p_blockvariable mynewblockvariable = new s_blockvariable(myblock);
  return mynewblockvariable;
}

std::string s_blockvariable::get_uid_implemented()
{
  std::string myuid;
  myuid += "real ";
  for (auto v : _variableprototype) {
    myuid += v->get_uid();
    if (v != _variableprototype.back())
    {
      myuid += ",";
    }
  }
  myuid += ";";
  return myuid;
}

void s_blockvariable::get_reference_list_implemented(references_list_t &rlist)
{
  rlist = {
    mytup1{"block", create_adms_list(_block)},
  };
  push_back_mytup1(rlist, "variableprototype", _variableprototype);
}

void s_blockvariable::get_attribute_list_implemented(attributes_list_t &alist)
{
}

void s_blockvariable::get_string_list_implemented(strings_list_t &slist)
{
}


/* ------- block -------------- */
void adms_block_list_variable_prepend_once_or_abort (p_block mymyblock,p_variableprototype myvariable)
{
  myprepend_or_fail<s_variableprototype>(mymyblock->_variableprototype,
    [&](p_variableprototype m)->bool {
      return !adms_variableprototype_cmp(m, myvariable);
    },
    [&](void)->void {
      adms_message_fatal("blockvariable=[%s] variable=[%s] already defined\n",
        mymyblock->get_uid().c_str(),myvariable->get_uid().c_str());
      //delete myvariable;
    },
    [&](void)->p_variableprototype {return myvariable;}
  );
}

p_block adms_block_new (p_module mymodule,p_lexval mylexval,p_adms myblock,adms_list myitem)
{
  p_block mynewblock = new s_block(mymodule, mylexval, myblock, myitem);
  return mynewblock;
}

std::string s_block::get_uid_implemented()
{
  std::string myuid;
  myuid += "begin :";
  myuid += _lexval->get_uid();
  myuid += "\n";

  for (auto i : _item)
  {
    myuid += i->get_uid();
    if (i != _item.back())
    {
      myuid += "\n";
    }
  }
  myuid += "end\n";
  return myuid;
}

void s_block::get_reference_list_implemented(references_list_t &rlist)
{
  rlist = {
    mytup1{"module", create_adms_list(_module)},
    mytup1{"lexval", create_adms_list(_lexval)},
    mytup1{"block", create_adms_list(_block)},
  };
  push_back_mytup1(rlist, "item", _item);
  push_back_mytup1(rlist, "variableprototype", _variableprototype);
}

void s_block::get_attribute_list_implemented(attributes_list_t &alist)
{
  push_back_attributes(alist, _attribute);
}

void s_block::get_string_list_implemented(strings_list_t &slist)
{
}

