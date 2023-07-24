# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:35:18 2023

@author: digi
"""


import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

#%% FUNCTIONS

def spectrum(signal_array):
   
    fs = 44.1E3
    Nfft = 2**18
    df = fs/Nfft
    spectrum_fft = np.fft.fft(np.asarray(signal_array),Nfft)
   
    return abs(spectrum_fft)/(max(abs(spectrum_fft)))

#%% AUDIO

# t0 = time.perf_counter()
# time.sleep(1)
# t1 = time.perf_counter() - t0

sample_rate = 44100 # sample rate
chunk = int(0.1*sample_rate) # number of data points to read at a time


p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,
              channels=1,
              rate=sample_rate,
              input=True,
              frames_per_buffer=chunk) #uses default input device


session = np.empty(0)

#%% REAL TIME STREAM AND PLOT

# MAX NO. OF POINTS TO STORE
# que = deque(maxlen = chunk)
# que_2 = deque(maxlen = 2**18)

while True:    # infinite loop,
# for n in range(5): # or specify the number of seconds
    
   
    data = np.fromstring(stream.read(chunk),dtype=np.int16)
    session = np.append(arr=session, values=data)
    # print(data)
    
    fft_result = spectrum(data)

    # for y in data :
    #     que.append(y)
        
	
    	# PLOTTING THE POINTS
    
        ## Multiple dynamic plots
    
    fig = plt.figure(1)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    
    ax1.plot(data)
    ax2.plot(fft_result)
    ax1.set_ylim(-50000,50000)
    # ax1.set_xlim()
    ax2.set_ylim(0,1)
    ax2.set_xlim(0,50000)
    plt.draw()
    plt.pause(0.001)
    plt.clf()
        
        ## Signal plot
    
    
    # plt.figure(1)
    # plt.plot(data)
    # # plt.scatter(range(len(que)),que)
    
    #   	 # SET Y AXIS RANGE
    # plt.ylim(-50000,50000)
     	
    #   	 # DRAW, PAUSE AND CLEAR
    # plt.draw()
    # plt.pause(0.001)
    # plt.clf()
    
    #     ## Spectrum plot
    
    # plt.figure(2)
    # plt.plot(fft_result)
    # plt.xlim(0,50000)
    # plt.draw()
    # plt.pause(0.001)
    # plt.clf()
       
plt.figure(555)
plt.plot(session)

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()


#%% Spectrum



session_spectre = spectrum(session)

fs = 44.1E3
Nfft = 2**18
df = fs/Nfft
frequency = np.arange(0,Nfft*df,df)

plt.figure(2)
plt.plot(frequency,session_spectre)

#%% READING ARRAY INTO AUDIO

pa=pyaudio.PyAudio()

read_stream = pa.open(format=pyaudio.paInt16, rate = sample_rate, channels = 1, input=True, output=True )
# Assuming you have a numpy array called samples
read_file = session.tostring()
read_stream.write(read_file)
