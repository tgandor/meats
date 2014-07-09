/****************************************************

Libconio 1.0 (C) 2004 FSL A.C.

Basado en la implementacion de conio.h escrita 
por Salvador Fernandez Barquin y adaptado a lib 
por Maximo Pech Jaramillo <makz@linuxmail.org>

Se permite su uso, copia, distribucion y modificacion 
bajo los términos de la GNU GPL versión 2.0 publicada 
por la Free Software Foundation.

*****************************************************/

#ifndef _CONIO_H
#define _CONIO_H

#ifndef _TERMIOS_H
#include <termios.h>
#endif
#ifndef _STDIO_H
#include <stdio.h>
#endif

#define ESC 033 /* Escape char */

struct textinfo
{
 int curx;
 int cury; 
};

enum
{
 BLACK,
 RED,
 GREEN,
 BROWN,
 BLUE,
 MAGENTA,
 CYAN,
 LIGHTGRAY,
 DARKGRAY,
 LIGHTRED,
 LIGHTGREEN,
 YELLOW,
 LIGHTBLUE,
 LIGHTMAGENTA,
 LIGHTCYAN,
 WHITE,
};

int getche();
int getch();
void clreol();
void clrscr();
void gotoxy(int, int);
void textcolor(int);
void textbackground(int);
int wherex();
int wherey();

#endif

