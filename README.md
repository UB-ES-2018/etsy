# etsy

El entorno de desarrollo esta configurado con docker siguiendo los pasos de los chicos de [capisde](https://www.capside.com/labs/deploying-full-django-stack-with-docker-compose/)

Prerequisites:

You will need to have docker installed at your system and running

Steps:

1. Clone the repo
2. Copy the env.example file to a new env file at the root of the project.
3. Set the password for the database at the env file
4. Build the containers: `docker-compose build`
5. Run the containers: `docker-compose up -d`
6. Test at your browser that `http://localhost` is up and running.

Access to docker containers:

1. 'docker ps' to get all containers information.
2. 'docker exec -it "container_name" /bin/sh' to enter into the container.

Run manage.py:

1. Enter to "etsy_web_1" container.
2. 'cd' to "etsy/web/etsy/".
3. 'python manage.py "command"'.

ATTENTION:

When 'docker-compose up', if database raises an error, check permissions in "postgres/docker-entrypoint-initdb.d/etsy_web.sh".
Detected related error also when doing migrations.
If the problem persits, try to:
  1. Enter to the postgres container.
  2. psql -U postgres -c "CREATE USER $DB_USER PASSWORD '$DB_PASS'"
  3. psql -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"
  4. Exit postgres container, enter to web's one and create superuser with 'python3 manage.py createsuperuser'
  
When 'docker-compose build' it may raise an error showing that "ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?", or similar. A solution to this may be adding docker to a security group, doing the following steps:
  1. 'sudo usermod -aG docker $USER'
  2. Login out and back in.
