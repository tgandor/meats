%{
#include <vector>
#include <string>
#include <cstring>
#include <cstdio>
using namespace std;

vector<string> tagstack;
int lineNo = 1;
bool dbg = false;
%}

%%

\n	++lineNo;

"<"[a-zA-Z1-6]+ { 
	tagstack.push_back(string(yytext+1, yytext+strlen(yytext))); 
	if (dbg) printf("Line %d: tag %s opened\n", lineNo, tagstack.back().c_str()); 
}

"/>" { 
	if (dbg) printf("Line %d: tag %s self-closed\n", lineNo, tagstack.back().c_str());
	tagstack.pop_back(); 
}

"</"[a-zA-Z1-6]+ { 
	if (dbg) printf("Line %d: tag %s closed, last == %s\n", lineNo, yytext+2, tagstack.back().c_str());
	if (strcmp(yytext+2, tagstack.back().c_str()) != 0)
	{
		printf("Line %d: tag %s closed, last == %s\n", lineNo, yytext+2, tagstack.back().c_str());
	}
	tagstack.pop_back();
}

<<EOF>> {
	if (!tagstack.empty())
	{
		puts("Error at EOF, unclosed tags:");
		for (int i = tagstack.size() - 1; i >= 0; --i)
			puts(tagstack[i].c_str());
	}
	return yywrap();
}
. ;

%%

// some shabby main from the internet

int main( int argc, char **argv )
{
	++argv, --argc;  /* skip over program name */
	if (argc > 0 && !strcmp("-d", *argv))
	{
		dbg = true;
		++argv, --argc;  /* skip over option */
	}
	if ( argc > 0 )
		yyin = fopen( argv[0], "r" );
	else
		yyin = stdin;
	yylex();
	return 0;
}
