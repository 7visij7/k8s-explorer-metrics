pipeline {
  agent any
  environment {
    REGISTRY = 'registry.company.com'
    REGCREDS = 'registry-admin-jenkins'
    KUBECONFIG_OMEGA = '/home/jenkins/.omega.k8s.company.com'
    KUBECONFIG_LUCILE = '/home/jenkins/.lucile.k8s.company.com'
    KUBECONFIG_CHARLIE = '/home/jenkins/.charlie.k8s.company.com'
    IMAGE_NAME = 'sre/explorer-metrics'
    PATCH = readFile 'kubectl.patch'
  }
  stages {
    stage('env') {
      steps {
        sh 'env'
      }
    }
    stage("build image") {
      steps {
        script {
          if(env.GIT_BRANCH =~ "master") {
            docker.withRegistry('https://' + env.REGISTRY, env.REGCREDS) {
              image = docker.build("${env.IMAGE_NAME}:${env.BUILD_ID}", "-f Dockerfile .")
              image.push()
            }
          }
        }
      }
    }
    stage("deploy to omega") {
      steps {
        script {
          if(env.GIT_BRANCH =~ "master") {
            sh "kubectl --kubeconfig=${env.KUBECONFIG_OMEGA} -n monitoring patch deployment metrics-app --patch \"${env.PATCH}\""
          }
        }
      }
    }
    stage("deploy to charlie") {
      steps {
        script {
          if(env.GIT_BRANCH =~ "master") {
            sh "kubectl --kubeconfig=${env.KUBECONFIG_CHARLIE} -n monitoring patch deployment metrics-app --patch \"${env.PATCH}\""
          }
        }
      }
    }
    stage("deploy to lucile") {
      steps {
        script {
          if(env.GIT_BRANCH =~ "master") {
            sh "kubectl --kubeconfig=${env.KUBECONFIG_LUCILE} -n monitoring patch deployment metrics-app --patch \"${env.PATCH}\""
          }
        }
      }
    }
  }
}
