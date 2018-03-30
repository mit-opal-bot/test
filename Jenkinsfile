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
'''
      }
    }
    stage('Pylint') {
      steps {
        sh 'pylint --output-format=parseable app.py || echo "pylint exited with $?"'
        step([
          $class: 'WarningsPublisher',
          canComputeNew: false,
          canResolveRelativePaths: false,
          consoleParsers: [[parserName: 'PyLint']],
          defaultEncoding: '',
          excludePattern: '',
          healthy: '',
          includePattern: '',
          messagesPattern: '',
          unHealthy: '0'])
      }
    }
  }
}