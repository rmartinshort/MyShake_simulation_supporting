#!/bin/bash

#For making a map of alert times for each earthquake

ps=southern_CA_alert_time_M4plus.ps
Jmap=M7i
R=-122/-115/32/36

errors=M4plus/Event_alert_time.csv
awk -F',' '{print $1,$2,$3,$4/15}' $errors > tmp
allphones=M4plus/pop_running_myshake_SCalifornia_0.001.csv

gmt makecpt -Cjet -T0/21/0.1 -Z > cols.cpt

gmt pscoast -Rd$R -J$Jmap -BWSne -B1.0f1.0g1.0 -Di -Glightgray -K --PS_MEDIA=Custom_7ix12i > $ps
gmt psxy $allphones -J$Jmap -R$R -Sc0.01,black -O -V -K  >> $ps
gmt psxy tmp -J$Jmap -R$R -Scc -O -K -V -Ccols.cpt -Wthin >> $ps

gmt psscale -D1i/1i/1.5i/0.1ih -E -Ccols.cpt -Ba3f3g3/:"Time to alert (s)": -O >> $ps


gmt ps2raster $ps -P -Tf
evince southern_CA_alert_time_M4plus.pdf
