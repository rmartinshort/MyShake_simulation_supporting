#!/usr/bin/env python

#RMS 2019
#Module for use with MyShake simulation project. Takes event errors dataframe and plots maps using Cartopy


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import cartopy.feature as cfeature
from matplotlib.transforms import offset_copy
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker




def map_alert_time(region_name,coords,detected_events,all_events,population):

    '''
    Plot a map where events are colored by time to first alert
    '''

    print(coords)
    
    coords = coords.split('/')
    minlon_extent = float(coords[0])
    maxlon_extent = float(coords[1])
    minlat_extent = float(coords[2])
    maxlat_extent = float(coords[3])
    
    print("Plotting alert time map")
    
    print(minlon_extent,maxlon_extent,minlat_extent,maxlat_extent)
    
    stamen_terrain = cimgt.Stamen('terrain-background')
    
    if region_name == "Taiwan":
       fig = plt.figure(figsize=(13, 15))
    elif region_name == "Haiti":
       fig = plt.figure(figsize=(22, 8))
    elif region_name == "Chile":
        fig = plt.figure(figsize=(8,20))
    else:
       fig = plt.figure(figsize=(20, 10))
       
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([minlon_extent, maxlon_extent, \
                minlat_extent, maxlat_extent])
    #ax.set_aspect(0.1,adjustable='datalim',share=True)

    ax.coastlines(resolution='10m',linewidth=0.3)

    # Add the Stamen data at zoom level 8.
    ax.add_image(stamen_terrain, 8, alpha=0.5)

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                linewidth=1, color='gray', alpha=1, linestyle='--')


    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 16, 'color': 'black'}
    gl.ylabel_style = {'size': 16, 'color': 'black'}
    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right= False 
    
    if region_name == "Taiwan":
       gl.xlocator =  mticker.MaxNLocator(nbins=6, steps=[1, 2, 3, 5, 10])
    elif region_name == "Chile":
       gl.xlocator =  mticker.MaxNLocator(nbins=3, steps=[1, 2, 3, 5, 10])
    else:
       gl.xlocator =  mticker.MaxNLocator(nbins=8, steps=[1, 2, 3, 5, 10])
       
    gl.ylocator = mticker.MaxNLocator(nbins=8, steps=[1, 2, 5, 10])
    
    
    #plot the population using phones
    ax.plot(population['lon'],population['lat'],'r.',\
            transform=ccrs.PlateCarree(),markersize=1)

    #plot the detected earthquakes
    
    #Set lower and upper values for the colorscale
    c_5 = np.percentile(detected_events['mu_alertT'],5)
    c_95 = np.percentile(detected_events['mu_alertT'],95)
    
    colorevents = detected_events['mu_alertT'].apply(lambda x: c_5 if x <= c_5 else x)
    colorevents = colorevents.apply(lambda x: c_95 if x >= c_95 else x)
    
    eqs = ax.scatter(detected_events['lon'],detected_events['lat'],\
            transform=ccrs.PlateCarree(),s=np.exp(detected_events['mag'])\
            ,edgecolor='k',zorder=10,c=colorevents,cmap='viridis',alpha=1)

    #plot all earthquakes (to show undetected)
    ax.scatter(all_events['lon'],all_events['lat'],\
            transform=ccrs.PlateCarree(),s=np.exp(0.95*all_events['mag'])\
            ,edgecolor='k',zorder=5,alpha=0.1,color='k')

    bar_ax = fig.add_axes([0.1, 0.2, 0.03, 0.6])

    cbar = plt.colorbar(eqs,cax=bar_ax)
    bar_ax.yaxis.set_ticks_position('left')
    bar_ax.yaxis.set_label_position('right')
    cbar.set_label('Time to first alert (s)', rotation=270,fontsize=20,labelpad=27)
    
    
    #plt.tight_layout()
    
    figname = '%s_map_alert_time.pdf' %region_name
    plt.savefig(figname,dpi=100)
    
    
