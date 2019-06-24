#!/usr/bin/env python
#RMS 2019

#Loop though event directories within some folder and generate plots of event error distribution and tracking as a function of update
#number

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import numpy as np
import glob
import re
import os



def main():

    parser = argparse.ArgumentParser(description="Run error plotting on a directory containing sub directories that each contain event information")
    parser.add_argument('--filepath', action='store', help='name of the folder containing the event information')
    
    rcParams['axes.titlepad'] = 10

    args = parser.parse_args()

    eventsfilepath = args.filepath

    if os.path.exists(eventsfilepath):
        os.chdir(eventsfilepath)
    else:
        raise ValueError('%s not found' %eventsfilepath)


    dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]

    #Plot error distribution plots
    for eventdir in dirs:
        print("Plotting in dir %s" %eventdir)
        error_distribution_plot(eventdir)
        error_distribution_plot_condensed(eventdir)
        plot_error_evolution(eventdir)

    print(dirs)
    
    
def error_distribution_plot_condensed(datafolder):
    
    '''Plot distribution of errors in a different style'''
    
    region_name = datafolder
    plt.style.use('seaborn-poster')
    
    fig = plt.figure(figsize=(20,10))
    
    figname = '%s_simulation_summary.pdf' %region_name
    
    all_errors = glob.glob("%s/*single_event*.csv" %(datafolder))
    summary_stats = glob.glob("%s/*event_errors*.csv" %(datafolder))
    
    if (len(all_errors) == 0) or (len(summary_stats) == 0):

        print('No event data found in %s' %datafolder)

    else:
        
        errors = pd.read_csv(summary_stats[0])
        summary = pd.read_csv(all_errors[0])
        
        print('Plotting summary figure for %s' %datafolder)
        
        etime = summary['datetime'].values[0].split('T')[0][2:]
        emag = summary['mag'].values[0]
        alert_time_mu = summary['mu_alertT'].values[0]
        alert_time_std = summary['std_alertT'].values[0]
        
        fig.suptitle('%s event, M%s: Mean time to first alert: %.2f s ($\sigma$ = %.2f s). 200 runs' %(etime,emag,alert_time_mu,alert_time_std), \
             fontsize=22)
        
        ax1 = fig.add_subplot(131)
        sns.distplot(errors['mag_error'],bins=50,norm_hist=False,axlabel='Magnitude error (Mb)',kde=False,ax=ax1)
        ax1.axvline(np.mean(errors['mag_error']),linestyle='--',color='r')
        ax1.set_title('$\mu$ = %.2f Mb, $\sigma$ = %.2f Mb' %(np.mean(errors['mag_error']),np.std(errors['mag_error'])))
        
        ax2 = fig.add_subplot(132)
        sns.distplot(errors['dist_error'],bins=50,norm_hist=False,axlabel='Distance error (km)',kde=False,ax=ax2)
        ax2.axvline(np.mean(errors['dist_error']),linestyle='--',color='r')
        ax2.set_title('$\mu$ = %.2f km, $\sigma$ = %.2f km' %(np.mean(errors['dist_error']),np.std(errors['dist_error'])))
        
        ax3 = fig.add_subplot(133)
        sns.distplot(errors['originT_error'],bins=50,norm_hist=False,axlabel='Origin time error (s)',kde=False,ax=ax3)
        ax3.axvline(np.mean(errors['originT_error']),linestyle='--',color='r')
        ax3.set_title('$\mu$ = %.2f s, $\sigma$ = %.2f s' %(np.mean(errors['originT_error']),np.std(errors['originT_error'])))
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.85)
        
        plt.savefig(figname,dpi=200)
    plt.close()
        
        
        
    
