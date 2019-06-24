# MyShake_simulation_supporting

Supporting scripts and plotting tools for the MyShake simulation paper  


## Generating maps and summary figures for regional simulations  

Step 1: Run some simulations. In the MyShake_Simulation package, edit the file 'simulate_multiple_events.py'. This contains various functions for running simulations in all 17 regions. Each region has its own function.
There is a 'config' dictinary object that can be edited with simulation paramaters such as fraction of population sampled (0.001 = 0.1%), the number of updates etc. Unless running a test I would enture that the paramters
are the sam for each of the regions.   

Step 2: Inside 'simulate_multiple_events.py', you can specify the path error_dir (currently set to
'/home/rmartinshort/Documents/Berkeley/MyShake_simulations/For_paper/region_error_analysis'). This is where the files needed to produce the figures will be moved after the
simulation is run.    

Step 3: Go to the directory specified by 'error_dir'. You will need to make separate directories for each region, then use move_all_data.sh to move the files into their appropriate locations.  

Step 4: Run 'Mapping_driver.sh' with the name of the region that you want to produce figures for. Alternatively, run Make_all_plots.py to make all the figures in one go. This worflow is a bit strange because it was adapted directly from bash scripts desinged to plot GMT maps of
each region. This should produce 4 new .pdf files in each region directory, for example:

Chile_map_alert_time.pdf  Chile_map_distance_error.pdf  Chile_map_mag_error.pdf and summary_results_Chile.pdf    


## Generating summary figures for single event simulations   

In this case, we run a large number of simulations of a single event and then plot their error distributions. 

Step 1: In 'simulate_multiple_events.py' there is a function called all_events(). This contains the parameters needed for simulating major earthquakes in all the of the regions. The regions of interest can be commented in and out
as necessary. Note that the start and end times of the event search and the minimum magnitude to download may vary from region to region.  

Step 2: Again, specify 'error_dir' in this function. This is the path to the folder where important files are written. Also note that these single event simulations can take a long time, especially if nupdates > 1 in regions with high
population densities.   

Step 3: Once the simulations are complete, go to the 'error_dir' you specified. Use the script 'generate_file_structure.py' to create a directory structure needed for production of the figures. You specify the name of a folder, then it creates 
subfolders for each region and puts the error .csv files into those folders.   

Step 4: Run 'generate_error_figs.py' and provide the path to the folder you've just made with 'generate_file_structure.py'. The script will loop though the subfolders and make error plots for each region. 

