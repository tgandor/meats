stats '/tmp/power_now.dat' using 1 prefix 'P'
set yrange [P_min-1:P_max+1]
plot '/tmp/power_now.dat', P_mean with lines
pause 3
reread
