// Naglowek: TGra.h

/*
	KLASY:
    ------
    TGra
*/

#ifndef TGraH
#define TGraH

#include "Byt.h"
#include "TGenerator.h"
#include "TPlansza.h"
#include "TMapa.h"
#include "TInterfejs.h"
#include "TOrganizm.h"
#include "TPrzedmiot.h"
#include "Wsp.h"

#include <string>
// #include <dir.h>
#include <sys/stat.h>
#include <stdio.h>
#include <unistd.h>

#include "itoa.hpp"

using std::string;
using std::list;

inline void Sleep(int miliseconds)
{
	usleep(1000 * miliseconds);
}

class TGra : public Byt
{
/* Dane gry: */
    char imie[30];
    Wsp Biezaca_Plansza;
    int Tura, Punkty, Koniec_Gry, Liczba_Potworkow, Ostatnia_Modlitwa;
    list<TPotwor*> Potwory;
/* Wewnetrzne "urzadzenia" : */
    TMapa *Mapa;
    TPlansza *Plansza;
/* Wewnetrzne funkcje - zwiazane z rozkazami: */
    void Wykonaj_Rozkaz(char rozkaz);
    void Idz_Lub_Bij(char kierunek);
    void Podnoszenie();
    void Upuszczanie();
    void Maly_Teleport();
    void Duzy_Teleport();
    void Modlitwa();
    void Posilek();
    void Zastosowanie();
    void Wladanie();
    void Zbij_Potwora(Wsp gdzie);
    void Potworki_Naprzod();
    void Zegnajcie_Potworki();

    void Sprzatanie();
    void Rezygnacja();
    void Zapisanie();
    void Umiesc_Potwora();
    void Umiesc_Przedmiot();
    string Status();
public:
/*  WLASCIWOSCI DOSTEPNE Z ZEWNATRZ  */
	TGenerator *Generator;
    TInterfejs *Interfejs;
    TJa *Ja;
/*  STANDARDOWE WARTOSCI  */
    TGra()
    {
        Mapa = new TMapa;
        Tura = 0;
        Biezaca_Plansza.x = 0;
        Biezaca_Plansza.y = 0;
        Koniec_Gry = 0;
        Punkty = 0;
        Liczba_Potworkow = 0;
        Ostatnia_Modlitwa = 0;
    }
/*  FUNKCJE STEROWANE Z MODULU MAIN  */
    virtual int Wczytywanie();
    virtual void Jakie_Imie();
    virtual int Wybor_Postaci(char *nazwa);
    void Inicjalizuj();
    void Tocz_Sie();
    virtual ~TGra()
    {
    	delete Mapa;
        delete Generator;
        delete Interfejs;
        delete Ja;
    }
};


/* NUMERY IDENTYFIKACYJNE KOMUNIKATOW */
#define SMIERC 			0
#define GLOD_POCZATEK 	1
#define GLOD_SILNY 		2
#define BRAK_KASY 		3
#define SPRZEDANE 		4
#define ATAK 			5
#define TRAFIENIE		6
#define BRON_W_DLON 	7
#define DOBRE_JEDZENIE	8
#define LEKKI_POSILEK	9
#define DALEJ_GLODNY	10
#define MODLITWA_START 	11
#define MODLITWA_OK		12
#define MODLITWA_ZLE	13
#define NIC_DO_UZYCIA	14
#define NIC_DO_JEDZENIA	15
#define NIC_DO_ODLOZENIA 16
#define NIC_TU_NIE_MA	17
#define CZY_DO_DOMU		18
#define CZY_BIC			19
#define WITAJ_W_PAX		20
#define CO_ZJESC        21
#define CO_UJAC         22
#define CO_UZYC         23
#define CO_PODNIESC     24
#define CO_POLOZYC      25
#define OK_ALE_GDZIE    26

/* PEWNE STALE WARTOSCI W GRZE,
	np. ceny teleportacji */
#define CENA_MT 200
#define CENA_DT 400
#define OPROCZ_KASY 0
#define CZEKAJ 1
#define NIE_CZEKAJ 0
#define DOLACZ 1
#define LICZBA_TOWAROW 3
#define OKRES_PRZEDMIOTOW 50
#define OKRES_POTWOROW 30
#define OKRES_MODLITWY 50

#endif
