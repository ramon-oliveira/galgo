from bisect import bisect_left
import random
import abc


class Selection(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def select(self, lf, n):
        pass


class RouletteSelection(Selection):

    def __init__(self):
        super(RouletteSelection, self).__init__()

    def select(self, lf, n):
        selected = []
        if n == 0:
            return selected

        for i in range(0, n-1, 2):
            rl = self.get_roulette(lf)
            r = random.uniform(0.0, 1.0)
            s1 = bisect_left(rl, r)

            rl = self.get_roulette(lf, s1)
            r = random.uniform(0.0, 1.0)
            s2 = bisect_left(rl, r)
            selected.append(s1)
            selected.append(s2)

        if n % 2 == 1:
            rl = self.get_roulette(lf)
            r = random.uniform(0.0, 1.0)
            selected.append(bisect_left(rl, r))

        return selected

    def get_roulette(self, lf, ignore=-1):
        acu_fit_sum = sum(lf) - (lf[ignore] if ignore != -1 else 0)
        per_acu_sum = 0.0
        per_acu = []
        for i, f in enumerate(lf):
            if i != ignore:
                per_acu_sum += (float(f)/acu_fit_sum)
            per_acu.append(per_acu_sum)
        return per_acu


class TournamentSelection(Selection):

    def __init__(self, k):
        super(TournamentSelection, self).__init__()
        self.k = k

    def select(self, lf, n):
        selected = []
        if n == 0:
            return selected
        for i in range(0, n-1, 2):
            s1 = self.get_tournament(lf)
            s2 = self.get_tournament(lf, s1)
            selected.append(s1)
            selected.append(s2)
        return selected

    def get_tournament(self, lf, ignore=-1):
        l = []
        for i in range(self.k):
            while True:
                r = random.randint(0, len(lf)-1)
                if r not in l and ignore != r:
                    l.append(r)
                    break
        l.sort()
        return l[0]
