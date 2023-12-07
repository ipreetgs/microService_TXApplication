pipeline {
    agent any

    environment {
        scannerHome = tool 'sonar-scanner'
        sonarqubeUrl = 'http://localhost:9000'  // Replace with your SonarQube server URL
    }


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
                def scannerCmd = "${scannerHome}/bin/sonar-scanner"
                withSonarQubeEnv(credentialsId: 'sonarqube', installationName: 'sonarqube')
                {
                    sh "${scannerCmd} \
                    -Dsonar.host.url=${sonarqubeUrl} \
                    -Dsonar.projectKey=jenkins \
                    -Dsonar.sources=src"
                }
          }   
        }
    }
}
