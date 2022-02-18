from matplotlib import pyplot as plt
from numpy.fft import rfftfreq
from scipy.io import wavfile
import numpy as np



def equalizer(data,fs,fre_range,factor):

    
    amp = np.fft.rfft(data)
     ###### if you want to plot the change befor equalizing (amp) and after (amp_equalized)
    freq = np.fft.rfftfreq(len(amp[:, 0]), 1 / fs)

    for i, f in enumerate(freq):

        if f > fre_range[0] and f < fre_range[1]:  # (1)
            amp[i] *= 1.15**factor 

    data_after_change = (np.fft.irfft(amp))

    return data_after_change

