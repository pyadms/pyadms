/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#ifndef ADMS_MESSAGE_H
#define ADMS_MESSAGE_H
#include "adms.h"
#include <cstdio>
#include <ctype.h>
#include <string.h>
#include <cstdlib>

/*-- Messaging --*/
typedef void (t_message) (const char*format, ...);

FILE *adms_file_open_read (const char* fileName);
void adms_message_info_impl(const char *format, ...);
#define adms_message_info(...)\
do {\
  if((root())\
    &&(root()->_info==admse_yes))\
    adms_message_info_impl(__VA_ARGS__);\
} while(0)

void adms_message_usage_impl(const char *format, ...);
void adms_message_usage_continue_impl(const char *format, ...);
#define adms_message_usage(...)\
do {\
  if((root())\
    &&(root()->_usage==admse_yes))\
    adms_message_usage_impl(__VA_ARGS__);\
} while(0)
#define adms_message_usage_continue(...)\
do {\
  if((root())\
    &&(root()->_usage==admse_yes))\
    adms_message_usage_continue_impl(__VA_ARGS__);\
} while(0)
void adms_message_verbose_impl(const char *format, ...);
#define adms_message_verbose(...)\
do {\
  if((root())\
    &&(root()->_verbose==admse_yes))\
    adms_message_verbose_impl(__VA_ARGS__);\
} while(0)
void adms_message_dbg_vla_impl(const char *format, ...);
#define adms_message_dbg_vla(...)\
do {\
  if((root())\
    &&(root()->_dbg_vla==admse_yes))\
    adms_message_dbg_vla_impl(__VA_ARGS__);\
} while(0)
void adms_message_warning_impl(const char *format, ...);
#define adms_message_warning(...)\
do {\
  if((root())\
    &&(root()->_warning==admse_yes))\
    adms_message_warning_impl(__VA_ARGS__);\
} while(0)
void adms_message_fatal_impl(const char *format, ...);
void adms_message_fatal_continue_impl(const char *format, ...);
#define adms_message_fatal(...)\
do {\
  if((root())\
    &&(root()->_fatal==admse_yes))\
    adms_message_fatal_impl(__VA_ARGS__);\
} while(0)
#define adms_message_fatal_continue(...)\
do {\
  if((root())\
    &&(root()->_fatal==admse_yes))\
    adms_message_fatal_continue_impl(__VA_ARGS__);\
} while(0)

#endif

