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


  