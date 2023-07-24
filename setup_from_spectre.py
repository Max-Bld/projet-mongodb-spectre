# This file contains your application setup code (should be run first and only one time)

import numpy as np
import aifc
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.signal import find_peaks
import os
import pandas as pd
from scipy import interpolate
from pymongo import MongoClient
import os
import shutil
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from matplotlib.ticker import FormatStrFormatter
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bson import ObjectId
import pathlib
import zipfile




def renamer():
    #%% Paths

    files_list = []
    
    # The next lines standardized the path file
    
    
    split_word = "b-spectre"
    root = (__file__.split(split_word)[0] + r"b-spectre\assets\theremin\pitched").replace( "\\", "/")
    
    #%%
    if os.path.exists(root) == False :        
        os.mkdir(f"{root}")
    
    keywords_banned = ['stereo', 'wav', 'silence']
    sound_source = root[-16:].removesuffix(r"/pitched")
    
    #%%
    
    if os.path.exists(f"{root}/Guitar.mono.1644.1/") == True :
    
        for guitar_file in os.listdir(f"{root}/Guitar.mono.1644.1/1644mono"):
            os.rename(f"{root}/Guitar.mono.1644.1/1644mono/{guitar_file}", f"{root}/Guitar.mono.1644.1/{guitar_file}")
        
        os.rmdir(f"{root}/Guitar.mono.1644.1/1644mono")
        
    else :
        pass
    
    
        #%% Cleaning the sound bank
    
    
    
    for folder in os.listdir(root):   
        if "stereo" in folder:
            shutil.rmtree(f"{root}/{folder}")
            print('delete stereo')
            continue
            
        elif "2496" in folder:
            shutil.rmtree(f"{root}/{folder}")
            print('delete 2496')
            continue
        
        for subfolder in os.listdir(f"{root}/{folder}"):
            
            if "__MACOSX" in subfolder:
                shutil.rmtree(f"{root}/{folder}/{subfolder}")
                print('delete mac')
                continue           
            
        #%% File standardization
        
    
    for folder in os.listdir(root):
    
    
        for file in os.listdir(f"{root}/{folder}") :
            
            
            # Remove files containing forbidden keywords
    
            files_list.append(file)
            for keyword in keywords_banned:
                if keyword in file:
                    os.remove(f"{root}/{folder}/{file}")
    
                 
                # Adding sound bank name
            
            keywords_to_change = ['.arco', '.stick', '.pizz', '.brass']
            keywords_dynamic = ['pp', 'mf', 'ff']    
            for file in os.listdir(f"{root}/{folder}") :
                if f"1_theremin" not in file:    
                    old_name =   f"{root}/{folder}/{file}"
                    new_name = f"{root}/{folder}/1_{sound_source}_{file}"
                    os.rename(old_name,new_name)
                else:
                    break
    
                    
                # Instrument name standardization
                
            for file in os.listdir(f"{root}/{folder}") :
                for keyword in keywords_to_change:
                    if keyword in file :
                        new_file = file.replace(keyword, keyword[1:])   
                        old_name =   f"{root}/{folder}/{file}"
                        new_name = f"{root}/{folder}/{new_file}"
                        os.rename(old_name,new_name)
    
            
                # Adding nodyn if dynamic is null
            
            for file in os.listdir(f"{root}/{folder}") :                    
                if 'ff' in file:
                    continue
                elif 'mf' in file:
                    continue
                elif 'pp' in file:
                    continue
                elif 'nodyn' in file:
                    continue
                else: 
                    new_file = file[:-5] + ".nodyn" + file[-5:]
                    old_name = f"{root}/{folder}/{file}"
                    new_name = f"{root}/{folder}/{new_file}"
                    os.rename(old_name,new_name)
    
                       
        #%% Replacing . with _ and uniformisation of file extension to .aiff
                        
        for file in os.listdir(f"{root}/{folder}") :                    
            new_file = file.lower().replace('.mono', '').replace('.', '_').replace('_aiff', '.aiff').replace("_aif", '.aiff')
            old_name = f"{root}/{folder}/{file}"
            new_name = f"{root}/{folder}/{new_file}"
            os.rename(old_name,new_name)
            
            
        
        for file in os.listdir(f"{root}/{folder}") :
            # print(file.count('_'))
            if file.count('_') < 4:
                os.remove(f"{root}/{folder}/{file}")
                continue
            
            elif file.count('_') > 5:
                os.remove(f"{root}/{folder}/{file}")
                continue
                        
            elif ((file.count('_') == 4) and 'mf' in file):
                new_file = file.replace('_mf', '_nooption_mf')
                old_name = f"{root}/{folder}/{file}"
                new_name = f"{root}/{folder}/{new_file}"
                os.rename(old_name,new_name)
                continue
                
            elif ((file.count('_') == 4) and 'pp' in file):
                new_file = file.replace('_pp', '_nooption_pp')
                old_name = f"{root}/{folder}/{file}"
                new_name = f"{root}/{folder}/{new_file}"
                os.rename(old_name,new_name)
                continue
            
            elif ((file.count('_') == 4) and 'ff' in file):
                new_file = file.replace('_ff', '_nooption_ff')
                old_name = f"{root}/{folder}/{file}"
                new_name = f"{root}/{folder}/{new_file}"
                os.rename(old_name,new_name)
                continue
                
            else:
                continue
    
    #%% Special process for guitar files
    
    if os.path.exists(f"{root}/Guitar.mono.1644.1/") == True :
    
        for guitar_file in os.listdir(f"{root}/Guitar.mono.1644.1/"):
            old_name = guitar_file
            new_name = guitar_file[:18] + guitar_file[21:25] + guitar_file[17:20] + guitar_file[25:]
            os.rename(f"{root}/Guitar.mono.1644.1/{old_name}",f"{root}/Guitar.mono.1644.1/{new_name}")
    else:
        pass
    
    #%% Special process for violin
    
    if os.path.exists(f"{root}/Violin.arco.mono.1644.1/") == True :
    
        for violinarco_file in os.listdir(f"{root}/Violin.arco.mono.1644.1/"):
            old_name = violinarco_file
            new_name = violinarco_file[:22] + violinarco_file[25:29] + violinarco_file[21:24] + violinarco_file[29:]
            os.rename(f"{root}/Violin.arco.mono.1644.1/{old_name}",f"{root}/Violin.arco.mono.1644.1/{new_name}")
            
    else:
        pass



