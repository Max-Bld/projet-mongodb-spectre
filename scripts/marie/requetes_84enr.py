import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import matplotlib.colors as mcolors
import pandas as pd




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
coll_name = "Full_data_with_harmonics_amp_and_pos"
collection = db[coll_name]




################################################
################### Requêtes ###################
################################################

# Requêtes : description de la base
liste_type_inst = []
pipeline = [{'$group':{'_id':"$type",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par type d\'instrument ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_type_inst.append(res['_id'])

liste_pitched = []
pipeline = [{'$group':{'_id':"$pitched",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par pitched true ou pitched false ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_pitched.append(res['_id'])

liste_instrument = []
pipeline = [{'$group':{'_id':"$instrument",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par instrument ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_instrument.append(res['_id'])

liste_option = []    
pipeline = [{'$group':{'_id':"$option",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par option ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_option.append(res['_id'])

liste_note = []    
pipeline = [{'$group':{'_id':"$note",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par note ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_note.append(res['_id'])

liste_dynamique = []    
pipeline = [{'$group':{'_id':"$dynamique",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par dynamique ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_dynamique.append(res['_id'])

# Les différentes modalités
print('\n\n+++ Récap des modalités +++')
print(f"type instrument : {liste_type_inst}")
print(f"pitched : {liste_pitched}")
print(f"instrument : {liste_instrument}")
print(f"option : {liste_option}")
print(f"note : {liste_note}")
print(f"dynamique : {liste_dynamique}")

# CRUD - Modification de l'option : 'novib' en 'nonvib'
# filter_query = {"option":"novib"} 
# update_query = {"$set":{"option":"nonvib"}} 
# collection.update_many(filter_query, update_query)
# Vérification de l'update
liste_option = []    
pipeline = [{'$group':{'_id':"$option",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par option ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_option.append(res['_id'])
    
# Vue 
# pipeline = [{"$match": {"instrument": "trumpet"}}]
# view = db.command("create", "vue_instrument_trumpet", viewOn="collection", pipeline = pipeline)




################################################
##################### Plot #####################
################################################

# Déclaration de l'axe des fréquence pour représenter les spectres
fs = 44.1E3
Nfft = 2**18
df = fs/Nfft
frequency = np.arange(0,Nfft*df,df)
index_frequency_chunk = np.where((frequency>50)&(frequency<15000))
frequency_chunk = frequency[index_frequency_chunk]

# Déclaration de l'axe du temps pour représenter les signaux
delta_t = 1/fs

# Les couleurs
couleur = mcolors.TABLEAU_COLORS # 10 couleurs
#couleur = mcolors.CSS4_COLORS # pour plus de couleurs...
couleur = couleur.keys()
couleur = list(couleur)
couleur.extend(['tab:black', 'tab:maroon','tab:khaki'])
couleur = ['dimgray',
 'salmon',
 'darkorange',
 'gold', 'darkgreen', 'turquoise', 
 'blueviolet',
 'coral',
 'gold',
 'gray',
 'palegreen',
 'cyan',
 'dodgerblue',
 'maroon',
 'khaki']

# Plot du spectre de tous les type d'instruments sur une note C4
plt.figure(1)
for i in range(len(liste_type_inst)):
    query = {"note":"C4", "type":liste_type_inst[i]} 
    results = collection.find(query)
    for x in results:
        plt.plot(frequency_chunk,np.asarray(x['spectre']), couleur[i], label=liste_type_inst[i])
        plt.title("Spectre de la note C4",fontsize=20)
        plt.legend(fontsize=10, bbox_to_anchor=(1.05, 1))
        plt.xscale("log")
        plt.xlabel('Frequence (Hz)',fontsize=15)
        plt.ylabel('Amplitude normalisé',fontsize=15)
        plt.tick_params(labelsize=15)
        plt.show()      
#plt.savefig("C:/Users/formation/Desktop/Plot_projet_spectre/Spectre_C4.png", dpi=300, bbox_inches='tight')

# Plot de tous les signaux par type d'instrument sur une note C4
fig, axs = plt.subplots(len(liste_type_inst), num = 'signal')
option=[]
for index in range(len(liste_type_inst)):
    query = {"note":"C4", "type":liste_type_inst[index]} 
    results = collection.find(query)
    for x in results:
        option.append(x['option'])
        if len(np.asarray(x['signal'])) % 2 == 0:
            axs[index].plot(np.arange(0,len(np.asarray(x['signal']))*delta_t - delta_t,delta_t),np.asarray(x['signal'])/max(np.asarray(x['signal'])), couleur[index], label=f"{liste_type_inst[index]}, {option[index]}")
            axs[index].legend(loc='upper right',fontsize=8)
        if len(np.asarray(x['signal'])) % 2 != 0:
            axs[index].plot(np.arange(0,len(np.asarray(x['signal']))*delta_t,delta_t),np.asarray(x['signal'])/max(np.asarray(x['signal'])), couleur[index], label=f"{liste_type_inst[index]}, {option[index]}")
            axs[index].legend(loc='upper right',fontsize=8)
fig.suptitle('Signal de la note C4',fontsize=15)
#plt.savefig("C:/Users/formation/Desktop/Plot_projet_spectre/Signaux_instrument.png", dpi=300, bbox_inches='tight')

# Analyse d'un signal
data = []
for i in range(len(liste_type_inst)):
    query = {"type":liste_type_inst[i], "note":"C4"} 
    results = collection.find(query)
    for x in results:
        row = {
            "Type": x["type"],
            "Longueur du signal": len(x["signal"]),
            "Moyenne du signal": np.mean(x["signal"]),
            "Minimum du signal": np.min(x["signal"]),
            "Médiane du signal": np.median(x["signal"]),
            "Maximum du signal": np.max(x["signal"]),
            "Quartile 25 du signal": np.percentile(x["signal"], q=25),
            "Quartile 75 du signal": np.percentile(x["signal"], q=75)
        }
        data.append(row)
caracteristiques_signaux = pd.DataFrame(data)

# Requête
pipeline = [{'$match': {"instrument":'theremin', "type":"trumpet", "pitched":True, "option":"novib", "dynamique":"mf"}},
            {'$group':{'_id':"$note",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par note ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")

# Plot du spectre de toutes les notes pour la trumpet
liste_note_CEG = ['C4', 'E4', 'G4']
N = len(liste_note_CEG)
plt.figure(3)
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.rainbow(np.linspace(0,1,N)))
for i in range(len(liste_note_CEG)):
    query = {"note":liste_note_CEG[i], "type":"trumpet"} 
    results = collection.find(query)
    for x in results:
        plt.plot(frequency_chunk,np.asarray(x['spectre']), label=liste_note_CEG[i])
        plt.title("Spectre des notes C4/E4/G4 pour la trompette",fontsize=20)
        plt.legend(fontsize=15)
        plt.xscale("log")
        plt.xlabel('Frequence (Hz)',fontsize=15)
        plt.ylabel('Amplitude normalisé',fontsize=15)
        plt.tick_params(labelsize=15)
        plt.show()
#plt.savefig("C:/Users/formation/Desktop/Plot_projet_spectre/Spectres_trompette.png", dpi=300, bbox_inches='tight')

# Les instruments ff sur une note, par exemple A4
pipeline = [{'$match': {"dynamique":"ff"}},
            {'$group':{'_id':"$type",'total':{'$count':{}}}}, 
            {'$sort':{'total':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre de documents pour chaque type d\'instrument ff ---')
liste_type_inst_ff = []
for res in results:
    print(f"{res['_id']} : {res['total']}")
    liste_type_inst_ff.append(res['_id'])

# Plot le spectre de tous les instruments ff sur la note A4
note = "A4"
N = len(liste_type_inst_ff)
plt.figure(4)
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.rainbow(np.linspace(0,1,N)))
for i in range(len(liste_type_inst_ff)):
    query = {"note":note, "type":liste_type_inst_ff[i]} 
    results = collection.find(query)
    for x in results:
        plt.plot(frequency_chunk,np.asarray(x['spectre']), label=liste_type_inst_ff[i])
        plt.title("Spectre de tous les instruments ff pour la note A4",fontsize=20)
        plt.legend(fontsize=10)
        plt.xscale("log")
        plt.xlabel('Frequence (Hz)',fontsize=15)
        plt.ylabel('Amplitude normalisé',fontsize=15)
        plt.tick_params(labelsize=15)
        plt.show()
#plt.savefig("C:/Users/formation/Desktop/Plot_projet_spectre/Spectres_instruments_ff_note_A4.png", dpi=300, bbox_inches='tight')

# Les instruments nonvib sur une note
pipeline = [{'$match': {"option":"nonvib"}},
            {'$group':{'_id':"$type",'total':{'$count':{}}}}, 
            {'$sort':{'total':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total nonvib ---')
liste_type_inst_nonvib = []
for res in results:
    print(f"{res['_id']} : {res['total']}")
    liste_type_inst_nonvib.append(res['_id'])

# Plot le spectre de tous les instruments nnovib sur la note A4
note = "A4"
N = len(liste_type_inst_nonvib)
plt.figure(5)
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.rainbow(np.linspace(0,1,N)))
for i in range(len(liste_type_inst_nonvib)):
    query = {"note":note, "type":liste_type_inst_nonvib[i]} 
    results = collection.find(query)
    for x in results:
        plt.plot(frequency_chunk,np.asarray(x['spectre']), label=liste_type_inst_nonvib[i])
        plt.title("Spectre de tous les instruments nonvib pour la note A4",fontsize=20)
        plt.legend(fontsize=10)
        plt.xscale("log")
        plt.xlabel('Frequence (Hz)',fontsize=15)
        plt.ylabel('Amplitude normalisé',fontsize=15)
        plt.tick_params(labelsize=15)
        plt.show()
#plt.savefig("C:/Users/formation/Desktop/Plot_projet_spectre/Spectres_instruments_nonvib_note_A4.png", dpi=300, bbox_inches='tight')




################################################
################## Harmonique ##################
################################################

# Vérification que toutes les valeurs de fréquences trouvées ci-dessous sont dans l'intervalle indiqué dans le fichier frequence_notes.csv
import pandas as pd
data = pd.read_csv("C:/Users/formation/Desktop/projet-mongo-maxime-marie-amine/assets/frequence_notes.csv")

# Trouver l'harmonique fondamentale (= la fréquence) de l'altoflute sur la note A4 
query1 = {"type":"altoflute", "note": "A4"} 
results1 = collection.find(query1)
for x in results1:
    print(x['harmonique_fondamental'][0])

# Vérifier que pour toutes les notes, la valeur de l'harmonique fondamentale (freq) est la même
# Méthode de calcul : on choisit une note ; pour chaque type d'instrument, on regarde l'harmonique amplitude et on sélectionne l'index de son max (index_max) ; la fréquence correspond à la valeur de harmonique fondamentale à cet index_max 
liste_type_inst
liste_note
freq = []
for i in range(len(liste_type_inst)):
    type_inst = liste_type_inst[i]
    note = liste_note[0]
    query1 = {"type":type_inst, "note":note} 
    results1 = collection.find(query1)
    
    for x in results1:
        print(f"\ninstrument : {type_inst}")
        print(f"note : {note}")
        print('--- harmonique amplitude ---')
        print(x['harmonique_amplitude'][0])
        print('--- harmonique fondamentale = frequence ---')
        print(x['harmonique_fondamental'][0])
        index_max = np.argmax(x['harmonique_amplitude'][0])
        valeur_fondamentale = x['harmonique_fondamental'][0][index_max]
        print(f"La fréquence : {valeur_fondamentale}")
    freq.append(valeur_fondamentale)
    
print(f'\n\n--> Voici toutes les valeurs de fréquence trouvées pour la note {liste_note[0]} : \n{freq}')


# Vérifier que pour toutes les notes, la valeur de l'harmonique fondamentale (freq) est la même
# Méthode de calcul : on choisit une note ; pour chaque type d'instrument, la fréquence correspond à la première valeur de l'array de harmonique fondmental
liste_type_inst
liste_note

dictio = {}
for j in range(len(liste_note)):
    freq = []
    for i in range(len(liste_type_inst)):
        type_inst = liste_type_inst[i]
        note = liste_note[j]
        query1 = {"type":type_inst, "note":note} 
        results1 = collection.find(query1)
        
        for x in results1:
            valeur_fondamentale = x['harmonique_fondamental'][0][0]
        freq.append(valeur_fondamentale)
    
    print(f'\n\n--> Voici toutes les valeurs de fréquence trouvées pour la note {liste_note[j]} : \n{freq}')
    print(f"La moyenne des fréquences pour la note {liste_note[j]} est : {round(np.mean(freq), 2)} (Hz)")
    print(f"L'écart type pour la note {liste_note[j]} est : {round(np.std(freq), 2)}")
    print(f"L'intervalle des fréquences pour la note {liste_note[j]} est : {data.loc[data['Note'].str.contains(liste_note[j]),:].iloc[0,4]}")
    np.where((380.995<np.asarray(freq))&(np.asarray(freq)<403.65))
    dictio[liste_note[j]] = round(np.mean(freq), 2)