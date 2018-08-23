import psycopg2
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import minmax_scale
import numpy as np

def get_data_multi(userId):
    conn = psycopg2.connect(host='localhost', database = 'city4age', user = 'city4age_dba', password = 'city4age_dba')
    cur = conn.cursor()
    sql = ("""           
            WITH q0 AS (
				SELECT
					vmv.id AS vmvId,
					dv.detection_variable_name,
					vmv.measure_type_id as dvid,
					vmv.measure_value,
					vmv.time_interval_id,
					vmv.measure_type_id,
					ti.interval_start
				FROM
					city4age_sr.variation_measure_value as vmv
				JOIN 
				    city4age_sr.time_interval AS ti ON (vmv.time_interval_id = ti.id)
				JOIN 
				    city4age_sr.cd_detection_variable as dv on (vmv.measure_type_id = dv.id)
				WHERE
					vmv.user_in_role_id = {0} and dv.id in (50, 47, 46, 73, 74, 78, 79, 75, 48, 96, 91)
			),
			 minmax AS (
				SELECT
					q0.dvid,
					MIN (q0.measure_value) AS min_val,
					MAX (q0.measure_value) AS max_val
				FROM
					q0
				GROUP BY
					q0.dvid
			),
                 q3 AS (
                    SELECT
                        q0.*,
                        minmax.max_val,
                        minmax.min_val
                    FROM
                        q0
                    JOIN minmax ON (
                        q0.dvid = minmax.dvid
                    )
                )
				SELECT
                    q3.*,
					(
						CASE
						WHEN (q3.max_val - q3.min_val) = 0 THEN
							0
						ELSE
							(
								(q3.measure_value - q3.min_val)
							) / (q3.max_val - q3.min_val)
						END
					) AS Normalised
				FROM
					q3
				ORDER BY
			    	q3.interval_start ASC
           """.format(userId))
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df


def prepare_and_pivot_data(df):
    for index, row in df.iterrows():
        df.set_value(index, 'measure_value', float(row['measure_value']))
        df.set_value(index, 'normalised', float(row['normalised']))
        df.set_value(index, 'interval_start',pd.datetime.strftime(row['interval_start'], "%Y-%m-%d"))
    df = df[['detection_variable_name', 'interval_start', 'measure_value', 'normalised']]
    pivot_df = df.pivot_table(columns = ['detection_variable_name'], values = 'normalised', index='interval_start', aggfunc='max')
    pivot_df = pivot_df.reset_index()
    pivot_df.index.name = None
    return pivot_df


# remove anomalous points - make train dataset
def fill_missing_values(df):
    # df = df.dropna(axis=0, how='any')
    df.fillna(0, inplace = True) # substitute with mean values
    df = df.reset_index(drop=True)
    return df


def stack_dataset(data):
    # print (data)
    # data = data.set_index('interval_start').stack().reset_index(name = 'value').rename(columns = {'level_1' : 'walk_distance'})
    data = data.set_index(['interval_start', 'cluster']).stack().reset_index(name = 'normalised')
    # data = data[data['detection_variable_name']=='walk_distance']
    return data

def normalize_dataset(data):
    sc = StandardScaler()
    transformed_data = sc.fit_transform(data)
    return transformed_data