# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 11:01:06 2023

@author: AI - MB sound music project
"""

import numpy as np
import aifc
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.signal import find_peaks


# File import

# Path 

Name_file = "1_bassclarinet_theremin_nooption_ff_C4B4.aiff"
datafolder = "C:/Users/Amine/Desktop/diginamic/AI_to_maxime_sound_study/main_project_1/"

# lib aifc testing features

signal = aifc.open(datafolder + Name_file)
getchannels = signal.getnchannels()
nframes = signal.getnframes()
samplewidth = signal.getsampwidth()

# Signal reader 

strsig = signal.readframes(nframes)
signal_amplitude = np.fromstring(strsig, np.short).byteswap()

# Sample frequency  

framerate = signal.getframerate()

fmax = framerate

# Time step => delta_t

delta_t = 1/fmax

# time axis based on the length of the signal

time = np.arange(0,len(signal_amplitude)*delta_t,delta_t)


# Test plot normalized signal

# plt.figure(1)
# plt.plot(time,signal_amplitude/max(signal_amplitude))
# plt.xlabel('Time (s)' ,fontsize =15)
# plt.ylabel('Normalized amplitude',fontsize =15)
# plt.tick_params(labelsize=20)
# plt.grid()



# Time signal on log representation 

signal_to_split = 20*np.log10(abs(hilbert(signal_amplitude)))


# Time signal normalized log representation

signal_to_split_normalized = signal_to_split - max(signal_to_split)


# Find the peaks where the silence is performed 

peaks_signal, _ = find_peaks(-1*(signal_to_split_normalized),height=80)

# plot the normlized log signal representation & the silence zones where the split is performed 

plt.figure(2)
plt.plot(time,signal_to_split_normalized,'b')
plt.plot(time[peaks_signal],signal_to_split_normalized[peaks_signal],'.r')
plt.xlabel('Time (s)' ,fontsize =15)
plt.ylabel('Log normalized amplitude',fontsize =15)
plt.tick_params(labelsize=20)
plt.grid()

 
# time and amplitude of the silence zones

peaks_time = time[peaks_signal]   
peaks_amplitude = signal_to_split_normalized[peaks_signal] 
 
# init list for spliting the signal based on the 13 notes played

time_to_cut = []    
time_to_cut.insert(0,0)
index_time_to_cut = []
index_time_to_cut.insert(0,0)

# defind the spliting zones based on silences

list_of_the_interval_split = []

for index_time_peaks in range(len(peaks_time)-1):
    if peaks_time[index_time_peaks] - peaks_time[index_time_peaks - 1] > 1:
        time_to_cut.append(peaks_time[index_time_peaks])
        index_time_to_cut.append(np.where(time == peaks_time[index_time_peaks])[0][0])
        list_of_the_interval_split.append(peaks_time[index_time_peaks] - peaks_time[index_time_peaks - 1])


print(np.std(np.array(list_of_the_interval_split)))    
    
# plot the spliting zones with vertical lines

plt.figure(3)
plt.plot(time,signal_to_split_normalized,'b')
for index_index_to_cut in time_to_cut:
    plt.axvline(index_index_to_cut,color='red')
plt.xlabel('Time (s)' ,fontsize =15)
plt.ylabel('Log normalized amplitude',fontsize =15)
plt.tick_params(labelsize=20)
plt.grid()


# define the signal list of the 13 signal with the spliting in the zones silence
    
list_signaux_split_log_signal = []
list_signal = []
    
for k in range(len(index_time_to_cut)-1):    
    list_signaux_split_log_signal.append(signal_to_split_normalized[np.asarray(index_time_to_cut[k]):np.asarray(index_time_to_cut[k+1])])
    list_signal.append(signal_amplitude[np.asarray(index_time_to_cut[k]):np.asarray(index_time_to_cut[k+1])])

# This fonction perform FFT on the signal to find the spectres
    
def spectrum(signal_array):
   
    fs = 44.1E3
    Nfft = 2**18
    df = fs/Nfft
    spectrum_fft = np.fft.fft(np.asarray(signal_array),Nfft)
   
    return abs(spectrum_fft)/(max(abs(spectrum_fft)))


# based on the 13 signals, find 13 spectre based on the function above

list_spectrum = []
for j_index_signal in list_signal:
    list_spectrum.append(spectrum(j_index_signal))

# defind the frequence axis 

fs = 44.1E3
Nfft = 2**18
df = fs/Nfft
frequency = np.arange(0,Nfft*df,df)

# defind the notes played based on the file name

legend = ['C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4']


# spectrum plot 
count =0

plt.figure(4)
plt.plot(frequency,list_spectrum[0],label = 'C4')
plt.xlim(100,10000)
plt.xscale('log')
plt.legend()
count += 1
plt.xlabel('Frequency (Hz)' ,fontsize =15)
plt.ylabel('Normalized amplitude',fontsize =15)
plt.tick_params(labelsize=20)
plt.grid()   

# create CSV of all spectre and signals
# import pandas as pd

# for jjj in range(len(list_spectrum)):
#     pd.DataFrame(list_signal[0]).to_csv('signal_'+legend[jjj]+'.csv')    
#     pd.DataFrame(list_spectrum[0][0:15000]).to_csv('spectre'+legend[jjj]+'.csv')    


index_chunk_frequency = np.where((frequency>50) & (frequency<15000))
chunk_frequency = frequency[index_chunk_frequency]

list_of_chunk_spectrum = []

for index_list_of_chunk_spectrum in list_spectrum:
    list_of_chunk_spectrum.append(index_list_of_chunk_spectrum[index_chunk_frequency])
    


# plt.plot(chunk_frequency,list_of_chunk_spectrum[0])
# plt.xscale('log')
# plt.legend()
# plt.xlabel('Frequency (Hz)' ,fontsize =15)
# plt.ylabel('Normalized amplitude',fontsize =15)
# plt.tick_params(labelsize=20)
# plt.grid()   



# In this subsection : the data to extract are the amplitude of the harmonic peaks from the spectrum 


# function for the files to have the data : 
    
def parameter_extractor(list_of_chunk_spectrum):    
    list_harmonics_amplitude = []
    list_harmonics_frequency_position = []
    list_harmonics_distances = []
    
    peaks_signal, _ = find_peaks((list_of_chunk_spectrum),height=0.00005)
    
    
    signal_to_test_the_technique = list_of_chunk_spectrum
    
    
    
    plt.plot(chunk_frequency,signal_to_test_the_technique)
    plt.plot(chunk_frequency[peaks_signal],signal_to_test_the_technique[peaks_signal],'.r')
    
    from scipy import interpolate
    f = interpolate.interp1d(chunk_frequency[peaks_signal],signal_to_test_the_technique[peaks_signal], kind = 'cubic')
    x_new = np.arange(min(chunk_frequency[peaks_signal]),max(chunk_frequency[peaks_signal]),df)
    y_new = f(x_new)
    
    
    peaks_signal_interpolation, _ = find_peaks(y_new,height=0.05)
    
    
    
    list_of_all_max_spectrum = []
    list_of_all_index_of_max_spectrum = []
    
    
          # list_of_max_spectrum.append(chunk_frequency[peaks_signal[index_peaks_signal]])
          # list_index_of_max_spectrum.append(peaks_signal[index_peaks_signal])
    
    local_max_spectrum = []
    local_index_max = []
    
    local_max_spectrum.append(chunk_frequency[peaks_signal_interpolation[0]])
    local_index_max.append(peaks_signal_interpolation[0])    
    
    
    for index_peaks_signal in range(1,len(peaks_signal_interpolation),1):
        
        if chunk_frequency[peaks_signal_interpolation[index_peaks_signal]] - chunk_frequency[peaks_signal_interpolation[index_peaks_signal - 1]] < 10:
            local_max_spectrum.append(chunk_frequency[peaks_signal_interpolation[index_peaks_signal]])
            local_index_max.append(peaks_signal_interpolation[index_peaks_signal]) 
        
        elif chunk_frequency[peaks_signal_interpolation[index_peaks_signal]] - chunk_frequency[peaks_signal_interpolation[index_peaks_signal - 1]] > 10:
            
            list_of_all_max_spectrum.append(local_max_spectrum)
            # print(list_of_all_max_spectrum)
        
            list_of_all_index_of_max_spectrum.append(local_index_max) 
            # print(list_of_all_index_of_max_spectrum)
            
            local_max_spectrum = []
            local_index_max = []
            
            local_max_spectrum.append(chunk_frequency[peaks_signal_interpolation[index_peaks_signal]])
            local_index_max.append(peaks_signal_interpolation[index_peaks_signal]) 
            
        if index_peaks_signal == len(peaks_signal)-1:
            
            list_of_all_max_spectrum.append(local_max_spectrum)    
            list_of_all_index_of_max_spectrum.append(local_index_max)     
        
        
    
    harmonics_amplitude = []
    harmonics_frequency_position = []
    harmonics_distances = []
    
    for index_list_of_all_index_of_max_spectrum in list_of_all_index_of_max_spectrum:
        
        harmonics_amplitude.append(max(signal_to_test_the_technique[index_list_of_all_index_of_max_spectrum]))
        
        for index_harmonic_frequency_pos in index_list_of_all_index_of_max_spectrum:
            if max(signal_to_test_the_technique[index_list_of_all_index_of_max_spectrum]) == signal_to_test_the_technique[index_harmonic_frequency_pos]:
                harmonics_frequency_position.append(chunk_frequency[index_harmonic_frequency_pos])    
            
    for index_calcul_harmonic_distance in range(len(harmonics_frequency_position)-1):
        harmonics_distances.append(harmonics_frequency_position[index_calcul_harmonic_distance+1] - harmonics_frequency_position[index_calcul_harmonic_distance])
        
        
    print(harmonics_amplitude)
    print(harmonics_frequency_position)
    print(harmonics_distances)
    
    list_harmonics_amplitude.append(harmonics_amplitude)
    list_harmonics_frequency_position.append(harmonics_frequency_position)
    list_harmonics_distances.append(harmonics_distances)
    return list_harmonics_amplitude,list_harmonics_frequency_position,list_harmonics_distances


list_harmonics_amplitude,list_harmonics_frequency_position,list_harmonics_distances = parameter_extractor(list_of_chunk_spectrum[0])

