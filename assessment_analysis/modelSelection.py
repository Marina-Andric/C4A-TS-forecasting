import dataProcess as dp
import modelAccuracy as ma
import featureSelection as fs

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import accuracy_score, roc_auc_score, average_precision_score, auc
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold

import pandas as pd
import numpy as np
import plotting as pltg


def compare_dfs(data1, data2):
    prep_data1 = dp.prepare_data(data1)
    prep_data2 = dp.prepare_data(data2)
    motility_data1 = dp.get_motility_data(prep_data1)
    motility_data2 = dp.get_motility_data(prep_data2)

    motility_data_all = pd.concat([motility_data1.set_index(['interval_start', 'user_in_role_id', 'risk_status']),
                                   motility_data2.set_index(['interval_start', 'user_in_role_id', 'risk_status'])],
                                  axis='columns', keys=['first', 'second'])
    print(motility_data_all)



def log_reg(motility_data, features):
    X = motility_data[features]
    y = motility_data['risk_status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    mul_lr = LogisticRegression(multi_class='multinomial', solver='newton-cg', C=1000.0, random_state=0)
    mul_lr.fit(X_train_std, y_train)

    X_combined_std = np.vstack((X_train_std, X_test_std))
    y_combined = np.hstack((y_train, y_test))
    print('Logistic regression accuracy: ')
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

    mul_lr = LogisticRegression(multi_class='multinomial', solver='newton-cg', C=1000.0, random_state=0)
    mul_lr.fit(X_train_std, y_train)

    X_combined_std = np.vstack((X_train_std, X_test_std))
    y_combined = np.hstack((y_train, y_test))

    # print (X_combined_std)
    # print (y_combined_std)
    # pltg.plot_decision_regions(X_gef_transformed, y_combined, labels =features_gef, name = 'gef', classifier = mul_lr)
    # pltg.plot_decision_regions(X_combined_std, y_combined, labels =features, name= 'all_features', classifier = mul_lr)


def selectFeatures_motility(motility_data):
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
                    'best_walk_distance_nui_difference', 'best_walk_distance_nui_value',
                    'best_walk_steps_nui_difference',
                    'best_walk_steps_nui_value',
                    'delta_walk_distance_nui_difference', 'delta_walk_distance_nui_value',
                    'delta_walk_steps_nui_difference',
                    'delta_walk_steps_nui_value']

    features_new = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'avg_walk_steps_nui_difference',
                    'avg_walk_steps_nui_value',
                    's1td_walk_distance_1_nui_difference', 's1td_walk_distance_1_nui_value',
                    's1td_walk_steps_1_nui_difference',
                    's1td_walk_steps_1_nui_value',
                    'b1est_walk_distance_1_nui_difference', 'b1est_walk_distance_1_nui_value',
                    'b1est_walk_steps_1_nui_difference',
                    'b1est_walk_steps_1_nui_value',
                    'd1elta_walk_distance_1_nui_difference', 'd1elta_walk_distance_1_nui_value',
                    'd1elta_walk_steps_1_nui_difference',
                    'd1elta_walk_steps_1_nui_value']

    features_selected_1 = [
                            'avg_walk_distance_nui_difference',  # 1
                           # 'std_walk_distance_nui_difference', # 2
                           # 'best_walk_distance_nui_difference',
                           # 'delta_walk_distance_nui_difference',
                           's_td_walk_distance_1_nui_difference',

                           'b_est_walk_distance_1_nui_difference',
                           'd_elta_walk_distance_1_nui_difference',

                           'd1elta50_walk_distance_1_nui_difference',
                           'd1elta75_walk_distance_1_nui_difference',

                           'avg_walk_steps_nui_difference',
                           # 'std_walk_steps_nui_difference',
                           # 'best_walk_steps_nui_difference',
                           # 'delta_walk_steps_nui_difference',
                           's_td_walk_steps_1_nui_difference',

                           'b_est_walk_steps_1_nui_difference',
                           'd_elta_walk_steps_1_nui_difference',

                           'd1elta50_walk_steps_1_nui_difference',
                           'd1elta75_walk_steps_1_nui_difference',
                           ]
    features_selected_2 = [
                            'avg_walk_distance_nui_difference',  # 1
                           'std_walk_distance_nui_difference', # 2
                           # 'b1est_walk_distance_1_nui_difference', # 3
                           # 'd1elta_walk_distance_1_nui_difference',
                           'best_walk_distance_nui_difference',
                           # 'delta_walk_distance_nui_difference',
                           # 's1td_walk_distance_1_nui_difference',
                            'd1elta50_walk_distance_1_nui_difference',
                            'd1elta75_walk_distance_1_nui_difference',

                           'avg_walk_steps_nui_difference',
                           'std_walk_steps_nui_difference',
                           # 'b1est_walk_steps_1_nui_difference',
                           # 'd1elta_walk_steps_1_nui_difference',
                           'best_walk_steps_nui_difference',
                           # 'delta_walk_steps_nui_difference',
                           # 's1td_walk_steps_1_nui_difference'
                            'd1elta50_walk_steps_1_nui_difference',
                            'd1elta75_walk_steps_1_nui_difference'

                           ]
    features_all = motility_data.columns[4:]
    # print (features_all)

    print(motility_data.shape)
    # print(motility_data)
    # log_reg(motility_data, features_all)

    # pltg.plot_bubble_chart(motility_data, ['gef_value', 'gef_difference'], 'gef_conf2_new')

    # fs.remove_fea_low_variance(motility_data.iloc[:, 4:])

    y = motility_data['risk_status']

    X_old = motility_data[features_selected_1]
    sc = StandardScaler()
    X_old_std = sc.fit_transform(X_old)
    f_old = fs.rfecv(X_old_std, y, name='Motility//lr_new', k=6)
    print(X_old.columns[f_old])

    X_new = motility_data[features_selected_2]
    sc = StandardScaler()
    X_new_std = sc.fit_transform(X_new)
    f_new = fs.rfecv(X_new_std, y, name='Motility//lr_old', k=6)
    print(X_new.columns[f_new])

