# Projet Spectre GUI

## Introduction

### But du projet

*Projet Spectre* a pour but de concevoir un programme capable d’identifier le type d’instrument de musique enregistré dans un fichier audio, quelle que soit la note jouée. Il s'appuie sur une base de données constituée d’environ trois mille fichiers audios dont sont extraits les spectres harmoniques.

### Projet Spectre GUI

A l'heure actuelle, nous proposons *Projet Spectre GUI*. C'est une interface graphique qui permet à l'utilisateur de sélectionner un fichier audio parmi la base de données et d'afficher le signal et le spectre.

*Projet Spectre GUI* est écrit en _Python_ et l'architecture de sa base de données NoSQL est en _MongoDB_. Les graphiques sont affichés à l'aide de la bibliothèque _matplotlib_ et l'interface graphique est générée par le module _Tkinter_.

## Configuration

### Dépendances

Les dépendances nécessaires pour le programme sont référencées dans **requirements.in**.

### Installation et exécution

1. Après vous être placé dans le chemin désiré, exécutez cette commande dans votre terminal pour télécharger sur votre ordinateur à la fois les programmes et la base de données :

        git clone https://www.github.com/Max-Bld/projet-mongodb-spectre.git

2. Exécutez ces commandes dans votre terminal pour installer les dépendances nécessaires à *Projet Spectre GUI* :

        python setup.py
        python Application.py        

4. Lancez le fichier main.py pour accéder à l'application graphique.

        python main.py

### Base de données

Nous proposons une base de données réduite pour tester *Projet Spectre GUI* qui permet : 
+ d'augmenter la vitesse des requêtes MongoDB dans l'application ;
+ éviter le long téléchargement des fichiers via internet (*web scraping*).

Son chemin d'accès est : _./projet-mongodb-spectre/assets/theremin/zip/_.

Si vous voulez cependant tester le web-scraping et obtenir la base de données entière (environ 20GB), un fichier **web_scraping.py** est disponible pour la télécharger depuis https://theremin.music.uiowa.edu/ .

La base de données (de test ou "scrapée") est sous format .zip et est dézippée automatiquement par le programme dans le dossier *./projet-mongodb-spectre/assets/theremin/pitched/*.

### Requêtes MongoDB

Le fichier **requetes.py** regroupe les requêtes les plus pertinentes. Il doit être exécuté après **main.py**. Ne l'exécutez pas en entier, mais exécutez chaque requête séparément pour obtenir un résultat clair.

