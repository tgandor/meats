// Modul: TGra2.cpp
// Funkcje zwiazane z konkretnymi czynnosciami
/*
	IMPLEMENTUJE:
	void Idz_Lub_Bij(char kierunek)
	void Idz_Lub_Bij(char kierunek);
    void Podnoszenie();
    void Upuszczanie();
    void Maly_Teleport();
    void Duzy_Teleport();
    void Modlitwa();
    void Posilek();
    void Zastosowanie();
    void Wladanie();
    void Umiesc_Potwora();
    void Umiesc_Przedmiot();
*/

#include "TGra.h"

/* ZMIANA WSPOLRZEDNYCH PRZY POSZCZEGOLNYCH RUCHACH */
const Wsp ruch[10] =
{
	{ 0, 0}, // niewykorzystywane
    {-1, 1}, // 1
    { 0, 1}, // 2 dol
    { 1, 1}, // 3
    {-1, 0}, // 4 lewo
    { 0, 0}, // 5
    { 1, 0}, // 6 prawo
    {-1,-1}, // 7
    { 0,-1}, // 8 gora
    { 1,-1}  // 9
};


/* FUNKCJE POMOCNICZE: */

void TGra::Zbij_Potwora(Wsp gdzie)
{
	list<TPotwor*>::iterator ppot;
	for(ppot = Potwory.begin(); ppot != Potwory.end(); ppot++)
    {
    	if(gdzie == (*ppot)->polozenie)
        	break;
    }
    if( (*ppot)->przyjmij_atak(Ja->atakuj()) ) /* Ubilismy potworka */
	{
        Punkty += (*ppot)->HPmax; /* punktowanie zwyciestw */
    	Plansza->akt_pole(gdzie);
        Plansza->Flagi(gdzie) &= SKLEP; /* gasimy bit potwornosci pola */
        delete *ppot;
        Potwory.erase(ppot);
    }
}

void TGra::Zegnajcie_Potworki()
{
	while(!Potwory.empty())
    {
    	delete Potwory.front();
        Potwory.pop_front();
    }
}

void TGra::Idz_Lub_Bij(char kierunek)
{
	Wsp &p = Ja->polozenie;
    Wsp dp = ruch[kierunek - '0'];
    int i;
    TPrzedmiot *temp;

    if(kierunek == '5')
    	return;
    if(p <<= dp) /*** RUCH W OBREBIE PLANSZY ****/
    {
        if(Plansza->Flagi(p + dp) & TU_JEST_POTWOR)
        {     /* BICIE POTWORA */
            Interfejs->Wypisz_Komunikat(ATAK);
        	Zbij_Potwora(p + dp);
        }
    	if (Plansza->Flagi(p + dp) == POLE_WOLNE)
    	{   /* RUCH PO WOLNYM POLU, LUB WYJSCIE ZE SKLEPU */
        	Plansza->akt_pole(p);
            if(Plansza->Flagi(p) == SKLEP)
            	wyczysc_liste(Plansza->Co_Tam_Jest(p));
        	p += dp;   /* zawartosc sklepu ginie po wyjsciu */
        	Interfejs->Pokaz_Mnie(p);
    	}
        else if(Plansza->Flagi(p + dp) == POLE_ZAJETE)
        	return;
        if(Plansza->Flagi(p + dp) == DOM)
        {   /* WEJSCIE DO DOMU = KONIEC GRY */
        	Interfejs->Wypisz_Komunikat(CZY_DO_DOMU, NIE_CZEKAJ);
            if(!Interfejs->Na_Pewno("", DOLACZ))
            	return;
            delete Plansza;
            while(!Potwory.empty())
            {
            	delete Potwory.front();
                Potwory.pop_front();
            }
            Sprzatanie();
            return;
        }
        if(Plansza->Flagi(p + dp) == SKLEP)
        {   /* WEJSCIE DO SKLEPU */
        	Plansza->akt_pole(p);
        	p += dp;
        	Interfejs->Pokaz_Mnie(p);

            for(i=0; i < LICZBA_TOWAROW; i++) /* Dynamiczny stan sklepu */
            {
            	temp = Generator->Daj_Przedmiot(OPROCZ_KASY);
                Plansza->Co_Tam_Jest(p).push_front(temp);
            }
            return;
		}

    }
    else         /**** RUCH NA INNA PLANSZE ****/
    {
        Zegnajcie_Potworki();
        Mapa->Zapisz(Plansza, Biezaca_Plansza);
        Biezaca_Plansza += p.Zmiana_Planszy(dp);
		Plansza = Mapa->Odczytaj(Biezaca_Plansza);
        if(!Plansza)
        	Plansza = Generator->Daj_Plansze();
        Plansza->wyswietl();
        Interfejs->Pokaz_Status(Status());
        p = p << dp;
        Interfejs->Pokaz_Mnie(p);
    }
}

