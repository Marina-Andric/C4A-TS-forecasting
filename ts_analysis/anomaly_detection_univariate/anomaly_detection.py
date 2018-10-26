import pandas as pd
import numpy as np
import datetime
import json
from matplotlib import cm, pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import importlib

from hmm_clustering import optimize_number_of_clusters
from visualization import create_single_variate_plot, create_oneSeries_single_variate_plot, plot_time_series
from  data_preparation import get_data, get_data1, prepare_data, prepare_data1

# for reproducibility
np.random.seed(0)

def form_cluster_values(mask, values):
    result = values[:]
    for i in range(0, len(mask)):
        if mask[i] == False:
            result[i] = "null"
    return result

def hmm_to_dict_single_variate(data, user, activity, cov_type):
    dict = {}
    prep_data = prepare_data(data,user,[activity])
    value, model = optimize_number_of_clusters(prep_data.iloc[: ,2:], list(range(2,10)), cov_type)
    mean = model.means_[0][0]
    var = model.covars_[0][0][0]
    trans_mat = model.transmat_
    print ('mean', mean)
    print ('trans_mat', trans_mat)
    print ('var', var)
    clusters=model.predict(prep_data.iloc[:,2:])
#     print(prep_data)
    prep_data1 = prepare_data1(data, user, [activity])
#     print(prep_data1)
    clusters1=model.predict(prep_data1.iloc[:,2:])
#     print (model.means_)
#     print (model.covars_)
    create_single_variate_plot(prep_data, user, clusters, activity)
#     create_oneSeries_single_variate_plot(prep_data, user, clusters, activity)
    create_oneSeries_single_variate_plot(prep_data1, user, clusters1, activity)
    values = prep_data[activity]
    dates = pd.to_datetime(prep_data['interval_start'])
    dates_list = [dates[i].strftime("%Y-%m-%d") for i in range(0, len(dates))]
    cluster = {}
    for i in range(0, model.n_components): # iterate through clusters
        cluster[i] = {}
        name = "cluster_" + str(i)
        mask = clusters==i
        items = form_cluster_values(mask, values)
        cluster[i].update({'name' : name, 'items' : items.values.tolist()})
    dict.update({activity:cluster, 'groups' : dates_list})
    return dict

data = get_data()
user = [115]
activity = 'physicalactivity_calories'

# prepared_data = prepare_data1(data, user, [activity])
# plot_time_series(prepared_data, user, activity)

prepare_data1(data, user, [activity])
dict_single_variate=hmm_to_dict_single_variate(data, user, activity, 'diag')

# with open('JSONs/single_variate_hmms.json', 'w') as outfile:
#     json.dump(dict_single_variate, outfile)

print("done")