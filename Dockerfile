FROM python:3.11.4-slim-bullseye

RUN pip install --upgrade pip

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

WORKDIR .

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
