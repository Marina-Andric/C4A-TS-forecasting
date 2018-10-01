import pandas as pd

df = pd.DataFrame({'col1': [0.1, 0.2, 0.3]})

df['col1'] = 1 - df['col1']

print (df)