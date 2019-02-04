var
r1, r2, A, B : real ;
i : integer;

begin
    A := (3+sqrt(5)) / (2*sqrt(5));
    B := 1 - A;
    r1 := (3+sqrt(5))/2;
    r2 := (3-sqrt(5))/2;

    for i := 0 to 20000 do
    begin
      writeln(i, A + B);
      A *= r1;
      B *= r2;
    end;
end.
