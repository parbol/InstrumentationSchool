import numpy as np
import matplotlib.pyplot as plt


class Track:
    
    def __init__(self, dxy, dz, phi, eta, pt, q):
        
        ##################### Track parameters with known vertex #######################
        ##### x(0) -> X position of the vertex
        ##### y(0) -> Y position of the vertex
        ##### z(0) -> Z position of the vertex
        ##### phi -> Direction of the particle in the transverse plane
        ##### eta -> Direction of the particle in the longitudinal plane 
        ##### pt -> transverse momentum
        ##### charge -> the charge
        #################################################################
        ##### In the z coordinate we have: pz = pt * sinh(eta) and z = pt * sinh(eta) / m * t + z(0)
        #################################################################
        ##### In the transverse plane we have:
        ##### Px(t) = Pt cos(wt - phi) and Py(t) = -Pt sin(wt - phi)
        ##### x(t) = Pt/qB [sin(wt - phi) + sin(phi)] + x(0)
        ##### y(t) = Pt/qB [cos(wt - phi) - cos(phi)] + y(0)
        #################################################################
        ##### Relation to the equation of the cirumference:
        ##### (x - x(0) - Pt/qB sin(phi))^2 + (y - y(0) + Pt/qB cos(phi))^2 = (Pt/qB)^2 
        ##### Therefore:
        ##### Radius = Pt/mw
        ##### Center of the circumference X = x(0) + Pt/qB sin(phi)
        ##### Center of the circumference Y = y(0) - Pt/qB cos(phi)
        #################################################################

        ######### Track parameters with respect to POCA #############
        ##### dxy -> Distance in the transverse plane from the POCA to the beam line
        ##### dz  -> Distance in z from the the POCA to the origin 
        ##### phi -> Direction of the particle in the transverse plane at the POCA
        ##### eta -> Direction of the particle in the longitudinal plane 
        ##### pt -> transverse momentum
        ##### charge -> the charge
        ##### With this we can easily produce the track
        #################################################################

        ######### How to use the POCA point as vertex #############
        ##### The point of closest approach is that in which the position and momentum
        ##### in the transverse plane are orthogonal (x, y) * (px, py) = 0
        ##### This implies that xpoca * px + ypoca * py = 0 => xpoca * px = -ypoca * py => xpoca / ypoca = -py / px
        ##### But py/px is by the definition the direction of the track at the POCA
        ##### Therefore: xpoca/ypoca = -tan(phi) 
        ##### If we write: xpoca = dxy * cos(phi_poca) and ypoca = dxy * sin(phi_poca) we have that:
        ##### 1 / tan(phi_poca) = -tan(phi) => cotan(phi_poca) = -tan(phi)
        ##### With this angle we can estimate: xpoca = dxy * cos(phi_poca) and ypoca = dxy*sin(phi_poca)
        ##### We can assume that t = 0 is the POCA point and then use the parametrization above 
        ##### pz = pt * sinh(eta) and z = pt * t + z(0) = pt * t + dz
        ##### x(t) = Pt/qB [sin(wt - phi) + sin(phi)] + x(0) = Pt/qB [sin(wt - phi) + sin(phi)] + dxy * cos(phi_poca)
        ##### y(t) = Pt/qB [cos(wt - phi) - cos(phi)] + y(0) = Pt/qB [cos(wt - phi) - cos(phi)] + dxy * sin(phi_poca)

        ##### rho = Pt/qB if we set Pt in GeV, B in Tesla and rho in cm is: (Pt [GeV]/ B[Tesla]) * 1000.0 / 3.0  

        self.dxy = dxy
        self.dz = dz
        self.phi = phi
        self.eta = eta
        self.theta = 2.0 * np.arctan(np.exp(-eta))
        self.pt = pt
        self.q = np.sign(q)
        self.pz = pt * np.sinh(eta) 

        #Some constants, maybe wise to put them somewhere else
        self.m = 0.1396
        b = 3.8
        self.E = np.sqrt(self.pt**2 + self.pz**2 + self.m**2)
        self.p = np.sqrt(self.pt**2 + self.pz**2)
        self.gamma = self.E/self.m
        self.beta = self.p/self.E
        self.w = self.q * 0.089880 * b / (self.gamma * self.m)
        self.betamomentum = self.p * self.beta
        

        #POCA points
        self.x_cp = dxy * np.cos(phi + np.pi/2.0)
        self.y_cp = dxy * np.sin(phi + np.pi/2.0)
        self.z_cp = self.dz       

        #Circle description
        self.rt = pt / (self.q * b) * (1000.0/2.998)
        self.x_c = self.rt * np.sin(phi) + self.x_cp
        self.y_c = -self.rt * np.cos(phi) + self.y_cp
        
        #List of intersections and measurements
        self.det = []
        self.subdet = []
        self.xi = np.asarray([])
        self.yi = np.asarray([])
        self.zi = np.asarray([])
        self.ti = np.asarray([])
        self.xm = np.asarray([])
        self.ym = np.asarray([])
        self.zm = np.asarray([])
        self.tm = np.asarray([])
        self.lxi = np.asarray([])
        self.lyi = np.asarray([])
        self.lzi = np.asarray([])
        self.lxm = np.asarray([])
        self.lym = np.asarray([])
        self.lzm = np.asarray([])
        self.lastT = 0

    
    def eval(self, t):
        
        # Returns the position of a track at time t    
        x = self.rt * np.sin(self.w * t - self.phi) + self.x_c       
        y = self.rt * np.cos(self.w * t - self.phi) + self.y_c
        z = 29.98 * self.pz / (self.gamma*self.m) * t + self.dz        

        return x, y, z


    def plot_points(self, x, y, z, ax1, ax2, ax3, ax4, fmt):

        ax2.plot(x, y, fmt, markersize=2)
        ax1.plot3D(x, z, y, fmt, markersize=2)
        ax3.plot(z, y, fmt, markersize=2)
        ax4.plot(z, x, fmt, markersize=2)


    def plot_intersections(self, ax1, ax2, ax3, ax4, fmt):

        self.plot_points(self.xi, self.yi, self.zi, ax1, ax2, ax3, ax4, fmt)


    def plot_measurements(self, ax1, ax2, ax3, ax4, fmt):

        self.plot_points(self.xm, self.ym, self.zm, ax1, ax2, ax3, ax4, fmt)


    def plot_track(self, ax1, ax2, ax3, ax4, fmt = 'g'):
              
        #We have all the ingredients, we just need to propagate the track for a given time
        t = np.linspace(0, self.ti[-1], 200)
        x, y, z = self.eval(t)
        ax1.plot3D(x, z, y, fmt)
        ax2.plot(x, y, fmt, label = 'Real track')
        #ax2.plot(0, 0, 'rx')
        ax3.plot(z, y, fmt)
        ax4.plot(z, x, fmt)
            
    def print(self):
        print('----Track info-----')
        print('x Poca:', self.x_cp)
        print('y Poca:', self.y_cp)
        print('z Poca:', self.z_cp)
        print('px:', self.pt*np.cos(self.phi))
        print('py:', self.pt*np.sin(self.phi))
        print('pz:', self.pz)
        print('q/pt:', self.q/self.pt)
