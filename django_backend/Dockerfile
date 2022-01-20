FROM python:3.9

ENV PYTHONUNBUFFERED=1
WORKDIR /django_backend

# Required to install mysqlclient with Pip
RUN apt-get update \
  && apt-get install python3-dev default-libmysqlclient-dev gcc -y


# Copy the application files into the image
COPY .. /django_backend/

RUN pip install -r requirements.txt

# Expose port 8000 on the container
EXPOSE 8000