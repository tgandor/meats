// Naglowek: TGenerator.h

/*
	KLASY:
    ------
    TGenerator
*/

#ifndef TGeneratorH
#define TGeneratorH

#include "Byt.h"
#include "TKontener.h"
#include "TOrganizm.h"
#include "TPrzedmiot.h"

class TGenerator : public Byt
{
    int ile_plansz_mam;
    int max_cena;
public:
    void WczytajDane(char *pl, char *stw, char *br, char *zbr,
    				 char *art,	char *jedz);
    void wypisz();
    TPlansza *Daj_Plansze();
    TPrzedmiot *Daj_Przedmiot(int kase_tez = 1);
    TPotwor *Daj_Potwora();
    virtual ~TGenerator();
private:
	TKontener Zapas_Plansz;
	Lista Stworki;
    Lista Jedzenie;
    Lista Bronie;
    Lista Zbroje;
    Lista Artefakty;
};

#endif
