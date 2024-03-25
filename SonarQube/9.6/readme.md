
## Build image

docker build -t titanium/sonarqube:9.6.1 .


## Iniciar entorno

docker-compose up


## Debug errors

docker-compose run --entrypoint /bin/bash -p 9000:9000 sonarqube

