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
          

    ########################################################################
    def getTracker(self, tr):
        
        trs = dict()
        trs['barrelMinR'] = tr.barrelMinR
        trs['barrelMaxR'] = tr.barrelMaxR
        trs['barrelLZ'] = tr.barrelLZ
        trs['endcapMinR'] = tr.endcapMinR
        trs['endcapMaxR'] = tr.endcapMaxR
        trs['endcapMinZ'] = tr.endcapMaxZ
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
        trays['psi'] = tray.eulerAngles.psi
        trays['theta'] = tray.eulerAngles.theta
        trays['phi'] = tray.eulerAngles.phi
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
        module['psi'] = m.eulerAngles.psi
        module['theta'] = m.eulerAngles.theta
        module['phi'] = m.eulerAngles.phi
        module['Lx'] = m.Lx
        module['Ly'] = m.Ly
        
        return module
                    