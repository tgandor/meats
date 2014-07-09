// Modul: TGra.cpp

/*
	IMPLEMENTUJE:
int TGra::Wybor_Postaci(char *nazwa)
void TGra::Jakie_Imie()
int TGra::Wczytywanie()
void TGra::Inicjalizuj()
void TGra::Tocz_Sie()
void TGra::Wykonaj_Rozkaz(char rozkaz)
void TGra::Rezygnacja()
void TGra::Zapisanie()
string TGra::Status()
*/

#include "TGra.h"


const string help =
"Dostepne polecenia:\n\
	q, Esc, F10, Ctrl-q, Ctrl-c, Ctrl-x - wyjscie z gry\n\
    s, F2 - zapisanie stanu i wyjscie\n\
    h, F1 - wyswietlenie pomocy (tego) \n\
    PORUSZANIE SIE: Strzalki lub NumPad (skosy!)\n\
    5, . - czekanie w miejscu (nic nierobienie)\n\
    w - branie broni do reki\n\
 	, - podnoszenie i kupowanie w sklepach\n\
    d - upuszczanie i sprzedawanie w sklepach\n\
    i - (inventory) co mam w plecaku?\n\
    a - uzywanie przedmiotow\n\
    e - jedzenie tego, co mozna zjesc\n\
    T - teleportacja dalekiego zasiegu\n\
    t - teleportacja krotkiego zasiegu\n\
    p - modlitwa\n\
Milej zabawy!";


int TGra::Wybor_Postaci(char *nazwa)
/* Wybor postaci sposrod znalezionych w pliku o nazwie
 * podanej w parametrze - chodzi o rozne profesje
 */
{
    int i,n;
    char c = 'a',d;
    TJa *temp;
    Lista lboh;
    Lista::iterator it;
	ifstream hero(nazwa);
    hero >> n;
    for(i=0; i<n; i++)
    {
        temp = new TJa;
        temp->wczytaj(hero);
        lboh.push_back(temp);
    }
    cout << "    Wybierz jedna z profesji:   (Esc = wczytaj gre)\n" << endl;
    for(it = lboh.begin(); it != lboh.end(); it++)
    {
    	temp = dynamic_cast<TJa*> (*it);
		cout << "        " << c << ". " << temp->profesja << endl;
    	c++;
    }
    cout << "\n     Nacisnij: a.." << --c << endl;
    while( (( d=getch() ) < 'a' && d != 27) || (d > c) );
    if(d == 27)
    	return 1;
    for(i='a'; i<d; i++)
    {
    	delete lboh.front();
        lboh.pop_front();
    }
    Ja = dynamic_cast<TJa*> ( lboh.front() );
    lboh.pop_front();
    for( ; i < c; i++)
    {
    	delete lboh.front();
        lboh.pop_front();
    }
    return 0;
}

void TGra::Jakie_Imie()
/* Pytanie o imie / nicka dla gracza, ktory bedzie
 * takze jego katalogiem tymczasowym. Przyzwoite imie
 * to takie, ktore ma do 29 znakow i mozna utworzyc
 * taki katalog
 */
{
    int i;
    string buf;
	cout << "\n\n\tJak sie nazywasz? ";
    cin >> buf;
    for(i=0; (i<29) && (buf[i]); i++)
    	imie[i] = buf[i];
    imie[i]=0;
    while(mkdir(imie))
    {
    	cout << "\tTo imie nie jest przyzwoite. Podaj inne> ";
	    cin >> buf;
    	for(i=0; i<29 && buf[i]; i++)
    		imie[i] = buf[i];
    	imie[i]=0;
    }
    chdir(imie);
}

int TGra::Wczytywanie()
/* Pytanie o imie / nicka dla gracza, ktory jest
 * takze jego katalogiem tymczasowym. Katalog musi istniec.
 */
{
    int i;
    string buf;
	cout << "\n\n\tJak sie nazywasz? ";
    cin >> buf;
    for(i=0; (i<29) && (buf[i]); i++)
    	imie[i] = buf[i];
    imie[i]=0;
    while( chdir(imie) && strcmp(imie, "?") )
    {
    	cout << "\tNie znam Cie. Powtorz lub wpisz '?' > ";
	    cin >> buf;
    	for(i=0; i<29 && buf[i]; i++)
    		imie[i] = buf[i];
    	imie[i]=0;
    }
    if( !strcmp(imie, "?") )
    	return 1; /* uzytkownik sie poddal */

	string nazwa = imie; nazwa += ".sav";  /* plik ma takie rozszerzenie */
    ifstream save(nazwa.c_str());
    if(!save)
    	return 1; /* jest folder, ale nie ma pliku */
    Mapa->pobierz(save); /* wczytywanie listy plansz, ktore sa na dysku */
    Ja = new TJa;
    Ja->przywroc(save);  /* wczytywanie danych o sobie */
    Biezaca_Plansza.wczytaj(save); /* na ktorej planszy stanelo? */
    save >> Tura;  /* jaki byl numer tury? */
    save.close();

    Plansza = Mapa->Odczytaj(Biezaca_Plansza);
    Plansza->wyswietl();
    Interfejs->Pokaz_Mnie(Ja->polozenie);
    Interfejs->Pokaz_Status(Status());

	return 0;
}

