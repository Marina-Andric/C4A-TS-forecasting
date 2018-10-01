import psycopg2
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import minmax_scale

def get_data(userId):
    conn = psycopg2.connect(host='localhost', database = 'city4age', user = 'city4age_dba', password = 'city4age_dba')
    cur = conn.cursor()
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
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df


def pivot_data(df):
    for index, row in df.iterrows():
        row['measure_value'] = float(row['measure_value'])
        row['normalised'] = float(row['normalised'])
        row['interval_start'] = pd.datetime.strftime(row['interval_start'], "%Y-%m-%d")
    pivot_df = df.pivot_table(columns = 'detection_variable_name', values = 'measure_value', index='interval_start', aggfunc='max')
    pivot_df = pivot_df.reset_index()
    pivot_df.index.name = None
    # print (pivot_df)
    return pivot_df


def find_correlated_activities_foractivity(df, activity):
    corr_matrix = df.corr(method = 'spearman')
    corr_activities = corr_matrix[corr_matrix[activity]>0.3][activity].index.tolist()
    return df[corr_activities]


# remove anomalous points - make train dataset
def prepare_dataset(df):
    df = df.dropna(axis=0, how='any')
    # df_noanomalies = df[df['home_time']==86400 and df['walk_distance_outdoor_slow_percentage'] == 100.0]
    df_noanomolies = df[df['physicalactivity_calories'] != 0]
    # df_noanomolies.dropna(axis=0) # drops rows with missing values
    df = df.reset_index(drop=True)
    return df


def extract_features_all(df):
    df = pd.DataFrame(df.to_records())
    df['interval_start'] = [pd.to_datetime(item) for item in df['interval_start']]
    df.columns = ['interval_start', 'physicalactivity_calories', 'physicalactivity_intense_time', 'physicalactivity_moderate_time', 'physicalactivity_soft_time', 'sleep_awake_time', 'sleep_deep_time', 'sleep_light_time', 'sleep_tosleep_time', 'sleep_wakeup_num', 'walk_distance', 'walk_steps']
    features = df[['interval_start', 'physicalactivity_calories', 'walk_distance']]
    return features


def normalize_features(data):
    sc = StandardScaler()
    for activity in list(data.columns)[1:]:
        sc = sc.fit(data[activity].reshape(-1, 1))
        data[activity] = sc.transform(data[activity].reshape(-1, 1))
    return data

# min_max scaling to [0, 1]
def scaling_features_minmax(data):
    scaled_data = minmax_scale.fit_tranform()
