from scipy.stats import landau
import numpy as np






class LGADSimulator:

    def __init__(self, thickness, radius, intLumi, loc, scale):
       
        self.thickness = thickness
        self.radius = radius
        self.intLumi = intLumi
        self.fluence = self.FluenceVsRadius(self.radius) * self.intLumi
        self.gain = self.GainVsFluence(self.fluence)
        self.loc = loc
        self.scale = scale


    def getResponse(self, id, p, angle, t):
       
        energyDeposit = self.bethe_block(p, id, self.thickness*np.cos(angle)) * self.gain
        MPV = self.MostProbableValue(p, id)



        


    def bethe_bloch(self, p_particle, id, length):
          

        m = self.getMass(id)
        m_particle = m * 1000.0
        z = 1.0

        # Physical Constants
        c = 299792458  # m/s
        mec2 = 0.511   # MeV (electron rest mass)
        K = 0.307075   # MeV cm^2 / mol
        # Material Properties (example: Silicon)
        # Z: Atomic number, A: Atomic mass (g/mol), I: Ionization potential (MeV)
        Z_target = 14
        A_target = 28.085
        I = 173e-6 # MeV
        d = 2.32 # g/cm3 (Si)

        # Kinematics
        # Energy in MeV
        # To MeV
        p = p_particle * 1000
        E = np.sqrt(p**2 + m**2)
        gamma = E / m
        beta = np.sqrt(1 - (1/gamma)**2)
    
        # Maximum energy transfer
        Tmax = (2 * mec2 * beta**2 * gamma**2) / (1 + 2 * gamma * (mec2 / m_particle) + (mec2 / m_particle)**2)

        epsilon = K * z**2 * (Z_target / A_target) * (1 / beta**2) * 0.5  
        # Bethe-Bloch Formula
        stopping_power = epsilon * (np.log(2 * mec2 * beta**2 * gamma**2 * Tmax / I**2) - beta**2)
        deltaE = stopping_power * d * length
        DeltaEMPV = deltaE + epsilon * (beta**2 + np.log(epsilon/Tmax)+0.194)
        
    
        #in GeV
        return stopping_power * d * length


    def MostProbableValue(self, p, id):
       
        if abs(id) == 13:
          
          return 1.21561e-05 + 8.89462e-07 / (p * p)
       
        elif abs(id) == 11:
          
          return 1.30030e-05 + 1.55166e-07 / (p * p)
       
        elif abs(id) == 321:
          
          return 1.20998e-05 + 2.47192e-06 / (p * p * p)
       
        elif abs(id) == 2212:
          
          return 1.13666e-05 + 1.20093e-05 / (p * p)

        else:
          
          return 1.24531e-05 + 7.16578e-07 / (p * p)
        

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
    

   
