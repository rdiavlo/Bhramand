import numpy as np
import matplotlib.pyplot as plt
from scipy import misc


# 1-D array
my_array = np.array([1.1, 9.2, 8.1, 4.7])

print(my_array.shape)
print(my_array[2])
print(my_array.ndim)




class ArrayWrapper(np.ndarray):
    def __init__(self, elements):
        self.name = None
        self.array = np.array(elements)


# 2-D array
array_2d = ArrayWrapper([[1, 2, 3, 9], [5, 6, 7, 8]])
array_2d.name = "Gorgonzallllaa"
print(f'{array_2d.name} has {array_2d.ndim} dimensions')
print(f'Its shape is {array_2d.shape}')
print(f'It has {array_2d.shape[0]} rows and {array_2d.shape[1]} columns')
print(array_2d)


"""
Features of numpy
shape

broadcast
"""
