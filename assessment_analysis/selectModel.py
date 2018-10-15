import dataProcess as dp
import modelAccuracy as ma
import featureSelection as fs

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import accuracy_score, roc_auc_score, average_precision_score, auc
from sklearn.preprocessing import StandardScaler

import pandas as pd
import numpy as np
import plotting as pltg

def compare_dfs(data1, data2):
    prep_data1 = dp.prepare_data(data1)
    prep_data2 = dp.prepare_data(data2)
    motility_data1 = dp.get_motility_data(prep_data1)
    motility_data2 = dp.get_motility_data(prep_data2)

    motility_data_all = pd.concat([motility_data1.set_index(['interval_start', 'user_in_role_id', 'risk_status']),
                                   motility_data2.set_index(['interval_start', 'user_in_role_id', 'risk_status'])], axis = 'columns', keys = ['first', 'second'])
    print(motility_data_all)


def log_reg(motility_data, features):
    X = motility_data[features]
    y = motility_data['risk_status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    mul_lr = LogisticRegression(multi_class='multinomial', solver = 'newton-cg', C = 1000.0, random_state=0)
    mul_lr.fit(X_train_std, y_train)

    X_combined_std = np.vstack((X_train_std, X_test_std))
    y_combined = np.hstack((y_train, y_test))
    print ('Logistic regression accuracy: ')
    ma.get_prediction_accuracy(mul_lr, X_combined_std, y_combined)


#################
# plotting
def make_plots():
    features = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value']
    X = motility_data[features]
    y = motility_data['risk_status']

    # print(motility_data[['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'risk_status']])
    # print (motility_data[['avg_walk_distance_nui_value', 'risk_status']])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    mul_lr = LogisticRegression(multi_class='multinomial', solver = 'newton-cg', C = 1000.0, random_state=0)
    mul_lr.fit(X_train_std, y_train)

    X_combined_std = np.vstack((X_train_std, X_test_std))
    y_combined = np.hstack((y_train, y_test))

    # print (X_combined_std)
    # print (y_combined_std)
    # pltg.plot_decision_regions(X_gef_transformed, y_combined, labels =features_gef, name = 'gef', classifier = mul_lr)
    # pltg.plot_decision_regions(X_combined_std, y_combined, labels =features, name= 'all_features', classifier = mul_lr)


def selectFeatures(motility_data):
    features_4 = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
                'avg_walk_steps_nui_value']
    features_8 = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
                'avg_walk_steps_nui_value',
                  'std_walk_distance_nui_difference', 'std_walk_distance_nui_value', 'std_walk_steps_nui_difference',
                  'std_walk_steps_nui_value']

    features_old = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
                'avg_walk_steps_nui_value',
                  'std_walk_distance_nui_difference', 'std_walk_distance_nui_value', 'std_walk_steps_nui_difference',
                  'std_walk_steps_nui_value',
                'best_walk_distance_nui_difference', 'best_walk_distance_nui_value', 'best_walk_steps_nui_difference',
                'best_walk_steps_nui_value',
                  'delta_walk_distance_nui_difference', 'delta_walk_distance_nui_value', 'delta_walk_steps_nui_difference',
                  'delta_walk_steps_nui_value']

    features_new = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
                'avg_walk_steps_nui_value',
                  's1td_walk_distance_1_nui_difference', 's1td_walk_distance_1_nui_value', 's1td_walk_steps_1_nui_difference',
                  's1td_walk_steps_1_nui_value',
                'b1est_walk_distance_1_nui_difference', 'b1est_walk_distance_1_nui_value', 'b1est_walk_steps_1_nui_difference',
                'b1est_walk_steps_1_nui_value',
                  'd1elta_walk_distance_1_nui_difference', 'd1elta_walk_distance_1_nui_value', 'd1elta_walk_steps_1_nui_difference',
                  'd1elta_walk_steps_1_nui_value']

    features_all = motility_data.columns[4:]
    # print (features_all)

    print (motility_data.shape)
    # print(motility_data)
    # log_reg(motility_data, features_all)

    # pltg.plot_bubble_chart(motility_data, ['gef_value', 'gef_difference'], 'gef_conf2_new')

    # fs.remove_fea_low_variance(motility_data.iloc[:, 4:])

    y = motility_data['risk_status']

    X_old = motility_data[features_old]
    sc = StandardScaler()
    X_old_std = sc.fit_transform(X_old)
    f_old = fs.rfecv(X_old_std, y, name = 'lr_old')
    print (X_old.columns[f_old])

    X_new = motility_data[features_new]
    sc = StandardScaler()
    X_new_std = sc.fit_transform(X_new)
    f_new = fs.rfecv(X_new_std, y, name = 'lr_new')
    print (X_new.columns[f_new])


# data1 = dp.get_data('localhost', 'city4age_dba', 'city4age_dba')
# data2 = dp.get_data('109.111.225.84', 'city4age_srv', 'city4age_srv')
# compare_dfs(data1, data2)

# data = dp.get_data('109.111.225.84', 'city4age_srv', 'city4age_srv')
data = dp.get_data('localhost', 'city4age_dba', 'city4age_dba')

prepared_data = dp.prepare_data(data)
motility_data = dp.get_motility_data(prepared_data)

selectFeatures(motility_data)

# log_reg(motility_data, features=['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
#                 'avg_walk_steps_nui_value',
#                   's1td_walk_distance_1_nui_difference', 's1td_walk_distance_1_nui_value', 's1td_walk_steps_1_nui_difference',
#                   's1td_walk_steps_1_nui_value',
#                 'b1est_walk_distance_1_nui_difference', 'b1est_walk_distance_1_nui_value', 'b1est_walk_steps_1_nui_difference',
#                 'b1est_walk_steps_1_nui_value',
#                   'd1elta_walk_distance_1_nui_difference', 'd1elta_walk_distance_1_nui_value', 'd1elta_walk_steps_1_nui_difference',
#                   'd1elta_walk_steps_1_nui_value'])
#
# log_reg(motility_data, features=['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
#                 'avg_walk_steps_nui_value',
#                   'std_walk_distance_nui_difference', 'std_walk_distance_nui_value', 'std_walk_steps_nui_difference',
#                   'std_walk_steps_nui_value',
#                 'best_walk_distance_nui_difference', 'best_walk_distance_nui_value', 'best_walk_steps_nui_difference',
#                 'best_walk_steps_nui_value',
#                   'delta_walk_distance_nui_difference', 'delta_walk_distance_nui_value', 'delta_walk_steps_nui_difference',
#                   'delta_walk_steps_nui_value'])

# log_reg(motility_data, features=['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value',
#        'avg_walk_steps_nui_difference', 'avg_walk_steps_nui_value',
#        's1td_walk_distance_1_nui_value', 's1td_walk_steps_1_nui_value'])

# pltg.plot_density_graph_feature(motility_data)