# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 14:37:26 2023

@author: Amine
"""


# module db mongo

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient




################################################
############## Connexion à la bdd ##############
################################################

# Connexion à la base de donnée 'projet-spectre'
client = MongoClient('mongodb://localhost:27017/')
db_name = "projet-spectre"
db = client[db_name]

# liste des collections de la base de données 'projet-spectre'
db.list_collection_names()

# Connexion à la collection 'data'
coll_name = "Full_data_with_harmonics_amp_and_pos_note_with_post_traitement_tkinter"
collection = db[coll_name]

fs = 44.1E3
Nfft = 2**18
df = fs/Nfft
delta_t = 1/fs
frequency = np.arange(0,Nfft*df,df)
index_frequency_chunk = np.where((frequency>50)&(frequency<15000))
frequency_chunk = frequency[index_frequency_chunk]


from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bson import ObjectId


root = Tk()
root.title('Database analysis musical instrument')
root.geometry("1400x900")

class Application:
    
    def __init__(self,root,start,stop,collection,frequency_chunk):
      
        self.start = start
        self.stop = stop
        self.root = root
        self.tree = ttk.Treeview(root)
        self.collection = collection
        self.frequency_chunk = frequency_chunk
        self.construct_table()
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        
        # self.graphic1()
        # self.graphic2()
        
        # defind botton

        self.previous_botton = Button(root,text="Previous",padx=20,pady=5,command=self.myCLick_previous)
        self.previous_botton.pack()
        self.previous_botton.place(x=1200, y=50)

        self.next_botton = Button(root,text="Next",padx=30,pady=5,command=self.myCLick_next)
        self.next_botton.pack()
        self.next_botton.place(x=1200, y=90)
        
    def initialisation_table(self):
        for record in self.tree.get_children():
            self.tree.delete(record)
        self.tree.pack(pady=20)
        
    def pymongo_module_call_data_init(self):
        
        
        # Define the range values
        lower_index = self.start
        upper_index = self.stop

        
        # Construct the aggregation pipeline
        pipeline = [
        {
        '$match':{"pitched": True}  # match documents 
        },
        {
        '$skip': lower_index  # Skip documents up to the lower index
        },
        {
        '$limit': upper_index - lower_index  # Limit the number of documents to select based on the index range
        }
        ]
                
        results = self.collection.aggregate(pipeline)
    
        count = self.start
        for x in results:
            self.tree.insert(parent = '', index='end', iid=count, text =str(count),values=tuple((str(x['_id']),x['type'], x['instrument'], x['option'],x['Note_first_harmonique'], x['Note_max_harmonique'],x['fichier_octave'])))
            count += 1

        self.tree.pack(pady=20)
        return count
    
    
    def pymongo_module_call_data(self):
        
        
        # Define the range values
        lower_index = self.start
        upper_index = self.stop

        
        # Construct the aggregation pipeline
        pipeline = [
        {
        '$match':{"pitched": True}  # match documents 
        },
        {
        '$skip': lower_index  # Skip documents up to the lower index
        },
        {
        '$limit': upper_index - lower_index  # Limit the number of documents to select based on the index range
        }
        ]
                
        results = self.collection.aggregate(pipeline)
        
        
        self.initialisation_table()
        count = self.start
        for x in results:
            print('i am here')
            self.tree.insert(parent = '', index='end', iid=count, text =str(count),values=tuple((str(x['_id']),x['type'], x['instrument'], x['option'],x['Note_first_harmonique'], x['Note_max_harmonique'],x['fichier_octave'])))
            count += 1

        self.tree.pack(pady=20)
        return count
        
    def init_graphic_signal(self):
        
        
        # Construct the aggregation pipeline
        pipeline = [
        {
        '$limit': 1  # Limit the number of documents to select based on the index range
        }
        ]
                
        results = self.collection.aggregate(pipeline)
        
        fig1 = plt.figure(figsize=(5, 4.2))
        for x in results:
            continue
        plt.plot(np.arange(0,len(np.asarray(x['signal']))*delta_t,delta_t),np.asarray(x['signal']/max(np.asarray(x['signal']))))
        
        plt.title("Signal",fontsize=10)
        plt.xlabel('Temps (s)',fontsize=10)
        plt.ylabel('Amplitude normalisé',fontsize=10)
        plt.tick_params(labelsize=10)
        plt.close()
        canvas = FigureCanvasTkAgg(fig1, master = self.root)
        canvas.get_tk_widget().place(x=145,y=280)
        canvas.draw()
        
    def graphic_signal(self,id_graph):
        
        # print(id_graph)
        #Construct the aggregation pipeline
        
        results = self.collection.find_one({'_id': ObjectId(id_graph)})
        
        fig3 = plt.figure(figsize=(5, 4.2))
    
        plt.plot(np.arange(0,len(np.asarray(results['signal']))*delta_t,delta_t),np.asarray(results['signal']/max(np.asarray(results['signal']))))
        plt.title("Signal",fontsize=10)
        plt.xlabel('Temps (s)',fontsize=10)
        plt.ylabel('Amplitude normalisé',fontsize=10)
        plt.tick_params(labelsize=10)
        
        plt.close()
        
        canvas = FigureCanvasTkAgg(fig3, master = self.root)
        canvas.get_tk_widget().place(x=145,y=280)
        canvas.draw()
        
        

    def init_graphic_spectre(self):
            
        #Construct the aggregation pipeline
        pipeline = [
        {
        '$limit': 1  # Limit the number of documents to select based on the index range
        }
        ]
                
        results = self.collection.aggregate(pipeline)
        
        
        fig2 = plt.figure(figsize=(5, 4.2))
        for x in results: 
            continue
        
        plt.plot(self.frequency_chunk,np.asarray(x['spectre']))
        plt.title("spectre",fontsize=10)
        plt.xlabel('Frequence (Hz)',fontsize=10)
        plt.ylabel('Amplitude normalisé',fontsize=10)
        plt.xscale('log')
        plt.tick_params(labelsize=10)
        plt.close()

        canvas2 = FigureCanvasTkAgg(fig2, master = self.root)
        canvas2.get_tk_widget().place(x=750,y=280)
        canvas2.draw()
        
    def graphic_spectre(self,id_graph):
        
        # print(id_graph)
        #Construct the aggregation pipeline
        
        results = self.collection.find_one({'_id': ObjectId(id_graph)})
        
        
        fig4 = plt.figure(figsize=(5, 4.2))
        spectrum_plot = np.asarray(results['spectre'])
        plt.plot(self.frequency_chunk,spectrum_plot)
        plt.title("spectre",fontsize=10)
        plt.xlabel('Frequence (Hz)',fontsize=10)
        plt.ylabel('Amplitude normalisé',fontsize=10)
        plt.xscale('log')
        plt.tick_params(labelsize=10)
        plt.close()
        canvas2 = FigureCanvasTkAgg(fig4, master = self.root)
        canvas2.get_tk_widget().place(x=750,y=280)
        canvas2.draw()
        
        
        
    def myCLick_previous(self):
        print('previous')
        
        self.start = self.start - 10 
        self.stop = self.stop - 10
        print(self.start)
        print(self.stop)
        
        if self.start >= 0 and self.stop >=0 :
            
            self.pymongo_module_call_data()
            
        else:
            self.start = self.start + 10 
            self.stop = self.stop + 10
        plt.close()
            
    def myCLick_next(self):  
        print('next')
        
        self.start = self.start + 10 
        self.stop = self.stop + 10
        print(self.start)
        print(self.stop)
        if self.start >= 0 and self.stop >=0 :
            
            self.pymongo_module_call_data()
        
        else:
            self.start = self.start - 10 
            self.stop = self.stop - 10
            
        
                        
    def construct_table(self):
        
        self.tree["columns"]=('Object ID','Database','Instrument',"Option",'1ere harmonique','Harmonique Max','fichier_octave')
        self.tree.column("#0",width=40,minwidth=25)
        self.tree.column("Object ID",width=180,minwidth=25)
        self.tree.column("Database",width=100,minwidth=25)
        self.tree.column("Instrument",width=100,minwidth=25)
        self.tree.column("Option",width=100,minwidth=25)
        self.tree.column("1ere harmonique",width=70,minwidth=25)
        self.tree.column("Harmonique Max",width=70,minwidth=25)
        self.tree.column("fichier_octave",width=250,minwidth=25)


        self.tree.heading("#0",text='Label')
        self.tree.heading("Object ID",text='Object ID')
        self.tree.heading("Database",text='Database')
        self.tree.heading("Instrument",text='Instrument')
        self.tree.heading("Option",text='Option')
        self.tree.heading("1ere harmonique",text='1ere harmonique')
        self.tree.heading("Harmonique Max",text='Harmonique Max')
        self.tree.heading("fichier_octave",text='Source')
        
        
        self.pymongo_module_call_data_init()
        # count = 0 
        # for record in self.list_items[self.start:self.stop]:
        #     print(record)
        #     self.tree.insert(parent = '', index='end', iid=count, text =str(count),values=tuple(record))
        #     count += 1

        self.tree.pack(pady=20)

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        print("note first harmonic is : ", self.tree.item(item)["values"])
        
        id_graph = self.tree.item(item)["values"][0]
        
        plt.close()
        self.graphic_spectre(id_graph)
        plt.close()
        self.graphic_signal(id_graph)
        plt.close()



start = 0
stop = 10

Object_initialisation = Application(root,start,stop,collection,frequency_chunk)

Object_initialisation.init_graphic_signal()
Object_initialisation.init_graphic_spectre()

root.mainloop()
   
