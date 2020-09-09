#python
1.The application run in real nas mockup modes(configure via .env file)
2. insert accesskey to credentials file 
!!!! IMPORTANT encode your credentials file in secret.yaml (use https://www.base64encode.org/)
3. configure .env file for runtime ,mockup(true,false).
# jenkins
1.must instal plugins (github,docker,shagent,jobdsl,xmljobtodsl>>for converting piplines)
2. create credentials (dockerhub ,git >> must bu ssh >>create keypair with jenkins username )
#k8s
install helm 3 ( curl -L https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash) run >> 

helm install -name elk . --namespace=default