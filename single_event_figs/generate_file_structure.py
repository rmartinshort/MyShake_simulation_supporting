#!/usr/bin/env python

import os
import glob

def main():
    
    projectdir='one_update_uncert_all_regions_paper'

    if not os.path.exists(projectdir):
       os.system('mkdir %s' %projectdir)

    region_event_files = glob.glob('*_single_event_*.csv')
    
    for fname in region_event_files:

        region_name = fname.split('_')[0]
        
        if region_name == 'New':
           region_name = 'New_Zealand'
        elif region_name == 'Central':
           region_name = 'Central_America'
        
        if not os.path.exists(region_name):
           os.system('mkdir %s' %region_name)

        os.system('mv *%s_* %s' %(region_name, region_name))
        os.system('mv %s %s' %(region_name,projectdir))


if __name__ == '__main__':

   main()

   
