# JCEM TOGO

## Configuration PostgreSQL

1. Copiez `.env.example` en `.env`
2. Remplissez `POSTGRES_PASSWORD` avec votre mot de passe local
3. Assurez-vous que PostgreSQL écoute sur `localhost:5432`

## Commandes utiles

- `python -m pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

## Notes Git

- Ne commitez jamais `.env`
- `.env.example` contient la structure de configuration sans secret

## Docker

Lance le site (Django + PostgreSQL) sans rien installer localement :

1. Copiez `.env.example` en `.env` (les valeurs par défaut suffisent pour un usage local)
2. `docker compose up --build`
3. Le site est accessible sur http://localhost:8000, le back-office sur http://localhost:8000/back-office/

La base de données PostgreSQL est persistée dans un volume Docker (`postgres_data`) et les migrations sont appliquées automatiquement au démarrage du conteneur `web`.

Pour tout arrêter : `docker compose down` (ajoutez `-v` pour supprimer aussi les données de la base).
