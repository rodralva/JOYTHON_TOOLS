
from iminuit import cost
from iminuit import Minuit
from numba_stats import norm, t
import numpy as np
from matplotlib import pyplot as plt
rng = np.random.default_rng(1)

# def model(x, a, b):
#     return a + b * x

# truth = (1., 2.)
# x = np.linspace(0, 1)
# ym = model(x, *truth)
# ye = 0.1
# y = rng.normal(ym, ye)

# c = cost.LeastSquares(x, y, ye, model)

# m = Minuit(c, *truth)
# m.interactive()

plt.plot(0,0)
plt.show()
