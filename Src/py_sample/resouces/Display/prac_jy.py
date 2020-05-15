import numpy as np
import matplotlib.pyplot as plt
# num：桁数
x = np.arange(0,8,0.1)         # 0から3まで0.1刻みで表示
exp_X = np.exp(x)
sum_exp_X = np.sum(exp_X)
y = exp_X / sum_exp_X         # ソフトマックス関数

plt.plot(x,y)
plt.show()


