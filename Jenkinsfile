@Library('testSummary') _
import edu.mit.jenkins.Utils

utils = new Utils()

pipeline {
  agent any
  stages {
    // Build the images first
    stage('Build Docker images') {
      steps {
        // Set GitHub commits statuses
        githubNotify context: 'Docker images', description: 'Build in progress',  status: 'PENDING'
        githubNotify context: 'Python linter', description: 'Build in progress',  status: 'PENDING'
        githubNotify context: 'Functional tests', description: 'Build in progress',  status: 'PENDING'
        sh '''
          cd ${WORKSPACE}/stuff
          docker-compose build
        '''
        echo "${currentBuild.result}"
        echo "${currentBuild.currentResult}"
      }
      post {
        always {
          script {
            if (currentBuild.currentResult == 'SUCCESS') {
              description = 'Built successfully'
            } else {
              description = 'Failed to build'
            }
            status = utils.gitHubStatusForBuildResult(currentBuild.currentResult)
            githubNotify context: 'Docker images', description: description,  status: status
          }
        }
      }
    }
    stage('Spin up servers') {
      steps {
        // Use Docker Compose to spin up servers for functional testing.
        sh '''
          cd ${WORKSPACE}/stuff
          docker-compose up -d
          docker-compose exec -T app /bin/sh -c \'until [ $(curl -k -s -L -w "%{http_code}" -o /dev/null "http://app:5000") -eq 200 ]; do echo "Waiting..."; sleep 1; done; echo "app container is ready"\'
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
          docker.image('python:3-alpine').inside("--user=root --network=${compose_network}") {
            sh '''
              pip install pylint
              pip install -r stuff/app/requirements.txt
              pylint --output-format=parseable stuff || echo "pylint exited with $?"
            '''
          }
        }
        script {
          docker.image('python:3-alpine').inside("--user=root --network=${compose_network}") {
            sh '''
              cd stuff
              pip install -r features/requirements.txt
              pip freeze
              behave --junit --junit-directory reports || echo "behave exited with $?"
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
      script {
        echo utils.getTestSummary()
        summary = utils.getTestSummary()
        status = utils.gitHubStatusForBuildResult(currentBuild.currentResult)
        // Set GitHub commits statuses
        githubNotify context: 'Python linter', description: 'Build in progress',  status: status
        githubNotify context: 'Functional tests', description: summary,  status: status
        info = utils.warningsInfo()
        echo info
        echo info.description
      }
    }
    // Keep disk use down by deleting any dangling docker images older than 10 days.
    // docker image ls --force --filter "until=240h"
  }
}
