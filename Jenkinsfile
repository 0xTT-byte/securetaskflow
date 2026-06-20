pipeline {

    agent any

    environment {
        IMAGE_NAME = "securetaskflow-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        GHCR_REPO  = "ghcr.io/0xTT-byte/securetaskflow"  // adjust to your actual GHCR path
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest tests/ -v'
            }
        }

        stage('Lint') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} ruff check app/'
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ghcr-creds', usernameVariable: 'GHCR_USER', passwordVariable: 'GHCR_TOKEN')]) {
                    sh '''
                        echo $GHCR_TOKEN | docker login ghcr.io -u $GHCR_USER --password-stdin
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${GHCR_REPO}:${IMAGE_TAG}
                        docker push ${GHCR_REPO}:${IMAGE_TAG}
                    '''
                }
            }
        }
    }
}
