pipeline {
  agent any
  stages {
    stage('Build Docker images') {
      // Set GitHub commits statuses
      githubNotify context: 'Docker images', description: 'Build in progress',  status: 'PENDING'
      githubNotify context: 'Python linter', description: 'Build in progress',  status: 'PENDING'
      githubNotify context: 'Functional tests', description: 'Build in progress',  status: 'PENDING'
      // Build the images first
      steps {
        sh '''
          cd ${WORKSPACE}/stuff
          docker-compose build
        '''
        echo "${currentBuild.result}"
        echo "${currentBuild.currentResult}"
        echo "${currentBuild}"
      }
      post {
        success {
          githubNotify context: 'Docker images', description: 'Build in progress',  status: 'SUCCESS'
        }
        failure {
          githubNotify context: 'Docker images', description: 'Build in progress',  status: 'FAILURE'
        }
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
        }
      }
    }
    stage('Run tests') {
      steps {
        // Add containers to compose network so containers can find each other.
        // Override user to the image's default of root because Jenkins
        // overrides all Docker users to the jenkins user (1000:1000).
        // Chown any created files to the jenkins user so it can read them
        // after tests have completed.
        script {
          docker.image('python:3').inside("--user=root --network=${compose_network}") {
            sh '''
              pip install pylint
              pylint --output-format=parseable stuff || echo "pylint exited with $?"
            '''
          }
        }
        script {
          docker.image('python:3').inside("--user=root --network=${compose_network}") {
            sh '''
              cd stuff
              pip install -r features/requirements.txt
              pip freeze
              behave --junit --junit-directory reports
              chown -R 1000:1000 reports
            '''
          }
        }
      }
    }
    stage('Collect results') {
      steps {
        step([
          $class: 'WarningsPublisher',
          consoleParsers: [[parserName: 'PyLint']],
        ])
        junit '**/reports/*.xml'
        sh 'printenv'
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
      // Set GitHub commits statuses
      githubNotify context: 'Python linter', description: 'Build in progress',  status: "${currentBuild.currentResult}"
      githubNotify context: 'Functional tests', description: 'Build in progress',  status: "${currentBuild.currentResult}"

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
