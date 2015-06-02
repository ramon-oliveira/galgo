from math import cos, exp, sqrt, pi
import json
import matplotlib.pyplot as plot
from galgo.factory import ga_factory

"""
Problem: Minimize the equation in fobjective (multidimensional)
"""


def fobjective(xs):
    sum1 = sum2 = 0.0
    for x in xs:
        sum1 += x ** 2
        sum2 += cos(2*pi*x)
    return 20 - (20*exp(-0.2*sqrt(sum1/len(xs)))) + exp(1) - exp(sum2/len(xs))


def ffitness(c):
    xs = []
    for g in c.genes:
        xs.append(g.decode())
    fo = fobjective(xs)
    ff = max(30 - fo, 0.0)
    return ff, fo


f = open("config2.json", "r")
jga = json.loads(f.read())

ga = ga_factory(jga)

npop = jga["population_size"]
nits = jga["n_iterations"]
neli = jga["k_elitist"]

lbest, cbest = ga.search(npop, nits, neli, ffitness)

print('Multidimensional problem')
print('Best solution:', cbest)

plot.ylabel('fitness')
plot.xlabel('generation')
plot.plot(lbest, label='best solution')
plot.legend(loc='lower right')
plot.savefig('outpu2.png')
