



class fullSystem:

    def __init__(self, listOfTrackers):

        self.trackers = listOfTrackers
        self.navigator = navigation(self.trackers)

    def propagateParticle(self, particle):

        trajectory = particle.Trajectory() 
        trajState = particle.TrajectoryState()
        layer = self.trackers[0].barrelLayers[0]
        for theLayer in layer.getLayers():
            trajState_, valid = self.propagate(trajState, layers)


