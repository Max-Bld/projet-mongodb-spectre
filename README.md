# Projet Spectre

## But du projet

Le Projet Spectre a pour but la conception d’un programme capable d’identifier le type d’instrument de musique enregistré dans un fichier audio, quelle que soit la note jouée. Il s'appuie sur un jeu de données d’environ quatre mille fichiers audios dont sont extraits les spectres harmoniques.

A l'avenir, ces données permettront de générer un modèle par apprentissage automatique supervisé, qui prédira quel instrument est joué.

## Dependencies

Les dépendances nécessaires pour le programme sont référencées dans **requirements.in**.

## About environment

The file named **.env-template** list the required environnement variables that your project need, but **does not** contains any citical informations such as credentials. It can contains **example values**. It's purpose is to show how to build the **.env** file.

The **.env** needs to be listed in the **.gitignore**, it's **not versionned**, it's **only in your system**.

---

## Configuration

List here the steps to follow to run the application.

- You need to have access to a MongoDB database
- Create a virtual environment
- Install the dependencies listed in requirements.in
- Create you .env file based on .env-template
- ...

## How to use

Describe here how to use, launch ... your application.

- Import the dataset using ...
- Run the application using ...

---

## Troubleshooting

You can list here, if needed, the common issues that the users of your app can encounter.
