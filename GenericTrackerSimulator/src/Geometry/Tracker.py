from GenericTrackerSimulator.src.Geometry.BarrelLayer import BarrelLayer
import sys
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO, filename='logs.log')


class Tracker:

    def __init__(self, barrelMinR, barrelMaxR, barrelLZ, endcapMinR, endcapMaxR, endcapMinZ, endcapMaxZ, index):

        #######################################################################
        # These parameters represent the tracker envelope:                    #
        # barrelMinR: min distance in R of the barrel                         #
        # barrelMaxR: max distance in R of the barrel                         #
        # barrelLZ: length of the barrel                                      #
        # endcapMinR: min distance in R of the endcap                         #
        # endcapMaxR: max distance in R of the endcap                         #
        # endcapMinZ: min distance in Z of the endcap                         #
        # endcapMaxZ: max distance in Z of the endcap                         #
        #######################################################################
        self.barrelMinR = barrelMinR
        self.barrelMaxR = barrelMaxR
        self.barrelLZ = barrelLZ
        self.endcapMinR = endcapMinR
        self.endcapMaxR = endcapMaxR
        self.endcapMinZ = endcapMinZ
        self.endcapMaxZ = endcapMaxZ
        
        # Id of this tracker
        self.trackerIndex = index

        # The tracker contains barrel layers and endcap disks
        self.nBarrelLayers = 0
        self.npEndcapDisks = 0
        self.nmEndcapDisks = 0
        self.barrelLayers = []
        self.pEndcapDisks = []
        self.mEndcapDisks = []
 
        # Sanity crosschecks on the geometry
        if self.barrelMinR <= 0:
            logging.error('The inner radius of the tracker barrel cannot be negative')
            sys.exit()
        if self.barrelMaxR <= self.barrelMinR:
            logging.error('The outter radius of the tracker barrel cannot be lower than the inner radius')
            sys.exit()
        if self.barrelLZ <= 0:
            logging.error('The Z length of the tracker barrel cannot be a negative number or 0')
            sys.exit()
        if self.endcapMinR <= 0:
            logging.error('The inner radius of the tracker endcap cannot be negative')
            sys.exit()
        if self.endcapMaxR <= self.endcapMinR:
            logging.error('The outter radius of the tracker endcap cannot be lower than the inner radius')
            sys.exit()
        if self.endcapMinZ <= 0:
            logging.error('The first position of the Z endcap cannot be a negative number or 0')
            sys.exit()
        if self.endcapMaxZ <= self.endcapMinZ:
            logging.error('The last position of the Z endcap cannot be lower than the first')
            sys.exit()

        logging.info('Setting up tracker volumen with Barrel inner radius: %d, outer radius: %d, and length: %d, and Endcap inner radius: %d, outer radius: %d, inner disk position: %d and outer disk position %d',
                     self.barrelMinR, self.barrelMaxR, self.barrelLZ, self.endcapMinR, self.endcapMaxR, self.endcapMinZ, self.endcapMaxZ)
        
       
    #######################################################################
    def addBarrelLayer(self, layer):

        if layer.R > self.barrelMaxR or layer.R < self.barrelMinR or layer.Lz > self.barrelLZ:
            logging.error('There was a barrel layer not fitting the tracker volume')
            sys.exit()
        if self.nBarrelLayers != 0 and layer.R <= self.barrelLayers[self.nBarrelLayers-1].R:
            logging.error('A layer with lower radius than an existing one has been tried')
            sys.exit()
        
        logging.info('Adding a barrel layer to the tracker at radius: %f', layer.R)
        
        layer.trackerIndex = self.trackerIndex
        layer.barrelIndex = self.nBarrelLayers
        self.barrelLayers.append(layer)
        self.nBarrelLayers = self.nBarrelLayers + 1

    #######################################################################
    def addEndcapDisk(self, disk):

        if disk.R > self.endcapMaxR or disk.R < self.endcapMinR or abs(disk.z) < self.endcapMinZ or abs(disk.z) > self.endcapMaxZ:
            logging.error('There was an endcap disk not fitting the tracker volume')
            sys.exit()
        disk.trackerIndex = self.trackerIndex
        if disk.z > 0:
            if self.npEndcapDisks != 0 and disk.z < self.pEndcapDisks[self.npEndcapDisks-1].z:
                logging.error('A positive disk with lower Z than an existing one has been tried')
                sys.exit()
            self.pEndcapDisks.append(disk)
            self.diskIndex = self.npEndcapDisks
            self.npEndcapDisks = self.npEndcapDisks + 1
        else:
            if self.nmEndcapDisks != 0 and disk.z > self.mEndcapDisks[self.nmEndcapDisks-1].z:
                logging.error('A nevative disk with lower Z than an existing one has been tried')
                sys.exit()
            self.mEndcapDisks.append(disk)
            self.diskIndex = self.nmEndcapDisks
            self.nmEndcapDisks = self.nmEndcapDisks + 1

        logging.info('Adding an endcap disk to the tracker at Z: %d', disk.z)

    
    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t1, t2, alpha=0.2):

        self.drawBarrel(ax1, ax2, ax3, ax4, t1, alpha)
        self.drawEndcaps(ax1, ax2, ax3, ax4, t2, alpha)


    ########################################################################################################
    def drawBarrel(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for b in self.barrelLayers:
            b.draw(ax1, ax2, ax3, ax4, t, alpha)
       

    ########################################################################################################
    def drawEndcaps(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for b in self.mEndcapDisks:
            b.draw(ax1, ax2, ax3, ax4, t, alpha)
        for b in self.pEndcapDisks:
            b.draw(ax1, ax2, ax3, ax4, t, alpha)


    ########################################################################################################
    def print(self):

        logging.info(f'Tracker with tracker index {self.trackerIndex}')
        for t in self.barrelLayers:
            t.print()
        for t in self.mEndcapDisks:
            t.print()
        for t in self.pEndcapDisks:
            t.print()
                
    
        
