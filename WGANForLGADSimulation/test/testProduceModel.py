import torch
import pandas as pd
import optparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


cuda = True if torch.cuda.is_available() else False # GPU Setting


if __name__=='__main__':
    
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='input', default='parquetfile.parquet', help='Input file')
    parser.add_option('-m', '--model', action='store', type='string', dest='model', default='model.pt', help='Model file')
    parser.add_option('-o', '--output', action='store', type='string', dest='output', default='output.pt', help='Output file')
    (opts, args) = parser.parse_args()

    device = 'cuda'
    if not cuda:
        device = 'cpu'

    
    model = torch.load(opts.model, weights_only = False, map_location=torch.device(device))
    model.eval()

    data = pd.read_parquet(opts.input).to_numpy()
    #scaler = StandardScaler()
    #data = scaler.fit_transform(data)
    tensordata = torch.tensor(data, dtype=torch.float32, device=device)
    loader = torch.utils.data.DataLoader(dataset=tensordata, batch_size = 512, shuffle=True)	 
    samples = torch.empty((0, data.shape[1]), dtype=torch.float32, device=device)
    latent_dim = 5
    for i, x in enumerate(loader):    
        #Running nstepgens times the generator
        generatorInput = x[:,1:4]
        z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32, device=device)
        z = torch.cat((z_, generatorInput), 1)
        events = model(z)
        sample = torch.cat((x[:,0:4], events.detach()), 1)
        samples = torch.cat((samples, sample), 0)


    data = samples.detach().cpu().numpy()
    dataset = pd.DataFrame({'id': data[:,0], 'p': data[:,1], 'phi': data[:,2], 't': data[:,3], 'toa': data[:,4], 'tot':data[:,5]})
    dataset.to_parquet(opts.output)

