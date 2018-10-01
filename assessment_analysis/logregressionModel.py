import dataProcess as dp
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import plotting as pltg

data = dp.get_data()
prepared_data = dp.prepare_data(data)

print (prepared_data.columns)

valid_data = prepared_data[prepared_data['data_validity_status'] == 'V']
features = valid_data[['nui_name', 'nui_value', 'nui_difference', 'risk_status']]

# X = features.iloc[:,0:-1]
X = features[['nui_value', 'nui_difference']]
y = features['risk_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

lr = LogisticRegression(C = 1000.0, random_state=0)
lr.fit(X_train_std, y_train)

# plotting
X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined_std = np.hstack((y_train, y_test))

# print (X_combined_std)
# print (y_combined_std)
# pltg.plot_decision_regions(X_combined_std, y_combined_std, classifier = lr)