def unzipper():
    # Get current working path and create unzipped files directory
    
    # The next two line standardized the path file
    split_word = "b-spectre"
    root = (__file__.split(split_word)[0])
    path_to_zip = fr"{root}b-spectre\assets\theremin\zip".replace( "\\", "/")
    path_to_extract = fr"{root}b-spectre\assets\theremin\pitched".replace( "\\", "/")

    file_list = os.listdir(path_to_zip)

        # Execute the loop if the unzipped files directory is empty

    if len(os.listdir(path_to_extract)) == 0:
        for n in range(len(file_list)): 
        
            zip_file = f"{path_to_zip}/{file_list[n]}"
            sub_folder_path = f"{path_to_extract}/{file_list[n]}".replace('.zip', '')
            os.mkdir(sub_folder_path)
            with zipfile.ZipFile(zip_file, 'r') as file_to_unzip:
                file_to_unzip.printdir()
                file_to_unzip.extractall(sub_folder_path)


def list_of_notes():
    
    
    # The next two line standardized the path file
    split_word = "b-spectre"
    path = (__file__.split(split_word)[0] + r"b-spectre\assets\frequence_notes.csv").replace( "\\", "/")
    
    # Read cvs of the note frequencies along all the musical octaves
    data = pd.read_csv(path)
    return data

