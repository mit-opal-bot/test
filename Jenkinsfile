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
        sh 'behave --junit --junit-output reports'
      }
    }
  }
}