import math
from src.Generator.genParticle import genParticle


class trajectoryState:

    def __init__(self, x, y, z, t, phi, eta, betaT):

        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.phi = phi
        self.eta = eta
        self.betaT = betaT

    def fromGenParticle(self, p):
        
        pz = p.pt * math.sinh(p.eta)
        E = math.sqrt(pz**2 + p.pt**2 + p.mass**2)
        p = math.sqrt(pz**2+p.pt**2)
        beta = p/E 
        self.x = p.x
        self.y = p.y
        self.z = p.z
        self.t = p.t
        self.phi = p.phi
        self.eta = p.eta
        self.betaT = beta
        
        
