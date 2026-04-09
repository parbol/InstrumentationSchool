import numpy as np
import sys
import optparse
from array import array
import pandas as pd


from TrackerSimulator.src.Tracker import Tracker
from TrackerSimulator.src.Track import Track


def insert(a, b, N):

    for i in range(0, N):
        if i < len(b):
            a[i] = b[i]
        else:
            a[i] = 0


if __name__ == "__main__":

   
    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-n', '--nevents', action='store', type=int,      dest='nEvents',    default=10,            help='Number of events')
    parser.add_option('-t', '--ntrack',  action='store', type=int,      dest='nTracks',    default=10,            help='Number of tracks')
    parser.add_option('-o', '--output',  action='store', type='string', dest='outputFile', default='output.root', help='Name of output file.')

    (opts, args) = parser.parse_args()

    #configuring the tracker
    layers = np.linspace(3, 114, num=20)
    layersz = np.linspace(130, 270, 5)
    sigma_rphi = 0.312/np.sqrt(12.00)
    sigma_z = 0.3
    tracker = Tracker(layers, layersz, sigma_rphi, sigma_z, 220.0, [0,0,0])

    eventCounter = 0
    phi = []
    eta = []
    pt = []
    charge = []

    events = dict()
    events['phi'] = []
    events['eta'] = []
    events['pt'] = []
    events['charge'] = []
    events['layer'] = []
    events['time'] = []
    events['index'] = []

    while eventCounter < int(opts.nEvents):

        if counter % 10000 == 0:
            print(counter*100.0/int(opts.nTracks))
    
        tphi = []
        teta = []
        tpt = []
        tcharge = []
        hlayer = []
        htime = []
        hindex = []
        for j in range(opt.nTracks):

            phi_ = np.random.uniform(0, 2.0*np.pi)
            eta_ = np.random.uniform(-1.7, 1.7)
            pt_ = np.random.triangular(15.0, 38, 50.0)
            if pt_ < 26 or pt_ > 50.0:
                continue
            charge_ = int(np.sign(np.random.uniform(-1.0, 1.0)))
            tphi.append(phi_)
            teta.append(eta_)
            tpt.append(pt_)
            tcharge.append(charge_)
        
            track = Track(0, 0, phi_, eta_, pt_, charge_)
            tracker.fullMeasurement(track)

            hlayer.append(track.l)
            htime.append(track.l)
            hindex.append(track.l)

            #x.append(track.xm)
            #y.append(track.ym)
            #z.append(track.zm)
            #l.append(l)
            #t.append(t)
        eventCounter = eventCounter + 1
        events['phi'].append(tphi)
        events['eta'].append(teta)
        events['pt'].append(tpt)
        events['charge'].append(tcharge)
        events['layer'].append(hlayer)
        events['time'].append(htime)
        events['index'].append(hindex)

    df = pd.DataFrame(events)

    



 
