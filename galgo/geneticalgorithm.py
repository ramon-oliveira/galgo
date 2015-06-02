from galgo.chromosome import Chromosome
from copy import deepcopy


class GeneticAlgorithm(object):

    def __init__(self, vars, enc, selection, crossover, mutation, scheduler):
        self.vars = vars
        self.enc = enc
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.scheduler = scheduler

    def search(self, npop, nits, neli, ffitness):
        generation = []

        for i in range(npop):
            generation.append(Chromosome(self.vars, self.enc))

        for c in generation:
            c.randomize()

        lbest = []
        lavg = []

        for t in range(nits):
            # Calculate fitness
            fit_sum = 0.0
            for c in generation:
                c.fitness, c.objective = ffitness(c)
                fit_sum += c.fitness
            lavg.append(fit_sum/len(generation))

            # Sort by fitness
            generation.sort(reverse=True)
            lbest.append(generation[0].fitness)

            # Schedule
            lf = [c.fitness for c in generation]
            lf = self.scheduler.schedule(lf)

            # Select
            s_i = self.selection.select(lf, npop - neli)

            # Generate next generation
            next_generation = []
            # - Pass elite
            for i in range(neli):
                next_generation.append(deepcopy(generation[i]))
            # - Crossover and Mutation
            # - - Pairs
            for i in range(0, len(s_i)-1, 2):
                a = s_i[i]
                b = s_i[i+1]
                c1, c2 = self.crossover.cross(generation[a], generation[b])
                next_generation.append(self.mutation.mutate(c1))
                next_generation.append(self.mutation.mutate(c2))

            # - - Forever alone
            if len(s_i) % 2 == i:
                a = s_i[len(s_i) - 1]
                next_generation.append(self.mutation.mutate(generation[a]))

            # Transfer generation
            generation = next_generation

        return lbest, generation[0]