def selectFeatures_physicalActivity(data):
    features_selected = [
        'avg_physicalactivity_moderate_time_nui_difference',  # 1
        'std_physicalactivity_moderate_time_nui_difference',  # 2
        'best_physicalactivity_moderate_time_nui_difference',
        # 'delta_physicalactivity_moderate_time_nui_difference',

        'avg_physicalactivity_calories_nui_difference',
        'std_physicalactivity_calories_nui_difference',
        'best_physicalactivity_calories_nui_difference',
        # 'delta_physicalactivity_calories_nui_difference',

        'avg_physicalactivity_intense_time_nui_difference',  # 1
        'std_physicalactivity_intense_time_nui_difference',  # 2
        'best_physicalactivity_intense_time_nui_difference',
        # 'delta_physicalactivity_intense_time_nui_difference',

        'avg_physicalactivity_soft_time_nui_difference',
        'std_physicalactivity_soft_time_nui_difference',
        'best_physicalactivity_soft_time_nui_difference',
        # 'delta_physicalactivity_soft_time_nui_difference',
    ]

    y = data['risk_status']

    # X_old = motility_data[features_selected_1]
    # sc = StandardScaler()
    # X_old_std = sc.fit_transform(X_old)
    # f_old = fs.rfecv(X_old_std, y, name='lr_new', k=6)
    # print(X_old.columns[f_old])

    X_new = data[features_selected]
    sc = StandardScaler()
    X_new_std = sc.fit_transform(X_new)
    f_new = fs.rfecv(X_new_std, y, name='PhysicalActivity//features_bi', k=5)
    print(X_new.columns[f_new])


