#!/usr/bin/env python
#RMS 2019

#Generate error plot from events

#import matplotlib
#matplotlib.use('Agg')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os

#mapping tools 
from Event_mapper import map_alert_time, map_mag_error, map_distance_error

plt.style.use('ggplot')

def main():

    parser = argparse.ArgumentParser(description="Error plotting tools for regional event analysis")

    parser.add_argument('--filepath',action='store',help='name of the folder containing the region and event information')
    parser.add_argument('--regionname',action='store',help='name of the region of interest')
    parser.add_argument('--regioncoords',action='store',nargs='+',help='coordinates of region bounding box in minlon/maxlon/minlat/maxlat')
    args = parser.parse_args()

    region_name = args.regionname
    eventfolder = args.filepath
    region_coords = args.regioncoords

    single_events = pd.read_csv(eventfolder+'/'+region_name+'_single_event_tw:Y_opt:Y_bnds.csv')

    error_tracking = pd.read_csv(eventfolder+'/'+region_name+'_error_tracking.csv',
                names=['evmag','estmag','otime_error','atime_error','dist_error','update_num'],skiprows=1)

    real_events = pd.read_csv(eventfolder+'/'+region_name+'_allevents.csv',header=None,names=\
                          ['lon','lat','depth','mag','date'])

    generate_event_errors_for_gmt(single_events,eventfolder)

    detected_events = pd.read_csv(eventfolder+'/Event_distance_error.csv',header=None,\
                            names=['lon','lat','depth','mag'])
    
    population = pd.read_csv(eventfolder+'/pop_running_myshake_%s_0.001.csv' %region_name,names=['lon','lat'])

    #Generate some more features

    single_events['total_trigs'] = single_events['nptrigs'] + single_events['nstrigs']
    single_events['fraction_p'] = single_events['nptrigs']/single_events['total_trigs']
    
    #This is a bit careless, but these column names get used in the summary_plot_for_paper function 
    single_events['Ln total triggers'] = np.log(single_events['nptrigs'] + single_events['nstrigs'])
    single_events['Total triggers'] = single_events['nptrigs'] + single_events['nstrigs']
    single_events['P trigger fraction'] = single_events['nptrigs']/single_events['Total triggers']
    single_events['estimated_mag'] = single_events['mag'] + single_events['mu_mag']
    single_events['Ln epicentral distance to first cluster centroid (km)'] = np.log(single_events['first_cluster_dist'])


    #Run functions and generate plots
    cwd = os.getcwd()

    os.chdir(eventfolder)
    print(os.getcwd)
    
    summary_plot_for_paper(single_events,region_name,real_events,detected_events)
    
    map_alert_time(region_name,region_coords[0],single_events,real_events,population)
    map_mag_error(region_name,region_coords[0],single_events,real_events,population)
    map_distance_error(region_name,region_coords[0],single_events,real_events,population)

    #error_panel_plot_split(single_events,region_name)
    #event_detection_histogram(real_events,detected_events,region_name)
    #plot_error_evolution(error_tracking,region_name)

    os.chdir(cwd)


def generate_event_errors_for_gmt(single_events,eventfolder,dist_thresh=30):

    single_events[['lon','lat','mu_alertT','mag']].to_csv(eventfolder+'/Event_alert_time.csv',header=False,index=False)
    single_events[['lon','lat','mu_dist','mag']].to_csv(eventfolder+'/Event_distance_error.csv',header=False,index=False)
    single_events[['lon','lat','mu_originT','mag']].to_csv(eventfolder+'/Event_origin_time.csv',header=False,index=False)

    good_events = single_events[single_events['mu_dist']<dist_thresh]
    bad_events = single_events[single_events['mu_dist']>dist_thresh]

    good_events[['lon','lat','mag']].to_csv(eventfolder+'/Events_located_within_thresh.csv',header=False,index=False)
    bad_events[['lon','lat','mag']].to_csv(eventfolder+'/Events_located_outside_thresh.csv',header=False,index=False)


