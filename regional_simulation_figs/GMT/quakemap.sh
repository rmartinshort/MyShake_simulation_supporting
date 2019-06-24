#!/bin/bash

ps=southern_CA_events_M4plus.ps
Jmap=M7i
R=-122/-115/32/36

events=M4plus/allevents.csv
awk -F',' '{print $1,$2,$3,$4/15}' $events > tmp
allphones=M4plus/pop_running_myshake_SCalifornia_0.001.csv

gmt pscoast -Rd$R -J$Jmap -BWSne -B1.0f1.0g1.0 -Di -Glightgray -K --PS_MEDIA=Custom_7ix12i > $ps
gmt psxy $allphones -J$Jmap -R$R -Sc0.01,black -O -V -K  >> $ps
gmt psxy tmp -J$Jmap -R$R -Scc -O -V -K -Ceq.cpt -Wthin >> $ps


gmt pslegend -R$R -J$Jmap -D-113/36/3i/0.3i -C0.1i/0.1i -L1.5 -O << EOF >> $ps
G -0.1i
H 20 Quakes
D 0.2i 1p
N 1
V 0 1p
S 0.1i c0.3 0.5 red thinnest,black 0.3i Earthquake: 0-5km depth
S 0.1i c0.3 0.5 orange thinnest,black 0.3i Earthquake: 5-10km depth
S 0.1i c0.3 0.5 yellow thinnest,black 0.3i Earthquake: 10-20km depth
S 0.1i c0.3 0.5 green thinnest,black 0.3i Earthquake: 20-50km depth
S 0.1i c0.3 0.5 blue thinnest,black 0.3i Earthquake: >50km depth
D 0.2i 1p
N 1
G 0.05i
EOF

gmt ps2raster $ps -P -Tf
evince southern_CA_events_M4plus.pdf
