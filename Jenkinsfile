pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/killerangaswamy56/python-jenkins-project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Run App') {
            steps {
                sh '. venv/bin/activate && python app.py &'
            }
        }
    }
}
