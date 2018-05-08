import pandas as pd
import numpy as np
import psycopg2
from matplotlib import pyplot as plt
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA

def get_data(userId, dvId):
    conn = psycopg2.connect(host = 'localhost', database = 'city4age', user = 'postgres', password = 'postgres')
    cur = conn.cursor()

    sql = (
        '''
        select gef_value, interval_start_label
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values
        where user_in_role_id = {0} and gef_type_id = {1} and (data_type = 'c' or data_type = 'i')
        order by interval_start_label
        '''.format(userId, dvId)
    )

    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df

def plot_time_series(data, title = 'some title'):
    plt.figure(figsize=(10, 4))
    plt.plot(data['interval_start_label'], data['gef_value'])
    plt.title(title)
    plt.grid(True)
    plt.xticks(rotation = 80)
    plt.show()

def plot_autocorrelation(data_series):
    autocorrelation_plot(data_series)
    plt.show()

def plot_residuals(model):
    residuals = pd.DataFrame(model.resid)
    residuals.plot()
    residuals.plot(kind = 'kde')
    # print("Residuals: " % residuals.describe())
    plt.show()


data = get_data(109, 501)
# plot_time_series(data, title = 'userId = 109, dvId = 501 (Overall), pilot = bhx')

for i in range(data.__len__()):
    data['interval_start_label'][i] = pd.datetime.strptime(data['interval_start_label'][i], '%Y/%m')
    data['gef_value'][i] = float(data['gef_value'][i])

data_series = pd.Series(data['gef_value'])
# plot_autocorrelation(data_series)

# comparison of arima models

# autoregressive models
model_410 = ARIMA(data['gef_value'].values, order=(4, 1, 0))
model_410_fit = model_410.fit(disp=0)

predicted_values = model_410_fit.predict(start=16, end=18)
print(predicted_values)

print (model_410_fit.aic)
print(model_410_fit.bic)
# print (model_410_fit.resid)
# plot_residuals(model_410_fit)

# random walk
model_rw = ARIMA(data['gef_value'].values, order=(0, 1, 0))
model_rw_fit = model_rw.fit(disp=0)

# plot_residuals(model_rw_fit)
print(model_rw_fit.aic)
print(model_rw_fit.bic)

# random walk with drift
model_rw_drift = ARIMA(data['gef_value'].values, order=(0, 1, 0))
model_rw_drift_fit = model_rw.fit(disp=0, trend='c')

# plot_residuals(model_rw_fit)
print('RW with drift aic: ' % model_rw_drift_fit.aic)
print('RW with drift bic: ' % model_rw_drift_fit.bic)

# linear exponential smoothing
# model_linexpsmooth = ARIMA(data['gef_values'].values, order=())

