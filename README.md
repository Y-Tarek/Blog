# Blog
Api and Admin dashboard for Blog posts & comments.

## API Documentation
https://documenter.getpostman.com/view/20343410/2s8YzZQzWg](https://documenter.getpostman.com/view/28439113/2sA3XTfL6S

## Prerequisite
>python

>postgressql

>Docker (optional for running docker container)

## Installtion
   If you have docker installed you can run the docker image provided inside the application by just running:
            
             Add .env file contains these variable
              - SQL_ENGINE=django.db.backends.postgresql (changeable)
              - SQL_DATABASE=blog (changeable)
              - SQL_HOST=db (This is database service in docker-compose file)
              - SQL_USER=postgres (changeable)
              - SQL_PASSWORD=postgres (changeable)
             docker-compose up --build
             Then go to (http://0.0.0.0:8000/admin) for admin dashboard and (http://0.0.0.0:8000/api) if the base URL.
             username and password for admin dashboard found in entrypoint.sh file.
             
  Or you can run it manually by:
   
         1- Add .env file contains these variable
              - SQL_ENGINE=django.db.backends.postgresql (changeable)
              - SQL_DATABASE=blog (changeable)
              - SQL_HOST=localhost (changeable)
              - SQL_USER=postgres (changeable)
              - SQL_PASSWORD=postgres (changeable)
         2- go inside the application and create virtual env to host the application requirements by running: (python -m venv venv).
         3- install the application required packages provided in requirements.txt file by running: (pip install -r requirememnts.txt).
         4- Run python manage.py makemigrations.
         5- Run python manage.py migrate.
         6- Run python manage.py createsuperuser (required for logining to admin dashboard).
              will ask for email, username , first_name, last_name and password
         7- Run python manage.py runserver.
         8- Run python manage.py test for running test casesx on APIs.
