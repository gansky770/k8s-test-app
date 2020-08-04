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
     }
   }
    
   stage('MERGE  to master branch') {
     checkout scm 
     withCredentials([usernamePassword(credentialsId: 'git', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) 
  // available as an env variable, but will be masked if you try to print it out any which way
  // note: single quotes prevent Groovy interpolation; expansion is by Bourne Shell, which is what you want
     sh 'echo $PASSWORD'
  // or inside double quotes for string interpolation
     echo "username is $USERNAME"
}
     //git branch: 'origin/master', credentialsId: 'git', url: 'ssh://git@github.com:gansky770/k8s-test-app.git'
     sh "git config --global user.email 'gansky.m@gmail.com'"
     sh "git config --global user.name 'gansky770'"
     sh "git checkout --force master"
     sh "git merge origin/development"
     //sh "git add ."
     //sh "git commit -m 'Merge development to master' "
     sh "git push -u origin master --force --verbose" 
     }
 }      
