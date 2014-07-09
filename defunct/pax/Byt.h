/*
	Klasa Byt (polimorficzna)
    Lista - wskaznikow na Byt
*/

#ifndef _Byt_included
#define _Byt_included

#include <string.h>
#include <list>

class Byt
{
public:
	char _nazwa[25];
    Byt();
    virtual char* nazwa()
    {
    	return _nazwa;
    }
    bool operator == (Byt inny)
    {
    	return !strcmp(_nazwa, inny._nazwa);
	}
	virtual ~Byt();
};

typedef std::list<Byt*> Lista;

void wyczysc_liste(Lista &l);

#endif
