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
