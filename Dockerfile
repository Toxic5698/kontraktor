FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev git\
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

RUN pip install --upgrade pip setuptools wheel

COPY app .app
RUN pip install -r .app/requirements.txt
