from objects import DominoStretch
from random import randint
import copy


def breed_naive(parent1, parent2, engine):
    number_of_tiles = len(parent1.domino_tiles)
    gene_a = randint(0, number_of_tiles - 1)
    gene_b = randint(0, number_of_tiles - 1)

    start_gene, end_gene = sorted([gene_a, gene_b])
    first_parent_tiles = parent1.domino_tiles[start_gene: end_gene + 1]
    second_parent_tiles = [t for t in parent2.domino_tiles if t not in first_parent_tiles]

    if len(second_parent_tiles):
        cutting_point = randint(0, len(second_parent_tiles) - 1)
        new_tiles = second_parent_tiles[:cutting_point] + first_parent_tiles + second_parent_tiles[cutting_point:]
    else:
        new_tiles = first_parent_tiles

    return DominoStretch([copy.copy(tile) for tile in new_tiles], engine=engine)


def breed_longer(parent1, parent2, engine):
    first_parent_tiles = parent1.longest_stretch
    second_parent_tiles = [t for t in parent2.domino_tiles if t not in first_parent_tiles]

    if len(second_parent_tiles):
        cutting_point = randint(0, len(second_parent_tiles) - 1)
        new_tiles = second_parent_tiles[:cutting_point] + first_parent_tiles + second_parent_tiles[cutting_point:]
    else:
        new_tiles = first_parent_tiles

    return DominoStretch([copy.copy(tile) for tile in new_tiles], engine=engine)
