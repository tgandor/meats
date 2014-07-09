#include "Byt.h"

Byt::Byt()
{
	*_nazwa=0;
}

Byt::~Byt()
{
}

void wyczysc_liste(Lista &l)
{
	while(l.size())
    {
    	delete l.front();
        l.pop_front();
    }
}
