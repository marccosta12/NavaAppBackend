# Backend Nava APP
Con el modelo de Django

# Conexión Base de datos
1. .env debe ser igual al de nava-dev-db
Base del fichero:
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=

2. Comprobar conexión
python manage.py runserver

3. Arrancar servidor
python manage.py runserver

Servidor: http://127.0.0.1:8000/


# GIT
0. Status
Git status

1. Add
Git add . 
Git add ./[name of file]

2. Commit
Git commit -m "message"

3. Push
Git push origin main [or branch]

4. Tag
git tag -a v0.1.0 -m "Message"
git push origin v0.1.0
git push --tags (push all tags)

5. Branch
git checkout -b <branch_name> (Create)
git checkout <branch_name> (Switch)

6. Restore
git reset --hard (Restore last commit)
git restore <file_path>

7. Pull
git pull origin main