void TGra::Inicjalizuj()
/* Grupa czynnosci, ktore sa wykonywane tylko raz -
 * na poczatku gry. Np. ustawienie domu, czyli miejsca
 * gdzie mozna zakonczyc gre "dobrowolnie", oraz komunikat
 * powitalny na poczatku gry...
 */
{
    randomize();
	Plansza = Generator->Daj_Plansze();
    Ja->polozenie = Plansza->Ustaw_Dom();
    Plansza->wyswietl();
    Ja->tura();
    Interfejs->Pokaz_Status(Status());
    Interfejs->Pokaz_Mnie(Ja->polozenie);
    Interfejs->Wypisz_Komunikat(WITAJ_W_PAX);
}

void TGra::Tocz_Sie()
{
	while(!Koniec_Gry)
    {
    	Tura++;
        if(!(Tura % OKRES_POTWOROW))
        	Umiesc_Potwora();
        if(!(Tura % OKRES_PRZEDMIOTOW))
        	Umiesc_Przedmiot();
        if(Ja->tura())
        	Sprzatanie();
        else
        {
	    	Interfejs->Pokaz_Ture(Tura);
    		Wykonaj_Rozkaz(Interfejs->Czekaj_Na_Rozkazy());
        	Potworki_Naprzod();
        }
    }
}

void TGra::Wykonaj_Rozkaz(char rozkaz)
/* funkcja ta wykonuje rozkazy (przekazuje sterowanie),
 * czyli przeprowadza czynnosci dostepne dla gracza,
 * poprzez inne funkcje
 */
{
	if(rozkaz > '0' && rozkaz <= '9')
        Idz_Lub_Bij(rozkaz);
    else if(rozkaz == 'T')
        Duzy_Teleport();
    else if(rozkaz == 't')
    	Maly_Teleport();
    else if(rozkaz == 'h')
    {
		Interfejs->Wypisz_Tekst(help, CZEKAJ);
    }
    else if(rozkaz == ',')
    	Podnoszenie();
    else if(rozkaz == 'd')
    	Upuszczanie();
    else if(rozkaz == 'q')
    	Rezygnacja();
    else if(rozkaz == 's')
    	Zapisanie();
    else if(rozkaz == 'p')
    	Modlitwa();
    else if(rozkaz == 'i')
    	Interfejs->Wypisz_Tekst(
        	Pokaz_Przedmioty(Ja->plecak), CZEKAJ);
    else if(rozkaz == 'e')
    	Posilek();
    else if(rozkaz == 'a')
    	Zastosowanie();
    else if(rozkaz == 'w')
    	Wladanie();
}


void TGra::Rezygnacja()
{

    if(!Interfejs->Na_Pewno("Czy na pewno chcesz zrezygnowac?"))
    	return;
    Sprzatanie();
}

void TGra::Zapisanie()
{
	string nazwa = imie; nazwa += ".sav";
    if(!Interfejs->Na_Pewno("Czy na pewno chcesz zapisac?"))
    	return;
	Koniec_Gry = 1;

    Mapa->Zapisz(Plansza, Biezaca_Plansza);

    ofstream save(nazwa.c_str());
    Mapa->zachowaj(save);
    Ja->zachowaj(save);
    Biezaca_Plansza.zapisz(save);
    save << Tura << endl;
    save.close();

    system("cls");
    system("pause");
}

void TGra::Sprzatanie()
/*  FUNKCJA brutalnie usuwajaca pliki z roboczego katalogu,
	oraz ustawiajaca zmienna koniec gry, co powoduje zakonczenie
    programu. Nalezy uwazac, zeby tej funkcji nie uruchomic
    w innym katalogu niz tymczasowy (np. w takim, w ktorym sa
    zrodla, bo trzeba bedzie ja napisac od nowa) */
{

	Zegnajcie_Potworki();
    system("cls");
	Koniec_Gry = 1;
    system("del /q *.*");
    chdir("..");
    rmdir(imie);

    /* Czasem warto skorzystac ze starego stdio */
    FILE *log = fopen("log.txt", "a+");
    fprintf(log, "%s\t%s\t-\t%d pkt.\n", imie, Ja->profesja, Punkty);
    fclose(log);
    /* To zamiast listy top 100 - po prostu nieposortowane wyniki */

    system("pause");

}

string TGra::Status()
/* Zwraca caly status jednostki, to co sie zawsze wyswietla
 * na dole ekranu: ilosc HP, zloto, sila, obciazenie itd.
 */
{
	string wynik;
    char buf[30];
    wynik = imie;
    wynik += " - ";
    wynik += Ja->profesja;
    wynik += "   Sila: ";
    wynik += itoa(Ja->sila + Ja->wzmocnienie, buf, 10);
    wynik += "   Konstytucja: ";
    wynik += itoa(Ja->konstytucja + Ja->hart, buf, 10);
    wynik += "   AC: ";
    wynik += itoa(Ja->opancerzenie, buf, 10);
    wynik += "\nPlansza: ";
    wynik += Biezaca_Plansza.w_nawiasach();
    wynik += "   $: ";
    wynik += itoa(Ja->kasa, buf, 10);
	wynik += "   HP: ";
    wynik += itoa(Ja->HP, buf, 10);
    wynik += "(";
    wynik += itoa(Ja->HPmax, buf, 10);
    wynik += ")  Wiara: ";
    wynik += itoa(Ja->wiara + Ja->poboznosc, buf, 10);
    if(Ja->glod == GLODNY)
    	wynik += "  Glodny";
    else if(Ja->glod == PRZEJEDZONY)
    	wynik += "  Przejedzony";
    if(Ja->obciazenie > PRZECIAZONY)
    	wynik += "  B. Ciezko!";
    else if(Ja->obciazenie > DOCIAZONY)
		wynik += "  Ciezko.";
    return wynik;
}
