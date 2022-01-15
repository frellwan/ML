# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:48:53 2020

@author: frell
"""

# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request 
from os import path, system
import json
#from yaml import *
from kubernetes import client, config
from k8tes import get_stuff
#import kubernetes
#from pick import pick  # install pick using `pip install pick`

def get_all_pods():
    #from kubernetes import client, config
    #contexts, active_context = config.list_kube_config_contexts()
    #if not contexts:
    #    print("Cannot find any context in kube-config file.")
    #    return
    #contexts = [context['name'] for context in contexts]
    #active_index = contexts.index(active_context['name'])
    #option, _ = pick(contexts, title="Pick the context to load",
    #                 default_index=active_index)
    # Configs can be set in Configuration class directly or using helper
    # utility
    config.load_kube_config()

    #v1 = client.CoreV1Api()
    #print(v1)
    print("Listing pods with their IPs:")
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    #podList = []
    #for item in ret.items:
	#    podString = '"node": "{}", "ip":"{}", "namespace":"{}", "name":"{}", "status":"{}"'
	#    podList.append(podString.format(item.spec.node_name, item.status.pod_ip, item.metadata.namespace, item.metadata.name, item.status.phase))
	
    #return podList




def create_job_object(podName, jobType):
    # Configureate Pod template container
    container = client.V1Container(
        name=podName,
        image="frellwan/cs498:mp3",
        command=["docker", "container", "run", "frellwan/cs498:mp3"])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": jobType}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=podName), spec=spec)

    return job


def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace="default")
    print("Job created. status='%s'" % str(api_response.status))


#Creatinf Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/img-classification/free', methods = ['GET', 'POST']) 
def free(): 
    if(request.method == 'GET'):
        return "", 405
    elif(request.method == 'POST'):
        job = create_job_object()
        
		#Create job based on dataset TYPE=ff DATASET=dataset  Quotas JOB_NAME
        system('/home/ec2-user/bin/kubectl create -f /users/ec2-user/free.yaml --namespace=free-service')
        return "", 200
    else:
        return "", 406

@app.route('/img-classification/premium', methods = ['GET', 'POST'])
def premium():
    if(request.method == 'GET'):
        return "", 405
    elif(request.method == 'POST'):
        job = create_job_object()
        create_job(batch_v1, job)
        #CREATE job based on dataset TYPE=cnn DATASET= No quotas JOB_NAME
        a = system('/home/ec2-user/bin/kubectl create -f /users/ec2-user/premium.yaml')
        
        #print(dataset, type(dataset))
        print(a, type(request))
        return "", 200
    else:
        return "", 406
		
@app.route('/config', methods = ['GET', 'POST'])
def config():
	if(request.method == 'GET'):
	    podList = get_stuff()
		
	    return "jsonify(podList)"
	else:
		return "", 406
	    

if __name__ == "__main__":
    config.load_kube_config()
    batch_v1 = client.BatchV1Api()
    app.run(host="0.0.0.0", port=80)