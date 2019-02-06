import matplotlib.pyplot as plot

# 最急降下法
# この関数がもっとも小さくなる x を求めてみる
def func(x: float) -> float:
    """計算対象の関数

    Arguments:
        x {float} -- 引数

    Returns:
        float -- 計算結果
    """

    return 2 * (x ** 2) + 2 * x + 1


def loss(f: func, x: float, t: float) -> float:
    """損失関数

    Arguments:
        f {func} -- 値を求める関数
        x {float} -- 確認する x 値
        t {float} -- 正しい値

    Returns:
        float -- 誤差値
    """
    y = f(x)
    return t - y


def numerical_gradient(f: func, x_value: float):
    """関数簡易微分

    Arguments:
        f   {func} -- 微分したい関数
        x_value {float} -- 微分する x 値

    Returns:
        float -- 微分して得た傾斜
    """
    h = 1e-4
    grad = 0.0

    x1 = x_value + h
    x2 = x_value - h

    fhx1 = f(x1)
    fhx2 = f(x2)

    grad = (fhx1 - fhx2) / 2*h
    return grad


loop = 800
lern = 1000000.0
current_x = 3.5
log = []

# 微分するのは誤差関数
loss_func = lambda x: loss(func, x, 0.0)


for n in range(loop):
    # 微分して
    gradient = numerical_gradient(loss_func, current_x)
    # 誤差を元にあるべき x に近づける
    current_x += gradient * lern
    log.append(current_x)


x = [x / 10.0 for x in range(-50, 50, 1)]
y = [func(v) for v in x]

log_y = [func(v) for v in log]

# 通常関数は青
plot.plot(x, y, c='blue')
# 微分による x 座標の移動は点で
plot.scatter(log, log_y, c='red')

plot.show()

