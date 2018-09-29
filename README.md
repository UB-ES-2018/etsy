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
2. 'docker exec -it "container_name"' to enter into the container.

Run manage.py:

1. Enter to "etsy_web_1" container.
2. 'cd' to "etsy/web/etsy/".
3. 'python manage.py runserver'.
