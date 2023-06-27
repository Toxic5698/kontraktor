FROM python:3.9


RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev git\
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

RUN pip install --upgrade pip

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

WORKDIR .

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
