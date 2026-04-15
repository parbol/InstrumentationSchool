import numpy as np
import sys
import optparse
from array import array
import pandas as pd


from TrackerSimulator.src.Tracker import Tracker
from TrackerSimulator.src.Track import Track
from TrackerSimulator.src.Noise import Noise


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

    #Dictionary to store events
    events = dict()
    events['phi'] = []
    events['eta'] = []
    events['pt'] = []
    events['charge'] = []
    events['hlayer'] = []
    events['hphi'] = []
    events['hindex'] = []
    
    
    eventCounter = 0
    while eventCounter < int(opts.nEvents):
       
        tphi = []
        teta = []
        tpt = []
        tcharge = []
        hlayer = []
        hphi = []
        hindex = []
        
        trackCounter = 0
        while trackCounter < int(opts.nTracks):

            phi_ = np.random.uniform(0, 2.0*np.pi)
            #Eta is zero for this application
            eta_ = np.random.uniform(0, 0)
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
              
            hlayer.extend(track.l.tolist())
            hphi.extend(np.atan2(track.ym, track.xm).tolist())
            hindex.extend([trackCounter for l in range(len(track.l))])
            trackCounter = trackCounter + 1

        noise = Noise(1)    
        tracker.createNoiseBarrel(noise)
        hlayer.extend(noise.l.tolist())
        hphi.extend(np.atan2(noise.ym, noise.xm).tolist())
        hindex.extend([-1 for l in range(len(noise.l))])

        eventCounter = eventCounter + 1
        events['phi'].append(tphi)
        events['eta'].append(teta)
        events['pt'].append(tpt)
        events['charge'].append(tcharge)
        events['hlayer'].append(hlayer)
        events['hphi'].append(hphi)
        events['hindex'].append(hindex)

    print('Phi', events['phi'])
    print('Eta', events['eta'])
    print('Pt', events['pt'])
    print('hlayer', events['hlayer'])
    print('hphi', events['hphi'])
    print('hindex', events['hindex'])


    df = pd.DataFrame(events)
    df.to_parquet(opts.outputFile)

    



 