def summary_plot_for_paper(single_events,region_name,real_events,detected_events):
    
    '''
    Generate figure for the MyShake simulation platform paper
    '''
    
    plt.style.use('seaborn-poster')
    
    fig=plt.figure(figsize=(20,15))
    
    fig.suptitle('Results for region %s' %region_name,fontsize=22)
    ax1 = fig.add_subplot(221)
    single_events.plot(x='mag',y='estimated_mag',c='P trigger fraction',colormap='jet',kind='scatter',s=50,ax=ax1);
    ax1.plot([4,9],[4,9],'k--')
    ax1.set_xlabel('True magnitude (Mb)')
    ax1.set_ylabel('Estimated magnitude (Mb)')
    
    ax2 = fig.add_subplot(222)
    single_events.plot(x='mag',y='mu_dist',c='Ln total triggers',colormap='jet',kind='scatter',s=50,ax=ax2);
    ax2.set_ylim([0,100])
    ax2.set_xlabel('True magnitude (Mb)')
    ax2.set_ylabel('Epicenter distance error (km)')
    
    ax3 = fig.add_subplot(223)
    single_events.plot(x='mag',y='mu_alertT',c='Ln epicentral distance to first cluster centroid (km)',colormap='jet',kind='scatter',s=50,ax=ax3);
    ax3.set_xlabel('True magnitude (Mb)')
    ax3.set_ylabel('Time to first alert (s)')
    
    ax4 = fig.add_subplot(224)
    minmag = min(real_events['mag'])
    maxmag = max(real_events['mag'])
    
    sns.distplot(real_events['mag'],kde=False,bins=np.arange(round(minmag,1),round(maxmag,1),0.1),label='Actual events',ax=ax4)
    sns.distplot(detected_events['mag'],kde=False,bins=np.arange(round(minmag,1),round(maxmag,1),0.1),label='Detected events',ax=ax4)
    ax4.set_xlabel('True Magnitude (Mb)')
    ax4.set_ylabel('Number of events')
    ax4.semilogy()
    ax4.legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    figname = "summary_results_%s.pdf" %region_name
    plt.savefig(figname,dpi=300)
    plt.close()
    

def error_panel_plot_split(events_df,region_name):

    fig = plt.figure(figsize=(15,10))

    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)

    events_mp = events_df[events_df['fraction_p']<0.25]
    events_ms = events_df[(events_df['fraction_p']>=0.25) & (events_df['fraction_p']<=0.75)]
    events_ms8 = events_df[events_df['fraction_p']>0.75]

    ax1.scatter(events_mp['mag'],events_mp['mu_dist'],color='b',label='<25% p triggers',alpha=0.7)
    ax1.scatter(events_ms['mag'],events_ms['mu_dist'],color='r',label='25-75% p triggers',alpha=0.7)
    ax1.scatter(events_ms8['mag'],events_ms8['mu_dist'],color='k',label='>75% p triggers',alpha=0.7)
    ax1.set_xlabel('Magnitude')
    ax1.set_ylabel('Distance error (km)')

    #ax2.scatter(events_mp['mag'],events_mp['mu_mag'],c=events_mp['mu_dist'],alpha=0.7,cmap='jet')
    #ax2.scatter(events_ms['mag'],events_ms['mu_mag'],c=events_ms['mu_dist'],alpha=0.7,cmap='jet')
    #ax2.scatter(events_ms8['mag'],events_ms8['mu_mag'],c=events_ms8['mu_dist'],alpha=0.7,cmap='jet')
    ax2.scatter(events_mp['mag'],events_mp['mu_mag'],color='b',label='<25% p triggers',alpha=0.7)
    ax2.scatter(events_ms['mag'],events_ms['mu_mag'],color='r',label='25-75% p triggers',alpha=0.7)
    ax2.scatter(events_ms8['mag'],events_ms8['mu_mag'],color='k',label='>75% p triggers',alpha=0.7)
    ax2.set_xlabel('Magnitude')
    ax2.set_ylabel('Magnitude error (Mb)')
    ax2.legend()

    X = np.linspace(4,7.5,10)
    ax3.plot(X,X,'k--')
    ax3.scatter(events_mp['mag'], events_mp['mag']+events_mp['mu_mag'],color='b',label='<25% p triggers',alpha=0.7)
    ax3.scatter(events_ms['mag'], events_ms['mag']+events_ms['mu_mag'],color='r',label='25-75% p triggers',alpha=0.7)
    ax3.scatter(events_ms8['mag'], events_ms8['mag']+events_ms8['mu_mag'],color='k',label='>75% p triggers',alpha=0.7)
    ax3.set_xlabel('True magnitude (Mb)')
    ax3.set_ylabel('Estimated magnitude (Mb)')

    #ax3.scatter(events_mp['mag'],events_mp['mu_originT'],color='b',label='<25% p triggers',alpha=0.7)
    #ax3.scatter(events_ms['mag'],events_ms['mu_originT'],color='r',label='25-75% p triggers',alpha=0.7)
    #ax3.scatter(events_ms8['mag'],events_ms8['mu_originT'],color='k',label='>75% p triggers',alpha=0.7)
    #ax3.set_xlabel('Magnitude')
    #ax3.set_ylabel('Origin time error (s)')

    ax4.scatter(events_df['mag'],events_df['mu_alertT'],color='k')
    ax4.set_xlabel('Magnitude')
    ax4.set_ylabel('Alert time (s)')

    ax5.scatter(events_mp['mu_dist'],events_mp['mu_mag'],color='b',label='<25% p triggers',alpha=0.7)
    ax5.scatter(events_ms['mu_dist'],events_ms['mu_mag'],color='r',label='25-75% p triggers',alpha=0.7)
    ax5.scatter(events_ms8['mu_dist'],events_ms8['mu_mag'],color='k',label='>75% p triggers',alpha=0.7)
    ax5.set_xlabel('Distance Error')
    ax5.set_ylabel('Magnitude error (Mb)')

    ax6.scatter(events_mp['total_trigs'],events_mp['mu_dist'],color='b',label='<25% p triggers',alpha=0.7)
    ax6.scatter(events_ms['total_trigs'],events_ms['mu_dist'],color='r',label='25-75% p triggers',alpha=0.7)
    ax6.scatter(events_ms8['total_trigs'],events_ms8['mu_dist'],color='k',label='>75% p triggers',alpha=0.7)
    ax6.set_xlabel('Total triggers')
    ax6.set_ylabel('Distance error (km)')

    plt.suptitle(region_name+' errors')
    plt.tight_layout()
    plt.savefig(region_name+"_errors_function_of_mag_M4.pdf",dpi=200)


