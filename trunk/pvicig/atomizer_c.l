%{

#include <stdio.h>
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

static int lineno;
static int offset;
static int column;

static void skip_comment();
static ATOM construct_atom(int type);
static int handle_single_char(int c);
static int handle_token(int t);
static int decision;

struct metrics atcMetrics;
static UNIQUE_DICTIONARY atcId; 

#define DECIDE(atom) { if((decision=handle_token(atom))!=-1) return construct_atom(decision); }

%}

intsuffix				[uU]?[lL]*
floatsuffix				[fF]
fracconst				([0-9]*\.[0-9]+)|([0-9]+\.)
exppart					[eE][-+]?[0-9]+
chartext				([^'])|(\\.)
stringtext				([^"])|(\\.)

%%

"\n"					{ ++lineno; ++offset; column=0; }
[\t\f\v\r ]+			{ offset += yyleng; column += yyleng; }
[-;,=/%?~&|()\+{}]		{ 
   decision = handle_single_char (*yytext);
   if (decision != -1)
     return construct_atom(decision); 
} 

"/*" { skip_comment(); }
"#"  { ++offset; do decision = input(), offset++; while (decision != '\n'); lineno++; column=0; }
"//" { offset+=2; do decision = input(), offset++; while (decision != '\n'); lineno++; column=0; }

[-{}\]\[();:?.+*/%^&|~!=<>,] handle_single_char(*yytext);

"..."					DECIDE(_ATOM(ELLIPSIS));
"+="					DECIDE(_ATOM(ADDEQ));
"-="					DECIDE(_ATOM(SUBEQ));
"*="					DECIDE(_ATOM(MULEQ));
"/="					DECIDE(_ATOM(DIVEQ));
"%="					DECIDE(_ATOM(MODEQ));
"^="					DECIDE(_ATOM(XOREQ));
"&="					DECIDE(_ATOM(ANDEQ));
"|="					DECIDE(_ATOM(OREQ));
"<<"					DECIDE(_ATOM(SL));
">>"					DECIDE(_ATOM(SR));
"<<="					DECIDE(_ATOM(SLEQ));
">>="					DECIDE(_ATOM(SREQ));
"=="					DECIDE(_ATOM(EQ));
"!="					DECIDE(_ATOM(NOTEQ));
"<="					DECIDE(_ATOM(LTEQ));
">="					DECIDE(_ATOM(GTEQ));
"&&"					DECIDE(_ATOM(ANDAND));
"||"					DECIDE(_ATOM(OROR));
"++"					DECIDE(_ATOM(PLUSPLUS));
"--"					DECIDE(_ATOM(MINUSMINUS));
"->"					DECIDE(_ATOM(ARROW));

"auto"					DECIDE(_ATOM(AUTO));
"break"					DECIDE(_ATOM(BREAK));
"case"					DECIDE(_ATOM(CASE));
"char"					DECIDE(_ATOM(CHAR));
"const"					DECIDE(_ATOM(CONST));
"continue"				DECIDE(_ATOM(CONTINUE));
"default"				DECIDE(_ATOM(DEFAULT));
"do"					DECIDE(_ATOM(DO));
"double"				DECIDE(_ATOM(DOUBLE));
"else"					{ atcMetrics.else_keywords++; DECIDE(_ATOM(ELSE)); }
"enum"					DECIDE(_ATOM(ENUM));
"extern"				DECIDE(_ATOM(EXTERN));
"float"					DECIDE(_ATOM(FLOAT));
"for"					{ atcMetrics.for_keywords++; DECIDE(_ATOM(FOR)); }
"goto"					DECIDE(_ATOM(GOTO));
"if"					{ atcMetrics.if_keywords++; DECIDE(_ATOM(IF)); }
"int"					DECIDE(_ATOM(INT));
"long"					DECIDE(_ATOM(LONG));
"register"				DECIDE(_ATOM(REGISTER));
"return"				DECIDE(_ATOM(RETURN));
"short"					DECIDE(_ATOM(SHORT));
"signed"				DECIDE(_ATOM(SIGNED));
"sizeof"				DECIDE(_ATOM(SIZEOF));
"static"				DECIDE(_ATOM(STATIC));
"struct"				DECIDE(_ATOM(STRUCT));
"switch"				DECIDE(_ATOM(SWITCH));
"typedef"				DECIDE(_ATOM(TYPEDEF));
"union"					DECIDE(_ATOM(UNION));
"unsigned"				DECIDE(_ATOM(UNSIGNED));
"void"					DECIDE(_ATOM(VOID));
"volatile"				DECIDE(_ATOM(VOLATILE));
"while"					{ atcMetrics.while_keywords++;  DECIDE(_ATOM(WHILE)); }

[a-zA-Z_][a-zA-Z_0-9]*	 { atcMetrics.identifiers++; unique_dictionary_add(atcId, yytext); DECIDE(_ATOM(IDENTIFIER)); }

"0"[xX][0-9a-fA-F]+{intsuffix}?		DECIDE(_ATOM(INTEGER));
"0"[0-7]+{intsuffix}?			DECIDE(_ATOM(INTEGER));
[0-9]+{intsuffix}?			DECIDE(_ATOM(INTEGER));

{fracconst}{exppart}?{floatsuffix}?	DECIDE(_ATOM(FLOATING));
[0-9]+{exppart}{floatsuffix}?		DECIDE(_ATOM(FLOATING));

"'"{chartext}*"'"			DECIDE(_ATOM(CHARACTER));
"L'"{chartext}*"'"			DECIDE(_ATOM(CHARACTER));

"\""{stringtext}*"\""			DECIDE(_ATOM(STRING));
"L\""{stringtext}*"\""			DECIDE(_ATOM(STRING));

<<EOF>> { 
  atcMetrics.lines=lineno; 
  atcMetrics.unique_ids = atcId->count;
  free_unique_dictionary(atcId);
  free(atcId);
  return (ATOM)0; 
}

.					{ fprintf(stderr, _("%d: unexpected character `%c'\n"), lineno, yytext[0]); }

%%

int
yywrap()
{
	return 1;
}

/*
 * Skip the comment - manually without matching
 * ---
 * Pominiêcie komentarza bez stosowania DAS
 */
static void
skip_comment()
{
	int c1, c2;

	offset += 2;  // for the /*
	column += 2;  // znaki /*

	c1 = input();
	c2 = input();
  
	while (c2 != EOF && !(c1 == '*' && c2 == '/')) 
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
	  atcMetrics.semicolons++;
	case ',':
	  return -1;
	/*
	Interesting atoms
	---
	Atomy, które s± ciekawe
	*/
	case '[': 
	case ']': 
	case '(': 
	case ')': 
	  return _ATOM(BRACKET);
	case '.': 
	  return _ATOM(SELECTOR);
	case '{': 
	  return _ATOM(BEGN);
	case '}': 
	  return _ATOM(END);
	case '+': 
	  atcMetrics.plus++;
	  return _ATOM(ARITHMETIC);
	case '-': 
	  atcMetrics.minus++;
	  return _ATOM(ARITHMETIC);
	case '*': 
	  atcMetrics.times++;
	case '/': 
	case '%': 
	  return _ATOM(ARITHMETIC);
	case '^': 
	case '&': 
	case '|': 
	case '~': 
	  return _ATOM(BITWISE);
	case '!': 
	case '?': 
	case ':': 
	  return _ATOM(LOGIC);
	case '<': 
	case '>': 
	  return _ATOM(RELATION);
	case '=': 
	  atcMetrics.assignments++;
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
  offset += yyleng;
  column += yyleng;
  switch(t)
  {
    case ADDEQ:  /* "+=" */
	  atcMetrics.plus++;
	  atcMetrics.assignments++;
	  return _ATOM(ASSIGNMENT);
    case SUBEQ:  /* "-=" */
	  atcMetrics.minus++;
	  atcMetrics.assignments++;
	  return _ATOM(ASSIGNMENT);
    case MULEQ:  /* "*=" */
	  atcMetrics.assignments++;
	  atcMetrics.times++;
	  return _ATOM(ASSIGNMENT);
    case DIVEQ:  /* "/=" */
    case MODEQ:  /* "%=" */
    case XOREQ:  /* "^=" */
    case ANDEQ:  /* "&=" */
    case OREQ:   /* "|=" */
	  atcMetrics.assignments++;
	  return _ATOM(ASSIGNMENT);
    case SL:     /* "<<" */
    case SR:     /* ">>" */
    case SLEQ:   /* "<<=" */
    case SREQ:   /* ">>=" */
	  return _ATOM(BITWISE);
    case ANDAND: /* "&&" */
    case OROR:   /* "||" */
	  return _ATOM(LOGIC);
    case PLUSPLUS:   /* "++" */
    case MINUSMINUS: /* "--" */
    case SIZEOF:     /* "sizeof" */
	  return _ATOM(ARITHMETIC);
    case ARROW:      /* "->" */
	  return _ATOM(SELECTOR);

    case FOR:       /* "for" */
    case CONTINUE:  /* "continue" */
    case GOTO:      /* "goto" */
    case IF:        /* "if" */
    case ELSE:      /* "else" */
    case WHILE:     /* "while" */
    case DO:        /* "do" */
    case SWITCH:    /* "switch" */
    case CASE:      /* "case" */
    case BREAK:     /* "break" */
    case DEFAULT:   /* "default" */
    case RETURN:    /* "return" */
	  return _ATOM(CONTROL);
	  
    case CHAR:    /* "char" */
    case FLOAT:   /* "float" */
    case DOUBLE:  /* "double" */
    case INT:     /* "int" */
    case LONG:    /* "long" */
	  return _ATOM(BUILTINTYPE);
    case TYPEDEF: /* "typedef" */
    case UNION:   /* "union" */
    case ENUM:    /* "enum" */
    case STRUCT:  /* "struct" */
	  return _ATOM(DECL);

    case EQ:     /* "==" */
    case NOTEQ:  /* "!=" */
    case LTEQ:   /* "<=" */
    case GTEQ:   /* ">=" */
	  return _ATOM(RELATION);
	/*
	Tokens to be filtered out 
	---
	Tokeny do odfiltrowania
	*/
    case SHORT:     /* "short" */
    case SIGNED:    /* "signed" */
    case STATIC:    /* "static" */
    case UNSIGNED:  /* "unsigned" */
    case ELLIPSIS:  /* "..." */
    case AUTO:      /* "auto" */
    case EXTERN:    /* "extern" */
    case VOLATILE:  /* "volatile" */
    case REGISTER:  /* "register" */
    case VOID:      /* "void" */
    case CONST:     /* "const" */
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
  /*
  offset already updated by handle_token
  ---
  offset zosta³ ju¿ zmodyfikowany w funkcji handle_token
  */
  ret_atom->start   = offset - yyleng; 
  ret_atom->len     = yyleng;
  ret_atom->code    = type;
  ret_atom->line    = lineno;
  return ret_atom;
}

void init_atclex()
{
  offset = 0;
  lineno = 1;
  column = 0;
  atcId = new_unique_dictionary();
}

