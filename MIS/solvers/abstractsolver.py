from abc import ABC, abstractmethod, abstractstaticmethod
import pathlib

class MWISSolver(ABC):

    @abstractmethod
    def load_weights(self, model_state_path):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def directory(self):
        pass

    @abstractstaticmethod
    def _prepare_instance(source_instance_file, cache_directory, **kwargs):
        pass

    @classmethod
    def _prepare_instances(C, instance_directory: pathlib.Path, cache_directory: pathlib.Path, **kwargs):
        import functools
        imap_unordered_bar(functools.partial(C._prepare_instance, cache_directory=cache_directory, **kwargs),
                           [graph_path.resolve() for graph_path in instance_directory.rglob("*.gpickle")], n_processes=32)
        # for graph_path in instance_directory.rglob("*.gpickle"):
        #     C._prepare_instance(graph_path.resolve(), cache_directory, **kwargs)

    @abstractmethod
    def train(self, train_data_path: pathlib.Path, results_path: pathlib.Path, parameters):
        pass

    @abstractmethod
    def solve(self, solve_data_path: pathlib.Path, results_path: pathlib.Path, parameters):
        pass


from multiprocessing import Pool
from tqdm import *


def imap_unordered_bar(func, args, n_processes=2):
    p = Pool(n_processes)
    args = list(args)
    # print(args)
    with tqdm(total=len(args)) as pbar:
        for i, res in tqdm(enumerate(p.imap_unordered(func, args))):
            pbar.update()
    pbar.close()
    p.close()
    p.join()
