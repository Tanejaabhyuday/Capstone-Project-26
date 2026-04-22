pipeline {
    agent any

    environment {
        // Replace with your actual Docker Hub username
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

        stage('Build Docker Image') {
            steps {
                script {
                    // This builds your debian-based container and installs the camera drivers/flask
                    bat "docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% ."
                    bat "docker tag %DOCKER_IMAGE%:%BUILD_NUMBER% %DOCKER_IMAGE%:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Ensure 'docker-hub-credentials' is set up in Jenkins Credentials
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", 
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
            echo 'Build Successful: Image pushed to Docker Hub.'
        }
        failure {
            echo 'Build Failed: Check if Docker Desktop is running on the Jenkins host.'
        }
    }
}
