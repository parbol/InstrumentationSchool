import pandas as pd
import optparse
import numpy as np
import matplotlib.pyplot as plt



if __name__=='__main__':
    
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='input', default='inputval.parquet', help='Input file')
    (opts, args) = parser.parse_args()

   

    data = pd.read_parquet(opts.input).to_numpy()
    
    #Figure 
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))

    axs[0][0].hist(data[:,0])
    axs[0][0].set_xlabel('particle id')
    
    axs[0][1].hist(data[:,1], bins=50)
    axs[0][1].set_xlabel('p [GeV]')

    axs[0][2].hist(data[:,2], bins=50)
    axs[0][2].set_xlabel('phi')

    axs[1][0].hist(data[:,3], bins=50)
    axs[1][0].set_xlabel('t [ns]')
    
    axs[1][1].hist(data[:,4], bins=50, range=(0, 10))
    axs[1][1].set_xlabel('toa [ns]')
    
    axs[1][2].hist(data[:,5], bins=50, range=(5, 17))
    axs[1][2].set_xlabel('tot [ns]')


    plt.show()

