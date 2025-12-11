set term postscript eps enhanced
set output 'Fe.band_dos.png'
set multiplot

xmin=0.0 ; xmax=2.131934
ymin=-10 ; ymax=10
G1=xmin ; H = 1.005738;N=1.826919;G2=2.407583;P=2.910452;H2=3.873372;P2=4.836293;N2=5.339162


set nokey
set title "                  Band structure and DOS of Fe"
set size 0.6,1.0
set rmargin 0
set xrange [xmin:xmax]
set yrange [ymin:ymax]
set arrow from H, ymin to  H,ymax nohead lt 5 lw 1
set arrow from N, ymin to  N,ymax nohead lt 5 lw 1
set arrow from G2, ymin to  G2,ymax nohead lt 5 lw 1
set arrow from P, ymin to  P,ymax nohead lt 5 lw 1
set arrow from H2, ymin to  H2,ymax nohead lt 5 lw 1
set arrow from P2, ymin to  P2,ymax nohead lt 5 lw 1
set arrow from N2, ymin to  N2,ymax nohead lt 5 lw 1
set ylabel 'E - E_F (eV)'
set xtics ('{/Symbol G}' G1,'H' H, 'N' N,'{/Symbol G}' G2, 'P' P, 'H' H2, 'P' P2, 'N' N2,)
set ytics ymin,2,ymax font 'Helvetica, 12'
plot 'bands.dat' u 1:($2+4.2654) w lines lw 2

set title " "
set origin 0.6,0
set lmargin 0.5
set size 0.35,1.0
set yr[-10:10]
set xr[0:0.85]
set noarrow
set ytics ( " " 0)
set ytics nomirror
set xtics ( " " 0)
set noylabel
p  'Fe.DOS' u 2:($1+4.2654) w lines lw 2 

unset multiplot