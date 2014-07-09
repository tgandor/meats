// Modul: TGenerator.cpp

#include "TGenerator.h"

void TGenerator::WczytajDane(char *pl, char *stw, char *br,
							 char *zbr, char *art, char *jedz)
{
/*  Funkcja wyczytuje dane o przykladowych obiektach do generowania
	podczas gry. W argumentach znajduja sie lancuchy, ktore sa nazwami
    plikow. Poszczegolne listy generatora wypelniaja sie obiektami.
    PRZY OKAZJI, funkcja ustala liczbe plansz, ktore sa dostepne,
    (dlatego, ze jest to lista "domowej roboty" i nie ma metody "size")
    a dla przedmiotow ustala maksymalna cene (do generowania pieniedzy) */

    int i,n,cena;
    TPotwor *potw;
    TArtefakt *arte;
    TBron *brr;
    TZbroja *zbrr;
    TJedzenie *jedzen;

    Stworki.size();

	ile_plansz_mam = Zapas_Plansz.wczytaj(pl);

    ifstream stwor(stw);
    stwor >> n;
    for(i=0; i<n; i++)
    {
    	potw = new TPotwor;
    	potw->wczytaj(stwor);
        Stworki.push_back(potw);
    }
    stwor.close();

    ifstream bron(br);
    bron >> n;
    for(i=0; i<n; i++)
    {
    	brr = new TBron;
    	cena = brr->wczytaj(bron);
        if(cena > max_cena)
        	max_cena = cena;
        Bronie.push_back(brr);
    }
    bron.close();

    ifstream zbroj(zbr);
    zbroj >> n;
    for(i=0; i<n; i++)
    {
    	zbrr = new TZbroja;
    	cena = zbrr->wczytaj(zbroj);
        if(cena > max_cena)
        	max_cena = cena;
        Zbroje.push_back(zbrr);
    }
    zbroj.close();

    ifstream artef(art);
    artef >> n;
    for(i=0; i<n; i++)
    {
    	arte = new TArtefakt;
    	cena = arte->wczytaj(artef);
        if(cena > max_cena)
        	max_cena = cena;
        Artefakty.push_back(arte);
    }
    artef.close();

    ifstream je(jedz);
    je >> n;
    for(i=0; i<n; i++)
    {
    	jedzen = new TJedzenie;
    	cena = jedzen->wczytaj(je);
        if(cena > max_cena)
        	max_cena = cena;
        Jedzenie.push_back(jedzen);
    }
    je.close();
}

void TGenerator::wypisz()
/* niewykorzystywana funkcja - pozwala wypisac
   zawartosc generatora, np. w celu sprawdzenia */
{
    Lista::iterator i;
    cout << "Stworki:" << endl;
    for(i = Stworki.begin(); i != Stworki.end(); i++)
    	cout << (dynamic_cast<TPotwor*>(*i))->gatunek << endl;
	cout << "\nJedzenie:" << endl;
    for(i = Jedzenie.begin(); i != Jedzenie.end(); i++)
    	cout << dynamic_cast<TPrzedmiot*>(*i)->nazwa << endl;
	cout << "\nArtefakty:" << endl;
    for(i = Artefakty.begin(); i != Artefakty.end(); i++)
    	cout << dynamic_cast<TPrzedmiot*>(*i)->nazwa << endl;
	cout << "\nZbroje:" << endl;
    for(i = Zbroje.begin(); i != Zbroje.end(); i++)
    	cout << dynamic_cast<TPrzedmiot*>(*i)->nazwa << endl;
	cout << "\nBronie:" << endl;
    for(i = Bronie.begin(); i != Bronie.end(); i++)
    	cout << dynamic_cast<TPrzedmiot*>(*i)->nazwa << endl;
}

