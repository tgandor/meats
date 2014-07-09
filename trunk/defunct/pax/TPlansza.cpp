
#include "TPlansza.h"

TPole::~TPole()
/* Usuwanie zawartosci pola (obiektow i wskaznikow),
   dlatego wszedzie delete i pop_front, a nie po prostu clear */
{
	while(Zawartosc.size())
    {
    	delete Zawartosc.front();
        Zawartosc.pop_front();
    }
}

void TPlansza::wyswietl()
/* Pokazanie planszy na ekranie */
{
    int i,j;
	for(i=0; i<60; i++)
    	for(j=0; j<15; j++)
        {
            gotoxy(i+10,j+5);
            cout << Pola[i][j].znak;
        }
}

void TPlansza::akt_pole(Wsp ktore)
/* Narysowanie pola, na ktorym cos bylo innego,
   np. postac glownego bohatera, i trzeba je odnowic */
{
	gotoxy(ktore.x+10, ktore.y+5);
    cout << Pola[ktore.x][ktore.y].znak;
}

void TPlansza::wczytaj(ifstream &str)
/* Wczytywanie planszy ze strumienia:
 * Zarowno dla wzorcow plansz w TGeneratorze,
 * jak i do wczytywania juz wygenerowanych plasz
 * w klasie TMapa
 */
{
    int i,j;
    for(j=0; j<15; j++)
    	for(i=0; i<60; i++)
        {
		    str >> Pola[i][j].znak;
            Pola[i][j].poczatkowy = Pola[i][j].znak;
            if(Pola[i][j].znak == '.')
            {
                Pola[i][j].Flagi = POLE_WOLNE;
            	continue;
            }
            switch(Pola[i][j].znak)
            {
            	case '\\':
                case '/':
                case '|':
                case '-':
                	Pola[i][j].Flagi = POLE_ZAJETE;
                    break;
                case '^':
                	Pola[i][j].Flagi = DOM;
                    break;
                case '&':
                	Pola[i][j].Flagi = SKLEP;
                    break;
                default:
                	wczytaj_liste(Pola[i][j].Zawartosc, str);
                    Pola[i][j].poczatkowy = '.';
            }
        }
    str >> ile;
}

void TPlansza::zapisz(ofstream &str)
/* Zapisywanie przy opuszczaniu planszy (TMapa)
 * (lub zapisywaniu gry)
 */
{
    int i,j;
    Lista::iterator it;
    
    for(j=0; j<15; j++)
    {
    	for(i=0; i<60; i++)
        {
		    str << Pola[i][j].znak;
            switch(Pola[i][j].znak)
            {
            	case '\\':
                case '/':
                case '|':
                case '-':
                case '.':
                case '&':
                case '^':
                	break;
                default:
                Lista &l = Pola[i][j].Zawartosc;
                if(l.size() > 0)
                	zapisz_liste(l, str);
            }
        }
        str << endl;
    }
    str << ile;
}

Wsp TPlansza::Daj_Wolne_Pole()
{
	Wsp wynik;
    do
    {
    	wynik.x = rand() % 60;
        wynik.y = rand() % 15;
    }
    while(Pola[wynik.x][wynik.y].Flagi != POLE_WOLNE);
    return wynik;
}


Wsp TPlansza::Ustaw_Dom()
{
	Wsp wynik;
    do
    {
    	wynik.x = rand() % 58 + 1; /* pomijamy skrajne pola */
        wynik.y = rand() % 13 + 1; /* zeby nie wejsc do domu od tylu */
    }
    while(Pola[wynik.x][wynik.y].Flagi != POLE_WOLNE);
    Pola[wynik.x][wynik.y].Flagi = DOM;
    Pola[wynik.x][wynik.y].znak = '^';
    return wynik;
}

