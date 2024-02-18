import networkx as nx
import plotly.graph_objects as go
import argparse
import os
from plotly.subplots import make_subplots

def plot_subgraph_plotly(graph:nx.classes.graph.Graph, 
                         center_node:str,
                         args, radius:int=1):
    # Extract subgraph nodes
     # Get layout
    layout = nx.spring_layout(graph)  # or any other layout algorithm you prefer
    
    # Create Plotly figure
    fig = make_subplots(rows=1, cols=2, column_widths=[0.7, 0.3], subplot_titles=("Graph", "Co-occurrence between items"))

    # Add nodes to the plot
    max_weight = float('-inf')  # Set to negative infinity to ensure any weight in the graph will be greater

    # Iterate over edges and update max_weight if a higher weight is found
    for u, v in graph.edges():
        edge_data = graph.get_edge_data(u, v)
        if edge_data is not None and 'weight' in edge_data:
            weight = edge_data['weight']
            max_weight = max(max_weight, weight)


    # Add edges to the plot
    for u, v in graph.edges():
        weight = graph.edges[u, v]['weight']
        color_intensity = weight/max_weight
        color = f'rgb({int(0 * color_intensity)}, {int(255 * color_intensity)}, {int(255 * color_intensity)})'

        fig.add_trace(go.Scatter(x=[layout[u][0], layout[v][0]], y=[layout[u][1], layout[v][1]], mode='lines',
                                 line=dict(width=2, color=color),
                                 hoverinfo='text'),
                                 row=1, col=1)
    for node in graph.nodes():
        if node == center_node:  # Highlight node of interest
            color = 'red'
            size = 15
            symbol = 'diamond-x'
        else:
            color = 'black'
            size = 10
            symbol = 'circle'
        fig.add_trace(go.Scatter(x=[layout[node][0]], y=[layout[node][1]], 
                                 mode='markers', name=node,
                                 marker=dict(size=size, color=color, 
                                             symbol=symbol),
                                 text=node, 
                                 hoverinfo='text'),
                                 row=1, col=1)
        

    # Add nodes to the list
    center_node_edges = list(graph.edges(center_node, data=True))  # Convert EdgeDataView to list

    # Sort edges by weight in descending order
    center_node_edges.sort(key=lambda x: x[2]['weight'], reverse=True)

    edge_weights_html = ""
    for edge in center_node_edges:
        neighbor = edge[1]
        weight = edge[2]['weight']
        edge_weights_html += f"{neighbor}: {weight}<br>"

    # Add the HTML content to the second subplot
    fig.add_trace(go.Scatter(x=[1], y=[1], mode='text', text=[edge_weights_html], showlegend=False), row=1, col=2)


    # Customize layout
    fig.update_layout(title=f"Retail items around product {center_node}", showlegend=False, hovermode='closest')
    fig.update_layout(height=600, width=800, font=dict(size=14))  # Adjust the font size as needed
    fig.update_xaxes(showgrid=False, zeroline=False, tickvals=[], ticktext=[])  # Hide gridlines, zeroline, and axis ticks
    fig.update_yaxes(showgrid=False, zeroline=False, tickvals=[], ticktext=[])
    # Show the plot
    if args.output_path:
        output_folder = os.path.dirname(args.output_path)
        if not os.path.exists(output_folder):
            print(f"Creating folder {output_folder}")
            os.makedirs(output_folder, exist_ok=True)
        fig.write_html(args.output_path)
    else:
        fig.write_html("subgraph.html")
    fig.show()
    return 0

