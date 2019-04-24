FROM python:3.6

# Prepare container
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip nginx supervisor
RUN pip3 install gunicorn

# Copy app files
RUN mkdir -p /usr/src/app
COPY ./ /usr/src/app
WORKDIR ./usr/src/app

# Install requirements
RUN pip3 install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

COPY ./deployment/nginx.conf /etc/nginx/sites-enabled/default

CMD supervisord -c /usr/src/app/deployment/supervisord.conf