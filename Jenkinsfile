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
   
    stage('Push') {
        environment { 
            GIT_AUTH = credentials('git') 
        }
        steps {
            sh('''
                git config --local credential.helper "!f() { echo username=\\$GIT_AUTH_USR; echo password=\\$GIT_AUTH_PSW; }; f"
                git push origin HEAD:$TARGET_BRANCH
            ''')
        }
    }
   
    
   stage('MERGE  to master branch') {
    checkout scm 
     //git branch: 'origin/development', credentialsId: 'git', url: 'https://github.com/gansky770/k8s-test-app.git'
     sh "git config --global user.email 'gansky.m@gmail.com'"
     sh "git config --global user.name 'gansky770'"
     sh "git checkout --force master"
     sh "git merge origin/development"
     //sh "git add ."
     //sh "git commit -m 'Merge development to master' "
     sh "git push -u origin master --force --verbose" 
     }
 }      
