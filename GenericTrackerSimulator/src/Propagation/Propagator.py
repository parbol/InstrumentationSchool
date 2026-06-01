############################################################################
############################################################################
############################################################################
############################################################################


class Propagator:

    def __init__(self, B):

        self.B = B

    def propagate(self, trajState, layer):

        ##### In the transverse plane we have:
        ##### Px(t) = Pt cos(wt - phi) and Py(t) = -Pt sin(wt - phi)
        ##### x(t) = Pt/qB [sin(wt - phi) + sin(phi)] + x(0)
        ##### y(t) = Pt/qB [cos(wt - phi) - cos(phi)] + y(0)
        ##### Relation to the equation of the cirumference:
        ##### (x - x(0) - Pt/qB sin(phi))^2 + (y - y(0) + Pt/qB cos(phi))^2 = (Pt/qB)^2 
        ##### Therefore:
        ##### Radius = Pt/mw
        ##### Center of the circumference X = x(0) + Pt/qB sin(phi)
        ##### Center of the circumference Y = y(0) - Pt/qB cos(phi)


        return trajState