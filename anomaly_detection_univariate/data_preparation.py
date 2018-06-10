import pandas as pd

# fetching data from the database
def get_data():
    import psycopg2
    import csv
    conn = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
    curr = conn.cursor()

    # data for walk distance (MEA)
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
            SELECT *
            from res
           """)
    curr.execute(sql)
    #     data_raw = curr.fetchall()
    with open("out.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in curr.description])  # write headers
        csv_writer.writerows(curr)
    curr.close()
    conn.close()
    data = pd.read_csv("out.csv")
        # data = pd.DataFrame(data_raw)
    return data


def get_data1():
    data = pd.read_csv("out.csv")
    #     data = pd.DataFrame(data_raw)
    return data


def prepare_data(data, user, activities):
    '''
    :param data: transaction data
    :param user: user_in_role_id in integer format
    :param activities: list of activity names
    :return:
    '''
    '''
    Takes pivoted data and transforms it in regular DataFrame. 
    Converts dates to date format (for plotting) 
    Sorts data based on dates in order to preserve temporal order
    !!!If used for Single-Variate clustering list have to be passed (for one activity)
    '''
    pivoted_data = select_pivot_users_activities(data, user, activities)
    pivoted_data = pivoted_data.reset_index()
    pivoted_data['interval_start'] = pd.to_datetime(pivoted_data['interval_start'])
    pivoted_data = pivoted_data.sort_values(['user_in_role_id', 'interval_start'])
    return pivoted_data


def prepare_data1(data, user, activities):
    #     pivoted_data = select_pivot_users_activities(data, user, activities)
    user_data = data[data['user_in_role_id'] == user]
    user_data['interval_start'] = pd.to_datetime(user_data['interval_start'])
    # user_data = user_data[(user_data['interval_end'] > '2017-6-1') & (user_data['interval_end'] < '2017-6-30')]
    user_data = user_data[user_data['detection_variable_name'].isin(activities)]
    pivoted_data = user_data.pivot_table(index=['user_in_role_id', 'interval_start'], columns='detection_variable_name',
                                         values='measure_value')
    pivoted_data = pivoted_data.reset_index()
    pivoted_data['interval_start'] = pd.to_datetime(pivoted_data['interval_start'])
    #     result_data = pivot_data['interval_end']
    pivoted_data = pivoted_data.sort_values(['user_in_role_id', 'interval_start'])
    return pivoted_data


def select_pivot_users_activities(data, user, activities):
    '''
    Pivots multivariate data - each activity becomes column
    Unnecessary step for single variate time series - maybe remove and adjust prepare data method
    '''
    user_data = data[data['user_in_role_id'] == user]
    user_data = user_data[user_data['detection_variable_name'].isin(activities)]
    pivot_data = user_data.pivot_table(index=['user_in_role_id', 'interval_start'], columns='detection_variable_name',
                                       values='measure_value')
    return pivot_data