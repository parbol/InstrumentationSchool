from GenericTrackerSimulator.src.Tools.Plane import Plane
from GenericTrackerSimulator.src.Geometry.Module import Module
import numpy as np
import math
import sys
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)



class Tray:
    
    def __init__(self, x, y, z, euler, TrayWidth, TrayLength):

        # Position of the tray
        self.x = x
        self.y = y
        self.z = z
        self.r = np.asarray([x, y, z])
        # Orientation of the tray
        self.vx = euler.apply(np.asarray([1.0, 0.0, 0.0]))
        self.vy = euler.apply(np.asarray([0.0, 1.0, 0.0]))
        self.vz = euler.apply(np.asarray([0.0, 0.0, 1.0]))
        self.eulerAngles = euler
        self.plane = Plane(self.x, self.y, self.z, self.vz[0], self.vz[1], self.vz[2])


        # Information of ID
        self.type = -1
        self.zside = -1
        self.trayIndex = -1
        self.barrelIndex = -1
        self.diskIndex = -1
        self.trackerIndex = -1
        
        # Information of tray dimensions
        self.TrayWidth = TrayWidth
        self.TrayLength = TrayLength
        self.maxZ = z + self.TrayLength / 2.0
        self.minZ = z - self.TrayLength / 2.0 
        
        # Module content
        self.nModules = 0
        self.modules = []

        if self.TrayWidth <= 0:
            logging.error('The tray width cannot be a negative number')
            sys.exit()
        if self.TrayLength <= 0:
            logging.error('The tray length cannot be a negative number')
            sys.exit()
              
        logging.info('Setting up a tray at position x: %f, y: %f, z: %f and width: %f, length: %f', self.x, self.y, self.z, self.TrayWidth, self.TrayLength)

    ########################################################################################################
    def addModule(self, module):

        #####Add here warnings and protections
       
        module.moduleIndex = self.nModules
        module.trayIndex = self.trayIndex
        module.barrelIndex = self.barrelIndex
        module.diskIndex = self.diskIndex
        module.trackerIndex = self.trackerIndex
        module.type = self.type
        module.zside = self.zside
        self.modules.append(module)
        self.nModules = self.nModules + 1

        logging.info('A module has been added at position x: %f, y: %f, z: %f', module.x, module.y, module.z)
   
 
    ########################################################################################################
    def toGlobal(self, v):

        return self.r + self.eulerAngles.apply(v)


    ########################################################################################################
    def toLocal(self, v):

        return self.eulerAngles.applyInverse(v - self.r)
    

    ########################################################################################################
    def isInside(self, p):
        print('TrayWidth', self.TrayWidth/2.0, 'TrayLength', self.TrayLength/2.0)
        print(p)
        if p[0] < -self.TrayWidth/2.0 or p[0] > self.TrayWidth/2.0:
            return False
        if p[1] < -self.TrayLength/2.0 or p[1] > self.TrayLength/2.0:
            return False
        return True

 
    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for m in self.modules:
            m.draw(ax1, ax2, ax3, ax4, t, alpha)

             









