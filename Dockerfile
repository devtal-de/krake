FROM python:alpine

RUN pip install  Django==3.2 
RUN apk add gcc build-base

ADD . /app

RUN pip install -r /app/requirements.txt
