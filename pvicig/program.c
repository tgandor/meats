#include "program.h"

/*
 * A dummy metrics structure for initializing
 * --- 
 *  Pomocnicza struktura do inicjalizacji (zerami)
 */
static struct metrics emptyMetrics;

int has_suffix(char *str, char *suffix)
{
  if( strlen(str) < strlen(suffix) )
    return 0;
  return !strcasecmp(str+strlen(str)-strlen(suffix), suffix);
}

enum program_type identify_program(char *filename)
{
  if (has_suffix(filename, ".ban"))
    return BANAL;
  if (has_suffix(filename, ".c"))
    return C;
  if (has_suffix(filename, ".cpp"))
    return C;
  if (has_suffix(filename, ".pas"))
    return PASCAL;
    /* Not a supported programming language */
  return NONE;
}

PROGRAM new_program(char *filename)
{
  FILE *input;
  PROGRAM result = calloc(1, sizeof(*result));
  /* 
   * Identify the kind of source 
   * --- 
   *  Identyfikacja rodzaju programu
   */
  result->kind = identify_program(filename);
  if (!result->kind)
  {
    free(result);
    return NULL;
  }
  /* 
   * Load the source into memory 
   * ---
   *  Wczytanie ¼ród³a do pamiêci
   */
  result->filename = strdup(filename);
  input = fopen(filename, "r");
  if (!input) 
  {
    free(result);
    return NULL;
  }
  afgettoch(&(result->source), input, '\0');
  fclose(input);
  return result;
}

/*
 * Free memeory resources occupied by program
 * ---
 *  Zwalnia pamiêæ zajmowan± przez program
 */
void free_program(PROGRAM prog)
{
  free(prog->filename);
  free(prog->source);
}

void output_program(PROGRAM prog)
{
  int i;
  if (!prog)
  {
    puts(_("No program - null pointer"));
    return;
  }
  
  puts(_("Program contents:"));
  printf(_("Filename: %s\n"), prog->filename);
  if ( output_source )
  {
    puts(_("--------- begin source ------------"));
    puts(prog->source);
    puts(_("---------- end source -------------"));
  }
  if ( use_metric != 2)
  {
    printf(_("Number of lexical atoms: %d\n"), prog->num_lex_atoms);
    if(verbose_flag)
      for(i=0; i<prog->num_lex_atoms; i++)
        atom_info(prog->lex_atoms[i]);
  }
  if ( use_metric )
  {
    printf(_("Metrics values (as they follow, for reference read metrics.h):\n"));
    for(i=0; i < sizeof(struct metrics) / sizeof(int); i++)
      printf("%d ", *((int*)&prog->theMetrics + i));
    printf("\n"); 
  }
}

int process_program(PROGRAM prog)
{
  if (verbose_flag)
    printf(_("Processing program %s...\n"), prog->filename);
  /* Potential preparation of special - eg. C - source */
  if (prog->kind == C && use_cpp)  
  {
    trim_directives_from(&(prog->source));
    preprocess_from(&(prog->source));
    trim_directives_from(&(prog->source));
	babble(_("File preprocessed."));
  }
  /* 
   * Lexical analysis for atoms 
   * ---
   *  Analiza leksykalna atomów
   */
  if (prog->kind == C)
  { 
    ATOM a;
    FILE *atom_out;
    atcin = (FILE*) fmemopen(prog->source, strlen(prog->source), "r");
    atom_out = (FILE*) open_memstream(&prog->lex_atoms, &prog->num_lex_atoms);
	init_atclex();
	atcMetrics = emptyMetrics;
    while ( a = atclex()) 
    {
      fwrite(&a, sizeof(ATOM), 1, atom_out);
    }
    fclose(atcin);
    fclose(atom_out);
    /*
    Convert size in bytes to count of atom pointers
    ---
    Zamiana rozmiaru w bajtach na liczbê wska¼nikow
    */
    prog->num_lex_atoms /= sizeof(ATOM); 
	prog->theMetrics = atcMetrics;
  }
  else if (prog->kind == BANAL)
  {
    ATOM a;
    FILE *atom_out;
    atbanin = (FILE*) fmemopen(prog->source, strlen(prog->source), "r");
    atom_out = (FILE*) open_memstream(&prog->lex_atoms, &prog->num_lex_atoms);
	init_atbanlex();
	atbanMetrics = emptyMetrics;
    while ( a = atbanlex()) 
    {
      fwrite(&a, sizeof(ATOM), 1, atom_out);
      // printf("%s - code %3d - type %s\n", a->content, a->code, atom_names[a->code]);
    }
    fclose(atbanin);
    fclose(atom_out);
    /*
    Convert size in bytes to count of atom pointers
    ---
    Zamiana rozmiaru w bajtach na liczbe wskaznikow
    */
    prog->num_lex_atoms /= sizeof(ATOM); 
	prog->theMetrics = atbanMetrics;
  }
  else if (prog->kind == PASCAL)
  {
    ATOM a;
    FILE *atom_out;
    atpasin = (FILE*) fmemopen(prog->source, strlen(prog->source), "r");
    atom_out = (FILE*) open_memstream(&prog->lex_atoms, &prog->num_lex_atoms);
	init_atpaslex();
	atpasMetrics = emptyMetrics;
    while ( a = atpaslex()) 
    {
      fwrite(&a, sizeof(ATOM), 1, atom_out);
    }
    fclose(atpasin);
    fclose(atom_out);
    /*
    Convert size in bytes to count of atom pointers
    ---
    Zamiana rozmiaru w bajtach na liczbe wskaznikow
    */
    prog->num_lex_atoms /= sizeof(ATOM); 
	prog->theMetrics = atpasMetrics;
  }
  
  babble(_("Processed."));
  return 1;
}

