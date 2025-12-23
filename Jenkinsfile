pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Security Gate') {
            parallel {
                stage('Semgrep SAST') {
                    steps {
                        echo 'Running Semgrep on Pull Request...'
                        // --error: Fails the build if bugs are found
                        sh 'semgrep scan --config=auto --error --output semgrep_report.txt .' 
                    }
                }
                stage('Trivy SCA') {
                    steps {
                        echo 'Running Trivy on Dependencies...'
                        // --exit-code 1: Fails the build if vulnerabilities are found
                        sh 'trivy fs --exit-code 1 --output trivy_report.txt .'
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main' // Only deploy if we are on the 'main' branch
            }
            steps {
                echo 'Deploying to Production Server...'
            }
        }
    }
}
