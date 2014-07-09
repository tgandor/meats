// Naglowek: TPlansza.h

/*
	KLASY:
    ------
    TPole
    TPlansza
 */

#ifndef TPlanszaH
#define TPlanszaH

#include "Byt.h"
#include "TOrganizm.h"
#include "TPrzedmiot.h"
/* wspolrzedne - typ Wsp */

#include <conio.h>
#include <iostream.h>
#include <fstream.h>

/* FLAGI POLA NA PLANSZY */
#define POLE_WOLNE 0
#define POLE_ZAJETE 1
#define DOM 2
#define SKLEP 3
#define TU_JEST_POTWOR 4

class TPole : public Byt
{
public:
	Lista Zawartosc;
    int Flagi;
    char znak;
    char poczatkowy;
    TPole() {};
    virtual ~TPole();
};

class TPlansza : public Byt
{
public:
	TPole Pola[60][15];
    int ile;
    virtual void wyswietl();
    virtual void akt_pole(Wsp ktore);
    void wczytaj(ifstream &str);
    void zapisz(ofstream &str);
    Wsp Daj_Wolne_Pole();
    Wsp Ustaw_Dom();
    /* INLINE'OWE funkcje przyspieszajace zapis */
    Lista& Co_Tam_Jest(Wsp gdzie)
    {
    	return Pola[gdzie.x][gdzie.y].Zawartosc;
    }
    char& Znak(Wsp gdzie)
    {
    	return Pola[gdzie.x][gdzie.y].znak;
    }
    char& Poczatkowy(Wsp gdzie)
    {
    	return Pola[gdzie.x][gdzie.y].poczatkowy;
    }
    int& Flagi(Wsp Gdzie)
	{
		return Pola[Gdzie.x][Gdzie.y].Flagi;
	}
};

#endif
