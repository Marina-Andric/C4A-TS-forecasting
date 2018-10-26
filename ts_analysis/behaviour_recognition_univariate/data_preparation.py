import psycopg2
import pandas as pd
import datetime

# returns a list of activities for a given user
# def get_list_activities(userId):
#     conn = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
#     curr = conn.cursor()
#     sql = ('''
#
#         select distinct view1.detection_variable_name
#         from city4age_sr.vw_detection_variable_derivation_per_user_in_role as view1
#         where view1.user_in_role_id = {0}
#         and view1.detection_variable_type = 'mea'
#
#     '''.format(userId)
#            )
#     curr.execute(sql)
#     data = pd.DataFrame(curr.fetchall())
#     data.columns = [i[0] for i in curr.description]
#     curr.close()
#     conn.close()
#     activities = data.values[:, 0]
#     return activities.tolist()

def insert_missing_dates(data):
    data['interval_start']=[item.strftime("%Y-%m-%d") for item in data['interval_start']]
    data=pd.pivot_table(data, index=['interval_start', 'detection_variable_name'])
    # data.index=pd.DatetimeIndex(data['interval_start'])
    data.set_index(['interval_start'])
    # print (len(data['interval_start']))
    indx=pd.date_range(data['interval_start'].min(), data['interval_start'].max())
    # print (indx)
    # print (len(indx))
    data.reindex(indx, fill_value=-5)
    # print (data)
    return data


def prepare_data(data, activity_name):
    '''
    :param data: transaction data
    :param activity_name: name of activity
    :return: activity_data
    '''
    sleep_activities = ['sleep_light_time', 'sleep_awake_time', 'sleep_deep_time', 'sleep_tosleep_time', 'sleep_wakeup_num']
    activity_data = data[data['detection_variable_name'] == activity_name]
    # print (activity_name)
    prepared_activity_data = activity_data[['interval_start','measure_value']]

    if activity_name in sleep_activities:
        prepared_activity_data['interval_start'] = [item.strftime("%Y-%m-%d") for item in prepared_activity_data['interval_start']]
        # prepared_activity_data.index = pd.DatetimeIndex(activity_data['interval_end'])
        # indx=pd.date_range(activity_data['interval_end'].min(), activity_data['interval_end'].max())
        # prepared_activity_data=prepared_activity_data.reindex(indx, fill_value=-5)
    else:
        prepared_activity_data['interval_start'] = [item.strftime("%Y-%m-%d") for item in prepared_activity_data['interval_start']]
        # prepared_activity_data.index = pd.DatetimeIndex(activity_data['interval_start'])
        # indx=pd.date_range(activity_data['interval_start'].min(), activity_data['interval_start'].max())
        # prepared_activity_data=prepared_activity_data.reindex(indx, fill_value=-5)

    return prepared_activity_data


def get_data(userId):
    conn = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
    curr = conn.cursor()
    # data for walk distance (MEA)
    sql = ("""
              WITH q0 AS
             (
              SELECT
               uir.pilot_code      ,
               vmv.user_in_role_id ,
               vmv.measure_value   ,
               vmv.time_interval_id,
               vmv.measure_type_id
              FROM
               city4age_sr.user_in_role AS uir
               JOIN
                city4age_sr.variation_measure_value AS vmv
                ON
                 (
                  uir.user_in_system_id = vmv.user_in_role_id
                 )
              where
               vmv.user_in_role_id = {0}
             )
             ,
             q1 AS
             (
              SELECT
               q0.pilot_code             ,
               q0.user_in_role_id        ,
               dv.detection_variable_type,
               dv.detection_variable_name,
               q0.measure_value          ,
               q0.time_interval_id
              FROM
               city4age_sr.cd_detection_variable as dv
               JOIN
                q0
                ON
                 (
                  q0.measure_type_id = dv.id
                 )
              where
               dv."id" in
               (
                select
                 view1.detection_variable_id
                from
                 city4age_sr.vw_detection_variable_derivation_per_user_in_role as view1
                where
                 view1.user_in_role_id                   = {0}

                 and view1.detection_variable_type       = 'mea'
               )
              ORDER BY
               dv.detection_variable_name
             )
             ,
             minmax AS
             (
              SELECT
               q1.detection_variable_name      ,
               MIN(q1.measure_value) as min_val,
               MAX(q1.measure_value) as max_val
              FROM
               q1
              GROUP BY
               q1.detection_variable_name
             )
             ,
             q2 AS
             (
              SELECT
               q1.*             ,
               ti.interval_start,
               ti.interval_end
              FROM
               q1
               JOIN
                city4age_sr.time_interval AS ti
                ON
                 (
                  q1.time_interval_id = ti.id
                 )
             )
             ,
             q3 AS
             (
              SELECT
               q2.*          ,
               minmax.max_val,
               minmax.min_val
              FROM
               q2
               JOIN
                minmax
                ON
                 (
                  q2.detection_variable_name = minmax.detection_variable_name
                 )
             )
             ,
             res AS
             (
              SELECT
               q3.pilot_code             ,
               q3.user_in_role_id        ,
               q3.detection_variable_type,
               q3.detection_variable_name,
               q3.interval_start         ,
               q3.interval_end           ,
               q3.measure_value          ,
               (
                CASE
                 WHEN (
                   q3.max_val - q3.min_val
                  )
                  = 0
                  THEN 0
                  ELSE (q3.measure_value - q3.min_val)/(q3.max_val - q3.min_val)
                END
               )
               as Normalised
              FROM
               q3
             )
            SELECT *
            from
             res
            ORDER BY res.interval_start ASC
           """.format(userId))
    curr.execute(sql)
    data = pd.DataFrame(curr.fetchall())
    data.columns = [item[0] for item in curr.description]
    return data


