import numpy as np
from GenericTrackerSimulator.src.Generation.genParticle import genParticle
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)

class trajectoryState:

    def __init__(self, x = 0, y = 0, z = 0, t = 0, phi = 0, eta = 0, E = 1, q = 1, beta = 0.8):

        # Speed of light in cm per ns
        self.c = 29.9792458
        # The position of the state at a given moment of the trajectory
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        # The direction of the state at a given moment of the trajectory
        self.phi = phi
        self.eta = eta
        self.theta = 0.0
        # The velocity of the state
        self.beta = beta
        self.gamma = 0.0
        self.vT = 0.0
        self.vZ = 0.0
        # The energy of the state
        self.E = E
        self.m = 0
        # The charge of the state
        self.q = q
        self.calculateDerivates()

    ###################################################################
    def calculateDerivates(self):

        self.theta = 2.0 * np.arctan(np.exp(-self.eta))
        self.gamma = np.sqrt(1.0/(1.0 - self.beta**2))
        self.vT = self.beta * np.sin(self.theta) * self.c
        self.vZ = self.beta * np.cos(self.theta) * self.c
        self.m = self.E / self.gamma

    ###################################################################
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
        self.calculateDerivates()
        
    ###################################################################
    def print(self):
        
        print(f'Trajectory state ({self.x}, {self.y}, {self.z}, {self.t})')
      