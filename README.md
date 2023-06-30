# Projet Spectre

## But du projet

*Projet Spectre* est un programme qui a pour but d’identifier le type d’instrument de musique enregistré dans un fichier audio, quelle que soit la note jouée. Il s'appuie sur un jeu de données d’environ trois mille fichiers audios dont sont extraits les spectres harmoniques.

Par exemple, admettons qu'une basse joue une note aigue pouvant facilement être confondue avec celle jouée par une guitare : grâce à l'analyse spectrale du fichier audio, le *Projet Spectre* sera capable de distinguer et d'identifier l'instrument joué.

## Dépendances

Les dépendances nécessaires pour le programme sont référencées dans **requirements.in**.

## About environment

The file named **.env-template** list the required environnement variables that your project need, but **does not** contains any citical informations such as credentials. It can contains **example values**. It's purpose is to show how to build the **.env** file.

The **.env** needs to be listed in the **.gitignore**, it's **not versionned**, it's **only in your system**.

---

## Utilisation

### Fonctionnalités

*Projet Spectre GUI* est une interface graphique qui permet à l'utilisateur de sélectionner un fichier audio parmi une base de données et d'afficher, à gauche, le signal et, à droite, le spectre.

### Mise en place

1. Exécuter cette commande dans votre terminal au chemin désiré pour télécharger à la fois les programmes et la base de données :

        git clone https://www.github.com/Max-Bld/projet-mongodb-spectre.git

2. Lancer le fichier setup.py pour installer les dépendances nécessaires à *Projet Spectre* :

        python setup.py

3. Lancer le fichier main.py pour accéder à l'application graphique.

        python main.py

## Troubleshooting

You can list here, if needed, the common issues that the users of your app can encounter.
