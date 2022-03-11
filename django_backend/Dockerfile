# pull official base image
FROM python:3.9

# set work directory
WORKDIR /usr/src/django_backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev gcc netcat -y

# install dependencies
#RUN pip install --upgrade pip
COPY ./requirements ./requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/django_backend/entrypoint.sh
RUN chmod 777 /usr/src/django_backend/entrypoint.sh


# run entrypoint.sh
ENTRYPOINT ["/usr/src/django_backend/entrypoint.sh"]
