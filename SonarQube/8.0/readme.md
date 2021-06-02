
**build**
docker build -t sgt/sonarqube:8 .

docker run -it -link 80_db_1:db -e SONARQUBE_JDBC_URL=jdbc:postgresql://db:5432/sonar -e SONAR_JDBC_USERNAME=sonar -e SONAR_JDBC_PASSWORD=sonar sgt/sonar:8.0 /bin/bash


docker-compose run -e SONARQUBE_JDBC_URL=jdbc:postgresql://db:5432/sonar -e SONARQUBE_JDBC_USERNAME=sonar -e SONARQUBE_JDBC_PASSWORD=sonar  sonarqube 

docker-compose run --entrypoint /bin/bash -e SONARQUBE_JDBC_URL=jdbc:postgresql://db:5432/sonar -e SONARQUBE_JDBC_USERNAME=sonar -e SONARQUBE_JDBC_PASSWORD=sonar  sonarqube 

docker-compose run --entrypoint /bin/bash -p 9000:9000 sonarqube