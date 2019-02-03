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


def softmax(a):
    exp_a = np.exp(a)
    sum_exp_a = np.sum(exp_a)
    return exp_a / sum_exp_a


def mean_squad_error(y: np.array, t: np.array) -> float:
    return 0.5 * np.sum((y-t)**2)


def cross_entropy_error(y: np.array, t: np.array) -> float:
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


if __name__ == "__main__":
   x = np.arange(-5.0, 5.0, 0.1)
   y = relu(x)
   plt.plot(x, y)
   plt.ylim(-0.1, 1.1)
   plt.show()
