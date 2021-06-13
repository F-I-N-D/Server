from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
import numpy as np

drones = [
    [100, 100],
    [50, 50],
    [400, 200],
]

locations = [
    [100, 100], 
    [200, 100],
    [300, 100]
]

tmp = cdist(drones, locations, "sqeuclidean")
_, optionalLocation = linear_sum_assignment(tmp)

print(optionalLocation)