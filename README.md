# Django Base Api

This is a base project for API applications built with Django and Django Rest Framework.

Includes several customizations on top of Django Rest Framework for JWT authentication, normalized responses and global exception handling.

Built with Django 2.1.7 and Django Rest Framework 3.9.2 . Tested with Python 3.6

## Environment variables

Api expects database settings to be defined in environment variables, to be able to run the server and tests. Required environment variables are:

**dbname**: Name of the database<br/>
**dbuser**: Name of the database user<br/>
**dbpass**: Password for database user<br/>
**dbhost**: Hostname of the database server<br/>
**dbport**: Port on which the database server is listening

## Development server

Run `python manage.py runserver` for a dev server. Navigate to `http://localhost:8000/`.

## Running unit tests

Run `python manage.py test` to execute the unit tests.


## Deployment

Project is bundled with a simple setup for deployment via Docker. After cd-ing into the project directory, run the following commands to build a docker image and run it:

**docker image build -t django-api-base .**<br/>
**docker run -d -p host_port:80 -e dbname=database_name -e dbuser=database_user -e dbpass=database_password -e dbhost=database_host -e dbport=database_port django-api-base**
