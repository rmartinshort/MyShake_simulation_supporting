#!/bin/bash

#For making a map of distance error for each earthquake

path=$1
region=$2
coords=$3
mediasize=$4

ps=$region\_distance_error.ps
Jmap=M7i
R=$coords

errors=$path/Event_distance_error.csv
actual_events=$path/$region\_allevents.csv

awk -F',' '{print $1,$2,$3,1.5^($4)/25}' $errors > tmp1
awk -F',' '{print $1,$2,1.5^($4)/25}' $actual_events > tmp2

allphones=$path/pop_running_myshake_$region\_0.001.csv

gmt makecpt -Cjet -T0/20/0.1 -Z > cols.cpt

gmt pscoast -Rd$R -J$Jmap -BWSne -B2.0f2.0g2.0 -Dh -Slightblue -Glightgray -K -N1,red -N2,blue -Wthin --PS_MEDIA=$mediasize > $ps
gmt psxy $allphones -J$Jmap -R$R -Sc0.01,black -O -V -K  >> $ps

gmt psxy tmp2 -J$Jmap -R$R -Scc -O -K -V -Wthin >> $ps
gmt psxy tmp1 -J$Jmap -R$R -Scc -O -K -V -Ccols.cpt -Wthin >> $ps

gmt psscale -D1.2i/-0.35i/2.5i/0.1ih -E -Ccols.cpt -Ba5f5g5/:"Epicenter distance error [km]": -O >> $ps

rm tmp1  tmp2

gmt ps2raster $ps -P -Tf
mv $region\_distance_error.pdf $path
rm $ps
evince $path/$region\_distance_error.pdf
