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
        sh '''python --version
docker-compose exec -T app /bin/bash -c \'until [ $(curl -k -s -L -w "%{http_code}" -o /dev/null "http://app:5000") -eq 200 ]; do echo "Waiting..."; sleep 1; done; echo "app container is ready"\'
'''
        pwd()
      }
    }
  }
}