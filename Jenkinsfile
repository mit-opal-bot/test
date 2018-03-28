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
        sh '''pip install flask behave pylint
ls -al
pwd
'''
      }
    }
    stage('Pylint') {
      steps {
        sh '''pwd
ls -al
pylint --output-format=parseable app.py > pylint.log || echo "pylint exited with $?"
cat pylint.log
'''
      }
    }
  }
}