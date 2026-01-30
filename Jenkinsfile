pipeline {
    agent any

    environment {
        BASE_URL = "http://127.0.0.1:9966/petclinic"
    }

    stages {

        stage('Compile') {
            steps {
                sh './mvnw clean compile'
            }
        }

        stage('Lint (Checkstyle – report only)') {
            steps {
                sh './mvnw checkstyle:check || true'
            }
        }

        stage('SpotBugs (report only)') {
            steps {
                sh './mvnw spotbugs:check || true'
            }
        }

        stage('PMD (report only)') {
            steps {
                sh './mvnw pmd:check || true'
            }
        }

        stage('Dependency Scan (OWASP - report only)') {
            steps {
                sh './mvnw org.owasp:dependency-check-maven:check || true'
            }
        }

        stage('Unit Tests with Coverage') {
            steps {
                sh './mvnw test jacoco:report || true'
            }
        }

        stage('Start App (background)') {
            steps {
                sh '''
                    nohup ./mvnw spring-boot:run \
                      -Dspring-boot.run.arguments=--server.port=9966 \
                      > app.log 2>&1 &
                    sleep 30
                '''
            }
        }

        stage('API Tests (Python – BLOCKING)') {
            steps {
                sh '''
                    cd api-tests
                    pip3 install -r requirements.txt
                    BASE_URL=${BASE_URL} pytest
                '''
            }
        }

        stage('Performance Test (JMeter – report only)') {
            steps {
                sh '''
                    /usr/local/bin/jmeter \
                        -n \
                        -t jmeter/petclinic-smoke.jmx \
                        -l target/jmeter-results.jtl \
                        -JHOST=127.0.0.1 \
                        -JPORT=9966 \
                  || true
                '''
            }
        }
    }

    post {
        always {

            // Stop Spring Boot app
            sh 'pkill -f spring-boot || true'

            // Unit test reports (non-blocking)
            catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                junit allowEmptyResults: true,
                    testResults: '**/target/surefire-reports/*.xml'
            }

            // API test reports (blocking already happened)
            catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                junit allowEmptyResults: true,
                    testResults: 'api-tests/**/pytest*.xml'
            }

            // JMeter performance reports (non-blocking)
            catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                performanceReport parsers: [
                    jmeterParser(
                        pattern: 'target/jmeter-results.jtl'
                    )
                ]
            }
        }
    }
}