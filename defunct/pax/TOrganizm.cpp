// Modul: TOrganizm.cpp

#include "TOrganizm.h"

int TJa::tura()
{
	energia -= EGZYSTENCJA;

    if(energia <= 0 || energia > GRANICA_PRZEJEDZENIA)
    	return 1;
    if(energia < GRANICA_GLODU)
        glod = GLODNY;
    else if(energia < GRANICA_SYTOSCI)
    	glod = SYTY;
    else
    	glod = PRZEJEDZONY;
    obciazenie = masa / WSPOLCZYNNIK_SILY;
    if(obciazenie > GRANICA)
	    return 1;
    energia -= obciazenie; // dla lekkiego 0
    if(HP < HPmax)
    	HP += rand() % konstytucja % (HPmax - HP);
    return 0;
}

int TPotwor::tura()
{
	return 0;
}

void TJa::wczytaj(ifstream &str)
/* Tutaj wczytujemy tylko wzorzec z pliku z wzorcami */
{
        str.getline(profesja,29);
        str.getline(profesja,29);
        str >> HPmax;
        HP = HPmax;
        str >> sila;
        str >> konstytucja;
        str >> wiara;
        szybkosc = 100;
}

void TPotwor::wczytaj(ifstream &str)
/* Tutaj wczytujemy tylko wzorzec z pliku z wzorcami */
{
        str.getline(gatunek,29);
        str.getline(gatunek,29);
        str >> HPmax;
        HP = HPmax;
        str >> sila;
        str >> konstytucja;
        str >> szybkosc;
        str >> rasa;
        str >> nastawienie;
        if(rasa == CZLOWIEK)
        	symbol = '@';
        else
        	str >> symbol;
}

void TJa::zachowaj(ofstream &str)
/* Zapisanie postaci do pozniejszego odczytania */
{
	str << profesja << endl;
    str << HPmax << endl;
    str << HP << endl;
    str << sila << endl;
    str << konstytucja << endl;
    str << wiara << endl;
    str << szybkosc << endl;
    str << kasa << endl;
    str << masa << endl;
    str << energia << endl;
    str << uzbrojenie << endl;
    str << opancerzenie << endl;
    str << przyspieszenie << endl;
    str << metabolizm << endl;
    str << wzmocnienie << endl;
    str << hart << endl;
    str << poboznosc << endl;
    str << obciazenie << endl;
    str << glod << endl;
    polozenie.zapisz(str);
    zapisz_liste(plecak, str);
}

void TJa::przywroc(ifstream &str)
/* Przywracanie dokladnego stanu postaci: zob. powyzsza funkcja */
{
	str >> profesja;
    str >> HPmax;
    str >> HP;
    str >> sila;
    str >> konstytucja;
    str >> wiara;
    str >> szybkosc;
    str >> kasa;
    str >> masa;
    str >> energia;
    str >>  uzbrojenie;
    str >>  opancerzenie;
    str >>  przyspieszenie;
    str >>  metabolizm;
    str >>  wzmocnienie;
    str >>  hart;
    str >>  poboznosc;
    str >>  obciazenie;
    str >>  glod;
    polozenie.wczytaj(str);
    wczytaj_liste(plecak, str);
}

void TJa::Przyswoj_Przedmiot(int ktory, Lista &skad)
/* Zwyczajne podnoszenie przedmiotu z listy - zawartosci pustego pola */
{
    Lista::iterator it;
	TPrzedmiot *co;

	if(ktory >= skad.size())
    	return;

    it = skad.begin();
    while(ktory--) it++;
    co = dynamic_cast<TPrzedmiot*>(*it);
    skad.erase(it);

    if(!strcmp(typeid(*co).name(), "TPieniadze"))
    {
        int temp = dynamic_cast<TPieniadze*>(co)->kwota;
    	kasa += temp;
        masa += temp;
        delete co; /* wyrzucamy sakiewke... */
        return;
    }
    if(!strcmp(typeid(*co).name(), "TZbroja")) /* zbroja nam dodaje DV */
    {
    	opancerzenie += dynamic_cast<TZbroja*>(co)->obrona;
    }
    else if(!strcmp(typeid(*co).name(), "TArtefakt"))
    {   /* artefakt nas wzmacnia przez sam fakt */
    	TArtefakt *temp = dynamic_cast<TArtefakt*>(co);
		przyspieszenie += temp->szybkosc;
		metabolizm += temp->energia;
		wzmocnienie += temp->sila;
		hart += temp->konstytucja;
		poboznosc += temp->wiara;
    }
    plecak.push_back(co);
    masa += co->masa;
}


