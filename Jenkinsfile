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
	JFROG_ARTIFACTORY_URL = "https://gurpreetgs.jfrog.io/artifactory/tx-demo-docker/"
	Image1 = "tx-blog-app-main-flask-app:latest"
        Image2 = "tx-blog-app-flask-blog-app:latest"
	DOCKER_IMAGE_NAME = "gurpreetgs.jfrog.io/docker-local-1/tx-blog-app-main-flask-app:latest"
	DOCKER_IMAGE_NAME2 = "gurpreetgs.jfrog.io/docker-local/tx-blog-app-flask-blog-app:latest"
	
        
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
	// stage('Manual Approval for deployment'){
 //                steps{              
 //                    script {
 //                        timeout(time: 10, unit: 'MINUTES'){
 //                            input ('Do you want to proceed with Deployment?')
 //                        }
 //                    }        
 //                } 
 //        }
	stage('Manual Approval for deployment') {
            steps {
                script {
                    // Send email for manual approval
                    emailext subject: 'Manual Approval Required',
                              body: 'Please approve the deployment by clicking on the following link: ${BUILD_URL}input',
                              to: 'ipreetgs@gmail.com',
                              mimeType: 'text/html'
                    
                    // Pause and wait for manual approval
                    input(id:'Proceed1', message: 'Promote build?',parameters:[[$class:'BooleanParameterDefinition', defaultValue: true, name: 'Please approve the deployment in your email client.', submitter: 'ipreetgs@gmail.com']])
                }
            }
        }
        stage('Deployment') {
            steps {
                echo 'Hi'
                sh 'docker-compose up -d'
            }
        }
    	stage('Scan Docker Image') {
            steps {
                // Scan Docker image
                sh " trivy image  -o reports/docker-image-scan.html --timeout 30m tx-blog-app-main-flask-app:latest"
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
		sh "trivy image -o reports/docker-image-scan1.html --timeout 30m tx-blog-app-flask-blog-app:latest"
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
	stage('Publist art. Jfrog') {
            steps {
		    sh 'docker tag $Image1 $DOCKER_IMAGE_NAME'
		    sh 'docker tag $Image2 $DOCKER_IMAGE_NAME2'
		    jf 'docker push $DOCKER_IMAGE_NAME'
		    jf 'docker push $DOCKER_IMAGE_NAME2'
	    	   // sh "jfrog rt docker-push ${Image1} --url=${JFROG_ARTIFACTORY_URL} --build-name=main-build --build-number=1"
	    	   // sh "jfrog rt docker-push ${Image2} --url=${JFROG_ARTIFACTORY_URL} --build-name=blog-build --build-number=1"
            }
        }
	stage('Publish build info') {
			steps {
				jf 'rt build-publish'
			}
		}
	stage('DAST Approval') {
            steps {
                script {
                    // Send email for manual approval
                    emailext subject: 'Manual Approval Required',
                              body: 'Please approve the DAST by clicking on the following link: ${BUILD_URL}input',
                              to: 'ipreetgs@gmail.com',
                              mimeType: 'text/html'
                    
                    // Pause and wait for manual approval
                    input(id:'Proceed1', message: 'Promote build?',parameters:[[$class:'BooleanParameterDefinition', defaultValue: true, name: 'Please approve the dast in your email client.', submitter: 'ipreetgs@gmail.com']])
                }
            }
        }
	stage('Nikto VAPT') {
            steps {
                sh 'nikto -h 192.168.6.118 -p 8080,8000,8090'
            }
        }
	stage('OWSP ZAP VAPT') {
            steps {
		catchError(buildResult: 'Success', stageResult: 'Success'){
                sleep time: 30, unit: 'SECONDS'
                sh 'docker run --rm -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t http://192.168.6.118:8090 -x xml_report.xml -r zap-report.html'
		sh 'echo Scan Done'
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
