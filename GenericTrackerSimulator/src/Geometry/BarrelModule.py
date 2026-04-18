from src.Tools.EulerRotation import EulerRotation
from src.Tools.Plane import Plane

import numpy as np
import math
import sys
import logging
logger = logging.getLogger(__name__)



class BarrelModule:

    def __init__(self, x, y, z, Lx, Ly, euler):

        self.x = x
        self.y = y
        self.z = z

        self.Lx = Lx
        self.Ly = Ly
        
        self.eulerAngles = euler
        self.r = np.asarray()
        z = np.asarray([0.0, 0.0, 1.0])
        n = self.eulerAngles.apply(z)
        self.pLLlocal = np.asarray([-Lx/2.0, -Ly/2.0, 0.0]) 
        self.pLRlocal = np.asarray([Lx/2.0, -Ly/2.0, 0.0]) 
        self.pULlocal = np.asarray([-Lx/2.0, Ly/2.0, 0.0]) 
        self.pURlocal = np.asarray([Lx/2.0, Ly/2.0, 0.0])

        self.plane = Plane(x[0], x[1], x[2], n[0], n[1], n[2]) 
        self.pLL = self.toGlobal(self.pLLlocal)
        self.pLR = self.toGlobal(self.pLRlocal)
        self.pUL = self.toGlobal(self.pULlocal)
        self.pUR = self.toGlobal(self.pURlocal)


    def toGlobal(self, v):

        return self.x + self.eulerAngles.apply(v)



    def toLocal(self, v):

        return self.eulerAngles.applyInverse(v - self.x)
    


    def isInside(self, p):

        if p[0] < -self.Lx/2.0 or p[0] > self.Lx/2.0:
            return False
        if p[1] < -self.Ly/2.0 or p[1] > self.Ly/2.0:
            return False
        return True
    




 def drawModule(self, ax1, ax2, ax3, ax4, t, alpha=0.2):

        x_start = [self.pLL[0], self.pLR[0], self.pUR[0], self.pUL[0], self.pLL[0]]
        y_start = [self.pLL[1], self.pLR[1], self.pUR[1], self.pUL[1], self.pLL[1]]
        z_start = [self.pLL[2], self.pLR[2], self.pUR[2], self.pUL[2], self.pLL[2]]
        ax1.plot3D(x_start , z_start, y_start, t, alpha=alpha)
        ax2.plot(x_start, y_start, t, alpha=alpha)
        ax3.plot(z_start, y_start, t, alpha=alpha)
        ax4.plot(z_start, x_start, t, alpha=alpha)