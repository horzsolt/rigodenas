pipeline {
  options {
    buildDiscarder(logRotator(numToKeepStr: '10')) // Retain history on the last 10 builds
    ansiColor('xterm')
    timestamps() // Append timestamps to each line
    timeout(time: 20, unit: 'MINUTES') // Set a timeout on the total execution time of the job
  }
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Setup') {
      steps {
        script {
          sh """
          pip install -r requirements.txt
          """
        }
      }
    }
    stage('Linting') {
      steps {
        script {
          sh """
          pylint **/*.py
          """
        }
      }
    }
    stage('Unit Testing') {
      steps {
        script {
          sh """
          python -m unittest discover -s tests/unit
          """
        }
      }
    }
  }
  post {
    success {  
      mail body: "<b>Example</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: '', charset: 'UTF-8', mimeType: 'text/html', subject: "SUCCESS CI: Project name -> ${env.JOB_NAME}", to: "horzsolt2006@gmail.com";  
    }  
    failure {  
      mail body: "<b>Example</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: '', charset: 'UTF-8', mimeType: 'text/html', subject: "ERROR CI: Project name -> ${env.JOB_NAME}", to: "horzsolt2006@gmail.com";
    }      
  }
}