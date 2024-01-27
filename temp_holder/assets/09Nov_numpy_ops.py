
import matplotlib.pyplot
import numpy as np
mystery_array = np.array([[[0, 1, 2, 3],
                           [4, 5, 6, 7]],

                          [[7, 86, 6, 98],
                           [5, 1, 0, 4]],

                          [[5, 36, 32, 48],
                           [97, 0, 27, 18]]])


print(mystery_array.ndim)
print(mystery_array.shape)
print(mystery_array)
print(mystery_array[:,:, 0])

k = np.arange(10, 30)
print(k)
print(type(k))

"""
Use Python slicing techniques on a to:

Create an array containing only the last 3 values of a - [27 28 29]

Create a subset with only the 4th, 5th, and 6th values - [13 14 15]

Create a subset of a containing all the values except for the first 12 (i.e., [22, 23, 24, 25, 26, 27, 28, 29])
- 22 23 24 25 26 27 28 29

Create a subset that only contains the even numbers (i.e, every second number)
"""
print("\ncheckkkk")
print(k[-3:])
print(k[3:6])
print(k[12:])
print(k[::2])


"""
Challenge 3
Reverse the order of the values in a, so that the first element comes last:

[29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10]"""
reversed_array = np.flip(k)
print(reversed_array)


"""Challenge 4
Print out all the indices of the non-zero elements in this array: [6,0,9,0,0,5,0]"""
t_aray = [6,0,9,0,0,5,0]
print(np.nonzero(t_aray))

t_np_array = np.array(t_aray)
print(t_np_array > 4)
print(np.nonzero(t_np_array > 4))
print(t_np_array[np.nonzero(t_np_array > 4)])


"""Challenge 5
Use NumPy to generate a 3x3x3 array with random numbers

Hint: Use the .random() function

Challenge 6
Use .linspace() to create a vector x of size 9 with values spaced out evenly between 0 to 100 (both included).

Challenge 7
Use .linspace() to create another vector y of size 9 with values between -3 to 3 (both included). Then plot x and y on a line chart using Matplotlib.

Challenge 8
Use NumPy to generate an array called noise with shape 128x128x3 that has random values. Then use Matplotlib's .imshow() to display the array as an image.

The random values will be interpreted as the RGB colours for each pixel.

"""


rng = np.random.default_rng(123456)
t_narray = rng.random(27)
t_narray = t_narray.reshape([3, 3, 3])
print(t_narray)
print(t_narray.shape)




t2_narray = np.linspace(0, 100, 9)
print(t2_narray)


# Use .linspace() to create another vector y of size 9 with values between -3 to 3 (both included).
# Then plot x and y on a line chart using Matplotlib.
t3_narray = np.linspace(-3, 3, 9)
import matplotlib.pyplot as plt

# plt.plot(t2_narray, t3_narray)
# plt.show()



# Use NumPy to generate an array called noise with shape 128x128x3 that has random values.
# Then use Matplotlib's .imshow() to display the array as an image.
# The random values will be interpreted as the RGB colours for each pixel.

rng = np.random.default_rng()
# noise = rng.random(128*128*3)
noise = rng.integers(40, 80, 128*128*3)
noise = noise.reshape((128, 128, 3))
print(noise)
# plt.imshow(noise)
# plt.show()


# rng = np.random.default_rng(seed=4567)
# print(rng.random())
# print(rng.random())



v1 = np.array([4, 5, 2, 7])
v2 = np.array([2, 1, 3, 3])

print(v1+v2)
print(v1*v2)
print(v1*2)


# broadcasting

array_2d = np.array([[1, 2, 3, 4],
                     [5, 6, 7, 8]])
print(array_2d*2)
print(array_2d+2)

print(np.zeros(20))

a1 = np.array([[1, 3],
               [0, 1],
               [6, 2],
               [9, 7]])

b1 = np.array([[4, 1, 3],
               [5, 8, 5]])

print(np.matmul(a1, b1))



