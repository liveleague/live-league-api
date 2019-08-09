FROM python:3.7
MAINTAINER Jack Sellers

ENV PYTHONUNBUFFERED 1

RUN mkdir /home/config
ADD config/requirements.txt /home/config/
RUN pip install -r /home/config/requirements.txt

RUN mkdir /home/app
WORKDIR /home/app
COPY . /home/app
RUN chmod g+s /home/app
RUN chmod -R o+rX /home/app
