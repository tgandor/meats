/* 
  pvicig -- compare programs' source codes to detect copies 
  Copyright (C) 2006 Tomasz Gandor

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
    
    ---------------------------------

  pvicig -- porównuje teksty ¼ród³owe programów i okre¶la ich podobieñstwo
  Copyright (C) 2006 Tomasz Gandor

    Niniejszy program jest wolnym oprogramowaniem; mo¿esz go
    rozprowadzaæ dalej i/lub modyfikowaæ na warunkach Powszechnej
    Licencji Publicznej GNU, wydanej przez Fundacjê Wolnego
    Oprogramowania - wed³ug wersji 2 tej Licencji lub (wed³ug twojego
    wyboru) której¶ z pó¼niejszych wersji.

    Niniejszy program rozpowszechniany jest z nadziej±, i¿ bêdzie on
    u¿yteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domy¶lnej
    gwarancji PRZYDATNO¦CI HANDLOWEJ albo PRZYDATNO¦CI DO OKRE¦LONYCH
    ZASTOSOWAÑ. W celu uzyskania bli¿szych informacji siêgnij do
    Powszechnej Licencji Publicznej GNU.

    Z pewno¶ci± wraz z niniejszym programem otrzyma³e¶ te¿ egzemplarz
    Powszechnej Licencji Publicznej GNU (GNU General Public License);
    je¶li nie - napisz do Free Software Foundation, Inc., 59 Temple
    Place, Fifth Floor, Boston, MA  02110-1301  USA
    
*/


/*
 * The headers, defines, includes are all in one file 
 * ---
 *  Wszystkie nag³ówki, makrodefinicje i tym podobne w osobnym pliku
 */
#include "main.h"

/* --------------------------------------
 * Variables
 * --
 *  Zmienne 
 ----------------------------------------*/

/* 
  The name this program was run with. 
  ---
  Nazwa, z któr± program zosta³ uruchomiony
*/
static const char *program_name;

/* 
  If nonzero, display usage information and exit.  
  ---
  Flaga wymuszaj±ca wypisanie pomocy do programu
*/
static int show_help = 0;

/* 
  If nonzero, print the version on standard output and exit.  
  ---
  Flaga wymuszaj±ca wypisanie informacji o wersji
*/
static int show_version = 0;

/*
  Increases amount of output data 
  --- 
  Zwiêksza ilo¶æ wypisywanych informacji
*/
int verbose_flag = 0;

/* 
  Decreases amount of output data (e.g. errors)
  --- 
  Zmniejsza ilo¶æ wypisywanych informacji (diagnostycznych)
*/
int quiet_flag = 0;

/*
 * Karp-Rabin hashing parameters
 * ---
 *  Parametry funkcji haszuj±cej do algorytmu Karpa-Rabina
 */
int KR_base      =   DEFAULT_KR_BASE;
int KR_modulus   =   DEFAULT_KR_MODULUS;

int GST_initial  =   DEFAULT_GST_INITIAL;
int GST_shortest =   DEFAULT_GST_SHORTEST;

int use_metric   = 0;
int zeros_matter = 0;
int use_cpp      = 0;

int output_source = 0;
int sort_asc      = 0;

/* 
  Long and short options 
  ---
  Opcje programu w formacie d³ugim i krótkim
*/
enum optcodes {
	GST_START = 500,
	GST_MIN,
	KR_BASE,
	KR_MOD,
	THERESHOLD
};

static const struct option long_options[] =
{
  {"version",   no_argument,       &show_version,  1  },
  {"help",      no_argument,       &show_help,     1  },
  {"quiet",     no_argument,       NULL,          'q' },
  {"verbose",   no_argument,       NULL,          'v' },
  {"output",    required_argument, NULL,          'o' },
  {"indicate",  required_argument, NULL,          'i' },
  {"gst-start", required_argument, NULL,    GST_START },
  {"gst-min",   required_argument, NULL,    GST_MIN   },
  {"kr-base",   required_argument, NULL,    KR_BASE   },
  {"kr-mod",    required_argument, NULL,    KR_MOD    },
  {"thereshold",required_argument, NULL,    THERESHOLD},
  {"metrics",   no_argument,       &use_metric,    1  },
  {"only-metrics", no_argument,    &use_metric,    2  },
  {"zero-same", no_argument,       &zeros_matter,  1  },
  {"use-cpp",   no_argument,       &use_cpp,       1  },
  {"source",    no_argument,       &output_source, 1  },
  {"sort-asc",  no_argument,       &sort_asc,      1  },
  {0, 0, 0, 0},
};
static char opt_str[] = "qvo:i:t:";

