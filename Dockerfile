#FROM python:3.9
#
#RUN pip install --upgrade pip
#
#COPY app/requirements.txt .
#RUN pip install -r requirements.txt
#
#COPY /app .
#
#WORKDIR .
#
#COPY ./entrypoint.sh /
#ENTRYPOINT ["sh", "/entrypoint.sh"]

FROM python:3.11.4-slim-bullseye AS app
LABEL maintainer="Petr Čech <petr@cechpetr.cz>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev git\
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python

USER python

COPY --chown=python:python app/requirements*.txt ./

RUN pip install --no-warn-script-location --no-cache-dir --user -r requirements.txt


ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

EXPOSE 8000

CMD ["gunicorn", "-c", "python:kontraktor.gunicorn", "app.kontraktor.wsgi"]
