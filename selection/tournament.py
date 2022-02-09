import random

from selection.base import SelectionBase


class TournamentSelection(SelectionBase):
    def __init__(self, tournament_size: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament_size = tournament_size

    def select_next(self, population):
        selected = [random.choice(population) for _ in range(self.tournament_size)]
        return max(selected, key=lambda x: x.get_fitness())
