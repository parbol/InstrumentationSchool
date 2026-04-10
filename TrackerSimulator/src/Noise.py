import numpy as np
import matplotlib.pyplot as plt


class Noise:
    
    def __init__(self, rate):
        
        

        self.rate = rate
        
        
        #List of intersections and measurements
        self.xm = np.asarray([])
        self.ym = np.asarray([])
        self.zm = np.asarray([])
        self.tm = np.asarray([])
       
    
    def plot_measurements(self, ax1, ax2, ax3, ax4, fmt):

        self.plot_points(self.xm, self.ym, self.zm, ax1, ax2, ax3, ax4, fmt)
          
    def print(self):
        print('----Noise info-----')
        print('Rate:', self.rate)
     
