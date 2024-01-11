pipeline {
    agent any

    environment {
        scannerHome = tool 'sonar-scanner'
        sonarqubeUrl = 'http://192.168.6.118:9000'  // Replace with your SonarQube server URL
        JAVA_HOME = "${tool 'java'}"
    }


    stages {
        stage('Git checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/ipreetgs/microService_TXApplication.git']])
            }
        }
        stage('SonarQube analysis') { 
            steps {
                withSonarQubeEnv(credentialsId: 'sonarqube', installationName: 'sonarqube')
                {
                    bat "${scannerHome}/bin/sonar-scanner \
                    -Dsonar.host.url=${sonarqubeUrl} \
                    -Dsonar.projectKey=jenkins"
                    // -Dsonar.sources=src"
                }
          }   
        }
        stage('docker-compose') {
            steps {
                echo 'Hi'
                bat 'docker-compose up -d'
            }
        }
    }
}
