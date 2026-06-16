import numpy as np
import sys

from GenericTrackerSimulator.src.Propagation.trajectoryState import trajectoryState
from scipy import optimize

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)

class Plane:

    def __init__(self, x0, y0, z0, nx, ny, nz):
        
        self.p = np.asarray([x0, y0, z0])
        self.n = np.asarray([nx, ny, nz])
        s = self.norm(self.n)
        if s < 1e-5:
            logging.error('Bad plane definition')
            sys.exit()
        self.n = self.n / s
        self.rotMatrix()

    def updatePosition(self, x0, y0, z0, nx, ny, nz):

        self.p = np.asarray([x0, y0, z0])
        self.n = np.asarray([nx, ny, nz])
        s = self.norm(self.n)
        if s < 1e-5:
            logging.error('Bad plane definition')
            sys.exit()
        self.n = self.n / s
        self.rotMatrix()

    def norm(self, v):
        return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    
    def phi(self):

        return np.arctan2(self.n[1], self.n[0])
    
    def theta(self):

        return np.arccos(self.n[2])
    
    def rotMatrix(self):
        cosphi = np.cos(self.phi())
        sinphi = np.sin(self.phi())
        costheta = np.cos(self.theta())
        sintheta = np.sin(self.theta())
        mat = [[cosphi*costheta, -sinphi, cosphi*sintheta],
               [sinphi*costheta, cosphi, sinphi*sintheta],
               [-sintheta, 0.0, costheta]]
       
        self.rot = np.asmatrix(mat)
        self.invrot = np.linalg.inv(self.rot)

    def intersection(self, B, ts):

        # Angular frequency of the helix
        w = ts.q * 0.089880 * B / (ts.gamma * ts.m)
        # Curvature radius
        r = ts.vT/w
        # phi
        phi0 = ts.phi
        # vz
        vz = ts.vZ
        # vector
        x0 = ts.x
        y0 = ts.y
        z0 = ts.z
        t0 = ts.t
        def fmin(t):
        
            A = self.n[0]
            B = self.n[1]
            C = self.n[2]
            D = -(A*self.p[0]+B*self.p[1]+C*self.p[2])
            x = r * (np.sin(w*t - phi0) + np.sin(phi0)) + x0
            y = r * (np.cos(w*t - phi0) - np.cos(phi0)) + y0
            z = vz * t + z0
            return A * x + B * y + C * z + D
        
    
        t_min = 0.01
        step = 0.01 
        tl = t_min + step
        t_max = 30.0
        while fmin(t_min) * fmin(tl) > 0:
            tl = tl + step
            if tl > t_max:
                return None, False
        t_min = tl - 2.0 * step
        t_max = tl + 2.0 * step
        s = optimize.brentq(fmin, t_min, t_max, full_output=True, disp=True)
        t = s[0]
        x = r * (np.sin(w*t - phi0) + np.sin(phi0)) + x0
        y = r * (np.cos(w*t - phi0) - np.cos(phi0)) + y0
        z = vz * t + z0
        phi = -w * t + phi0
        t = t + t0
        newTraj = trajectoryState(x = x, y = y, z = z, t = t, phi = phi, eta = ts.eta, E = ts.E, q = ts.q, beta= ts.beta)       
        if self.belongsToPlane(x, y, z):
            return newTraj, True
        else:
            return None, False


    def intersectionStraight(self, x0, y0, z0, vx, vy, vz):

        A = self.n[0]
        B = self.n[1]
        C = self.n[2]
        D = -(A*self.p[0]+B*self.p[1]+C*self.p[2])
        Delta = A * x0 + B * y0 + C * z0
        Kapa = A * vx + B * vy + C * vz
        t = (-Delta-D)/Kapa
        x = x0 + vx * t
        y = y0 + vy * t
        z = z0 + vz * t
        return x, y, z
    
    def belongsToPlane(self, x, y, z):

        A = self.n[0]
        B = self.n[1]
        C = self.n[2]
        D = -(A*self.p[0]+B*self.p[1]+C*self.p[2])
        k = A * x + B * y + C *z + D
        if np.abs(k) < 1e-3:
            return True
        return False
