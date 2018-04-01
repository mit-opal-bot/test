pipeline {
  agent any
  stages {
    stage('Build Docker images') {
      steps {
        sh 'printenv'
        sh '''
          cd $WORKSPACE/stuff
          /usr/local/bin/docker-compose build
        '''
      }
    }
    stage('Spin up') {
      steps {
        sh '''
          cd $WORKSPACE/stuff
          /usr/local/bin/docker-compose up -d
          /usr/local/bin/docker-compose exec app /bin/bash -c 'until [ $(curl -k -s -L -w "%{http_code}" -o /dev/null "http://app:5000") -eq 200 ]; do echo "Waiting..."; sleep 1; done; echo "app container is ready"'
        '''
      }
    }
  }
  post {
    always {
      sh '''
        cd $WORKSPACE/stuff
        /usr/local/bin/docker-compose down -v
      '''
    }
  }
    // stage('Build') {
    //   steps {
    //     githubNotify context: 'Notification key', description: 'Chata',  status: 'PENDING'
    //     sh 'pip install flask behave pylint requests'
    //   }
    // }
    // stage('Pylint') {
    //   steps {
    //     sh 'pylint --output-format=parseable app.py || echo "pylint exited with $?"'
    //     step([
    //       $class: 'WarningsPublisher',
    //       consoleParsers: [[parserName: 'PyLint']],
    //     ])
    //   }
    // }
    // stage('Behave') {
    //   steps {
    //     sh 'behave --junit --junit-directory reports'
    //     sh 'rm -rf reports'
    //   }
    // }
    // stage('Results') {
    //   steps {
    //     githubNotify context: 'Notification key', description: 'Woobata',  status: 'SUCCESS'
    //   }
    // }

}
