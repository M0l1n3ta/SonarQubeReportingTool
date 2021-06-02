

docker build -t sgt/sonarqube:lts .


docker-compose run -e SONARQUBE_JDBC_URL=jdbc:postgresql://db:5432/sonar -e SONARQUBE_JDBC_USERNAME=sonar -e SONARQUBE_JDBC_PASSWORD=sonar  sonarqube bash

docker-compose run --entrypoint /bin/bash -e SONARQUBE_JDBC_URL=jdbc:postgresql://db:5432/sonar -e SONARQUBE_JDBC_USERNAME=sonar -e SONARQUBE_JDBC_PASSWORD=sonar  sonarqube 


docker-compose run -u 0 --entrypoint /bin/bash sonarqube

docker-compose run  --entrypoint /bin/bash sonarqube

docker commit --pause <id> sgt/sonarqube:lts 