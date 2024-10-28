pipeline {
    agent any

    environment {
        // Define environment variables
        REPO_URL = 'https://github.com/yourusername/your-repo.git' // Your GitHub repo URL
        TARGET_SERVER = 'user@your-server.com' // Your target server
        TARGET_DIR = '/path/to/deployment/directory' // Deployment directory on the target server
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out the code from GitHub...'
                // Checkout code from the repository
                checkout scm
            }
        }

        stage('Build Application') {
            steps {
                echo 'Building the application...'
                // Example build command; modify as necessary for your project
                sh 'npm install' // For Node.js projects
                // sh './gradlew build' // For Java projects
                // sh 'python setup.py install' // For Python projects
            }
        }

        stage('Deploy to Server') {
            steps {
                echo 'Deploying to the target server...'
                // Transfer files to the target server and execute deployment commands
                sh """
                scp -r ./* ${TARGET_SERVER}:${TARGET_DIR}
                ssh ${TARGET_SERVER} 'cd ${TARGET_DIR} && npm run start' // Adjust command as needed
                """
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
            // Optional: Notify via email or other services
        }
        failure {
            echo 'Deployment failed!'
            // Optional: Notify via email or other services
        }
        always {
            echo 'Cleaning up workspace...'
            // Clean up workspace if needed
            cleanWs()
        }
    }
}
