Program Samotnik;

Uses
  crt;      (* biblioteka procedur ekranu *)

Var
  P: array [1..50] of string; (* tablica na plansze - 2 wymiarowa znakow *)
  F: text;                    (* zmienna plikowa - do wczytania planszy *)
  i, j, n,                     (* zmienne pomocnicze *)
  x, y : integer;              (* wspolrzedne na planszy *)
  c, e: char;                  (* znaki do wczytywania z klawiatury *)
  zazn : boolean;              (* mowi nam, czy udalo sie zaznaczyc pole *)

procedure wczytaj_plansze;
(* pobiera poczatkowa plansze z pliku plansza.txt *)
begin
  assign(F, 'plansza.txt');
  reset(F);
  readln(F, n);

  for i := 1 to n do
    readln(F, p[i]);

  close(F);
end;

procedure odswiez(k, l: integer);
(* aktualizuje na ekranie pojedyncze pole *)
begin
  gotoxy(k, l);
  write(p[k,l]);
  gotoxy(k, l);
end;

procedure pokaz_plansze;
(* wyswietla - odswieza - cala plansze *)
begin
  clrscr;                        (*czyszczenie ekranu*)
  for i := 1 to n do
    for j:= 1 to n do
    odswiez(i, j);
end;

procedure ruch(v, w: integer);
(* ruch kursora po ekranie, parametry: zmiana wspolrzednych *)
begin
  if (x+w > 0) and (x+w < n+1) and (y+v > 0) and (y+v < n+1) then
    if p[x+w, y+v] <> '#' then
    begin
    x:= x + w;               (*zmiana wspolrzednych*)
    y:= y + v;
    gotoxy(x, y)
    end;       (*zmiana polozenia*)
end;

procedure gdzie;
(* na podstawie kodu wcisnietego klawisza przemieszcza kursor *)
begin
      case c of                (*na klawiaturze num*)
           '8', #72: ruch(-1, 0);         (*gora*)
           '2', #80: ruch(1, 0);         (*dol*)
           '4', #75: ruch(0, -1);         (*lewo*)
           '6', #77: ruch(0, 1);        (*prawo*)
           '7', #71: ruch(-1,-1);
           '9', #73: ruch(-1, 1);
           '1', #79: ruch(1, -1);
           '3', #81: ruch(1, 1);
      end;
end;

procedure odznacz;
(* przywraca zaznaczone pole do stanu pierwotnego *)
begin
    p[x, y]:= 'o';
    zazn := false;
    odswiez(x, y);
end;

procedure pobierz;
(* reaguje na zadanie ruchu uzytkownika, wykonuje ruch *)
(* lub odznacza pole w przypadku rezygnacji / bledu    *)
begin
case e of
          '8', #72: begin
                     if (p[x, y-1]='o') and (p[x, y-2]='.') then
                     begin
                        p[x, y]:= '.';
                        odswiez(x, y);
                        p[x, y-1]:='.';
                        odswiez(x, y-1);
                        ruch(-2, 0);
                        p[x, y]:= 'o';
                        odswiez(x, y);
                     end
                     else
                       odznacz;
                    end;         (*gora*)
          '2', #80: begin
                     if (p[x, y+1]='o') and (p[x, y+2]='.') then
                        begin
                        p[x, y]:= '.';
                        odswiez(x, y);
                        p[x, y+1]:='.';
                        odswiez(x, y+1);
                        ruch(2, 0);
                        p[x, y]:= 'o';
                        odswiez(x, y);
                        end
                        else
                          odznacz;
                       end;        (*dol*)
          '4', #75: begin
                     if (p[x-1, y]='o') and (p[x-2, y]='.') then
                        begin
                        p[x, y]:= '.';
                        odswiez(x, y);
                        p[x-1, y]:='.';
                        odswiez(x-1, y);
                        ruch(0, -2);
                        p[x, y]:= 'o';
                        odswiez(x, y);
                        end
                        else
                          odznacz;
                       end;         (*lewo*)
          '6', #77: begin
                     if (p[x+1, y]='o') and (p[x+2, y]='.') then
                        begin
                        p[x, y]:= '.';
                        odswiez(x, y);
                        p[x+1, y]:='.';
                        odswiez(x+1, y);
                        ruch(0, 2);
                        p[x, y]:= 'o';
                        odswiez(x, y);
                        end
                        else
                          odznacz;
                              (*prawo*)
                      end;
           otherwise odznacz; (* gnu pascal *)
           { default: odznacz; (* borland pascal, delphi *) }
          end;
end;

procedure zaznacz;
(* zaznacza dane pole *)
begin
  if p[x, y] = 'o' then
  begin
    p[x, y]:= '0';
    zazn := true;
    odswiez(x, y);
  end;
end;

(* PROGRAM GLOWNY *)
Begin

clrscr;
wczytaj_plansze;
pokaz_plansze;
gotoxy(1,24);
writeln('Aleksandra Grabiec, gr. 1, Matematyka sem. VI, magisterskie');
write('Sterowanie: strzalki lub numpad, Enter - wybor pola, Esc - wyjscie');

x := 4;
y := 4;
zazn := false;
gotoxy(x, y);                  (*polozenie poczatkowe*)

repeat   (* poczatek petli nieskonczonej *)

  repeat
    repeat
      c := readkey;            (*wczytanie znaku*)

      if ord(c) = 0 then
        c := readkey;
      if ord(c) = 27 then       (* punkt wyjscia z programu *)
        halt;
      gdzie;                    (* poruszanie sie po planszy *)
    until (ord(c) = 13);        (* wybor kamyka *)
    zaznacz;
  until zazn;

  e := readkey;
   if ord(e) = 0 then
     e := readkey;
   pobierz;                    (* analiza i ew. wykonanie zadanego ruchu *)

until false;  (* koniec petli nieskonczonej *)

End.
