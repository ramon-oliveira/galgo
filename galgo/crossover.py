import abc
import random

import galgo.encode as encode
from galgo.chromosome import Chromosome


class Crossover(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, probability):
        self.probability = probability

    @abc.abstractmethod
    def cross(self, p1, p2):
        pass


class BinaryCrossover(Crossover):

    def __init__(self, probability, ncuts):
        super(BinaryCrossover, self).__init__(probability)
        self.ncuts = ncuts

    def cross(self, p1, p2):
        assert len(p1.genes) == len(p2.genes)

        r = random.uniform(0.0, 1.0)
        if r > self.probability:
            return p1, p2

        clen = 0
        for g in p1.genes:
            clen += len(g.code)

        assert self.ncuts < clen

        cuts = [clen-1]
        for i in range(self.ncuts):
            while True:
                r = random.randint(0, clen-2)
                if r not in cuts:
                    break
            cuts.append(r)
        cuts.sort()

        p1code = []
        for g in p1.genes:
            p1code += g.code

        p2code = []
        for g in p2.genes:
            p2code += g.code

        assert len(p1code) == clen
        assert len(p2code) == clen

        c1code = []
        c2code = []
        i = j = 0
        while i < clen:
            while i <= cuts[j]:
                if j % 2 == 0:
                    c1code.append(p1code[i])
                    c2code.append(p2code[i])
                else:
                    c1code.append(p2code[i])
                    c2code.append(p1code[i])
                i += 1
            j += 1

        c1 = encode.binary_chromosome(p1.vars, c1code)
        c2 = encode.binary_chromosome(p2.vars, c2code)

        return c1, c2


class BlendCrossover(Crossover):

    def __init__(self, probability, alpha=0.5):
        super(BlendCrossover, self).__init__(probability)
        self.alpha = alpha

    def cross(self, p1, p2):
        assert len(p1.genes) == len(p2.genes)

        r = random.uniform(0.0, 1.0)
        if r > self.probability:
            return p1, p2

        c1 = Chromosome(p1.vars, p1.encoding)
        c2 = Chromosome(p2.vars, p2.encoding)

        for i in range(len(p1.genes)):
            maxv = max(p1.genes[i].decode(), p2.genes[i].decode())
            minv = min(p1.genes[i].decode(), p2.genes[i].decode())
            d = maxv - minv
            begin = max(p1.genes[i].domain.begin, minv - (d*self.alpha))
            end = min(p1.genes[i].domain.end, maxv + (d*self.alpha))
            c1.genes[i].encode(random.uniform(begin, end))
            c2.genes[i].encode(random.uniform(begin, end))

        return c1, c2


class AverageCrossover(Crossover):

    def __init__(self, probability):
        super(AverageCrossover, self).__init__(probability)

    def cross(self, p1, p2):
        assert len(p1.genes) == len(p2.genes)

        r = random.uniform(0.0, 1.0)
        if r > self.probability:
            return p1, p2

        c1 = Chromosome(p1.vars, p1.encoding)
        c2 = Chromosome(p2.vars, p2.encoding)

        for i in range(len(p1.genes)):
            avg = (p1.genes[i].decode()+p2.genes[i].decode())/2.0
            if random.randint(0, 1) == 0:
                c1.genes[i].encode(avg)
                c2.genes[i].encode(p2.genes[i].decode())
            else:
                c2.genes[i].encode(avg)
                c1.genes[i].encode(p1.genes[i].decode())

        return c1, c2
