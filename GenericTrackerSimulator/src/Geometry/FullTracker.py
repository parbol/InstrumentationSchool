############################################################################
############################################################################
############################################################################
############################################################################
from GenericTrackerSimulator.src.Navigation.navigation import navigation
from GenericTrackerSimulator.src.Propagation.trajectoryState import trajectoryState
from GenericTrackerSimulator.src.Propagation.Propagator import Propagator
from GenericTrackerSimulator.src.Generation.genParticle import genParticle
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO, filename='logs.log')


class FullTracker:

    def __init__(self, listOfTrackers=[]):

        self.trackers = listOfTrackers
        self.propagator = Propagator(3.8)

    #########################################################    
    def setNavigator(self):

        self.navigator = navigation(self.trackers)

    #########################################################    
    def addTracker(self, tr):

        tr.trackerIndex = len(self.trackers)
        self.trackers.append(tr)

    #########################################################    
    def propagateParticle(self, particle):
        
        trajState = trajectoryState()
        trajState.fromGenParticle(particle)
        
        valid = True

        # We start with the first layer of the barrel or
        # the first layers of the endcap (positive and negative)
        nextLayers = [[0, 0, 0], [0, 0, 1], [0, 0, -1]]
        
        while valid:
            
            mint = 1e7
            minLayer = None
            minTrajState = None
            valid = False
          
            for l in nextLayers:
                
                # Choose the next possible layer
                layer = None
                if l[2] == 0:
                    layer = self.trackers[l[0]].barrelLayers[l[1]]
                elif l[2] == 1:
                    layer = self.trackers[l[0]].pEndcapDisks[l[1]]
                elif l[2] == -1:
                    layer = self.trackers[l[0]].mEndcapDisks[l[1]]
                
                newTrajState, validT = self.propagator.propagate(trajState, layer)
               
                if validT:
                    valid = True
                    if newTrajState.t >= 0.0 and newTrajState.t < mint:
                        mint = newTrajState.t
                        minLayer = layer
                        minTrajState = newTrajState
            if minLayer != None:
                particle.layerIntersections.append(minTrajState)           
                m, newTrajStateModule, validModule = self.propagator.finePropagation(trajState, minLayer)
                if validModule:
                    particle.intersections.append([m, newTrajStateModule])
                    trajState = newTrajStateModule
                else:
                    trajState = minTrajState
                nextLayers = minLayer.connections 
            else:
                break

    ########################################################################################################
    def draw(self, ax1, ax2, ax3, ax4, t1, t2, alpha=0.2):

        for tr in self.trackers:
            tr.draw(ax1, ax2, ax3, ax4, t1, t2, alpha)


    ########################################################################################################
    def drawBarrel(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for tr in self.trackers:
            tr.drawBarrel(ax1, ax2, ax3, ax4, t, alpha)
       

    ########################################################################################################
    def drawEndcaps(self, ax1, ax2, ax3, ax4, t, alpha=0.2):
        
        for tr in self.trackers:
            tr.drawEndcaps(ax1, ax2, ax3, ax4, t, alpha)
       
    
    ########################################################################################################
    def print(self):
        
        for i, t in enumerate(self.trackers):
            logging.info(f'Tracker {i}')
            t.print()
            