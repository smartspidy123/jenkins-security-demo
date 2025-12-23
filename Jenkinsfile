pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Security Gate') {
            steps {
                echo ' 🛡️ Scanning for Viruses & Secrets...'
                // STRICT MODE: We use "p/secrets" and "p/default" to catch everything
                // --error: Fails the build if ANY issue is found
                sh 'semgrep scan --config=p/secrets --config=p/default --error --output semgrep_report.txt .'
            }
        }

        stage('Deploy Website') {
            // This stage ONLY runs if "Security Gate" passed
            steps {
                echo ' ✅ Code is Safe! Deploying to Live Server...'
                // We overwrite the live website with the new code
                sh 'cp index.html ~/Downloads/my-website/index.html'
            }
        }
    }
}
