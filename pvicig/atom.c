#include "atom.h"

void atom_info(const ATOM a)
{
	printf("Atom code: %d=%s, text: %s, start: %d, len: %d, line: %d\n",
			a->code, atom_names[a->code], a->content, a->start, a->len, a->line);
}

