from GenericTrackerSimulator.src.Geometry.Module import Module
from GenericTrackerSimulator.src.Geometry.Tray import Tray
from GenericTrackerSimulator.src.Tools.EulerRotation import EulerRotation
import numpy as np
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)

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
        self.diskIndex = index

        # Barrel Layer Id
        if z > 0:
            self.type = 1
        else:
            self.type = -1
        self.trackerIndex = 0
        self.barrelIndex = -1

        # Barrel contains trays in the positive and negative Ds
        self.nTrays = 0
        self.Trays = []
        
        # Navigation
        self.connections = []

        # Sanity checks for barrel information
        if self.R <= 0:
            logging.error('The radius of an endcap disk cannot be negative')
            sys.exit()
    
        if self.X0 <= 0:
            logging.error('The radiation length cannot be negative')
            sys.exit()
        
        logging.info('Setting up a disk with radius: %f, z pos: %f and radiation length: %f', self.R, self.z, self.X0)



    ########################################################################################################
    def addTray(self, tray):

        tray.type = self.type
        if self.z >= 0:
            tray.zside = 1
        else:
            tray.zside = 0
        tray.trayIndex = self.nTrays
        tray.diskIndex = self.diskIndex
        tray.trackerIndex = self.trackerIndex
        self.nTrays = self.nTrays + 1
        self.Trays.append(tray)
        
        logging.info('A tray has been added to the disk at position x: %f, y: %f, z: %f', tray.x, tray.y, tray.z)


    

    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for tr in self.Trays:
            tr.draw(ax1, ax2, ax3, ax4, t, alpha)
       




    
   