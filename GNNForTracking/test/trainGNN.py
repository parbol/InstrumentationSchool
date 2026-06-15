import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData
import optparse
import torch.nn.functional as F

import GNNForTracking.src.GNNModel as GNNModel

def buildData(points_path, edge_path):

    df=pd.read_parquet(points_path)
    #Round the values of the dataset to 4 decimal places
    df = df.round(4)
    #Add a column to use as index from 0 to the length of the dataset
    df['n_label'] = range(0, len(df))
    
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
    
    # Importing the dataset
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




if __name__ == "__main__":


    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    
    parser.add_option('-i', '--inputTrainPoint',  action='store', type='string', dest='inputTrainPoint', default='input.parquet', help='Name of input point training file.')
    parser.add_option('-e', '--inputTrainEdge',  action='store', type='string', dest='inputTrainEdge', default='input.parquet', help='Name of input edge training file.')
    parser.add_option('-v', '--inputValidationPoint',  action='store', type='string', dest='inputValidationPoint', default='input.parquet', help='Name of input validation point file.')
    parser.add_option('-w', '--inputValidationEdge',  action='store', type='string', dest='inputValidationEdge', default='input.parquet', help='Name of input validation edge file.')

    (opts, args) = parser.parse_args()
    #Some global variables
    
    # Prepare and get the data
    train_data = buildData(opts.inputTrainPoint, opts.inputTrainEdge)
    val_data = buildData(opts.inputValidationPoint, opts.inputValidationEdge)

    # Select the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Create model and optimizer
    model = GNNModel(hidden_channels=32).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

    def train():
        model.train()
        optimizer.zero_grad()
        pred = model(train_data.x_dict, train_data.edge_index_dict,
                     train_data['source', 'target'].edge_index)
        target = train_data['source', 'target'].edge_label
        loss = F.mse_loss(pred, target)
        loss.backward()
        optimizer.step()
        return float(loss)

    @torch.no_grad()
    def test(data):
        data = data.to(device)
        model.eval()
        pred = model(data.x_dict, data.edge_index_dict,
                     data['source', 'target'].edge_index)
        pred = pred.clamp(min=0, max=1)
        target = data['source', 'target'].edge_label.float()
        rmse = F.mse_loss(pred, target).sqrt()
        return float(rmse)

    # Actual training
    for epoch in range(1, 3001):
        train_data = train_data.to(device)
        loss = train()
        train_rmse = test(train_data)
        val_rmse = test(val_data)
        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Train: {train_rmse:.4f}, '          f'Val: {val_rmse:.4f}')


    test_data = val_data

    with torch.no_grad():
        test_data = test_data.to(device)
        pred = model(test_data.x_dict, test_data.edge_index_dict,
                     test_data['source', 'target'].edge_index)
        print(pred.shape)
        pred = pred.clamp(min=0, max=1)
        target = test_data['source', 'target'].edge_label.float()
        rmse = F.mse_loss(pred, target).sqrt()
        print(f'Test RMSE: {rmse:.4f}')

    sour = test_data['source', 'target'].edge_index[0].cpu().numpy()
    tar = test_data['source', 'target'].edge_index[1].cpu().numpy()
    pred = pred.cpu().numpy()
    print(pred.shape)
    target = target.cpu().numpy()

    res=pd.DataFrame({'source': sour, 'target': tar, 'pred': pred, 'compare': target})
    print(res.shape)

    #Add a new column if pred is greater or equal than 0.5 then 1 else 0.5
    res['weight'] = np.where(res['pred']>=0.5, 1., 0.)

    #compare column rating_1 with target and if they are equal add up

    cont=0
    for i in res.itertuples():
        if i.compare == i.weight:
            cont+=1

    #Calculate the accuracy
    accuracy = cont/len(res)
    print('Accuracy:', accuracy)
    print('Number of correct predictions:', cont)

    torch.save(model.state_dict(), f'model_{NTRACKS}_val100_epochs3000_{WINDOW}_all_test.pth')

    connected_accuracy = 0.
    nonconnected_accuracy = 0.

    n1,n2=0,0
    ncon,nncon=0,0
    for i in res.itertuples():
        if i.compare == 0.:
            if i.compare == i.weight: n1+=1
            nncon+=1
        elif i.compare == 1.0:
            if i.compare == i.weight: n2+=1
            ncon+=1

    connected_accuracy = n2/ncon
    nonconnected_accuracy = n1/nncon

    print(f'Accuracy in connected edges:     {n2}/{ncon} = {connected_accuracy}')
    print(f'Accuracy in non connected edges: {n1}/{nncon} = {nonconnected_accuracy}')