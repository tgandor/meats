// Naglowek Wsp.h:
/* STRUKTURA: Wsp
 * Jest to zwykla struktura 2 wspolrzednych, wzbogacona
 * o pewne funkcje czlonkowskie, np. operatory dodawania
 * lub operatory testowania przesuniecia <<=, lub przesuwania <<
 * w przestrzeni modularnej
 */

#ifndef WspH
#define WspH

#include <stdlib.h>
#include <fstream>

#include "itoa.hpp"

/* WSPOLRZEDNE */
struct Wsp
{
	int x,y;
    Wsp operator+= (Wsp value)
    /* zwykla operacja dodawania z przypisaniem */
    {
    	x+=value.x;
        y+=value.y;
        return *this;
    }
    int operator <<= (Wsp value)
    /* operator odpowiada na pytanie:
     * "Czy po przesunieciu sie o wspolrzedne value
     * bede nadal znajdowac sie na tej samej planszy
     */
    {
    	int X,Y;
        X = x + value.x;
        Y = y + value.y;
        if(X < 0 || X > 59 || Y < 0 || Y > 14)
        	return 0;
        else
        	return 1;
    }
    Wsp operator+ (Wsp value);
    Wsp operator << (Wsp value);
    int operator == (Wsp value);
    Wsp operator- (Wsp value);
    int Czy_Blisko(Wsp value);
    Wsp Zmiana_Planszy(Wsp value);
    const char *nazwa_pliku();
    char *w_nawiasach();
    void wczytaj(std::ifstream &str);
    void zapisz(std::ofstream &str);

};

#endif
