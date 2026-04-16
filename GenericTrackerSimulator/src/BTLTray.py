from src.Plane import Plane
from src.Module import Module
from src.BTLRU import BTLRU
from src.BTLId import BTLId

import numpy as np
import sys



class BTLTray:
    
    def __init__(self, btlId, x, y, z, euler, TrayWidth, TrayLength, RULength, ModuleLength, ModuleWidth):

        self.r = np.asarray([x, y, z])
        sinphi = (self.r[1]/np.sqrt(self.r[0]**2+self.r[1]**2)) 
        cosphi = (self.r[0]/np.sqrt(self.r[0]**2+self.r[1]**2))
        if cosphi > 1.0:
            cosphi = 1.0
        if cosphi < -1.0:
            cosphi = -1.0
        if sinphi >= 0:
            self.phi = np.arccos(cosphi)
        else:
            self.phi = -np.arccos(cosphi) + 2.0*np.pi
        normal = np.asarray([self.r[0], self.r[1], 0.0])
        self.n = normal/np.linalg.norm(normal)
        self.btlId = btlId
        self.TrayWidth = TrayWidth
        self.TrayLength = TrayLength
        self.RULength = RULength
        self.ModuleLength = ModuleLength
        self.ModuleWidth = ModuleWidth 
        self.eulerAngles = euler
        self.plane = Plane(self.r[0], self.r[1], self.r[2], self.n[0], self.n[1], self.n[2])
        self.RUSpace = (self.TrayLength - 6.0 * self.RULength)/5.0
        self.zFirstRU = np.abs(z) - TrayLength/2.0 + self.RULength/2.0
        if self.btlId.side == -1:
            self.zFirstRU = -1.0 * self.zFirstRU
        self.RUs = []
        for rutype in range(0, 3):
            for runumber in range(0,2):
                pos = rutype*2 + runumber
                btl = BTLId()
                btl.setTray(self.btlId.tray)
                btl.setSide(self.btlId.side)
                btl.setRU(rutype,runumber)
                ru = BTLRU(btl, x, y, self.zFirstRU + btl.side * pos *(self.RULength + self.RUSpace), self.eulerAngles, self.TrayWidth, self.RULength, self.ModuleLength, self.ModuleWidth)
                self.RUs.append(ru)


    def intersection(self, track):
        
        valid, x, y, z, t = self.plane.intersection(track)
        x2 = track.pt * np.cos(track.phi)
        y2 = track.pt * np.sin(track.phi)
        z2 = track.pz
        #print("Momentum", x2, y2, z2)
        #print(track.pt * np.cos(track.phi), track.pt*np.sin(track.phi), track.pz)
        #print(self.plane.p, self.plane.n)
        #print(x, y, z, t, valid)
        for m in self.RUs:
            d = np.abs(z - m.r[2])
            if d <= m.RULength/2.0:
                valid, moduleId, point = m.intersection(x, y, z, track)
                if valid:
                    return True, moduleId, point
        return False, [], []



    def draw(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for m in self.RUs:
            m.draw(ax1, ax2, ax3, ax4, t, alpha)

             









