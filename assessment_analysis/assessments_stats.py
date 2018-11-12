import psycopg2
import pandas as pd
import numpy as np
import datetime
from tabulate import tabulate
from random import shuffle

# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go
# plotly.tools.set_credentials_file(username='marina08', api_key='1RyNwG5VQ6mfyaawvTEP')

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.size'] = 15.0

def get_data():
    conn = psycopg2.connect(host = 'localhost', port = '5432', dbname = 'city4age', user = 'city4age_dba', password = 'city4age_dba')
    sql = '''
    SELECT
        assessment. ID AS aid,
        dv.detection_variable_type,
        uir."id" AS userId,
        dv.detection_variable_name,
        assessment.assessment_comment,
        assessment.data_validity_status,
        assessment.risk_status,
        assessment.created
    FROM
        city4age_sr.assessment
    JOIN city4age_sr.assessed_gef_value_set AS agef ON assessment."id" = agef.assessment_id
    JOIN city4age_sr.geriatric_factor_value AS gef ON agef.gef_value_id = gef."id"
    JOIN city4age_sr.cd_detection_variable AS dv ON gef.gef_type_id = dv. ID
    JOIN city4age_sr.user_in_role AS uir ON gef.user_in_role_id = uir."id"
    -- WHERE
    --     author_id = 228
    ORDER BY
        created,
        detection_variable_type,
        detection_variable_name
    '''
    cur = conn.cursor()
    cur.execute(sql)
    df = pd.DataFrame(cur.fetchall())
    df.columns = [item[0] for item in cur.description]
    return df

def prepare_data(data):
    data['created'] = [datum.strftime('%Y-%m-%d') for datum in data['created']]
    data['created'] = [datetime.datetime.strptime(datum, '%Y-%m-%d') for datum in data['created']]
    return data

# pc risk statuses

def pie_risk_status(data):
    labels = np.unique(data['risk_status'])
    labels_chart = ['Risk alert' if status == 'A' else 'Risk warning' if status == 'W' else 'No Risk' for status in np.unique(data['risk_status'])]
    # print (data['risk_status'] == 'A')
    values = [np.sum(1 if data['risk_status'][i]==status else 0 for i in range(0, len(data)))/len(data)*100 for status in labels]
    # print (values)
    colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    plt.pie(values, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, labels = labels_chart)
    # plt.legend(patches, labels_chart, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def get_asse_month(prepared_data):
    asse_month = np.sum([1 if prepared_data['created'][i].month==4 else 0 for i in range(0, len(prepared_data))])
    print (asse_month)

def asse_to_excel(grouped_data):
    grouped_data = prepared_data.groupby(['userid', 'detection_variable_name']).size()
    # print (grouped_data)
    grouped_data = grouped_data.reset_index()
    print (tabulate(grouped_data, headers='keys', tablefmt='psql'))
    writer = pd.ExcelWriter('output.xlsx')
    grouped_data.to_excel(writer, 'Sheet1')
    writer.save()

def pie_factors(data):
    labels = np.unique(data['detection_variable_name'])
    # labels = ['quality_of_sleep' 'health-physical'
    #  'instrumental_activities_of_daliy_living' 'physical_activity'
    #  'basic_activities_of_daliy_living' 'motility' 'walking']

    # labels_chart = ['Risk alert' if status == 'A' else 'Risk warning' if status == 'W' else 'No Risk' for status in np.unique(data['risk_status'])]
    # print (data['risk_status'] == 'A')
    shuffle(labels) # shuffle in place. This is to avoid
    print (labels)
    values = [np.sum(1 if data['detection_variable_name'][i]==factor else 0 for i in range(0, len(data)))/len(data)*100 for factor in labels]
    # print (values)
    colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'violet', 'moccasin', 'gainsboro', 'lightblue']
    plt.pie(values, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, labels = labels)
    # plt.legend(patches, labels_chart, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    # plt.savefig('Images\\Assessments_stats\\assessment_pie.png')

data = get_data()
prepared_data = prepare_data(data)
# print (data)
# pie_factors(prepared_data)
# pie_risk_status(prepared_data)

get_asse_month(prepared_data)
# asse_to_excel(prepared_data)
# print (len(prepared_data))