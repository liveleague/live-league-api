FROM python:3.7
MAINTAINER Jack Sellers

ENV PYTHONUNBUFFERED 1

RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip install -r /config/requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN mkdir -p /media
RUN groupadd varwwwusers
RUN adduser www-data varwwwusers
RUN chgrp -R varwwwusers /media/
RUN chmod -R 770 /media/
