pipeline {
    agent any

    environment {
        IMAGE_NAME = "priyabratakhandual/rto-student-registration"
        APP_REPO = "https://github.com/priyabratakhandual/RTO.git"
        GITOPS_REPO = "https://github.com/priyabratakhandual/gitops.git"
    }

    stages {

        stage('Clone Application Repository') {
            steps {
                git branch: 'main',
                url: "${APP_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$BUILD_NUMBER .
                '''
            }
        }

        stage('DockerHub Login') {

            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {

            steps {

                sh '''
                docker push $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }

        stage('Update GitOps Repository') {

            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {

                    sh '''

                    rm -rf gitops

                    git clone https://$GIT_USER:$GIT_PASS@github.com/priyabratakhandual/gitops.git

                    cd gitops/rto

                    sed -i "s/tag:.*/tag: \\"$BUILD_NUMBER\\"/" values.yaml

                    git config user.email "jenkins@local"
                    git config user.name "jenkins"

                    git add values.yaml

                    git diff --cached --quiet || git commit -m "Update image tag to $BUILD_NUMBER"

                    git push origin main
                    '''
                }
            }
        }
    }

    post {

        success {
            echo 'CI/CD Pipeline Completed Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}