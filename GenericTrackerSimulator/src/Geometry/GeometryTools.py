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
import json

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO, filename='logs.log')



class GeometryTools:
    
    #####################################################################################
    # Geometry tools for importing and exporting databases                              #
    # The geometry will be dumped into a json file with all the information .           #
    #####################################################################################

    def __init__(self, ftr):

        # All units are in cm
        self.ftr = ftr
        
    
    ########################################################################################################ç
    def exportGeometry(self, filename):

        geom = dict()
        geom['trackers'] = []
        for tr in self.ftr.trackers:
            
            trs = self.getTracker(tr)
            geom['trackers'].append(trs)
          
        with open(filename, 'w') as f:
                json.dump(geom, f, ensure_ascii=False, indent=4)

    
    ########################################################################
    def importGeometry(self, filename):
    
        with open(filename) as json_data:
            info = json.load(json_data)
    

        for tr in info['trackers']:

            tracker = Tracker(tr['barrelMinR'], tr['barrelMaxR'], tr['barrelLZ'],
                              tr['endcapMinR'], tr['endcapMaxR'], tr['endcapMinZ'],
                              tr['endcapMaxZ'], tr['trackerIndex'])            
            
            for bl in tr['barrelLayers']:

                blayer = BarrelLayer(bl['R'], bl['Lz'], bl['X0'], bl['barrelIndex'])

                for tray in bl['nTrays']:
                    euler = EulerRotation(0.0, 0.0, 0.0)
                    vx = np.asarray([tray['vx0'], tray['vx1'], tray['vx2']])
                    vy = np.asarray([tray['vy0'], tray['vy1'], tray['vy2']])
                    vz = np.asarray([tray['vz0'], tray['vz1'], tray['vz2']])
                    euler.setFromVectors(vx, vy, vz)
                    tra = Tray(tray['x'], tray['y'], tray['z'], euler,
                                tray['TrayWidth'], tray['TrayLength'])
                    blayer.addTray(tra, -1)                     
                    for m in tray['Modules']:
                    
                        eulerM = EulerRotation(0.0, 0.0, 0.0)
                        vxm = np.asarray([m['vx0'], m['vx1'], m['vx2']])
                        vym = np.asarray([m['vy0'], m['vy1'], m['vy2']])
                        vzm = np.asarray([m['vz0'], m['vz1'], m['vz2']])
                        eulerM.setFromVectors(vxm, vym, vzm)
                        mod = Module(m['x'], m['y'], m['z'], m['Lx'],
                                     m['Ly'], eulerM)
                        tra.addModule(mod)
                
                for tray in bl['pTrays']:
                    
                    euler = EulerRotation(0.0, 0.0, 0.0)
                    vx = np.asarray([tray['vx0'], tray['vx1'], tray['vx2']])
                    vy = np.asarray([tray['vy0'], tray['vy1'], tray['vy2']])
                    vz = np.asarray([tray['vz0'], tray['vz1'], tray['vz2']])
                    euler.setFromVectors(vx, vy, vz)
                    tra = Tray(tray['x'], tray['y'], tray['z'], euler,
                                tray['TrayWidth'], tray['TrayLength'])
                     
                    blayer.addTray(tra, 1)
                    for m in tray['Modules']:
                        eulerM = EulerRotation(0.0, 0.0, 0.0)
                        vxm = np.asarray([m['vx0'], m['vx1'], m['vx2']])
                        vym = np.asarray([m['vy0'], m['vy1'], m['vy2']])
                        vzm = np.asarray([m['vz0'], m['vz1'], m['vz2']])
                        eulerM.setFromVectors(vxm, vym, vzm)
                        mod = Module(m['x'], m['y'], m['z'], m['Lx'],
                                     m['Ly'], eulerM)
                        tra.addModule(mod)
                    

                tracker.addBarrelLayer(blayer)

            for ed in tr['mEndcapDisks']:

                edisk = EndcapDisk(ed['R'], ed['z'], ed['X0'], ed['diskIndex'])
                
                for tray in ed['Trays']:
                    euler = EulerRotation(0.0, 0.0, 0.0)
                    vx = np.asarray([tray['vx0'], tray['vx1'], tray['vx2']])
                    vy = np.asarray([tray['vy0'], tray['vy1'], tray['vy2']])
                    vz = np.asarray([tray['vz0'], tray['vz1'], tray['vz2']])
                    euler.setFromVectors(vx, vy, vz)
                    tra = Tray(tray['x'], tray['y'], tray['z'], euler,
                                tray['TrayWidth'], tray['TrayLength'])
                    edisk.addTray(tra)                     
                    for m in tray['Modules']:
                        eulerM = EulerRotation(0.0, 0.0, 0.0)
                        vxm = np.asarray([m['vx0'], m['vx1'], m['vx2']])
                        vym = np.asarray([m['vy0'], m['vy1'], m['vy2']])
                        vzm = np.asarray([m['vz0'], m['vz1'], m['vz2']])
                        eulerM.setFromVectors(vxm, vym, vzm)
                        mod = Module(m['x'], m['y'], m['z'], m['Lx'],
                                     m['Ly'], eulerM)
                        tra.addModule(mod)
                
                tracker.addEndcapDisk(edisk) 
      
            for ed in tr['pEndcapDisks']:

                edisk = EndcapDisk(ed['R'], ed['z'], ed['X0'], ed['diskIndex'])
                
                for tray in ed['Trays']:
                    
                    euler = EulerRotation(0.0, 0.0, 0.0)
                    vx = np.asarray([tray['vx0'], tray['vx1'], tray['vx2']])
                    vy = np.asarray([tray['vy0'], tray['vy1'], tray['vy2']])
                    vz = np.asarray([tray['vz0'], tray['vz1'], tray['vz2']])
                    euler.setFromVectors(vx, vy, vz)
                    tra = Tray(tray['x'], tray['y'], tray['z'], euler,
                                tray['TrayWidth'], tray['TrayLength'])
                    edisk.addTray(tra)                     
                    for m in tray['Modules']:
                        eulerM = EulerRotation(0.0, 0.0, 0.0)
                        vxm = np.asarray([m['vx0'], m['vx1'], m['vx2']])
                        vym = np.asarray([m['vy0'], m['vy1'], m['vy2']])
                        vzm = np.asarray([m['vz0'], m['vz1'], m['vz2']])
                        eulerM.setFromVectors(vxm, vym, vzm)
                        mod = Module(m['x'], m['y'], m['z'], m['Lx'],
                                     m['Ly'], eulerM)
                        tra.addModule(mod)
                
                tracker.addEndcapDisk(edisk) 

            self.ftr.addTracker(tracker)



    ########################################################################
    def getTracker(self, tr):
        
        trs = dict()
        trs['barrelMinR'] = tr.barrelMinR
        trs['barrelMaxR'] = tr.barrelMaxR
        trs['barrelLZ'] = tr.barrelLZ
        trs['endcapMinR'] = tr.endcapMinR
        trs['endcapMaxR'] = tr.endcapMaxR
        trs['endcapMinZ'] = tr.endcapMinZ
        trs['endcapMaxZ'] = tr.endcapMaxZ
        trs['trackerIndex'] = tr.trackerIndex
        trs['nBarrelLayers'] = tr.nBarrelLayers
        trs['barrelLayers'] = []
        for blayer in tr.barrelLayers:
            bls = self.getBarrelLayer(blayer)
            trs['barrelLayers'].append(bls)
        
        trs['npEndcapDisks'] = tr.npEndcapDisks
        trs['pEndcapDisks'] = []
        for pdisk in tr.pEndcapDisks:
            dd = self.getEndcapDisk(pdisk)
            trs['pEndcapDisks'].append(dd)

        trs['nmEndcapDisks'] = tr.nmEndcapDisks
        trs['mEndcapDisks'] = []
        for mdisk in tr.mEndcapDisks:
            dd = self.getEndcapDisk(mdisk)
            trs['mEndcapDisks'].append(dd)

        return trs
                
    ########################################################################
    def getBarrelLayer(self, blayer):

        bls = dict()  
        bls['R'] = blayer.R
        bls['Lz'] = blayer.Lz
        bls['X0'] = blayer.X0
        bls['trackerIndex'] = blayer.trackerIndex
        bls['barrelIndex'] = blayer.barrelIndex            
        bls['nnTrays'] = blayer.nnTrays
        bls['nTrays'] = []
        for tray in blayer.nTrays:

            trays = self.getTray(tray)
            bls['nTrays'].append(trays)
        
        bls['npTrays'] = blayer.npTrays
        bls['pTrays'] = []
        for tray in blayer.pTrays:
            trays = self.getTray(tray)
            bls['pTrays'].append(trays)

        return bls

    ########################################################################
    def getEndcapDisk(self, disk):

        disks = dict()
        disks['R'] = disk.R
        disks['z'] = disk.z
        disks['X0'] = disk.X0
        disks['trackerIndex'] = disk.trackerIndex
        disks['diskIndex'] = disk.diskIndex
        disks['nTrays'] = disk.nTrays
        disks['Trays'] = []

        for tray in disk.Trays:

            trayd = self.getTray(tray)
            disks['Trays'].append(trayd)

        return disks

    ########################################################################
    def getTray(self, tray):
       
        trays = dict()
        trays['trackerIndex'] = tray.trackerIndex
        trays['barrelIndex'] = tray.trackerIndex
        trays['diskIndex'] = tray.diskIndex
        trays['trayIndex'] = tray.trayIndex
        trays['type'] = tray.type
        trays['zside'] = tray.zside
        trays['x'] = tray.x
        trays['y'] = tray.y
        trays['z'] = tray.z
        trays['vx0'] = tray.eulerAngles.vx[0]
        trays['vx1'] = tray.eulerAngles.vx[1]
        trays['vx2'] = tray.eulerAngles.vx[2]
        trays['vy0'] = tray.eulerAngles.vy[0]
        trays['vy1'] = tray.eulerAngles.vy[1]
        trays['vy2'] = tray.eulerAngles.vy[2]
        trays['vz0'] = tray.eulerAngles.vz[0]
        trays['vz1'] = tray.eulerAngles.vz[1]
        trays['vz2'] = tray.eulerAngles.vz[2]
        trays['TrayWidth'] = tray.TrayWidth
        trays['TrayLength'] = tray.TrayLength
        trays['nModules'] = tray.nModules
        trays['Modules'] = []
        for m in tray.modules:

            mod = self.getModule(m)
            trays['Modules'].append(mod)
            
        return trays


    ########################################################################
    def getModule(self, m):
          
        module = dict()
        module['trackerIndex'] = m.trackerIndex
        module['barrelIndex'] = m.trackerIndex
        module['diskIndex'] = m.diskIndex
        module['trayIndex'] = m.trayIndex
        module['moduleIndex'] = m.moduleIndex
        module['type'] = m.type
        module['zside'] = m.zside
        module['x'] = m.x
        module['y'] = m.y
        module['z'] = m.z
        module['vx0'] = m.eulerAngles.vx[0]
        module['vx1'] = m.eulerAngles.vx[1]
        module['vx2'] = m.eulerAngles.vx[2]
        module['vy0'] = m.eulerAngles.vy[0]
        module['vy1'] = m.eulerAngles.vy[1]
        module['vy2'] = m.eulerAngles.vy[2]
        module['vz0'] = m.eulerAngles.vz[0]
        module['vz1'] = m.eulerAngles.vz[1]
        module['vz2'] = m.eulerAngles.vz[2]
        module['psi'] = m.eulerAngles.psi
        module['Lx'] = m.Lx
        module['Ly'] = m.Ly
        
        return module
                    