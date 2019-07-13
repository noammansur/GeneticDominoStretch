class DominoTile(object):
    def __init__(self, left, right, count):
        self.left = left
        self.right = right
        self.count = count

    def __repr__(self):
        return '({}, {})'.format(self.left, self.right)

    def __eq__(self, other):
        return self.count == other.count

    def __copy__(self):
        return DominoTile(self.left, self.right, self.count)


class DominoStretch(object):
    def __init__(self, domino_tiles, engine):
        self.domino_tiles = domino_tiles
        self.stretches, self.longest_stretch = self.split_stretch()
        self.fitness = engine.calculate_fitness(self)

    def __repr__(self):
        return 'Tiles: {}, Number of Stretches: {}, Longest: {}, Fitness = {}'.format(
            ','.join(str(t) for t in self.domino_tiles), len(self.stretches), len(self.longest_stretch), self.fitness)

    @property
    def signature(self):
        return ','.join([str(t.count) for t in self.domino_tiles])

    def split_stretch(self):
        longest_stretch_length = 1
        stretches = []
        current_stretch = [self.domino_tiles[0]]
        last_tile = self.domino_tiles[0]

        for tile in self.domino_tiles[1:]:
            if last_tile.right != tile.left:
                stretches.append(current_stretch)
                longest_stretch_length = max(longest_stretch_length, len(current_stretch))
                current_stretch = [tile]
            else:
                current_stretch.append(tile)
            last_tile = tile

        stretches.append(current_stretch)
        longest_stretch_length = max(longest_stretch_length, len(current_stretch))

        return stretches, next(s for s in stretches if len(s) == longest_stretch_length)
