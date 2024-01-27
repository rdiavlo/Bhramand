
from scipy import datasets
import numpy as np
import matplotlib.pyplot as plt


img = datasets.face()
print(img)
# plt.imshow(img)
# plt.show()


"""
Challenge
What is the data type of img? Also, what is the shape of img and how many dimensions does it have?
What is the resolution of the image?"""
print(type(img))
print(img.shape)
print(img.ndim)

"""
"""
# GREYSCALE
# img_t = img / 255
# print(img_t)
# grey_vals = np.array([0.2126, 0.7152, 0.0722])
# img_t = np.matmul(img_t, grey_vals)
# plt.imshow(img_t, cmap="gray")

# flip image
# img_t = np.flip(img_t, (0, 1))

# rotate image
# img_t = np.rot90(img)
# plt.imshow(img_t)
# plt.show()


print(r"""  

  (0_/    \_o)
  /-(O)--(O)-\
 (__.  \/  .__)
====(__/\__)====
      `--'
      _||_
    /'.. ..'\
   | : _|_ : |
   ||: _|_ : ||
   ||: _|_ :  ||
   ||: _|_ :   ||
   ||:     :    ||
   ||:     :     ||
   ||:     :   ||
   ||:     :  ||
   || `..'   ||
   ( | || | | )
    \| | | |/
     | || |
     | || |
     | | | |
     | |  | |
     | |   | |
 __,-' |    | '-,__
(___,--'     `--,___) """)

# solarize
# print("="*50)
# img_t = 255 - img
# print(img_t[0][0])
# print("="*50)
# print(img[0][0])
# plt.imshow(img_t)
# plt.show()


# custom image
import PIL.Image as Image

c_img = Image.open("../temp_holder/assets/assets/yummy_macarons.jpg")
c_img = np.array(c_img)

print(c_img)
plt.imshow(255 - c_img)
plt.show()
