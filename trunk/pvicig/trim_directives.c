#include "trim_directives.h"

char* trim_directives(char *source)
{
	regex_t *regex;
	regmatch_t *match;
	int err_nr;
	size_t num_sub;
	int offset = 0;
	char *line = 0;
	char *output = 0;
	/*
	puts("Oto co dostaje na wejsciu:");
	puts(source);
	printf("Mam %d dyrektyw\n", NUM_DIRECTIVES);
	*/
	regex = (regex_t *) malloc (sizeof(regex_t));
	assert(regex != 0);
	memset(regex, 0, sizeof(regex_t));
	// err_nr = regcomp(regex, "^[ \t]*#[ \t]*([a-zA-Z])*.*$",  REG_NEWLINE /* | REG_EXTENDED */);
	err_nr = regcomp(regex, "^[ \t]*#[ \t]*([^ \t]*).*$", REG_NEWLINE  | REG_EXTENDED  );
	// printf("Blad: %d\n", err_nr);
	num_sub = regex->re_nsub + 1;
	match = (regmatch_t *) malloc (sizeof(regmatch_t) * num_sub);
    assert(match != 0);
	
	while (regexec(regex, source + offset, num_sub, match, 0) == 0) {
		int skip;
		int total_length;
		int directive_length;
		
 	    // err_nr = regexec(regex, source + offset, num_sub, match, 0);
		// printf("Blad: %d\n", err_nr);
		// printf("%d %d\n", match->rm_so, match->rm_eo);
		
		// dopisanie do wyjscia tego, co poprzedza -- concat up to here
		astrn0cat(&output, source+offset, match->rm_so);

		total_length = match->rm_eo - match->rm_so;
		directive_length = match[1].rm_eo - match[1].rm_so;

		// wyci±gniêcie dyrektywy z linii -- extract directive
		astrn0cpy(&line, source+offset+match[0].rm_so, total_length);
		// printf("Total: >%s<\n", line);
		astrn0cpy(&line, source+offset+match[1].rm_so, directive_length);
		// printf(">%s<\n", line);
		
		skip = match->rm_eo;
		if (is_useful_directive(line))
		{
			// puts("Ta dyrektywa jest ok\n");
			astrn0cat(&output, source+offset, total_length);
		}
		else 
		{
			// puts("Ta dyrektywa zostanie usunieta");
			while (source[offset+skip] == '\n' || source[offset+skip] == '\r') ++skip;
		}
		// printf("Output now: ~%s~\n Offset: %d\n", output, offset);
		offset += skip;
	}
	// Append the rest to output
	astrcat(&output, source+offset);

	astrfree(&line);
	// printf("Final output: \n>%s<\n", output);
	regfree(regex);
	free(regex);
	return output;
    // return source;
}

void trim_directives_from(char **source)
{
	char *temp;
	temp = *source;
	*source = trim_directives(*source);
	free(temp);
}

int is_useful_directive(char *directive)
{
	int i;
	for (i = 0; i < NUM_DIRECTIVES; i++) 
	{
		if(!strcmp(directive, neccessary_directives[i]))
			return 1;
	}
	return 0;
}

char *trim_all_directives(char *source)
{
	regex_t *regex;
	regmatch_t *match;
	int err_nr;
	size_t num_sub;
	int offset = 0;
	char *output = 0;
	regex = (regex_t *) malloc (sizeof(regex_t));
	assert(regex != 0);
	memset(regex, 0, sizeof(regex_t));
	err_nr = regcomp(regex, "^[ \t]*#.*$", REG_NEWLINE  | REG_EXTENDED  );
	num_sub = regex->re_nsub + 1;
	match = (regmatch_t *) malloc (sizeof(regmatch_t) * num_sub);
    assert(match != 0);
	
	while (regexec(regex, source + offset, num_sub, match, 0) == 0) {
		int skip;
		
		// dopisanie do wyjscia tego, co poprzedza -- concat up to here
		astrn0cat(&output, source+offset, match->rm_so);

		skip = match->rm_eo;
		printf("Output now: ~%s~\n Offset: %d\n", output, offset);
		offset += skip;
	}
	// Append the rest to output
	astrcat(&output, source+offset);

	// printf("Final output: \n>%s<\n", output);
	return output;
    // return source;
}

