// Naglowek: TMapa.h

/*
	KLASY:
    ------
    TMapa
*/

#ifndef TMapaH
#define TMapaH

#include "Byt.h"
#include "Wsp.h"
#include "TPlansza.h"

#include <fstream>

class TMapa : public Byt
{
/*  DANE  */
	std::list<Wsp> Dostepne_Plansze;
public:
/*  USLUGI  */
    TPlansza* Odczytaj(Wsp ktora);
    TPlansza* Daj_Inna(Wsp &niz_ktora);
    void Zapisz(TPlansza *co, Wsp gdzie);
/*  KONSERWACJA  */
	void zachowaj(std::ofstream &str);
    void pobierz(std::ifstream &str);
};

#endif
