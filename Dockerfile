FROM python:3.9

RUN pip install --upgrade pip

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

WORKDIR .

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
