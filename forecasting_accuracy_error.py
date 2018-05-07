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
        where interval_start_label = '{0}' and data_type = 'p'
        ), 
        q2 as (
        select gef_value, gef_type_id, interval_start_label, user_in_role_id
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where interval_start_label = '{0}' and data_type = 'c'
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


march_predicted_expected = get_gef_values('2018/03')
april_predicted_expected = get_gef_values('2018/04')

# print(april_predicted_expected)

# march

march_predicted = march_predicted_expected['predicted']
march_expected = march_predicted_expected['expected']

forecast_errors_march = [float(march_expected[i]) - float(march_predicted[i]) for i in range(len(march_expected))]
# print (forecast_errors_march)

print ('March')

mean_error_march = np.mean(forecast_errors_march) # forecast bias
print ('Mean error for March %f' % mean_error_march)

mean_absolute_error = np.mean(np.abs(forecast_errors_march))
print('Mean absolute error for March %f' % mean_absolute_error)

mean_squared_error = np.mean([np.float_power(forecast_errors_march[i], 2) for i in range(len(forecast_errors_march))])
print('Mean squared error for March %f' % mean_squared_error)

root_mean_squared_error = np.sqrt(mean_squared_error)
print('Root mean squared error %f' % root_mean_squared_error)

# april

print ('April')

april_predicted = april_predicted_expected['predicted']
april_expected = april_predicted_expected['expected']


forecast_errors_april = [float(april_expected[i]) - float(april_predicted[i]) for i in range(len(april_expected))]

mean_error_april = np.mean(forecast_errors_april) # forecast bias
print ('Mean error for April %f' % mean_error_april)

mean_absolute_error = np.mean(np.abs(forecast_errors_april))
print('Mean absolute error for April %f' % mean_absolute_error)

mean_squared_error = np.mean([np.float_power(forecast_errors_april[i], 2) for i in range(len(forecast_errors_april))])
print('Mean squared error for April %f' % mean_squared_error)

root_mean_squared_error = np.sqrt(mean_squared_error)
print('Root mean squared error %f' % root_mean_squared_error)




