// Modul: TInterfejs.cpp

#include "TInterfejs.h"

char TInterfejs::Czekaj_Na_Rozkazy()
/* FUNKCJA STANDARYZUJE NACISNIETE KLAWISZE
 * to znaczy zwraca pojedynczy znak - jednoznacznie
 * identyfikujacy dany rozkaz, natomiast moze to
 * byc zwiazane z roznymi klawiszami
 */
{
	char c;
    do
    {
    	c=getch();
        if(c >= '1' && c <= '9') // kierunkowe - dobry rozkaz
        	return c;
        switch(c)
        {
            case 'h': // pomoc
            case 's': // zapis
            case 'p': // modlitwa
            case ',': // podnoszenie
            case 'e': // jedzenie
            case 'd': // upuszczanie
            case 'a': // stosowanie
            case 'w': // wladanie
            case 'q': // koniec
            case 't': // bliski teleport
            case 'T': // daleki teleport
            case 'i': // inventory
            	return c;
            case '.': // czekanie
            	return '5';
        	case 0:
            	c=getch();
                if(c > 78 && c < 82) // dol, ~ lewo, ~ prawo
                	return c - 78 + '0';
                if(c > 70 && c < 74) // gora, ~ lewo, ~ prawo
                	return c - 64 + '0';
                switch(c)
                {
                	case 75: // lewo
                    	return '4';
                    case 77: // prawo
                    	return '6';
                    case 59: // F1
                    	return 'h';
                    case 60: // F2
                    	return 's';
                    case 68: // F10
                    	return 'q';
				}
                break; // jezeli jest inny specjalny...
            case 3: // ctrl - C
            case 27: // Esc
            case 17: // ctrl - Q
            case 24: // ctrl - X
            	return 'q';
        }

    }
    while(1); // az do prawidlowego
}

void TInterfejs::pobierz_komunikaty(char *nazwa_pliku)
/* Wczytuje z pliku teksty wyswietlanych komunikatow */
{
    int i;
    string temp;
    temp = "";
	ifstream kom(nazwa_pliku);
    for(i=0; i < LICZBA_KOMUNIKATOW; i++)
    {
        kom >> komunikaty[i];
    	while(1) // wczytywanie wielu wyrazow
        {
        	kom >> temp;
            if(temp == "#")
            	break; /* opuszczamy wewnetrzna iteracje - koniec wiersza */
            komunikaty[i] += ' ';
            komunikaty[i] += temp; /* konkatenacja kolejnych wyrazow */
        }
    }
    kom.close();
}

int TInterfejs::Na_Pewno(char *pytanie, int czy_dolaczyc)
/* Potwierdzenie watpliwych rozkazow */
{
    char c;
    if(!czy_dolaczyc)
    {
    	gotoxy(1,1);
        clreol();
    }
	cout << pytanie << "(t/n)";
    c = getch();
    if(c == 't')
    	return 1;
    else
    	return 0;
}

void TInterfejs::Wypisz_Komunikat(int nr_kom, int czekaj)
/* Wypisuje chwiliwy, krotki komunikat gry */
{
	gotoxy(1,1);
    clreol();
    cout << komunikaty[nr_kom];
    if(czekaj)
    {
    	while(!kbhit());
    	gotoxy(1,1);
    	clreol();
    }
}

int TInterfejs::Wybor(int ile_mozliwosci)
/* Do stwierdzenia, ktora z opcji wybral uzytkownik */
/* Uwaga, zwraca o 1 mniej (jak tablice w C) */
/* A dla bledu: -1 */
{
	char c;
    do
    {
    	c=getch();
    }
    while( (c < 'a' && c!=27 && c!=',') || c > ('a' + ile_mozliwosci-1));
    /* Mozna nacisnac Esc, co oznacza niewybranie niczego */
    /* Lub przecinek, co oznacza wybranie wszystkiego */
    if(c == 27)
    	return -1;
    if(c == ',')
    	return -2;
    return c - 'a';
}

void TInterfejs::Wypisz_Tekst(string tekst, int czy_czekac)
/* Pozwala na wypisanie dluzszego tekstu, ze scrollowaniem
 * taki tekst trzeba potem wyczyscic...
 */
{
    int znakow = 80, linii=4, j;
    unsigned i;
	gotoxy(1,1);
    for(i=0; i < tekst.length(); i++)
    {
    	cout << tekst[i];
        znakow--;
        if(znakow == 0 || tekst[i] == '\n')
        {
        	linii--;
            if(linii == 0)
            {
            	cout << "(dalej)";
            	getch();
                Wyczysc_Tekst();
                linii = 4;
            }
            znakow = 80;
        }
    }
    gotoxy(1,5);
    cout << "       "; /* usuniecie napisu dalej */
    if(czy_czekac)
    	getch();
}

void TInterfejs::Wyczysc_Tekst()
/* Usuwa efekty wykonania metody Wypisz_Tekst() */
{
	for(int j=4; j>=1; j--)
    {
    	gotoxy(1,j);
        clreol();
    }
}

void TInterfejs::Pokaz_Status(string status)
/* Czysci linie na dole ekranu i wypisuje w nich przekazany
 * w parametrze status
 */
{
	gotoxy(1, 21); clreol();
    gotoxy(1, 22); clreol();
    gotoxy(1, 21);
    cout << status;
}

void TInterfejs::Pokaz_Ture(int tura)
/* Do wypisywania numeru biezacej tury */
{
	gotoxy(44, 23);
    cout << "Tura: " << tura;
    Wyczysc_Tekst();
}

void TInterfejs::Pokaz_Mnie(Wsp gdzie)
/* Umieszcza na ekranie symbol glownego bohatera */
{
	gotoxy(gdzie.x+10, gdzie.y+5);
    cout << '@';
	gotoxy(gdzie.x+10, gdzie.y+5);
}

void TInterfejs::Pokaz_Potwora(Wsp gdzie, TPotwor* co)
/* Wyswietlenie na ekranie postaci jakiegos potworka */
{
	gotoxy(gdzie.x+10, gdzie.y+5);
    cout << co->symbol;
}
