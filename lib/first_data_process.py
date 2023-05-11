import numpy as np
import pandas as pd
import gc #garbage collector interface
import os

def Bin2Np_ADC(FileName:str,header_lines:int=6):
    """Dumps ADC binary .dat file with given header lines(6) and wvf size defined in header. \n
    Returns a npy array with Raw Wvf 
    If binary files are modified(header/data types), ask your local engineer"""
    
    DEBUG=False
    
    headers= np.fromfile(FileName, dtype='I') #read first event header
    header = headers[:6] #read first event header
    NSamples=int(header[0]/2-header_lines*2)
    Event_size=header_lines*2+NSamples

    data=np.fromfile(FileName, dtype='H');
    N_Events=int( data.shape[0]/Event_size );

    data    = np.reshape(data,(N_Events,Event_size))[:,header_lines*2:]
    headers = np.reshape(headers,(N_Events , int(Event_size/2) )  )[:,:header_lines]
    headers=headers.astype(float)
    
    first=headers[:,4]*2**32
    second=headers[:,5]
    TIMESTAMP  = first + second 
    TIMESTAMP *= 8e-9 #Unidades TriggerTimeStamp(PC_Units) * 8e-9

    if DEBUG:
        print("Header:",header)
        print("Waveform Samples:",NSamples)
        print("Event_size(wvf+header):",Event_size)
        
        print("N_Events:",N_Events)
        print("Run time: {:.2f}".format((TIMESTAMP[-1]-TIMESTAMP[0])/60) + " min" )
        print("Rate: {:.2f}".format(N_Events/(TIMESTAMP[-1]-TIMESTAMP[0])) + " Events/s" )
        print("#####################################################################\n")

    return data , TIMESTAMP;


def save_Bin2Np(file_in:str,file_out:str,compressed=True,file_timestamp="Timestamp"):
    """Self-explainatory. Computation time x10 slower than un-compresed, size x3 times smaller"""
    data_npy, timestamp = Bin2Np_ADC(file_in)
    if compressed:
        np.savez_compressed(file_out,data_npy)
        np.savez_compressed(file_timestamp,timestamp)
    else:         
        np.save(file_out,data_npy)
        np.save(file_timestamp,timestamp)
    
    del data_npy,timestamp #free memory
    gc.collect()

def save_Run_Bin2Np(Run:int,Channel,in_path:str="../data/raw/",out_path:str="../data/raw/",out_name:str="RawADC",Compressed:bool=True) :
    """Run is an int, channel is an int array/list. In/out paths are strings."""
    os.system("mkdir -p " + out_path+"run"+str(Run).zfill(2)+"/") # create output folder if not present
    for ch in Channel:
        inchan  = in_path+"run"+str(Run).zfill(2)+"/wave"+str(ch)+".dat"
        ADC_outchan = out_path+"run"+str(Run).zfill(2)+"/"+out_name+"_ch"+str(ch)  
        Timestamp_outchan = out_path+"run"+str(Run).zfill(2)+"/"+"Timestamp"+"_ch"+str(ch)  

        check_file_C = os.path.isfile(ADC_outchan+".npz")#compresed flag
        check_file_U = os.path.isfile(ADC_outchan+".npy")#uncompresed
        if check_file_C or check_file_U: 
            print("-----------------")
            print("Already dumped: ",inchan," to: ",ADC_outchan+".np*",Timestamp_outchan+".np*")
            print("-----------------")
        else:
            print("-----------------")
            print("Dumping: ",inchan," to: ",ADC_outchan+".np*",Timestamp_outchan+".np*")
            print("-----------------")
            save_Bin2Np(inchan,ADC_outchan,compressed=Compressed,file_timestamp=Timestamp_outchan)
