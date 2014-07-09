// Naglowek: TKontener.h

/*
	KLASY:
    ------
    TKontener
*/

#ifndef TKontenerH
#define TKontenerH

#include "Byt.h"
#include "TPlansza.h"

class TKontener : public Byt
{
public:
	TKontener()
    {
    	N=0;
        E=0;
    }
	TPlansza Tutaj;
    TKontener *E, *N, *W, *S;
    int wczytaj(char *nazwa);
	void usun_nast();
};

#endif
