pipeline {
  agent any
  stages {
    stage('Build Docker images') {
      // Build the images before doing anything else
      steps {
        sh '''
          cd ${WORKSPACE}/stuff
          docker-compose build
        '''
      }
    }
    stage('Spin up servers') {
      steps {
        // Use Docker Compose to spin up servers for functional testing.
        sh '''
          cd ${WORKSPACE}/stuff
          docker-compose up -d
          docker-compose exec -T app /bin/bash -c \'until [ $(curl -k -s -L -w "%{http_code}" -o /dev/null "http://app:5000") -eq 200 ]; do echo "Waiting..."; sleep 1; done; echo "app container is ready"\'
        '''
        // Divine the network name just created by docker compose.
        script {
          compose_container = sh (returnStdout: true, script: """
            cd ${WORKSPACE}/stuff && docker-compose ps -q | head -n 1
          """).trim()
          compose_network = sh (returnStdout: true, script: """
            cd ${WORKSPACE}/stuff
            docker inspect ${compose_container} -f \'{{range \$key, \$value := .NetworkSettings.Networks}}{{printf \"%s\" \$key}}{{end}}\'
          """).trim()
          echo "Docker Compose network is ${compose_network}."
          // Run tests
          // e.g. docker run --network $COMPOSE_NET --network-alias test python:3
          docker.image('python:3').inside("--user=root --network=${compose_network}") {
            sh '''
              cd stuff
              pip install -r features/requirements.txt
              pip freeze
              behave
              chown -R 1000:1000 *
            '''
          }
        }
      }
    }
    stage('Run tests') {
      steps {
        echo "Docker Compose network is still ${compose_network}."
      }
    }
  }
  post {
    always {
      // Make sure to shut down and remove containers, volumes, and networks
      // created by this run.
      sh '''
        cd ${WORKSPACE}/stuff
        docker-compose down -v
      '''
    }
    // If this build failed, delete the Docker images it built.
    // If this build succeeded, keep its Docker images but delete any older
    // saved versions of those images.
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
