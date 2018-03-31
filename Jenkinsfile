pipeline {
  agent {
    docker {
      image 'python:3'
      args '''-u root
-p 3000:3000'''
    }
    
  }
  stages {
    stage('Build') {
      steps {
        githubNotify context: 'Notification key', description: 'This is a shorted example',  status: 'PENDING'
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
      }
    }
    stage('Results') {
      steps {
        githubNotify context: 'Notification key', description: 'Woobata',  status: 'SUCCESS'
      }
    }
  }
}
