import pandas as pd
import optparse
import numpy as np
import matplotlib.pyplot as plt



if __name__=='__main__':
    
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-i', '--input', action='store', type='string', dest='input', default='inputval.parquet', help='Input file')
    parser.add_option('-r', '--reference', action='store', type='string', dest='reference', default='reference.parquet', help='Reference file')
    (opts, args) = parser.parse_args()

   

    data = pd.read_parquet(opts.input).to_numpy()
    ref = pd.read_parquet(opts.reference).to_numpy()
    
    #Figure 
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    axs[0].hist(data[:,4], bins=50, range=(0, 0.5), color='blue')
    axs[0].set_xlabel('toa - t [ns]')
    axs[1].hist(data[:,5], bins=50, range=(0, 20), color='blue')
    axs[1].set_xlabel('tot [ns]')
    #axs[0].hist(ref[:,4], bins=50, range=(0, 0.5), color='red')
    #axs[0].set_xlabel('toa - t [ns]')
    #axs[1].hist(ref[:,5], bins=50, range=(0, 20), color='red')
    #axs[1].set_xlabel('tot [ns]')
    

    plt.savefig('comparison.png')

