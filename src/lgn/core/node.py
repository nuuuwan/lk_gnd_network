from dataclasses import dataclass

from lgn.utils import shape_utils


@dataclass
class Node:
    i: int
    name: str
    centroid: list
    population: int
    area: int

    @staticmethod
    def from_ent(i: int, ent):
        raw_geo = ent.get_raw_geo()
        area = shape_utils.compute_area(raw_geo)
        population = ent.population

        return Node(
            i = i,
            name=ent.name,
            centroid=ent.centroid,
            population=population,
            area=area,
        )

    def __str__(self):
        return f'({self.i:d}) {self.name}'