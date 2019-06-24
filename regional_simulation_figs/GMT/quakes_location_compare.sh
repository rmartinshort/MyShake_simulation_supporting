#!/bin/bash

#For making a map of earthquakes that were poorly located vs ones that are located within 30km of their epicenter

path=$1
region=$2
coords=$3
legendloc=$4
mediasize=$5

ps=$region\_quakes_locate.ps
Jmap=M7i
R=$coords

good_events=$path/Events_located_within_thresh.csv
bad_events=$path/Events_located_outside_thresh.csv
actual_events=$path/$region\_allevents.csv

awk -F',' '{print $1,$2,1.5^($3)/25}' $good_events > tmp1
awk -F',' '{print $1,$2,1.5^($3)/25}' $bad_events > tmp2
awk -F',' '{print $1,$2,1.5^($4)/25}' $actual_events > tmp3

allphones=$path/pop_running_myshake_$region\_0.001.csv

gmt pscoast -Rd$R -J$Jmap -BWSne -B2.0f2.0g2.0 -Dh -Slightblue -Glightgray -K -N1,red -N2,blue -Wthin --PS_MEDIA=$mediasize > $ps
gmt psxy $allphones -J$Jmap -R$R -Sc0.01,black -O -V -K  >> $ps

#plot all the events
gmt psxy tmp3 -J$Jmap -R$R -Scc -O -K -V -Wthin,blue >> $ps
#plot the good events
gmt psxy tmp1 -J$Jmap -R$R -Scc -Ggreen -O -K -V -Wthin,black >> $ps
#plot the bad events
gmt psxy tmp2 -J$Jmap -R$R -Scc -Gred -O -K -V -Wthin,black >> $ps


gmt pslegend -R$R -J$Jmap -D$legendloc -C0.1i/0.1i -L1.5 -O << EOF >> $ps
G -0.1i
H 20 Quakes
D 0.2i 1p
N 1
V 0 1p
S 0.1i c0.3 0.5 red thinnest,black 0.3i Poorly located event
S 0.1i c0.3 0.5 green thinnest,black 0.3i Well located event
D 0.2i 1p
N 1
G 0.05i
EOF

rm tmp1 tmp2 tmp3

gmt ps2raster $ps -P -Tf

mv $region\_quakes_locate.pdf $path
rm $ps
evince $path/$region\_quakes_locate.pdf
