from GenericTrackerSimulator.src.Geometry.FullTracker import FullTracker
from GenericTrackerSimulator.src.Geometry.Tracker import Tracker
from GenericTrackerSimulator.src.Geometry.BarrelLayer import BarrelLayer
from GenericTrackerSimulator.src.Geometry.EndcapDisk import EndcapDisk
from GenericTrackerSimulator.src.Geometry.Tray import Tray
from GenericTrackerSimulator.src.Geometry.Module import Module
from GenericTrackerSimulator.src.Tools.EulerRotation import EulerRotation
import numpy as np
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)



class GeometryBuilder:
    
    #####################################################################################
    # This class builds a tracker geometry: it can be tuned to get different geometries #
    # The geometry will be dumped into a json file with all the information .           #
    #####################################################################################

    def __init__(self):

        # All units are in cm
        self.ftr = FullTracker()
        
        tr = Tracker(barrelMinR = 9.0, barrelMaxR = 31.0, barrelLZ = 71, 
                    endcapMinR = 9.0, endcapMaxR = 31.0, 
                    endcapMinZ = 72.0, endcapMaxZ = 130.0)
        
        #################################################################################
        # Looping on the barrel layers                                                  #
        #################################################################################
        NLayers = 4
        for i in range(NLayers):
            # Phi information
            NPhiTray = 24
            phiShift = 0.0
            if i % 2 != 0:
                phiShift = np.pi/24.0
            PhiTraySize = np.pi/12.0
            
            # Z Information
            NZTray = 2
            zShift = 0.1
            Lz = 70.0
            ZTraySize = (Lz-1)/2.0
            
            # Radiation length
            X0 = 25.0
            
            # Radius information
            r = 10 + 5 * i
            
            # Module information
            wSizeModule = 2.0
            nWGap = 1
            lSizeModule = 10.0
            nLGap = 1
            
            # Building the layer
            bLayer = BarrelLayer(radius=r, Lz = Lz, X0 = X0, index=i)
            
            # Building trays in the layer
            self.makeTraysAllAround(bLayer, phiShift = phiShift, NPhiTray = NPhiTray, 
                                      PhiTraySize = PhiTraySize, zShift = zShift, 
                                      NZTray = NZTray, ZTraySize = ZTraySize,
                                      nWGap = nWGap, nLGap= nLGap,
                                      wSizeModule = wSizeModule, lSizeModule = lSizeModule)
            tr.addBarrelLayer(bLayer)


        #################################################################################
        # Looping on the endcap disks                                                   #
        #################################################################################
        NDisk = 4
        for i in range(NDisk):
            
            NXTray = 10
            xShift = 0.1
            yShift = 0.1
            r = 30.0
            xTraySize = r / 6.0 
            z = Lz + 4 + 10 * i
            
            # Radiation length
            X0 = 25.0

            # Module information
            nWGap = 1
            nLGap = 1
            wSizeModule = 2
            lSizeModule = 2
            diskp = EndcapDisk(radius=r, z=z, X0=X0, index=i)
            self.makeTraysInDisk(disk=diskp, xShift=xShift, yShift = yShift, NXTray=NXTray, xTraySize = xTraySize, 
                                 nWGap=nWGap, nLGap=nLGap,
                                 wSizeModule=wSizeModule, lSizeModule=lSizeModule)
            tr.addEndcapDisk(diskp)
            diskm = EndcapDisk(radius=r, z=-z, X0=X0, index=i)
            self.makeTraysInDisk(disk=diskm, xShift=xShift, yShift = yShift, NXTray=NXTray, xTraySize = xTraySize, 
                                 nWGap=nWGap, nLGap=nLGap,
                                 wSizeModule=wSizeModule, lSizeModule=lSizeModule)
            tr.addEndcapDisk(diskm)
            
        self.ftr.addTracker(tr)

        
    ########################################################################################################
    def makeTraysAllAround(self, blayer, phiShift, NPhiTray, PhiTraySize, zShift, NZTray, ZTraySize,
                           nWGap, nLGap, wSizeModule, lSizeModule):

        ########################################################################################################
        # This method creates Trays at different positions in Phi
        # phiShift: Initial displacement of the first tray
        # NPhiTray: Number of trays
        # PhiTraySize: Angular size of the tray
        # zShift: Initial displacement of the first tray in Z
        # NZTray: Number of Z trays
        # ZTraySize: Size of the tray in Z
        # nWModules: Number of modules in the phi direction
        # nLModules: Number of modules in the longitudinal direction
        # wSizeModule: Size of the modules in the phi direction
        # lSizeModule: Size of the modules in the longitudinal direction
        ########################################################################################################
        
        # Sanity checks on the geometry of the trays
        if PhiTraySize * NPhiTray > np.pi * 2.0:
            logging.error('The configuration of trays is not correct in phi')
            sys.exit()
        
        if ZTraySize * NZTray + 2.0 * zShift> blayer.Lz:
            logging.error('The configuration of trays is not correct in Z')
            sys.exit()


        trayWidth = 2.0 * blayer.R * np.sin(PhiTraySize/2.0)
        phiSpaceBetweenTrays = (2.0 * np.pi - PhiTraySize * NPhiTray) / NPhiTray 
        trayLength = ZTraySize
        zSpaceBetweenTrays = ((blayer.Lz / 2.0) - zShift) / (NZTray/2)
        for i in range(NPhiTray):
            phi = (phiShift + PhiTraySize/2.0) + i * (PhiTraySize + phiSpaceBetweenTrays)
            x = blayer.R * np.cos(phi)
            y = blayer.R * np.sin(phi)
            for j in range(int(np.floor(NZTray/2))):
                zp = (zShift + ZTraySize/2.0) + j * (ZTraySize + zSpaceBetweenTrays)
                zm = -(zShift + ZTraySize/2.0) - j * (ZTraySize + zSpaceBetweenTrays)                
                vx = np.asarray([np.sin(phi), -np.cos(phi), 0.0])
                vz = np.asarray([np.cos(phi), np.sin(phi), 0.0])
                vy = np.cross(vz, vx)
                euler = EulerRotation()
                euler.setFromVectors(vx, vy, vz)
                
                # Create the trays through the center rotation and size
                tp = Tray(x = x, y = y, z = zp, euler = euler, TrayWidth = trayWidth, TrayLength = trayLength)
                self.makeModulesInTray(tp, nWGap, nLGap, wSizeModule, lSizeModule)
                tm = Tray(x = x, y = y, z = zm, euler = euler, TrayWidth = trayWidth, TrayLength = trayLength)
                self.makeModulesInTray(tm, nWGap, nLGap, wSizeModule, lSizeModule)
                blayer.addTray(tp, 1)
                blayer.addTray(tm, 0)


    ########################################################################################################
    def makeTraysInDisk(self, disk, xShift, yShift, NXTray, xTraySize,
                           nWGap, nLGap, wSizeModule, lSizeModule):

        ########################################################################################################
        # This method creates Trays at different positions in Phi
        # xShift: Initial displacement of the first tray
        # NXTray: Number of x trays
        # xTraySize: Size of the tray in Z
        # nWModules: Number of modules in the phi direction
        # nLModules: Number of modules in the longitudinal direction
        # wSizeModule: Size of the modules in the phi direction
        # lSizeModule: Size of the modules in the longitudinal direction
        ########################################################################################################
        
        # Sanity checks on the geometry of the trays
        if xShift + NXTray/2.0 * xTraySize > disk.R:
            logging.error('The configuration of trays is not correct in the disk')
            sys.exit()
        
        xSpaceBetweenTrays = (disk.R - xShift - NXTray/2.0 * xTraySize)/ (NXTray/2) 
        for i in range(int(NXTray/2)):
            xp = xShift + (xTraySize/2.0) + i * (xTraySize+xSpaceBetweenTrays)
            xm = -xShift - (xTraySize/2.0) - i * (xTraySize+xSpaceBetweenTrays)
            xpmax = xp + xTraySize/2.0
            xmmin = xp - xTraySize/2.0
            yTraymax = np.sqrt(disk.R**2-xpmax**2)
            yTraymin = -np.sqrt(disk.R**2-xpmax**2)
            trayLength = yTraymax - yShift
            yp = yShift + trayLength/2.0
            ym = -yShift - trayLength/2.0      
            vx = np.asarray([1.0, 0.0, 0.0])
            vz = np.asarray([0.0, 0.0, 1.0])
            vy= np.cross(vz, vx)
            if disk.z < 0:
                vx = np.asarray([1.0, 0.0, 0.0])
                vz = np.asarray([0.0, 0.0, -1.0])
                vy= np.cross(vz, vx)
            euler = EulerRotation()
            euler.setFromVectors(vx, vy, vz)
                
            # Create the trays through the center rotation and size
            tp = Tray(x = xp, y = yp, z = disk.z, euler = euler, TrayWidth = xTraySize, TrayLength = trayLength)
            tp.type = 1
            self.makeModulesInTray(tray=tp, nWGap=nWGap, nLGap=nLGap, wSizeModule=wSizeModule, lSizeModule=lSizeModule)
            disk.addTray(tp)
            tm = Tray(x = xm, y = yp, z = disk.z, euler = euler, TrayWidth = xTraySize, TrayLength = trayLength)
            tm.type = 1
            self.makeModulesInTray(tray=tm, nWGap=nWGap, nLGap = nLGap, wSizeModule=wSizeModule, lSizeModule=lSizeModule)
            disk.addTray(tm)
            tpm = Tray(x = xp, y = ym, z = disk.z, euler = euler, TrayWidth = xTraySize, TrayLength = trayLength)
            tpm.type = 1
            self.makeModulesInTray(tray=tpm, nWGap=nWGap, nLGap=nLGap, wSizeModule=wSizeModule, lSizeModule=lSizeModule)
            disk.addTray(tpm)
            tmm = Tray(x = xm, y = ym, z = disk.z, euler = euler, TrayWidth = xTraySize, TrayLength = trayLength)
            tmm.type = 1
            self.makeModulesInTray(tray=tmm, nWGap=nWGap, nLGap = nLGap, wSizeModule=wSizeModule, lSizeModule=lSizeModule)
            disk.addTray(tmm)

    

    ########################################################################################################
    def makeModulesInTray(self, tray, nWGap, nLGap, wSizeModule, lSizeModule):

        nWModules = int(np.floor(tray.TrayWidth/(nWGap+wSizeModule)))
        nLModules = int(np.floor(tray.TrayLength/(nLGap+lSizeModule)))
        
        if nWModules * wSizeModule > tray.TrayWidth or nLModules * lSizeModule > tray.TrayLength:
            logging.error('The module configuration is not correct')
            sys.exit()
        
        stepWidth = tray.TrayWidth / nWModules
        stepLength = tray.TrayLength / nLModules    
        for ix in range(nWModules):
            for iy in range(nLModules):
                rmin = (-tray.TrayWidth/2.0 + stepWidth/2.0) * tray.vx + (-tray.TrayLength/2.0 + stepLength/2.0) * tray.vy 
                rmod = tray.r + rmin + ix * stepWidth * tray.vx + iy * stepLength * tray.vy
                m = Module(rmod[0], rmod[1], rmod[2], wSizeModule, lSizeModule, tray.eulerAngles)
                m.trackerIndex = tray.trackerIndex
                m.barrelIndex = tray.barrelIndex
                m.diskIndex = tray.diskIndex
                m.type = tray.type
                m.zside = tray.zside         
                tray.addModule(m)
