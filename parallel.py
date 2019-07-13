from itertools import chain
from multiprocessing import Process, Manager


class ParallelExecutor(object):
    """
    A class to run a given method in parallel on a set of inputs
    """

    def __init__(self, func, input, level_of_parallelism):
        self.level_of_parallelism = level_of_parallelism
        self.func = func
        self.input = input

    def _get_partitions(self):
        return [self.input[i::self.level_of_parallelism] for i in xrange(self.level_of_parallelism)]

    def _execute_sequentially(self, input_partition, return_list):
        for single_input in input_partition:
            return_list.append(self.func(*single_input))

    def execute(self):
        manager = Manager()
        processes = []
        exec_results = []

        for input_partition in self._get_partitions():
            exec_results.append(manager.list())
            processes.append(Process(target=self._execute_sequentially, args=(input_partition, exec_results[-1])))
            processes[-1].start()

        map(lambda p: p.join(), processes)
        return list(chain.from_iterable(exec_results))


if __name__ == '__main__':
    def f(x):
        return x

    results = ParallelExecutor(f, [(i,) for i in range(12)], 4).execute()
    print results

