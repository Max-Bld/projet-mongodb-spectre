# Projet Spectre

## Introduction

### But du projet

*Projet Spectre* est un programme qui a pour but d’identifier le type d’instrument de musique enregistré dans un fichier audio, quelle que soit la note jouée. Il s'appuie sur un jeu de données d’environ trois mille fichiers audios dont sont extraits les spectres harmoniques.

### Projet Spectre GUI

Pour l'instant, nous proposons *Projet Spectre GUI* est une interface graphique qui permet à l'utilisateur de sélectionner un fichier audio parmi une base de données et d'afficher, à gauche, le signal et, à droite, le spectre.

## Configuration

### Mise en place

1. Exécuter cette commande dans votre terminal au chemin désiré pour télécharger à la fois les programmes et la base de données :

        git clone https://www.github.com/Max-Bld/projet-mongodb-spectre.git

2. Lancer le fichier setup.py pour installer les dépendances nécessaires à *Projet Spectre* :

        python setup.py

3. Lancer le fichier main.py pour accéder à l'application graphique.

        python main.py

### Dépendances

Les dépendances nécessaires pour le programme sont référencées dans **requirements.in**.
