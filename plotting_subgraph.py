import argparse
import networkx as nx
import plotly.graph_objects as go
import json
import matplotlib.pyplot as plt
parser=argparse.ArgumentParser()
parser.add_argument('--graph_path', help='Path to the graph', default='graph.gml')
parser.add_argument('--product_dict_path', help='Path to the product dictionary', default='product_dict.json')
parser.add_argument('--output_path', help='Path to the output', default='subgraph.html')
parser.add_argument('--center_node', help='Center node')
args=parser.parse_args()

def plot_subgraph_plotly(graph, center_node, radius=1):
    # Extract subgraph nodes
    subgraph_nodes = nx.single_source_shortest_path_length(graph, center_node, radius)
    subgraph = graph.subgraph(subgraph_nodes)
    
    # Get layout
    layout = nx.spring_layout(subgraph)  # or any other layout algorithm you prefer
    
    # Create Plotly figure
    fig = go.Figure()

    # Add nodes to the plot
    for node in subgraph.nodes():
        if node == center_node:  # Highlight node of interest
            color = 'red'
            size = 15
        else:
            color = 'skyblue'
            size = 10
        fig.add_trace(go.Scatter(x=[layout[node][0]], y=[layout[node][1]], mode='markers', 
                                 marker=dict(size=size, color=color),
                                 text=node, hoverinfo='text'))

    # Add edges to the plot
    for u, v in subgraph.edges():
        fig.add_trace(go.Scatter(x=[layout[u][0], layout[v][0]], y=[layout[u][1], layout[v][1]], mode='lines',
                                 line=dict(width=1, color='gray'),
                                 hoverinfo='none'))

    # Customize layout
    fig.update_layout(title=f"Subgraph centered around node {center_node}", showlegend=False, hovermode='closest')
    fig.update_xaxes(showgrid=False, zeroline=False)  # Hide gridlines and zeroline
    fig.update_yaxes(showgrid=False, zeroline=False)

    # Show the plot
    fig.write_html(args.output_path)
    fig.show()
    return 0





def main():
    graph = nx.read_gml(args.graph_path)
    with open(args.product_dict_path, 'r') as f:
        product_dict = json.load(f)
    # Select a subgraph
    if args.center_node:
        if args.center_node not in graph.nodes():
            print(f"Node {args.center_node} not in the graph")
            return
        else:
            plot_subgraph_plotly(graph, args.center_node, 1)
    else:
        print("No center node specified")
    return

if __name__=="__main__":
    main()