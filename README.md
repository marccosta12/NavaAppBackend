# Backend Nava APP
Con el modelo de Django

# Conexión Base de datos
1. .env debe ser igual al de nava-dev-db
Base del fichero:
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_PORT=

2. Activar venv
.\venv\Scripts\Activate

3. Update BD
python manage.py makemigrations [App name] 

3. 1 Migrar BD
python manage.py migrate

4. Arrancar servidor
python manage.py runserver

Servidor: http://127.0.0.1:8000/

# Crear APP nueva
python manage.py startapp [nombre app]

1. Registrar las apps
settings.py -> INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'users',
    [nombre app],
]

2. Esqueletos de modelos
[nombre app]/models.py
Crear la estructura de la base de datos
Ejemplo:
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

3. Crear migración
python manage.py makemigrations
python manage.py migrate


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



