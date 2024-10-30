FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

