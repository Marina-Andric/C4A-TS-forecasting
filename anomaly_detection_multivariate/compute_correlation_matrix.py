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
from data_preparation import get_data, pivot_data, find_correlated_activities_foractivity, get_train_dataset, extract_features_all
import visualization
from visualization import corr_visualization
warnings.filterwarnings("ignore")


data = get_data(116)
# activity = 'physicalactivity_calories'
# print (data)
pivoted_data = pivot_data(data)
pivoted_data.to_csv('all data.csv', sep = '\t')
# df_selected_features = find_correlated_activities_foractivity(df, activity)

train_dataset = get_train_dataset(pivoted_data)
train_dataset.to_csv('train dataset.csv', sep = '\t' )

model, traindata_clusters = fit_hmm(train_dataset)

pivoted_data = pivoted_data.dropna(axis=0, how='any')
data_probabs = get_cluster_probabs(model, pivoted_data)
data_probabs.to_csv('probabs', sep='\t')
print (min(data_probabs['max_probab']))





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

