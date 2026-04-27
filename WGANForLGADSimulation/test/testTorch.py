from WGANForLGADSimulation.src.Generator import Generator
from WGANForLGADSimulation.src.Discriminator import Discriminator
import torch
import pandas as pd
import optparse
import numpy as np
import matplotlib.pyplot as plt


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
    loader = torch.utils.data.DataLoader(dataset=tensordata, batch_size = 64, shuffle=True)	 


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
        #generator_optimizer.cuda()
        discriminator_loss_real.cuda()
        discriminator_loss_fake.cuda()
        #discriminator_optimizer.cuda()

    epochs = []
    loss_disc = []
    loss_gen = []
    n_epochs = 50 # suggested default = 200
    latent_dim = 5
    nstepsgen = 5
    nstepsdis = 1
    for epoch in range(n_epochs):
        numericLossDiscriminator = 0
        numericLossGenerator = 0
        for i, x in enumerate(loader):    
            #Running nstepgens times the generator
            generatorInput = x[:,1:4]
            realEvents = x[:, 1:6]
            for istep in range(nstepsgen):
                generator_optimizer.zero_grad()
                z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32, device=device)
                z = torch.cat((z_, generatorInput), 1)
                fakeEvents_ = generator(z)
                fakeEvents = torch.cat((generatorInput, fakeEvents_), 1)
                g_loss = generator_loss(fakeEvents, realEvents)
                g_loss.backward()
                generator_optimizer.step()
                numericLossGenerator = g_loss.item()
                #numericLossGenerator = g_loss.detach().cpu().numpy()[0]
            #Running nstepgdis times the generator
            z_ = torch.tensor(np.random.normal(0, 1, (generatorInput.shape[0],latent_dim)), dtype=torch.float32, device=device)
            z = torch.cat((z_, generatorInput), 1)
            fakeEvents_ = generator(z)
            fakeEvents = torch.cat((generatorInput, fakeEvents_), 1)
            fakeCat = torch.zeros(fakeEvents.shape[0], 1, device=device)
            realCat = torch.ones(realEvents.shape[0], 1, device=device)
            for istep in range(nstepsdis):
                discriminator_optimizer.zero_grad()
                realEventCat = discriminator(realEvents)
                d_loss_real = discriminator_loss_real(realEventCat, realCat)
                d_loss_real.backward()
                fakeEventCat = discriminator(fakeEvents.detach())
                d_loss_fake = discriminator_loss_fake(fakeEventCat, fakeCat)
                d_loss_fake.backward()
                discriminator_optimizer.step()
                #d_l_r = d_loss_real.detach().cpu().numpy()[0]
                #d_l_f = d_loss_fake.detach().cpu().numpy()[0]
                d_l_r = d_loss_real.item()
                d_l_f = d_loss_fake.item()
                numericLossDiscriminator = 0.5 * (d_l_r + d_l_f)
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
    plt.yscale('log')
    # Plotting the last 100 values
    plt.plot(np.asarray(epochs), np.asarray(loss_gen), color='blue')
    plt.plot(np.asarray(epochs), np.asarray(loss_disc), color='red')
    plt.savefig('loss.png')
