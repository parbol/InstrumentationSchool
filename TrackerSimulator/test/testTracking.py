import math
import numpy as np
import matplotlib.pyplot as plt
from random import Random
import sys


from TrackerSimulator.src.Tracker import Tracker
from TrackerSimulator.src.Track import Track
from TrackerSimulator.src.Plane import Plane
from TrackerSimulator.src.Module import Module






if __name__ == "__main__":

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

    #configuring the tracker
    layers = np.linspace(1, 114, 15)
    layersz = np.linspace(130, 270, 5)
    sigma_rphi = 0.01
    sigma_z = 0.01
    tracker = Tracker(layers, layersz, sigma_rphi, sigma_z, 220.0, [0,0,0])
    tracker.plot_tracker(ax1, ax2, ax3, ax4)
    

    #An example track 
    track = Track(0, 0, np.pi/2.0, 0.1, 10, 1.0)
    tracker.fullMeasurement(track)
    track.plot_track(ax1, ax2, ax3, ax4, 'r')
    track.plot_measurements(ax1, ax2, ax3, ax4, 'y*')
    print(track.l)
    #counter = 0
    #alist = []
    #while counter < 50:
    #    phi = np.random.uniform(0, 2.0*np.pi)
    #    eta = np.random.uniform(-1.6, 1.6)
    #    pt = np.random.uniform(2.0, 20.0)
    #    charge = np.sign(np.random.uniform(-1.0, 1.0))
    #    track = Track(0, 0, phi, eta, pt, charge)
    #    tracker.fullMeasurement(track)
    #    track.plot_track(ax1, ax2, ax3, ax4, 'r')
    #    track.plot_measurements(ax1, ax2, ax3, ax4, 'y*')
    #    counter = counter + 1
                  
           
    
    plt.show()



 