def error_panel_plot(single_events):

    fig = plt.figure(figsize=(10,10))
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    ax1.scatter(single_events['mag'],single_events['mu_dist'],color='b')
    ax1.set_xlabel('Magnitude')
    ax1.set_ylabel('Distance error (km)')

    ax2.scatter(single_events['mag'],single_events['mu_mag'],color='r')
    ax2.set_xlabel('Magnitude')
    ax2.set_ylabel('Magnitude error (Mb)')

    ax3.scatter(single_events['mag'],single_events['mu_originT'],color='g')
    ax3.set_xlabel('Magnitude')
    ax3.set_ylabel('Origin time error (s)')

    ax4.scatter(single_events['mag'],single_events['mu_alertT'],color='k')
    ax4.set_xlabel('Magnitude')
    ax4.set_ylabel('Alert time (s)')

    plt.tight_layout()
    plt.savefig("Errors_function_of_mag_M4.pdf",dpi=200)


def plot_error_evolution(error_tracking,region_name):

    '''
    Input: File containing error tracking infromation
    Output: A png file showing error evolution as a function of update number
    '''

    error_tracking['update_diff'] = error_tracking['update_num'].diff()


    index_vals = list(error_tracking[error_tracking['update_diff']!=1].index)

    all_error_dfs = []

    for i in range(len(index_vals)-1):
        ind1 = index_vals[i]
        ind2 = index_vals[i+1]

        error_df = error_tracking[ind1:ind2]
        if len(error_df) > 3:
            all_error_dfs.append(error_df)


    fig = plt.figure(figsize=(8,16))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    for error_df in all_error_dfs:
        ax1.plot(error_df['update_num'].values,error_df['estmag'].values,'-o',alpha=0.5)
        ax1.set_xlabel('Update number')
        ax1.set_ylabel('Estimated magnitude')
        ax2.plot(error_df['update_num'].values,error_df['otime_error'].values,'-o',alpha=0.5)
        ax2.set_xlabel('Update number')
        ax2.set_ylabel('Origin time error (s)')
        ax3.plot(error_df['update_num'].values,error_df['dist_error'].values,'-o',alpha=0.5)
        ax3.set_xlabel('Update number')
        ax3.set_ylabel('Epicenter distance error (km)')
        #ax3.set_ylim([0,100])

    #ax1.legend()

    fig.suptitle('Error evolution with updates for region %s' %region_name,y=1.05)
    plt.tight_layout()
    savefigname = '%s_error_tracking_fig_M4.pdf' %region_name
    plt.savefig(savefigname,dpi=200)


def event_detection_histogram(real_events,detected_events,region_name):

    #print(real_events)

    #print('Detected_events')
    #print(detected_events)

    #print(len(detected_events),len(real_events))

    minmag = min(real_events['mag'])
    maxmag = max(real_events['mag'])

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    sns.distplot(real_events['mag'],kde=False,bins=np.arange(round(minmag,1),round(maxmag,1),0.1),label='Actual events',ax=ax)
    sns.distplot(detected_events['mag'],kde=False,bins=np.arange(round(minmag,1),round(maxmag,1),0.1),label='Detected events',ax=ax)
    ax.set_xlabel('Magnitude')
    ax.set_ylabel('Number of events')
    plt.semilogy()
    plt.legend()
    savefigname = '%s_event_detection_histogram.png' %region_name
    plt.title('Detected events %s' %region_name)
    plt.show()
    plt.savefig(savefigname,dpi=200)
    





if __name__ == "__main__":

    main()
