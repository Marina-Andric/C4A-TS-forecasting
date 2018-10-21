import pandas as pd
import numpy as np

df = pd.DataFrame({'col1': [1, 1, 2, 3], 'col2': [4, 4, 5, 6], 'col3': [7, 10, 8, 9]})

# pivoted_df = pd.pivot_table(df, index = ['col1', 'col2'], values  = 'col3', aggfunc={"lam1": lambda x: np.percentile(x, 50)}).reset_index()
# print (pivoted_df)

def lam1(x):
    return np.percentile(x, 50)

def lam2(x):
    return np.percentile(x, 75)

pivoted_df = df.pivot_table(index = ['col1', 'col2'], values  = 'col3',
                            aggfunc=[lam1, lam2]).reset_index()

f1 = lambda x: np.percentile(x, 50)
f2 = lambda x: np.percentile(x, 75)

pivoted_df = (df.groupby(['col1', 'col2'])['col3']
                .agg([('lam1', f1), ('lam2', f2)])
                .reset_index())

print (pivoted_df)