int TJa::Kup_Przedmiot(int ktory, Lista &gdzie)
/* Podnosimy sobie n-ty przedmiot, ale pieniedzy ubywa
   - to jest kupowanie... */
{
    Lista::iterator it;
    TPrzedmiot *co;

	if(ktory >= gdzie.size())
    	return 1;

    it = gdzie.begin();
    while(ktory--) it++;
    co = dynamic_cast<TPrzedmiot*>(*it);

    if(co->cena > kasa)
		return 1;

    gdzie.erase(it);
    if(!strcmp(typeid(*co).name(), "TZbroja")) /* zbroja nam dodaje DV */
    {
    	opancerzenie += dynamic_cast<TZbroja*>(co)->obrona;
    }
    else if(!strcmp(typeid(*co).name(), "TArtefakt"))
    {   /* artefakt nas wzmacnia przez sam fakt */
    	TArtefakt *temp = dynamic_cast<TArtefakt*>(co);
		przyspieszenie += temp->szybkosc;
		metabolizm += temp->energia;
		wzmocnienie += temp->sila;
		hart += temp->konstytucja;
		poboznosc += temp->wiara;
    }
    plecak.push_back(co);
    masa += co->masa;
    kasa -= co->cena; /* zaplata */
    return 0;
}

TPrzedmiot* TJa::Oddaj_Przedmiot(int ktory, Lista &gdzie)
{
    Lista::iterator it;
    TPrzedmiot *wynik;
    if(ktory >= plecak.size())
		return 0;
    it = plecak.begin();
    while(ktory--) it++;
    wynik = dynamic_cast<TPrzedmiot*>(*it);
    plecak.erase(it);
    gdzie.push_front(wynik);
    masa -= wynik->masa;
    if(!strcmp(typeid(*wynik).name(), "TZbroja")) /* zbroja nam dodaje DV */
    {
    	opancerzenie -= dynamic_cast<TZbroja*>(wynik)->obrona;
    }
    else if(!strcmp(typeid(*wynik).name(), "TArtefakt"))
    {   /* artefakt nas wzmacnia przez sam fakt */
    	TArtefakt *temp = dynamic_cast<TArtefakt*>(wynik);
		przyspieszenie -= temp->szybkosc;
		metabolizm -= temp->energia;
		wzmocnienie -= temp->sila;
		hart -= temp->konstytucja;
		poboznosc -= temp->wiara;
    }
    return wynik;
}

TPrzedmiot* TJa::Sprzedaj_Przedmiot(int ktory, Lista &gdzie)
{
    Lista::iterator it;
    TPrzedmiot *wynik;

    if(ktory >= plecak.size())
		return 0;

    it = plecak.begin();
    while(ktory--) it++;
    wynik = dynamic_cast<TPrzedmiot*>(*it);
    plecak.erase(it);
    gdzie.push_front(wynik);
    kasa += wynik->cena;
    masa += wynik->cena;
    masa -= wynik->masa;
    if(!strcmp(typeid(*wynik).name(), "TZbroja")) /* zbroja nam dodaje DV */
    {
    	opancerzenie -= dynamic_cast<TZbroja*>(wynik)->obrona;
    }
    else if(!strcmp(typeid(*wynik).name(), "TArtefakt"))
    {   /* artefakt nas wzmacnia przez sam fakt */
    	TArtefakt *temp = dynamic_cast<TArtefakt*>(wynik);
		przyspieszenie -= temp->szybkosc;
		metabolizm -= temp->energia;
		wzmocnienie -= temp->sila;
		hart -= temp->konstytucja;
		poboznosc -= temp->wiara;
    }
    return wynik;
}

int TJa::przyjmij_atak(int punkty_ataku)
{
	int szczescie = rand();
    if(punkty_ataku - szczescie % (konstytucja + opancerzenie) > 0)
    	HP -= punkty_ataku - szczescie % (konstytucja + opancerzenie);
    if(HP > 0)
		return 0;
    return 1;
}

int TPotwor::przyjmij_atak(int punkty_ataku)
{
	int szczescie = rand();
    if(punkty_ataku - szczescie % konstytucja > 0)
    	HP -= punkty_ataku - szczescie % konstytucja;
    if(HP > 0)
		return 0;
    return 1;
}

int TJa::atakuj()
{
	return rand() % (sila + uzbrojenie + wzmocnienie);
}

int TPotwor::atakuj()
{
	return rand() % sila;
}


