import pandas as pd
import numpy as np

data = np.array([['', 'col1', 'col2'],
                ['row1', 1, 2],
                ['row2', 3, 4]])
# print (data[1:,0])
df = pd.DataFrame(data=data[1:,1:].astype(int), index=data[1:,0],columns=data[0,1:])
print(df)

filters=np.array([['', 'col1', 'col2', 'col3'],
                 ['row1', 1, 1, 'a'],
                 ['row2', 1, 2, 'a'],
                 ['row3', 2, 2, 'a'],
                  ['row4', 2, 4, 'a']])
dff = pd.DataFrame(data=filters[1:,1:], index=filters[1:,0],columns=filters[0,1:])
dff[['col1', 'col2']].apply(pd.to_numeric, errors='coerce')
print (dff)

rdf = df.join(dff, how='left', lsuffix='_1', rsuffix='_2')
print (rdf)
# ndf=ndf[ndf.col1.isin(df.col1)]
# print(df1)

# df1 = df[df['col2'].isin(ndf[ndf['col1']==df['col1']]['col2'])]
# print (df1)
# print(dff.groupby(['col1'])['col2'])
# df1 = df[df['col1'].isin([1,2]) & df['col2'].isin(dff[df['col1']]['col2'])]
# df1 = df[df['col1'] in [1,2]]
# print(df1)