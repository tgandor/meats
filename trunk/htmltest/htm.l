%{
#include <vector>
#include <string>
#include <cstring>
#include <cstdio>
#include <algorithm>
using namespace std;

vector<string> tagstack;
vector<int> linestack;
int lineNo = 1;
bool dbg = false;
bool quiet = false;
const char *legal[] =
{
"img",
"br",
"hr",
"input",
};
const char **legal_end = legal+(sizeof(legal)/sizeof(const char*));

int g_argc;
char **g_argv;

FILE *closeme = 0;
%}

%%

\n	++lineNo;

"<"[a-zA-Z1-6]+ { 
	tagstack.push_back(string(yytext+1, yytext+strlen(yytext))); 
	linestack.push_back(lineNo);
	if (dbg) printf("  (dbg) Line %d: <%s> opened\n", lineNo, tagstack.back().c_str()); 
}

"/>" { 
	if (tagstack.empty())
	{
		printf("  Line %d: misplaced self closing\n", lineNo);
	}
	else
	{
		if (dbg) printf("  (dbg) Line %d: <%s/> self-closed\n", lineNo, tagstack.back().c_str());
		tagstack.pop_back(); 
		linestack.pop_back();
	}
}

"</"[a-zA-Z1-6]+ { 
	if (dbg) printf("  (dbg) Line %d: </%s> closed\n", lineNo, yytext+2);
	if (tagstack.empty())
	{
		printf("  Line %d: no opening tag for </%s> found!\n", lineNo, yytext+2);
	}
	else if (strcmp(yytext+2, tagstack.back().c_str()) != 0)
	{
		while (!tagstack.empty() && find(legal, legal_end, tagstack.back()) != legal_end)
		{
			if (!quiet) printf("  Warn: discarding unclosed <%s> from line  %d\n", tagstack.back().c_str(), linestack.back());
			tagstack.pop_back();
			linestack.pop_back();
		}
		if (tagstack.empty())
		{
			printf("  Line %d: no opening tag for </%s> found!\n", lineNo, yytext+2);
		}
		else if (strcmp(yytext+2, tagstack.back().c_str()) == 0)
		{
			tagstack.pop_back();
			linestack.pop_back();
		}
		else
		{
			printf("  Line %d: </%s> closed, last == <%s> (line %d)\n", lineNo, yytext+2, 
				tagstack.back().c_str(), linestack.back());
		}
	}
	else
	{
		tagstack.pop_back();
		linestack.pop_back();
	}
}

. ;

%%

int yywrap()
{
	if (closeme) 
		fclose(closeme);
	if (!tagstack.empty())
	{
		puts("Error at EOF, unclosed tags:");
		for (int i = tagstack.size() - 1; i >= 0; --i)
			printf("  Line %d: %s\n", linestack[i], tagstack[i].c_str());
	}
	lineNo = 1;
	tagstack.clear();
	linestack.clear();
	switch (g_argc)
	{
	case -1:
		return 1;
	case 0:
		yyin = stdin;
		--g_argc;
		return 0;
	case 1:
		--g_argc;
	default:
		printf("--- Opening: %s ---\n", *g_argv);
		yyin = closeme = fopen( *g_argv++, "r" );
		if (!closeme)
		{
			fprintf(stderr, "Error opening file: %s\n", g_argv[-1]);
			exit(1);
		}
		--g_argc;
		return 0;
	}
}

int main( int argc, char **argv )
{
	g_argv = ++argv, g_argc = --argc;  /* skip over program name */
	if (argc > 0 && !strcmp("-d", *g_argv))
	{
		dbg = true;
		++g_argv, --g_argc;  /* skip over option */
	}
	if (argc > 0 && !strcmp("-q", *g_argv))
	{
		quiet = true;
		++g_argv, --g_argc;  /* skip over option */
	}
	yywrap();
	yylex();
	return 0;
}
