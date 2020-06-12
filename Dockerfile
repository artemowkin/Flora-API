FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /flora

COPY Pipfile Pipfile.lock /flora/
RUN pip install pipenv && pipenv install --system

COPY . /flora/
