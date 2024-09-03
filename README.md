# Watchtrack
![Photo de Profile](https://github.com/Cori-bot/Watchtrack/blob/main/WatchTrack.png "Watchtrack")

Il s'agit d'un bot Discord permettant de gérer une liste de films, de séries, de mangas et d'animes. Vous pouvez ajouter, modifier et filtrer les médias en utilisant diverses commandes.

## Discord

***Pour tester le bot avant de le telecharger, vous pouvez rejoindre le serveur discord de test → [ici](https://discord.gg/E3X3WBZE2w)***

## Fonctionnalités

- Ajouter des médias à votre liste
- Modifier ou supprimer des éléments multimédias
- Afficher la liste complète des éléments multimédias
- Filtrer les médias par type et par état

## Commandes du robot
Voici les commandes que vous pouvez utiliser avec le robot :

- /add : Ajoute un film, une série, un manga ou un anime à votre liste.
    - Paramètres : type, nom, statut, saison (optionnel), épisode (optionnel), volume (optionnel), chapitre (optionnel).

- /modify : Modifie ou supprime un film, une série, un manga ou un anime de votre liste.
    - Paramètres : type, nom, action, statut (optionnel), saison (optionnel), épisode (optionnel), volume (optionnel), chapitre (optionnel).

- /list : Affiche la liste complète de vos films, séries, mangas et animes.
    - Paramètres : order (optionnel) : « A ➜ Z » ou “Z ➜ A”.

- /filter : Permet d'afficher les médias par type et par statut.
    - Paramètres : type, statut (facultatif), ordre.

- /explanations : Affiche un message d'explication avec toutes les commandes disponibles et leurs descriptions.

## Prérequis

- Python 3.8 ou supérieur
- Un jeton de bot Discord

## Installation

### 1. Installer Python

#### Windows

1. Téléchargez Python à partir du [site officiel de Python] (https://www.python.org/downloads/).
2. Exécutez le programme d'installation et assurez-vous de cocher la case « Add Python to PATH ».
3. Suivez les instructions pour terminer l'installation.

#### Linux

Sur les systèmes basés sur Ubuntu/Debian :

```bash
sudo apt update
sudo apt install python3 python3-pip
```
Sur les systèmes basés sur Fedora/RHEL :

```bash
sudo dnf install python3 python3-pip
```

### 2. Cloner le dépôt

Clonez ce dépôt sur votre machine locale en utilisant Git :

```bash
git clone https://github.com/yourusername/your-repository.git
cd votre-dépôt
```

### 3. Configurer un environnement virtuel

#### Windows

1. Installez le paquetage virtualenv si vous ne l'avez pas déjà fait :
```bash
pip install virtualenv
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
```

3. Activez l'environnement virtuel :
```bash
.\N-venv\Scripts\Nactivate
```

#### Linux

1. Installez le paquet virtualenv si ce n'est pas déjà fait :
```bash
pip3 install virtualenv
```

2. Créez un environnement virtuel :
```bash
python3 -m venv venv
```

3. Activez l'environnement virtuel :
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

#### Une fois l'environnement virtuel activé, installez les paquets nécessaires :

```bash
pip install -r requirements.txt
```

### 5. Configurer le Bot

1. Créez un fichier nommé .env dans le répertoire racine du projet.
2. Ajoutez votre jeton de bot au fichier .env :
```env
TOKEN=votre-token-discord-bot
```
Remplacez votre-token-discord-bot par votre jeton de bot actuel depuis le portail des développeurs de Discord.

## Exécuter le bot

#### Avec l'environnement virtuel activé et les dépendances installées, vous pouvez lancer le bot en utilisant :
```bash
python bot.py
```