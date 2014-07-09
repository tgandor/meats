// Naglowek: TOrganizm.h

/*
	KLASY:
    ------
    TOrganizm (abstrakcyjna)
    TJa
    TPotwor
*/

#ifndef TOrganizmH
#define TOrganizmH

#include "Byt.h"
#include "Wsp.h"
#include "TPrzedmiot.h"

#include <string.h>
#include <fstream>
#include <iostream>
#include "conio.h"

/* DEFINICJE STALYCH  -  gatunki */
#define CZLOWIEK 0
#define  ZWIERZE 1
#define DUCH 2

/* Stale dotyczace gry */
#define MAX_KASA_POCZ 1000
#define MIN_ENERGIA_POCZ 1000
#define MAX_BONUS_ENERGII 1000
#define EGZYSTENCJA 2 // ilosc kalorii zuzywana w kazdej turze

#define GLODNY 0
#define GRANICA_GLODU 1000
#define SYTY   1
#define GRANICA_SYTOSCI 4000
#define PRZEJEDZONY  2
#define GRANICA_PRZEJEDZENIA 8000

#define LEKKI 0
#define DOCIAZONY 1
#define PRZECIAZONY 2
#define GRANICA 3
#define WSPOLCZYNNIK_SILY 650



/* KLASY */
class TOrganizm : public Byt
{
public:
	Wsp polozenie;
    int HP;
    int HPmax;
    int sila;
    int konstytucja;
    int szybkosc;
	virtual int tura()=0;
    virtual void wczytaj(std::ifstream &str)=0;
    virtual int przyjmij_atak(int punkty_ataku) = 0;
    virtual int atakuj() = 0;
};

class TJa : public TOrganizm
{
public:
/*  DANE WLASCIWE TYLKO GLOWNEMU BOHATEROWI  */
	char profesja[30]; /* zawod */
    int energia; /* ilosc sil witalnych */
    int kasa; /* aktywa */
    int masa; /* calkowity ladunek na plecach */
    int wiara; /* sila modlitwy */
    int uzbrojenie;
    int opancerzenie;
    int przyspieszenie;
    int metabolizm; /* zuzycie kalorii */
    int wzmocnienie;
    int hart;      /* wzmocnienie konstytucji */
    int poboznosc; /* wzmocnienie wiary */
    int obciazenie; /* stopnie obciazenia ladunkiem */
    int glod; /* zarowno nadmiar, jak niedobor energii */
    Lista plecak;
/*  KONSERWACJA KLASY - OPERACJE WE/WY  */
    virtual void wczytaj(std::ifstream &str);
    void zachowaj(std::ofstream &str);
    void przywroc(std::ifstream &str);
/*  INICJALIZACJA PRZY TWORZENIU OBIEKTU  */
	TJa()
    {
         energia = MIN_ENERGIA_POCZ + rand() % MAX_BONUS_ENERGII;
         kasa = rand() % MAX_KASA_POCZ;
         masa = kasa;
         uzbrojenie = opancerzenie = przyspieszenie = 0;
         metabolizm = wzmocnienie = 0;
    }
/*  FUNKCJE UZYTKOWE  */
    virtual int tura();
    virtual int przyjmij_atak(int punkty_ataku);
    virtual int atakuj();

    void Przyswoj_Przedmiot(int ktory, Lista &gdzie);
    int Kup_Przedmiot(int ktory, Lista &gdzie);
    TPrzedmiot* Oddaj_Przedmiot(int ktory, Lista &gdzie);
    TPrzedmiot* Sprzedaj_Przedmiot(int ktory, Lista &gdzie);
};


class TPotwor : public TOrganizm
{
public:
/*  DANE - o potworach wiemy mniej...  */
	char gatunek[30];
    int nastawienie;
    int rasa;
    char symbol;
/*  PRZYGOTOWANIE KLASY  */
    virtual void wczytaj(std::ifstream &str);
/*  FUNKCJE UZYKTOWE  */
    virtual int tura();
    virtual int przyjmij_atak(int punkty_ataku);
    virtual int atakuj();
};

#endif
