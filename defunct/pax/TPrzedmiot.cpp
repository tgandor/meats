// Modul: Tprzedmiot.cpp

#include "TPrzedmiot.h"

int TPrzedmiot::wczytaj(ifstream &str)
/* Niby czysto wirtualna, a jednak...
 * wczytuje wspolne dla wszystkich przedmiotow
 * cechy. Nastepne funkcje wczytuja pozostale
 * atrybuty specyficznych typow przedmiotow
 */
{
	str.getline(nazwa, 29);
	str.getline(nazwa, 29);
	str >> masa >> cena;
    return cena;
}

int TArtefakt::wczytaj(ifstream &str)
{
    int cena;
	cena = TPrzedmiot::wczytaj(str);
    str >> sila >> konstytucja >> szybkosc >> wiara >> energia;
    str >> symbol;
    return cena;
}

int TBron::wczytaj(ifstream &str)
{
	int cena;
	cena = TPrzedmiot::wczytaj(str);
    str >> atak;
    symbol = ')';
    return cena;
}

int TZbroja::wczytaj(ifstream &str)
{
    int cena;
	cena = 	TPrzedmiot::wczytaj(str);
    str >> obrona;
    symbol = '[';
    return cena;
}

int TJedzenie::wczytaj(ifstream &str)
{
    int cena;
	cena = 	TPrzedmiot::wczytaj(str);
    str >> kalorie;
    symbol = '%';
    return cena;
}

int TPieniadze::wczytaj(ifstream &str)
{
	symbol = '$';
    str >> kwota;
    return 0;
}

void TPrzedmiot::zapisz(ofstream &str)
/* Niby czysto wirtualna, a jednak...
 * wczytuje wspolne dla wszystkich przedmiotow
 * cechy. Nastepne funkcje wczytuja pozostale
 * atrybuty specyficznych typow przedmiotow
 */
{
    str << nazwa << endl;
	str << masa << endl;
    str << cena << endl;
}

void TArtefakt::zapisz(ofstream &str)
{
	TPrzedmiot::zapisz(str);
    str << sila << endl;
    str <<  konstytucja << endl << szybkosc << endl;
    str << wiara << endl << energia << endl;
    str << symbol << endl;
}

void TBron::zapisz(ofstream &str)
{
	TPrzedmiot::zapisz(str);
    str << atak << endl;
}

void TZbroja::zapisz(ofstream &str)
{
	TPrzedmiot::zapisz(str);
    str << obrona << endl;
}

void TJedzenie::zapisz(ofstream &str)
{
	TPrzedmiot::zapisz(str);
    str << kalorie << endl;
}

void TPieniadze::zapisz(ofstream &str)
{
    str << kwota << endl;
}


string Pokaz_Jedzenie(Lista &l)
/* Wybiera z listy l tylko produkty spozywcze
 * Zwraca stringa, ktory jest juz gotowy do
 * podejmowania wyboru, co zjesc
 */
{
	string wynik;
    string test = "TJedzenie";
    Lista::iterator it;
    TJedzenie *temp;
    char c='a';

    wynik = "Jedzenie:";
    for(it = l.begin(); it != l.end(); it++)
    {
    	if( test == typeid(*(*it)).name() )
        {
        	temp = dynamic_cast<TJedzenie*>(*it);
            wynik += '\n';
            wynik += c++;
            wynik += ". ";
            wynik += temp->nazwa;
        }
    }
    return wynik;
}

string Pokaz_Przedmioty(Lista &l)
/* Pokazuje przedmioty z danej listy - obojetnie
 * czy to juz stan naszego posiadania, czy jeszcze
 * na podlodze
 */
{
	string wynik;
    Lista::iterator it;
    TPrzedmiot *temp;
    char c='a';

    wynik = "Przedmioty:";
    for(it = l.begin(); it != l.end(); it++)
    {
    	temp = dynamic_cast<TPrzedmiot*>(*it);
        wynik += '\n';
        wynik += c++;
        wynik += ". ";
        wynik += temp->nazwa;
    }
    return wynik;
}

string Pokaz_Bronie(Lista &l)
/* Wyswietla tylko bronie. Dla wyboru nowej aktywnej
 * broni
 */
{
	string wynik;
    string test = "TBron";
    Lista::iterator it;
    TBron *temp;
    char c='a';

    wynik = "Uzbrojenie:";
    for(it = l.begin(); it != l.end(); it++)
    {
    	if( test == typeid(*(*it)).name() )
        {
        	temp = dynamic_cast<TBron*>(*it);
            wynik += '\n';
            wynik += c++;
            wynik += ". ";
            wynik += temp->nazwa;
        }
    }

    return wynik;
}

string Cennik(Lista &l)
/* To samo, co Pokaz_Przedmioty(), ale jeszcze z cenami */
{
	string wynik;
    char buf[30], c='a';
    Lista::iterator it;
    TPrzedmiot *temp;

    wynik = "Cennik:";
    for(it = l.begin(); it != l.end(); it++)
    {
    	temp = dynamic_cast<TPrzedmiot*>(*it);
        wynik += '\n';
        wynik += c++;
        wynik += ". ";
        wynik += temp->nazwa;
        wynik += " - ";
        wynik += itoa(temp->cena, buf, 10);
    }
    return wynik;
}

int Ile_Jedzenia(Lista &l)
/* Zwraca liczbe elementow pozywienia na przekazanej liscie */
{
    Lista::iterator it;
    string test = "TJedzenie";
    int wynik=0;

    for(it = l.begin(); it != l.end(); it++)
    	if( test == typeid(*(*it)).name() )
    		wynik++;
    return wynik;
}

int Ile_Broni(Lista &l)
/* Zwraca liczbe uzbrojenia wystepujace na danej liscie */
{
    Lista::iterator it;
    string test = "TBron";
    int wynik=0;

    for(it = l.begin(); it != l.end(); it++)
    	if( test == typeid(*(*it)).name() )
    		wynik++;
    return wynik;
}

void wczytaj_liste(Lista &l, ifstream &str)
{
    char typ[30];
    TPrzedmiot *temp;

    int i,n;
	str >> n;
    for(i=0; i < n; i++)
    {
    	str >> typ;
        if(!strcmp(typ, "TZbroja"))
        	temp = new TZbroja;
        else if(!strcmp(typ, "TBron"))
        	temp = new TBron;
        else if(!strcmp(typ, "TJedzenie"))
        	temp = new TJedzenie;
        else if(!strcmp(typ, "TArtefakt"))
        	temp = new TArtefakt;
        else if(!strcmp(typ, "TPieniadze"))
        	temp = new TPieniadze(0);
        temp->wczytaj(str);
        l.push_back(temp);
    }
}



void zapisz_liste(Lista &l, ofstream &str)
{
    Lista::iterator it;
    TPrzedmiot *temp;

    str << endl;
	str << l.size() << endl;
    for(it = l.begin(); it != l.end(); it++)
    {
    	str << typeid(*(*it)).name() << endl;
        temp = dynamic_cast<TPrzedmiot*>(*it);
        temp->zapisz(str);
    }
}


