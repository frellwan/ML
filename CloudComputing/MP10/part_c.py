from pyspark import *
from pyspark.sql import SparkSession
from graphframes import *

sc = SparkContext()
spark = SparkSession.builder.appName('fun').getOrCreate()


def get_shortest_distances(graphframe, dst_id):
    # TODO
    # Find shortest distances in the given graphframe to the vertex which has id `dst_id`
    # The result is a dictionary where key is a vertex id and the corresponding value is
    # the distance of this node to vertex `dst_id`.
    shortestPath = graphframe.shortestPaths(landmarks=[dst_id])
    rdd = shortestPath.select('id', 'distances').sort('id').rdd.collect()

    paths = {}
    for row in rdd:
        if len(row[1]) > 0:
            paths[row[0]] = row[1].popitem()[1]
        else:
            paths[row[0]] = -1

    return paths


if __name__ == "__main__":
    vertex_list = []
    edge_list = []
    with open('dataset/graph.data') as f:
        for line in f:
            # TODO: Parse line to get vertex id
            nodes = line.split()
            src = nodes[0]  
            dst_list = list(nodes[1:]) 

            # TODO: Parse line to get ids of vertices that src is connected to
            dst_list = list(nodes[1:])  
            vertex_list.append((src,))
            edge_list += [(src, dst) for dst in dst_list]

    vertices = spark.createDataFrame(vertex_list, ["id"])  # TODO: Create dataframe for vertices
    edges = spark.createDataFrame(edge_list, ["src", "dst"])  # TODO: Create dataframe for edges

    g = GraphFrame(vertices, edges)
    sc.setCheckpointDir("/tmp/shortest-paths")

    # We want the shortest distance from every vertex to vertex 1
    for k, v in get_shortest_distances(g, '1').items():
        print(k, v)