pipeline {
  agent any
  stages {
    stage('Build Docker images') {
      // Build the images before doing anything else
      steps {
        sh 'printenv'
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
          def potato = sh returnStdout: true, script: 'echo potatoes'
          println potato
          def compose_container = sh returnStdout: true, script: 'docker-compose ps -q | head -n 1'
          println compose_container
          def compose_network = sh returnStdout: true, script: 'docker inspect \$COMPOSE_CONTAINER -f \'{{range \$key, \$value := .NetworkSettings.Networks}}{{printf "%s" \$key}}{{end}}\''
          println compose_network
        }
        // sh """
        //   docker-compose ps -q | head -n 1
        //   COMPOSE_CONTAINER=\$(docker-compose ps -q | head -n 1)
        //   COMPOSE_NETWORK=\$(docker inspect \$COMPOSE_CONTAINER -f \'{{range \$key, \$value := .NetworkSettings.Networks}}{{printf "%s" \$key}}{{end}}\')
        //   echo \$COMPOSE_CONTAINER
        //   echo \$COMPOSE_NETWORK
        // """
        // Run tests
        // e.g. docker run --network $COMPOSE_NET --network-alias test python:3
        // docker.image('python:3').inside("--network=${COMPOSE_NETWORK}")
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
