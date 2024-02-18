import networkx as nx
from itertools import permutations
import json
import pandas as pd
import argparse
"""
    The purpose of this file is to build a graph from the Dunnhumby dataset.
"""

parser=argparse.ArgumentParser()
parser.add_argument('--data_path', help='Path to the dataset', default='data/transactions_200626.csv')
parser.add_argument('--output_path', help='Path to save the graph', default='graph.gml')
parser.add_argument('--product_dict_path', help='Path to save the product dictionary', default='product_dict.json')
args=parser.parse_args()


def main():
    # Load the dataset
    dataset = pd.read_csv(args.data_path)
    
    # Getting unique products
    products = dataset["PROD_CODE"].unique()
    # Making a dictionary of products
    product_dict = {product: i for i, product in enumerate(products)}
    # Saving the dictionary using json
    with open(args.product_dict_path, 'w') as f:
        json.dump(product_dict, f)
    
    prod_to_index: bool = False

    # Creating graph
    graph = nx.Graph()

    date_group = dataset.groupby('SHOP_DATE')
    for g,date_df in date_group:
        client_df = date_df.groupby('CUST_CODE')
        for _,client in client_df:
            # Transform the products into indexes
            client["prod_index"] = client["PROD_CODE"].apply(lambda x: product_dict[x])
            # Create all the possible pairs of products
            if prod_to_index:
                pairs = list(permutations(client["prod_index"], 2))
            else:
                pairs = list(permutations(client["PROD_CODE"], 2))
            # Add the pairs to the graph
            for pair in pairs:
                if graph.has_edge(pair[0], pair[1]):
                    graph[pair[0]][pair[1]]['weight'] += 1
                else:
                    graph.add_edge(pair[0], pair[1], weight=1)
        
    # See the graph
    print("Number of nodes: ", graph.number_of_nodes())
    print("Number of edges: ",graph.number_of_edges())

    # Save the graph
    nx.write_gml(graph, args.output_path)
    return

if __name__ == "__main__":
    main()