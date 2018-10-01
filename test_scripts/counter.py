import collections
from collections import Counter
import numpy as np

words = [1, 2, 3, 1]

c = Counter (words)
print (c.most_common())
print (c[1])

print (type(c[2]))

b = [np.int32(item) for item in words]

print (b)
print (type(b[1]))