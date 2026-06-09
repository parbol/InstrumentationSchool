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

    def drawIntersections(self, ax1, ax2, ax3, ax4, t='y*', alpha=0.2):

        x = []
        y = []
        z = []
        for i in self.intersections:
            ts = i[1]
            x.append(ts.x)
            y.append(ts.y)
            z.append(ts.z)
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        self.plot_points(x, y, z, ax1, ax2, ax3, ax4, t)
            
    def plot_points(self, x, y, z, ax1, ax2, ax3, ax4, fmt):

        ax2.plot(x, y, fmt, markersize=2)
        ax1.plot3D(x, z, y, fmt, markersize=2)
        ax3.plot(z, y, fmt, markersize=2)
        ax4.plot(z, x, fmt, markersize=2)