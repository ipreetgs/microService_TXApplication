pipeline {
    agent any
    tools {
		jfrog 'jfrog-cli'
	}

    environment {
        scannerHome = tool 'sonar-scanner'
        sonarqubeUrl = 'http://192.168.6.118:9000'  // Replace with your SonarQube server URL
        JAVA_HOME = "${tool 'java'}"
        APPD_ACCOUNT = credentials('AppDynamicsAAC')
        APPD_ACCESSKEY = credentials('AppDynamicsSEC')
	WEBSITES = 'http://192.168.6.118:8090/,http://192.168.6.118:8000/'
        // APPD_ACCOUNT = 'credentials(AppDynamics).username'
        // APPD_ACCESSKEY = 'credentials(AppDynamics).password'
	JFROG_ARTIFACTORY_URL = "https://gurpreetgs.jfrog.io/artifactory/"
	Image1 = "tx-blog-app-main-flask-app:latest"
        Image2 = "tx-blog-app-flask-blog-app:latest"
	DOCKER_IMAGE_NAME = "gurpreetgs.jfrog.io/docker-local/hello-frog:1.0.0"
        
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
                sh 'bearer scan . --format=html --output=reports/bearer-scan-report.html'
            }
        }
	stage('Publish Bearer Scan Report') {
        steps {
            publishHTML target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'bearer-scan-report.html',
                reportName: 'Bearer Scan',
                reportTitles: 'Bearer Scan'
            ]
        }
    }
	stage('Scan Python Code') {
            steps {
                // Scan Python code
                sh "trivy filesystem --ignore-unfixed --vuln-type os,library --format template --template table -o reports/python-code-scan.html ."
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
                sh "trivy image --ignore-unfixed --vuln-type os,library --format template --template table -o reports/docker-image-scan.html --timeout 30m tx-blog-app-main-flask-app:latest"
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
		sh "trivy image --ignore-unfixed --vuln-type os,library --format template --template table -o reports/docker-image-scan1.html --timeout 30m tx-blog-app-flask-blog-app:latest"
                publishHTML target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'docker-image-scan1.html',
                    reportName: 'Docker Image Scan blog',
                    reportTitles: 'Docker Image Scan blog app'
                ]

                // Fail the build on CRITICAL vulnerabilities
                sh "trivy image --ignore-unfixed --vuln-type os,library --exit-code 1 --severity CRITICAL tx-blog-app-flask-blog-app:latest"
            }
        }
	// stage('Publist art. Jfrog') {
 //            steps {
 //                sh 'echo hello'
	    	   sh "jfrog rt docker-push ${Image1} --url=${JFROG_ARTIFACTORY_URL} --build-name=main-build --build-number=1"
	    	   sh "jfrog rt docker-push ${Image2} --url=${JFROG_ARTIFACTORY_URL} --build-name=blog-build --build-number=1"
 //            }
 //        }
	stage('Nikto VAPT') {
            steps {
                sh 'nikto -h 192.168.6.118 -p 80,88,443,9090,9000,8080,8000'
            }
        }
	// stage('ZAP VAPT') {
 //            steps {
 //                sh 'echo hello'
 //            }
 //        }

	// stage('Run ZAP Scan') {
 //            steps {
 //                script {
 //                    // Start ZAP in daemon mode
 //                    sh 'zap.sh -daemon -host 192.168.6.118 -port 8092 -config api.disablekey=true'
 //                    // Wait for ZAP to start
 //                    waitUntil { sh(script: 'curl -s http://192.168.6.118:8092/JSON/core/view/version/ | grep -q "Version"', returnStatus: true) == 0 }
 //                    // Run ZAP Spider and Active Scan
	// 	    def websites = env.WEBSITES.split(',')
	// 	    for (website in env.WEBSITES) {
 //                        echo "Scanning website: $website"
 //                        // Run ZAP Spider and Active Scan
 //                        sh "curl -X POST http://192.168.6.118:8092/JSON/spider/action/scan/ -d \"url=$website\""
 //                        sh "curl -X POST http://192.168.6.118:8092/JSON/ascan/action/scan/ -d \"url=$website\""
 //                        // Wait for scans to complete
 //                        waitUntil { sh(script: 'curl -s http://192.168.6.118:8092/JSON/spider/view/status/ | grep -q "\"status\":\"100\""', returnStatus: true) == 0 }
 //                        waitUntil { sh(script: 'curl -s http://192.168.6.118:8092/JSON/ascan/view/status/ | grep -q "\"status\":\"100\""', returnStatus: true) == 0 }
 //                        // Generate ZAP report for each website
 //                        sh "curl -o zap-report-$website.html http://192.168.6.118:8092/OTHER/core/other/htmlreport/"
 //                    }
 //                }
 //            }
 //        }
        stage('Start ZAP') {
            steps {
                script {
                    // Start ZAP as a daemon
                    sh 'zap.sh -daemon -host 127.0.0.1 -port 8092 -config api.disablekey=true'
                }
            }
        }

     //    stage('Run ZAP Scan') {
     //        steps {
     //            script {
     //                // Perform ZAP spidering and scanning
     //                sh 'zap-cli -p 8092 -config api.key="" --verbose quick-scan -o /reports/zap-report.html -u http://192.168.6.118:8000'
     //            }
     //        }
     //    }

     //    stage('Shutdown ZAP') {
     //        steps {
     //            script {
     //                // Shutdown ZAP after the scan is complete
     //                sh 'zap-cli -p 8092 --verbose shutdown'
     //            }
     //        }
     //    }

	    // post {
	    //     always {
	    //         // Archive ZAP scan reports as artifacts
	    //         archiveArtifacts 'reports/zap-report.html'
	    //     }
	    // }


        stage('Publish ZAP Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'report',
                    reportFiles: 'zap-report.html',
                    reportName: 'ZAP Report',
                    reportTitles: 'ZAP Report'
                ])
            }
        }
    }
}
