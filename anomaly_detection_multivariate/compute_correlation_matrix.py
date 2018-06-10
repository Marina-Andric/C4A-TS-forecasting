import pandas as pd
import psycopg2
import csv
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from hmm_multi import learn_hmm_multi
from multivariate_plotting import create_multi_variate_plot
import warnings
warnings.filterwarnings("ignore")

def get_data(userId):
    conn = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
    curr = conn.cursor()
    sql = ("""
            WITH q0 AS (
            SELECT
            uir.pilot_code, 
            vmv.user_in_role_id,
            vmv.measure_value,
            vmv.time_interval_id,
            vmv.measure_type_id
            FROM
            city4age_sr.user_in_role AS uir 
            JOIN city4age_sr.variation_measure_value AS vmv ON (uir.user_in_system_id = vmv.user_in_role_id)
            WHERE vmv.user_in_role_id = {0}
            ),
            q1 AS (
            SELECT
            q0.pilot_code,
            q0.user_in_role_id,
            dv.detection_variable_type,
            dv.detection_variable_name,
            q0.measure_value,
            q0.time_interval_id
            FROM
            city4age_sr.cd_detection_variable as dv
            JOIN q0 ON (q0.measure_type_id = dv.id)
            ORDER BY
            dv.detection_variable_name
            ),
            minmax AS (
            SELECT 
            q1.detection_variable_name,
            MIN(q1.measure_value) as min_val,
            MAX(q1.measure_value) as max_val
            FROM
            q1
            GROUP BY
            q1.detection_variable_name
            ),
            q2 AS (
            SELECT
            q1.*,
            ti.interval_start
            FROM
            q1 JOIN city4age_sr.time_interval AS ti ON (q1.time_interval_id = ti.id)
            ),
            q3 AS (
            SELECT
            q2.*,
            minmax.max_val,
            minmax.min_val 
            FROM 
            q2 JOIN minmax ON (q2.detection_variable_name = minmax.detection_variable_name)
            ),
            res AS (
            SELECT
            q3.pilot_code,
            q3.user_in_role_id,
            q3.detection_variable_type,
            q3.detection_variable_name,
            q3.interval_start,
            q3.measure_value,
            (CASE WHEN (q3.max_val - q3.min_val) = 0 THEN 0
            ELSE (q3.measure_value - q3.min_val)/(q3.max_val - q3.min_val)
            END) as Normalised
            FROM
            q3
            )
            SELECT detection_variable_name, interval_start, measure_value, normalised
            from res
            order by interval_start
           """.format(userId))
    curr.execute(sql)
    # with open("out.csv", "w") as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     csv_writer.writerow([i[0] for i in curr.description])  # write headers
    #     csv_writer.writerows(curr)
    # data = pd.read_csv("out.csv")
    data_raw = curr.fetchall()
    df = pd.DataFrame(data_raw)
    df.columns = [iter[0] for iter in curr.description]
    curr.close()
    conn.close()
    return df

def corr_visualization(df):
    corr = df.corr(method = 'spearman')
    dim = df.__len__()
    # print ("correlation matrix", corr)
    mask = np.zeros((11, 11)) # hardcoded
    mask[np.triu_indices_from(mask, k=1)] = True
    fig, ax = plt.subplots(figsize = (10, 8))
    sns.heatmap(corr, cmap=sns.diverging_palette(220, 10, as_cmap=True), square=True, ax=ax, vmin = -1, vmax = 1, fmt = ".2f", annot=True, mask=mask)
    plt.show()

def pivot_data(df):
    for i in range(df.__len__()):
        df['measure_value'][i] = float(df['measure_value'][i])
        df['normalised'][i] = float(df['normalised'][i])
        df['interval_start'][i] = pd.datetime.strftime(df['interval_start'][i], "%Y-%m-%d")
    df = df.pivot_table(values=['normalised'], index=['interval_start'], columns='detection_variable_name', aggfunc='max')
    # print (df)
    # df.to_csv("res.csv", sep='\t')
    return df

# select correlated features
def extract_features_normal(df):
    df = pd.DataFrame(df.to_records())
    df['interval_start'] = [pd.to_datetime(item) for item in df['interval_start']]
    df.columns = ['interval_start', 'physicalactivity_calories', 'physicalactivity_intense_time', 'physicalactivity_moderate_time', 'physicalactivity_soft_time', 'sleep_awake_time', 'sleep_deep_time', 'sleep_light_time', 'sleep_tosleep_time', 'sleep_wakeup_num', 'walk_distance', 'walk_steps']
    features = df[['interval_start', 'physicalactivity_calories', 'walk_distance']]
    # features = features[features['physicalactivity_calories'] != 0] # exclude anomalies
    # features = features[features['walk_distance'] != 0]  # exclude anomalies
    return features

def extract_features_all(df):
    df = pd.DataFrame(df.to_records())
    df['interval_start'] = [pd.to_datetime(item) for item in df['interval_start']]
    df.columns = ['interval_start', 'physicalactivity_calories', 'physicalactivity_intense_time', 'physicalactivity_moderate_time', 'physicalactivity_soft_time', 'sleep_awake_time', 'sleep_deep_time', 'sleep_light_time', 'sleep_tosleep_time', 'sleep_wakeup_num', 'walk_distance', 'walk_steps']
    features = df[['interval_start', 'physicalactivity_calories', 'walk_distance']]
    return features

def fit_hmm_normal(data):
    bic, model = learn_hmm_multi(data.iloc[:,1:], 8)
    clusters = model.predict(data.iloc[:,1:])

    data['cluster'] = clusters

    activities = ['physicalactivity_calories', 'walk_distance']
    create_multi_variate_plot(data, activities)
    return model

def multivariate_hmm_all(model,data):
    # print (data.shape)
    clusters = model.predict(data.iloc[:,1:])
    probabs = model.predict_proba(data.iloc[:,1:])
    print (probabs.shape)
    # print (probabs)
    probabs_np = np.array(probabs)
    max_probabs = np.amax(probabs_np, 1)
    data['cluster'] = clusters
    data['max_probabs'] = max_probabs
    return data

data = get_data(116)
# print (data)
df = pivot_data(data)
# corr_visualization(df)
prepared_data1 = extract_features_normal(df)
model = fit_hmm_normal(prepared_data1)

prepared_data2 = extract_features_all(df)
result = multivariate_hmm_all(model, prepared_data2)
print(result)
print(result[result['walk_distance']==0])
# print(result[result['max_probabs'] < 0.7])
# print (probabs_all)
# prepared_data['probabs'] = probabs_all

