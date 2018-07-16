import psycopg2
import pandas as pd
import data_preparation
from data_preparation import get_data
from data_preparation import pivot_data, prepare_dataset, normalize_features
import hmm_multi
from hmm_multi import fit_hmm
import multivariate_plotting
from multivariate_plotting import create_many_singlevariate_plots, create_multivariate_plot2, plot_feature_distributions, pca, plot_feature_distributions2, plot_cluster_distribution, visualize_clustering
import warnings
warnings.filterwarnings("ignore")
import visualization
from visualization import plot_feature_correlations, corr_visualization
import numpy as np

# for reproducibility 
np.random.seed(0)

data = get_data(130)
activities = ['interval_start', 'physicalactivity_calories', 'physicalactivity_intense_time', 'physicalactivity_moderate_time', 'physicalactivity_soft_time', 'sleep_awake_time', 'sleep_deep_time', 'sleep_light_time', 'sleep_tosleep_time', 'sleep_wakeup_num', 'walk_distance', 'walk_steps']
pivoted_data = pivot_data(data)[activities]

# print (pivoted_data.describe())
# pivoted_data.to_csv('data_bhx_130_newest.csv', sep='\t')

prepared_data = prepare_dataset(pivoted_data)
# print (prepared_data)
prepared_data.to_csv('prepared data cr130.csv', sep='\t')

# Print main statistics per feature
# print (prepared_data.describe())

# Visualize feature distributions
# plot_feature_distributions2(prepared_data)

# corr_visualization(prepared_data)


# data_clusters.to_csv('data clusters cr130.csv', sep='\t')

# print (np.unique(data_clusters['cluster']))
# plot_cluster_distribution(data_clusters)
# plot_feature_normalized(prepared_data)

normalized_data = normalize_features(prepared_data)
normalized_data.to_csv('xlsx/cr130_normalized.csv')

# model, data_clusters = fit_hmm(normalized_data)
# print (np.unique(data_clusters['cluster']))

model, data_clusters = fit_hmm(prepared_data)
visualize_clustering(model, data_clusters)

# print (data_clusters)

# Visualize clusters (via PCA)
# pca(data_clusters)
create_multivariate_plot2(data_clusters)



# create_multivariate_plot2(data_clusters)



