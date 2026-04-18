from src.Tools.Plane import Plane
from src.Geometry.BarrelModule import BarrelModule

import math
import sys
import logging
logger = logging.getLogger(__name__)



class Tray:
    
    def __init__(self, btlId, x, y, z, euler, TrayWidth, TrayLength):

        self.x = x
        self.y = y
        self.z = z
        self.R = math.sqrt(x**2 + y**2)
        self.nx = x / self.R
        self.ny = y / self.R
        self.TrayWidth = TrayWidth
        self.TrayLength = TrayLength
        self.maxZ = z + self.TrayLength / 2.0
        self.minZ = z - self.TrayLength / 2.0 
        self.eulerAngles = euler
        self.plane = Plane(self.x, self.y, self.z, self.nx, self.ny, 0.0)
        self.nModules = 0
        self.modules = []

        if self.TrayWidth <= 0:
            logging.error('The tray width cannot be a negative number')
            sys.exit()
        if self.TrayLength <= 0:
            logging.error('The tray length cannot be a negative number')
            sys.exit()
              
        logging.info('Setting up a tray at position x: %d, y: %d, z: %d and width: %d, length: %d', self.x, self.y, self.z, self.TrayWidth, self.TrayLength)



    def addModule(self, module):

        #####Add here warnings and protections
        
        self.modules.append(module)
        self.nModules = self.nModules + 1

        logging.info('A module has been added at position x: %d, y: %d, z: %d', module.x, module.y, module.z)
   


    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for m in self.RUs:
            m.draw(ax1, ax2, ax3, ax4, t, alpha)

             









