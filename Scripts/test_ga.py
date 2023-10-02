import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np


class TestGA(unittest.TestCase):
    def testGA(self):
        pop = poplib.Population(pop_size=10, gene_count=5)
        sim = simlib.Simulation()

        for generation in range(10):
            sim.eval_population(pop, 2400)
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            fitmap = poplib.Population.get_fitness_map(fits)

            print(generation, np.max(fits), np.mean(fits))

            fmax = np.max(fits)
            for cr in pop.creatures:
                if cr.get_distance_travelled() == fmax:
                    elite = cr
                    break

            new_gen = []
            for cid in range(len(pop.creatures)):
                p1_ind = poplib.Population.select_parent(fitmap)
                p2_ind = poplib.Population.select_parent(fitmap)
                dna = genlib.Genome.crossover(pop.creatures[p1_ind].dna,
                                              pop.creatures[p2_ind].dna)
                dna = genlib.Genome.point_mutate(dna, 0.1, 0.25)
                dna = genlib.Genome.grow_mutate(dna, 0.25)
                dna = genlib.Genome.shrink_mutate(dna, 0.25)
                cr = crlib.Creature(1)
                cr.update_dna(dna)
                new_gen.append(cr)

            new_gen[0] = elite
            csv_filename = str(generation) + "_elite.csv"
            genlib.Genome.to_csv(elite.dna, csv_filename)
            pop.creatures = new_gen


unittest.main()
