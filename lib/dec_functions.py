import numpy as np
##For now, numba doesn't support np.fft, stay tunned for this: https://github.com/numba/numba/issues/5864
from scipy.fft import rfft, irfft  #10k ~4s

#custom function for the filter
def gauss(x, sigma, n, mean = 0, norm = 1):
    a = 1
    if norm == "standard":
        a = 1/(sigma*np.sqrt(2*np.pi))
    else:
        a = norm
    y = a*np.exp(-(x-mean)**n/(2*sigma**n))
    y[0]=0;
    return y

def deconvolve(ADCs:np.ndarray,SER:np.ndarray,FILTER=None,CPUs:int=6)->np.ndarray:
    ADCs_dec=np.zeros(ADCs.shape)
    ped=250;
    SER_FFT=np.fft.rfft(SER)
    if  FILTER is None:
        ADCs_dec=irfft(rfft(ADCs,axis=1)*FILTER/rfft(SER_FFT),axis=1,workers=CPUs)
    else:
        ADCs_dec=irfft(rfft(ADCs,axis=1)/rfft(SER_FFT),axis=1,workers=CPUs)

    return ADCs_dec;

#Framework interface, not debugged yet
def compute_DecWvf(VARS:tuple)->np.ndarray:
    if len(VARS)==2:#no filter involved
        adc,ser=VARS
        return deconvolve(adc,ser)
    elif len(VARS)==3:#with filter
        adc,ser,filt=VARS
        return deconvolve(adc,ser,filt)
    else:
        raise NotImplementedError("Inputs must be 2 or 3 tuple longs")