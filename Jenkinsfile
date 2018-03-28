pipeline {
  agent {
    docker {
      image 'python:3'
      args '-p 3000:3000'
    }
    
  }
  stages {
    stage('Build') {
      steps {
        sh '''pip install --user flask
pip install --user behave
pip freeze'''
      }
    }
  }
}