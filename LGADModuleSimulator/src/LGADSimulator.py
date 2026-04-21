from scipy.stats import landau
import numpy as np






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
        self.landau = landau(loc=self.loc, scale=self.scale)


    def getResponse(self, id, p, angle, t):
       
        mpv, scale = self.LandauParameters(id, p, self.thickness/np.cos(angle))
        ran = landau(loc=mpv, scale=scale)
        energyDeposit = ran.rvs(1)


        
    def getTOAandTOT(self, energyDeposit, mpv):

        samplingSpace = self.loc + 20.0*self.scale
        samplingStep = self.clock
        
        toa = 0.0
        l = 0.0
        while l < samplingSpace:

            val = self.landau.pdf(l) * energyDeposit
            if val > self.threshold:
               toa = l
               break
            l = l + samplingStep
                
        toc = 0.0
        l = samplingSpace
        while l > 0: 
            val = self.landau.pdf(l) * energyDeposit
            if val > self.threshold:
               toc = l
               break
            l = l - samplingStep

        SignalToNoise = (self.landau.pdf(self.loc) * energyDeposit / self.referenceChargeColl) / self.noiseLevel
        sigmaJitter1 = self.loc / SignalToNoise
        sigmaJitter2 = (toc - self.loc) / SignalToNoise
        sigmaTDC = self.sigmaTDC
        sigmaLandauNoise = self.evaluate(energyDeposit, mpv)
        sigmaToA = np.sqrt(sigmaJitter1**2 + sigmaTDC**2 + sigmaLandauNoise**2)
        sigmaToC = np.sqrt(sigmaJitter2**2 + sigmaTDC**2 + sigmaLandauNoise**2)


    

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
        
        return mpv, scale

               
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
    
    
    def FluenceVsRadius(self, r):
       
       return 1.937*math.power(r,-1.706)
    

    def GainVsFluence(self, f):
       
       return min(15.0,30.0-f)
    

   
