from pyspark import *
from pyspark.sql import SparkSession
from graphframes import *

sc = SparkContext()
spark = SparkSession.builder.appName('fun').getOrCreate()


def get_connected_components(graphframe):
    # TODO:
    # get_connected_components is given a graphframe that represents the given graph
    # It returns a list of lists of ids.
    # For example, [[a_1, a_2, ...], [b_1, b_2, ...], ...]
    # then a_1, a_2, ..., a_n lie in the same component,
    # b_1, b2, ..., b_m lie in the same component, etc
    result = graphframe.connectedComponents().select('component', 'id').rdd.groupByKey().map(list).collect()
    
    node_list = []
    for node in result:
        node_list.append(v for v in node[1])

    return node_list    


if __name__ == "__main__":
    vertex_list = []
    edge_list = []
    with open('dataset/graph.data') as f:  # Do not modify
        for line in f:
            nodes = line.split()
            src = nodes[0]  # TODO: Parse src from line
            dst_list = list(nodes[1:])  # TODO: Parse dst_list from line
            vertex_list.append((src,))
            edge_list += [(src, dst) for dst in dst_list]

    vertices = spark.createDataFrame(vertex_list, ["id"])  # TODO: Create vertices dataframe
    edges = spark.createDataFrame(edge_list, ["src", "dst"])  # TODO: Create edges dataframe

    g = GraphFrame(vertices, edges)
    sc.setCheckpointDir("/tmp/connected-components")

    result = get_connected_components(g)
    for line in result:
        print(' '.join(line))