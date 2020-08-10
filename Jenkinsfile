node {
   stage('chekout scm') {
     checkout scm 
     sh "git rev-parse --abbrev-ref HEAD > GIT_BRANCH"                        
     git_branch = readFile('GIT_BRANCH').trim()
     echo git_branch

     
   }
   
  //  stage('sonarqube server') {
  //     //checkout scm
  // sh "docker-compose up  -d" 
  //   }
  
   
   stage('docker build/push ') {
    //sh 'sleep 2m'
     docker.withRegistry('https://index.docker.io/v1/','dockerhub') {
       //def app = docker.build("gansky/k8stest:${BUILD_NUMBER}", '--network k8stest-pipeline_sonarnet .').push()
       def app = docker.build("gansky/k8stest:${BUILD_NUMBER}", '.').push()
        
     }
   }
   
   
   
    
   stage('MERGE  to master branch') {
      cleanWs()
      checkout scm
      sh "cat /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/values.yaml"
      sh "sed '/imagetag/d' /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/values.yaml > /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/temp.yaml  "
      sh "echo imagetag: ${BUILD_NUMBER} >> /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/temp.yaml"
      sh "cat /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/temp.yaml > /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/values.yaml"
      sh "cat /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/values.yaml"
      sh "rm /var/jenkins_home/workspace/k8stest-pipeline/helm-k8s-test-app/temp.yaml"

         
      script {
                    sshagent(credentials:['git']) {
                        sh """
                            git config user.email "ci-user@email.com"
                            git config user.name "Jenkins"
                            git add .
                            git commit -m 'push development'
                            // git push  -u origin HEAD:development 
                            git checkout master
                            git merge development
                            git push  -u origin master 
                        """
                    }
                }
    //cleanWs()
    //checkout scm
      
    //  sh "git config --global user.email 'gansky.m@gmail.com'"
    //  sh "git config --global user.name 'Jenkins'"
    //  //sh "git remote add origin git@github.com:gansky770/k8s-test-app.git"
    //  sh "git checkout --force master"
    //  sh "git merge origin/development"
    //  //sh "git add ."
    //  //sh "git commit -m 'Merge development to master' "
    //  sh "git push -u origin master --force --verbose" 
     }
 }      
