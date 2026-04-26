from LGADModuleSimulator.src.LGADSimulator import LGADSimulator
import numpy as np
import matplotlib.pyplot as plt
import optparse
import pandas as pd



if __name__ == "__main__":


    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-n', '--nevents', action='store', type=int,      dest='nEvents',    default=10,            help='Number of events')
    parser.add_option('-o', '--output',  action='store', type='string', dest='outputFile', default='output.root', help='Name of output file.')

    (opts, args) = parser.parse_args()
    #Some global variables
    
    lgad = LGADSimulator(thickness=0.3, radius=1.0, 
                        intLumi = 0.0, taur = 2.0,
                        taud=3.0, clock=3.0,
                        threshold=0.9525, noiseLevel=0.2750, sigmaTDC=0.010)
    
    events = dict()
    events['id'] = []
    events['p'] = []
    events['phi'] = []
    events['t'] = []
    events['toa'] = []
    events['tot'] = []

    eventCounter = 0
    while eventCounter < int(opts.nEvents):

        #We select the kind of particle
        p = np.random.uniform(1.0, 20) #GeV
        idselect = np.random.uniform(0, 1)
        id = 0
        idselect = 0.9
        if idselect < 0.03:
            id = 13
        elif idselect >= 0.03 and idselect < 0.06:
            id = 11
        elif idselect >= 0.06 and idselect < 0.25:
            id = 321
        elif idselect >= 0.25 and idselect < 0.35:
            id = 2212
        else:
            id = 121
        phi = np.random.normal(0, np.pi/12.0)
        if abs(phi) > np.pi/4.0:
            continue
        t = np.random.uniform(1, 5) #ns
        toa, tot, charge = lgad.getResponse(id, p, phi, t)
        if charge == -1:
            continue
        events['id'].append(id)
        events['p'].append(p)
        events['phi'].append(phi)
        events['t'].append(t)
        events['toa'].append(toa)
        events['tot'].append(tot)
        eventCounter = eventCounter + 1
   

    df = pd.DataFrame(events)
    df.to_parquet(opts.outputFile)

    #fig, ax = plt.subplots()
    #lgad.drawEvent(ax, 13, 10, 0, 0)
    #plt.show()
    
