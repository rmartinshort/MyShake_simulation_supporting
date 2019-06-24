#!/usr/bin/env python

import os

def main():

    dirs = ['Peru','Chile','Italy','Central_America','Oklahoma','Japan','Indonesia','Haiti','SCalifornia','NCalifornia','Turkey','Nepal','Taiwan','New_Zealand','Korea','Kashmir']
 

    for fname in dirs:

        #os.system('rm %s/*dist*.png' %fname)
        #os.system('rm %s/*.pdf' %fname)

        os.system('./Mapping_driver.sh %s' %fname)


if __name__ == "__main__":
    main()