def map_mag_error(region_name,coords,detected_events,all_events,population):

    '''
    Plot a map where events are colored by magnitude error
    '''
    
    coords = coords.split('/')
    minlon_extent = float(coords[0])
    maxlon_extent = float(coords[1])
    minlat_extent = float(coords[2])
    maxlat_extent = float(coords[3])
    
    print("Plotting magnitude error map")
    
    print(minlon_extent,maxlon_extent,minlat_extent,maxlat_extent)
    
    stamen_terrain = cimgt.Stamen('terrain-background')
    
    if region_name == "Taiwan":
       fig = plt.figure(figsize=(13, 15))
    elif region_name == "Haiti":
       fig = plt.figure(figsize=(22, 8))
    elif region_name == "Chile":
        fig = plt.figure(figsize=(8,20))
    else:
       fig = plt.figure(figsize=(20, 10))
       
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([minlon_extent, maxlon_extent, \
                minlat_extent, maxlat_extent])

    ax.coastlines(resolution='10m',linewidth=0.3)

    # Add the Stamen data at zoom level 8.
    ax.add_image(stamen_terrain, 8, alpha=0.5)

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                linewidth=1, color='gray', alpha=1, linestyle='--')

    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 18, 'color': 'black'}
    gl.ylabel_style = {'size': 18, 'color': 'black'}
    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right= False 

    if region_name == "Taiwan":
       gl.xlocator =  mticker.MaxNLocator(nbins=6, steps=[1, 2, 3, 5, 10])
    elif region_name == "Chile":
       gl.xlocator =  mticker.MaxNLocator(nbins=3, steps=[1, 2, 3, 5, 10])
    else:
       gl.xlocator =  mticker.MaxNLocator(nbins=8, steps=[1, 2, 3, 5, 10])
       
    gl.ylocator = mticker.MaxNLocator(nbins=8, steps=[1, 2, 5, 10])
    

    #plot the population using phones
    ax.plot(population['lon'],population['lat'],'r.',\
            transform=ccrs.PlateCarree(),markersize=1)

    #plot the detected earthquakes
    
    c_5 = np.percentile(detected_events['mu_mag'],5)
    c_95 = np.percentile(detected_events['mu_mag'],95)
    
    colorevents = detected_events['mu_mag'].apply(lambda x: c_5 if x <= c_5 else x)
    colorevents = colorevents.apply(lambda x: c_95 if x >= c_95 else x)
    
    eqs = ax.scatter(detected_events['lon'],detected_events['lat'],\
            transform=ccrs.PlateCarree(),s=np.exp(detected_events['mag'])\
            ,edgecolor='k',zorder=10,c=colorevents,cmap='viridis')

    #plot all earthquakes (to show undetected)
    ax.scatter(all_events['lon'],all_events['lat'],\
            transform=ccrs.PlateCarree(),s=np.exp(0.95*all_events['mag'])\
            ,edgecolor='k',zorder=5,alpha=0.2,color='k')

    bar_ax = fig.add_axes([0.1, 0.2, 0.03, 0.6])

    cbar = plt.colorbar(eqs,cax=bar_ax)
    bar_ax.yaxis.set_ticks_position('left')
    bar_ax.yaxis.set_label_position('right')
    cbar.set_label('Magnitude error (Mb)', rotation=270,fontsize=20,labelpad=27)
    
    plt.tight_layout()
    
    figname = '%s_map_mag_error.pdf' %region_name
    plt.savefig(figname,dpi=200)
    
    
def map_distance_error(region_name,coords,detected_events,all_events,population):

    '''
    Plot a map where events are colored by distance error
    '''
    
    coords = coords.split('/')
    minlon_extent = float(coords[0])
    maxlon_extent = float(coords[1])
    minlat_extent = float(coords[2])
    maxlat_extent = float(coords[3])
    
    print('Plotting distance error map')
    
    print(minlon_extent,maxlon_extent,minlat_extent,maxlat_extent)
    
    stamen_terrain = cimgt.Stamen('terrain-background')
    
    if region_name == "Taiwan":
       fig = plt.figure(figsize=(13, 15))
    elif region_name == "Haiti":
       fig = plt.figure(figsize=(22, 8))
    elif region_name == "Chile":
        fig = plt.figure(figsize=(8,20))
    else:
       fig = plt.figure(figsize=(20, 10))
    
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
    ax.set_extent([minlon_extent, maxlon_extent, \
                minlat_extent, maxlat_extent])

    ax.coastlines(resolution='10m',linewidth=0.3)

    # Add the Stamen data at zoom level 8.
    ax.add_image(stamen_terrain, 8, alpha=0.5)

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                linewidth=1, color='gray', alpha=1, linestyle='--')

    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 18, 'color': 'black'}
    gl.ylabel_style = {'size': 18, 'color': 'black'}
    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right= False 

    if region_name == "Taiwan":
       gl.xlocator =  mticker.MaxNLocator(nbins=6, steps=[1, 2, 3, 5, 10])
    elif region_name == "Chile":
       gl.xlocator =  mticker.MaxNLocator(nbins=3, steps=[1, 2, 3, 5, 10])
    else:
       gl.xlocator =  mticker.MaxNLocator(nbins=8, steps=[1, 2, 3, 5, 10])
       
    gl.ylocator = mticker.MaxNLocator(nbins=8, steps=[1, 2, 5, 10])
    
    #plot the population using phones
    ax.plot(population['lon'],population['lat'],'r.',\
            transform=ccrs.PlateCarree(),markersize=1)

    #plot the detected earthquakes
    
    #Set lower and upper values for the colorscale
    c_5 = np.percentile(detected_events['mu_dist'],5)
    c_95 = np.percentile(detected_events['mu_dist'],95)
    
    colorevents = detected_events['mu_dist'].apply(lambda x: c_5 if x <= c_5 else x)
    colorevents = colorevents.apply(lambda x: c_95 if x >= c_95 else x)
    
    eqs = ax.scatter(detected_events['lon'],detected_events['lat'],\
            transform=ccrs.PlateCarree(),s=np.exp(detected_events['mag'])\
            ,edgecolor='k',zorder=10,c=colorevents,cmap='viridis')

    #plot all earthquakes (to show undetected)
    ax.scatter(all_events['lon'],all_events['lat'],\
            transform=ccrs.PlateCarree(),s=np.exp(0.95*all_events['mag'])\
            ,edgecolor='k',zorder=5,alpha=0.2,color='k')

    bar_ax = fig.add_axes([0.1, 0.2, 0.03, 0.6])

    cbar = plt.colorbar(eqs,cax=bar_ax)
    bar_ax.yaxis.set_ticks_position('left')
    bar_ax.yaxis.set_label_position('right')
    cbar.set_label('Epicenter distance error (km)', rotation=270,fontsize=20,labelpad=27)
    
    plt.tight_layout()

    figname = '%s_map_distance_error.pdf' %region_name
    plt.savefig(figname,dpi=200)
    
    