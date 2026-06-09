from GenericTrackerSimulator.src.Geometry.FullTracker import FullTracker
from GenericTrackerSimulator.src.Geometry.Tracker import Tracker
from GenericTrackerSimulator.src.Geometry.BarrelLayer import BarrelLayer
from GenericTrackerSimulator.src.Geometry.EndcapDisk import EndcapDisk
from GenericTrackerSimulator.src.Geometry.GeometryBuilder import GeometryBuilder
from GenericTrackerSimulator.src.Geometry.GeometryTools import GeometryTools
from GenericTrackerSimulator.src.Generation.genParticle import genParticle

import matplotlib.pyplot as plt
import numpy as np
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)



if __name__=='__main__':


    gBuilder = GeometryBuilder()
    #If we want to generate a geometry from Geometry Builder
    gBuilder.build()
    #gTools = GeometryTools(gBuilder.ftr)
    #gTools.exportGeometry('tracker.json')
    #sys.exit()

    #gTools = GeometryTools(gBuilder.ftr)
    #gTools.importGeometry('tracker.json')
    gBuilder.ftr.setNavigator()

    p =  genParticle(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 0.1, 1, 13)
    gBuilder.ftr.propagateParticle(p)

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
    ax1.set_ylabel('y [cm]')
    ax1.set_zlabel('z [cm]')
    ax2.set_xlabel('x [cm]')
    ax2.set_ylabel('y [cm]')
    ax3.set_xlabel('z [cm]')
    ax3.set_ylabel('y [cm]')
    ax4.set_xlabel('z [cm]')
    ax4.set_ylabel('x [cm]')

    #gBuilder.ftr.draw(ax1, ax2, ax3, ax4, t1='b--', t2='r--')
    #plt.show()
