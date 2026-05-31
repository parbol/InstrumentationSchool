from GenericTracker.src.Geometry.Module import Module
from GenericTracker.src.Geometry.Tray import Tray
from GenericTracker.src.Tools.EulerRotation import EulerRotation
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
        
        logging.info('A tray has been added to the layer at position x: %d, y: %d, z: %d', tray.x, tray.y, tray.z)


    ########################################################################################################
    def makeTraysAllAround(self, phiShift, NPhiTray, NPhiSize, zShift, NZTray, NZSize,
                           nWModules, nLModules, wSizeModule, lSizeModule):

        ########################################################################################################
        # This method creates Trays at different positions in Phi
        # phiShift: Initial displacement of the first tray
        # NPhiTray: Number of trays
        # NPhiSize: Angular size of the tray
        # zShift: Initial displacement of the first tray in Z
        # NZTray: Number of Z trays
        # nWModules: Number of modules in the phi direction
        # nLModules: Number of modules in the longitudinal direction
        # wSizeModule: Size of the modules in the phi direction
        # lSizeModule: Size of the modules in the longitudinal direction
        ########################################################################################################
        
        # Sanity checks on the numbers
        if NPhiSize * NPhiTray > np.pi * 2.0:
            logging.error('The configuration of trays is not correct')
            sys.exit()
        if NZSize * NZTray + 2.0 * zShift> self.Lz:
            logging.error('The configuration of trays is not correct')
            sys.exit()

        trayWidth = 2.0 * self.R * np.sin(NPhiSize/2.0)
        trayLength = NZSize
        for i in range(NPhiTray):
            phi = phiShift + NPhiSize/2.0 + i * 2.0 * np.pi / NPhiTray
            x = self.R * np.cos(phi)
            y = self.R * np.sin(phi)
            for j in range(NZTray):
                zp = zShift + NZSize/2.0 + j * self.Lz / (NZTray/2.0)
                zm = -zShift + NZSize/2.0 - j * self.Lz / (NZTray/2.0)
                vx = np.asarray([np.sin(phi), -np.cos(phi), 0.0])
                vy = np.asarray([0.0, 0.0, 1.0])
                vz = np.asarray([np.cos(phi), np.sin(phi), 0.0])
                euler = EulerRotation()
                euler.setFromVectors(vx, vy, vz)
                # Create the trays through the center rotation and size
                tp = Tray(x, y, zp, euler, trayWidth, trayLength)
                tp.makeModulesInBarrelTray(nWModules, nLModules, wSizeModule, lSizeModule)
                tm = Tray(x, y, zm, euler, trayWidth, trayLength)
                tm.makeModulesInBarrelTray(nWModules, nLModules, wSizeModule, lSizeModule)
                self.addTray(tp, 1)
                self.addTray(tm, 0)









    
   