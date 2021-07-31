import numpy as np
import matplotlib.pylab as plt


def step_func(x):
    return np.array(x > 0, dtype=np.int)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    return np.maximum(0, x)


def identity_function(x):
    return x


def mean_squad_error(y: np.array, t: np.array) -> float:
    return 0.5 * np.sum((y-t)**2)


def identity_function(x):
    return x


def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T

    x = x - np.max(x)  # for overflow
    return np.exp(x) / np.sum(np.exp(x))


def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)

    # ラベルデータの時の分岐
    if t.size == y.size:
        t = t.argmax(axis=1)

    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


def softmax_loss(X, t):
    y = softmax(X)
    return cross_entropy_error(y, t)


if __name__ == "__main__":
   x = np.arange(-5.0, 5.0, 0.1)
   y = relu(x)
   plt.plot(x, y)
   plt.ylim(-0.1, 1.1)
   plt.show()
