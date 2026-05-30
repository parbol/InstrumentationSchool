from GenericTracker.src.Geometry.BarrelModule import BarrelModule
from GenericTracker.src.Geometry.BarrelTray import Tray
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
        self.nTrays = 0

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
    def addTray(self, tray):

        if tray.maxZ > self.Lz/2.0 or tray.minZ < -self.Lz/2.0 or tray.R >= self.R:
            logging.error('The tray is not fitting the layer')
            sys.exit()

        self.nTrays = self.nTrays + 1
        self.Trays.append(tray)
        
        logging.info('A tray has been added to the layer at position x: %d, y: %d, z: %d', tray.x, tray.y, tray.z)


    ########################################################################################################
    def makeTrayCrown(self, phiShift, NPhiModule, NPhiSize, zShift, NZModule, NZSize):

        if NPhiSize * NPhiModule > np.pi * 2.0:
            logging.error('The crown configuration is not correct')
            sys.exit()
        if NZSize * NZSize > self.Lz:
            logging.error('The crown configuration is not correct')
            sys.exit()

        trayWidth = 2.0 * self.R * np.sin(NPhiSize/2.0)
        trayLength = NZSize
        for i in range(NPhiModule):
            phi = phiShift + i * 2.0 * np.pi / NPhiModule
            x = self.R * np.cos(phi)
            y = self.R * np.sin(phi)
            for j in range(NZModule):
                zp = zShift + j * self.Lz / (NZModule/2.0)
                zm = -zShift - j * self.Lz / (NZModule/2.0)
                vx = np.asarray([np.sin(phi), -np.cos(phi), 0.0])
                vy = np.asarray([0.0, 0.0, 1.0])
                vz = np.asarray([np.cos(phi), np.sin(phi), 0.0])
                euler = EulerRotation()
                euler.setFromVectors(vx, vy, vz)
                tp = Tray(x, y, zp, euler, trayWidth, trayLength)
                tm = Tray(x, y, zm, euler, trayWidth, trayLength)









    
   