# Kakao-farmer_backend

# Application FastAPI - Authentification avec SQLite et Tortoise ORM

## Description
Cette application FastAPI permet l'authentification des utilisateurs avec un système d'inscription et de connexion sécurisé. Elle utilise **SQLite** comme base de données et **Tortoise ORM** pour la gestion des modèles.

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/MacDallas123/kakao-farmer-backend.git
```
### 2 - Environnement

Choisissez l'une des options suivantes, celle qui vous convient

#### OPTION 1 : Utilisation d'un environnement virtuel

##### a. Créer un environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Sur Mac/Linux
env\Scripts\activate    # Sur Windows
```

##### b. Installer les dépendances
```bash
cd Kakao-farmer_backend

pip install -r requirements.txt
```
#### OPTION 2 : Utilisation d'un environnement docker

##### a. Installer docker dans votre système

Suivre la documentation appropriée en fonction du système dans lequel vous vous trouvez

##### b. Construire l'image docker
```bash
cd Kakao-farmer_backend

docker build -t kakao-farmer-backend .
```

## Configuration de la base de données

L'application utilise **SQLite**. Aucun réglage supplémentaire n'est nécessaire, car la base de données sera automatiquement créée.

## Lancer l'application

### 1. Démarrer le serveur
Assurez-vous d’être à la racine du projet, puis exécutez :
```bash
uvicorn app.main:app --reload # Apres avoir demarrer l'environnement virtuel (OPTION 1)

docker run -p 8000:8000 kakao-farmer-backend # (OPTION 2)
```

L’API sera accessible à l’adresse suivante :
```
http://127.0.0.1:8000
```

## Points de terminaison API

### Créer un utilisateur
**POST** `users/register`
- **Corps de la requête (JSON)** :
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "motdepasse",
  "status": "user"
}
```

### Se connecter et obtenir un token
**POST** `users/login`
- **Corps de la requête (form-data)** :
```json
{
  "identifier": "johndoe", // username or email
  "password": "motdepasse",
}
```

### Accéder à une route protégée
**GET** `/protected`
- **Headers** :
```http
Authorization: Bearer <TOKEN>
```

## Structure du projet
```
app/
│── routes/
│   ├── notifications.py   # Routes notifications
│   ├── orders.py          # Routes commandes
│   ├── posts.py           # Routes postes
│   ├── products.py        # Routes produits'
│   ├── users.py           # Routes des utilisateurs
│── utils/
│   ├── security.py        # Fonctions de hashage et JWT
│── auth.py                # Paramètres d'authentification
│── config.py              # variables globales
│── main.py                # Point d’entrée de l'application
│── database.py            # Initialisation de la base de données
│── models.py              # Modèles Tortoise ORM
│── schemas.py             # Forme Données echangées
│── __init__.py            # Fichier d'initialisation
```
