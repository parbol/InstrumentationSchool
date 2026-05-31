from GenericTracker.src.Tools.Plane import Plane
from GenericTracker.src.Geometry.Module import Module
import numpy as np
import math
import sys
import logging
logger = logging.getLogger(__name__)



class Tray:
    
    def __init__(self, x, y, z, euler, TrayWidth, TrayLength, nxModules, nyModules, xSizeModule, ySizeModule):

        self.x = x
        self.y = y
        self.z = z
        self.r = np.asarray([x, y, z])
        normal = np.asarray([self.r[0], self.r[1], 0.0])
        self.n = normal/np.linalg.norm(normal)
        vn = np.asarray([-self.n[1], self.n[0], 0.0])
        self.vn = vn/np.linalg.norm(vn)    
        self.nxModules = nxModules
        self.nyModules = nyModules
        self.xSizeModules = xSizeModule
        self.ySizeModules = ySizeModule
        self.type = 0
        self.zside = 0
        self.trayIndex = 0
        self.barrelIndex = 0
        self.trackerIndex = 0
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
       
        module.moduleIndex = self.nModules
        self.modules.append(module)
        self.nModules = self.nModules + 1

        logging.info('A module has been added at position x: %d, y: %d, z: %d', module.x, module.y, module.z)
   

    def makeModulesInBarrelTray(self, nWModules, nLModules, wSizeModule, lSizeModule):

        if nWModules * wSizeModule > self.TrayWidth or nLModules * lSizeModule > self.TrayLength:
            logging.error('The module configuration is not correct')
            sys.exit()
        stepWidth = self.TrayWidth / nWModules
        stepLength = self.TrayLength / nLModules    
        for ix in range(nWModules):
            for iz in range(nLModules):
                x = self.x + (-self.TrayWidth/2.0 + (ix * stepWidth + stepWidth/2.0)) * self.vn[0]
                y = self.y + (-self.TrayWidth/2.0 + (ix * stepWidth + stepWidth/2.0)) * self.vn[1]
                z = self.z + (-self.TrayLength/2.0 + (iz * stepLength + stepLength/2.0))
                m = Module(x, y, z, wSizeModule, lSizeModule, self.eulerAngles)
                m.trackerIndex = self.trackerIndex
                m.barrelIndex = self.barrelIndex
                m.endcapIndex = self.endcapIndex
                m.type = self.type
                m.zside = self.zside         
                self.addModule(m)



    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for m in self.RUs:
            m.draw(ax1, ax2, ax3, ax4, t, alpha)

             









