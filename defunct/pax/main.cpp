
#include "Byt.h"
#include "TKontener.h"
#include "TGra.h"
#include "TGenerator.h"
#include "TKontener.h"

#include <fstream.h>
#include <conio.h>

int main(int argc, char* argv[])
{
	/* ZMIENNE */
    typedef char linia[30];  /* LOKALNY TYP, DLA PRZEJRZYSTOSCI */
    linia plansze, komunikaty, stwory, herosi,
    	  artefakty, zbroje, bronie, jedzenie;

    /* INICJALIZACJA PROGRAMU - DANE ZEWNÊTRZNE */
	ifstream ini("pax.ini");
    ini.getline(plansze, 29);
    ini.getline(komunikaty, 29);
	ini.getline(herosi, 29);
    ini.getline(stwory, 29);
    ini.getline(artefakty, 29);
    ini.getline(zbroje, 29);
    ini.getline(bronie, 29);
    ini.getline(jedzenie, 29);
    ini.close();
    /* KONIEC INICJALIZACJI: PROGRAM WCZYTAL NAZWY PLIKOW */

	/* GLOWNY OBIEKT PROGRAMU */
	TGra *Gra;
	Gra = new TGra;
    /* TWORZENIE SKLADOWYCH - POZWALA NA EW. PODMIANE */
    Gra->Generator = new TGenerator;
    Gra->Interfejs = new TInterfejs;
    /* WCZYTYWANIE DANYCH - Z PLIKOW I KLAWIATURY */
    Gra->Generator->WczytajDane(plansze, stwory, bronie, zbroje,
    							artefakty, jedzenie);
    Gra->Interfejs->pobierz_komunikaty(komunikaty);

    if(Gra->Wybor_Postaci(herosi))    /* czy wybrano nowa postac */
    {
	    clrscr();
    	if(Gra->Wczytywanie())         /* wczytywanie zapisanej gry */
        	return 1;   /* najwyrazniej sie nie udalo */
    }
    else
    {
	    clrscr();                    /* tworzenie nowego bohatera */
    	Gra->Jakie_Imie();
        clrscr();
	    Gra->Inicjalizuj();
    }

    Gra->Tocz_Sie();

    delete Gra;

	return 0;   /* poprawne zakonczenie gry: wyjscie, zapisanie, dom */
}

