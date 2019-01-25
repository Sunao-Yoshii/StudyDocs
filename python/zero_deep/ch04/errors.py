# coding: utf-8

import numpy as np


def mean_squad_error(y: np.array, t: np.array) -> float:
    return 0.5 * np.sum((y-t)**2)


def cross_entropy_error(y: np.array, t: np.array) -> float:
    delta = 1e-7
    return -np.sum(t * np.log(y + delta))


if __name__ == "__main__":
    t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    y = [0.1, 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
    print(mean_squad_error(np.array(y), np.array(t)))
    print(cross_entropy_error(np.array(y), np.array(t)))
