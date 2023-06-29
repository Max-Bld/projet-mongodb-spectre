# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:52:02 2023

@author: digi
"""

import os
import pathlib
import zipfile

path = "C:/Users/digi/maxime_blanchard/projet_spectre/data/"

file_list = os.listdir(path)

path_to_extract = "C:/Users/digi/maxime_blanchard/projet_spectre/sounds/"


#%%

for n in range(len(file_list)): # for looping through the whole file_list

    file_name = path + file_list[n]
    sub_folder_path = (path_to_extract + file_list[n]).replace('.zip', '')
    os.mkdir(sub_folder_path)
    with zipfile.ZipFile(file_name, 'r') as file_to_unzip:
        file_to_unzip.printdir()
        file_to_unzip.extractall(sub_folder_path)
