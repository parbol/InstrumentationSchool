###########################################################
###########################################################
###########################################################
from scipy.stats import landau
import numpy as np
import matplotlib.pyplot as plt



class LGADSimulator:

    def __init__(self, thickness, radius, intLumi, loc, scale, clock, threshold):
       
        self.thickness = thickness
        self.radius = radius
        self.intLumi = intLumi
        self.fluence = self.FluenceVsRadius(self.radius) * self.intLumi
        self.gain = self.GainVsFluence(self.fluence)
        self.loc = loc
        self.scale = scale
        self.clock = clock
        self.threshold = threshold
        self.signal = landau(loc=self.loc, scale=self.scale)
        self.signalMax = self.signal.pdf(self.scale)
        self.fCPerGev = 0.160217663/0.015

    #######################################################
    def getResponse(self, id, p, angle, t):
       
        mpv, scale = self.LandauParameters(id, p, self.thickness/np.cos(angle))
        print('MPV:', mpv)
        ran = landau(loc=mpv, scale=scale)
        energyDeposit = ran.rvs(1)[0]
        charge = energyDeposit * self.fCPerGev * self.gain
        print('Gain', self.gain)
        print('Charge', charge)
        mpcharge = mpv * self.fCPerGev * self.gain 
        toa, tot = self.getTOAandTOT(charge, mpcharge, t)
        return toa, tot, charge


    #######################################################    
    def getTOAandTOT(self, charge, mpcharge, t):

        #Return negative tot if no signal
        if self.signalMax * charge <= self.threshold:
           return 0, -1
        samplingSpace = self.loc + 20.0*self.scale
        samplingStep = self.clock
        print('Sampling between', 0, samplingSpace, self.threshold)
        toa = 0.0
        l = 0.0
        while l < samplingSpace:

            val = self.signal.pdf(l) * charge
            print(val)
            if val > self.threshold:
               toa = l
               break
            l = l + samplingStep
                
        toc = 0.0
        l = samplingSpace
        while l > 0: 
            val = self.signal.pdf(l) * charge
            if val > self.threshold:
               toc = l
               break
            l = l - samplingStep

        #SignalToNoise = (self.landau.pdf(self.loc) * energyDeposit / self.referenceChargeColl) / self.noiseLevel
        #sigmaJitter1 = self.loc / SignalToNoise
        #sigmaJitter2 = (toc - self.loc) / SignalToNoise
        #sigmaTDC = self.sigmaTDC
        #sigmaLandauNoise = self.evaluate(energyDeposit, mpv)
        #sigmaToA = np.sqrt(sigmaJitter1**2 + sigmaTDC**2 + sigmaLandauNoise**2)
        #sigmaToC = np.sqrt(sigmaJitter2**2 + sigmaTDC**2 + sigmaLandauNoise**2)

        return t+toa, t+toc
    

    #######################################################    
    def LandauParameters(self, id, p, l):
       
        #https://inspirehep.net/files/c19072326d8b479e4fa9b8ca7a57cf0e

        #Some constants adapted to silicon
        I = 173e-6 # Ionizing potential in MeV
        delta = 0.0 # Shielding term (not considered)
        mec2 = 0.511   # MeV (electron rest mass)
        
        # Kinematics
        m = self.getMass(id)
        E = np.sqrt(p**2 + m**2)
        gamma = E / m
        beta = np.sqrt(1 - (1/gamma)**2)
        
        scale = 0.017825 * l / beta**2 # MeV
        mpv = scale * (np.log(2 * mec2 * beta**2 * gamma**2/I) + np.log(scale/I) + 0.2 - beta**2 - delta) # MeV
        
        return 0.001*mpv, 0.001*scale #In GeV


    #######################################################    
    def getMass(self, id):
       
        #All masses in GeV
        if abs(id) == 13:
          
          return 0.10566
       
        elif abs(id) == 11:
          
          return 0.00051
       
        elif abs(id) == 321:
          
          return 0.49368
       
        elif abs(id) == 2212:
          
          return 0.93827

        else:
          
          return 0.13957
    

    #######################################################    
    def FluenceVsRadius(self, r):
       
       return 1.937*np.power(r,-1.706)
    
    
    #######################################################    
    def GainVsFluence(self, f):
       
       return min(15.0,30.0-f)
    

    #######################################################   
    def drawEvent(self, ax, id, p, angle, t):
       
        toa, tot, charge = self.getResponse(id, p, angle, t)
        print(toa, tot, charge)
        if tot == -1:
           print('No signal detected')
           return
        n = int(4.0 * tot/self.clock)
        a = np.linspace(toa-tot, toa + 3.0*tot, n)
        ax.plot(a, self.signal.pdf(a), color = 'b')
        ax.axvline(x = toa, color = 'b', linestyle='dashed')
        ax.axvline(x = tot, color = 'b', linestyle='dashed')
        ax.axhline(y = self.threshold, color = 'r', linestyle='dashed')
        ax.set_xlabel('Time [ns]')
        ax.set_ylabel('Charge [fC]')

