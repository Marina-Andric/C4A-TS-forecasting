import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
a = [list([i, j]) for i in range(4) for j in range(3)]
print (a[0:11])

b = [2118.0,
2896.0,
3776.0,
4293.0,
7081.0,
3171.0,
5288.0,
5060.0,
4827.0,
3736.0,
5446.0,
4553.0,
3059.0,
6098.0,
5214.0,
2842.0,
3310.0,
7775.0,
3091.0,
5151.0,
6624.0,
8748.0,
7183.0,
9091.0,
7163.0,
8006.0,
6467.0,
10125.0,
9172.0,
9536.0
]
reversed_b = b[::-1]
print (reversed_b)
df = pd.DataFrame(data = reversed_b)
print (df)
fig, ax = plt.subplots(figsize = (6, 4))
plt.xticks(np.arange(0, 31))
for label in ax.get_xticklabels()[::2]:
    label.set_visible(False)
ax.grid(True)
ax.plot(df)
plt.show()
