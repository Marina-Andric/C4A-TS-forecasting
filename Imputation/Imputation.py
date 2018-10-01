import pandas as pd
import numpy as np
import psycopg2
import warnings

warnings.filterwarnings("ignore")  # suppress warnings for deprecated calls
from matplotlib import pyplot as plt


def get_data():
    conn = psycopg2.connect(host="localhost", database="city4age", user="postgres", password="postgres")
    curr = conn.cursor()

    sql = ('''
             with t1 as (
            select avg(gef_value) as avg_imputed, "count"(*) as count1, cdv.detection_variable_name, data_type
            from city4age_sr.vw_gef_calculated_interpolated_predicted_values view1 inner join city4age_sr.cd_detection_variable cdv
            on view1.gef_type_id = cdv."id"
            where data_type = 'i' 
            GROUP BY cdv.detection_variable_name, data_type
            ), t2 as (
            select avg(gef_value) as avg_computed, "count"(*) as count2, cdv.detection_variable_name, data_type
            from city4age_sr.vw_gef_calculated_interpolated_predicted_values view1 inner join city4age_sr.cd_detection_variable cdv
            on view1.gef_type_id = cdv."id"
            where data_type = 'c'
            GROUP BY cdv.detection_variable_name, data_type
            ), t3 as ( 
            select avg(gef_value) as avg_computed_imputed, "count"(*) as count3, cdv.detection_variable_name
            from city4age_sr.vw_gef_calculated_interpolated_predicted_values view1 inner join city4age_sr.cd_detection_variable cdv
            on view1.gef_type_id = cdv."id"
            where data_type in ('c', 'i')
            GROUP BY cdv.detection_variable_name
            ), stats as (
            select round(t1.avg_imputed, 2) as avg_imputed, round(t2.avg_computed, 2) as avg_computed, count1::float/(count1 + count2)*100 as percentage_imputed, t1.detection_variable_name, round(t3.avg_computed_imputed, 2) as avg_computed_imputed
            from t2 join t3 
            on t2.detection_variable_name = t3.detection_variable_name 
            right join t1 
            on t1.detection_variable_name = t3.detection_variable_name
            )
-- select * from t3
             select avg_imputed, avg_computed, avg_computed_imputed, percentage_imputed, detection_variable_name
             from stats
            order by detection_variable_name    ''')
    curr.execute(sql)
    df_stats = pd.DataFrame(curr.fetchall())
    df_stats.columns = [iter[0] for iter in curr.description]
    return df_stats


data = get_data()
print (data)
# data.to_pickle('neki_fajl.ppp')

bar_width = 0.25
opacity = 0.5

# plot missing data and the pattern
plt.figure(figsize=(9, 3.5))
perc = data['percentage_imputed']
var_xticks = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI',
              'XVII', 'XVIII']
var_label = data['detection_variable_name'].values

labels = pd.DataFrame()
labels[' '] = var_xticks
labels['name'] = data['detection_variable_name']
labels.set_index(' ', inplace=True)
labels.columns = [" "]

# print (labels)
# var_label[:, 0] = var_xticks


xaxis = np.arange(len(perc)) * 1 / 2
plt.bar(xaxis, perc, bar_width, alpha=opacity, label=labels, align='center')
plt.ylabel("% missing values")
# plt.xlabel("variable name")
plt.xticks(xaxis, var_xticks)
plt.legend(loc='best', bbox_to_anchor=(1.5, 1.1))
ycoords = [2, 4, 6, 8, 10, 12, 14, 16]
for y in ycoords:
    plt.axhline(y, alpha=0.25, color='grey')
plt.tight_layout()
plt.show()

# data to plot
avg_computed = data['avg_computed']
avg_computed_imputed = data['avg_computed_imputed']
avg_imputed = data['avg_imputed']
# print (avg_imputed)
data_size = len(avg_computed)

# create plot
plt.figure(figsize=(9, 3.5))
index = np.arange(data_size)
bar_width = 0.25

rects1 = plt.bar(index, avg_computed, bar_width,
                 alpha=opacity,
                 #                  color='b',
                 label='mean computed values', align='center')

rects2 = plt.bar(index + bar_width, avg_computed_imputed, bar_width,
                 alpha=opacity,
                 color='g',
                 label='mean computed + imputed values', align='center')

rects3 = plt.bar(index + 2 * bar_width, avg_imputed, bar_width,
                 alpha=opacity,
                 color='r',
                 label='mean imputed values', align='center')

# plt.xlabel('avg values')
plt.ylabel('Scores')
# plt.title('Scores by person')
plt.xticks(index + bar_width, var_xticks)
plt.legend(loc='best', bbox_to_anchor=(1.5, 1.1))
ycoords = [0.5, 1, 1.5, 2.0, 2.5, 3, 3.5]
for y in ycoords:
    plt.axhline(y, alpha=0.25, color='grey')

plt.tight_layout()
plt.show()
