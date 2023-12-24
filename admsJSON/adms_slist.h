/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_SLIST_H
#define ADMS_SLIST_H
#include <string>

struct s_adms;
typedef s_adms *p_adms;
struct s_slist;
typedef s_slist *p_slist;


p_slist adms_slist_new (p_adms d);
p_slist adms_slist_copy (p_slist l);
void adms_slist_concat (p_slist* l1,p_slist l2);
#if 0
p_slist adms_slist_find (p_slist l,p_kadms data);
int adms_slist_index (p_slist l, p_kadms data);
#endif
void adms_slist_free (p_slist l);

p_slist adms_slist_last (p_slist l);
unsigned int adms_slist_length (p_slist l);
p_slist adms_slist_nth (p_slist l,unsigned int  n);
p_adms adms_slist_nth_data (p_slist l,unsigned int n);
void adms_slist_print(std::string message,p_slist l);
p_adms adms_slist_pull(p_slist* l);
void adms_slist_push(p_slist* l,p_adms data);
p_slist adms_slist_reverse (p_slist l);
void adms_slist_inreverse (p_slist* l);
struct s_slist
{
  p_adms data;
  p_slist next;
};
#endif

