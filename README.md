###
 # Building a unifi Cloud Native logging facility FULL CYCLE - Python/CI/CD/HELM
 
 The stack we are are going to use are:
- [ECK] https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html
- Kibana 
- Filebeat 
## PYTHON APPLICATION
-  [BOTO]  collecting a number of EC2 instances running on  AWS Account (mockup Create random value from 1 to 50)
- The application run in real and mockup modes configure via: 
- - .env file
- - secret.yaml    
- - configmap.yaml
- Python application  will produce a log every 10 seconds(can be configure from .env) in infinity loop.


 
 ## K8S:
Created a helm package to package the application 
- ### !!!! IMPORTANT encode your credentials file in secret.yaml (use https://www.base64encode.org/)
- curl -L https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash) 

 ## JENKINS:
 #### preset:

- 1. must install plugins (github,docker,shagent,jobdsl,xmljobtodsl>>for converting piplines)
- 2. create credentials (dockerhub ,git >> must bu ssh >>create keypair with jenkins username )
#
 - Jenkins used to build on every push under branch development.
 - Image created with the number of the JENKINSBUILDNUMBER.
 - AUTO MERGE  to master branch.
 -  Updated  HELM chart to the latest IMAGE build NUMBER

## ARGO:
 - runs on every change that happens on  MASTER BRANCH.(WEBHOOK CONFIGURED)
