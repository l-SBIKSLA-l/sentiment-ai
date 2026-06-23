// Jenkinsfile Pipeline CI/CD SentimentAI
pipeline {
    agent any // S'exécute sur n'importe quel agent disponible [cite: 471]
    
    environment {
        IMAGE_NAME = 'sentiment-ai' [cite: 474]
        // Remplacer "VOTRE_PSEUDO" par ton identifiant GitHub exact (en minuscules) 
        REGISTRY   = 'ghcr.io/l-SBIKSLA-l' 
        // Récupère le SHA court du commit pour un tag unique [cite: 477, 478]
        IMAGE_TAG  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }
    
    stages {
        // Stage 1: Récupération du code source [cite: 503]
        stage('Checkout') {
            steps {
                checkout scm // Utilise la configuration Git du job Jenkins [cite: 505, 508]
                echo "Branche : ${env.BRANCH_NAME}" [cite: 509, 511]
                echo "Commit : ${env.GIT_COMMIT}" [cite: 512, 514]
                sh 'git log --oneline -5' [cite: 515, 516]
            }
        }
        
        // Stage 2: Analyse de la syntaxe Python (Fail Fast) [cite: 519, 521]
        stage('Lint') {
            steps {
                sh '''
                docker run --rm \
                  --volumes-from jenkins \
                  -w $WORKSPACE \
                  python:3.12-slim \
                  sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"
                ''' [cite: 527, 528, 529, 530, 531]
            }
        }
        
        // Stage 3: Construction de l'image et exécution des tests [cite: 545, 547]
        stage('Build & Test') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ." [cite: 551]
                sh """
                docker run --rm \
                  ${IMAGE_NAME}:${IMAGE_TAG} \
                  pytest tests/ -v \
                  --cov src \
                  --cov-report=xml:coverage.xml \
                  --cov-report term-missing \
                  --cov-fail-under 70
                """ [cite: 552, 553, 554, 555, 556, 557, 558]
            }
            post {
                failure {
                    echo 'Tests échoués ou coverage insuffisant (<70%)' [cite: 562]
                }
            }
        }
        
        // Stage 4: Publication de l'image (uniquement sur la branche main) [cite: 569, 570]
        stage('Push') {
            when { branch 'main' } [cite: 572]
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) { [cite: 574, 575, 576]
                    sh "echo \$REGISTRY_PASS | docker login ghcr.io -u \$REGISTRY_USER --password-stdin" [cite: 580, 581]
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}" [cite: 582]
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:latest" [cite: 583, 584]
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:latest" [cite: 585]
                }
            }
        }
    }
    
    post {
        always {
            // Nettoyer les conteneurs de test, qu'il y ait succès ou échec [cite: 483, 485]
            sh 'docker compose down -v 2>/dev/null || true' [cite: 485]
        }
        success {
            echo "Pipeline réussi ! Image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}" [cite: 486, 488]
        }
        failure {
            echo 'Pipeline échoué. Consultez les logs ci-dessus.' [cite: 490, 491]
        }
    }
}
