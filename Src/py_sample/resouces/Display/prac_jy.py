import numpy as np
import matplotlib.pyplot as plt
import random
import time

weight = 10
num = 5

for i in range(100):

    a = np.arange(0,i+1,0.1)
    exp_a = np.exp(a)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    rn_int = int(random.choice(y)*10**num)
    if rn_int > 10**(num-1):
        rn_int = 10**(num-1)
    if rn_int == 0:
        rn_int = random.randint(1,10**(num-2))
    plt.plot(a,y)
    plt.show()
    rad_int = random.randint(1,10**(num-1))

    print(i+1)

    plt.close()
