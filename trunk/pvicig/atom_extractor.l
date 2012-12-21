%{
#include "unique_dictionary.h"
void add_atom();

struct unique_dictionary atomdict;

%}

%x atom

%%

"_ATOM("         BEGIN(atom);
<atom>[A-Z]+     unique_dictionary_add(&atomdict, yytext);
<atom>")"        BEGIN(INITIAL);
<*>.                ;
<*>"\n"             ;

%%

int main(int argc, char **argv)
{
  DICTIONARY_ENTRY iter;
  int i;
  int c;
  FILE *h_out, *c_out, *temp;
  int close_c=0, close_h=0;
  /*
  process options
  ---
  przetwarzanie opcji
  */
  while ((c = getopt(argc, argv, "C:H:")) != -1)
  {
    switch(c)
	{
	case 'C':
	  temp = fopen(optarg, "w");
	  if (temp)
	  {
	    c_out=temp;
		close_c=1;
	  }
	  break;
	case 'H':
	  temp = fopen(optarg, "w");
	  if (temp)
	  {
	    h_out=temp;
		close_h=1;
	  }
	  break;
	case '?':
	  fprintf(stderr, "Ignored some option... (%c)\n", optopt);
	  break;
	}
  }
  
  for (i=optind; i<argc; i++) 
  {
    if ( yyin = fopen(argv[i], "r") ) 
	{
      yylex();
	  fclose(yyin);
	}
  }
  if (atomdict.entries)
  {
    /* Header file */
	if (close_h)
	  fprintf(h_out, "#ifndef _INC_ATOM_CODES_H\n#define _INC_ATOM_CODES_H\n");
    fprintf(h_out, "enum atoms \n{\n");
    fprintf(h_out, "  %s,\n", atomdict.entries->word);
	iter = atomdict.entries->next;
	while (iter)
	{
      fprintf(h_out, "  %s,\n", iter->word);
	  iter = iter->next;
	}
	fprintf(h_out, "};\n");
	fprintf(h_out, "\nextern const char *atom_names[];\n");
	if(close_h)
	  fprintf(h_out, "\n#endif\n");
	
	/* C file */
	fprintf(c_out, "\nconst char *atom_names[] = \n{\n");
    fprintf(c_out, "  \"%s\",\n", atomdict.entries->word);
	iter = atomdict.entries->next;
	while (iter)
	{
      fprintf(c_out, "  \"%s\",\n", iter->word);
	  iter = iter->next;
	}
	fprintf(c_out, "};\n");
  }
  if (close_h)
    fclose(h_out);
  if (close_c)
    fclose(c_out);

  return 0;
}

int yywrap()
{
  return 1;
}

