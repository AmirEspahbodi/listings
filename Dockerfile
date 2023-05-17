# Pull base image
FROM python:3.10.10-slim

RUN mkdir /working
WORKDIR /working


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./dornica_test /working
CMD ["python3", "-m", "scripts.on_start"]
