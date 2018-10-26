import pandas as pd
import numpy as np

idx = pd.date_range('09-01-2013', '09-30-2013')

data = np.array([['', 'col1', 'col2'],
                ['09-02-2013', 1, 2],
                ['09-03-2013', 3, 4]])
# print (data[1:,0])
df = pd.DataFrame(data=data[1:,1:].astype(int), index=data[1:,0], columns=data[0,1:])

print (df.values)

df.index = pd.DatetimeIndex(df.index)

df = df.reindex(idx, fill_value=0)
print (df)

s = pd.Series({'09-02-2013': 2,
               '09-03-2013': 10,
               '09-06-2013': 5,
               '09-07-2013': 1})
s.index = pd.DatetimeIndex(s.index)

# s = s.reindex(idx, fill_value=0)
# print(s)