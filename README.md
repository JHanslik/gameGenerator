# Création du fichier README.md

cat > README.md << EOL

# GameForge - Générateur de jeux vidéo par IA

## Description

GameForge est une plateforme web permettant aux utilisateurs de créer des concepts de jeux vidéo originaux à l'aide de modèles d'intelligence artificielle. L'application génère automatiquement un univers de jeu cohérent, une histoire immersive, des personnages, des illustrations et une fiche de présentation complète.

## Fonctionnalités

- Formulaire de création guidée pour définir le type de jeu
- Génération assistée par IA pour le scénario, les personnages et l'univers
- Génération d'images conceptuelles
- Mode d'exploration libre pour inspiration
- Système d'authentification et de gestion des projets
- Partage public/privé des créations

## Installation

1. Cloner le dépôt

```bash
git clone <url-du-dépôt>
cd gameforge
```

2. Créer un environnement virtuel et l'activer

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Créer une base de données MySQL

```bash
mysql -u root -p
CREATE DATABASE gameforge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'gameforge_user'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON gameforge.* TO 'gameforge_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

5. Créer un fichier .env à la racine du projet

```
SECRET_KEY=votre_clé_secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
HUGGINGFACE_API_KEY=votre_clé_api_huggingface

# Database settings
DB_NAME=gameforge
DB_USER=gameforge_user
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=3306
```

6. Appliquer les migrations

```bash
python manage.py migrate
```

7. Créer un superutilisateur (facultatif)

```bash
python manage.py createsuperuser
```

8. Lancer le serveur de développement

```bash
python manage.py runserver
```

9. Accéder à l'application à l'adresse http://localhost:8000

## Technologies utilisées

- Django
- MySQL
- Tailwind CSS
- Hugging Face API
  EOL