def get_motility_data():
    # data1 = dp.get_data('localhost', 'city4age_dba', 'city4age_dba')
    # data2 = dp.get_data('109.111.225.84', 'city4age_srv', 'city4age_srv')
    # compare_dfs(data1, data2)

    # data = dp.get_data('109.111.225.84', 'city4age_srv', 'city4age_srv')
    # data = dp.get_data('localhost', 'city4age_dba', 'city4age_dba')
    # prepared_data = dp.prepare_data(data)
    # motility_data = dp.get_motility_data(prepared_data)

    motility_data = pd.read_csv('Data//assessments_1710_multi.csv')
    return motility_data

def get_physicalActivity_data():
    # data = dp.get_data_physicalActivity('localhost', 'city4age_dba', 'city4age_dba')
    # prepared_data = dp.prepare_data(data)
    # physicalActivity_data = dp.pivot_physicalActivity_data(prepared_data)
    # dp.to_xlxs(physicalActivity_data, 'physicalActivity_0811_config1_multi') # save
    # dp.to_xlxs(physicalActivity_data, 'physicalActivity_0811_config1_bi')

    physicalActivity_data = pd.read_csv('Data//physicalActivity_0811_config1_multi.csv') # read
    return physicalActivity_data

physicalActivity_data = get_physicalActivity_data()
# selectFeatures_physicalActivity(physicalActivity_data)
# log_reg(physicalActivity_data, ['avg_physicalactivity_moderate_time_nui_difference',
#        'std_physicalactivity_intense_time_nui_difference',
#        'avg_physicalactivity_soft_time_nui_difference'])
pltg.plot_density_graph_feature(physicalActivity_data)

# print (physicalActivity_data)
# log_reg(physicalActivity_data, ['gef_value', 'gef_difference'])


# Relative changes
# all_perc_changes = dp.get_all_perc_changes()
# factor_changes = dp.prepare_and_save(all_perc_changes)
# factor_changes = pd.read_csv('Data//relative_changes.csv')
# print (factor_changes)
# pltg.plot_relative_changes(factor_changes, factor_changes.columns[3:])

# motility_data = get_motility_data()
# selectFeatures(motility_data)
# dp.find_perc_chg()
features = ['avg_walk_distance_perc_change', 'avg_walk_steps_perc_change', 'std_walk_distance_perc_change', 'std_walk_steps_perc_change',
            'best_walk_distance_perc_change', 'best_walk_steps_perc_change',
            'delta_walk_distance_perc_change', 'delta_walk_steps_perc_change',
            's_td_walk_distance_1_perc_change', 'd_elta_walk_distance_1_perc_change']
# features = ['avg_walk_distance_perc_change', 'std_walk_distance_perc_change']
# pltg.plot_perc_changes(data1, features)

# logistic regression
# log_reg(motility_data, ['gef_value', 'gef_difference'])

# pltg.scatter_with_color_dimension_graph(motility_data['d1elta50_walk_steps_1_nui_difference'], motility_data['risk_status'], ['Number of Observations', 'delta50_walk_steps_nui_difference', 'delta50_walk_steps_nui_difference'])
# pltg.scatter_with_color_dimension_graph(motility_data['d1elta75_walk_steps_1_nui_difference'], motility_data['risk_status'], ['Number of Observations', 'delta75_walk_steps_nui_difference', 'delta75_walk_steps_nui_difference'])
#
# pltg.scatter_with_color_dimension_graph(motility_data['d1elta50_walk_distance_1_nui_difference'], motility_data['risk_status'], ['Number of Observations', 'delta50_walk_distance_nui_difference', 'delta50_walk_distance_nui_difference'])
# pltg.scatter_with_color_dimension_graph(motility_data['d1elta75_walk_distance_1_nui_difference'], motility_data['risk_status'], ['Number of Observations', 'delta75_walk_distance_nui_difference', 'delta75_walk_distance_nui_difference'])

# pltg.scatter_with_color_dimension_graph(motility_data['gef_difference'], motility_data['risk_status'], ['Number of Observations', 'gef_value', 'gef_value'])
# pltg.plot_bubble_chart(motility_data, ['avg_walk_distance_nui_difference', 'delta_walk_distance_nui_difference'], 'avg_delta_nui_diffs')