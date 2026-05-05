pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/killerangaswamy56/python-jenkins-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t python-jenkins-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop python-container || exit 0'
                bat 'docker rm python-container || exit 0'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 5000:5000 --name python-container python-jenkins-app'
            }
        }
    }
}
