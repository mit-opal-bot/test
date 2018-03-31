pipeline {
  agent {
    docker {
      image 'python:3'
      args '''-u root'''
    }
    
  }
  stages {
    stage('Build') {
      steps {
        sh 'printenv'
        // githubNotify context: 'Notification key', description: 'Chata',  status: 'PENDING'
        sh 'pip install flask behave pylint requests'
      }
    }
    stage('Pylint') {
      steps {
        sh 'pylint --output-format=parseable app.py || echo "pylint exited with $?"'
        step([
          $class: 'WarningsPublisher',
          consoleParsers: [[parserName: 'PyLint']],
        ])
      }
    }
    stage('Behave') {
      steps {
        sh 'behave --junit --junit-directory reports'
        sh 'rm -rf reports'

      }
    }
    stage('Results') {
      steps {
        // githubNotify context: 'Notification key', description: 'Woobata',  status: 'SUCCESS'
      }
    }
  }
}
