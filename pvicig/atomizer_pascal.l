%{

/* input-output routines */
#include <stdio.h>
/* strdup */
#include <string.h>

#include "main.h"
#include "atom.h"
#include "atom_codes.h"
#include "metrics.h"

/* 
Macro for distinction by another parser
---
Makro rozpoznawane przez parser getatoms
*/
#define _ATOM(name) name

#define YY_DECL ATOM yylex()

static int lineno=1;
static int offset;
static int column;

static ATOM construct_atom(int type);
static int handle_single_char(int c);
static int handle_token(int t);
static int decision; 

struct metrics atpasMetrics;
static UNIQUE_DICTIONARY atpasId; 

#define DECIDE(atom) { if((decision=handle_token(atom))!=-1) return construct_atom(decision); }

/* A couple of auxiliary functions */
static void skip_brace_comment();
static void skip_star_comment();

%}

NQUOTE [^']

%%

"AND"         DECIDE(_ATOM(AND));
"ARRAY"       DECIDE(_ATOM(ARRAY));
"CASE"        DECIDE(_ATOM(CASE));
"CONST"       DECIDE(_ATOM(CONST));
"DIV"         DECIDE(_ATOM(DIV));
"DO"          DECIDE(_ATOM(DO));
"DOWNTO"      DECIDE(_ATOM(DOWNTO));
"ELSE"        { atpasMetrics.else_keywords++; DECIDE(_ATOM(ELSE)); }
"FOR"         { atpasMetrics.for_keywords++; DECIDE(_ATOM(FOR)); }
"FORWARD"     DECIDE(_ATOM(FORWARD));  
"INLINE"      DECIDE(_ATOM(INLINE));
"FUNCTION"    DECIDE(_ATOM(FUNCTION));
"GOTO"        DECIDE(_ATOM(GOTO));
"IF"          { atpasMetrics.if_keywords++; DECIDE(_ATOM(IF)); }
"IN"          DECIDE(_ATOM(IN));
"LABEL"       DECIDE(_ATOM(LABEL));
"MOD"         DECIDE(_ATOM(MOD));
"NIL"         DECIDE(_ATOM(NIL));
"NOT"         DECIDE(_ATOM(NOT));
"OF"          DECIDE(_ATOM(OF));
"OR"          DECIDE(_ATOM(OR));
"XOR"	      DECIDE(_ATOM(XOR));
"OTHERWISE"   DECIDE(_ATOM(OTHERWISE));
"PACKED"      DECIDE(_ATOM(PACKED));
"BEGIN"       DECIDE(_ATOM(BEGN));
"END"         DECIDE(_ATOM(END));
"FILE"        DECIDE(_ATOM(PFILE));
"PROCEDURE"   DECIDE(_ATOM(PROCEDURE));
"PROGRAM"     DECIDE(_ATOM(PROGRAMKEWORD));
"RECORD"      DECIDE(_ATOM(RECORD));
"REPEAT"      { atpasMetrics.while_keywords++; DECIDE(_ATOM(REPEAT)); }
"SET"         DECIDE(_ATOM(SET));
"THEN"        DECIDE(_ATOM(THEN));
"TO"          DECIDE(_ATOM(TO));
"TYPE"        DECIDE(_ATOM(TYPE));
"UNTIL"       DECIDE(_ATOM(UNTIL));
"VAR"         DECIDE(_ATOM(VAR));
"WHILE"       { atpasMetrics.while_keywords++; DECIDE(_ATOM(WHILE)); } 
"WITH"        DECIDE(_ATOM(WITH));

"ORD"	DECIDE(_ATOM(ORD));
"USES"	DECIDE(_ATOM(USES));

"REAL"       DECIDE(_ATOM(BUILTINTYPE)); 
"EXTENDED"   DECIDE(_ATOM(BUILTINTYPE)); 
"INTEGER"    DECIDE(_ATOM(BUILTINTYPE)); 
"LONGINT"    DECIDE(_ATOM(BUILTINTYPE)); 
"BOOLEAN"    DECIDE(_ATOM(BUILTINTYPE)); 
"BYTE"       DECIDE(_ATOM(BUILTINTYPE)); 
"CHAR"       DECIDE(_ATOM(BUILTINTYPE)); 
"STRING"     DECIDE(_ATOM(BUILTINTYPE)); 
"ANSISTRING" DECIDE(_ATOM(BUILTINTYPE)); 
"POINTER"    DECIDE(_ATOM(BUILTINTYPE)); 


[a-zA-Z_]([a-zA-Z0-9_])* { atpasMetrics.identifiers++; unique_dictionary_add(atpasId, yytext); DECIDE(_ATOM(IDENTIFIER)); }
[0-9]+    DECIDE(_ATOM(DIGSEQ));

":="|"/=" { atpasMetrics.assignments++; DECIDE(_ATOM(ASSIGNMENT)); }
"+=" { atpasMetrics.assignments++; atpasMetrics.plus++; DECIDE(_ATOM(ASSIGNMENT)); }
"*=" { atpasMetrics.assignments++; atpasMetrics.times++; DECIDE(_ATOM(ASSIGNMENT)); }
"-=" { atpasMetrics.assignments++; atpasMetrics.minus++; DECIDE(_ATOM(ASSIGNMENT)); }

'[^']*'	DECIDE(_ATOM(STRINGLIT));

