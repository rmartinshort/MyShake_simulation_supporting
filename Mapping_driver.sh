#!/bin/bash

#Driver program for making MyShake maps and plots for some region
region=$1

regionname=$region
regionpath=$region

if [ $regionname = 'SCalifornia' ]; then
  coords=-122/-115/32/36
  legendloc=-113.5/36/3i/0.3i
  mediasize=Custom_8ix11i
elif [ $regionname = 'NCalifornia' ]; then
  coords=-124/-119/35/39
  legendloc=-118/39/3i/0.3i
  mediasize=Custom_10ix11i
elif [ $regionname = 'Korea' ]; then
  coords=126/130/34/39
  legendloc=131/39/3i/0.3i
  mediasize=Custom_14ix11i
elif [ $regionname = 'New_Zealand' ]; then
  coords=170/177/-45/-39
  legendloc=176/-40/3i/0.3i
  mediasize=Custom_12ix11i
elif [ $regionname = 'Kashmir' ]; then
  coords=70/76/32/40
  legendloc=77/40/3i/0.3i
  mediasize=Custom_15ix15i
elif [ $regionname = 'Haiti' ]; then
  coords=-75/-70.5/17.5/20
  legendloc=-68.5/20/3i/0.3i
  mediasize=Custom_8ix11i
elif [ $regionname = 'Indonesia' ]; then
  coords=117/125/-4/3
  legendloc=127/3/3i/0.3i
  mediasize=Custom_8ix12i
elif [ $regionname = 'Nepal' ]; then
  coords=80/88/26/31
  legendloc=90/31/3i/0.3i
  mediasize=Custom_7.5ix10i
elif [ $regionname = 'Taiwan' ]; then
  coords=119.8/122.2/21.5/25.5
  legendloc=123.2/25.5/3i/0.3i
  mediasize=Custom_15ix12i
elif [ $regionname = 'Turkey' ]; then
  coords=25/35/35/43
  legendloc=36.0/43.3/3i/0.3i
  mediasize=Custom_11ix12i
elif [ $regionname = 'Chile' ]; then
  coords=-74.5/-68.5/-42/-18
  legendloc=-67.5/-17.8/3i/0.3i
  mediasize=Custom_37ix10i
elif [ $regionname = 'Peru' ]; then
  coords=-84/-69/-20/-2
  legendloc=-65.5/-2/3i/0.3i
  mediasize=Custom_11ix11i
elif [ $regionname = 'Mexico' ]; then
  coords=-106/-95/13/23
  legendloc=-101/25.3/3i/0.3i
  mediasize=Custom_9ix10i
elif  [ $regionname = 'Central_America' ]; then
  coords=-93/-76/7/19
  legendloc=-73/19/3i/0.3i
  mediasize=Custom_9ix11i
elif [ $regionname = 'Oklahoma' ]; then
  coords=-103.9/-94.1/33.1/38.0
  legendloc=-91.7/38.0/3i/0.3i
  mediasize=Custom_8ix12i
elif [ $regionname = 'Japan' ]; then 
  coords=135.6/141.2/33.3/36.7
  legendloc=142.6/36.7/3i/0.3i
  mediasize=Custom_8ix11i
elif [ $regionname = 'Italy' ]; then
  coords=10/19/40/46
  legendloc=21/46/3i/0.3i
  mediasize=Custom_8ix12i
fi


#Make error plots and cartopy maps
./Error_analysis.py --filepath $regionpath --regionname $regionname --regioncoords=$coords

#Make alert time map
#./quakemap_alert_time.sh $regionpath $regionname $coords $mediasize

#Make origin time map
#./quakemap_origin_time.sh $regionpath $regionname $coords $mediasize

#Make distance error map
#./quakemap_dist_error.sh $regionpath $regionname $coords $mediasize

#Make map showing good and bad events
#./quakes_location_compare.sh $regionpath $regionname $coords $legendloc $mediasize

rm tmp*
