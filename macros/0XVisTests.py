# ---------------------------------------------------------------------------------------------------------------------- #
#  ========================================= RUN:$ python3 0XVisTests.py 0 0,1,2 ======================================= #
# This macro will show the individual EVENTS of the introduced runs and channels to see if everything is working fine    #
# Ideally we want to work in /pnfs/ciemat.es/data/neutrinos/FOLDER and so we mount the folder in our computer with:      #
# $ sshfs USER@pcaeXYZ.ciemat.es:/pnfs/ciemat.es/data/neutrinos/FOLDER ../data  --> making sure empty data folder exists #
# ---------------------------------------------------------------------------------------------------------------------- #

import sys; sys.path.insert(0, '../'); from lib import *; print_header()

##### INPUT RUNS AND OPTIONS #####
try:
    input_folder   = sys.argv[1]
    input_runs     = sys.argv[2]
    input_channels = sys.argv[3]
except IndexError:
    input_folder   = input("Please select FOLDER (e.g Feb22_2): ")
    input_runs     = input("Please select RUNS (separated with commas): ")
    input_channels = input("Please select CHANNELS (separated with commas): ")

runs     = [int(r) for r in input_runs.split(",")]
channels = [int(c) for c in input_channels.split(",")]

info = {"MONTH": [input_folder]}
OPT  = {
    "MICRO_SEC":   True,
    "NORM":        False,                # Runs can be displayed normalised (True/False)
    "LOGY":        False,               # Runs can be displayed in logy (True/False)
    "SHOW_AVE":    "AveWvfSPE",             # If computed, vis will show average (AveWvf,AveWvfSPE,etc.)
    "SHOW_PARAM":  True,                 # Print terminal information (True/False)
    "CHARGE_KEY":  "ChargeAveRange",     # Select charge info to be displayed. Default: "ChargeAveRange" (if computed)
    "PEAK_FINDER": False,                # Finds possible peaks in the window (True/False)
    "LEGEND":      False                 # Shows plot legend (True/False)
    }
###################################

##### LOAD RUNS #####
# my_runs = load_npy(runs,channels,preset="RAW",info=info,compressed=True)
my_runs = load_npy(runs,channels,preset="ANA",info=info,compressed=True)
# my_runs = load_npy(runs,channels,preset="CUTS",info=info,compressed=True) # Fast load (no ADC)
print(my_runs[runs[0]][channels[0]].keys())
#####################

##### EVENT VISUALIZER #####
# vis_npy(my_runs, ["RawADC"], evt_sel = -1, same_plot = False, OPT = OPT) # Input variables should be lists of integers
# vis_npy(my_runs, ["ADC"], evt_sel = -1, same_plot = False, OPT = OPT) # Input variables should be lists of integers
#####################

##### CUTS #####
# cut_min_max(my_runs, ["PedMax"], {"PedMax": [-99,14]})
# cut_min_max_sim(my_runs, ["PeakAmp", "ChargeAveRange"], {"PeakAmp": [30,45], "ChargeAveRange": [1.2, 2]})
# cut_lin_rel(my_runs, ["PeakAmp", "ChargeAveRange"])
################

##### HISTOGRAMS #####
for r in runs:
    for c in channels:
        vis_var_hist(my_runs, r, c, "RawPedMean", [0.1,99.9], OPT = {"SHOW": True})
#         vis_var_hist(my_runs, r, c, "ChargeAveRange",[0.1,99.9], {"SHOW": True})
        # vis_two_var_hist(my_runs, r, c, ["PedMax", "PedAmp"], OPT = {"SHOW": True})
######################
