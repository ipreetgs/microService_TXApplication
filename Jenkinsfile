pipeline {
    agent any

    environment {
        scannerHome = tool 'sonar-scanner'
        sonarqubeUrl = 'http://192.168.6.118:9000'  // Replace with your SonarQube server URL
        JAVA_HOME = "${tool 'java'}"
        APPD_ACCOUNT = credentials('AppDynamicsAAC')
        APPD_ACCESSKEY = credentials('AppDynamicsSEC')
        // APPD_ACCOUNT = 'credentials(AppDynamics).username'
        // APPD_ACCESSKEY = 'credentials(AppDynamics).password'
        
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
                    // bat "${scannerHome}/bin/sonar-scanner \
                    sh "${scannerHome}/bin/sonar-scanner \
                    -Dsonar.host.url=${sonarqubeUrl} \
                    -Dsonar.projectKey=jenkins"
                    // -Dsonar.sources=src"
                }
          }   
        }
        stage('Prepare Config AppDynamics') {
            steps {
                script {
                    // Replace placeholders in appdynamics.cfg
                    sh 'sed -i "s|account = |account = ${APPD_ACCOUNT}|g" appdynamics.cfg'
                    sh 'sed -i "s|accesskey = |accesskey = ${APPD_ACCESSKEY}|g" appdynamics.cfg'
                    sh 'sed -i "s|account = |account = ${APPD_ACCOUNT}|g" appdynamics1.cfg'
                    sh 'sed -i "s|accesskey = |accesskey = ${APPD_ACCESSKEY}|g" appdynamics1.cfg'

                    // Copy appdynamics.cfg to the build context
                    sh 'cp appdynamics.cfg ./'
                    sh 'cp appdynamics1.cfg ./'
                }
            }
        }
        stage('docker-compose') {
            steps {
                echo 'Hi'
        //         bat 'docker-compose up -d'
            }
        }
    }
}
