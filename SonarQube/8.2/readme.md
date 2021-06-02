
## Build image

docker build -t sgt/sonarqube:8.2 .


## Iniciar entorno

docker-compose up


##Debug errors

docker-compose run --entrypoint /bin/bash -p 9000:9000 sonarqube

