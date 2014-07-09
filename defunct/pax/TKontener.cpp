// Modul: TKontener.h

#include "TKontener.h"

int TKontener::wczytaj(char *nazwa)
/*  Wczytuje plansze do listy dwukierunkowej,
    ktora miala byc najpierw drzewem wielokierunkowym,
    i zwraca ich liczbe w sumie, tyle, ile ich jest
    w pliku z planszami */
{
    TKontener *temp;
    int n,i;
	ifstream wejscie(nazwa);
    wejscie >> n;
    if(n>0)
    {
    	Tutaj.wczytaj(wejscie);
        temp = this;
    }
    for(i=1; i<n; i++)
    {
        temp->N = new TKontener;
        temp->N->E = temp;
        temp = temp->N;
        temp->N = 0;
    	temp->Tutaj.wczytaj(wejscie);
    }
    return n;
}

void TKontener::usun_nast()
/*  Usuwa wszystkie nastepne "kontenery",
    ktore sie znajduja sie na polnoc od niego.
    Przy zwalnianiu pamieci. */
{
	TKontener *temp, *CU;
    temp = N;
    while(temp)
    {
       CU = temp;
       temp = temp->N;
       delete CU;
    }
}


