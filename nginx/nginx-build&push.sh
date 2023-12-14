#?/bin/sh

docker login -u cechpetr -p
docker build -t cechpetr/shi-server --platform linux/amd64 .
docker push cechpetr/shi-server:latest
