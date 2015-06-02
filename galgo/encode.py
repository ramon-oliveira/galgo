from galgo.chromosome import Chromosome


def binary_chromosome(variables, code):
    c = Chromosome(variables, "BINARY")

    i = 0
    for g in c.genes:
        g.code = code[i:i+len(g.code)]
        i += len(g.code)

    return c
