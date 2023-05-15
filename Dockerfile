# Pull base image
FROM python:3.10.10-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1

WORKDIR /dornica_test

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
