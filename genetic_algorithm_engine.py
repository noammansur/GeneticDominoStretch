import copy

from random import randint, shuffle
import random

from objects import DominoStretch
from parallel import ParallelExecutor
from utils import timing


class DominoGeneticAlgorithm(object):
    
    def __init__(self, population_size, elite_size, mutation_rate, max_generations, breed_method,
                 number_of_stretches_penalty, stretch_length_penalty, parallelism_level):
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.breed_method = breed_method
        self.number_of_stretches_penalty = number_of_stretches_penalty
        self.stretch_length_penalty = stretch_length_penalty
        self.parallelism_level = parallelism_level

    @timing
    def run_genetic_algorithm(self, input):
        """
        Runs main algorithm logic
        :param input: The Domino tiles to be used
        :type input: list of objects.DominoTile
        :return: The solution domino stretch or the best found
        :rtype: DominoStretch
        """
        pop = self._initial_population(self.population_size, input)

        progress = []
        gen = 0
        converged = False
        mutation_rate = self.mutation_rate
        last_solution_fitness = float('inf')

        while gen < self.max_generations:
            best_solution, pop = self._create_next_generation(
                pop, self.elite_size, mutation_rate, self.breed_method)
            if best_solution.fitness == 0:
                converged = True
                break

            elif last_solution_fitness == best_solution.fitness:
                # In case we didn't improve in the round we multiply the mutation rate by two to
                # kick us off the local minimum
                mutation_rate = min(1.0, 2 * mutation_rate)
            else:
                mutation_rate = self.mutation_rate

            print("Generation {} Ended, Current fitness: {}, Mutation rate {}".format(
                    gen, best_solution.fitness, mutation_rate))
            last_solution_fitness = best_solution.fitness
            progress.append(last_solution_fitness)
            gen += 1

        return converged, gen, progress, best_solution

    @timing
    def _create_next_generation(self, current_generation, elite_size, mutation_rate, breed_method):
        """
        The main algorithm flow, rank -> select best and create from them the mating pool -> breed -> mutate
        """
        ranked_pop = self._rank_results(current_generation)
        selection_results = self._selection(ranked_pop, elite_size)
        matingpool = self._mating_pool(current_generation, selection_results)
        children = self._breed_population(matingpool, elite_size, breed_method)
        next_generation = self._mutate(children, mutation_rate)
        return current_generation[ranked_pop[0][0]], next_generation

    @timing
    def _initial_population(self, population_size, input_tiles):
        """
        Create randomly the initial population
        """
        population = []

        for i in range(population_size):
            new_input = [copy.copy(tile) for tile in input_tiles]
            shuffle(new_input)
            population.append(DominoStretch(new_input, engine=self))
        return population

    @staticmethod
    def _create_random_stretch(input_tiles, engine):
        new_input = [copy.copy(tile) for tile in input_tiles]
        shuffle(new_input)
        return DominoStretch(new_input, engine=engine)

    def _rank_results(self, pop):
        """
        Rank the stretches by their fitness, lowest fitness first
        """
        return sorted([(idx, p.fitness) for idx, p in enumerate(pop)], key=lambda (idx, fitness): fitness)

    def _selection(self, ranked_pop, elite_size):
        """
        Select the best candidates to form with them the mating pool
        (1) Pick the elite (number is determined by elite_size)
        (2) Until you picked enough:
            -- Randomly choose 4 specs
            -- Take the fittest of them
        """
        selection_results = []

        for i in range(0, elite_size):
            selection_results.append(ranked_pop[i][0])

        while len(selection_results) < len(ranked_pop):
            candidates = [ranked_pop[randint(0, len(ranked_pop) - 1)] for _ in range(4)]
            best_candidate = min(candidates, key=lambda (idx, fitness): fitness)[0]
            selection_results.append(best_candidate)

        return selection_results

    def _mating_pool(self, current_generation, selection_results):
        """
        Build the mating pool with the selection
        """
        return [current_generation[idx] for idx in selection_results]

    def _breed_population(self, mating_pool, elite_size, breed_method):
        """
        Breed a new population using the mating pool
        It will be consisted of the elite group from previous generation and the
        breeding of two parents from the mating pool
        """
        children = []
        children_to_breed = len(mating_pool) - elite_size

        # Add the elite
        for i in range(0, elite_size):
            children.append(mating_pool[i])

        shuffle(mating_pool)
        pool = random.sample(mating_pool, len(mating_pool))
        breed_inputs = [(pool[i], pool[len(mating_pool) - i - 1], self) for i in range(children_to_breed)]
        children.extend(ParallelExecutor(breed_method, breed_inputs, self.parallelism_level).execute())

        return children

    def _mutate(self, children, mutation_rate):
        """
        Add mutation to the new children by shuffling tiles randomly
        """
        mutated_pop = []
    
        for child in children:
            if random.random() < mutation_rate:
                tiles = child.domino_tiles
                shuffle(tiles)
                mutated_pop.append(DominoStretch(tiles, engine=self))
            else:
                mutated_pop.append(child)
        return mutated_pop

    def calculate_fitness(self, domino_stretch):
        """
        Calculate the fitness for a given domino stretch based on the penalties defined
        """
        longest_stretch_length, number_of_stretches = len(domino_stretch.longest_stretch), len(domino_stretch.stretches)

        return (number_of_stretches - 1) * self.number_of_stretches_penalty + \
               (len(domino_stretch.domino_tiles) - longest_stretch_length) * self.stretch_length_penalty

