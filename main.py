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

    

from setup import parameter_extractor
from setup import list_of_notes
from setup import traitement_du_signal_spliteur
from setup import renamer
from setup import unzipper

# STEP 1 : Unzip file the file with all the sound files

unzipper()

# STEP 2 : Make all the name standard for the treatement 

renamer()

# STEP 3 : read CSV file with the frequencies relative to all the notes

list_note = list_of_notes()

# STEP 4 : append numerical values based on the spectrum analysis and the peak extractor

list_total_signal,list_total_spectre,list_file_names,list_total_harmonics_amplitude,list_total_harmonics_frequency_position,list_total_harmonics_distances,list_total_list_str_max_harmonic_note,list_total_list_str_first_harmonic_note = traitement_du_signal_spliteur(list_note)

#%% DB MONGO

# Création bdd mongo avec signleton

from mongo_db_singleton import *

mongo_client = MongoDBSingleton.get_instance().client

# Clean from previous database

database_list = mongo_client.list_database_names()

if 'projet-spectre' in database_list:
    db = mongo_client.drop_database('projet-spectre')

# Create project's database

db = mongo_client['projet-spectre']


# Définir le schéma des documents de la collection
schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["pitched", "type", "instrument", "option", "dynamique","fichier_octave", "signal", "spectre", "harmonique_amplitude", "harmonique_fondamental", "harmonique_distance_entre_harmonique","Note_first_harmonique","Note_max_harmonique"],
        "properties": {
            "pitched": {"bsonType": "bool"},
            "type": {"bsonType": "string"},
            "instrument": {"bsonType": "string"},
            "option": {"bsonType": "string"}, 
            "dynamique": {"bsonType": "string"},
            "fichier_octave" : {"bsonType": "string"},
            "signal": {"bsonType": "array"},
            "spectre": {"bsonType": "array"},   
            "harmonique_amplitude": {"bsonType": "array"},
            "harmonique_fondamental": {"bsonType": "array"},
            "harmonique_distance_entre_harmonique": {"bsonType": "array"},
            "Note_first_harmonique": {"bsonType": "string"},
            "Note_max_harmonique" : {"bsonType": "string"},
            
        }
    }
}

# Cette commande acte comme un buffer pour remedier au nettoyage de la base de donnee dans chaque Run

db_stats = db.command('dbStats')
if db_stats['collections'] == 0:
    collection = db.create_collection("Full_data_with_harmonics_amp_and_pos_note_with_post_traitement_tkinter", validator=schema)
else :
    collection = db['Full_data_with_harmonics_amp_and_pos_note_with_post_traitement_tkinter']

#%% AJOUT DANS LA DB

    # Séparation des informations à partir des noms de fichiers

for index_file_name in range(len(list_file_names)):
    informations = list_file_names[index_file_name].split('_')

    pitched = bool(informations[0])
    type_instrument_mongo = informations[1]
    instrument_mongo = informations[2]
    option_mongo = informations[3]
    dynamique_mongo = informations[4]
    file_octave_mongo = list_file_names[index_file_name]
    signal_mongo = list_total_signal[index_file_name].tolist()
    spectre_mongo = list_total_spectre[index_file_name].tolist()
    harmonique_amplitude_mongo = list_total_harmonics_amplitude[index_file_name]
    harmonique_fondamental_mongo = list_total_harmonics_frequency_position[index_file_name]
    harmonique_distance_between_harmonics_mongo = list_total_harmonics_distances[index_file_name]
    Note_first_harmonique_mongo = str(list_total_list_str_first_harmonic_note[index_file_name])
    Note_max_harmonique_mongo = str(list_total_list_str_max_harmonic_note[index_file_name])
    
    
  
    doc_new = {
      'pitched': pitched,
      'type': type_instrument_mongo,
      'instrument': instrument_mongo,
      'option': option_mongo, 
      'dynamique': dynamique_mongo,
      'fichier_octave' : file_octave_mongo,
      'signal': signal_mongo,
      'spectre': spectre_mongo,
      'harmonique_amplitude': harmonique_amplitude_mongo,
      'harmonique_fondamental': harmonique_fondamental_mongo,
      'harmonique_distance_entre_harmonique': harmonique_distance_between_harmonics_mongo,
      'Note_first_harmonique' : Note_first_harmonique_mongo,
      'Note_max_harmonique':Note_max_harmonique_mongo
    }
      
    
        # Ajouter ce dict comme un nouveau document dans la db mongodb
        
    collection.insert_one(doc_new)


# Lancement de l'application GUI

from Application import init_application

init_application(collection)


   
    
    
    
    
    






    




