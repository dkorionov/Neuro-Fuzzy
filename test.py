import sys

# from memory_profiler import profile
from memory_profiler import profile

from fuzzy_logic import *

@profile
def func():
    x1 = TrainingSample(np.array([0.1, 0.9, 0.11, 0.7, 0.015, 0.8, 0.22, 0.37, 0.5]), "x1", 3, ["M", "S", "D"])
    x2 = TrainingSample(np.array([2.6, 0.5, 2.8, 1.3, 0.7, 0.45, 1.4, 2.8, 1.3]), "x2", 3, ["M", "S", "D"])
    d = TrainingSample(np.array([3.2, 7.1, 1.5, 4.1, 5.9, 5.5, 1.4, 2.8, 8.1]), "d", 3, ["M", "S", "D"])
    model = FuzzyModel()
    model.add_training_data(x1)
    model.add_training_data(x2)
    model.add_training_result(d)
    model.create_rules()
    # model.print_rules()

func()

print((0.1-0.47)/0.35)

