# !/bin/python
import numpy as np


def __perceptron_base(np_arg, weight, bias):
    tmp = np.sum(np_arg * weight) + bias
    if tmp <= 0:
        return 0
    else:
        return 1


def AND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    return __perceptron_base(x, w, b)


def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    return __perceptron_base(x, w, b)


def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    return __perceptron_base(x, w, b)


def XOR(x1, x2):
    a1 = NAND(x1, x2)
    a2 = OR(x1, x2)
    return AND(a1, a2)

