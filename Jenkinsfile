pipeline {
    agent any

    environment {
        scannerHome = tool 'sonar-scanner'
        sonarqubeUrl = 'http://192.168.6.118:9000'  // Replace with your SonarQube server URL
        JAVA_HOME = "${tool 'java'}"
        APPD_ACCOUNT = credentials('AppDynamicsAAC')
        APPD_ACCESSKEY = credentials('AppDynamicsSEC')
	WEBSITES = 'http://192.168.6.118:8090/,http://192.168.6.118:8000/'
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
	stage('Bearer Code Scaning') {
            steps {
                sh 'bearer scan .'
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
	stage('Nikto VAPT') {
            steps {
                sh 'nikto -h 192.168.6.118 -p 80,88,443,9090,9000,8080,8000'
            }
        }
	stage('ZAP VAPT') {
            steps {
                sh 'echo hello'
            }
        }
	stage('Run ZAP Scan') {
            steps {
                script {
                    // Start ZAP in daemon mode
                    sh 'zap.sh -daemon -host 0.0.0.0 -port 5555 -config api.disablekey=true'

                    // Wait for ZAP to start
                    waitUntil { sh(script: 'curl -s http://localhost:5555/JSON/core/view/version/ | grep -q "Version"', returnStatus: true) == 0 }

                    // Run ZAP Spider and Active Scan
		    def websites = env.WEBSITES.split(',')
		    for (website in env.WEBSITES) {
                        echo "Scanning website: $website"

                        // Run ZAP Spider and Active Scan
                        sh "curl -X POST http://localhost:5555/JSON/spider/action/scan/ -d \"url=$website\""
                        sh "curl -X POST http://localhost:5555/JSON/ascan/action/scan/ -d \"url=$website\""

                        // Wait for scans to complete
                        waitUntil { sh(script: 'curl -s http://localhost:5555/JSON/spider/view/status/ | grep -q "\"status\":\"100\""', returnStatus: true) == 0 }
                        waitUntil { sh(script: 'curl -s http://localhost:5555/JSON/ascan/view/status/ | grep -q "\"status\":\"100\""', returnStatus: true) == 0 }

                        // Generate ZAP report for each website
                        sh "curl -o zap-report-$website.html http://localhost:5555/OTHER/core/other/htmlreport/"
                    }
                }
            }
        }

        stage('Publish ZAP Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'zap-report.html',
                    reportName: 'ZAP Report',
                    reportTitles: 'ZAP Report'
                ])
            }
        }
    }
}
