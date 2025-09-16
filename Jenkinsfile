pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    ansiColor('xterm')
    timestamps()
  }

  stages {
    stage('Prepare') {
      steps {
        cleanWs()
        // Use the same checkout Jenkins used to fetch the Jenkinsfile
        checkout scm
      }
    }

    stage('Install Dependencies') {
      steps {
        script {
          if (isUnix()) {
            sh """#!/bin/bash
set -euo pipefail
python3 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
"""
          } else {
            bat """
@echo off
python -m venv venv
call venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
"""
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          if (isUnix()) {
            sh """#!/bin/bash
set -euo pipefail
. venv/bin/activate
pytest --maxfail=1 --disable-warnings -q
"""
          } else {
            bat """
@echo off
call venv\\Scripts\\activate
pytest --maxfail=1 --disable-warnings -q
"""
          }
        }
      }
    }

    stage('Run App') {
      steps {
        script {
          if (isUnix()) {
            sh """#!/bin/bash
. venv/bin/activate
nohup python app.py > app.log 2>&1 & echo $! > app.pid || true
"""
          } else {
            bat """
@echo off
call venv\\Scripts\\activate
START /B python app.py > app.log 2>&1
echo started > app.pid
"""
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'app.log', allowEmptyArchive: true
      echo "Pipeline finished. Check app.log and app.pid in workspace."
    }
    failure {
      echo "Build failed — see console and app.log for details."
    }
  }
}
