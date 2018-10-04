import dataProcess as dp
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

import numpy as np
import plotting as pltg

def plot_density_graph_feature(data):
    for feature in data.columns[1:]:
        labels = ["Number of Observations", feature, feature]
        pltg.scatter_with_color_dimension_graph(data[feature], data['risk_status'], labels)


data = dp.get_data('localhost', 'city4age_dba', 'city4age_dba')
# data = dp.get_data('109.111.225.84', 'city4age_srv', 'city4age_srv')
prepared_data = dp.prepare_data(data)
motility_data = dp.get_motility_data(prepared_data)
# plot_density_graph_feature(motility_data)
# print (motility_data)


# X = motility_data.iloc[:, 1:]
features = ['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value']
# features = ['gef_value', 'gef_difference']
X = motility_data[features]

y = motility_data['risk_status']

# print(motility_data[['avg_walk_distance_nui_difference', 'avg_walk_distance_nui_value', 'risk_status']])
print (motility_data[['avg_walk_distance_nui_value', 'risk_status']])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

mul_lr = LogisticRegression(multi_class='multinomial', solver = 'newton-cg', C = 1000.0, random_state=0)
mul_lr.fit(X_train_std, y_train)

# prediction accuracy
# print ("Logistic regression Train Accuracy :: ", metrics.accuracy_score(train_y, lr.predict(train_x)))
# print ("Logistic regression Test Accuracy :: ", metrics.accuracy_score(test_y, lr.predict(test_x)))
print ("Multinomial Logistic regression Train Accuracy :: ", accuracy_score(y_train, mul_lr.predict(X_train_std)))
print ("Multinomial Logistic regression Test Accuracy :: ", accuracy_score(y_test, mul_lr.predict(X_test_std)))

# plotting
X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined_std = np.hstack((y_train, y_test))


# print (X_combined_std)
# print (y_combined_std)
pltg.plot_decision_regions(X_combined_std, y_combined_std, labels =features, classifier = mul_lr)