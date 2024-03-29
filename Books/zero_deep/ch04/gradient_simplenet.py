import sys, os
sys.path.append(os.pardir)

import numpy as np
from common.functions import softmax, cross_entropy_error
from common.gradient import numerical_gradient

class SimpleNet:
    def __init__(self):
        self.W = np.random.randn(2, 3) # ガウス分布で初期化

    def predict(self, x: np.array):
        return np.dot(x, self.W)

    def loss(self, x, t):
        z = self.predict(x)
        y = softmax(z)
        loss = cross_entropy_error(y, t)
        return loss


if __name__ == "__main__":
    net = SimpleNet()
    print(f'Current weight: \n{net.W}')

    x = np.array([0.6, 0.9])
    p = net.predict(x)
    print(f'Predict: {p}')
    print(f'Max Index: {np.argmax(p)}')

    t = np.array([0, 0, 1])
    print(f'Loss: {net.loss(x, t)}')
