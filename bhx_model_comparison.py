import pandas as pd
import numpy as np
import psycopg2
import math
import datetime
from matplotlib import pyplot as plt
from matplotlib import dates
# from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
import warnings

warnings.filterwarnings("ignore")

def get_data(userId, dvId):
    conn = psycopg2.connect(host='localhost', database='city4age', user='postgres', password='postgres')
    cur = conn.cursor()

    sql = (
        '''
        select gef_value, interval_start_label, detection_variable_name
        from city4age_sr.vw_gef_calculated_interpolated_predicted_values 
        where user_in_role_id = {0} and gef_type_id = {1} and (data_type = 'c' or data_type = 'i')
        order by interval_start_label
        '''.format(userId, dvId)
    )

    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [iter[0] for iter in cur.description]
    return df

def plot_time_series(data, title='some title'):
    plt.figure(figsize=(10, 4))
    plt.plot(data['interval_start_label'], data['gef_value'])
    plt.title(title)
    plt.grid(True)
    plt.xticks(rotation=80)
    plt.show()


def plot_autocorrelation(data_series):
    autocorrelation_plot(data_series)
    plt.show()


def plot_residuals(model_fit):
    residuals = pd.DataFrame(model_fit.resid)
    residuals.plot()
    residuals.plot(kind='kde')
    # print("Residuals: " % residuals.describe())
    plt.show()


def find_optimal_model(train_data):
    aic = 1000  # some initial value
    for p in range(5):
        for d in range(2):
            for q in range(5):
                for drift in ('nc', 'c'):
                    try:
                        order = (p, d, q)
                        model_fit = ARIMA(train_data, order=order).fit(disp=False, trend=drift, transparams=True)
                        # print('%s, order = (%d, %d, %d), aic = %f, bic = %f' % (drift, p, d, q, model_fit.aic, model_fit.bic))
                        if not (math.isnan(model_fit.aic)) and model_fit.aic < aic:
                            aic = model_fit.aic
                            model_optimal = model_fit
                            order_optimal = order
                    except:
                        pass
    return aic, order_optimal, model_optimal

def generate_date(sourcedate, steps=3):
    result = []
    for i in range(0, steps):
        month = sourcedate.month + i
        year = sourcedate.year + month // 12
        month = (month + 1) % 12
        result.append((datetime.date(year, month, 1)))
    return result

def plot_forecasts(data, forecasts, conf_int, userId):
    figure = plt.figure(figsize=(10, 4))
    plt.plot(data['interval_start_label'], data['gef_value'], label = 'actual')
    interval_forecasts = generate_date(data['interval_start_label'].values[-1])
    plt.plot(interval_forecasts, forecasts, color = 'red', label = 'forecast')
    plt.plot(interval_forecasts, [conf_int[0][0], conf_int[1][0], conf_int[2][0]],
             color='lightblue', label = '95.0% limits')
    plt.plot(interval_forecasts, [conf_int[0][1], conf_int[1][1], conf_int[2][1]],
             color='lightblue')
    plt.legend(loc = 'best')
    plt.title('userId = %d and factor name = %s' %(userId, factor_name))
    plt.grid(True)
    labels = [pd.datetime.strftime(item, "%Y/%m") for item in data['interval_start_label']]
    labels.extend([pd.datetime.strftime(item, "%Y/%m") for item in interval_forecasts])
    plt.xticks(labels, rotation=80)
    plt.yticks(np.arange(0, 5, step = 0.5))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    plt.show()
    # plt.savefig('forecastplot.png')

userId = 115
factorId = 501
data = get_data(userId, factorId)
factor_name=data['detection_variable_name'][0]

for i in range(data.__len__()):
    data['interval_start_label'][i] = pd.datetime.strptime(data['interval_start_label'][i], '%Y/%m')
    data['gef_value'][i] = float(data['gef_value'][i])

# plot_time_series(data, title = 'title')
# data_series = pd.Series(data['gef_value'])
# plot_autocorrelation(data_series)

# data = data.iloc[:-1, :]
train_data = data['gef_value'].values
print (train_data)
# test_data = data['gef_value']
# print('test data: ', test_data)

# aic, order_optimal, model_optimal = find_optimal_model(train_data)
# print('aic: %f, order=%s' % (aic, order_optimal))
# forecasts, stderr, conf_int = model_optimal.forecast(steps=3)
# plot_forecasts(data, forecasts, conf_int, userId)

# out-of-sample validation - estimation of errors

model_fit = ARIMA(train_data, order=(0, 0, 0)).fit(disp=False, trend='c', transparams=True)
forecasts, stderr, conf_int = model_fit.forecast(steps=3)
plot_forecasts(data, forecasts, conf_int, userId)

print('order = (%d, %d, %d), aic = %f, bic = %f' % (0, 0, 0, model_fit.aic, model_fit.bic))
