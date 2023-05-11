# This library processes the runs and channel structure neccesary for everything else
# Simplicity is the key

import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '../')


def open_run_var(run_path:str,var_name:str,channels,compressed=True,DEBUG=False):

    run_var=dict();

    if DEBUG: print("----------")
    for ch in channels:
        
        run_var[ch]=open_ch_var(run_path,var_name,ch,compressed,DEBUG)

    return run_var;

def open_ch_var(run_path:str,var_name:str,ch,compressed=True,DEBUG=False):
        if compressed: 
            full_path = run_path+var_name+"_ch"+str(ch)+".npz"
            if DEBUG: print("Opening: ",var_name," channel:",ch, " ,in:",full_path)
            ch_var=np.load(full_path ,allow_pickle=True,mmap_mode='r') ["arr_0"]
            if (var_name.__contains__("ADC")): #prevents crashes from numba and other optimizers-> all adcs are read as floats
                ch_var=ch_var.astype(float) # raw wvfs format is np.uint16
            if ch_var.shape==():# we are loading a dictionary
                ch_var=ch_var.item()
        else: 
            full_path = run_path+var_name+"_ch"+str(ch)+".npy"
            if DEBUG: print("Opening: ",var_name," channel:",ch, " ,in:",full_path)
            ch_var=np.load(full_path ,allow_pickle=True)
            if (var_name.__contains__("ADC")):
                ch_var=ch_var.astype(float) 
            if ch_var.shape==():# we are loading a dictionary
                ch_var=ch_var.item()
        return ch_var;

def open_runs_table(excel_file_path="",sheet='Sheet1'):
    """Creates a dictionary with run properties out of an exel table

    Args:
        run (int):number of the run
        excel_file_path (str): excel containing the runs table data sheet. Defaults to "".
        sheet (str, optional):sheet in the excel file. Defaults to 'Sheet1'.

    Returns:
        Dictionary with run properties: polarity, type of run, thresholds, aprox duration... etc can be computed here
    """
    df = pd.read_excel(excel_file_path, sheet_name=sheet,engine='openpyxl')
    df['Channels']    = df['Channels']   .apply(lambda x: list(map(int,x.split(" ")))) #excell only allows one value per cell, convert channels from string to array of ints
    df['Polarity']    = df['Polarity']   .apply(lambda x: list(map(int,x.split(" "))))
    df['OverVoltage']    = df['OverVoltage']   .apply(lambda x: list(map(float,x.split(" "))))
    df['ChannelName'] = df['ChannelName'].apply(lambda x: x.split(" "))
    df["Polarity"]=df.apply(lambda x: dict(zip(x["Channels"],x["Polarity"])),axis=1)

    return df

def open_run_properties(run,excel_file_path="",sheet='Sheet1'):
    
    df=open_runs_table(excel_file_path,sheet)
    props=df.loc[df['Run'] == run].to_dict(orient='records')[0]
    return props

def save_run_var(run_var,run_path,var_name,compressed=True):
    channels=run_var.keys()

    print("----------")
    for ch in channels:
        
        if compressed:
            full_path = run_path+var_name+"_ch"+str(ch)+".npz"
            np.savez_compressed(full_path,run_var[ch])
    
        else: 
            full_path = run_path+var_name+"_ch"+str(ch)+".npy"
            np.save(full_path,run_var[ch])
        
        print("Saving: ",var_name," channel:",ch, " ,in:",full_path)



def do_run_things(VAR,func):
    
    if type(VAR)== dict:#single variable passed here
        channels=VAR.keys()
        # Do stuff on every channel of the run
        things=dict()
        
        print("----------")
        for ch in channels: 
            print("Doing: ",func.__name__," on channel:",ch)
            things[ch]=func(VAR[ch]);
        
        return things

    elif type(VAR) == tuple:# we are facing multiple input variables
        channels=VAR[0].keys()

        # Do stuff on every channel of the run
        things=dict()

        print("----------")
        for ch in channels: 
            vars_ch=tuple(var[ch] for var in VAR) #prepare all the variables only in the selected channel

            print("Doing: ",func.__name__," on channel:",ch)
            things[ch]=func(vars_ch);
        
        return things
