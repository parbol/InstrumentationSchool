from WGANForLGADSimulation.src.Generator import Generator
from WGANForLGADSimulation.src.Discriminator import Discriminator
import torch
import pandas as pd
import optparse
import numpy as np


cuda = True if torch.cuda.is_available() else False # GPU Setting


if __name__=='__main__':
    
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='input', default='inputval.parquet', help='Input file')
    (opts, args) = parser.parse_args()

    device = 'cuda'
    if not cuda:
        device = 'cpu'

    data = pd.read_parquet(opts.input).to_numpy()
    tensordata = torch.tensor(data, dtype=torch.float32, device=device)
    loader = torch.utils.data.DataLoader(dataset=tensordata, batch_size = 2048, shuffle=True)	 


    generator = Generator()
    discriminator = Discriminator()
    
    generator_loss = torch.nn.MSELoss()
    generator_optimizer = torch.optim.Adam(generator.parameters(), lr=0.001)

    discriminator_loss_real = torch.nn.BCELoss()
    discriminator_loss_fake = torch.nn.BCELoss()
    discriminator_optimizer = torch.optim.Adam(discriminator.parameters(), lr=0.001)


    if cuda:
        generator.cuda()
        discriminator.cuda()
        generator_loss.cuda()
        generator_optimizer.cuda()
        discriminator_loss_real.cuda()
        discriminator_loss_fake.cuda()
        discriminator_optimizer.cuda()

    n_epochs = 10 # suggested default = 200
    latent_dim = 5
    nstepsgen = 5
    nstepsdis = 3
    for epoch in range(n_epochs):
        for i, x in enumerate(loader):    
            #Running nstepgens times the generator
            generatorInput = x[:,1:3]
            print(generatorInput)
            realEvents = x[:, 4:6]
            for istep in range(nstepsgen):
                generator_optimizer.zero_grad()
                z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32)
                z = torch.cat((z_, generatorInput), 1)
                fakeEvents = generator(z)
                g_loss = generator_loss(fakeEvents, realEvents)
                g_loss.backward()
                generator_optimizer.step()
            
            #Running nstepgdis times the generator
            z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32)
            z = torch.cat((z_, generatorInput), 1)
            fakeEvents = generator(z)
            fakeCat = torch.zeros(fakeEvents.shape[0],1)
            realCat = torch.ones(realEvents.shape[0],1)
            for istep in range(nstepsdis):
                discriminator_optimizer.zero_grad()
                realEventCat = discriminator(realEvents)
                d_loss_real = discriminator_loss_real(realEventCat, realCat)
                d_loss_real.backward()
                fakeEventCat = discriminator(fakeEvents.detach())
                d_loss_fake = discriminator_loss_fake(fakeEventCat, fakeCat)
                d_loss_fake.backward()
                discriminator_optimizer.step()


