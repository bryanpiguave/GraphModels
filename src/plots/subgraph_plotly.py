import networkx as nx
import plotly.graph_objects as go
import argparse
def plot_subgraph_plotly(graph:nx.classes.graph.Graph, 
                         center_node:str,
                         args, radius:int=1):
    # Extract subgraph nodes
     # Get layout
    layout = nx.spring_layout(graph)  # or any other layout algorithm you prefer
    
    # Create Plotly figure
    fig = go.Figure()

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
        color = f'rgb({int(255 * color_intensity)}, {int(255 * color_intensity)}, {int(255 * color_intensity)})'

        fig.add_trace(go.Scatter(x=[layout[u][0], layout[v][0]], y=[layout[u][1], layout[v][1]], mode='lines',
                                 line=dict(width=2, color=color),
                                 hoverinfo='text', 
                                 hovertext=f'Weight: {weight}'))
    for node in graph.nodes():
        if node == center_node:  # Highlight node of interest
            color = 'red'
            size = 15
        else:
            color = 'black'
            size = 10
        fig.add_trace(go.Scatter(x=[layout[node][0]], y=[layout[node][1]], mode='markers', 
                                 marker=dict(size=size, color=color),
                                 text=node, hoverinfo='text'))
    # Customize layout
    fig.update_layout(coloraxis=dict(colorscale='Viridis', colorbar=dict(title='Weight', ticks='outside', tickvals=[0, max_weight], ticktext=['0', str(max_weight)])))
    fig.update_layout(title=f"Subgraph centered around node {center_node}", showlegend=False, hovermode='closest')
    fig.update_xaxes(showgrid=False, zeroline=False, tickvals=[], ticktext=[])  # Hide gridlines, zeroline, and axis ticks
    fig.update_yaxes(showgrid=False, zeroline=False, tickvals=[], ticktext=[])
    # Show the plot
    if args.output_path:
        fig.write_html(args.output_path)
    else:
        fig.write_html("subgraph.html")
    fig.show()
    return 0

