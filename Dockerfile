FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev git\
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

RUN pip install --upgrade pip

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

WORKDIR .

COPY ./web-entrypoint.sh /
ENTRYPOINT ["sh", "/web-entrypoint.sh"]

CMD ["gunicorn", "-c", "python:config.gunicorn", "config.wsgi"]
