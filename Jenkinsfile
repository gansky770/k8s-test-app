node {
   def commit_id
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
     }
   }
    
   stage('MERGE  to master branch') {
     checkout scm 
     credentialsId:'jenkins-labs'
     
    //  sh"git config --global user.email "you@example.com" " "
    //  sh"git config --global user.name "Your Name" "
     sh "git merge origin/master origin/development"
     sh "git push origin master"
     }
 }      
