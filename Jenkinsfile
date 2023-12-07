pipeline {
    agent any

    stages {
        stage('Git checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ipreetgs/microService_TXApplication.git']])
            }
        }
        stage('docker-compose') {
            steps {
                echo 'Hi'
                bat 'docker-compose up -d'
            }
        }
        stage('SonarQube analysis') { 
            steps { 
                withSonarQubeEnv(credentialsId: 'sonarqube', installationName: 'sonarqube')
                {
                    sh '${SCANNER_HOME**}**}/bin/sonar-scanner \
                    -Dsonar.projectKey=Demo \
                    -Dsonar.host.url=http://localhost:9000/'
                }
          }   
        }
    }
}
