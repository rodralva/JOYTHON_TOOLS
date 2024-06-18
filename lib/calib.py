# This file should take care of the calibration of all the days, for now the value copypasting isn't automated, 
# and is extracted from the Excel files in the CIEMAT NEUTRINOs google drive
# https://drive.google.com/drive/folders/12tga108L78UwGpQPW8NM7d8Q0AtKRnJZ?usp=sharing

import numpy as np

def GetGains(WEEK,CH,OV,MODE="PE"):

    SAMPLING=4e-9
    BITS= 16384
    DYNAMIC_RANGE= 2
    AMP= np.array([250,250,250,250,1560]) ## this is not true, the Amp is this /50 Ohms  from the ADC  resistance. Antonio includes the 50 Ohms in the ADC  in the measure. THIS IS NOT the amp,  which would be for exmaple: 250 Ohms/50 Ohms = 5s

    #                           ADCs to V     ticks to sec          C to e-      still need to correct by Gain of specific run
    ADCxTicks2e=       DYNAMIC_RANGE/BITS     * SAMPLING  / AMP  /e_charge

    #Calibraitons for the 5 weeks data taking

    if CH<4:

        # if CH>2: CH+=1;

        if   (WEEK=="APSAIA_VUV")   & (OV==3):   GAIN=np.array([4.62E+06,	4.84E+06,	4.72E+06,	4.79E+06 ])
        elif (WEEK=="APSAIA_VUV")   & (OV==4):   GAIN=np.array([6.34E+06,	6.59E+06,	6.54E+06,	6.61E+06 ])
        elif (WEEK=="APSAIA_VUV")   & (OV==5):   GAIN=np.array([8.13E+06,	8.40E+06,	8.46E+06,	8.53E+06 ])
        
        elif (WEEK=="APSAIA_VIS")   & (OV==3):   GAIN=np.array([4.68E+06,	4.89E+06,	4.78E+06,	4.80E+06 ])
        elif (WEEK=="APSAIA_VIS")   & (OV==4):   GAIN=np.array([6.47E+06,	6.69E+06,	6.64E+06,	6.63E+06 ])
        elif (WEEK=="APSAIA_VIS")   & (OV==5):   GAIN=np.array([8.29E+06,	8.56E+06,	8.63E+06,	8.58E+06 ])
        
        elif (WEEK=="APSAIA_VUV_2") & (OV==3):   GAIN=np.array([4.95E+06,	5.12E+06,	4.99E+06,	5.06E+06 ])
        elif (WEEK=="APSAIA_VUV_2") & (OV==4):   GAIN=np.array([6.75E+06,	6.98E+06,	6.90E+06,	6.97E+06 ])
        elif (WEEK=="APSAIA_VUV_2") & (OV==5):   GAIN=np.array([8.65E+06,	8.96E+06,	8.96E+06,	9.06E+06 ])
        
        elif (WEEK=="DAPHNE_VIS")   & (OV==3):   GAIN=np.array([5.06E+06,	5.30E+06,	5.05E+06,	5.14E+06 ])
        elif (WEEK=="DAPHNE_VIS")   & (OV==4):   GAIN=np.array([6.83E+06,	7.18E+06,	7.00E+06,	7.08E+06 ])
        elif (WEEK=="DAPHNE_VIS")   & (OV==5):   GAIN=np.array([8.87E+06,	9.15E+06,	9.13E+06,	9.20E+06 ])
        
        elif (WEEK=="DAPHNE_VUV")   & (OV==3):   GAIN=np.array([5.06E+06,	5.30E+06,	5.05E+06,	5.14E+06 ])
        elif (WEEK=="DAPHNE_VUV")   & (OV==4):   GAIN=np.array([6.83E+06,	7.18E+06,	7.00E+06,	7.08E+06 ])
        elif (WEEK=="DAPHNE_VUV")   & (OV==5):   GAIN=np.array([8.87E+06,	9.15E+06,	9.13E+06,	9.20E+06 ])
        else:   raise ValueError("No OV and WEEK combination found!");

        ADCxTicks2PE=ADCxTicks2e[:-1]/GAIN   

        if MODE=="PE":    return ADCxTicks2PE [CH]# Direct factor conversion from ticksxadcs to Photo-electrons (includes amplification from electronics an ADC details)
        if MODE=="GAIN":  return GAIN         [CH]# Pure 1PE->measuredElectrons ratio (adimensional), should be arround 1e6 ( depends on sensor and OV)

    elif CH==4:
        if   (WEEK=="APSAIA_VUV")   & (OV==2  ): GAIN = 1.48E+06
        elif (WEEK=="APSAIA_VUV")   & (OV==2.5): GAIN = 1.86E+06
        elif (WEEK=="APSAIA_VUV")   & (OV==3  ): GAIN = 2.24E+06
        
        elif (WEEK=="APSAIA_VIS")   & (OV==2  ): GAIN = 1.49E+06
        elif (WEEK=="APSAIA_VIS")   & (OV==2.5): GAIN = 1.86E+06
        elif (WEEK=="APSAIA_VIS")   & (OV==3  ): GAIN = 2.24E+06
        
        elif (WEEK=="APSAIA_VUV_2") & (OV==2  ): GAIN = 1.46E+06
        elif (WEEK=="APSAIA_VUV_2") & (OV==2.5): GAIN = 1.83E+06
        elif (WEEK=="APSAIA_VUV_2") & (OV==3  ): GAIN = 2.20E+06
        
        elif (WEEK=="DAPHNE_VIS")   & (OV==7 ): GAIN = 2.52E+06
        elif (WEEK=="DAPHNE_VIS")   & (OV==9 ): GAIN = 3.30E+06
        elif (WEEK=="DAPHNE_VIS")   & (OV==12): GAIN = 4.46E+06
        
        elif (WEEK=="DAPHNE_VUV")   & (OV==7 ): GAIN = 2.52E+06
        elif (WEEK=="DAPHNE_VUV")   & (OV==9 ): GAIN = 3.31E+06
        elif (WEEK=="DAPHNE_VUV")   & (OV==12): GAIN = 4.46E+06        
        else:   raise ValueError("No OV and WEEK combination found!");
        
        ADCxTicks2PE=ADCxTicks2e[-1]/GAIN   
    
        if MODE=="PE":    return ADCxTicks2PE # Direct factor conversion from ticksxadcs to Photo-electrons (includes amplification from electronics an ADC details)
        if MODE=="GAIN":  return GAIN         # Pure 1PE->measuredElectrons ratio (adimensional), should be arround 1e6 ( depends on sensor and OV)
        
    else:   raise ValueError("MODE argument is either PE or GAIN");

