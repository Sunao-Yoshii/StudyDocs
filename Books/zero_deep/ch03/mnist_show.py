
import sys
import os
sys.path.append(os.pardir)

import numpy as np
from PIL import Image
from dataset.mnist import load_mnist


def img_show(img):
    pil_image = Image.fromarray(np.uint8(img))
    pil_image.show()


(x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)

img = x_train[1]
label = t_train[1]
print(label)

print(img.shape)  # (784,)
img = img.reshape(28, 28)  # 形状を元の画像サイズに変形
print(img.shape)  # (28, 28)

img_show(img)
