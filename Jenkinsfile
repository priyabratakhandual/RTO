pipeline {
    agent any

    environment {

        AWS_REGION = 'ap-south-1'
        ACCOUNT_ID = '953472632969'

        ECR_REPOSITORY = 'myapp'
        EKS_CLUSTER_NAME = 'my-eks-cluster'

        IMAGE_TAG = "${BUILD_NUMBER}"

        SECRET_NAME = 'rto-app-secret'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                -t myapp:$IMAGE_TAG .
                '''
            }
        }

        stage('Login To ECR') {
            steps {
                sh '''
                aws ecr get-login-password \
                --region $AWS_REGION | \
                docker login \
                --username AWS \
                --password-stdin \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Push To ECR') {
            steps {
                sh '''
                docker tag \
                myapp:$IMAGE_TAG \
                $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/myapp:$IMAGE_TAG

                docker push \
                $ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/myapp:$IMAGE_TAG
                '''
            }
        }

        stage('Configure EKS') {
            steps {
                sh '''
                aws eks update-kubeconfig \
                --region $AWS_REGION \
                --name $EKS_CLUSTER_NAME
                '''
            }
        }

        stage('Create Kubernetes Secret') {
            steps {
                sh '''
                aws secretsmanager get-secret-value \
                --secret-id $SECRET_NAME \
                --region $AWS_REGION \
                --query SecretString \
                --output text > .env

                kubectl delete secret student-registration-secret \
                --ignore-not-found

                kubectl create secret generic \
                student-registration-secret \
                --from-env-file=.env
                '''
            }
        }

        stage('Deploy To EKS') {
            steps {
                sh '''

                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml

                kubectl set image deployment/student-registration \
                student-registration=$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/myapp:$IMAGE_TAG

                kubectl rollout status deployment/student-registration
                '''
            }
        }

    }

    post {

        success {
            echo 'Deployment Successful'
        }

        failure {
            echo 'Deployment Failed'
        }
    }
}