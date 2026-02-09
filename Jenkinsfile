pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        JMETER_HOME     = "C:\\tools\\apache-jmeter-5.6.3"
        PERF_THRESHOLD = "10"
        SONAR_PROJECT  = "petclinic-rest-testing-demo"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build + Tests') {
            steps {
                bat "mvn clean verify"
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('JMeter Performance') {
            steps {
                bat """
                %JMETER_HOME%\\bin\\jmeter.bat -n ^
                -t jmeter\\petclinic-smoke.jmx ^
                -l result.csv
                """
            }
        }

        stage('Record Performance') {
            steps {
                bat """
                if not exist perf\\history mkdir perf\\history
                C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe ^
                -ExecutionPolicy Bypass ^
                -File perf\\extract.ps1 result.csv perf\\history\\trend.csv
                """
            }
        }

        stage('Fetch Baseline') {
    when { not { branch 'master' } }
    steps {
        bat """
        if not exist perf mkdir perf
        copy "%JENKINS_HOME%\\workspace\\petclinic-multibranch_master\\perf\\baseline.csv" perf\\baseline.csv
        """
    }
}


        stage('Performance Gate') {
            when { not { branch 'master' } }
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat """
                    C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe ^
                    -ExecutionPolicy Bypass ^
                    -File perf\\compare.ps1 perf\\baseline.csv result.csv %PERF_THRESHOLD%
                    """
                }
            }
        }

        stage('Reviewer Override') {
            when {
                expression { currentBuild.currentResult == 'FAILURE' }
            }
            steps {
                input message: "Performance regression detected. Override merge?"
                script {
                    currentBuild.result = 'SUCCESS'
                }
            }
        }

        stage('Update Baseline') {
            when { branch 'master' }
            steps {
                bat """
                if not exist perf mkdir perf
                copy result.csv perf\\baseline.csv
                """
            }
        }

        stage('Performance Chart') {
            steps {
                plot csvFileName: 'trend.csv',
                     csvSeries: [[file: 'perf/history/trend.csv']],
                     group: 'Performance',
                     title: 'Response Time Trend',
                     yaxis: 'Milliseconds',
                     style: 'line'
            }
        }

        stage('HTML Dashboard') {
            steps {
                bat """
                C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe ^
                -ExecutionPolicy Bypass ^
                -File perf\\dashboard.ps1
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'result.csv, perf/baseline.csv, perf/history/trend.csv, perf/dashboard.html', fingerprint: true
        }
    }
}