def error_distribution_plot(datafolder):

    '''Plot distribution of errors for event time, magnitude and location'''

    region_name = datafolder
    fig = plt.figure(figsize=(20,6))
    fig.suptitle('Errors for region %s' %(region_name), fontsize=20)
    
    plt.style.use("ggplot")

    all_errors = glob.glob("%s/*single_event*.csv" %(datafolder))
    summary_stats = glob.glob("%s/*event_errors*.csv" %(datafolder))

    if (len(all_errors) == 0) or (len(summary_stats) == 0):

        print('No event data found in %s' %datafolder)

    else:

        print('Plotting errors for %s' %datafolder)

        for item in list(sorted(summary_stats)):

            trigger_weight_flag = item.split('/')[-1].split(':')[1][0]
            opt_flag = item.split('/')[-1].split(':')[2][0]

            data = pd.read_csv(item)
            #data = data[data['dist_error']<200]
            #print(trigger_weight_flag)
            label = "Tw: %s, Opt: %s" %(trigger_weight_flag,opt_flag)

            ax1 = fig.add_subplot(251)
            sns.distplot(data['mag_error'],bins=50,norm_hist=False,axlabel='Magnitude error (Mb)',kde=False,ax=ax1)
            ax1.legend(loc='upper left',bbox_to_anchor=(0.1,1.2))
            ax2 = fig.add_subplot(252)
            sns.distplot(data['dist_error'],bins=50,norm_hist=False,axlabel='Distance error (km)',kde=False,ax=ax2)
            ax3 = fig.add_subplot(253)
            sns.distplot(data['originT_error'],bins=50,norm_hist=False,axlabel='Origin time error (s)',kde=False,ax=ax3)
            ax4 = fig.add_subplot(254)
            sns.regplot(data['originT_error'],data['dist_error'],fit_reg=False,ax=ax4,label=label)
            ax4.set(xlabel='Origin time error (s)', ylabel='Distance error (km)')
            #ax4.legend(loc='upper left',bbox_to_anchor=(0.1,1.2))


        ax5 = fig.add_subplot(255)

        itemcount = 0

        for item in list(sorted(all_errors)):

            table = pd.read_csv(item)

            row = table.iloc[0]
            time = row[0]
            lat = row[1]
            lon = row[2]
            depth = row[3]
            mag = row[4]

            mag_mean = row[5]
            mag_sd = row[6]
            dist_mean = row[7]
            dist_sd = row[8]
            otime_mean = row[9]
            otime_sd = row[10]
            atime_mean = row[11]
            atime_sd = row[12]
            nsamp = row[13]

            if itemcount == 0:

                ax5.text(0,0.05,'Magnitude: M %s' %mag)
                ax5.text(0,0.1,'Depth: %s km' %depth)
                ax5.text(0,0.15,'Coordinates (lon/lat): %.3f/%.3f' %(lon,lat))
                ax5.text(0,0.2,'Origin time: %s' %re.sub("[']",'',time))


            ax5.text(0,0.95,'Error mean and standard deviation')
            ax5.text(0,0.9,'Mag: $\mu$ = %.2f Mb $\sigma$ = %.2f Mb' %(mag_mean,mag_sd))
            ax5.text(0,0.85,'Dist: $\mu$ =  %.2f km $\sigma$ = %.2f km' %(dist_mean,dist_sd))
            ax5.text(0,0.8,'Otime: $\mu$ = %.2f s  $\sigma$ = %.2f s' %(otime_mean, otime_sd))
            ax5.text(0,0.65,'Time to first alert: %.2f s' %(atime_mean),fontsize=16)
            ax5.text(0,0.55,'Number of runs: %.i' %(nsamp),fontsize=16)

            itemcount += 1

            ax5.axis('off')

        fig.tight_layout()

        figname = 'Errors_region_%s_opt:%s.pdf' %(region_name,opt_flag)
        plt.savefig(datafolder+'/'+figname,dpi=400)
    
    plt.close()


def plot_error_evolution(datafolder):

    '''
    Input: File containing error tracking infromation
    Output: A png file showing error evolution as a function of update number
    '''

    error_tracking_file = glob.glob('%s/*error_tracking.csv' %datafolder)

    if len(error_tracking_file) == 0:
        print('No error tracking file found in %s' %datafolder)

    else:

        error_tracking_file = error_tracking_file[0]  #There should only be 1 of these

        error_tracking = pd.read_csv(error_tracking_file,
                names=['evmag','estmag','otime_error','atime_error','dist_error','update_num'],skiprows=1)

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

        region_name = error_tracking_file.split('_')[0]

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
        savefigname = '%s_error_tracking_fig.pdf' %region_name
        plt.savefig(savefigname,dpi=200)
    
    plt.close()



if __name__ == "__main__":

    main()
