from functools import cached_property

import numpy as np

SPEED_WALK, SPEED_TRAIN = 4, 60


class NetworkVector:
    @cached_property
    def m_distance_walking(self):
        n = self.n_nodes
        m = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance = self.get_distance(i, j)
                else:
                    distance = 0

                m[i, j] = distance
        return m

    @cached_property
    def m_distance_railway(self):
        return np.matrix(self.dist_matrix.todense())

    @cached_property
    def v_population(self):
        return np.matrix(
            [node.population / 1_000.0 for node in self.node_list],
            dtype=float,
        )

    @cached_property
    def m_population_pairs(self):
        return np.transpose(self.v_population) * self.v_population

    @cached_property
    def average_travel_time(self):
        travel_time_walking = self.m_distance_walking / SPEED_WALK
        travel_time_railway = self.m_distance_railway / SPEED_TRAIN

        travel_time = np.minimum(
            travel_time_walking,
            travel_time_railway,
        )

        pop_pairs = self.m_population_pairs
        pop_pairs_weighted_travel_time = np.multiply(pop_pairs, travel_time)

        average_meet_time = np.sum(pop_pairs_weighted_travel_time) / np.sum(
            pop_pairs
        )
        return average_meet_time