TGenerator::~TGenerator()
{
/*  W destruktorze sa oprozniane listy i zwalniana pamiec
	zajmowana przez obiekty (tak trzeba, poniewaz listy przechowuja
    tylko wskazniki) */

	while(Stworki.size())
    {
    	delete Stworki.front();
        Stworki.pop_front();
    }

    while(Bronie.size())
    {
    	delete Bronie.front();
        Bronie.pop_front();
    }

	while(Zbroje.size())
    {
    	delete Zbroje.front();
        Zbroje.pop_front();
    }

	while(Jedzenie.size())
    {
    	delete Jedzenie.front();
        Jedzenie.pop_front();
    }

	while(Artefakty.size())
    {
    	delete Artefakty.front();
        Artefakty.pop_front();
    }

    Zapas_Plansz.usun_nast();
}



TPlansza* TGenerator::Daj_Plansze()
/*  Zwraca wylosowana plansze */
{
	int i;
    TPlansza *wynik;
    TKontener *temp;

    temp = &Zapas_Plansz;
    /* UWAGA!!! pierwsza plansza nie moze byc ograniczona */
    /* bo nie mozna jej usunac z listy plansz wzorcowych */
    i = rand() % ile_plansz_mam;
    while(i--)
    	temp = temp->N;
    wynik = new TPlansza;
    *wynik = temp->Tutaj;
    if(temp->Tutaj.ile > 0)
    /* Zmniejszamy liczbe dla plansz ograniczonych */
    	temp->Tutaj.ile--;
    if(temp->Tutaj.ile == 0)
    /* A to byla juz ostatnia plansza tego typu */
    {
        ile_plansz_mam--; /* teraz bede miec mniej */
    	if(temp->N != 0)
        	temp->N->E = temp->E;
        if(temp->E != 0)
        	temp->E->N = temp->N;
        delete temp;   /* Zakladam, ze istnieje plansza, ktorej moze */
    }                  /* byc dowolnie duzo egzemplarzy - zreszta pierwsza*/
	return wynik;
}



TPrzedmiot* TGenerator::Daj_Przedmiot(int kase_tez)
/*  Generuja kazdy z typow przedmiotow:
	Bronie, Zbroje, Jedzenie, Artefakty i Pieniadze */
{
	Lista::iterator it;
    int i;
    Lista *l;
    TPrzedmiot *wsk;

    i = rand() % (4 + kase_tez);
    switch(i)
    {
    case 0:
    	wsk = new TArtefakt;
        l = &Artefakty;
	    i = rand() % l->size();
    	it = l->begin();
	    while(i--) it++;
    	*dynamic_cast<TArtefakt*>(wsk) = *dynamic_cast<TArtefakt*>(*it);
        break;
    case 1:
    	wsk = new TJedzenie;
        l = &Jedzenie;
    	i = rand() % l->size();
    	it = l->begin();
    	while(i--) it++;
    	*dynamic_cast<TJedzenie*>(wsk) = *dynamic_cast<TJedzenie*>(*it);
        break;
    case 2:
    	wsk = new TZbroja;
        l = &Zbroje;
    	i = rand() % l->size();
	    it = l->begin();
    	while(i--) it++;
    	*dynamic_cast<TZbroja*>(wsk) = *dynamic_cast<TZbroja*>(*it);
        break;
    case 3:
    	wsk = new TBron;
        l = &Bronie;
    	i = rand() % l->size();
	    it = l->begin();
    	while(i--) it++;
    	*dynamic_cast<TBron*>(wsk) = *dynamic_cast<TBron*>(*it);
        break;
    case 4:
    	wsk = new TPieniadze(rand() % max_cena);
        wsk->symbol = '$';
	}
    return wsk;
}

TPotwor* TGenerator::Daj_Potwora()
/*  Zwraca wskaznik na nowego potwor(k)a */
{
	int i;
    Lista::iterator it;
    TPotwor *wynik;

    i = rand() % Stworki.size();
    it = Stworki.begin();
    while(i--)
    {
    	it++;
    }
    wynik = new TPotwor;
    *wynik = *dynamic_cast<TPotwor*>(*it);
    return wynik;
}
