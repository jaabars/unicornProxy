pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry.cslash.io/dev'
        IMAGE_NAME = 'glg-unicorn-proxy'
        DOCKER_CREDENTIALS_ID = 'harbor-dev-creds'
        KUBE_CONFIG_CREDENTIALS_ID = 'kubeconfig-credentials'
        KUBE_NAMESPACE = 'nlg'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDENTIALS_ID) {
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                    }
                }
            }
        }

        /* stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBE_CONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl apply -f deployment.yaml -n ${KUBE_NAMESPACE}
                        kubectl apply -f service.yaml -n ${KUBE_NAMESPACE}
                        kubectl set image deployment/fastapi-custom-report fastapi-custom-report=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        } */
    }
}
