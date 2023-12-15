#?/bin/sh

# fill token above -p
docker login -u cechpetr -p
docker build -t cechpetr/shi-server --platform linux/amd64 .
# change number of version
docker push cechpetr/shi-server:v1.0
