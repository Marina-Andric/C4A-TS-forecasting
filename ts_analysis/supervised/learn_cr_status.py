import pandas as pd
import psycopg2
import sql_query
import sql_query as queries
import numpy as np

def get_data():
    connection = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
    cur = connection.cursor()
    # try:
    #     cur.execute(queries.query0)
    #     connection.commit()
    # except psycopg2.ProgrammingError:
    #     pass
    cur.execute(queries.query1)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    print (df)
    return df

def prepare_data(data):
    data['val']=[float(data['val'][i]) for i in range(len(data['val']))]
    pivoted_data=pd.pivot_table(data, values='val', columns=['var_name'], index=['cr_id', 'day_m', 'trimester'])
    mask = [pivoted_data['home_time'].values[i] < 86400 for i in range(len(pivoted_data))]
    filtered_data=pivoted_data[mask]
    print (filtered_data)
    a=filtered_data.groupby(['cr_id','trimester'])['home_time'].count().reset_index(name='count')
    to_keep=a[a['count']>=10]
    print (to_keep)
    # nto_keep = to_keep.groupby(['col1']).agg(lambda x: list(x)).reset_index()
    # print (len(to_keep))
    filtered_data=filtered_data.reset_index()
    # filtered_data=filtered_data[filtered_data['cr_id'].isin(to_keep['cr_id']) & filtered_data['trimester'].isin(nto_keep['trimester'])]
    filtered_data=filtered_data.set_index(['cr_id', 'day_m', 'trimester'])
    return filtered_data

# needs to be sorted beforehand
def compute_stats(data):
    sumofvals=data.groupby(['cr_id', 'trimester']).agg(['sum', 'mean'])
    print(sumofvals)
    # pivoted_data_sum=pd.pivot_table(data, values='val', columns=['var_name'], index=['cr_id', 'trimester', 'status'], aggfunc=np.sum)
    # pivoted_data_avg=pd.pivot_table(data, values='val', columns=['var_name'], index=['cr_id', 'trimester', 'status'], aggfunc=np.mean)
    # pivoted_data_stddev=pd.pivot_table(data, values='val', columns=['var_name'], index=['cr_id', 'trimester', 'status'], aggfunc=np.std)
    # pivoted_data_median=pd.pivot_table(data, values='val', columns=['var_name'], index=['cr_id', 'trimester', 'status'], aggfunc=np.median)
    # pivoted_data_perc = pd.pivot_table(data, values='val', columns=['var_name'], index=['cr_id', 'trimester', 'status'], aggfunc=lambda x: np.percentile(x, q=75))
    return ""

data = get_data()
