# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:55:15 2023

@author: digi
"""

import os
import shutil

    #%% Paths

files_list = []

    # Current working path

split_word = "b-spectre"
root = (__file__.split(split_word)[0] + r"b-spectre\assets\theremin\pitched").replace( "\\", "/")

keywords_banned = ['stereo', 'wav', 'silence']
sound_source = root[-16:].removesuffix(r"/pitched")

#%%

for guitar_file in os.listdir(f"{root}/Guitar.mono.1644.1/1644mono"):
    os.rename(f"{root}/Guitar.mono.1644.1/1644mono/{guitar_file}", f"{root}/Guitar.mono.1644.1/{guitar_file}")

os.rmdir(f"{root}/Guitar.mono.1644.1/1644mono")

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
    
        # Remove files containing forbidden keywords

for folder in os.listdir(root):
    for file in os.listdir(f"{root}/{folder}"):
        files_list.append(file)
        for keyword in keywords_banned:
            if keyword in file:
                os.remove(f"{root}/{folder}/{file}")
         
        # Adding sound bank name
    
    keywords_to_change = ['.arco', '.stick', '.pizz', '.brass']
    keywords_dynamic = ['pp', 'mf', 'ff']    
    for file in os.listdir(f"{root}/{folder}") :
        old_name =   f"{root}/{folder}/{file}"
        new_name = f"{root}/{folder}/1_{sound_source}_{file}"
        os.rename(old_name,new_name)              
        
        # Instrument name standardization
        
    for file in os.listdir(f"{root}/{folder}") :
        for keyword in keywords_to_change:
            if keyword in file :
                new_file = file.replace(keyword, keyword[1:])   
                old_name =   f"{root}/{folder}/{file}"
                new_name = f"{root}/{folder}/{new_file}"
                os.rename(old_name,new_name)   
    
        # Adding mf if dynamic is null
    
    for file in os.listdir(f"{root}/{folder}") :                    
        if '.ff' in file:
            continue
        elif '.mf' in file:
            continue
        elif '.pp' in file:
            continue
        else: 
            new_file = file[:-5] + "_mf" + file[-5:]
            old_name = f"{root}/{folder}/{file}"
            new_name = f"{root}/{folder}/{new_file}"
            os.rename(old_name,new_name)
           
        # Replacing . with _ and uniformisation of file extension to .aiff
            
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


for guitar_file in os.listdir(f"{root}/Guitar.mono.1644.1/"):
    old_name = guitar_file
    new_name = guitar_file[:18] + guitar_file[21:25] + guitar_file[17:20] + guitar_file[25:]
    os.rename(f"{root}/Guitar.mono.1644.1/{old_name}",f"{root}/Guitar.mono.1644.1/{new_name}")
    
#%% Special process for cello

for violinarco_file in os.listdir(f"{root}/Violin.arco.mono.1644.1/"):
    old_name = violinarco_file
    new_name = violinarco_file[:22] + violinarco_file[25:29] + violinarco_file[21:24] + violinarco_file[29:]
    os.rename(f"{root}/Violin.arco.mono.1644.1/{old_name}",f"{root}/Violin.arco.mono.1644.1/{new_name}")
    

#%%