void TGra::Podnoszenie()
{
	int ktory;
    Lista &l = Plansza->Co_Tam_Jest(Ja->polozenie);

    if(l.size() == 0) /* proba podnoszenia na pustym polu */
    {
    	Interfejs->Wypisz_Komunikat(NIC_TU_NIE_MA);
        return;
    }

    if(Plansza->Flagi(Ja->polozenie) == SKLEP)
    {   /* Zakupy w sklepie... */
		Interfejs->Wypisz_Tekst(Cennik(l));
    	ktory = Interfejs->Wybor(l.size());
        if(ktory == -1)
        	return;
        if(ktory == -2)
        	return;
        Ja->Kup_Przedmiot(ktory, l);
    }
    else /* podnoszenie z podlogi, nie w sklepie */
    {
		Interfejs->Wypisz_Tekst(Pokaz_Przedmioty(l));
    	ktory = Interfejs->Wybor(l.size());
        if(ktory == -1)
        	return;
        if(ktory == -2)
        	return;
        Ja->Przyswoj_Przedmiot(ktory, l);
        if(l.empty()) /* poza sklepem trzeba sie troszczyc o znak pola */
        {
        	Plansza->Znak(Ja->polozenie) = '.';
        }
        else
        {
            Plansza->Znak(Ja->polozenie) =
            	dynamic_cast<TPrzedmiot*>(l.front())->symbol;
        }
    }
    Interfejs->Pokaz_Status(Status());
}

void TGra::Upuszczanie()
{
    int ktory;
    Lista &l = Plansza->Co_Tam_Jest(Ja->polozenie);
    TPrzedmiot *temp;

    if(Ja->plecak.size() == 0)
    {
    	Interfejs->Wypisz_Komunikat(NIC_DO_ODLOZENIA);
        return;
    }

	Interfejs->Wypisz_Tekst(Pokaz_Przedmioty(Ja->plecak));
    ktory = Interfejs->Wybor(Ja->plecak.size());
    if(ktory == -1)
    	return;
    if(ktory == -2)
    	return;

    if(Plansza->Flagi(Ja->polozenie) == SKLEP)
    {
    	Ja->Sprzedaj_Przedmiot(ktory, l);
        Interfejs->Pokaz_Status(Status()); /* na pewno jestesmy bogatsi */
    }
    else
    {
	    temp = Ja->Oddaj_Przedmiot(ktory, l);
    	Plansza->Znak(Ja->polozenie) = temp->symbol;
        Interfejs->Pokaz_Status(Status()); /* cos sie moglo zmienic */
    }
}

void TGra::Maly_Teleport()
{
    if(Ja->kasa < CENA_MT)
    {
    	Interfejs->Wypisz_Komunikat(BRAK_KASY);
        return;
    }
	Plansza->akt_pole(Ja->polozenie);
    Ja->polozenie = Plansza->Daj_Wolne_Pole();
    Interfejs->Pokaz_Mnie(Ja->polozenie);
    Ja->kasa -= CENA_MT;
    Ja->masa -= CENA_MT;
    Interfejs->Pokaz_Status(Status());
}

void TGra::Duzy_Teleport()
{
    if(Ja->kasa < CENA_DT)
    {
    	Interfejs->Wypisz_Komunikat(BRAK_KASY);
        return;
    }
    TPlansza *temp;
    Wsp stare;
    stare = Biezaca_Plansza;
    temp = Mapa->Daj_Inna(Biezaca_Plansza);
    if(!temp)
    {
    	Interfejs->Wypisz_Komunikat(OK_ALE_GDZIE);
    	return;
    }
    Zegnajcie_Potworki();
    Mapa->Zapisz(Plansza, stare);
    Plansza = temp;
    Plansza->wyswietl();
    Ja->kasa -= CENA_DT;
    Ja->masa -= CENA_DT;
    Interfejs->Pokaz_Status(Status());
    Ja->polozenie = Plansza->Daj_Wolne_Pole();
    Interfejs->Pokaz_Mnie(Ja->polozenie);
}


void TGra::Modlitwa()
{
    Interfejs->Wypisz_Komunikat(MODLITWA_START, NIE_CZEKAJ);
    Sleep(500);
    if(rand() % (Ja->wiara + Ja->poboznosc) + Tura >
    	Ostatnia_Modlitwa + OKRES_MODLITWY )
    {
    	Umiesc_Przedmiot();
	    Interfejs->Wypisz_Komunikat(MODLITWA_OK);
        Ja->HP = Ja->HPmax;
        Interfejs->Pokaz_Status(Status());
        Ostatnia_Modlitwa = Tura;
    }
    else
    	Interfejs->Wypisz_Komunikat(MODLITWA_ZLE);
}



void TGra::Umiesc_Potwora()
{
	TPotwor *nowicjusz;
    nowicjusz = Generator->Daj_Potwora();
    nowicjusz->polozenie = Plansza->Daj_Wolne_Pole();
    Plansza->Flagi(nowicjusz->polozenie) = TU_JEST_POTWOR;
    Interfejs->Pokaz_Potwora(nowicjusz->polozenie, nowicjusz);
	Liczba_Potworkow++;
    Potwory.push_front(nowicjusz);
}