def parameter_extractor(chunk_spectrum,chunk_frequency,list_note):    
    
    # This function act on the spectrum to extract the harmonic notes of the first bar and the max bar on the spectrum
    # These value are used in the Tkinter app
    
    
    # Init
 
    list_max_harmonic_note = []
    list_first_harmonic_note = []
    
    
    # Spectrum threshold to detect all the peaks above 0.000002
    
    
    peaks_signal, _ = find_peaks((chunk_spectrum),height=0.00002)
    
    # Signal processing parameters
    
    fs = 44.1E3
    Nfft = 2**18
    df = fs/Nfft

   
    # Interpolation of the spectrum maximum for more precise harmonic detection 
    
    f = interpolate.interp1d(chunk_frequency[peaks_signal],chunk_spectrum[peaks_signal], kind = 'cubic')
    x_new = np.arange(min(chunk_frequency[peaks_signal]),max(chunk_frequency[peaks_signal]),df)
    y_new = f(x_new)
    
    
    # Detection of all the minimum
    
    peaks_signal_interpolation, _ = find_peaks(y_new,height=0.05)
    
    # In this subsection, the traitement is more complex since the spectrul extremum are not single in each peak
    # For each harmonic all the max higher than the threshold are kept and stored in list for each bar in the spectrum
    
    #init 
    
    list_of_all_max_spectrum = []
    list_of_all_index_of_max_spectrum = []
    
    local_max_spectrum = []
    local_index_max = []
    
    local_max_spectrum.append(chunk_frequency[peaks_signal_interpolation[0]])
    local_index_max.append(peaks_signal_interpolation[0])    
    
    # The max of each spectrum is kept
    # output all the minimum extrmum relative to the max of each bar 
    # Traitement accuracy 77.3%
    
    for index_peaks_signal in range(1,len(peaks_signal_interpolation),1):
        
        if chunk_frequency[peaks_signal_interpolation[index_peaks_signal]] - chunk_frequency[peaks_signal_interpolation[index_peaks_signal - 1]] < 10:
            local_max_spectrum.append(chunk_frequency[peaks_signal_interpolation[index_peaks_signal]])
            local_index_max.append(peaks_signal_interpolation[index_peaks_signal]) 
        
        elif chunk_frequency[peaks_signal_interpolation[index_peaks_signal]] - chunk_frequency[peaks_signal_interpolation[index_peaks_signal - 1]] > 10:
            
            list_of_all_max_spectrum.append(local_max_spectrum)
        
            list_of_all_index_of_max_spectrum.append(local_index_max) 
            
            local_max_spectrum = []
            local_index_max = []
            
            local_max_spectrum.append(chunk_frequency[peaks_signal_interpolation[index_peaks_signal]])
            local_index_max.append(peaks_signal_interpolation[index_peaks_signal]) 
            
        if index_peaks_signal == len(peaks_signal)-1:
            
            list_of_all_max_spectrum.append(local_max_spectrum)    
            list_of_all_index_of_max_spectrum.append(local_index_max)     
        
    # append harmonics_amplitude,harmonics_frequency_position,harmonics_distances based on the csv file of the frequency value relative to the musical note
    
    harmonics_amplitude = []
    harmonics_frequency_position = []
    harmonics_distances = []
    
    for index_list_of_all_index_of_max_spectrum in list_of_all_index_of_max_spectrum:
        
        # conditon pour stocker les max des valeur de spectre local 
        harmonics_amplitude.append(max(chunk_spectrum[index_list_of_all_index_of_max_spectrum]))
        
        for index_harmonic_frequency_pos in index_list_of_all_index_of_max_spectrum:
            if max(chunk_spectrum[index_list_of_all_index_of_max_spectrum]) == chunk_spectrum[index_harmonic_frequency_pos]:
                harmonics_frequency_position.append(chunk_frequency[index_harmonic_frequency_pos])    
            
    for index_calcul_harmonic_distance in range(len(harmonics_frequency_position)-1):
        harmonics_distances.append(harmonics_frequency_position[index_calcul_harmonic_distance+1] - harmonics_frequency_position[index_calcul_harmonic_distance])
        

    # If the file is not supported by the traitement, this condition act as a buffer
    
    if len(harmonics_frequency_position) != 0:
        first_harmonic = harmonics_frequency_position[0]
        print('----------------------')
        print('first harmonics')
        print(first_harmonic)
        max_harmonic = harmonics_frequency_position[np.argmax(harmonics_amplitude)]
        print('Max harmonics')
        print(max_harmonic)
        
        
        # index value of harmonic to musical notes based on the csv file in assets 
        str_first_harmonic_note = list_note['Note'][np.where((first_harmonic>=list_note['Min'])&(first_harmonic<=list_note['Max']))[0][0]]
        str_max_harmonic_note = list_note['Note'][np.where((max_harmonic>=list_note['Min'])&(max_harmonic<=list_note['Max']))[0][0]]
    
    else :     
        str_first_harmonic_note = None
        str_max_harmonic_note = None
    
    
    return harmonics_distances,harmonics_frequency_position,harmonics_distances,str_max_harmonic_note,str_first_harmonic_note


