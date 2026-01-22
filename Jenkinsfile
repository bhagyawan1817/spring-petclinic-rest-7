pipeline {
    agent any

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
        stage('Performance Test (JMeter – report only)') {
            steps {
                sh '''
                    jmeter \
                        -n \
                        -t jmeter/petclinic-smoke.jmx \
                        -l target/jmeter-results.jtl \
                        -JHOST=localhost \
                        -JPORT=9966 \
                    ||true
                '''
            }
        }
    }
    post {
        always {

            // Unit test reports (non-blocking)
            catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') {
                junit allowEmptyResults: true,
                    testResults: '**/target/surefire-reports/*.xml'
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


