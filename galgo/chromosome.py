from galgo import gene


class Chromosome(object):

    """
    Class to represent the chromosome
    """

    def __init__(self, vars, encoding):
        """
        Arguments
            vars: Variables to be encoded
            encoding: type fo encoding will be used (real or binary)
        """
        self.genes = []
        self.fitness = None
        self.objective = None
        self.vars = vars
        self.encoding = encoding

        if encoding == "BINARY":
            for var in vars:
                self.genes.append(gene.BinaryGene(var))
        elif encoding == "REAL":
            for var in vars:
                self.genes.append(gene.RealGene(var))
        else:
            raise AttributeError

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return str(self.genes)

    def randomize(self):
        for g in self.genes:
            g.randomize()
