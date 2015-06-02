import random
import abc
from math import floor, log


class Gene(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, domain):
        self.domain = domain

    @abc.abstractmethod
    def decode(self):
        pass

    @abc.abstractmethod
    def encode(self, n):
        pass

    def randomize(self):
        r = random.uniform(self.domain.begin, self.domain.end)
        self.encode(r)

    def trunc_precision(self, n):
        n /= self.domain.precision
        return round(n)*self.domain.precision

    def __repr__(self):
        return '%.4f' % (self.decode())


class BinaryGene(Gene):

    def __init__(self, domain):
        super(BinaryGene, self).__init__(domain)
        L = floor(log((domain.end-domain.begin)/domain.precision, 2)) + 1
        self.code = [False]*int(L)

    def decode(self):
        d = 0
        for i in range(len(self.code)):
            d += (1 << i) if self.code[i] else 0
        dbegin = self.domain.begin
        dend = self.domain.end
        ret = dbegin + (float(dend-dbegin)/((1 << len(self.code)) - 1))*d
        return self.trunc_precision(ret)

    def encode(self, x):
        x = self.trunc_precision(x)
        dbegin = self.domain.begin
        dend = self.domain.end
        dprecision = self.domain.precision
        assert (x > (dbegin-dprecision) and x < (dend+dprecision))

        y = ((1 << len(self.code)) - 1) * (x-dbegin)
        y /= (dend - dbegin)

        yint = int(round(y))

        for i in range(len(self.code)):
            self.code[i] = True if (yint & (1 << i)) > 0 else False


class RealGene(Gene):

    def __init__(self, domain):
        super(RealGene, self).__init__(domain)
        self.code = 0

    def decode(self):
        return self.code

    def encode(self, x):
        x = self.trunc_precision(x)
        assert x >= self.domain.begin and x <= self.domain.end
        self.code = x
