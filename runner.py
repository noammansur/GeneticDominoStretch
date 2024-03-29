import matplotlib.pyplot as plt
from random import randint, shuffle
from itertools import izip
import logging

from breeders import breed_naive, breed_longer
from genetic_algorithm_engine import DominoGeneticAlgorithm
from objects import DominoTile, DominoStretch


def init_loggers(show_debug=True):
    if NO_LOGS:
        return
    logging.getLogger().setLevel(logging.INFO if not show_debug else logging.DEBUG)


# Debug mode
NO_LOGS = False
DEBUG = False

# Parameters
NUMBER_OF_TILES = 200
POP_SIZE = 200
ELITE_SIZE = 20
MUTATION_RATE = 0.01
NUMBER_OF_GENERATIONS = 2000

# Optimization selection
USE_LONGER_BREED_METHOD = True
LEVEL_OF_PARALLELISM = 4

# Penalties
NUMBER_OF_STRETCHES_PENALTY = 10
STRETCH_LENGTH_PENALTY = 10

numbers = [randint(1, 6) for i in range(NUMBER_OF_TILES + 1)]
domino_tiles = [DominoTile(x, y, i) for i, (x, y) in enumerate(izip(numbers, numbers[1:]))]

breed_method = breed_longer if USE_LONGER_BREED_METHOD else breed_naive

engine = DominoGeneticAlgorithm(
    population_size=POP_SIZE, elite_size=ELITE_SIZE, mutation_rate=MUTATION_RATE,
    max_generations=NUMBER_OF_GENERATIONS, breed_method=breed_method,
    number_of_stretches_penalty=NUMBER_OF_STRETCHES_PENALTY, stretch_length_penalty=STRETCH_LENGTH_PENALTY,
    parallelism_level=LEVEL_OF_PARALLELISM)

solution_stretch = DominoStretch(domino_tiles, engine)
print('Expected Solution: {}'.format(solution_stretch))

shuffle(domino_tiles)
print('==============================================\n')

init_loggers(show_debug=DEBUG)
converged, gen_count, progress, solution = engine.run_genetic_algorithm(input=domino_tiles)
if converged:
    print('Converged in generation number %d' % gen_count)
else:
    print('Failed to converge after %d generations' % NUMBER_OF_GENERATIONS)

print("Final result: {}".format(solution))

# Plotting the improvement graph
plt.plot(progress)
plt.ylabel('Fitness')
plt.xlabel('Generation')
plt.show()
