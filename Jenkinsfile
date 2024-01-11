pipeline {
    agent any

    environment {
        scannerHome = tool 'sonar-scanner'
        sonarqubeUrl = 'http://192.168.6.118:9000'  // Replace with your SonarQube server URL
        JAVA_HOME = "${tool 'java'}"
        APPD_ACCOUNT = credentials('AppDynamicsAAC')
        APPD_ACCESSKEY = credentials('AppDynamicsSEC')
        TRIVY_VERSION = 'v0.18.3'
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
                    // sh 'cp appdynamics.cfg ./'
                    // sh 'cp appdynamics1.cfg ./'
                }
            }
        }
        stage('docker-compose') {
            steps {
                echo 'Hi'
                sh 'docker-compose up -d'
            }
        }
    	stage('Scan Docker Image') {
            steps {
                // Install Trivy
                sh "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin ${TRIVY_VERSION}"

                // Scan Docker image
                sh "trivy image --ignore-unfixed --vuln-type os,library --format template --template '@html.tpl' -o reports/docker-image-scan.html tx-blog-app-main-flask-app:latest"
                publishHTML target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'docker-image-scan.html',
                    reportName: 'Docker Image Scan',
                    reportTitles: 'Docker Image Scan'
                ]

                // Fail the build on CRITICAL vulnerabilities
                sh "trivy image --ignore-unfixed --vuln-type os,library --exit-code 1 --severity CRITICAL tx-blog-app-main-flask-app:latest"
		// scan img2
		sh "trivy image --ignore-unfixed --vuln-type os,library --format template --template '@html.tpl' -o reports/docker-image-scan.html flask-blog-app:latest"
                publishHTML target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'docker-image-scan.html',
                    reportName: 'Docker Image Scan',
                    reportTitles: 'Docker Image Scan'
                ]

                // Fail the build on CRITICAL vulnerabilities
                sh "trivy image --ignore-unfixed --vuln-type os,library --exit-code 1 --severity CRITICAL flask-blog-app:latest"
            }
        }

        stage('Scan Python Code') {
            steps {
                // Install Trivy
                sh "curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin ${TRIVY_VERSION}"

                // Scan Python code
                sh "trivy filesystem --ignore-unfixed --vuln-type os,library --format template --template '@html.tpl' -o reports/python-code-scan.html ."
                publishHTML target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'python-code-scan.html',
                    reportName: 'Python Code Scan',
                    reportTitles: 'Python Code Scan'
                ]

                // Fail the build on CRITICAL vulnerabilities
                sh "trivy filesystem --ignore-unfixed --vuln-type os,library --exit-code 1 --severity CRITICAL ."
            }
        }
    }
}
