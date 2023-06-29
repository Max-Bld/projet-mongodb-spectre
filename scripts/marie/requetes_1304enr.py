import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
from reordonner_notes import reordonner_notes
from sort_listes import sort_listes


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
#coll_name = "Full_data_with_harmonics_amp_and_pos"
coll_name = "Full_data_with_harmonics_amp_and_pos_note_with_post_traitement"
collection = db[coll_name]




################################################
################### Requêtes ###################
################################################

# Requêtes : description de la base
# Type d'instrument
liste_type_inst = []
pipeline = [{'$group':{'_id':"$type",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par type d\'instrument ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_type_inst.append(res['_id'])

# Pitched
liste_pitched = []
pipeline = [{'$group':{'_id':"$pitched",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par pitched true ou pitched false ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_pitched.append(res['_id'])

# Instrument
liste_instrument = []
valeur=[]
pipeline = [{'$group':{'_id':"$instrument",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par instrument ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_instrument.append(res['_id'])
    valeur.append(res['total_instrument'])
# Histogramme de la distribution
plt.figure(1)
sns.barplot(x=liste_instrument, y=valeur).set(title="Distribution des instruments")
plt.xticks(rotation=45, ha='right')
plt.show()

# Option
liste_option = []  
valeur=[]  
pipeline = [{'$group':{'_id':"$option",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par option ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_option.append(res['_id'])
    valeur.append(res['total_instrument'])
# Histogramme de la distribution
plt.figure(2)
sns.barplot(x=liste_option, y=valeur).set(title="Distribution des options")
plt.show()

# Dynamique
liste_dynamique = []  
valeur=[]  
pipeline = [{"$match":{"instrument":"altoflute", "option":"nooption"}},
            {'$group':{'_id':"$dynamique",'total_instrument':{'$count':{}}}}, 
            {'$sort':{'total_instrument':-1}}]        
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par dynamique ---')
for res in results:
    print(f"{res['_id']} : {res['total_instrument']}")
    liste_dynamique.append(res['_id'])
    valeur.append(res['total_instrument'])  
# Histogramme de la distribution
plt.figure(3)
sns.barplot(x=liste_dynamique, y=valeur).set(title="Distribution des dynamiques")  
plt.show()

# Note 1st harmonique  
liste_notes_harmo = []
valeur=[]
pipeline = [{"$group":{"_id":"$Note_first_harmonique", "total_note":{"$count":{}}}},
            {"$sort":{"_id":1}}]
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par note ---')
for res in results:
    print(f"{res['_id']} : {res['total_note']}")
    liste_notes_harmo.append(res['_id'])
    valeur.append(res['total_note'])
# Histogramme de la distribution
plt.figure(4)
sorted_liste_note, sorted_liste_valeur = reordonner_notes(liste_notes_harmo, valeur)
sns.barplot(x=sorted_liste_note, y=sorted_liste_valeur).set(title="Distribution des notes (1st harmonique)")
plt.xticks(rotation=45, ha='right')
plt.show()

# Note max harmonique
liste_notes_harmo = []
valeur=[]
pipeline = [{"$group":{"_id":"$Note_max_harmonique", "total_note":{"$count":{}}}},
            {"$sort":{"_id":1}}]
results = collection.aggregate(pipeline)
print('\n--- Nombre total de documents par note ---')
for res in results:
    print(f"{res['_id']} : {res['total_note']}")
    liste_notes_harmo.append(res['_id'])
    valeur.append(res['total_note'])
# Histogramme de la distribution
plt.figure(5)
sorted_liste_note, sorted_liste_valeur = reordonner_notes(liste_notes_harmo, valeur)
sns.barplot(x=sorted_liste_note, y=sorted_liste_valeur).set(title="Distribution des notes (max harmonique)")
plt.xticks(rotation=45, ha='right')
plt.show()

# Les différentes modalités
print('\n\n+++ Récap des modalités +++')
print(f"type instrument : {liste_type_inst}")
print(f"pitched : {liste_pitched}")
print(f"instrument : {liste_instrument}")
print(f"option : {liste_option}")
print(f"dynamique : {liste_dynamique}")
print(f"harmonique premiere : {liste_notes_harmo}")




################################################
##################### Plot #####################
################################################

# Nombre de valeurs qui sont égale à 0 ou nooption 
# Répartition des instruments lorsque Note_max_harmonique = '0' : pas de match trouvé sur la note
pipeline = [{"$match":{"Note_max_harmonique":"0"}},
            {"$group":{"_id":{
                            "note_max_harmonique": "$Note_max_harmonique",
                            "instrument" : "$instrument"
                            }, "total":{"$count":{}}}},
            {"$sort":{"_id":1}}]
results = collection.aggregate(pipeline)
print("Nombre d'enregistrements pour lesquels nous n\'avons pas trouvé de note_max_harmonique : ")
instr = []
tot = []
for res in results:
    print(f"{res['_id']['instrument']} : {res['total']}")
    instr.append(res['_id']['instrument'])
    tot.append(res['total'])
plt.figure(6)
sns.barplot(x=instr, y=tot).set(title="Note max harmonique inconnue (='0')")
plt.show()

# Répartition des instruments lorsque Note_first_harmonique = '0' : pas de match trouvé sur la note
pipeline = [{"$match":{"Note_first_harmonique":"0"}},
            {"$group":{"_id":{
                            "Note_first_harmonique": "$Note_first_harmonique",
                            "instrument" : "$instrument"
                            }, "total":{"$count":{}}}},
            {"$sort":{"_id":1}}]
results = collection.aggregate(pipeline)
print("Nombre d'enregistrements pour lesquels nous n\'avons pas trouvé de note_first_harmonique : ")
instr = []
tot = []
for res in results:
    print(f"{res['_id']['instrument']} : {res['total']}")    
    instr.append(res['_id']['instrument'])
    tot.append(res['total'])
plt.figure(7)
sns.barplot(x=instr, y=tot).set(title="Note first harmonique inconnue (='0')")
plt.show()

# Répartition des instruments lorsque option = 'nooption'
pipeline = [{"$match":{"option":"nooption"}},
            {"$group":{"_id":{
                            "option": "$nooption",
                            "instrument" : "$instrument"
                            }, "total":{"$count":{}}}},
            {"$sort":{"_id":1}}]
results = collection.aggregate(pipeline)
print("Nombre d'enregistrements pour lesquels nous n\'avons pas trouvé d\'option : ")
instr = []
tot = []
for res in results:
    print(f"{res['_id']['instrument']} : {res['total']}")    
    instr.append(res['_id']['instrument'])
    tot.append(res['total'])
plt.figure(8)
sns.barplot(x=instr, y=tot).set(title="Option inconnue (='nooption')")
plt.show()

# Distribution selon type-instrument-option-dynamique - choix 1 
ok = []  
valeur = []  
pipeline = [
    { "$group": {
        "_id": {
            "type": "$type",
            "instrument": "$instrument",
            "option": "$option",
            "dynamique": "$dynamique"
        },
        "total": { "$count": {} }
    }}
]
results = collection.aggregate(pipeline)
for res in results:
    print(f"{res['_id']} : {res['total']}")
    ok.append(str(res['_id']).replace('{', '').replace('}', '').replace('\'type\': ', '').replace(' \'instrument\':', '').replace(' \'option\':', '').replace(' \'dynamique\':', '').replace('\'', ''))
    valeur.append(res['total'])    
plt.figure(9)
sns.barplot(y=ok, x=valeur).set(title="Distribution selon les modalités d'instruments")
plt.show()

# Distribution selon type-instrument-option-dynamique - choix 2 -> on enlève theremin
ok = []  
valeur = []  
pipeline = [
    { "$group": {
        "_id": {
            "instrument": "$instrument",
            "option": "$option",
            "dynamique": "$dynamique"
        },
        "total": { "$count": {} }
    }}
]
results = collection.aggregate(pipeline)
for res in results:
    print(f"{res['_id']} : {res['total']}")
    ok.append(str(res['_id']).replace('{', '').replace('}', '').replace('\'instrument\':', '').replace(' \'option\':', '').replace(' \'dynamique\':', '').replace('\'', ''))
    valeur.append(res['total'])    
plt.figure(10)
ok_sorted, valeur_sorted = sort_listes(ok, valeur)
sns.barplot(y=ok_sorted, x=valeur_sorted).set(title="Distribution selon les modalités d'instruments")
plt.show()

# Distribution du spectre musical
x = []
y = []
valeur = []
pipeline = [
    { "$group": {
        "_id": {
            "Note_first_harmonique": "$Note_first_harmonique",
            "instrument": "$instrument"
        },
        "total": { "$count": {} }
    }
}, {'$sort':{'Note_first_harmonique':-1}}]
results = collection.aggregate(pipeline)
for res in results:
    print(f"{res['_id']} : {res['total']}")
    x.append(res['_id']['instrument'])
    y.append(res['_id']['Note_first_harmonique'])
    valeur.append(res['total'])   

data = pd.DataFrame({'Instrument': x, 'Note': y, 'valeur': valeur})
pivot_data = data.pivot(index='Note', columns='Instrument', values='valeur')
pivot_data = pivot_data.fillna(0)
plt.figure(11)
sns.heatmap(pivot_data, annot=True, cbar=True, cmap='plasma', annot_kws={"fontsize": 8})
plt.yticks(rotation=0)
plt.tick_params(axis='y', labelsize=8)
plt.title("Distribution du spectre musical")
plt.show()

# Distribution du spectre musical pour la 3ème octave puis 3/4/5/6
for j in range(4):
    x = []
    y = []
    valeur = []
    pipeline = [
        {"$match": {"Note_first_harmonique":{"$regex":str(j+3)}}},
        { "$group": {
            "_id": {
                "Note_first_harmonique": "$Note_first_harmonique",
                "instrument": "$instrument"
            },
            "total": { "$count": {} }
        }
    }, {'$sort':{'Note_first_harmonique':-1}}]
    results = collection.aggregate(pipeline)
    for res in results:
        print(f"{res['_id']} : {res['total']}")
        x.append(res['_id']['instrument'])
        y.append(res['_id']['Note_first_harmonique'])
        valeur.append(res['total'])   
    
    data = pd.DataFrame({'Instrument': x, 'Note': y, 'valeur': valeur})
    pivot_data = data.pivot(index='Note', columns='Instrument', values='valeur')
    pivot_data = pivot_data.fillna(0)
    index_values = pivot_data.index.tolist()
    new_index_order = index_values[::-1]
    pivot_table_reindexed = pivot_data.reindex(index=new_index_order)
    plt.figure(12+j)
    sns.heatmap(pivot_table_reindexed, annot=True, cbar=True, cmap='plasma', annot_kws={"fontsize": 10})
    plt.yticks(rotation=0)
    plt.tick_params(axis='both', labelsize=15)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Distribution du spectre musical pour la {j+3}ème octave",fontsize=20)
    plt.show()

# Y a-t'il des doublons dans nos enregistrements? 
doublon = []
pipeline = [
    { "$group": {
        "_id": {
            "type": "$type,",
            "pitched": "$pitched",
            "option": "$option",
            "instrument": "$instrument",
            "dynamique": "$dynamique"
        },
        "total": { "$count": {} }
    }
}]
results = collection.aggregate(pipeline)
for res in results:
    print(f"{res['_id']} : {res['total']/12}") # on divise par 12 car chaque enregistrement est toujours représenté 12 fois (1 enregistrement par note)
    if res['total']/12 > 1 :
        doublon.append([[res['_id']['instrument'],res['_id']['dynamique'],res['_id']['option']], res['total']/12])

print(f"Voici tous les instruments - dynamique - option qui ont des doublons : \n{doublon}")

##### Stop
# Distribution selon condition harmo1 = harmo_max et harmo1 != harmo_max    ============> en cours 
ok = []  
valeur = [] 
pipeline = [
    {"$match":{"Note_max_harmonique":{"$eq":"C5"}}},
    {"$group":{
        "_id":{
            "Note_max_harmonique": "$Note_max_harmonique",
            "Note_first_harmonique": "$Note_first_harmonique"
        },
        "total": { "$count": {} }
    }}
]
results = collection.aggregate(pipeline)
for res in results:
    print(f"{res['_id']} : {res['total']}")
    ok.append(str(res['_id']).replace('{', '').replace('}', '').replace('\'Note_max_harmonique\': ', '').replace('\'Note_first_harmonique\': ', ''))
    valeur.append(res['total'])    

ar = []
liste_note = []
# Pour C5
ok = 38
pas_ok = 7+4
tot = ok + pas_ok
ok = ok/tot*100
pas_ok = pas_ok/tot*100

ar.append([ok, pas_ok])
liste_note.append('C5')
df = pd.DataFrame(ar, index = liste_note, columns = ['ok', 'pas_ok'])
df.plot(kind='bar', stacked=True, color=['steelblue', 'red'])


##à 2
ok = []  
valeur = [] 
pipeline = [
    {
        "$match": {"Note_max_harmonique": { "$ne": "$Note_first_harmonique" }, "Note_max_harmonique":{"$eq":"C5"}  }
    },
    {   "$group": {
            "_id": {
                "Note_max_harmonique": "$Note_max_harmonique",
                "Note_first_harmonique": "$Note_first_harmonique"
            },
            "total": { "$count": {} }
        }
    }
]
results = collection.aggregate(pipeline)
for res in results:
    print(f"{res['_id']} : {res['total']}")


