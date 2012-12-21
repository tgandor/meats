%{

/* input-output routines */
#include <stdio.h>
/* strdup */
#include <string.h>

#include "main.h"
#include "atom.h"
#include "atom_codes.h"
#define _ATOM(name) name

#define YY_DECL ATOM yylex()

static int lineno=1;
static int offset;
static int column;

static ATOM construct_atom(int type);
static int handle_single_char(int c);
static int handle_token(int t);
static int decision; 

struct metrics atbanMetrics;
static UNIQUE_DICTIONARY atbanId; 

#define DECIDE(atom) { if((decision=handle_token(atom))!=-1) return construct_atom(decision); }

%}
	
intsuffix				([uU][lL]?)|([lL][uU]?)

%%

"\n"					{ ++lineno; ++offset; column=0; }
[\t\f\v\r ]+			{ offset += yyleng; column += yyleng; }
[-;,=*/%?~&|()\+{}]		{ 
   decision = handle_single_char (*yytext);
   if (decision != -1)
     return construct_atom(decision); 
} 

"+="					DECIDE(_ATOM(ADDEQ));
"-="					DECIDE(_ATOM(SUBEQ));
"*="					DECIDE(_ATOM(MULEQ));
"/="					DECIDE(_ATOM(DIVEQ));
"%="					DECIDE(_ATOM(MODEQ));
"=="					DECIDE(_ATOM(EQ));
"!="					DECIDE(_ATOM(NOTEQ));
"<="					DECIDE(_ATOM(LTEQ));
">="					DECIDE(_ATOM(GTEQ));
"&&"					DECIDE(_ATOM(ANDAND));
"||"					DECIDE(_ATOM(OROR));
"++"					DECIDE(_ATOM(PLUSPLUS));
"--"					DECIDE(_ATOM(MINUSMINUS));

"else"					{ atbanMetrics.else_keywords++; DECIDE(_ATOM(ELSE)); }
"if"					{ atbanMetrics.if_keywords++; DECIDE(_ATOM(IF)); }
"while"					{ atbanMetrics.while_keywords++; DECIDE(_ATOM(WHILE)); }

"print"					DECIDE(_ATOM(PRINT));
"input"					DECIDE(_ATOM(INPUT));

[a-zA-Z_][a-zA-Z_0-9]*	 { atbanMetrics.identifiers++; unique_dictionary_add(atbanId, yytext); DECIDE(_ATOM(IDENTIFIER)); }

"0"[xX][0-9a-fA-F]+{intsuffix}?		{ return construct_atom(_ATOM(INTEGER)); }
"0"[0-7]+{intsuffix}?			{ return construct_atom(_ATOM(INTEGER)); }
[0-9]+{intsuffix}?			{ return construct_atom(_ATOM(INTEGER)); }


.	{ 
   fprintf(stderr, _("%d: unexpected character `%c'\n"), lineno, *yytext); 
   ++offset; ++column;
}

<<EOF>> { 
  atbanMetrics.lines=lineno; 
  atbanMetrics.unique_ids = atbanId->count;
  free_unique_dictionary(atbanId);
  free(atbanId);
  return (ATOM)0; 
}

%%

int yywrap()
{
	return 1;
}

int handle_single_char(int c)
{
  switch(c)
  {
    /* 
	Atoms which are not interesting 
	---
	Atomy, które nie s± ciekawe
	*/ 
    case ';':
	case ',':
	  return -1;
	/*
	Interesting atoms
	---
	Atomy, które s± ciekawe
	*/
	case '{': 
	  return _ATOM(BEGN);
	case '}': 
	  return _ATOM(END);
	case '+':
	  atbanMetrics.plus++;
	  return _ATOM(ARITHMETIC);
	case '-':
	  atbanMetrics.minus++;
	  return _ATOM(ARITHMETIC);
	case '*':
	  atbanMetrics.times++;
	case '/':
	  return _ATOM(ARITHMETIC);
	case '=':
	  atbanMetrics.assignments++;
	  return _ATOM(ASSIGNMENT);
	/*
	Atoms we don't really know or distinct
	---
	Atomy, których nie znamy lub generalizujemy
	*/
	default:
	  return _ATOM(OTHER);
  }
  return _ATOM(IMPOSSIBLE);
}

int handle_token(int t)
{
  switch(t)
  {
    case ADDEQ:  /* "+=" */
    case SUBEQ:  /* "-=" */
    case MULEQ:  /* "*=" */
    case DIVEQ:  /* "/=" */
    case MODEQ:  /* "%=" */
	  atbanMetrics.assignments++;
	  return _ATOM(ASSIGNMENT);
    case EQ:  /* "==" */
    case NOTEQ:  /* "!=" */
    case LTEQ:  /* "<=" */
    case GTEQ:  /* ">=" */
	  return _ATOM(RELATION);
    case ANDAND:  /* "&&" */
    case OROR:  /* "||" */
	  return _ATOM(LOGIC);
    case PLUSPLUS:  /* "++" */
    case MINUSMINUS:  /* "--" */
      return _ATOM(ARITHMETIC);
    case ELSE:  /* "else" */
    case IF:  /* "if" */
    case WHILE:  /* "while" */
	  return _ATOM(CONTROL);

    case PRINT:  /* "print" */
    case INPUT:  /* "input" */
	  return t;

	default:
	  return _ATOM(OTHER);
  }
  return _ATOM(IMPOSSIBLE);
}

ATOM 
construct_atom(int type)
{
  ATOM atbanlval;
  atbanlval = calloc(1, sizeof(struct atom));
  atbanlval->content = strdup(atbantext);
  atbanlval->start   = offset;
  atbanlval->len     = yyleng;
  atbanlval->code    = type;
  atbanlval->line    = lineno;
  offset += yyleng;
  column += yyleng;
  return atbanlval;
}

void init_atbanlex()
{
  offset = 0;
  lineno = 1;
  column = 0;
  atbanId = new_unique_dictionary();
}

