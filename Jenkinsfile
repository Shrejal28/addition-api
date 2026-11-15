// Jenkinsfile - CI/CD Pipeline for Addition API (Git-based)
pipeline {
    agent any

    environment {
        PYTHON  = 'C:\\Users\\Shrejal\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        GIT_URL = 'https://github.com/Shrejal28/addition-api.git'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '=== Cloning from GitHub ==='
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/Shrejal28/addition-api.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '=== Installing Python dependencies ==='
                bat "\"${PYTHON}\" -m pip install fastapi \"uvicorn[standard]\" pydantic pytest httpx evidently pandas"
            }
        }

        stage('Lint') {
            steps {
                echo '=== Running flake8 linting ==='
                bat "\"${PYTHON}\" -m pip install flake8"
                bat "\"${PYTHON}\" -m flake8 main.py --max-line-length=120 || echo Lint warnings found"
            }
        }

        stage('Run Pytest') {
            steps {
                echo '=== Running Pytest ==='
                bat "if not exist reports mkdir reports"
                bat "\"${PYTHON}\" -m pytest test_main.py -v --tb=short --junitxml=reports\\test_results.xml"
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/test_results.xml'
                }
            }
        }

        stage('Generate Evidently Report') {
            steps {
                echo '=== Generating Evidently monitoring report ==='
                bat "\"${PYTHON}\" evidently_report.py"
            }
        }

        stage('Start FastAPI Smoke Test') {
            steps {
                echo '=== Running FastAPI smoke test ==='
                bat """
                    start /B \"${PYTHON}\" -m uvicorn main:app --host 127.0.0.1 --port 8001
                    timeout /t 8 /nobreak
                    curl -f http://127.0.0.1:8001/ && echo [OK] Health check passed || echo [WARN] Health check failed
                    curl -f \"http://127.0.0.1:8001/add?num1=10&num2=5\" && echo [OK] Add endpoint passed || echo [WARN] Add endpoint failed
                    for /f \"tokens=5\" %%a in ('netstat -aon ^| findstr :8001') do taskkill /F /PID %%a 2>nul || echo Server stopped
                """
            }
        }

        stage('Archive Reports') {
            steps {
                echo '=== Archiving reports ==='
                archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo '✅ Addition API pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
        always {
            echo '=== Pipeline finished ==='
        }
    }
}
