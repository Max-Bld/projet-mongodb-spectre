#!/usr/bin/env python3

import sys
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import random


def spectrum(signal_array):
   
    fs = 44.1E3
    Nfft = 2**18
    spectrum_fft = np.fft.fft(np.asarray(signal_array),Nfft)
   
    return abs(spectrum_fft)/(max(abs(spectrum_fft)))




def main():
    
    sample_rate = 44100 # sample rate
    chunk = int(0.1*sample_rate) # number of data points to read at a time
    delta_t = 1/44100
        
    time_axis = np.arange(0,delta_t*chunk,delta_t)
    
    Nfft = 2**18
    delta_f = sample_rate/Nfft
    frequency_axis = np.arange(0,delta_f*Nfft,delta_f)
    


    p=pyaudio.PyAudio() # start the PyAudio class
    stream=p.open(format=pyaudio.paInt16,
              channels=1,
              rate=sample_rate,
              input=True,
              frames_per_buffer=chunk) #uses default input device


    session = np.empty(0)


    while True:
     
        data = np.fromstring(stream.read(chunk),dtype=np.int16)
        session = np.append(arr=session, values=data)
        
        frequence = random.randrange(50, 10000)
        
        
        w = 2 * np.pi * frequence

        amplitude  = np.sin(w*time_axis)

        fft_result = spectrum(amplitude)
        
        sin_data = data + amplitude
        
        
        fig = plt.figure(1)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        
        ax1.plot(time_axis,sin_data)
        ax2.plot(frequency_axis,fft_result)
        ax1.set_ylim(-1,1)
        ax1.set_xlim(0,0.01)
        ax2.set_ylim(0,1)
        ax2.set_xlim(0,5000)
        plt.draw()
        plt.pause(0.001)
        plt.clf()
        
        print("-----------------------------------")
        print(len(sin_data)) #4410
        chunk_frequency = frequency_axis[np.where((frequency_axis>20)&(frequency_axis<15000))]
        chunk_spectre = fft_result[np.where((frequency_axis>20)&(frequency_axis<15000))]
        
        print(len(fft_result[np.where((frequency_axis>20)&(frequency_axis<15000))])) # spectre 80000
        
        F_max = chunk_frequency[np.argmax(chunk_spectre)]
        print(str(F_max)) # Fmax 
        
        print(frequence)

        print("-----------------------------------")

            
        
        
    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == '__main__':
    
    main()
    

























