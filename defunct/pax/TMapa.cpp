// Modul: TMapa.cpp

#include "TMapa.h"
#include "Wsp.h"


TPlansza* TMapa::Odczytaj(Wsp ktora)
/*  Odczytuje plansze o zadanych wspolrzednych,
    a jezeli jeszcze takiej nie ma w kolekcji
    to zwraca NULL */
{
	TPlansza *wynik;
    list<Wsp>::iterator it;
    int match=0;

    for(it=Dostepne_Plansze.begin(); it !=Dostepne_Plansze.end(); it++)
    {
    	if(*it == ktora)
        {
        	match=1;
            break;
        }
    }
    if(match)
    {
        wynik = new TPlansza;
        ifstream wejscie(ktora.nazwa_pliku());
        wynik->wczytaj(wejscie);
        wejscie.close();
        return wynik;
    }
    else
    	return 0;
}

TPlansza* TMapa::Daj_Inna(Wsp &niz_ktora)
/*  Odczytuje plansze o innych niz zadane wspolrzednych,
    a jezeli jeszcze takiej nie ma w kolekcji (np. jest
    tylko 1, to zwraca NULL, ustawia parametr na wylosowana
    plansze */
{
	TPlansza *wynik;
    list<Wsp>::iterator it;
    int ok=0,i;
    if(Dostepne_Plansze.size() == 0)
    	return 0;
    if(Dostepne_Plansze.size() == 1 && Dostepne_Plansze.front() == niz_ktora)
    	return 0;
    while(!ok)
    {
    	it = Dostepne_Plansze.begin();
    	for(i=0; i < rand() % Dostepne_Plansze.size(); i++)
        	it++;
        if(!(*it == niz_ktora))
        	ok = 1;
    }
    wynik = new TPlansza;
    niz_ktora = *it;
    ifstream wejscie(niz_ktora.nazwa_pliku());
    wynik->wczytaj(wejscie);
    wejscie.close();
    return wynik;
}

void TMapa::Zapisz(TPlansza *co, Wsp gdzie)
/* Kasuje plansze */
{
    list<Wsp>::iterator it;
    int match=0;

    for(it=Dostepne_Plansze.begin(); it !=Dostepne_Plansze.end(); it++)
    {
    	if(*it == gdzie)
        {
        	match=1;
            break;
        }
    }

    ofstream wyjscie(gdzie.nazwa_pliku());
    co->zapisz(wyjscie);
    wyjscie.close();

    delete co;

    if(match)
		return;
    Dostepne_Plansze.push_front(gdzie);
}

void TMapa::zachowaj(ofstream &str)
{
    list<Wsp>::iterator it;
	str << Dostepne_Plansze.size() << endl;
    for(it = Dostepne_Plansze.begin(); it != Dostepne_Plansze.end(); it++)
    	it->zapisz(str);
}

void TMapa::pobierz(ifstream &str)
{
	int i,n;
    Wsp temp;

    str >> n;
    for(i=0; i<n; i++)
    {
    	temp.wczytaj(str);
        Dostepne_Plansze.push_back(temp);
    }
}
