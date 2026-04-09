import numpy as np
import sys
import optparse
import ROOT as r
from array import array

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
    parser.add_option('-n', '--ntrack', action='store', type=int, dest='nTracks', default=10, help='Number of tracks')
    parser.add_option('-o', '--output', action='store', type='string', dest='outputFile', default='output.root', help='Name of output file.')


    (opts, args) = parser.parse_args()

    #configuring the tracker
    layers = np.linspace(3, 114, num=20)
    layersz = np.linspace(130, 270, 5)
    sigma_rphi = 0.312/np.sqrt(12.00)
    sigma_z = 0.3
    tracker = Tracker(layers, layersz, sigma_rphi, sigma_z, 220.0, [0,0,0])
    NMax = 
    pt = array('f', [0])
    phi = array('f', [0])
    eta = array('f', [0])
    charge = array('i', [0])
    type = array('i', [0])
    nEvent = array('i', [0])
    nhits = array('i', [0])
    xe = array('f', NMax*[0])
    ye = array('f', NMax*[0])
    ze = array('f', NMax*[0])
    xge = array('f', NMax*[0])
    yge = array('f', NMax*[0])
    zge = array('f', NMax*[0])
    x = array('f', NMax*[0])
    y = array('f', NMax*[0])
    z = array('f', NMax*[0])
    xg = array('f', NMax*[0])
    yg = array('f', NMax*[0])
    zg = array('f', NMax*[0])
    
    tree = r.TTree("hits", "hits")
    tree.Branch('pt', pt, 'pt/F')
    tree.Branch('phi', phi, 'phi/F')
    tree.Branch('eta', eta, 'eta/F')
    tree.Branch('charge', charge, 'charge/I')
    tree.Branch('type', type, 'type/I')
    tree.Branch('nEvent', nEvent, 'nEvent/I')  
    tree.Branch('nhits', nhits, 'nhits/I')  
    tree.Branch('xe', xe, 'xe[nhits]/F')
    tree.Branch('ye', ye, 'ye[nhits]/F')
    tree.Branch('ze', ze, 'ze[nhits]/F')
    tree.Branch('xge', xge, 'xge[nhits]/F')
    tree.Branch('yge', yge, 'yge[nhits]/F')
    tree.Branch('zge', zge, 'zge[nhits]/F')
    tree.Branch('x', x, 'x[nhits]/F')
    tree.Branch('y', y, 'y[nhits]/F')
    tree.Branch('z', z, 'z[nhits]/F')
    tree.Branch('xg', xg, 'xg[nhits]/F')
    tree.Branch('yg', yg, 'yg[nhits]/F')
    tree.Branch('zg', zg, 'zg[nhits]/F')

    counter = 0
    alist = []
    while counter < int(opts.nTracks):

        if counter % 10000 == 0:
            print(counter*100.0/int(opts.nTracks))
        phi_ = np.random.uniform(0, 2.0*np.pi)
        #phi_ = np.random.uniform(5.0*np.pi/180.0, 5.0*np.pi/180.0 + 4.0*np.pi/180.0)
        eta_ = np.random.uniform(-1.7, 1.7)
        #pt_ = np.random.uniform(26.0, 50.0)
        pt_ = np.random.triangular(15.0, 38, 50.0)
        if pt_ < 26 or pt_ > 50.0:
            continue
        charge_ = int(np.sign(np.random.uniform(-1.0, 1.0)))
        track = Track(0, 0, phi_, eta_, pt_, charge_)
        tracker.fullMeasurement(track)
        pt[0] = pt_
        phi[0] = phi_
        eta[0] = eta_
        nEvent[0] = counter
        charge[0] = charge_
        nhits[0] = len(track.lxi)
        type[0] = 0
        insert(xe, track.lxi, NMax)
        insert(ye, track.lyi, NMax)
        insert(ze, track.lzi, NMax)
        insert(x, track.lxm, NMax)
        insert(y, track.lym, NMax)
        insert(z, track.lzm, NMax)
        insert(xge, track.xi, NMax)
        insert(yge, track.yi, NMax)
        insert(zge, track.zi, NMax)
        insert(xg, track.xm, NMax)
        insert(yg, track.ym, NMax)
        insert(zg, track.zm, NMax)
       
        tree.Fill()
        counter = counter + 1
           
    f = r.TFile(opts.outputFile, "RECREATE")
    f.WriteObject(tree, "hits")
    f.Close()

    



 
