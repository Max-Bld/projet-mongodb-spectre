# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 16:57:07 2023

@author: digi
"""

    # Importing librairies

import requests
from bs4 import BeautifulSoup
import urllib.request

    # Get HTML code from the main page ('parent') containing links to sub-sections (children)

parent = "https://theremin.music.uiowa.edu/"

response = requests.get(parent)

soup = BeautifulSoup(response.content, 'html.parser')

    # Put in a list all the other sections' path ('children')

list_child = []

for link in soup.find_all('a'):
    list_child.append(link.get('href'))

children=[]

for n in list_child:
    if 'MIS' in n :
        children.append(n)

    # Soup list

soup_list = []

for child in children:
    response = requests.get(parent + child)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_list.append(soup)

   # Put in a list all sound files URL
    
sound_list = []
            
    # Soup list
            
for n in range(len(soup_list)):
    for link in soup_list[n].find_all('a'):
        sound_list.append(link.get('href'))
        if 'zip' not in sound_list[-1]:
            sound_list.remove(sound_list[-1])            

    # Replace ' ' by '%20'
            
sound_list_2=[]

for n in sound_list:
    sound_list_2.append(n.replace(' ', '%20'))
    
    # Get rid of duplicates  

sound_list_3 = sound_list_2

for n in sound_list_3:
    if ('ff' in n) or ('pp' in n) or ('mf' in n):
        sound_list_3.remove(n)

    #%% Download all sound files listed in the previous list with their respective names

split_word = "b-spectre"
root = (__file__.split(split_word)[0])
path_to_dl_files = fr"{root}b-spectre\assets\theremin\zip".replace( "\\", "/")

for n in sound_list_3 :
    urllib.request.urlretrieve(parent+n, f"{path_to_dl_files}/{n.split('/')[-1]}")