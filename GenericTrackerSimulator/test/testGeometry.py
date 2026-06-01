from GenericTrackerSimulator.src.Geometry.FullTracker import FullTracker
from GenericTrackerSimulator.src.Geometry.Tracker import Tracker
from GenericTrackerSimulator.src.Geometry.BarrelLayer import BarrelLayer
import matplotlib.pyplot as plt
import numpy as np




if __name__=='__main__':


    #Set barrel layers of the first tracker
    tr = Tracker(barrelMinR = 9.0, barrelMaxR = 38.0, barrelLZ = 71, 
                 endcapMinR =9.0, endcapMaxR = 38.0, 
                 endcapMinZ = 36.0, endcapMaxZ = 50.0)
    
    for i in range(4):

        phiShift = 0.0
        if i % 2 != 0:
            phiShift = np.pi/24.0
        r = 10 + 5 * i
        Lz = 70.0
        X0 = 25.0
        bLayer = BarrelLayer(radius=r, Lz = Lz, X0 = X0, index=i)
        PhiTraySize = np.pi/12.0
        ZTraySize = (Lz-1)/2.0
        lsize = 2.0 * r * np.sin(PhiTraySize/2.0)
        wSizeModule = 2.0
        nWModules = int(np.floor(lsize/wSizeModule))
        lSizeModule = 10.0
        nLModules = int(np.floor(ZTraySize/lSizeModule))
        bLayer.makeTraysAllAround(phiShift = phiShift, NPhiTray = 24, 
                                  PhiTraySize = PhiTraySize, zShift = 0.1, 
                                  NZTray = 2, ZTraySize = ZTraySize,
                                  nWModules = nWModules, nLModules= nLModules,
                                  wSizeModule = wSizeModule, lSizeModule = lSizeModule)
        tr.addBarrelLayer(bLayer)

        
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

    tr.draw(ax1, ax2, ax3, ax4, t='b--')
    plt.show()
