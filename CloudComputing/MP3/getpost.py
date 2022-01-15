# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request 
from os import path, system
import json
#from yaml import *
from kubernetes import client, config
from k8tes import get_stuff
#import kubernetes
from pick import pick  # install pick using `pip install pick`

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
    #Configs can be set in Configuration class directly or using helper
    #utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    #v1 = client.BatchV1Api()
    print(v1)
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    podList = []
    for item in ret.items:
	    podDict = {"node":item.spec.node_name, "ip":item.status.pod_ip, "namespace":item.metadata.namespace, "name":item.metadata.name, "status":item.status.phase}
	    podList.append(podDict)
	    print(podDict)
    return podList

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
        dataset = request.get_json()
		#Create job based on dataset TYPE=ff DATASET=dataset  Quotas JOB_NAME
        a = system('/home/ec2-user/bin/kubectl create -f /home/ec2-user/free.yaml --namespace=free-service')
        #print(dataset, type(dataset))
        print(a, type(request))
        return "", 200
    else:
        return "", 406

@app.route('/img-classification/premium', methods = ['GET', 'POST'])
def premium():
	if(request.method == 'GET'):
		return "", 405
	elif(request.method == 'POST'):
		dataset = request.get_json()
		#CREATE job based on dataset TYPE=cnn DATASET= No quotas JOB_NAME
		a = system('/home/ec2-user/bin/kubectl create -f /home/ec2-user/premium.yaml')
        #print(dataset, type(dataset))
		print(a, type(request))
		return "", 200
	else:
		return "", 406
		
@app.route('/config', methods = ['GET', 'POST'])
def getconfig():
	if(request.method == 'GET'):
	    podList = get_all_pods()
	    podsDict = {"pods":podList}
	    print(podsDict)
	    return json.dumps(podsDict)
	else:
		return "", 406
	    

if __name__ == "__main__":
    app.run(host="0.0.0.0")