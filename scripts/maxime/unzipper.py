# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 09:52:02 2023

@author: digi
"""

import os
import pathlib
import zipfile

    # Get current working path and create unzipped files directory

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