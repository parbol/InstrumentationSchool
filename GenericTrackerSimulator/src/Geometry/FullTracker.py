############################################################################
############################################################################
############################################################################
############################################################################
from src.Navigation.navigation import navigation
from src.Propagation.trajectoryState import trajectoryState
from src.Generator.genParticle import genParticle



class FullTracker:

    def __init__(self, listOfTrackers):

        self.trackers = listOfTrackers
        self.navigator = navigation(self.trackers)

    
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
        
