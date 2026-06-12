from WGANForLGADSimulation.src.Generator import Generator
from WGANForLGADSimulation.src.Discriminator import Discriminator
import torch
import pandas as pd
import optparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


cuda = True if torch.cuda.is_available() else False # GPU Setting

####################Parameters######################
batch_size=8192
batch_size=1024
#12 dimensions for the latent_space
latent_dim = 12
latent_dim = 6
#3 conditional variables: p, phi and t
conditional_dim = 3
#2 output variables: toa, tot
output_dim = 2
#Learning rate
lr = 0.0005
#Number of epochs
n_epochs=200
#N steps generation
nstepsgen = 1
#N steps discriminator
nstepsdis = 5
####################Parameters######################

if __name__=='__main__':
    
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='input', default='inputval.parquet', help='Input file')
    (opts, args) = parser.parse_args()

    device = 'cuda'
    if not cuda:
        device = 'cpu'

    data = pd.read_parquet(opts.input).to_numpy()
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    tensordata = torch.tensor(data, dtype=torch.float32, device=device)
    loader = torch.utils.data.DataLoader(dataset=tensordata, batch_size = batch_size, shuffle=True)	 

    generator = Generator(latent_dim=latent_dim, conditional_dim=conditional_dim, output_dim=output_dim)
    discriminator = Discriminator(conditional_dim=conditional_dim, output_dim=output_dim)

    if cuda:
        generator.cuda()
        discriminator.cuda()
    generator_optimizer = torch.optim.Adam(generator.parameters(), lr=lr)
    discriminator_optimizer = torch.optim.Adam(discriminator.parameters(), lr=lr)

    epochs = []
    loss_disc = []
    loss_gen = []
    for epoch in range(n_epochs):
        numericLossDiscriminator = 0
        numericLossGenerator = 0
        for i, x in enumerate(loader):    
            #Running nstepgens times the generator
            generatorInput = x[:,1:4]
            realEvents = x[:, 1:6]
            #Running nstepgdis times the generator
            for istep in range(nstepsdis):
                discriminator_optimizer.zero_grad()
                z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32, device=device)
                z = torch.cat((z_, generatorInput), 1)
                fakeEvents_ = generator(z)
                fakeEvents = torch.cat((generatorInput, fakeEvents_), 1)
                fakeEventCat = discriminator(fakeEvents.detach())
                realEventCat = discriminator(realEvents)
                f_loss = torch.mean(fakeEventCat) - torch.mean(realEventCat)
                #d_loss = f_loss + 10.0 * gradient_penalty(discriminator, realEvents, fakeEvents.detach())
                f_loss.backward()
                discriminator_optimizer.step()
                d_l = f_loss.item()
                numericLossDiscriminator = d_l 
            for istep in range(nstepsgen):
                generator_optimizer.zero_grad()
                z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32, device=device)
                z = torch.cat((z_, generatorInput), 1)
                fakeEvents_ = generator(z)
                fakeEvents = torch.cat((generatorInput, fakeEvents_), 1)
                fakeEventCat = discriminator(fakeEvents)
                g_loss = -torch.mean(fakeEventCat)
                g_loss.backward()
                generator_optimizer.step()
                numericLossGenerator = g_loss.item()
        print('Epoch:', epoch, 'Generator loss:', numericLossGenerator, 'Discriminator loss:', numericLossDiscriminator)
        epochs.append(epoch)
        loss_gen.append(numericLossGenerator)
        loss_disc.append(numericLossDiscriminator)

    torch.save(generator, 'generator.pt')
    torch.save(discriminator, 'discriminator.pt')

    print(epochs)
    print(loss_gen)
    print(loss_disc)
    # Defining the Plot Style
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    #plt.yscale('log')
    # Plotting the last 100 values
    plt.plot(np.asarray(epochs), np.asarray(loss_gen), color='blue')
    plt.plot(np.asarray(epochs), np.asarray(loss_disc), color='red')
    plt.savefig('loss.png')
