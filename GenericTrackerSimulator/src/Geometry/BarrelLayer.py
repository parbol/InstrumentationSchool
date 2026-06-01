from GenericTrackerSimulator.src.Geometry.Module import Module
from GenericTrackerSimulator.src.Geometry.Tray import Tray
from GenericTrackerSimulator.src.Tools.EulerRotation import EulerRotation
import numpy as np
import sys
import logging

logger = logging.getLogger(__name__)

class BarrelLayer:
    
    def __init__(self, radius, Lz, X0, index):

        ####################################################################################################
        #                                   Representation of a Barrel Layer                               #
        # radius:  Radius of the layer                                                                     # 
        # Lz:      Length in Z of the layer                                                                # 
        # X0:      Mean radiation length up to this layer                                                  # 
        ####################################################################################################
        self.R = radius
        self.Lz = Lz
        self.X0 = X0
        self.barrelIndex = index

        # Barrel Layer Id
        self.trackerIndex = 0
        self.barrelIndex = 0
        
        # Barrel contains trays in the positive and negative sides
        self.npTrays = 0
        self.nnTrays = 0
        self.nTrays = []
        self.pTrays = []

        # Sanity checks for barrel information
        if self.R <= 0:
            logging.error('The radius of a barrel layer cannot be negative')
            sys.exit()
        if self.Lz <= 0:
            logging.error('The length of a barrel layer cannot be negative')
            sys.exit()
        if self.X0 <= 0:
            logging.error('The radiation length cannot be negative')
            sys.exit()
        
        logging.info('Setting up a layer with radius: %d, length: %d and radiation length: %d', self.R, self.Lz, self.X0)


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
    def makeTraysAllAround(self, phiShift, NPhiTray, PhiTraySize, zShift, NZTray, ZTraySize,
                           nWModules, nLModules, wSizeModule, lSizeModule):

        ########################################################################################################
        # This method creates Trays at different positions in Phi
        # phiShift: Initial displacement of the first tray
        # NPhiTray: Number of trays
        # PhiTraySize: Angular size of the tray
        # zShift: Initial displacement of the first tray in Z
        # NZTray: Number of Z trays
        # ZTraySize: Size of the tray in Z
        # nWModules: Number of modules in the phi direction
        # nLModules: Number of modules in the longitudinal direction
        # wSizeModule: Size of the modules in the phi direction
        # lSizeModule: Size of the modules in the longitudinal direction
        ########################################################################################################
        
        # Sanity checks on the geometry of the trays
        if PhiTraySize * NPhiTray > np.pi * 2.0:
            logging.error('The configuration of trays is not correct in phi')
            sys.exit()
        
        if ZTraySize * NZTray + 2.0 * zShift> self.Lz:
            logging.error('The configuration of trays is not correct in Z')
            sys.exit()


        trayWidth = 2.0 * self.R * np.sin(PhiTraySize/2.0)
        phiSpaceBetweenTrays = (2.0 * np.pi - PhiTraySize * NPhiTray) / NPhiTray 
        print('phiSpaceBetweenTrays', phiSpaceBetweenTrays)
        trayLength = ZTraySize
        zSpaceBetweenTrays = ((self.Lz / 2.0) - zShift) / (NZTray/2)
        for i in range(NPhiTray):
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
        






    
   