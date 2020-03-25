set output 'rymy.png'
set terminal png
set yrange [0:10]
unset key
plot '12345.gnuplot' using 1:2 lt rgb "red" with steps, \
'12345.gnuplot' using 1:3 lt rgb "red" with steps, \
'12345.gnuplot' using 1:4 lt rgb "red" with steps, \
'12345.gnuplot' using 1:5 lt rgb "blue" with steps
