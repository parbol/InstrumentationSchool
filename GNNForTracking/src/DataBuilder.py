import numpy as np
import pandas as pd
import torch
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData



class DataBuilder:

    def __init__(self, filename):
         
    df = pd.read_parquet(filename)
    
    #Round the values of the dataset to 4 decimal places
    df = df.round(4)
    
    ##Add a column to use as index from 0 to the length of the dataset
    #df['n_label'] = range(0, len(df))
    
    #Empty hetero graph 
    data=HeteroData()

    #node names
    nodes_s=df['n_label'].values
    nodes_t=df['n_label'].values
    
    #Add nodes to the graph
    data['source'].node_id = torch.tensor(nodes_s, dtype=torch.long)
    data['target'].node_id = torch.tensor(nodes_t, dtype=torch.long)
    
    #Add node attributes, in this case the position of the points
    data['source'].x = torch.Tensor(df[['x', 'y', 'z']].values)
    data['target'].x = torch.Tensor(df[['x', 'y', 'z']].values)
    
    # Creating the edge structure
    phi_window = 45 * np.pi/180.0
    for row in df.rows:
        if row['layer'] == 0:
            phi = np.atan2(row['y'], row['x'])
            for row2 in df.rows:
                if row['layer'] <= row2['layer']:
                    continue
                phi2 = np.atan2(row2['y'], row2['x'])
                phi2pos = np.asarray([np.cos(phi2), np.sin(phi2)])
                phimax = phi + phi_window/2.0
                phimaxois = np.asarray([np.cos(phi2), np.sin(phi2)])
                phitest = phi2
                if phitest < 0.0:
                    phitest = phitest + np.pi * 2.0
                if phitest > phimax 

                phimin = phi - phi_window/2.0
                if phi < phimax


                
    
    
    df_edge = pd.read_parquet(edge_path)
    df_edge = df_edge.replace({'weight':0.5}, 0.)

    edge_index = torch.tensor([df_edge['Source'], df_edge['Target']], dtype=torch.long)
    data['source', 'weight', 'target'].edge_index = edge_index
    
    #edge attributes
    weight_val = torch.from_numpy(df_edge['weight'].values).to(torch.float)
    
    data['source', 'weight', 'target'].edge_label = weight_val
    
    #check if the data is valid
    print(data.validate(raise_on_error=True))

    data = T.ToUndirected()(data)
    del data['target', 'rev_weight', 'source'].edge_label

    return data