# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 14:45:10 2020

@author: frell
"""

import json
import boto3
from collections import defaultdict

class Graph:
    # Constructor
    def __init__(self, Table):
        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.table = Table
        
    # function to add an edge to graph
    def addEdge(self,u,v):
        self.graph[u].append(v) 

	# Function to print a BFS of graph
    def BFS(self, start): 
        # Mark all the vertices as not visited
        visited = [] 
        
        # Create a queue for BFS 
        queue = [(start, 0)]
        distance = 0
        
        while queue:
            # pop shallowest node (first node) from queue
            node = queue.pop(0)
            if node[0] not in visited:
                # add node to list of checked nodes
                visited.append(node[0])
                self.table.put_item(Item={'source': start, 'destination': node[0], 'distance': str(node[1])})
                neighbours = self.graph[node[0]]
 
                # add neighbours of node to queue
                for neighbour in neighbours:
                    queue.append((neighbour, node[1]+1))
                    

def parseGraph(Graph, jsonGraph):
	# ex: "Chicago->Urbana, Urbana->Springfield, Chicago->Lafayette"
    graphString = jsonGraph.split(',')

    cities = {}

    #Add cities to dictionary
    for nodes in graphString:
        nodeList = nodes.split('->')
        
        if (nodeList[0] in cities):
            cities[nodeList[0]] += 1
        else:
            cities[nodeList[0]] = 1
        
        if (nodeList[1] in cities):
            cities[nodeList[1]] += 1
        else:
            cities[nodeList[1]] = 1
            
        #Add each node to the graph
        Graph.addEdge(nodeList[0], nodeList[1])
    
    #Loop through each city to find distances to connected cities
    for city in cities:
        Graph.BFS(city)
        
        

def lambda_handler(event, context):
    # TODO implement
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('MP2_CS498')
    
    requestBody = event.get('graph')

    graph = Graph(table)
    parseGraph(graph, requestBody)

    return {
        'statusCode': 200,
        'body': json.dumps('Completed Graph')
    }

