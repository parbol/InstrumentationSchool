############################################################################
############################################################################
############################################################################
############################################################################
from GenericTrackerSimulator.src.Navigation.navigation import navigation
from GenericTrackerSimulator.src.Propagation.trajectoryState import trajectoryState
from GenericTrackerSimulator.src.Generation.genParticle import genParticle



class FullTracker:

    def __init__(self, listOfTrackers=[]):

        self.trackers = listOfTrackers
    
    def setNavigator(self):

        self.navigator = navigation(self.trackers)

    def addTracker(self, tr):

        tr.trackerIndex = len(self.trackers)
        self.trackers.append(tr)

    def propagateParticle(self, particle):
        
        trajState = trajectoryState()
        trajState.fromGenParticle(particle)
        
        valid = True

        # We start with the first layer of the barrel or
        # the first layers of the endcap (positive and negative)
        nextLayers = [[0, 0, 0], [0, 0, 1], [0, 0, -1]]
        
        while valid:
            
            mint = 1e7
            minLayer = []
            minTrajState = []
            valid = False

            for l in nextLayers:
                layer = []
                if l[2] == 0:
                    layer = self.ftr.trackers[l[0]].barrelLayers[l[1]]
                elif l[2] == 1:
                    layer = self.ftr.trackers[l[0]].pEndcapDisks[l[1]]
                elif l[2] == -1:
                    layer = self.ftr.trackers[l[0]].mEndcapDisks[l[1]]
                
                newTrajState, validT = self.propagator.propagate(trajState, layer)
                if validT:
                    valid = True
                    if newTrajState.t >= 0.0 and newTrajState.t < mint:
                        mint = newTrajState.t
                        minLayer = layer
                        minTrajState = newTrajState
            
            hit, validHit = self.produceHit(minTrajState, minLayer)
            if validHit:
                self.trajectory.addHit(hit)
            nextLayers = minLayer.connections

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
       
    
   