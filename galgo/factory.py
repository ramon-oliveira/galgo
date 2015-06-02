from galgo.geneticalgorithm import GeneticAlgorithm
from galgo.variable import Variable
from galgo.selection import RouletteSelection, TournamentSelection
from galgo.crossover import BinaryCrossover, BlendCrossover, AverageCrossover
from galgo.mutation import BinaryMutation, DeltaMutation
from galgo.scheduler import IdentityScheduler, LinearScheduler


def variables_factory(lv):
    vs = []
    for v in lv:
        vs.append(Variable(v["begin"], v["end"], v["precision"]))
    return vs


def ga_factory(jga):
    vs = variables_factory(jga["variables"])
    en = jga["encoding"]

    # Selection
    s = None
    if jga["selection"]["type"] == "ROULETTE":
        s = RouletteSelection()
    elif jga["selection"]["type"] == "TOURNAMENT":
        s = TournamentSelection(jga["selection"]["size"])
    else:
        raise AttributeError

    # Crossover
    c = None
    ctype = jga["crossover"]["type"]
    cprobability = jga["crossover"]["probability"]
    if ctype == "BINARY":
        c = BinaryCrossover(cprobability, jga["crossover"]["n_cut"])
    elif ctype == "BLEND":
        c = BlendCrossover(cprobability, jga["crossover"]["alpha"])
    elif ctype == "AVERAGE":
        c = AverageCrossover(cprobability)
    else:
        raise AttributeError

    # Mutation
    m = None
    mtype = jga["mutation"]["type"]
    mprobability = jga["mutation"]["probability"]
    if mtype == "BINARY":
        m = BinaryMutation(mprobability)
    elif mtype == "DELTA":
        m = DeltaMutation(mprobability)
    else:
        raise AttributeError

    # Scheduler
    sc = None
    sctype = jga["scheduler"]
    if sctype == "IDENTITY":
        sc = IdentityScheduler()
    elif sctype == "LINEAR":
        sc = LinearScheduler(jga["n_iterations"])
    else:
        raise AttributeError

    return GeneticAlgorithm(vs, en, s, c, m, sc)
