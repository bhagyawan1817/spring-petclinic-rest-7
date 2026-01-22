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
    }
    post {
        always {
            junit '**/target/surefire-reports/*.xml'
        }
    }
    // post {
    // always {
    //     warnings(
    //         canResolveRelativePaths: true,
    //         parserConfigurations: [
    //             checkstyle(pattern: '**/checkstyle-result.xml'),
    //             // spotbugs(pattern: '**/spotbugsXml.xml'),
    //             // pmdParser(pattern: '**/pmd.xml')
    //         ]
    //     )

    //     dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
    //}
    // }
}