int 
report(char *error)
{
  if(!quiet_flag)
    fprintf(stderr, "\t%s\n", error);
  return 0;
}

int 
babble(char *message)
{
	if(verbose_flag)
		fprintf(stderr, "%s\n", message);
	return 1;
}

int
check_gst_params()
{
	if ( GST_shortest < 2 ) 
	{
		report(_("Too short minimal match length."));
		if ( GST_initial >= 2 * DEFAULT_GST_SHORTEST )
			return 1;
		return 2;
	}
	if(GST_initial < GST_shortest) 
	{
		report(_("Wrong Greedy String Tiling parameters."));
		return 3;
	}
	return 0;
}

int
check_kr_params()
{
  if(KR_base < 2)
	  return report(_("Too low Karp Rabin base."));
  if(KR_modulus < 7)
	  return report(_("Too low Karp Rabin modulus."));
  if(!is_prime(KR_modulus))
	  return report(_("Karp Rabin modulus must be prime."));
  if(!is_prime(KR_base))
	  return report(_("We want Karp Rabin base to be prime too."));
  if( ((long long) KR_base + 1) * KR_modulus > (long long) INT_MAX )
	  return report(_("Too large Karp Rabin parameters (overflow)."));
  return 1;
}

static void 
usage()
{
  printf(_("\
`%s' - copy detection program\n\
"), PACKAGE);
  printf(_("\
\n\
Usage: %s [OPTION]... ARGUMENTS\n"), program_name);
  fputs(_("\
\n\
If a long option shows an argument as mandatory, then it is mandatory\n\
for the equivalent short option also.  Similarly for optional arguments.\n\
"), stdout);
  fputs(_("\
\n\
General Options:\n\
  -q, --quiet               supress errors, warnings and excess information\n\
  -v, --verbose             output more detailed information\n\
  -i, --indicate=FILENAME   compare this file aganist all other arguments only\n\
  -o, --output=FILENAME     redirect stdout to file FILENAME\n\
      --version             print version and exit\n\
      --help                display this help message\n\
\n\
Algorithm Options:\n\
  -t, --thereshold=VALUE    only display comparisons which yield more than VALUE %\n\
      --gst-start=VALUE     for GST algorithm: initial search length\n\
      --gst-min=VALUE       minimal (final) tile length in GST algorithm\n\
      --kr-base=VALUE       the Karp Rabin multiplier\n\
      --kr-mod=VALUE        the Karp Rabin modulus\n\
      --metrics             use also atribute counting metric\n\
      --only-metrics        use only atribute counting metric\n\
      --zero-same           when comparing metrics, don't ignore zeros\n\
      --use-cpp             preprocess C files wich cpp before processing\n\
      --source              display source in verbose mode when displaying program\n\
      --sort-asc            sort results ascending (default: sort descending\n\
"), stdout);
  fputs(_("\
\n\
Report bugs to: <Tomasz.Gandor@gmail.com>\n\
"), stdout);
}