def traitement_du_signal_spliteur(list_note):
        
    
    list_total_signal = []
    list_total_spectre = []
    list_file_names = []
    
    list_total_harmonics_amplitude = []
    list_total_harmonics_frequency_position = []
    list_total_harmonics_distances = []
    list_total_list_str_max_harmonic_note = []
    list_total_list_str_first_harmonic_note = []
    
    
    split_word = "b-spectre"
    path_data_organiser = (__file__.split(split_word)[0] + r"b-spectre/assets/theremin/pitched/ensemble_instrument").replace( "\\", "/")
    datafolder = (__file__.split(split_word)[0] + r"b-spectre/assets/theremin/pitched/ensemble_instrument/").replace( "\\", "/")
    
    
    for n in os.listdir(path_data_organiser):
    
        Name_file = n
        
        signal = aifc.open(datafolder + Name_file)
        getchannels = signal.getnchannels()
        nframes = signal.getnframes()
        samplewidth = signal.getsampwidth()
        
        #%% Signal reader 
        
        strsig = signal.readframes(nframes)
        signal_amplitude = np.fromstring(strsig, np.short).byteswap()
        
        # Sample frequency  
        
        framerate = signal.getframerate()
        
        fmax = framerate
        
        # Time step => delta_t
        
        delta_t = 1/fmax
        
        # time axis based on the length of the signal
        
        time = np.arange(0,len(signal_amplitude)*delta_t,delta_t)
        
        
        #%% Test plot normalized signal
        
        # plt.figure(1)
        # plt.plot(time,signal_amplitude/max(signal_amplitude))
        # plt.xlabel('Time (s)' ,fontsize =15)
        # plt.ylabel('Normalized amplitude',fontsize =15)
        # plt.tick_params(labelsize=20)
        # plt.grid()
        
        
        
        #%% Time signal on log representation 
        
        signal_to_split = 20*np.log10(abs(hilbert(signal_amplitude)))
        
        
        # Time signal normalized log representation
        
        signal_to_split_normalized = signal_to_split - max(signal_to_split)
        
        
        # Find the peaks where the silence is performed 
        
        peaks_signal, _ = find_peaks(-1*(signal_to_split_normalized),height=80)
        
        #%% plot the normlized log signal representation & the silence zones where the split is performed 
        
        # plt.figure(2)
        # plt.plot(time,signal_to_split_normalized,'b')
        # plt.plot(time[peaks_signal],signal_to_split_normalized[peaks_signal],'.r')
        # plt.xlabel('Time (s)' ,fontsize =15)
        # plt.ylabel('Log normalized amplitude',fontsize =15)
        # plt.tick_params(labelsize=20)
        # plt.grid()
        
         
        #%% time and amplitude of the silence zones
        
        peaks_time = time[peaks_signal]   
        peaks_amplitude = signal_to_split_normalized[peaks_signal] 
         
        # init list for spliting the signal based on the 13 notes played
        
        time_to_cut = []    
        time_to_cut.insert(0,0)
        index_time_to_cut = []
        index_time_to_cut.insert(0,0)
        
        # defind the spliting zones based on silences
        
        for index_time_peaks in range(len(peaks_time)-1):
            if peaks_time[index_time_peaks] - peaks_time[index_time_peaks - 1] > 1:
                time_to_cut.append(peaks_time[index_time_peaks])
                index_time_to_cut.append(np.where(time == peaks_time[index_time_peaks])[0][0])
        
        
        # plot the spliting zones with vertical lines
        
        # plt.figure(3)
        # plt.plot(time,signal_to_split_normalized,'b')
        # for index_index_to_cut in time_to_cut:
        #     plt.axvline(index_index_to_cut,color='red')
        # plt.xlabel('Time (s)' ,fontsize =15)
        # plt.ylabel('Log normalized amplitude',fontsize =15)
        # plt.tick_params(labelsize=20)
        # plt.grid()
        
        
        #%% define the signal list of the 13 signal with the spliting in the zones silence
            
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
        
        
        #%% based on the 13 signals, find 13 spectre based on the function above
        
        list_spectrum = []
        for j_index_signal in list_signal:
            list_spectrum.append(spectrum(j_index_signal))
        
        #%% defind the frequence axis 
        
        fs = 44.1E3
        Nfft = 2**18
        df = fs/Nfft
        frequency = np.arange(0,Nfft*df,df)
        
        # defind the notes played based on the file name
            
        
        # spectrum plot 
        # count =0
        
        # plt.figure(4)
        # for index_list_spectrum in list_spectrum:
        #     plt.plot(frequency,index_list_spectrum,label = legend[count])
        #     plt.xlim(100,10000)
        #     plt.xscale('log')
        #     plt.legend()
        #     count += 1
        # plt.xlabel('Frequency (Hz)' ,fontsize =15)
        # plt.ylabel('Normalized amplitude',fontsize =15)
        # plt.tick_params(labelsize=20)
        # plt.grid()   
        
        #%% create CSV of all spectre and signals
        # import pandas as pd
        
        # for jjj in range(len(list_spectrum)):
        #     pd.DataFrame(list_signal[0]).to_csv('signal_'+legend[jjj]+'.csv')    
        #     pd.DataFrame(list_spectrum[0][0:15000]).to_csv('spectre'+legend[jjj]+'.csv')    
        
        
        index_chunk_frequency = np.where((frequency>50) & (frequency<15000))
        chunk_frequency = frequency[index_chunk_frequency]
        
        list_of_chunk_spectrum = []
        
        for index_list_of_chunk_spectrum in list_spectrum:
            list_of_chunk_spectrum.append(index_list_of_chunk_spectrum[index_chunk_frequency])
        
        #%%
        
        list_harmonics_amplitude = []
        list_harmonics_frequency_position = []
        list_harmonics_distances = []
        list_str_max_harmonic_note =  []
        list_str_first_harmonic_note = []
        
        for index_list_of_chunk_spectrum_data_num in list_of_chunk_spectrum:
            harmonics_amplitude,harmonics_frequency_position,harmonics_distances,str_max_harmonic_note,str_first_harmonic_note = parameter_extractor(index_list_of_chunk_spectrum_data_num,chunk_frequency,list_note)
            list_harmonics_amplitude.append(harmonics_amplitude)
            list_harmonics_frequency_position.append(harmonics_frequency_position)
            list_harmonics_distances.append(harmonics_distances)
            list_str_max_harmonic_note.append(str_max_harmonic_note)
            list_str_first_harmonic_note.append(str_first_harmonic_note)
    
    
    #%%
    
        # Noms des notes de l'octave:
    
        # notes = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5']
        
            # A la condition qu'il y ait bien douze fichiers splittés        
        
        for x in list_signal:                   # Ajouter les signaux
            list_total_signal.append(x)             
        
        for z in list_of_chunk_spectrum:        # Ajouter les spectres
            list_total_spectre.append(z)
        
        for y in range(len(list_signal)):       # Ajouter le nom des notes aux fichiers
            list_file_names.append(n)
            
        for index_list_harmonics_amplitude in list_harmonics_amplitude:  # Ajouter de variable nnumérique
            list_total_harmonics_amplitude.append(index_list_harmonics_amplitude)
        
        for index_list_harmonics_amplitude in list_harmonics_frequency_position:  # Ajouter de variable nnumérique
            list_total_harmonics_frequency_position.append(index_list_harmonics_amplitude)
            
        for index_list_harmonics_frequency_position in list_harmonics_frequency_position:  # Ajouter de variable nnumérique
            list_total_harmonics_distances.append(index_list_harmonics_frequency_position)
        
        for index_list_str_max_harmonic_note in list_str_max_harmonic_note:  # Ajouter de variable nnumérique
            list_total_list_str_max_harmonic_note.append(index_list_str_max_harmonic_note)    
        
        for index_list_str_first_harmonic_note in list_str_first_harmonic_note:  # Ajouter de variable nnumérique
            list_total_list_str_first_harmonic_note.append(index_list_str_first_harmonic_note)
        
    return list_total_signal,list_total_spectre,list_file_names,list_total_harmonics_amplitude,list_total_harmonics_frequency_position,list_total_harmonics_distances,list_total_list_str_max_harmonic_note,list_total_list_str_first_harmonic_note