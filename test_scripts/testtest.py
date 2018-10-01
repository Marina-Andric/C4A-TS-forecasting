import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler

dict = {'column1' : [1, 2, 3], 'column2' : [4, 5, 6]}
df = pd.DataFrame(dict)

# print (df)
# case1 = df.iloc[:, 1:]
# case3 = df['column2']
# # print (case1.dtype)
# # case2 = df.iloc[:, 1:]
# # print (case2.dtype)
# print ('case1\n', case1)
# print ('case3\n', case3)

# data = [[1, 2, 3], [4, 5, 6], [7, 18, 9]]
#
# print (data[0])
# sc = StandardScaler()
# transformed_data = sc.fit_transform(data)
#
# print (transformed_data)

vals = [False, False, False]

import numpy as np

print (np.unique((vals)))