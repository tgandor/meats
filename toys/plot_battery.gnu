set yrange [20:35]
stats '/tmp/power_now.dat' using 1 prefix 'P'
plot '/tmp/power_now.dat', P_mean with lines
pause 3
reread
