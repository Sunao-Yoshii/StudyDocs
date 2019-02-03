import numpy as np


def numerical_diff(f, x: np.array):
    h = 1e-4  # 0.0001
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_gradient(f, x: np.array):
    h = 1e-4
    grad = np.zeros_like(x)  # x と同一形状の配列を生成
    for idx in range(x.size):
        tmp_val = x[idx]
        # f(x+h) の計算
        x[idx] = tmp_val + h
        fxh1 = f(x)

        # f(x-h) の計算
        x[idx] = tmp_val - h
        fxh2 = f(x)

        grad[idx] = (fxh1 - fxh2) / (2 * h)
        x[idx] = tmp_val  # 値を元に戻す
    return grad


def gradient_discendant(f, init_x: np.array, lr: float = 0.01, step_num: int = 100):
    x = init_x
    for i in range(step_num):
        grad = numerical_gradient(f, x)
        x -= lr * grad
    return x

