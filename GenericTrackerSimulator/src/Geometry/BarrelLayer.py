from src.Geometry.Tray import Tray
import sys
import logging
logger = logging.getLogger(__name__)

class BarrelLayer:
    
    def __init__(self, radius, Lz, X0, index):

        ####################################################################################################
        #                                   Representation of a Barrel Layer                               #
        # radius:  Radius of the layer                                                                     # 
        # Lz:      Length in Z of the layer                                                                # 
        # X0:      Mean radiation length up to this layer                                                  # 
        ####################################################################################################
        self.R = radius
        self.Lz = Lz
        self.X0 = X0
        self.nTrays = 0

        if self.R <= 0:
            logging.error('The radius of a barrel layer cannot be negative')
            sys.exit()
        if self.Lz <= 0:
            logging.error('The length of a barrel layer cannot be negative')
            sys.exit()
        if self.X0 <= 0:
            logging.error('The radiation length cannot be negative')
            sys.exit()
        
        logging.info('Setting up a layer with radius: %d, length: %d and radiation length: %d', self.R, self.Lz, self.X0)


    ########################################################################################################
    def addTray(self, tray):

        if tray.maxZ > self.LZ/2.0 or tray.minZ < -self.LZ/2.0 or tray.R >= self.R:
            logging.error('The tray is not fitting the layer')
            sys.exit()

        self.nTrays = self.nTrays + 1
        self.Trays.append(tray)
        
        logging.info('A tray has been added to the layer at position x: %d, y: %d, z: %d', tray.x, tray.y, tray.z)


    
    
   