pipeline {
    agent any

    environment {
        // Update these two lines with your actual Docker Hub details
        DOCKER_IMAGE = "your-dockerhub-username/capstone-project-26"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' 
    }

    stages {
        stage('Cleanup & Checkout') {
            steps {
                // Wipes the workspace to ensure a fresh start
                cleanWs()
                git branch: 'main', url: 'https://github.com/Tanejaabhyuday/Capstone-Project-26.git'
                
                // DEBUG: This will list all files in your console log. 
                // Check the log to see if package.json is in a subfolder!
                bat 'dir' 
            }
        }

        stage('Install Dependencies') {
            steps {
                // If package.json is in a subfolder (e.g., 'server'), 
                // wrap the bat command in: dir('server') { bat 'npm install' }
                bat 'npm install'
            }
        }

        stage('Security Audit') {
            steps {
                // 'exit 0' ensures the build continues even if audit finds issues
                bat 'npm audit fix --force || exit 0'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% ."
                    bat "docker tag %DOCKER_IMAGE%:%BUILD_NUMBER% %DOCKER_IMAGE%:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "%DOCKER_CREDENTIALS_ID%", 
                                 passwordVariable: 'DOCKER_PASSWORD', 
                                 usernameVariable: 'DOCKER_USERNAME')]) {
                    
                    // Windows-specific syntax for accessing environment variables in batch
                    bat "echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin"
                    bat "docker push %DOCKER_IMAGE%:%BUILD_NUMBER%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the "dir" output in the "Cleanup & Checkout" stage to verify file paths.'
        }
    }
}
