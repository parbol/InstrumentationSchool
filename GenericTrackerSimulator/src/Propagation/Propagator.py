############################################################################
############################################################################
############################################################################
############################################################################
import numpy as np


class Propagator:

    def __init__(self, B, ftr):

        self.ftr = ftr
        self.B = B

    def propagate(self, trajState, layer):

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
        
        # In cm per ns
        c = 29.9792458
        gamma = np.sqrt(1.0/(1.0 - trajState.beta**2))
        m = trajState.E / gamma
        w = trajState.q * 0.089880 * self.B / (gamma * m)
        vT = trajState.beta * np.sin(trajState.theta) * c
        R = vT/w
        vZ = trajState.beta * np.cos(trajState.theta) * c
        x_0 = trajState.x - R * (np.sin(w*trajState.t - trajState.phi) + np.sin(trajState.phi))
        y_0 = trajState.y - R * (np.cos(w*trajState.t - trajState.phi) - np.cos(trajState.phi))
        z_0 = trajState.z - vZ * trajState.t  

        x_c = x_0 + R * np.sin(trajState.phi)
        y_c = y_0 - R * np.cos(trajState.phi)

        #Estimating the intersection with a circle or with a plane
        finalT = 0             
        if layer.type == 0:
            
            ri2 = layer.R**2           
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
                    return
                else:      
                    y1_c = (-by - np.sqrt(rooty)) / (2.0 * ay)
                    y2_c = (-by + np.sqrt(rooty)) / (2.0 * ay)
                    if abs((y1_c - y_c) / R) > 1.0:
                        return
                    if abs((y2_c[j] - y_c) / R) > 1.0:
                        return
                    t1 = 1.0 / w * self.convertAngle((trajState.phi + np.arccos((y1_c - y_c) / R)))
                    t2 = 1.0 / w * self.convertAngle((trajState.phi + np.arccos((y2_c - y_c) / R)))
                    t3 = 1.0 / w * self.convertAngle((trajState.phi - np.arccos((y1_c - y_c) / R)))
                    t4 = 1.0 / w * self.convertAngle((trajState.phi - np.arccos((y2_c - y_c) / R)))
                    tarr = np.sort(np.array([t1, t2, t3, t4]), axis=None)
                    for ft in tarr:
                        if ft > 0:
                            finalT = ft
                            break
            else:
                x1_c = (-bx - np.sqrt(rootx)) / (2.0 * ax)
                x2_c = (-bx + np.sqrt(rootx)) / (2.0 * ax)
                if abs((x1_c - x_c) / R) > 1.0:
                    return
                if abs((x2_c - x_c) / R) > 1.0:
                    return
                t1 = 1.0 / w * self.convertAngle((trajState.phi + np.arcsin((x1_c - x_c) / R)))
                t2 = 1.0 / w * self.convertAngle((trajState.phi + np.arcsin((x2_c - x_c) / R)))
                t3 = 1.0 / w * self.convertAngle((trajState.phi + np.pi - np.arcsin((x1_c - x_c) / R)))
                t4 = 1.0 / w * self.convertAngle((trajState.phi + np.pi - np.arcsin((x2_c - x_c) / R)))
                tarr = np.sort(np.array([t1, t2, t3, t4]), axis=None)
                tv = 99999
                for ft in tarr:
                    if ft > 0:
                        finalT = ft
                        break
        else:
            finalT = (layer.z - z_0)/vZ
  
  


        return trajState