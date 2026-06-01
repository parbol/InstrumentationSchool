from GenericTracker.src.Tools.Plane import Plane
from GenericTracker.src.Geometry.Module import Module
import numpy as np
import math
import sys
import logging
logger = logging.getLogger(__name__)



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
        self.type = 0
        self.zside = 0
        self.trayIndex = 0
        self.barrelIndex = 0
        self.trackerIndex = 0
        
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
              
        logging.info('Setting up a tray at position x: %d, y: %d, z: %d and width: %d, length: %d', self.x, self.y, self.z, self.TrayWidth, self.TrayLength)

    ########################################################################################################
    def addModule(self, module):

        #####Add here warnings and protections
       
        module.moduleIndex = self.nModules
        self.modules.append(module)
        self.nModules = self.nModules + 1

        logging.info('A module has been added at position x: %d, y: %d, z: %d', module.x, module.y, module.z)
   
 
    ########################################################################################################
    def makeModulesInBarrelTray(self, nWModules, nLModules, wSizeModule, lSizeModule):

        if nWModules * wSizeModule > self.TrayWidth or nLModules * lSizeModule > self.TrayLength:
            logging.error('The module configuration is not correct')
            sys.exit()
        stepWidth = self.TrayWidth / nWModules
        stepLength = self.TrayLength / nLModules    
        for ix in range(nWModules):
            for iz in range(nLModules):
                rmod = self.r
                rmin = (-self.TrayWidth/2.0 + stepWidth/2.0) * self.vx + (-self.TrayLength/2.0 + stepLength/2.0) * self.vy 
                rmod = rmin + ix * self.vx + iz * self.vy
                m = Module(rmod[0], rmod[1], rmod[2], wSizeModule, lSizeModule, self.eulerAngles)
                m.trackerIndex = self.trackerIndex
                m.barrelIndex = self.barrelIndex
                m.endcapIndex = self.endcapIndex
                m.type = self.type
                m.zside = self.zside         
                self.addModule(m)

 
    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for m in self.RUs:
            m.draw(ax1, ax2, ax3, ax4, t, alpha)

             









