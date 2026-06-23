// Jenkinsfile Pipeline CI/CD SentimentAI
pipeline {
    agent any // S'exécute sur n'importe quel agent disponible
    
    environment {
        IMAGE_NAME = 'sentiment-ai'
        // Remplacer "VOTRE_PSEUDO" par ton identifiant GitHub exact (en minuscules)
        REGISTRY   = 'ghcr.io/l-sbiksla-l' 
        // Récupère le SHA court du commit pour un tag unique
        IMAGE_TAG  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }
    
    stages {
        // Stage 1: Récupération du code source
        stage('Checkout') {
            steps {
                checkout scm // Utilise la configuration Git du job Jenkins
                echo "Branche : ${env.BRANCH_NAME}"
                echo "Commit : ${env.GIT_COMMIT}"
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
                    echo 'Tests échoués ou coverage insuffisant (<70%)'
                }
            }
        }
        
        // Stage 4: Publication de l'image (uniquement sur la branche main)
        stage('Push') {
            when { branch 'main' }
            steps {
                // Syntaxe condensée sur une ligne pour éviter tout problème de parser Groovy
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
            // Nettoyer les conteneurs de test, qu'il y ait succès ou échec
            sh 'docker compose down -v 2>/dev/null || true'
        }
        success {
            echo "Pipeline réussi ! Image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline échoué. Consultez les logs ci-dessus.'
        }
    }
}
