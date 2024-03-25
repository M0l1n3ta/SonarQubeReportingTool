

## Running SonarScanner CLI from the Docker image
To scan using the SonarScanner CLI Docker image, use the following command:


docker run \
    --rm \
    -e SONAR_HOST_URL="http://${SONARQUBE_URL}" \
    -e SONAR_SCANNER_OPTS="-Dsonar.projectKey=${YOUR_PROJECT_KEY}" \
    -e SONAR_TOKEN="myAuthenticationToken" \
    -v "${YOUR_REPO}:/usr/src" \
    sonarsource/sonar-scanner-cli


## Run sonarscanner Locally


```
 sonar-scanner -D sonar.login=sqa_277b77c3a68d108975ed38ae1582196c2c7ae4c7
```