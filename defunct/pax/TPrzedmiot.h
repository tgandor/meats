// Naglowek: TPrzedmiot.h

/*
	KLASY:
    ------
    TPrzedmiot (abstrakcyjna, polimorf., bo pochodzi od Bytu)
    TArtefakt
    TBron
    TZbroja
    TJedzenie
    TPieniadze
*/

#ifndef TPrzedmiotH
#define TPrzedmiotH

#include "Byt.h"

#include <fstream>
#include <iostream>
#include <string>
#include <typeinfo>

#include "itoa.hpp"

using namespace std;

class TPrzedmiot : public Byt
{
public:
    char nazwa[30];
	int masa;
    int cena;
    char symbol;
    virtual int wczytaj(ifstream &str)=0;
    virtual void zapisz(ofstream &str)=0;
};

class TBron : public TPrzedmiot
{
public:
	int atak;
    virtual int wczytaj(ifstream &str);
    virtual void zapisz(ofstream &str);
};

class TZbroja : public TPrzedmiot
{
public:
	int obrona;
    virtual int wczytaj(ifstream &str);
    virtual void zapisz(ofstream &str);};

class TJedzenie : public TPrzedmiot
{
public:
	int kalorie;
    virtual int wczytaj(ifstream &str);
    virtual void zapisz(ofstream &str);
};

class TPieniadze : public TPrzedmiot
{
public:
	int kwota;
    TPieniadze(int ile)
    {
    	kwota = ile;
        symbol = '$';
        strcpy(nazwa, "Zloto");
    }
    virtual int wczytaj(ifstream &str);
    virtual void zapisz(ofstream &str);
};

class TArtefakt : public TPrzedmiot
{
public:
	int sila;
    int konstytucja;
    int szybkosc;
    int wiara;
    int energia;
    virtual int wczytaj(ifstream &str);
    virtual void zapisz(ofstream &str);
};

string Pokaz_Jedzenie(Lista &l);
string Pokaz_Przedmioty(Lista &l);
string Pokaz_Bronie(Lista &l);
string Cennik(Lista &l);

void wczytaj_liste(Lista &l, ifstream &str);
void zapisz_liste(Lista &l, ofstream &str);

int Ile_Broni(Lista &l);
int Ile_Jedzenia(Lista &l);

#endif
