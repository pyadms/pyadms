/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef JSON_SERIALIZER_H
#define JSON_SERIALIZER_H
#include "adms.h"
#include <list>
#include <unordered_map>
#include <utility>
#include <vector>
#include <iostream>

struct json_object {
  json_object(size_t sn, p_adms pt) : serial_number(sn), pointer(pt) {}

  size_t serial_number;
  p_adms pointer;
  std::string uid;
  strings_list_t strings;
  references_list_t   references;
  attributes_list_t   attributes;
//// also do math info ////
};


typedef std::unordered_map<p_adms, json_object *> json_map_t;
typedef std::vector<json_object *> json_list_t;

void json_serialize(p_adms top, json_map_t &/*json_index*/, json_list_t &/*json_rindex*/);
void json_write(std::ostream &out, json_map_t &/*json_index*/, json_list_t &/*json_rindex*/);

#endif