int
main (int argc, char *const *argv)
{
  /*
   * Iterators, indexes, counters
   * ---
   *  Zmienne pomocnicze, steruj±ce
   */
  int i,j;
  int program_count, temp_count;
  DICTIONARY_ENTRY iter;
  
  /* 
  option character 
  ---
  zdekodowany symbol opcji
  */
  int option_char;

  /*
  flag - if set we only compare the input files against the indicated source
  ---
  flaga - gdy ustawiona porównujemy tylko z wskazanym programem
  */
  int one_suspect = 0;
  
  /*
  a vector of programs to process
  ---
  tablica programów do przetworzenia
  */
  PROGRAM *programs, *temp_programs, suspect_program=NULL;

  /*
  a data structure to store filenames and make them unique
  ---
  struktura danych do przechowywania nazw plików
  */
  UNIQUE_DICTIONARY filenames;
  char *suspect_filename;
  
  /*
  an array of pointers to a comparison structure
  ---
  tablica wska¼ników do struktury opisuj±cej porównanie programów
  */
  COMPARISON *comparisons;
  int comparison_count;

  /*
  a minimal value of simmilarity to be shown in results
  ---
  minimalny poziom podobieñstwa do wy¶wietlenia w wynikach
  */
  double thereshold = 0.5;

  /*
  adjust locale - for messages in many languages
  ---
  ustawienia lokalne - komunikaty w wielu jêzykach
  */

  setlocale(LC_ALL, "");
  bindtextdomain(PACKAGE, LOCALEDIR);
  textdomain(PACKAGE);
  
  /*
  decode program options with getopt_long
  ---
  przeanalizowanie opcji programu funkcj± getopt_long
  */
  while ( (option_char = getopt_long (argc, argv, opt_str,
     long_options, NULL)) != EOF) 
  {
    // printf(_("Seen option: %d (%c)\n"), option_char, option_char>0 ? option_char : '?');
    switch(option_char)
    {
    case 'v':
      verbose_flag = 1;
      break;
    case 'q':
      quiet_flag = 1;
      break;
    case 'i':
      one_suspect = 1;
      suspect_filename = optarg;
      break;
	case GST_MIN:
	  GST_shortest = atoi(optarg);
	  break;
	case GST_START:
	  GST_initial = atoi(optarg);
	  break;
	case KR_MOD:
	  KR_modulus = atoi(optarg);
	  break;
	case KR_BASE:
	  KR_base = atoi(optarg);
	  break;
	case THERESHOLD:
	case 't':
	  thereshold = atof(optarg)/100;
	  if (thereshold < 0)
		  thereshold = 0;
	  if (thereshold > 1)
		  thereshold = .99;
	  break;
	case 'o':
	  if ( !freopen(optarg, "w", stdout) )
	  {
		  exit( EXIT_FAILURE );
	  }
	  break;
    default:
      break;
    }
  }
  
  /*
  Handle trivial options
  ---
  Obs³uga prostych opcji
  */
  program_name = argv[0];
  if (show_help)
  {
    usage();
    return EXIT_SUCCESS;
  }
  if (show_version)
  {
    printf("%s %s\n", PACKAGE, VERSION);
    return EXIT_SUCCESS;
  }
  
  switch (check_gst_params())
  {
	  case 3:
		  report(_("Resetting GST initial  to 2 * GST shortest."));
		  GST_initial = 2 * GST_shortest;
		  break;
	  case 2:
		  report(_("Resetting GST initial to default."));
		  GST_initial = DEFAULT_GST_INITIAL;
	  case 1:
		  report(_("Resetting GST shortest to default."));
		  GST_shortest = DEFAULT_GST_SHORTEST;
		  break;
	  default:
		  break;
  }

  if(!check_kr_params())
  {
	  report(_("Resetting Karp Rabin params to default."));
	  KR_base = DEFAULT_KR_BASE;
	  KR_modulus = DEFAULT_KR_MODULUS;
  }
  
  /*
  Handle a one-to-many compared program
  ---
  Wczytanie wskazanego programu do porownania
  */
  if (one_suspect)
  {
    printf(_("Suspected file: %s\n"), suspect_filename);
    suspect_program = new_program(suspect_filename);
    if (!suspect_program)
    {
      report(_("The suspect program was't loaded correctly."));
      return EXIT_FAILURE;
    }
    if (!process_program(suspect_program))
    {
      report(_("The suspect program was't processed correctly."));
      return EXIT_FAILURE;
    }
	if (verbose_flag)
      output_program(suspect_program);
  }
  
  /*
  Check if enough arguments
  ---
  Sprawdzenie, czy nie za ma³o argumentów
  */
  program_count = argc - optind;
  if (program_count + one_suspect < 2) 
  {
    report(_("Not enough arguments."));
    return EXIT_FAILURE;
  }

  /*
   * Making sure if filenames are unique
   * ---
   *  Upewnienie siê, czy nazwy plików s± unikatowe
   */
  filenames = new_unique_dictionary();
  for(i=optind; i<argc; i++)
    unique_dictionary_add(filenames, argv[i]);

  if (one_suspect)
    delete_from_unique_dictionary(filenames, suspect_filename);
    
  /*
  Check if enough unique arguments
  ---
  Sprawdzenie, czy nie za ma³o unikatowych argumentów
  */
  program_count = filenames->count;
  if (program_count + one_suspect < 2) 
  {
    report(_("Not enough unique arguments."));
    return EXIT_FAILURE;
  }
  
  /*
  loading programs into memory and processing them
  ---
  wczytywanie programów do pamiêci i przetwarzanie ich
  */
  programs = (PROGRAM *) malloc (sizeof(PROGRAM) * program_count);
  iter = filenames->entries;
  program_count = 0;
  while(iter)
  {
    PROGRAM temp = new_program(iter->word);
    if (temp)
    {
      programs[program_count++] = temp;
    }
    else 
    {
	  if(!quiet_flag)
        fprintf(stderr, _("File: `%s' not loaded correctly.\n"), iter->word);
    }
    iter = iter->next;
  }
  
  /*
  Check if enough succesfully loaded programs
  ---
  Sprawdzenie, czy nie za ma³o wczytanych programów
  */
  if (program_count + one_suspect < 2) 
  {
    report(_("Not enough loaded programs."));
    return EXIT_FAILURE;
  }

  /*
  process programs - prepare for comparision
  ---
  przetwórz programy - przygotowanie do porównania
  */
  temp_programs = (PROGRAM *) malloc (sizeof(PROGRAM) * program_count);
  temp_count = 0;
  for (i=0; i < program_count; i++)
  {
    if (process_program(programs[i]) != 0) 
    {
      temp_programs[temp_count++] = programs[i];
	  if (verbose_flag)
        output_program(programs[i]);
    }
    else
    {
	  if(!quiet_flag)
		  fprintf(stderr, _("Program `%s' not processed.\n"), programs[i]->filename);
      free_program(programs[i]);
    }
  }
  free(programs);
  programs = temp_programs;
  program_count = temp_count;

  /*
  Check if enough succesfully processed programs
  ---
  Sprawdzenie, czy nie za ma³o przeanalizowanych programów
  */
  if (program_count + one_suspect < 2) 
  {
    puts(_("Not enough processed programs."));
    return EXIT_FAILURE;
  }
  babble("Programs processed.");
  /*
   * Program comparison 
   * ---
   *  Porównywanie programów
   */
  if (one_suspect) 
  {
    /* 
    N = O(N) comparisions of programs (linear)
    ---
    N = O(N) liniowa liczba porównañ
    */
    comparisons = (COMPARISON *) malloc (sizeof(COMPARISON) * program_count);
    for(i=0; i < program_count; i++)
      comparisons[i] = compare_programs(suspect_program, programs[i]);
    comparison_count = program_count;
  }
  else 
  {
    /* 
    N * (N-1) / 2 = O(N^2) comparisions of programs (square complexity)
    ---
    N * (N-1) / 2 = O(N^2) liczba porównañ proporcjonalna do kwadratu
    */
    comparison_count = program_count * (program_count-1) / 2;
    comparisons = (COMPARISON *) malloc ( sizeof(COMPARISON) * comparison_count );
    comparison_count = 0; 
    for (i=0; i < program_count - 1; i++)
      for (j=i+1; j < program_count; j++)
        comparisons[comparison_count++] = compare_programs(programs[i], programs[j]);
  }
  
  /*
  sort results descending
  ---
  sortowanie wyników malej±co wzglêdem podobieñstwa
  */
  qsort(comparisons, comparison_count, sizeof(COMPARISON), compare_comparison);
  
  /*
  print results to output
  ---
  wydrukowanie wyników na wyj¶cie
  */
  for (i=0; i < comparison_count; i++)
  {
    if ( comparisons[i]->overall >= thereshold )
      output_comparison(comparisons[i]);
  }
  
  return EXIT_SUCCESS;
}

