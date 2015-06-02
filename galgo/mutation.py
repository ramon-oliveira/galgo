import abc
import random

import galgo.encode as encode


class Mutation(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, probability):
        self.probability = probability

    @abc.abstractmethod
    def mutate(self, c):
        pass


class BinaryMutation(Mutation):

    def __init__(self, probability):
        super(BinaryMutation, self).__init__(probability)

    def mutate(self, c):
        newcode = []
        for g in c.genes:
            newcode += g.code

        for i in range(len(newcode)):
            r = random.uniform(0.0, 1.0)
            if r < self.probability:
                newcode[i] = not newcode[i]

        return encode.binary_chromosome(c.vars, newcode)


class DeltaMutation(Mutation):

    def __init__(self, probability):
        super(DeltaMutation, self).__init__(probability)

    def mutate(self, c):
        for i in range(len(c.genes)):
            r = random.uniform(0.0, 1.0)
            if r < self.probability:
                xi = c.genes[i].decode()
                dbegin = c.genes[i].domain.begin
                dend = c.genes[i].domain.end

                u = random.uniform(dbegin, dend)
                if random.randint(0, 1) == 0:
                    xi -= u/10
                else:
                    xi += u/10

                xi = max(xi, dbegin)
                xi = min(xi, dend)
                c.genes[i].encode(xi)

        return c
