# Accès à Mes Données

Ce projet permet de télécharger et d'organiser des données à partir de Neo4j en utilisant des scripts Python. Vous trouverez ci-dessous les étapes pour accéder et générer les données.

## Prérequis

1. **Téléchargez les fichiers nécessaires** :
   - `download_script.py` : Contient les fonctions pour récupérer et sauvegarder les données depuis Neo4j.
   - `run.py` : Le script principal qui exécute les fonctions de téléchargement.
   - `requirements.txt` : Liste des dépendances nécessaires pour faire fonctionner les scripts.

2. **Installation des dépendances** :
   Assurez-vous d'installer les dépendances répertoriées dans le fichier `requirements.txt`.

## Étapes d'installation

1. **Placez les fichiers `download_script.py` et `run.py` dans le même dossier.**

2. **Créer et activer un environnement virtuel** :
   Il est recommandé d'utiliser un environnement virtuel pour gérer les dépendances.
   
   Créez un environnement virtuel avec la commande suivante :

   ```bash
   python -m venv env
   ```

   Activez l'environnement :

   - Sous **Windows** :
     ```bash
     .\env\Scripts\activate
     ```
   - Sous **macOS/Linux** :
     ```bash
     source env/bin/activate
     ```

3. **Installer les dépendances** :

   Installez les dépendances nécessaires depuis `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

## Exécution

Une fois l'environnement virtuel configuré et les dépendances installées, exécutez le script principal pour générer les données :

```bash
python run.py
```

Et Paafff, les données sont téléchargés et sauvegardes automatiquement !
