
import math
import matplotlib.pyplot as plt, numpy as np

a = [1, 2, 3]



# for i in a:
#         t_param = i*4
#         res = sigmoid_func(t_param)
#         print(round(res, 4))
# print("--"*50)
# for i in a:
#         t_param = i*2
#         res = sigmoid_func(t_param)
#         print(round(res, 4))
# print("--"*50)
# for i in a:
#         t_param = i
#         res = sigmoid_func(t_param)
#         print(round(res, 4))
# print("--"*50)
# for i in a:
#         t_param = i*0.4
#         res = sigmoid_func(t_param)
#         print(round(res, 4))
# print("--"*50)

c = 1
def sigmoid_func(inp):
        z = inp * c
        out = 1/(1 + math.exp(-z))
        return out

for i in range(18):
        x = np.linspace(-1, 1, 500)
        print(x)
        y = np.array(list(map(sigmoid_func, x)))
        print(y)

        pt = plt.scatter(x, y)
        c += 1
        print("LOOP...", c)


plt.show()