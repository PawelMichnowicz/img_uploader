FROM python:3.10.2-slim

RUN mkdir /code
WORKDIR /code

RUN apt update
RUN python -m pip install --upgrade pip
COPY . .
RUN pip install -r app/requirements.txt

EXPOSE 8000