# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 14:15:31 2023

@author: digi
"""

import matplotlib.pyplot as plt
import numpy as np 

f = [20, 100, 400, 1000, 3200, 12800]
label_freq=[]

alpha = 0.0056 * (np.asarray(f)**0.75)

distance = np.arange(0,3.02,0.02)

Initial_amplitude = 1 

amplitude_all_frequencies_in_each_distance_log = []
amplitude_all_frequencies_in_each_distance = []



for index_alpha in alpha:
    amplitude_all_frequencies_in_each_distance_log.append(20*np.log10(Initial_amplitude*np.exp(-index_alpha*distance)))
    amplitude_all_frequencies_in_each_distance.append((Initial_amplitude*np.exp(-index_alpha*distance)))

for n in f :
    label_freq.append(str(n)+" Hz")


index_freq = 0
plt.figure(1)
for index_amplitude_all_frequencies_in_each_distance_log in amplitude_all_frequencies_in_each_distance_log :
    plt.plot(distance,index_amplitude_all_frequencies_in_each_distance_log,label=label_freq[index_freq])
    index_freq = index_freq +1 
    # plt.yscale('log')
    plt.ylim(-50,0)
   
    plt.legend(loc='lower right')
    plt.xlabel("m")
    plt.ylabel("dB")
    plt.grid()

    
index_freq = 0
plt.figure(2)
for index_amplitude_all_frequencies_in_each_distance in amplitude_all_frequencies_in_each_distance :
    plt.plot(distance,index_amplitude_all_frequencies_in_each_distance,label=label_freq[index_freq])
    index_freq = index_freq +1 
    # plt.yscale('log')
    
    plt.legend()
    plt.xlabel("m")
    plt.ylabel("dB")
    plt.grid()
