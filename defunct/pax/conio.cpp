/****************************************************

Libconio 1.0 (C) 2004 FSL A.C.

Basado en la implementacion de conio.h escrita 
por Salvador Fernandez Barquin y adaptado a lib 
por Maximo Pech Jaramillo <makz@linuxmail.org>

Se permite su uso, copia, distribucion y modificacion 
bajo los términos de la GNU GPL versión 2.0 publicada 
por la Free Software Foundation.

*****************************************************/

#include "conio.h"

struct textinfo text={0, 0};

int getche()
{
        struct termios t;
        int c;

	tcgetattr(0,&t);
        t.c_lflag&=~ICANON;
        tcsetattr(0,TCSANOW,&t);
        fflush(stdout);
        c=getchar();
        t.c_lflag|=ICANON;
        tcsetattr(0,TCSANOW,&t);
        return c;
}

int getch()
{
        struct termios t;
        int c;

        tcgetattr(0,&t);
        t.c_lflag&=~ECHO+~ICANON;
        tcsetattr(0,TCSANOW,&t);
        fflush(stdout);
        c=getchar();
        t.c_lflag|=ICANON+ECHO;
        tcsetattr(0,TCSANOW,&t);
        return c;
}

void gotoxy(int x, int y)
{
printf("%c[%d;%dH", ESC, y, x);
text.curx = x;
text.cury = y;
}

void clreol()
{
printf("%c[K", ESC);
}

void clrscr(void)
{
printf("%c[2J", ESC);
gotoxy(0, 0);
}

void textcolor(int color)
{
if(color >= BLACK && color <= LIGHTGRAY ) /* dark color */
 printf ("%c[0;%dm", ESC, 30+color);
else	
 printf("%c[1;%dm", ESC, 30+(color-8));
}

void textbackground(int color)
{
printf ("%c[%dm", ESC, 40+color);
}
 
int wherex(void)
{
 return text.curx;
}

int wherey(void)
{
 return text.cury;
}
