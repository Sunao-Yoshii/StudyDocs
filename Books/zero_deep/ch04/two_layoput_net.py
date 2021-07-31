import sys, os
import numpy as np
sys.path.append(os.pardir)

from common.functions import *
from common.gradient import numerical_gradient


class TwoLayoutNet:

    def __init__(self, \
                 input_size: int,
                 hidden_size: int,
                 output_size: int,
                 weight_init_std = 0.01):
        # Weight の初期化
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)


    def predict(self, x):
        """NN での判定処理"""
        w1, w2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']

        a1 = np.dot(x, w1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, w2) + b2
        y = softmax(a2)
        return y


    def loss(self, x, t):
        """損失関数: 期待値との損失誤差を計算する"""
        y = self.predict(x)
        return cross_entropy_error(y, t)


    def accuracy(self, x, t):
        """正確性: どの程度結果が答えに近いか計算する"""
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        t = np.argmax(t, axis=1)
        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy


    def numerical_gradient(self, x, t):
        """損失誤差を元に、値を微分した結果を返す"""
        def loss_W(W): return self.loss(x, t)
        grads = {}
        grads['W1'] = numerical_gradient(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient(loss_W, self.params['b2'])
        return grads


if __name__ == "__main__":
    net = TwoLayoutNet(input_size=784, hidden_size=100, output_size=10)
    x = np.random.rand(100, 784)
    t = np.random.rand(100, 10)
    rands = net.numerical_gradient(x, t)
    print(rands['W1'].shape)
    print(rands['b1'].shape)
    print(rands['W2'].shape)
    print(rands['b2'].shape)
