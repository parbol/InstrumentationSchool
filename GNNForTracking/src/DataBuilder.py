import numpy as np
import pandas as pd
import torch
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData



class DataBuilder:

    def __init__(self, filename, phi_window):
         
        self.filename = filename
        self.phi_window = phi_window 

    def build(self):
        
        df = pd.read_parquet(self.filename)
        df = df.reset_index()  # Make sure indexes pair with number of rows
        
        #Round the values of the dataset to 4 decimal places
        #df = df.round(4)
    
        ##Add a column to use as index from 0 to the length of the dataset
        #df['n_label'] = range(0, len(df))
    
        #Empty hetero graph 
        data=HeteroData()

        #node names
        nodes_s=df['label'].values
        nodes_t=df['label'].values

        #Add nodes to the graph
        data['source'].node_id = torch.tensor(nodes_s, dtype=torch.long)
        data['target'].node_id = torch.tensor(nodes_t, dtype=torch.long)
    
        #Add node attributes, in this case the position of the points
        data['source'].x = torch.Tensor(np.copy(df[['x', 'y', 'z']].values))
        data['target'].x = torch.Tensor(np.copy(df[['x', 'y', 'z']].values))
    
        # Creating the edge structure for those points in a phi window with respect to the see
        phi_window = self.phi_window * np.pi/180.0
        uprow = []
        downrow = []
        weight = []
        for index, row in df.iterrows():
            p1 = np.asarray([row['x'], row['y']])
            #phi1 = np.atan2(row['y'], row['x'])
            node1 = row['label']
            for jindex, row2 in df.iterrows():
                if abs(row['layer'] + 1 - row2['layer']) > 0.5:
                    continue
                p2 = np.asarray([row2['x'], row2['y']])
                DeltaP = p2 - p1
                phi = np.acos(np.dot(p1, DeltaP)/(np.linalg.norm(p1)*np.linalg.norm(DeltaP)))    
                if phi < phi_window/2.0:
                    node2 = row2['label']
                    uprow.append(node1)
                    downrow.append(node2)
                    if row['particle'] == row2['particle']:
                        weight.append(1.0)
                    else:
                        weight.append(0.0)
        
        
        edge_index = torch.tensor([uprow, downrow], dtype=torch.long)
        weight_val = torch.tensor(weight, dtype=torch.float)

        
        data['source', 'weight', 'target'].edge_index = edge_index
        data['source', 'weight', 'target'].edge_label = weight_val
    
                        
        #check if the data is valid
        print('The data looks good', data.validate(raise_on_error=True))

        data = T.ToUndirected()(data)
        del data['target', 'rev_weight', 'source'].edge_label

        return data


    ########################################################################################                  
    def DeltaPhi(self, phi1, phi2):

        x1 = np.asarray([np.cos(phi1), np.sin(phi1)])
        x2 = np.asarray([np.cos(phi2), np.sin(phi2)])
        return np.acos(np.dot(x1, x2))
    


