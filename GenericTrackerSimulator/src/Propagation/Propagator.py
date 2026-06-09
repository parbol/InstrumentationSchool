############################################################################
############################################################################
############################################################################
############################################################################
import numpy as np
from GenericTrackerSimulator.src.Propagation.trajectoryState import trajectoryState
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)


class Propagator:

    def __init__(self, B):

        self.B = B
    
    ###############################################################
    def propagate(self, ts, layer):

        ##################### Track parameters with known vertex #######################
        ##### x(0) -> X position of the vertex
        ##### y(0) -> Y position of the vertex
        ##### z(0) -> Z position of the vertex
        ##### phi -> Direction of the particle in the transverse plane
        ##### eta -> Direction of the particle in the longitudinal plane 
        ##### pt -> transverse momentum
        ##### charge ->self.rt = pt / (self.q * b) * (1000.0/2.998) the charge
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
        
        # Angular frequency of the helix
        w = ts.q * 0.089880 * self.B / (ts.gamma * ts.m)
        # Curvature radius
        R = ts.vT/w
        # Redefine the time in such a way that the trajectory state lives in t = 0
        # In these conditions:
        x0 = ts.x 
        y0 = ts.y
        z0 = ts.z
        t0 = ts.t

        x_c = x0 + R * np.sin(ts.phi)
        y_c = y0 - R * np.cos(ts.phi)

        # The final time will be stored here
        finalT = 0             
        
        #Estimating the intersection with a circle or with a plane
        if layer.type == 0:
            ri2 = layer.R**2           
            x_0 = x_c
            y_0 = y_c
            delta = -R**2 + x_0**2 + y_0**2 + ri2
            ax = 4. * x_0**2 + 4. * y_0**2
            bx = -4. * delta * x_0
            cx = delta**2 - 4. * y_0**2 * ri2
            ay = 4. * x_0**2 + 4. * y_0**2
            by = -4. * delta * y_0
            cy = delta**2 - 4. * x_0**2 * ri2
            rootx = bx**2 - 4.0 * ax * cx
            rooty = by**2 - 4.0 * ay * cy
            x1_c = 0
            x2_c = 0
            y1_c = 0
            y2_c = 0
            if rootx < 0:
                if rooty < 0:
                    return None, False
                else:      
                    y1_c = (-by - np.sqrt(rooty)) / (2.0 * ay)
                    y2_c = (-by + np.sqrt(rooty)) / (2.0 * ay)
                    if abs((y1_c - y_c) / R) > 1.0:
                        return None, False
                    if abs((y2_c - y_c) / R) > 1.0:
                        return None, False
                    t1 = 1.0 / w * self.convertAngle((ts.phi + np.arccos((y1_c - y_c) / R)))
                    t2 = 1.0 / w * self.convertAngle((ts.phi + np.arccos((y2_c - y_c) / R)))
                    t3 = 1.0 / w * self.convertAngle((ts.phi - np.arccos((y1_c - y_c) / R)))
                    t4 = 1.0 / w * self.convertAngle((ts.phi - np.arccos((y2_c - y_c) / R)))
                    tarr = np.sort(np.array([t1, t2, t3, t4]), axis=None)
                    for ft in tarr:
                        if ft > 1e-3:
                            finalT = ft
                            break
            else:
                x1_c = (-bx - np.sqrt(rootx)) / (2.0 * ax)
                x2_c = (-bx + np.sqrt(rootx)) / (2.0 * ax)
                if abs((x1_c - x_c) / R) > 1.0:
                    return None, False
                if abs((x2_c - x_c) / R) > 1.0:
                    return None, False
                t1 = 1.0 / w * self.convertAngle((ts.phi + np.arcsin((x1_c - x_c) / R)))
                t2 = 1.0 / w * self.convertAngle((ts.phi + np.arcsin((x2_c - x_c) / R)))
                t3 = 1.0 / w * self.convertAngle((ts.phi + np.pi - np.arcsin((x1_c - x_c) / R)))
                t4 = 1.0 / w * self.convertAngle((ts.phi + np.pi - np.arcsin((x2_c - x_c) / R)))
                tarr = np.sort(np.array([t1, t2, t3, t4]), axis=None)
                for ft in tarr:
                    if ft > 1e-3:
                        finalT = ft
                        break
        # If the intersection is with the endcap 
        else:
            finalT = (layer.z - z0)/ts.vZ
        if finalT <= 1e-3:
            return None, False
        finalPhi = -w * finalT + ts.phi
        finalX = R * (np.sin(w*finalT - ts.phi) + np.sin(ts.phi)) + x0
        finalY = R * (np.cos(w*finalT - ts.phi) - np.cos(ts.phi)) + y0
        finalZ = ts.vZ * finalT + z0
        finalT = finalT + t0
        # Build new trajectoy State
        newTs = trajectoryState(x = finalX, y = finalY, z = finalZ, t = finalT, phi = finalPhi, eta = ts.eta, E = ts.E, q = ts.q, beta = ts.beta)

        return newTs, True
    
    ###############################################################
    def convertAngle(self, theta):
        if theta > np.pi:
            return theta - np.pi * 2.0
        elif theta < -np.pi:
            return theta + np.pi * 2.0
        return theta 

    ###############################################################
    def finePropagation(self, ts, layer):

        if layer.type == 0:

            m, newts, valid = self.finePropagationBarrel(ts, layer)
            return m, newts, valid
        
        else:

            m, newts, valid = self.finePropagationEndcap(ts, layer)
            return m, newts, valid
        
    ###############################################################
    def finePropagationBarrel(self, ts, layer):

        storedTraj = []
        trays = []
        for tray in layer.nTrays:
            newTraj, valid = tray.plane.intersection(self.B, ts)
            if not valid:
                continue
            print('holaaaa')
            if tray.isInside(tray.toLocal(np.asarray([newTraj.x, newTraj.y, newTraj.z]))):
                print('never here')
                storedTraj.append(newTraj)
                trays.append(tray)
                
        for tray in layer.pTrays:
            newTraj, valid = tray.plane.intersection(self.B, ts)
            if not valid:
                continue
            print('holaaaa')
            if tray.isInside(tray.toLocal(np.asarray([newTraj.x, newTraj.y, newTraj.z]))):
                print('never here')
                storedTraj.append(newTraj)
                trays.append(tray) 
        
        if len(storedTraj) == 0:
            return None, None, False
        
        tmin = 9999.0
        theTray = None
        theTraj = None
        for i, ts in enumerate(storedTraj):
            if ts.t < tmin:
                tmin = ts.t
                theTray = trays[i]
                theTraj = ts
        
        for m in theTray.modules:
            if m.isInside(m.toLocal(np.asarray([theTraj.x, theTraj.y, theTraj.z]))):
                return m, theTraj, True
            
        return None, None, False        
        
                
    ###############################################################
    def finePropagationEndcap(self, ts, layer):

        storedTraj = []
        trays = []
        for tray in layer.Trays:
            newTraj, valid = tray.plane.intersection(self.B, ts)
            if not valid:
                continue
            if tray.isInside(tray.toLocal(np.asarray([newTraj.x, newTraj.y, newTraj.z]))):
                storedTraj.append(newTraj)
                trays.append(tray)
        if len(storedTraj) == 0:
            return None, None, False
        tmin = 9999.0
        theTray = None
        theTraj = None
        for i, ts in enumerate(storedTraj):
            if ts.t < tmin:
                tmin = ts.t
                theTray = trays[i]
                theTraj = ts
        
        for m in theTray.modules:
            if m.isInside(m.toLocal(np.asarray([theTraj.x, theTraj.y, theTraj.z]))):
                return m, theTraj, True
            
        return None, None, False        
          