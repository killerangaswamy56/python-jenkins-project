pipeline {
  agent any

  options {
    // avoid long-running console tails; keep workspace clean for each run
    skipDefaultCheckout(true)
    ansiColor('xterm')
    timestamps()
  }

  stages {
    stage('Prepare') {
      steps {
        // Remove any stale workspace (safer than manual deletes)
        cleanWs()
        // Use the same checkout that Jenkins used to fetch the Jenkinsfile (avoid double-checkout problems)
        checkout scm
      }
    }

    stage('Checkout Code (ensure branch & credentials)') {
      steps {
        // If your pipeline is loaded from SCM, checkout scm above is enough.
        // Use an explicit checkout if you need to specify branch/credentials:
        script {
          // Uncomment and edit the block below if you must explicitly pass credentials and branch.
          /*
          checkout([$class: 'GitSCM',
            branches: [[name: '*/main']], 
            userRemoteConfigs: [[url: 'https://github.com/killerangaswamy56/python-jenkins-project.git', credentialsId: 'github-pat']]
          ])
          */
          echo "Repository is present. Using already checked out sources."
        }
      }
    }

    stage('Install Dependencies') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              python3 -m venv venv
              . venv/bin/activate
              python -m pip install --upgrade pip
              pip install -r requirements.txt
            '''
          } else {
            // Windows agent
            bat '''
              python -m venv venv
              call venv\\Scripts\\activate
              python -m pip install --upgrade pip
              pip install -r requirements.txt
            '''
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              . venv/bin/activate
              pytest --maxfail=1 --disable-warnings -q
            '''
          } else {
            bat '''
              call venv\\Scripts\\activate
              pytest --maxfail=1 --disable-warnings -q
            '''
          }
        }
      }
    }

    stage('Run App') {
      steps {
        script {
          if (isUnix()) {
            // start app in background with nohup and store pid
            sh '''
              . venv/bin/activate
              nohup python app.py > app.log 2>&1 & echo $! > app.pid
              echo "App started (pid=$(cat app.pid))"
            '''
          } else {
            // Windows: start as background process with START /B and save pid using tasklist
            bat '''
              call venv\\Scripts\\activate
              START /B python app.py > app.log 2>&1
              timeout /t 2 /nobreak >nul
              for /f "tokens=2 delims=," %%I in ('tasklist /fi "imagename eq python.exe" /fo csv /nh') do @echo %%I > app.pid || echo unknown > app.pid
              echo "App 'started' (app.pid created)"
            '''
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'app.log', allowEmptyArchive: true
      junit allowEmptyResults: true, testResults: '**/test-*.xml'  // optional if you produce junit xml
      echo "Pipeline finished. Check app.log and app.pid in workspace."
    }
    failure {
      echo "Build failed — see console and app.log for details."
    }
  }
}
