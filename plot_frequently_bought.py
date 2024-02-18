import argparse
import networkx as nx
import plotly.graph_objects as go
import os
import matplotlib.pyplot as plt
from src.plots.subgraph_plotly import plot_subgraph_plotly 
parser=argparse.ArgumentParser()
parser.add_argument('--graph_path', help='Path to the graph', default='graph.gml')
parser.add_argument('--product_dict_path', help='Path to the product dictionary', default='product_dict.json')
parser.add_argument('--output_path', help='Path to the output')
parser.add_argument('--center_node', help='Center node',default='PRD0903052')
args=parser.parse_args()
# Create a sample graph
G = nx.read_gml(args.graph_path)
# Define the query node
query_node = args.center_node

def subgraph_frequently_together(graph:nx.classes.graph.Graph, 
                                 center_node:str, 
                                 radius:int=1):
    """
    Construct a subgraph centered around a query node, including nodes that are frequently bought together
    with the query node within a given radius.

    Parameters:
    - graph (nx.classes.graph.Graph): The input graph.
    - center_node (str): The query node around which the subgraph will be centered.
    - radius (int): The radius within which to consider nodes as frequently bought together. Default is 1.

    Returns:
    - subgraph (nx.classes.graph.Graph): The subgraph containing the query node and nodes frequently bought together.
    """

    # Compute the maximum weight within radius 2 from the query node
    ego = nx.ego_graph(graph, center_node, radius=radius)
    max_weight = max(ego.edges[u, v]['weight'] for u, v in ego.edges())
    # Get the nodes with the largest weight within a radius
    nodes_with_max_weight = [center_node] + [node for node in ego.nodes() if any(ego.edges[node, neighbor]['weight'] >= max_weight for neighbor in ego.neighbors(node))]
    # Construct the subgraph
    subgraph = graph.subgraph(nodes_with_max_weight)
    return subgraph

# Construct the subgraph
radius = 3
subgraph = subgraph_frequently_together(G, query_node, radius=radius)
# Draw the subgraph
pos = nx.random_layout(subgraph)  # Use random layout
# Highlight the query node
plt.figure()
plt.title("Products within a radius of {} from node {}".format(radius,query_node))
nx.draw(subgraph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=1)
nx.draw_networkx_nodes(subgraph, pos, nodelist=[query_node], node_color='red', node_size=700)
plt.tight_layout()
# Display the plot
os.makedirs('visualization', exist_ok=True)
plt.savefig("visualization/subgraph.png")

def subgraph_top_nodes_with_largest_weights(graph, query_node, top_n=10):
    # Get the neighbors of the query node and their weights
    neighbor_weights = [(neighbor, graph.edges[query_node, neighbor]['weight']) for neighbor in graph.neighbors(query_node)]
    
    # Sort the neighbors by weight in descending order and get the top n
    top_nodes = [neighbor for neighbor, weight in sorted(neighbor_weights, key=lambda x: x[1], reverse=True)[:top_n]]
    
    # Construct the subgraph with the query node and top nodes
    nodes_of_interest = [query_node] + top_nodes
    subgraph = graph.subgraph(nodes_of_interest)
    
    return subgraph

# Get the neighbors of the query node and their weights
neighbor_weights = [(neighbor, G.edges[query_node, neighbor]['weight']) for neighbor in G.neighbors(query_node)]
top_10_nodes = sorted(neighbor_weights, key=lambda x: x[1], reverse=True)[:10]

# Print the top 10 nodes and their corresponding weights
print("Top 10 nodes with largest weights connected to node", query_node, ":")
for node, weight in top_10_nodes:
    print("Node:", node, "Weight:", weight)


subgraph = subgraph_top_nodes_with_largest_weights(G, query_node, top_n=10)
plot_subgraph_plotly(subgraph, query_node, args, radius=1)

degrees = dict(G.degree())

# Find the node with the maximum degree
most_connected_node = max(degrees, key=degrees.get)

print("Most connected node:", most_connected_node)
print("Degree:", degrees[most_connected_node])
