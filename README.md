# k8spython

-> .\flaskExample\myApp contains all the artifacts to copy in the docker image which will be generated

-> The myConfig file is the kubeconfig to authenticate to you K8S cluster. Open this file in a text editor to see the article to know how generate your kubeconfig.

-> .\flaskExample contains the Dockerfile and the YAML file to deploy to K8S. You have to be in this directory to do the docker build . -t imagename:tag

-> .\k0sclient conatins other artifacts\test that has been done used in building this POC

