from src.Plane import Plane
from src.Module import Module
from src.BTLTray import BTLTray
from src.EulerRotation import EulerRotation
from src.BTLId import BTLId
import numpy as np
import sys

class BarrelLayer:
    
    def __init__(self, radius, Lz, X0):

        ####################################################################################################
        #                                   Representation of a Barrel Layer                               #
        # radius:  Radius of the layer                                                                     # 
        # Lz:      Length in Z of the layer                                                                # 
        # X0:      Mean radiation length up to this layer                                                  # 
        ####################################################################################################
        self.R = radius
        self.Lz = Lz
        self.X0 = X0
        self.scattbase = (0.0136*0.0136) / X0
        self.nTrays = 0
        self.Trays = []


    ########################################################################################################
    def addTray(self, tray):

        self.nTrays = self.nTrays + 1
        self.Trays.append(tray)
    
    
    ########################################################################################################
    def getClosestTray(self, traj):

        # This method estimates which is the closest tray for a given trajectory
        intersection = traj.intersectBarrel
   
    ########################################################################################################
    def intersection(self, track):

        phi = track.phi
        eta = track.eta
        trays = []
        side = 0
        if eta >= 0:
            trays = self.pTrays
            side = 1
        else:
            trays = self.mTrays
            side = -1

        trayNumber = self.getClosestTray(phi, trays)
        navigationWindow = 2
        navigationList = []
        for i in range(0, navigationWindow+1):
            navigationList.append(i)
            if i != 0:
                navigationList.append(-i)
        for i in navigationList:
            checkTrayNumber = (trayNumber + i) % 36
            valid, id, point = trays[checkTrayNumber].intersection(track)
            if valid:
                return True, id, point, [3]
        return False, [], [], [3]


    def getBTLModule(self, detInfo):
        
        tray = detInfo.tray
        side = detInfo.side
        RU = detInfo.RU
        module = detInfo.module
       
        if side > 0:

            return self.pTrays[tray].RUs[RU].Modules[module]
        
        else:

            return self.mTrays[tray].RUs[RU].Modules[module]


    def getModule(self, detInfo):

        tray = detInfo.tray
        side = detInfo.side
        RU = detInfo.RU
        module = detInfo.module
       
        if side > 0:

            return self.pTrays[tray].RUs[RU].Modules[module].module
        
        else:

            return self.mTrays[tray].RUs[RU].Modules[module].module


    def writeGeometry(self, fileName):

        f = open(fileName, 'w')
        for tray in self.pTrays:
            for ru in tray.RUs:
                for module in ru.Modules:
                    module.write(f)
        for tray in self.mTrays:
            for ru in tray.RUs:
                for module in ru.Modules:
                    module.write(f)
        f.close()


    def readGeometry(self, fileName):

        f = open(fileName)
        for i in f.readlines():
            line = i.split()
            side = int(line[0])
            tray = int(line[1])
            RUType = int(line[2])
            RUNumber = int(line[3])
            module = int(line[4])
            btl = BTLId()
            btl.setSide(side)
            btl.setTray(tray)
            btl.setRU(RUType, RUNumber)
            btl.setModule(module)
            mod = self.getBTLModule(btl)
            x = float(line[5])
            y = float(line[6])
            z = float(line[7])
            psi = float(line[8])
            theta = float(line[9])
            phi = float(line[10])
            r = np.asarray([x, y, z])
            euler = EulerRotation(psi, theta, phi)
            mod.updatePosition(r, euler)
        f.close()

    def getScatteringMagnitude(self, dl, betamomentum):

        # This method calculates the real scattering suffered by
        # the muon when traversing distance dl of the voxel. It
        # returns the angular deviation and spatial displacement.     
        cov = self.scattbase/(betamomentum)**2 * np.matrix([[dl, dl*dl/2.0], [dl*dl/2.0, dl*dl*dl/3.0]])
        angle, disp = np.random.multivariate_normal([0,0], cov, 1)[0].T
        return angle, disp

    
    def fullMeasurement(self, track):
 
        #Intersection
        status, detInfo, v, det = self.intersection(track)
        if not status:
            return False
        x = np.asarray([v[0]])
        y = np.asarray([v[1]])
        z = np.asarray([v[2]])
        t = np.asarray([v[3]])

        xTracker = track.xi[len(track.xi)-1]
        yTracker = track.yi[len(track.yi)-1]
        zTracker = track.zi[len(track.zi)-1]
        vectorTracker = np.asarray([xTracker, yTracker, zTracker])

        track.xi = np.concatenate((track.xi, x), axis=0)
        track.yi = np.concatenate((track.yi, y), axis=0)
        track.zi = np.concatenate((track.zi, z), axis=0)
        track.ti = np.concatenate((track.ti, t), axis=0)
        track.det = track.det + det
        
        module = self.getModule(detInfo)
        detInfoList = [detInfo.side, detInfo.tray, detInfo.RUType, detInfo.RUNumber, detInfo.module]
        track.subdet = track.subdet + [detInfoList]
        globalVector = np.asarray([v[0], v[1], v[2]])
        localVector = module.toLocal(globalVector)
        lx = np.asarray([localVector[0]])
        ly = np.asarray([localVector[1]])
        lz = np.asarray([localVector[2]])
        track.lxi = np.concatenate((track.lxi, lx), axis=0)
        track.lyi = np.concatenate((track.lyi, ly), axis=0)
        track.lzi = np.concatenate((track.lzi, lz), axis=0)
        localX = localVector[0]
        localY = localVector[1]

        #Spatial uncertainty
        xunc = np.random.normal(0, self.rphi_error)
        yunc = np.random.normal(0, self.z_error)
        #Multiple scattering
        dl = np.linalg.norm(globalVector-vectorTracker)
        betamomentum = track.betamomentum
        xangle, xdisp = self.getScatteringMagnitude(dl, betamomentum)
        yangle, ydisp = self.getScatteringMagnitude(dl, betamomentum)
        localX += (xunc + xdisp)
        localY += (yunc + ydisp)
        localVector[0] = localX
        localVector[1] = localY
        newGlobalVector = module.toGlobal(localVector)
        
        #Time uncertainty
        var_t = np.random.normal(0, self.t_error)
        newt = v[3] + var_t


        x_meas = np.asarray([newGlobalVector[0]])
        y_meas = np.asarray([newGlobalVector[1]])
        z_meas = np.asarray([newGlobalVector[2]])
        lx_meas = np.asarray([localVector[0]])
        ly_meas = np.asarray([localVector[1]])
        lz_meas = np.asarray([localVector[2]])
        t_meas = np.asarray([newt])
        

        track.xm = np.concatenate((track.xm, x_meas), axis=0)
        track.ym = np.concatenate((track.ym, y_meas), axis=0)
        track.zm = np.concatenate((track.zm, z_meas), axis=0)
        track.tm = np.concatenate((track.tm, t_meas), axis=0)
        track.lxm = np.concatenate((track.lxm, lx_meas), axis=0)
        track.lym = np.concatenate((track.lym, ly_meas), axis=0)
        track.lzm = np.concatenate((track.lzm, lz_meas), axis=0)
        if not module.isInside(localVector):
            return False
        return True
      

    def draw(self, ax1, ax2, ax3, ax4, t):

        for m in self.pTrays:
            m.draw(ax1, ax2, ax3, ax4, t)
        for m in self.mTrays:
            m.draw(ax1, ax2, ax3, ax4, t)


             









