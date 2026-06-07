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
        #self.navigator = navigation(self.trackers)

    
    def addTracker(self, tr):

        self.trackers.append(tr)


    def propagateParticle(self, particle):

        trajState = trajectoryState(0, 0, 0, 0, 0, 1)
        trajState.fromGenParticle(particle)
        
        valid = True
        nextLayers = [self.trackers[0].barrelLayers[0]]
        
        while valid:
            
            mint = 1e7
            minLayer = []
            minTrajState = []
            valid = False
            for l in nextLayers:
                newTrajState, newLayer, validT = self.propagator.propagate(trajState, l)
                if validT:
                    valid = True
                    if newTrajState.t >= 0.0 and newTrajState.t < mint:
                        mint = newTrajState.t
                        minLayer = newLayer
                        minTrajState = newTrajState
                hit, validHit = self.produceHit(minTrajState, minLayer)
                if validHit:
                    self.trajectory.addHit(hit)
        
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
       
    
   