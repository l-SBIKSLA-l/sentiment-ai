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
        // Stage 1: Informations du code source
        stage('Checkout Info') {
            steps {
                script {
                    // Résout le problème du "detached HEAD" en cherchant le nom de la branche distante/locale liée au commit
                    env.ACTUAL_BRANCH = sh(script: "git name-rev --name-only HEAD | sed 's|remotes/origin/||' | sed 's|tags/||'", returnStdout: true).trim()
                }
                echo "Branche réelle détectée : ${env.ACTUAL_BRANCH}"
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
        
        // Stage 4: Publication de l'image (S'exécute uniquement sur la branche main)
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
            // Nettoyer les conteneurs et volumes de test résiduels pour éviter de saturer le serveur
            sh 'docker compose down -v 2>/dev/null || true'
        }
        success {
            echo "Pipeline réussi ! Image : ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline échoué. Consultez les logs ci-dessus.'
        }
    }
}
