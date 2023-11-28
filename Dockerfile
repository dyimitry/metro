FROM python:3.8-slim

RUN mkdir /src

COPY ./requirements.txt /src

RUN pip install -r /src/requirements.txt --no-cache-dir

COPY ./.env /src

COPY ./alembic.ini /src
COPY ./alembic /src/alembic

COPY ./auchan /src
COPY db/db.py /src
COPY ./main.py /src

WORKDIR /src