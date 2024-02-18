# GraphModels

The purpose of this repository is to explore different 
approaches for graph data modelling as well as 
the process of training graph neural networks.

![image](https://www.spsc.tugraz.at/collections/assets/pgm.png)
# Dataset 
The dataset can be found in the following link:
https://www.dunnhumby.com/source-files/

# Requirements
The following project uses conda as package manager. 
To install the necessary libraries, run the following command.

```
    conda env create --name pyg -f pyg.yaml 
    conda activate pyg
```

# Analysis 

The graph building process can be run with the following command:
```
    python graph_building.py
```
To plot the graph based on a center node, run the following command:
```
    python plot_frequently_bought.py
```
# Author 
Bryan Piguave 
