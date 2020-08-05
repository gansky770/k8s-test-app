node {
   stage('chekout scm') {
     checkout scm 
     sh "git rev-parse --abbrev-ref HEAD > GIT_BRANCH"                        
     git_branch = readFile('GIT_BRANCH').trim()
     echo git_branch

     
   }
   
  //  stage('sonarqube server') {
  //     //checkout scm
  //     sh "docker-compose up  -d" 
  //   }
  
   
   stage('docker build/push') {
    //sh 'sleep 2m'
     docker.withRegistry('https://index.docker.io/v1/','dockerhub') {
       //def app = docker.build("gansky/k8stest:${BUILD_NUMBER}", '--network k8stest-pipeline_sonarnet .').push()
       def app = docker.build("gansky/k8stest:${BUILD_NUMBER}", '.').push()
       sh "export TAG=${BUILD_NUMBER}" 
       sh " printenv | sort "
       sh "env"
        
     }
   }
   
   
   
    
   stage('MERGE  to master branch') {
      cleanWs()
      checkout scm
      script {
                    sshagent(['git']) {
                        sh """
                            git config user.email "ci-user@email.com"
                            git config user.name "Jenkins"
                            git tag -a "v${env.DEPLOY_VERSION}" \
                                -m "Generated by: ${env.JENKINS_URL}" \
                                -m "Job: ${env.JOB_NAME}" \
                                -m "Build: ${env.BUILD_NUMBER}" \
                                -m "Env Branch: ${env.BRANCH_NAME}"
                            git push origin "v${env.DEPLOY_VERSION}"
                        """
                    }
                }
    //cleanWs()
    //checkout scm
      
     //sh "git config --global user.email 'gansky.m@gmail.com'"
     //sh "git config --global user.name 'Jenkins'"
     //sh "git checkout --force master"
     //sh "git merge origin/development"
     //sh "git add ."
    // sh "git commit -m 'Merge development to master' "
     //sh "git push -u origin master --force --verbose" 
     }
 }      
