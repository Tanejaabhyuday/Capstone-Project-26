pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/Tanejaabhyuday/Capstone-Project-26.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test Application') {
            steps {
                echo "Checking Python syntax..."
                bat 'python -m py_compile app.py'
            }
        }

        stage('Run Flask App') {
            steps {
                echo "Starting Flask application..."
                bat 'python app.py'
            }
        }

    }

    post {
        success {
            echo 'Application started successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
