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


    data = pd.read_parquet(opts.input).to_numpy()
    tensordata = torch.tensor(data, device='cuda')
    loader = torch.utils.data.DataLoader(dataset=tensordata, batch_size = 2048, shuffle=True)	 


    generator = Generator()
    discriminator = Discriminator()
    
    generator_loss = torch.nn.MSELoss()
    generator_optimizer = torch.optim.Adam(generator.parameters(), lr=0.001)

    if cuda:
        generator.cuda()
        discriminator.cuda()
        generator_loss.cuda()
        generator_optimizer.cuda()

    n_epochs = 10 # suggested default = 200
    latent_dim = 5
    nstepsgen = 5
    nstepsdis = 3
    for epoch in range(n_epochs):
        for i, (x, _) in enumerate(loader):    
            #Running nstepgens times the generator
            for istep in range(nstepsgen):
                generator_optimizer.grad()
                generatorInput = x[:,1:3]
                realEvents = x[:, 4:5]
                z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)))
                z = torch.cat(z_, generatorInput)
                fakeEvents = generator(realEvents)
                g_loss = generator_loss(fakeEvents, realEvents)
                g_loss.backward()
                generator_optimizer.step()
            #Running nstepgdis times the generator
            for istep in range(nstepsdis):
                generator_optimizer.grad()
                generatorInput = x[:,1:3]
                realEvents = x[:, 4:5]
                z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)))
                z = torch.cat(z_, generatorInput)
                fakeEvents = generator(realEvents)
                g_loss = generator_loss(fakeEvents, realEvents)
                g_loss.backward()
                generator_optimizer.step()




            # Adversarial ground truths (For more detail, refer *Read_More below)
            valid = Variable(Tensor(imgs.size(0), 1).fill_(1.0), requires_grad=False) # imgs.size(0) == batch_size(1 batch) == 64, *TEST_CODE
            fake = Variable(Tensor(imgs.size(0), 1).fill_(0.0), requires_grad=False) # And Variable is for caclulate gradient. In fact, you can use it, but you don't have to. 
                                                                                # requires_grad=False is default in tensor type. *Read_More
        
        # Configure input
        real_imgs = imgs.type(Tensor) # As mentioned, it is no longer necessary to wrap the tensor in a Variable.    