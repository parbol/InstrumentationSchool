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
        self.det = np.asarray([], dtype=np.int32)
        self.l = np.asarray([], dtype=np.int32)
       
    def plot_points(self, x, y, z, ax1, ax2, ax3, ax4, fmt):

        ax2.plot(x, y, fmt, markersize=2)
        ax1.plot3D(x, z, y, fmt, markersize=2)
        ax3.plot(z, y, fmt, markersize=2)
        ax4.plot(z, x, fmt, markersize=2)
    
    def plot_measurements(self, ax1, ax2, ax3, ax4, fmt):

        self.plot_points(self.xm, self.ym, self.zm, ax1, ax2, ax3, ax4, fmt)
          
    def print(self):
        print('----Noise info-----')
        print('Rate:', self.rate)
     
