import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData
import optparse
import torch.nn.functional as F
import sys
from GNNForTracking.src.GNNModel import GNNModel
from GNNForTracking.src.DataBuilder import DataBuilder
from torch_geometric.nn import to_hetero




if __name__ == "__main__":


    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    
    parser.add_option('-i', '--inputTrainPoint',  action='store', type='string', dest='inputTrainPoint', default='input.parquet', help='Name of input point training file.')
    parser.add_option('-v', '--inputValidationPoint',  action='store', type='string', dest='inputValidationPoint', default='input.parquet', help='Name of input validation point file.')

    (opts, args) = parser.parse_args()
    #Some global variables

    # Select the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Prepare and get the data
    builderTrain = DataBuilder(opts.inputTrainPoint, 45.0)
    train_data = builderTrain.build()
    builderVal = DataBuilder(opts.inputValidationPoint, 45.0)
    val_data = builderVal.build()

    # Create model and optimizer
    model = GNNModel(train_data.metadata(), hidden_channels=32).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)


    # Actual training
    train_data = train_data.to(device)
    val_data = val_data.to(device)

    theTrainLoss = 0
    theValLoss = 0
    for epoch in range(1, 3000):
        model.train()
        optimizer.zero_grad()
        pred = model(train_data.x_dict, train_data.edge_index_dict,
                     train_data['source', 'target'].edge_index)
        target = train_data['source', 'target'].edge_label
        loss = F.mse_loss(pred, target)
        loss.backward()
        optimizer.step()
        theTrainLoss = loss.item()
        with torch.no_grad():    
            model.eval()
            pred = model(val_data.x_dict, val_data.edge_index_dict,
                     val_data['source', 'target'].edge_index)
            pred = pred.clamp(min=0, max=1)
            target = val_data['source', 'target'].edge_label.float()
            theValLoss = F.mse_loss(pred, target).sqrt()
        print(f'Epoch: {epoch:03d}, Loss: {theTrainLoss:.4f}, Val: {theValLoss:.4f}')


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
    target = target.cpu().numpy()
    print('---pred', pred)
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

    torch.save(model.state_dict(), f'model.pth')

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