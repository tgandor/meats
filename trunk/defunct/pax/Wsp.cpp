// Modul: Wsp.cpp

#include "Wsp.h"

#include <string.h>
#include <stdlib.h>

Wsp Wsp::operator+ (Wsp value)
/* dodanie odpowiednich wspolrzednych do siebie */
{
	Wsp wynik;
    wynik.x = x + value.x;
    wynik.y = y + value.y;
    return wynik;
}

Wsp Wsp::operator <<  (Wsp value)
/* przesuniecie sie o value - jezeli wykracza to poza
 * rozmiar planszy - wowczas nastepuje zawiniecie i przejscie
 * na drugi koniec - ale moze to juz byc inna plansza...
 */
{
	Wsp wynik;

    wynik.x = x + value.x;
    if(wynik.x > 59)
    	wynik.x = 0;
    else if(wynik.x < 0)
    	wynik.x = 59;

    wynik.y = y + value.y;
    if(wynik.y > 14)
    	wynik.y = 0;
    else if(wynik.y < 0)
    	wynik.y = 14;

    return wynik;
}

int Wsp::operator == (Wsp value)
/* zwykly operator porownania obydwu pol */
{
	if(x == value.x && y==value.y)
    	return 1;
    else
    	return 0;
}

int Wsp::Czy_Blisko(Wsp value)
{
	if( (abs(x-value.x) < 2) && (abs(y-value.y) < 2) )
    	return 1;
    return 0;
}


Wsp Wsp::operator- (Wsp value)
{
	Wsp wynik;

    if(x == value.x)
    	wynik.x = 0;
    else if(x > value.x)
    	wynik.x = 1;
    else
    	wynik.x = -1;

    if(y == value.y)
    	wynik.y = 0;
    else if(y > value.y)
    	wynik.y = 1;
    else
    	wynik.y = -1;

    return wynik;
}

Wsp Wsp::Zmiana_Planszy(Wsp value)
/* Zwraca wspolrzedne, o ktore zmieni sie plansza
 * po wykonaniu ruchu przekazywanego w parametrze:
 * jezeli nic sie nie zmieni, to otrzymamy {0,0},
 * a np. jezeli przejdziemy o 1 plansze w prawo: {1,0}
 * w dol {0,1} itd.
 */
{
	Wsp wynik;
    wynik.x = 0;
    wynik.y = 0;

    if (x + value.x > 59)
    	wynik.x = 1;
    else if(x + value.x < 0)
    	wynik.x = -1;
    if (y + value.y  > 14)
    	wynik.y = 1;
    else if (y + value.y < 0)
    	wynik.y = -1;
    return wynik;
}

const char* Wsp::nazwa_pliku()
/* zwraca nazwe pliku, ktory bedzie tymczasowo
 * przechowywal plansze o podanych wspolrzednych:
 * stad pl_ (plansza) i nastepnie m/p <liczba>
 * m/p <liczba> - m ^= minus, p ^= plus
 */
{
    static char buf[60];
    char temp[30];
    strcpy(buf,"pl_");
    if(x < 0)
    	strcat(buf,"m");
    else
    	strcat(buf,"p");
    strcat(buf, itoa(abs(x), temp, 10) );
    if(y < 0)
    	strcat(buf,"m");
    else
    	strcat(buf,"p");
	strcat(buf, itoa(abs(y), temp, 10) );
    return buf;
}

char* Wsp::w_nawiasach()
/* zwraca wspolrzedne w zapisie nawiasowym -
 * np. do statusu, gdzie bedzie takze biezaca plansza
 */
{
    static char buf[30];
    char temp[30];
    strcpy(buf,"(");
    strcat(buf, itoa(x, temp, 10) );
   	strcat(buf,", ");
	strcat(buf, itoa(y, temp, 10) );
   	strcat(buf,")");
    return buf;
}

void Wsp::wczytaj(ifstream &str)
{
	str >> x;
    str >> y;
}

void Wsp::zapisz(ofstream &str)
{
	str << x << endl;
    str << y << endl;
}



