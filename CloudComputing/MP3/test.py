# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:16:24 2020

@author: frell
"""

from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
def get_stuff():
    config.load_kube_config()
    
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        
if __name__ == "__main__":
    get_stuff()