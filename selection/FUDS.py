from evolalg.selection.tournament import TournamentSelection
from evolalg.selection.selection import Selection
import random
import math


class FitnessUniformDeletionScheme(Selection):
    def __init__(self, popsize: int, tournament_size: int, fmin: float, fmax: float, fit_attr='fitness', *args, **kwargs):
        self.fit_attr = fit_attr
        self.levels = []
        self.fmin = fmin
        self.fmax = fmax
        self.popsize = popsize
        self.tournament_size = tournament_size
        self.num_of_levels = int(math.sqrt(popsize))
        self.levels = [[] for _ in range(self.num_of_levels)]
        self.tournament = TournamentSelection(tournament_size=self.tournament_size)

    def select_next(self):
        population = []
        for level in self.levels:
            population += level
        return self.tournament.select_next(population)

    def add(self, ind):
        # deletion
        levels_len = [len(x) for x in self.levels]
        max_len = max(levels_len)
        level_index = levels_len.index(max_len)
        random_index = random.randint(0, len(self.levels[level_index]) - 1)
        self.levels[level_index].pop(random_index)

        eps = (self.fmax - self.fmin) / self.num_of_levels
        level = int((getattr(ind, self.fit_attr) - self.fmin) / eps)
        if level == self.num_of_levels:
            level -= 1
        self.levels[level].append(ind)

    def init(self, population):
        eps = (self.fmax - self.fmin) / self.num_of_levels
        for ind in population:
            level = int((getattr(ind, self.fit_attr) - self.fmin) / eps)
            if level == self.num_of_levels:
                level -= 1
            self.levels[level].append(ind)

    def call(self, population: list, count=None):
        pass
