FROM python:3.7
MAINTAINER Jack Sellers

ENV PYTHONUNBUFFERED 1

RUN mkdir /home/config
ADD config/requirements.txt /home/config/
RUN pip install -r /home/config/requirements.txt

RUN mkdir /home/app
WORKDIR /home/app
COPY . /home/app

RUN mkdir -p /home/app/media
RUN groupadd varwwwusers
RUN adduser www-data varwwwusers
RUN chgrp -R varwwwusers /home/app/media
RUN chmod -R 770 /home/app/media
