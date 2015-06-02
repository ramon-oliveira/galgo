
class IdentityScheduler(object):

    def __init__(self):
        pass

    def schedule(self, lf):
        return lf


class LinearScheduler(object):

    def __init__(self, nits):
        self.C = 1.2
        self.nits = nits
        self.inc = 0.8 / nits

    def schedule(self, lf):
        fmax = lf[0]
        fmin = lf[len(lf) - 1]
        favg = sum(lf)/len(lf)

        alpha = None
        beta = None

        if fmax == fmin:
            self.C += self.inc
            return lf

        if fmin > (self.C*favg - fmax)/(self.C - 1):
            alpha = (favg*(self.C - 1))/(fmax - favg)
            beta = (favg*(fmax - self.C*favg))/(fmax - favg)
        else:
            alpha = favg/(favg - fmin)
            beta = -fmin*favg/(favg - fmin)

        lf = [alpha*f + beta for f in lf]

        self.C += self.inc

        return lf
