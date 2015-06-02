from math import cos
import json
import matplotlib.pyplot as plot
from galgo.factory import ga_factory

"""
Problem: Maximize the equation in fobjective (unidimensional)
"""


def fobjetive(xs):
    return cos(20 * xs[0]) - abs(xs[0])/2 + (xs[0]*xs[0]*xs[0])/4.0


def ffitness(c):
    xs = [c.genes[0].decode()]
    fo = fobjetive(xs)
    ff = fo+4
    return ff, fo


f = open("config1.json", "r")
jga = json.loads(f.read())

ga = ga_factory(jga)

npop = jga["population_size"]
nits = jga["n_iterations"]
neli = jga["k_elitist"]

lbest, cbest = ga.search(npop, nits, neli, ffitness)

print('Unidimensional problem')
print('Best solution:', cbest)

plot.ylabel('fitness')
plot.xlabel('geracao')
plot.plot(lbest, label='melhor')
plot.legend(loc='lower right')
plot.savefig('output1.png')
