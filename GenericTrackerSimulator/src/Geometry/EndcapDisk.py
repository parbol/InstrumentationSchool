from GenericTrackerSimulator.src.Geometry.Module import Module
from GenericTrackerSimulator.src.Geometry.Tray import Tray
from GenericTrackerSimulator.src.Tools.EulerRotation import EulerRotation
import numpy as np
import sys
import logging

logger = logging.getLogger(__name__)

class EndcapDisk:
    
    def __init__(self, radius, z, X0, index):

        ####################################################################################################
        #                               Representation of an Endcap Disk                                   #
        # radius:  Radius of the disk                                                                      # 
        # z:       z position                                                                              # 
        # X0:      Mean radiation length up to this layer                                                  # 
        ####################################################################################################
        self.R = radius
        self.z = z
        self.X0 = X0
        self.endcapIndex = index

        # Barrel Layer Id
        self.trackerIndex = 0
        
        # Barrel contains trays in the positive and negative Ds
        self.npTrays = 0
        self.nnTrays = 0
        self.nTrays = []
        self.pTrays = []

        # Sanity checks for barrel information
        if self.R <= 0:
            logging.error('The radius of an endcap disk cannot be negative')
            sys.exit()
        if self.Lz <= 0:
            logging.error('The length of an endcap disk cannot be negative')
            sys.exit()
        if self.X0 <= 0:
            logging.error('The radiation length cannot be negative')
            sys.exit()
        
        logging.info('Setting up a disk with radius: %f, z pos: %f and radiation length: %f', self.R, self.z, self.X0)


    ########################################################################################################
    def addTray(self, tray, zside):

        if tray.TrayLength > self.Lz/2.0:
            logging.error('The tray is not fitting the layer')
            sys.exit()

        if zside >= 0:
            tray.type = 1
            tray.zside = 1
            tray.trayIndex = self.npTrays
            tray.barrelIndex = self.barrelIndex
            tray.trackerIndex = self.trackerIndex
            self.npTrays = self.npTrays + 1
            self.pTrays.append(tray)
        else:
            tray.type = 1
            tray.zside = 0
            tray.trayIndex = self.nnTrays
            tray.barrelIndex = self.barrelIndex
            tray.trackerIndex = self.trackerIndex
            self.nnTrays = self.nnTrays + 1
            self.nTrays.append(tray)
        
        logging.info('A tray has been added to the layer at position x: %f, y: %f, z: %f', tray.x, tray.y, tray.z)


    ########################################################################################################
    def makeTraysInDisk(self, xShift, NXTray, xTraySize,
                           nWModules, nLModules, wSizeModule, lSizeModule):

        ########################################################################################################
        # This method creates Trays at different positions in Phi
        # xShift: Initial displacement of the first tray
        # NXTray: Number of x trays
        # xTraySize: Size of the tray in Z
        # nWModules: Number of modules in the phi direction
        # nLModules: Number of modules in the longitudinal direction
        # wSizeModule: Size of the modules in the phi direction
        # lSizeModule: Size of the modules in the longitudinal direction
        ########################################################################################################
        
        # Sanity checks on the geometry of the trays
        if xShift + NXTray/2.0 * xTraySize > self.R:
            logging.error('The configuration of trays is not correct in the disk')
            sys.exit()
        
        xSpaceBetweenTrays = (self.R - xShift - NXTray * xTraySize)/ (NXTray/2) 
        for i in range(int(NXTray/2)):
            xp = xShift + (xTraySize/2.0) + i * (xTraySize+xSpaceBetweenTrays)
            xm = -xShift - (xTraySize/2.0) - i * (xTraySize+xSpaceBetweenTrays)
            xpmax = xp + xTraySize/2.0
            xmmin = xp - xTraySize/2.0
            
            phi = (phiShift + PhiTraySize/2.0) + i * (PhiTraySize + phiSpaceBetweenTrays)
            x = self.R * np.cos(phi)
            y = self.R * np.sin(phi)
            for j in range(int(np.floor(NZTray/2))):
                zp = (zShift + ZTraySize/2.0) + j * (ZTraySize + zSpaceBetweenTrays)
                zm = -(zShift + ZTraySize/2.0) - j * (ZTraySize + zSpaceBetweenTrays)                
                vx = np.asarray([np.sin(phi), -np.cos(phi), 0.0])
                vz = np.asarray([np.cos(phi), np.sin(phi), 0.0])
                vy = np.cross(vz, vx)
                euler = EulerRotation()
                euler.setFromVectors(vx, vy, vz)
                
                # Create the trays through the center rotation and size
                tp = Tray(x = x, y = y, z = zp, euler = euler, TrayWidth = trayWidth, TrayLength = trayLength)
                tp.makeModulesInBarrelTray(nWModules, nLModules, wSizeModule, lSizeModule)
                tm = Tray(x = x, y = y, z = zm, euler = euler, TrayWidth = trayWidth, TrayLength = trayLength)
                tm.makeModulesInBarrelTray(nWModules, nLModules, wSizeModule, lSizeModule)
                self.addTray(tp, 1)
                self.addTray(tm, 0)

    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for tr in self.pTrays:
            tr.draw(ax1, ax2, ax3, ax4, t, alpha)
        for tr in self.nTrays:
            tr.draw(ax1, ax2, ax3, ax4, t, alpha)
        






    
   