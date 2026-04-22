pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/capstone-project-26"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials' 
    }

    stages {
        stage('Cleanup & Checkout') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Tanejaabhyuday/Capstone-Project-26.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Using pip for your Python requirements
                bat 'pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
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
                    
                    bat "echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin"
                    bat "docker push %DOCKER_IMAGE%:%BUILD_NUMBER%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }
    }

    post {
        success {
            echo 'Python Project Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the console logs for Python/Docker errors.'
        }
    }
}
