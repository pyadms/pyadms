/***
This is a derivative work of ADMS.  Original code is copyight the original authors.
Modifications Copyright Luther T. Cat

ADMS
Copyright (C) 2015  Luther T. Cat
Original code copyright the original authors.
***/

#include "adms_message.h"
#include "adms_admsmain.h"
#include <cstdarg>
#include <cassert>

/*-- Messaging --*/
FILE* adms_file_open_read (const char* myfilename)
{
  FILE* fh=fopen(myfilename,"r");
  if(!fh)
    adms_message_fatal("%s: failed to open file [read mode]\n",myfilename);
  return fh;
}

void adms_message_info_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[info...] ",stdout);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stdout); else fputs("NULL",stdout);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stdout,"%e",d);
          break;
        case 'c':
          c=va_arg (ap,int);
          fprintf(stdout,"%c",c);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stdout,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stdout,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stdout,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stdout,"%p",p);
          break;
        default:
          fputc(*format,stdout);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stdout);
      }
    }
  }
  va_end (ap);
  fflush(stdout);
}

void adms_message_usage_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[usage..] ",stdout);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stdout); else fputs("NULL",stdout);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stdout,"%e",d);
          break;
        case 'c':
          c=va_arg (ap,int);
          fprintf(stdout,"%c",c);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stdout,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stdout,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stdout,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stdout,"%p",p);
          break;
        default:
          fputc(*format,stdout);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stdout);
      }
    }
  }
  va_end (ap);
  fflush(stdout);
}
void adms_message_usage_continue_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stdout); else fputs("NULL",stdout);
          break;
        case 'c':
          c=va_arg (ap,int);
          fputc(c,stdout);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stdout,"%e",d);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stdout,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stdout,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stdout,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stdout,"%p",p);
          break;
        default:
          fputc(*format,stdout);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stdout);
      }
    }
  }
  va_end (ap);
  fflush(stdout);
}
void adms_message_verbose_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[verbose] ",stdout);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stdout); else fputs("NULL",stdout);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stdout,"%e",d);
          break;
        case 'c':
          c=va_arg (ap,int);
          fprintf(stdout,"%c",c);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stdout,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stdout,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stdout,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stdout,"%p",p);
          break;
        default:
          fputc(*format,stdout);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stdout);
      }
    }
  }
  va_end (ap);
  fflush(stdout);
}
void adms_message_dbg_vla_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[dbg_vla] ",stdout);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stdout); else fputs("NULL",stdout);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stdout,"%e",d);
          break;
        case 'c':
          c=va_arg (ap,int);
          fprintf(stdout,"%c",c);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stdout,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stdout,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stdout,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stdout,"%p",p);
          break;
        default:
          fputc(*format,stdout);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stdout);
      }
    }
  }
  va_end (ap);
  fflush(stdout);
}
void adms_message_warning_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[warning] ",stderr);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stderr); else fputs("NULL",stderr);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stderr,"%e",d);
          break;
        case 'c':
          c=va_arg (ap,int);
          fprintf(stderr,"%c",c);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stderr,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stderr,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stderr,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stderr,"%p",p);
          break;
        default:
          fputc(*format,stderr);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stderr);
      }
    }
  }
  va_end (ap);
  fflush(stderr);
}

void adms_message_fatal_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[fatal..] ",stderr);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stderr); else fputs("NULL",stderr);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stderr,"%e",d);
          break;
        case 'c':
          c=va_arg (ap,int);
          fprintf(stderr,"%c",c);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stderr,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stderr,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stderr,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stderr,"%p",p);
          break;
        default:
          fputc(*format,stderr);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stderr);
      }
    }
  }
  va_end (ap);
  fflush(stderr);
#ifndef NDEBUG
  assert(0);
#endif
  exit(1);
}
void adms_message_fatal_continue_impl(const char *format, ...)
{
  va_list ap;
  int insideformat=0;
  int i;
  char* s;
  char c;
  double d;
  void* p;
  fputs("[fatal..] ",stderr);
  va_start(ap, format);
  for(;*format;format++)
  {
    if(insideformat)
    {
      insideformat=0;
      switch(*format) 
      {
        case 's':
          s=va_arg (ap,char*);
          if(s) fputs(s,stderr); else fputs("NULL",stderr);
          break;
        case 'c':
          c=va_arg (ap,int);
          fputc(c,stderr);
          break;
        case 'e':
          d=va_arg (ap,double);
          fprintf(stderr,"%e",d);
          break;
        case 'g':
          d=va_arg (ap,double);
          fprintf(stderr,"%g",d);
          break;
        case 'f':
          d=va_arg (ap,double);
          fprintf(stderr,"%f",d);
          break;
        case 'i':
          i=va_arg (ap,int);
          fprintf(stderr,"%i",i);
          break;
        case 'p':
          p=va_arg (ap,void*);
          fprintf(stderr,"%p",p);
          break;
        default:
          fputc(*format,stderr);
      }
    }
    else
    {
      switch(*format) 
      {
        case '%':
          insideformat=1;
          break;
        default:
          fputc(*format,stderr);
      }
    }
  }
  va_end (ap);
  fflush(stderr);
}

