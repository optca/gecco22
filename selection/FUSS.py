import random

from evolalg.selection.selection import Selection


class FitnessUniformSelectionScheme(Selection):
    def __init__(self, e, fit_attr="fitness", max_items=None, *args, **kwargs):
        self.e = e
        self.fit_attr = fit_attr
        self.max_items = max_items

        self.population = []

    def get_random_value(self, minimum, maximum):
        return random.uniform(minimum - 0.5 * self.e, maximum + 0.5 * self.e)

    def select_next(self, min_fitness, max_fitness):
        random_value = self.get_random_value(min_fitness, max_fitness)
        return min(self.population, key=lambda x: abs(getattr(x, self.fit_attr) - random_value))

    def call(self, population: list, count=None):
        result = []
        if count is None:
            count = len(population)

        for i in population:
            self.population.append(i)
            if self.max_items is not None:
                if len(self.population) > self.max_items:
                    temp = []
                    self.population = sorted(self.population, key=lambda x: getattr(x, self.fit_attr))
                    for j in range(len(self.population) - 5):
                        interval_mean = sum([getattr(x, self.fit_attr) for x in self.population[j:j+5]]) / 5
                        temp.append(interval_mean - getattr(self.population[i], self.fit_attr))
                    m = temp.index(min(temp))
                    del_index = random.randint(m, m + 5)
                    self.population.pop(del_index)

        max_fitness = getattr(max(self.population, key=lambda x: getattr(x, self.fit_attr)), self.fit_attr)
        min_fitness = getattr(min(self.population, key=lambda x: getattr(x, self.fit_attr)), self.fit_attr)

        for _ in range(count):
            selected = self.select_next(min_fitness, max_fitness)
            result.append(selected)

        return result
