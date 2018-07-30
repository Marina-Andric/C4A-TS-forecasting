import pandas as pd
import numpy as np
import psycopg2
from sklearn.metrics import mean_absolute_error

def get_gef_values(month):
    conn = psycopg2.connect(host = "localhost", database = "city4age", user = "postgres", password = "postgres")
    cur = conn.cursor()

    sql = (
        '''
        with q1 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id, pilot_code
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label = '{0}' and data_type = 'p' and pilot_code = 'bhx'
        ), 
        q2 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label = '{0}' and data_type = 'c' and pilot_code = 'bhx' 
        )
        select q1.gef_value as predicted, q2.gef_value as expected, q1.gef_type_id, q1.user_in_role_id, q1.pilot_code
        from q1 join q2 on q1.interval_start_label = q2.interval_start_label and q1.gef_type_id = q2.gef_type_id
        and q1.user_in_role_id = q2.user_in_role_id
        '''.format(month)
    )
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df

def get_gef_values_overall(month):
    conn = psycopg2.connect(host = "localhost", database = "city4age", user = "postgres", password = "postgres")
    cur = conn.cursor()

    sql = (
        '''
        with q1 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id, pilot_code 
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label = '{0}' and data_type = 'p' and pilot_code = 'bhx' and detection_variable_name = 'overall'
        ), 
        q2 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id 
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label = '{0}' and data_type = 'c' and pilot_code = 'bhx' and detection_variable_name = 'overall'
        )
        select q1.gef_value as predicted, q2.gef_value as expected, q1.gef_type_id, q1.user_in_role_id, q1.pilot_code
        from q1 join q2 on q1.interval_start_label = q2.interval_start_label and q1.gef_type_id = q2.gef_type_id
        and q1.user_in_role_id = q2.user_in_role_id
        '''.format(month)
    )
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df


def get_gef_values3(month1, month2, month3):
    conn = psycopg2.connect(host = "localhost", database = "city4age", user = "postgres", password = "postgres")
    cur = conn.cursor()

    sql = (
        '''
        with q1 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id, pilot_code
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label in ('{0}', '{1}', '{2}') and data_type = 'p' and pilot_code = 'bhx'
        ), 
        q2 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label in ('{0}', '{1}', '{2}') and data_type = 'c' and pilot_code = 'bhx'
        )
        select q1.gef_value as predicted, q2.gef_value as expected, q1.gef_type_id, q1.user_in_role_id, q1.pilot_code
        from q1 join q2 on q1.interval_start_label = q2.interval_start_label and q1.gef_type_id = q2.gef_type_id
        and q1.user_in_role_id = q2.user_in_role_id
        '''.format(month1, month2, month3)
    )
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df

# march_predicted_expected = get_gef_values('2018/03')

# print(predicted_expected)

# march

# march_predicted = march_predicted_expected['predicted']
# march_expected = march_predicted_expected['expected']
#
# forecast_errors_march = [float(march_expected[i]) - float(march_predicted[i]) for i in range(len(march_expected))]
# # print (forecast_errors_march)
#
# print ('March')
#
# mean_error_march = np.mean(forecast_errors_march) # forecast bias
# print ('Mean error for March %f' % mean_error_march)
#
# mean_absolute_error = np.mean(np.abs(forecast_errors_march))
# print('Mean absolute error for March %f' % mean_absolute_error)
#
# mean_squared_error = np.mean([np.float_power(forecast_errors_march[i], 2) for i in range(len(forecast_errors_march))])
# print('Mean squared error for March %f' % mean_squared_error)
#
# root_mean_squared_error = np.sqrt(mean_squared_error)
# print('Root mean squared error %f' % root_mean_squared_error)

date = '2018/06'
predicted_expected = get_gef_values_overall(date)
# predicted_expected = get_gef_values(date)
# predicted_expected = get_gef_values3('2018/01', '2018/02', '2018/03')

predicted = predicted_expected['predicted']
expected = predicted_expected['expected']

print ('data points %d' %len(predicted))

forecast_errors = [float(expected[i]) - float(predicted[i]) for i in range(len(expected))]

mean_predicted = np.mean(predicted)
print ('mean predicted %f' % mean_predicted)

mean_expected = np.mean(expected)
print ('mean expected %f' % mean_expected)

mean_error = np.sum(forecast_errors) # forecast bias
print ('Mean error for %s is %f' % (date, mean_error))

mean_absolute_error = np.mean(np.abs(forecast_errors))
print('Mean absolute error for %s is %f' % (date,  mean_absolute_error))

mean_absolute_percentage_error = np.mean([np.abs(float(expected[i]) - float(predicted[i]))/float(expected[i]) for i in range(len(expected))])*100
print('Mean absolute percentage error for %s is %f' % (date, mean_absolute_percentage_error))

mean_squared_error = np.mean([np.float_power(forecast_errors[i], 2) for i in range(len(forecast_errors))])
print('Mean squared error for %s is %f' % (date, mean_squared_error))

root_mean_squared_error = np.sqrt(mean_squared_error)
print('Root mean squared error %f' % root_mean_squared_error)

# mean absolute deviation
# mean_absolute_deviation =

# for overall


