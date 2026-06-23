// Jenkinsfile Pipeline CI/CD SentimentAI
pipeline {
    agent any // S'exécute sur n'importe quel agent disponible
    
    environment {
        IMAGE_NAME = 'sentiment-ai'
        REGISTRY   = 'ghcr.io/l-sbiksla-l' 
        // Récupère le SHA court du commit pour un tag unique
        IMAGE_TAG  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }
    
    stages {
        // Stage 1: Informations du code source (Le téléchargement est géré automatiquement par Jenkins)
        stage('Checkout Info') {
            steps {
                // Version robuste pour récupérer le nom de la branche réelle, même si env.BRANCH_NAME est null
                script {
                    env.ACTUAL_BRANCH = sh(script: "git rev-parse --abbrev-ref HEAD", returnStdout: true).trim()
                }
                echo "Branche détectée : ${env.ACTUAL_BRANCH}"
                echo "Commit ID : ${IMAGE_TAG}"
                sh 'git log --oneline -5'
            }
        }
        
        // Stage 2: Analyse de la syntaxe Python (Fail Fast)
        stage('Lint') {
            steps {
                sh '''
                docker run --rm \
                  --volumes-from jenkins \
                  -w $WORKSPACE \
                  python:3.12-slim \
                  sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"
                '''
            }
        }
        
        // Stage 3: Construction de l'image et exécution des tests
        stage('Build & Test') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh """
                docker run --rm \
                  ${IMAGE_NAME}:${IMAGE_TAG} \
                  pytest tests/ -v \
                  --cov src \
                  --cov-report=xml:coverage.xml \
                  --cov-report term-missing \
                  --cov-fail-under 70
                """
            }
            post {
                failure {
                    echo 'Tests échoués ou couverture de code insuffisante (<70%)'
                }
            }
        }
        
        // Stage 4: Publication de l'image (uniquement si on est sur la branche main)
        stage('Push') {
            when {
                expression { return env.ACTUAL_BRANCH == 'main' }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_PASS')]) {
                    sh "echo \$REGISTRY_PASS | docker login ghcr.io -u \$REGISTRY_USER --password-stdin"
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:latest"
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:latest"
                }
            }
        }
    }
    
    post {
        always {
            // Nettoyer les conteneurs et volumes de test résiduels
            sh 'docker compose down -v 2>/dev/null || true'
        }
        success {
            echo "Pipeline réussi ! Image poussée si sur main : ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline échoué. Consultez les logs ci-dessus.'
        }
    }
}