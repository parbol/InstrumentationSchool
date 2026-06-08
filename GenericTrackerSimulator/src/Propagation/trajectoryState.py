import numpy as np
from GenericTrackerSimulator.src.Generation.genParticle import genParticle


class trajectoryState:

    def __init__(self, x = 0, y = 0, z = 0, t = 0, phi = 0, eta = 0, E = 1, q = 1, beta = 1):

        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.phi = phi
        self.eta = eta
        self.beta = beta
        self.theta = 2.0 * np.arctan(np.exp(-eta))
        self.E = E
        self.q = q

    def fromGenParticle(self, p):
        
        pz = p.pt * np.sinh(p.eta)
        E_ = np.sqrt(pz**2 + p.pt**2 + p.mass**2)
        p_ = np.sqrt(pz**2+p.pt**2)
        beta = p_/E_ 
        self.x = p.x
        self.y = p.y
        self.z = p.z
        self.t = p.t
        self.phi = p.phi
        self.eta = p.eta
        self.beta = beta
        self.E = E_
        self.q = p.q
        
        
