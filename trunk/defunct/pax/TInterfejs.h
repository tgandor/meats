// Naglowek TInterfejs.h

/*
	KLASY:
    ------
    TInterfejs
*/

#ifndef TInterfejsH
#define TInterfejsH

#include "Byt.h"
#include "Wsp.h"
#include "TOrganizm.h"

#include <iostream.h>
#include <fstream.h>
#include <string.h>
#include <conio.h>

#define LICZBA_KOMUNIKATOW 27

class TInterfejs : public Byt
{
	string komunikaty[LICZBA_KOMUNIKATOW];
    void Wyczysc_Tekst();
public:

	virtual char Czekaj_Na_Rozkazy();
    void pobierz_komunikaty(char *nazwa_pliku);
    void Wypisz_Komunikat(int nr_kom, int czekaj=1);
    int Na_Pewno(char *pytanie, int czy_dolaczyc=0);
    void Wypisz_Tekst(string tekst, int czy_czekac=0);
    int Wybor(int ile_mozliwosci);
    void Pokaz_Status(string status);
    void Pokaz_Ture(int tura);
    void Pokaz_Mnie(Wsp gdzie);
    void Pokaz_Potwora(Wsp gdzie, TPotwor* co);
};

#endif