void TGra::Umiesc_Przedmiot()
{
	Wsp nowe;
    TPrzedmiot *nowy;
    nowe = Plansza->Daj_Wolne_Pole();
    nowy = Generator->Daj_Przedmiot();
    Plansza->Co_Tam_Jest(nowe).push_front(nowy);
    Plansza->Znak(nowe) = nowy->symbol;
    Plansza->akt_pole(nowe);
}

void TGra::Posilek()
{
    int ktore, ile;
    Lista::iterator it;
    string test = "TJedzenie";
    TJedzenie *temp;
    Lista &l = Ja->plecak;

    ile = Ile_Jedzenia(l);
    if(!ile)
    {
    	Interfejs->Wypisz_Komunikat(NIC_DO_JEDZENIA);
        return;
    }
	Interfejs->Wypisz_Tekst(Pokaz_Jedzenie(l));
    ktore = Interfejs->Wybor(ile);

    ile = 0;
    for(it = l.begin(); it != l.end(); it++)
    {
    	if( test == typeid(*(*it)).name() )
        	if(ile == ktore)
            	break;
            else
    			ile++;
    }
    temp = dynamic_cast<TJedzenie*>(*it);
    l.erase(it);
    Ja->energia += temp->kalorie;  // przybywa sily
    Ja->masa -= temp->masa;    // a torba robi sie lzejsza
    delete temp; // jedzenie zjedzone
    Interfejs->Pokaz_Status(Status());
}

void TGra::Zastosowanie()
{
    int ktore;
    Lista::iterator it;
    Lista &l = Ja->plecak;

    if(l.empty())
    {
    	Interfejs->Wypisz_Komunikat(NIC_DO_UZYCIA);
        return;
    }
	Interfejs->Wypisz_Tekst(Pokaz_Przedmioty(l));
    ktore = Interfejs->Wybor(l.size());
	it = l.begin();
    while (ktore --) it++;
    if(!strcmp(typeid(*(*it)).name(), "TArtefakt") && !(rand() % 10))
    	Zegnajcie_Potworki();
    Ja->masa -= dynamic_cast<TPrzedmiot*>(*it)->masa;
    delete *it;
    l.erase(it);
}

void TGra::Wladanie()
{
    int ktore, ile;
    Lista::iterator it;
    string test = "TBron";
    TBron *temp;
    Lista &l = Ja->plecak;

    ile = Ile_Broni(l);
    if(!ile)
    {
    	Interfejs->Wypisz_Komunikat(CO_UJAC);
        return;
    }
	Interfejs->Wypisz_Tekst(Pokaz_Bronie(l));
    ktore = Interfejs->Wybor(ile);

    ile = 0;
    for(it = l.begin(); it != l.end(); it++)
    {
    	if( test == typeid(*(*it)).name() )
        	if(ile == ktore)
            	break;
            else
    			ile++;
    }
    temp = dynamic_cast<TBron*>(*it);
    l.erase(it);
    Ja->masa -= temp->masa; // jezeli nia walczymy, nie ma jej w plecaku
    Ja->uzbrojenie = temp->atak;
    delete temp; // bron uzyta nie moze byc odlozona
    Interfejs->Pokaz_Status(Status());
}

void TGra::Potworki_Naprzod()
{
	list<TPotwor*>::iterator ppot;
    Wsp dp;
    int i,n; // do obliczania liczby atakow na ture potworka

    for(ppot = Potwory.begin(); ppot != Potwory.end(); ppot++)
    {
        n = (*ppot)->szybkosc / Ja->szybkosc;   // ile razy szybszy
        if( ((*ppot)->szybkosc % Ja->szybkosc) < (rand() % Ja->szybkosc) )
        	n++;  // ile razy wolniejszy lub reszta z szybkosci
        for(i=0; i<n; i++)
	        if((*ppot)->polozenie.Czy_Blisko(Ja->polozenie))
    	    {
        		Interfejs->Wypisz_Komunikat(TRAFIENIE);
            	if( Ja->przyjmij_atak((*ppot)->atakuj()) ) /* Juz po mnie */
	            {
    	            Interfejs->Pokaz_Status(Status());
        	    	Interfejs->Wypisz_Komunikat(SMIERC);
            	    Koniec_Gry = 1;
                	Sprzatanie();
	                break;
    	        }
        	    Interfejs->Pokaz_Status(Status());
	        }
    	    else /* Jezeli jest daleko, to goni mnie: najchetniej po skosie */
        	{
        		dp = Ja->polozenie - (*ppot)->polozenie;
	            if(Plansza->Flagi((*ppot)->polozenie + dp) != POLE_WOLNE)
    	        	continue;
    			Plansza->akt_pole((*ppot)->polozenie);
            	Plansza->Flagi((*ppot)->polozenie) &= SKLEP; /* mnozymy przez 3 */
	            (*ppot)->polozenie += dp;
    	        Plansza->Flagi((*ppot)->polozenie) |= TU_JEST_POTWOR;
        	    Interfejs->Pokaz_Potwora((*ppot)->polozenie, *ppot);
	        }
    }
}
