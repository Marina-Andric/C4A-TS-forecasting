import pandas as pd
import psycopg2
import csv
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from hmm_multi import fit_hmm, get_cluster_probabs
from multivariate_plotting import create_multi_variate_plot
import warnings
import data_preparation
from data_preparation import get_data, pivot_data, find_correlated_activities_foractivity, prepare_dataset, extract_features_all
import visualization
from visualization import corr_visualization
warnings.filterwarnings("ignore")
import datetime

data_train = get_data(118)
# activity = 'physicalactivity_calories'
# print (data)
pivoted_data_train = pivot_data(data_train)
# pivoted_data_train.to_csv('all data.csv', sep = '\t')
# df_selected_features = find_correlated_activities_foractivity(df, activity)

train_dataset = prepare_dataset(pivoted_data_train)
train_dataset.to_csv('train dataset.csv', sep = ',')

model, traindata_clusters = fit_hmm(train_dataset)

# data_test = get_data(109)
# pivoted_data_test = pivot_data(data_test)
# pivoted_data_test = pivoted_data_test.dropna(axis=0, how='any')
#
# data_test_probabs = get_cluster_probabs(model, pivoted_data_test)
# data_test_probabs.to_csv('test probabs.csv', sep='\t')
# print (min(data_test_probabs['max_probab']))

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
dataset_synthetic = pd.read_csv('testdataset_synthetic.csv', sep=',', parse_dates=['interval_start'], date_parser=dateparse, index_col=0)


data_test_probabs = get_cluster_probabs(model, dataset_synthetic)
data_test_probabs.to_csv('sythetic_probabs1.csv', sep='\t')
print (min(data_test_probabs['max_probab']))

# pivoted_data = pivoted_data.dropna(axis=0, how='any')
# data_probabs = get_cluster_probabs(model, pivoted_data)
# data_probabs.to_csv('probabs', sep='\t')
# print (min(data_probabs['max_probab']))



# prepared_data1 = extract_features_normal(df)
# model = fit_hmm_normal(prepared_data1)
#
# prepared_data2 = extract_features_all(df)
# result = multivariate_hmm_all(model, prepared_data2)
# print(result)
# print(result[result['walk_distance']==0])


# print(result[result['max_probabs'] < 0.7])
# print (probabs_all)
# prepared_data['probabs'] = probabs_all

