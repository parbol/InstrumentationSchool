from LGADModuleSimulator.src.LGADSimulator import LGADSimulator

import numpy as np
import matplotlib.pyplot as plt





if __name__ == "__main__":

    #Some global variables
    fig, ax = plt.subplots()
    
    lgad = LGADSimulator(thickness=0.3, radius=1.0, 
                        intLumi = 0.0, taur = 2.0,
                        taud=3.0, clock=3.0,
                        threshold=0.9525, noiseLevel=0.2750, sigmaTDC=0.010)
    
    lgad.drawEvent(ax, 13, 10, 0, 0)
    
    plt.show()
    
