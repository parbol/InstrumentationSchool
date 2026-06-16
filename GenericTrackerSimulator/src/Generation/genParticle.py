import numpy as np

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)

class genParticle:

    def __init__(self, x, y, z, t, phi, eta, pt, mass, q, id):

        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.phi = phi
        self.eta = eta
        self.pt = pt
        self.mass = mass
        self.id = id
        self.q = q
        self.intersections = []
        self.layerIntersections = []

    ##############################################################################
    def drawIntersections(self, ax1, ax2, ax3, ax4, t='y*', alpha=0.2):

        x = []
        y = []
        z = []
        for i in self.intersections:
            ts = i[1]
            #ts = i
            x.append(ts.x)
            y.append(ts.y)
            z.append(ts.z)
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        self.plot_points(x, y, z, ax1, ax2, ax3, ax4, t)

    #############################################################################        
    def plot_points(self, x, y, z, ax1, ax2, ax3, ax4, fmt):

        ax2.plot(x, y, fmt, markersize=5)
        ax1.plot3D(x, z, y, fmt, markersize=5)
        ax3.plot(z, y, fmt, markersize=5)
        ax4.plot(z, x, fmt, markersize=5)

    #############################################################################        
    def draw(self, B, ax1, ax2, ax3, ax4, fmt):

        #We have all the ingredients, we just need to propagate the track for a given time
        t = np.linspace(0, self.layerIntersections[-1].t, 200)
        x, y, z = self.eval(B, t)
        ax1.plot3D(x, z, y, fmt)
        ax2.plot(x, y, fmt, label = 'Real track')
        #ax2.plot(0, 0, 'rx')
        ax3.plot(z, y, fmt)
        ax4.plot(z, x, fmt)


    #############################################################################        
    def eval(self, B, t):
        
        pz = self.pt * np.sinh(self.eta)
        E = np.sqrt(self.pt**2+pz**2+self.mass**2)
        gamma = E / self.mass
        beta = np.sqrt((1.0-1.0/gamma**2))
        # Speed of light in cm per ns
        c = 29.9792458
        theta = 2.0 * np.arctan(np.exp(-self.eta))
        vT = beta * np.sin(theta) * c
        vZ = beta * np.cos(theta) * c
        # Angular frequency of the helix
        w = self.q * 0.089880 * B / (gamma * self.mass)
        # Curvature radius
        R = vT/w
        x = R * (np.sin(w*t - self.phi) + np.sin(self.phi)) + self.x
        y = R * (np.cos(w*t - self.phi) - np.cos(self.phi)) + self.y
        z = vZ * t + self.z
      
        return x, y, z
    
    def print(self):

        logging.info(f'Particle at: ({self.x}, {self.y}, {self.z}) with phi: {self.phi}, eta: {self.eta}, pt: {self.pt}, id: {self.id}, charge: {self.q}')
        