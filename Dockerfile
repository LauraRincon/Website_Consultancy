# build using:	 "sudo docker build --tag web_consultancy:latest ."
# run using:	 "sudo docker run -ti -p 8000:8000 web_consultancy:latest bash"
# then in container use: "./runserver"

# Defining base OS
FROM ubuntu:20.04

# Docker file information
LABEL MANTAINER = "ricardo.jimenez.anchia@gmail.com"
LABEL version = "1.0"
LABEL description = "Docker image for Webpage"

# Choose user root and getting libraries
USER root
RUN apt-get update
RUN apt-get install --yes python3-pip

# Creating project directory
FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install django-widget-tweaks
RUN pip install -r requirements.txt
COPY . /code/
