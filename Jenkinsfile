pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "your-dockerhub-username/capstone-project-26"
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Tanejaabhyuday/Capstone-Project-26.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                // Changed sh to bat
                bat 'npm install'
            }
        }
        stage('Security Audit') {
            steps {
                // Changed sh to bat
                bat 'npm audit fix --force || exit 0' 
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Changed sh to bat
                    bat "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    bat "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                }
            }
        }
        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", 
                                 passwordVariable: 'DOCKER_PASSWORD', 
                                 usernameVariable: 'DOCKER_USERNAME')]) {
                    // Using powershell or bat for the login string
                    bat "echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin"
                    bat "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                    bat "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }
    }
    post {
        success { echo 'Deployment Successful' }
        failure { echo 'Build Failed - Check Console Output' }
    }
}
