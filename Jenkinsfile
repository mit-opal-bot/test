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
        githubNotify context: 'Docker images', description: 'In progress...',  status: 'PENDING'
        githubNotify context: 'Python linter', description: 'In progress...',  status: 'PENDING'
        githubNotify context: 'Functional tests', description: 'In progress...',  status: 'PENDING'
        sh '''
          cd ${WORKSPACE}/stuff
          docker-compose build
        '''
      }
      post {
        always {
          script {
            if (currentBuild.currentResult == 'SUCCESS') {
              description = 'Images built successfully.'
            } else {
              description = 'Images failed to build.'
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
              cd stuff
              pip install pylint
              pip install -r app/requirements.txt
              pip install -r features/requirements.txt
              pylint --rcfile=${WORKSPACE}/.pylintrc --output-format=parseable app || echo "pylint exited with $?"
              behave --junit --junit-directory reports || echo "behave exited with $?"
              chown -R 1000:1000 reports
            '''
          }
        }
      }
    }
    stage('Collect results') {
      steps {
        // It appears the best Jenkins' plugins can do right now is say if
        // there are any warnings or errors at all. The diff results are
        // between runs of the same branch, so not useful when wanting to know
        // what the change will be if a PR is merged.
        //
        // It isn't easy to compare a pull request's results to its target
        // branch. See https://issues.jenkins-ci.org/browse/JENKINS-13056,
        // https://issues.jenkins-ci.org/browse/JENKINS-31812,
        // https://wiki.jenkins.io/display/JENKINS/Static+Analysis+in+Pipelines?focusedCommentId=133956792#comment-133956792.
        // It might be possible in version 3.0 of analysis-core-plugin when
        // that's ready.
        step([
          $class: 'WarningsPublisher',
          consoleParsers: [[parserName: 'PyLint']],
        ])
        junit '**/reports/*.xml'
        script {
          // PyLint commit status
          info = utils.warningsInfo()
          echo info.totalDescription
          echo info.diffDescription
          status = (info.total == 0) ? 'SUCCESS' : 'FAILURE'
          githubNotify context: 'Python linter', description: info.totalDescription,  status: status
        }
        script {
          // Functional test commit status 
          summary = utils.getTestSummary()
          status = utils.gitHubStatusForBuildResult(currentBuild.currentResult)
          githubNotify context: 'Functional tests', description: summary,  status: status
        }
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
    // Keep disk use down by deleting any dangling docker images older than 10 days.
    // docker image prune --force --filter "until=240h"
  }
}
