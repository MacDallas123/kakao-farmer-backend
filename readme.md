# Application FastAPI - Authentification avec SQLite et Tortoise ORM

## Description
Cette application FastAPI permet l'authentification des utilisateurs avec un système d'inscription et de connexion sécurisé. Elle utilise **SQLite** comme base de données et **Tortoise ORM** pour la gestion des modèles.

## Installation

### 1. Cloner le projet
```bash
copier l'archive
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)
```bash
python -m venv env
source env/bin/activate  # Sur Mac/Linux
env\Scripts\activate    # Sur Windows
```

### 3. Installer les dépendances
```bash
pip install fastapi uvicorn tortoise-orm pydantic
```

## Configuration de la base de données
L'application utilise **SQLite**. Aucun réglage supplémentaire n'est nécessaire, car la base de données sera automatiquement créée.

## Lancer l'application

### 1. Démarrer le serveur
Assurez-vous d’être à la racine du projet, puis exécutez :
```bash
uvicorn app.main:app --reload
```

L’API sera accessible à l’adresse suivante :
```
http://127.0.0.1:8000
```

## Points de terminaison API

### Créer un utilisateur
**POST** `/register`
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
**POST** `/login`
- **Corps de la requête (form-data)** :
  - `username`: `johndoe`
  - `password`: `motdepasse`

### Accéder à une route protégée
**GET** `/protected`
- **Headers** :
```http
Authorization: Bearer <TOKEN>
```

## Structure du projet
```
app/
│── main.py           # Point d’entrée de l'application
│── database.py       # Initialisation de la base de données
│── models.py         # Modèles Tortoise ORM
│── routes/
│   ├── auth.py       # Routes d'authentification
│   ├── users.py      # Routes des utilisateurs
│── utils/
│   ├── security.py   # Fonctions de hashage et JWT
│── __init__.py       # Fichier d'initialisation
```