import numpy as np
import sys
from scipy import optimize

from TrackerSimulator.src.Track import Track

class Plane:

    def __init__(self, x0, y0, z0, nx, ny, nz):
        
        self.p = np.asarray([x0, y0, z0])
        self.n = np.asarray([nx, ny, nz])
        s = self.norm(self.n)
        if s < 1e-5:
            print('Bad plane definition')
            sys.exit()
        self.n = self.n / s
        self.rotMatrix()

    def updatePosition(self, x0, y0, z0, nx, ny, nz):

        self.p = np.asarray([x0, y0, z0])
        self.n = np.asarray([nx, ny, nz])
        s = self.norm(self.n)
        if s < 1e-5:
            print('Bad plane definition')
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

    def intersection(self, track):

        def fmin(t):
        
            A = self.n[0]
            B = self.n[1]
            C = self.n[2]
            D = -(A*self.p[0]+B*self.p[1]+C*self.p[2])
            r = track.rt
            w = track.w
            phi = track.phi
            pzct = (29.98/(track.gamma*track.m)) * track.pz
            x0 = track.x_c
            y0 = track.y_c
            z0 = track.dz
            Delta = A * x0 + B * y0 + C * z0
            return Delta + D + A * r * np.sin(w*t-phi) + B * r * np.cos(w*t-phi) + C * pzct * t
    
    
        
        #t_min = (track.gamma*track.m) / (29.98*track.pz) * (z_min - track.dz)
        #t_max = (track.gamma*track.m) / (29.98*track.pz) * (z_max - track.dz)
        #ftmin = fmin(t_min)

        t_min = 0.0
        t_max = 14.0
        if fmin(t_min) * fmin(t_max) > 0:
            return False, -1.0, -1.0, -1.0, -1.0
        s = optimize.brentq(fmin, t_min, t_max, full_output=True, disp=True)
        t = s[0]
        x,y,z = track.eval(t)           
        if self.belongsToPlane(x, y, z):
            return True, x, y, z, t
        else:
            return False, x, y, z, t


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
