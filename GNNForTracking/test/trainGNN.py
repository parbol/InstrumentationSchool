import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData
import optparse


if __name__ == "__main__":


    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    
    parser.add_option('-i', '--input',  action='store', type='string', dest='inputFile', default='input.parquet', help='Name of input file.')

    (opts, args) = parser.parse_args()
    #Some global variables

    df = pd.read_parquet(opts.inputFile)
    
    #Empty hetero graph 
    data=HeteroData()
    
    nodes_s=df['label'].values
    nodes_t=df['label'].values
    




