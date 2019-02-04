
#include "unique_dictionary.h"

UNIQUE_DICTIONARY
new_unique_dictionary()
{
	return (UNIQUE_DICTIONARY) calloc ( 1, sizeof (struct unique_dictionary) );
}

void
unique_dictionary_add(UNIQUE_DICTIONARY dictionary, const char *word)
{
	DICTIONARY_ENTRY new_entry;

	if (lookup_unique_dictionary(dictionary, word) != (DICTIONARY_ENTRY)0)
		return;
	new_entry = (DICTIONARY_ENTRY) malloc (sizeof(*new_entry));
	new_entry->next = dictionary->entries;
	new_entry->word = strdup(word);
	new_entry->data = 0;
	dictionary->entries = new_entry;
	++(dictionary->count);
}

void
free_unique_dictionary(UNIQUE_DICTIONARY dictionary)
{
	DICTIONARY_ENTRY curr, next;
	curr = dictionary->entries;
	while (curr)
	{
		next = curr->next;
		free(curr->word);
		free(curr);
		curr = next;
	}
}

DICTIONARY_ENTRY
lookup_unique_dictionary(UNIQUE_DICTIONARY dictionary, const char *word)
{
	DICTIONARY_ENTRY result;
	result = dictionary->entries;
	while (result && strcmp(word, result->word))
		result = result->next;
	return result;
}

void
output_unique_dictionary(UNIQUE_DICTIONARY dictionary)
{
	if (!dictionary->entries)
	{
		puts("The dictionary is empty");
	}
	else
	{
		DICTIONARY_ENTRY iter;
		printf("%d entries:\n", dictionary->count);
		iter = dictionary->entries;
		while (iter)
		{
			puts(iter->word);
			iter = iter->next;
		}
	}
}

int
delete_from_unique_dictionary(UNIQUE_DICTIONARY dictionary, const char *word)
{
	DICTIONARY_ENTRY entry, temp;
	int deleted = 0;
	/* Not found */
	if ( lookup_unique_dictionary(dictionary, word) == 0 )
		return 0;
	/* Chopping off head */
	if ( dictionary->entries && !strcmp(dictionary->entries->word, word) )
	{
		temp = dictionary->entries;
		dictionary->entries = dictionary->entries->next;
		free(temp->word);
		free(temp);
		--(dictionary->count);
		return 1;
	}
	/* Somwhere on the list */
	entry = dictionary->entries;
	while ( entry && entry->next && !deleted )
	{
		if ( !strcmp (entry->next->word, word) )
		{
			deleted = 1;
			temp = entry->next;
			entry->next = entry->next->next;
			free(temp->word);
			free(temp);
			--(dictionary->count);
		}
		entry = entry->next;
	}
	return deleted ? 1 : -1;
}

