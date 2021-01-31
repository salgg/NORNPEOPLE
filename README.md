# NORNPEOPLE CHALLENGE #
## simple login-logout app ##
Descripción:
Nordpeople challenge usando PYTHON, CSS, validaciones Frontend, arquitectura MVC, POO, postgresql, intgridad y normalización de la base de datos y buenas prácticas

Requisitos:
* Tener instalado y configurado Python3 (más información en https://www.python.org/downloads/)
* Tener instalado y configurado Postgresql 9.5 o mayor (más información en https://www.postgresql.org/download/)

Instrucciones para instalación:
1. Instalar Psycopg usando "pip install psycopg2-binary psycopg2" (más información en https://www.psycopg.org/docs/install.html#quick-install)
2. Instalar Django usando "pip install django" (más información en  https://docs.djangoproject.com/en/3.1/topics/install/#installing-official-release)
3. Ubicarse en la carpeta /nornpeoplechallenge del proyecto 
4. Abrir el archivo /nornpeoplechallege/nornpeoplechallenge/settings.py 
5. En settings.py buscar en la linea #77 en el apartado "DATABASES" la sección del engine 'django.db.backends.postgresql_psycopg2' y de ser necesario cambiar los valores de los campos NAME,USER,PASSWORD, HOST Y PORT por los valores necesarios para conectarse a la base de datos postgresql 
6. Abrir una terminal ubicada en la carpeta principal del proyecto donde se encuentra el arhivo manage.py
7. En la terminal ejecutar el comando: python manage.py makemigrations
8. En la terminal ejecutar el comando: python manage.py migrate
9. En la terminal ejecutar el comando: python manage.py collectstatic y poner 'yes'
10. En la terminal ejecutar el comando: python manage.py createsuperuser y responder lo que se te pide para crear el primer usuario
11. En la terminal ejecutar el comando: python manage.py runserver

¡Se ha instalado! Ahora abre en un navegador web y pon la dirección http://localhost:8000/ para empezar a usar la app con el usuario que creaste en el paso 10
