from GenericTrackerSimulator.src.Geometry.Module import Module
from GenericTrackerSimulator.src.Geometry.Tray import Tray
from GenericTrackerSimulator.src.Tools.EulerRotation import EulerRotation
import numpy as np
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)

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
        self.type = 0
        self.trackerIndex = -1
        self.barrelIndex = index
        self.diskIndex = -1
        
        # Barrel contains trays in the positive and negative sides
        self.npTrays = 0
        self.nnTrays = 0
        self.nTrays = []
        self.pTrays = []

        # Navigation
        self.connections = []

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

        tray.type = self.type
        if zside >= 0:
            tray.zside = 1
            tray.trayIndex = self.npTrays
            tray.barrelIndex = self.barrelIndex
            tray.trackerIndex = self.trackerIndex
            self.npTrays = self.npTrays + 1
            self.pTrays.append(tray)
        else:
            tray.zside = 0
            tray.trayIndex = self.nnTrays
            tray.barrelIndex = self.barrelIndex
            tray.trackerIndex = self.trackerIndex
            self.nnTrays = self.nnTrays + 1
            self.nTrays.append(tray)
        
        logging.info('A tray has been added to the layer at position x: %f, y: %f, z: %f', tray.x, tray.y, tray.z)


    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for tr in self.pTrays:
            tr.draw(ax1, ax2, ax3, ax4, t, alpha)
        for tr in self.nTrays:
            tr.draw(ax1, ax2, ax3, ax4, t, alpha)
        






    
   