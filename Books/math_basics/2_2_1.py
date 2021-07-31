import random
import matplotlib.pyplot as plot

random.seed(65535)

def actual(x):
    """目指すべき線"""
    return 0.6 * x + 4


actual_data = [(x, actual(x)) for x in range(-100, 100)]
data_set = [(x, actual(x) + random.randint(-5, 5)) for x in range(-100, 100)]

# 目標 data_set から、actual のパラメータを類推する
def func(x, weight):
    return weight[0] * x + weight[1]


def loss(func, data, actual, weight):
    calc = func(data, weight)
    return (actual - calc)**2


def numerical_gradient(f, weight):
    """偏微分式にアップデート"""
    h = 1e-4
    grad = []

    for i in range(0, len(weight)):
        cpy1 = weight[:]
        cpy2 = weight[:]
        cpy1[i] = cpy1[i] + h
        cpy2[i] = cpy2[i] - h
        fhx1 = f(cpy1)
        fhx2 = f(cpy2)
        grad.append((fhx1 - fhx2) / (2 * h))
    return grad


lern = 0.000002
weight = [-2, 3]  # 最初の重みは適当
for n in range(5000):
    def error(weight):
        all_err = 0.0
        for data in data_set:
            x, actual_y = data
            all_err += (actual_y - func(x, weight))**2
        return all_err / 2.0
    grads = numerical_gradient(error, weight)
    weight = [weight[0] - grads[0] * lern, weight[1] - grads[1] * lern]
    print(weight)

    #for data in data_set:
    #    x, y = data
    #    loss_func = lambda w: loss(func, x, y, w)
    #    grads = numerical_gradient(loss_func, weight)
    #    weight = [weight[0] - grads[0] * lern, weight[1] - grads[1] * lern]


def pline(data, color):
    x = [x for x, y in data]
    y = [y for x, y in data]
    plot.plot(x, y, c=color)


def scatter(data):
    x = [x for x, y in data]
    y = [y for x, y in data]
    plot.scatter(x, y, c='green')


lerning = [(x, func(x, weight)) for x in range(-100, 100)]
yellows = [(x, func(x, [-2, -3])) for x in range(-100, 100)]

pline(actual_data, 'blue')
pline(lerning, 'red')
#pline(yellows, 'yellow')
scatter(data_set)

plot.show()