[-:,.=>\[(<\]+);/*^] { 
   decision = handle_single_char (*yytext);
   if (decision != -1)
     return construct_atom(decision); 
} 

".."    DECIDE(_ATOM(DOTDOT));
"<="    DECIDE(_ATOM(LE));
">="    DECIDE(_ATOM(GE));
"<>"    DECIDE(_ATOM(NOTEQUAL));
"<<"    DECIDE(_ATOM(SL));
">>"    DECIDE(_ATOM(SR));
"**"    DECIDE(_ATOM(STARSTAR));

[0-9]+"."[0-9]+(e[+-]?[0-9]+)?   DECIDE(_ATOM(REALNUMBER));
[0-9]+e[+-]?[0-9]+   DECIDE(_ATOM(REALNUMBER));

"(*"  skip_star_comment();
"{"   skip_brace_comment();

"//"        { offset+=2; while (input() != '\n') ++offset; lineno++; column=0; }
"\n"|"\r\n" { lineno++; offset+=yyleng; column=0; }
[ \t\f]+    { offset+=yyleng; column+=yyleng; }    

<<EOF>> { 
  atpasMetrics.lines=lineno; 
  atpasMetrics.unique_ids = atpasId->count;
  free_unique_dictionary(atpasId);
  free(atpasId);
  return (ATOM)0; 
}

.    { fprintf (stderr, _("'%c' (%d) illegal charcter at line %d\n"), *yytext, *yytext, lineno); }

%%

int
yywrap ()
{
  return 1;
}

static void skip_brace_comment()
{
  int c;
  while (c = input())
  {
    offset++;
	column++;
    if (c == '}')
      break;
    else if (c == '\n')
	{
      lineno++;
	  column = 0;
	}
  }
  if (!c)
  {
    fprintf (stderr, _("unexpected EOF inside comment at line %d\n"), lineno);
    exit (1);
  }
}

static void skip_star_comment()
{
	int c1, c2;

	offset += 2;  // for the (*
	column += 2;  // znaki (*

	c1 = input();
	c2 = input();
  
	while (c2 != EOF && !(c1 == '*' && c2 == ')')) 
	{
		if (c1 == '\n') 
		{
			++lineno;
			column = 0;
		}
		else
		    ++column;
		++offset;
		c1 = c2;
		c2 = input();
	}
	++column;
	++offset;
}

/*
Filter single-character tokens and return them as symbolic names
---
Filtrowanie tokenów, które s± jednoznakowe i zwracanie ich jako kodów symbolicznych
*/
int handle_single_char(int c)
{
  offset ++;
  column ++;
  switch(c)
  {
  /* 
	Atoms which are not interesting 
	---
	Atomy, które nie s± ciekawe
	*/ 
	case ';': 
	  atpasMetrics.semicolons++;
    case ',':    /*  COMMA  */
    case ':':    /*  COLON  */
	  return -1;
	/*
	Interesting atoms
	---
	Atomy, które s± ciekawe
	*/
    case '^':    /*  UPARROW  */
    case '.':    /*  DOT  */
	  return _ATOM(SELECTOR);
    case '=':    /*  EQUAL  */
    case '>':    /*  GT  */
    case '<':    /*  LT  */
	  return _ATOM(RELATION);
    case '[':    /*  LBRAC  */
    case ']':    /*  RBRAC  */
    case '(':    /*  LPAREN  */
    case ')':    /*  RPAREN  */
	  return _ATOM(BRACKET);
    case '+':    /*  PLUS  */
	  atpasMetrics.plus++;
	  return _ATOM(ARITHMETIC);
    case '-':    /*  MINUS  */
	  atpasMetrics.minus++;
	  return _ATOM(ARITHMETIC);
    case '*':    /*  STAR  */
	  atpasMetrics.times++;
    case '/':    /*  SLASH  */
	  return _ATOM(ARITHMETIC);
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
  offset += yyleng;
  column += yyleng;
  switch(t)
  {
    case CASE:
    case OTHERWISE:
    case IF:
    case THEN:
    case ELSE:
    case FOR:
    case TO:
    case DOWNTO:
    case REPEAT:
    case UNTIL:
    case WHILE:
    case DO:
    case GOTO:
      return _ATOM(CONTROL);

    case ORD:
    case MOD:
    case DIV:
    case SL:        /*   "<<"    */
    case SR:        /*   ">>"    */
    case STARSTAR:  /*   "**"    */
	  return _ATOM(ARITHMETIC);

    case AND:
    case OR:
    case XOR:
    case NOT:
	  return _ATOM(LOGIC);
	  
    case USES:
	  return _ATOM(OTHER);
    case NIL:
      return _ATOM(INTEGER);

    case LE:        /*   "<="    */
    case GE:        /*   ">="    */
    case NOTEQUAL:  /*   "<>"    */
    case IN:
	  return _ATOM(RELATION);
	  
    case RECORD:
    case ARRAY:
    case SET:
	case PFILE:
	  return _ATOM(BUILTINTYPE);
	/*
	Tokens to be filtered out 
	---
	Tokeny do odfiltrowania
	*/
    case OF:
    case WITH:
    case CONST:
    case VAR:
    case TYPE:
    case DOTDOT:    /*   ".."    */
    case LABEL:
    case PACKED:
    case PROCEDURE:
    case FORWARD:
    case INLINE:
    case FUNCTION:
    case PROGRAMKEWORD:
	  return -1;
	default:
	  return t;
  }
  return _ATOM(IMPOSSIBLE);
}

ATOM 
construct_atom(int type)
{
  ATOM ret_atom;
  ret_atom = calloc(1, sizeof(struct atom));
  ret_atom->content = strdup(yytext);
  ret_atom->start   = offset - yyleng;
  ret_atom->len     = yyleng;
  ret_atom->code    = type;
  ret_atom->line    = lineno;
  return ret_atom;
}

void init_atpaslex()
{
  offset = 0;
  lineno = 1;
  column = 0;
  atpasId = new_unique_dictionary();
}

