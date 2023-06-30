# Projet Spectre GUI

## Introduction

### But du projet

*Projet Spectre* a pour but de concevoir un programme capable d’identifier le type d’instrument de musique enregistré dans un fichier audio, quelle que soit la note jouée. Il s'appuie sur une base de données constituée d’environ trois mille fichiers audios dont sont extraits les spectres harmoniques.

### Projet Spectre GUI

A l'heure actuelle, nous proposons *Projet Spectre GUI* : c'est une interface graphique qui permet à l'utilisateur de sélectionner un fichier audio parmi la base de données et d'afficher le signal et le spectre.

*Projet Spectre GUI* est écrit en _Python_ et l'architecture de sa base de données NoSQL est en _MongoDB_. Les graphiques sont affichés à l'aide de la bibliothèque _matplotlib_ et l'interface graphique est générée par le module _Tkinter_.

## Configuration

### Installation

1. Après vous être placé dans le chemin désiré, exécutez cette commande dans votre terminal pour télécharger sur votre ordinateur à la fois les programmes et la base de données :

        git clone https://www.github.com/Max-Bld/projet-mongodb-spectre.git

2. Exécutez ces fichiers dans votre IDE Python pour installer les dépendances nécessaires à *Projet Spectre GUI* :

        setup.py
        Application.py        

3. Lancez le fichier _main.py_ pour accéder à l'application graphique.

        main.py

### Utilisation

1. Une fois que le fichier _main.py_ est lancé, après que le processus de traitement des données est terminée, une fenêtre _Tkinter_ s'ouvrira dans votre barre Windows en arrière-plan :

   ![barre windows](https://i.ibb.co/BcH064y/barre-windows.png)

   Affichez-la et utilisez-les fonctionnalités de *Projet Spectre GUI*.

2. Voici les différentes fonctionnalités de *Projet Spectre GUI* :
   
   ![fonctionnalites](https://i.ibb.co/Wxd6K82/fonctionnalites.png)


   + Sélectionner un fichier audio parmi la base de données en double cliquant dessus.
   + Accéder aux différentes caractéristiques du fichier audio :     
     - ID : un identifiant unique ;
     - Database : indique le nom de la banque de sons (ex : Theremin) ;
     - Instrument : indique le nom de l'instrument (ex : altoflute) ;
     - Option : précise si l'instrument a été joué avec un certain effet (ex : vib signifie que l'instrument a été joué avec un effet de vibrato) ;
     - 1ere H : indique la note de la première harmonique qui apparait dans le spectre ;
     - H Max : indique la note de l'harmonique la plus forte dans le spectre ;
     - Source : indique le nom du fichier source ;
   + Afficher le signal dans le temps du fichier audio, et son spectre selon la fréquence en abscisse et de l'amplitude à l'axe des ordonnées ;
   + Vous déplacer dans la base de données page par page à l'aide des boutons _Previous_ et _Next_.
   

### Dépendances

Les dépendances nécessaires pour le programme sont référencées dans **requirements.in**.

### Base de données

Nous proposons une base de données réduite pour tester *Projet Spectre GUI* qui permet : 
+ d'augmenter la vitesse des requêtes MongoDB dans l'application ;
+ éviter le long téléchargement des fichiers via internet (*web scraping*).

Son chemin d'accès est : _./projet-mongodb-spectre/assets/theremin/zip/_.

Si vous voulez cependant tester le web-scraping et obtenir la base de données entière (environ 20GB), un fichier **web_scraping.py** est disponible pour la télécharger depuis https://theremin.music.uiowa.edu/ .

La base de données (de test ou "scrapée") est sous format .zip et est dézippée automatiquement par le programme dans le dossier *./projet-mongodb-spectre/assets/theremin/pitched/*.

### Requêtes MongoDB

Le fichier **requetes.py** regroupe les requêtes les plus pertinentes. Il doit être exécuté après **main.py**. Ne l'exécutez pas en entier, mais exécutez chaque requête séparément pour obtenir un résultat clair.

