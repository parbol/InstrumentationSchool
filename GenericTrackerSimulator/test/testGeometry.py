from GenericTrackerSimulator.src.Geometry.FullTracker import FullTracker
from GenericTrackerSimulator.src.Geometry.Tracker import Tracker
from GenericTrackerSimulator.src.Geometry.BarrelLayer import BarrelLayer
from GenericTrackerSimulator.src.Geometry.EndcapDisk import EndcapDisk
from GenericTrackerSimulator.src.Geometry.GeometryBuilder import GeometryBuilder
from GenericTrackerSimulator.src.Geometry.GeometryTools import GeometryTools
from GenericTrackerSimulator.src.Generation.genParticle import genParticle

import matplotlib.pyplot as plt
import numpy as np
import optparse
import pandas as pd

import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)



if __name__=='__main__':

    parser = optparse.OptionParser(usage='usage: %prog [options] path', version='%prog 1.0')
    parser.add_option('-n', '--nevents', action='store', type=int,      dest='nEvents',    default=10,            help='Number of events')
    parser.add_option('-o', '--output',  action='store', type='string', dest='outputFile', default='output.parquet', help='Name of output file.')

    (opts, args) = parser.parse_args()
    #Some global variables


    gBuilder = GeometryBuilder()
    #If we want to generate a geometry from Geometry Builder
    gBuilder.build()
    gTools = GeometryTools(gBuilder.ftr)
    #gTools.exportGeometry('tracker.json')
    #sys.exit()

    #gTools = GeometryTools(gBuilder.ftr)
    #gTools.importGeometry('tracker.json')
    gBuilder.ftr.setNavigator()

   
    #Some global variables
    #fig = plt.figure(figsize = plt.figaspect(0.3))
    fig = plt.figure(figsize = (8, 8), layout="constrained")
    gs0 = fig.add_gridspec(2, 1, height_ratios=[2,1])
    ax1 = fig.add_subplot(gs0[0], projection = '3d')
    gs1 = gs0[1].subgridspec(1,3)
    ax2 = fig.add_subplot(gs1[0])
    ax3 = fig.add_subplot(gs1[1])
    ax4 = fig.add_subplot(gs1[2])
    ax1.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax1.set_xlabel('x [cm]')
    ax1.set_ylabel('z [cm]')
    ax1.set_zlabel('y [cm]')
    ax2.set_xlabel('x [cm]')
    ax2.set_ylabel('y [cm]')
    ax3.set_xlabel('z [cm]')
    ax3.set_ylabel('y [cm]')
    ax4.set_xlabel('z [cm]')
    ax4.set_ylabel('x [cm]')


    gBuilder.ftr.drawBarrel(ax1, ax2, ax3, ax4, t='b--')

    nParticles = opts.nEvents
    counterNodes = 0
    counter = 0
    nLayers = 6
    particle = dict()
    particle['particle'] = []
    particle['x'] = []
    particle['y'] = []
    particle['z'] = []
    particle['layer'] = []
    particle['pt'] = []
    particle['charge'] = []
    particle['label'] = []

    while counter < nParticles:
        print('Counter', counter)
        x = y = z = t = 0
        phi = np.random.uniform(0.0, 2.0*np.pi)
        eta = np.random.uniform(-0.5, 0.5)
        pt = np.random.uniform(0.5, 10.0)
        mass = 0.1395
        charge = np.sign(np.random.uniform(-1.0, 1.0))
        id = 121
        p =  genParticle(x = x, y = y, z = z, t = t, phi = phi, eta = eta, pt = pt, mass = mass, q=charge, id = id)
        gBuilder.ftr.propagateParticle(p)
        if len(p.layerIntersections) != nLayers or len(p.intersections) != nLayers:
            continue
        for i, ts in enumerate(p.layerIntersections):
            print(i)
            mod = p.intersections[i][0]
            particle['particle'].append(counter)
            particle['x'].append(ts.x)
            particle['y'].append(ts.y)
            particle['z'].append(ts.z)
            particle['layer'].append(mod.barrelIndex)
            particle['pt'].append(ts.pt)
            particle['charge'].append(ts.q)
            particle['label'].append(counterNodes)
            counterNodes = counterNodes + 1   
        p.drawIntersections(ax1, ax2, ax3, ax4, t='g*')
        p.draw(gBuilder.ftr.propagator.B, ax1, ax2, ax3, ax4, fmt='r')
        counter = counter + 1

    df = pd.DataFrame(particle)
    df.to_parquet(opts.outputFile)
   
    plt.show()
