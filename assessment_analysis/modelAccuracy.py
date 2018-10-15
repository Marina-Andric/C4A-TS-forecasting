from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, KFold
import numpy as np


def get_prediction_accuracy(model, X, y):
    # print ("Multinomial Logistic regression Train Accuracy :: ", accuracy_score(y_train, mul_lr.predict(X_train_std)))
    # print ("Multinomial Logistic regression Test Accuracy :: ", accuracy_score(y, model.predict(X)))
    # y_score = mul_lr.predict(X_test_std)
    # print ('auc score: ', auc(np.array(y_test.values), np.array(y_score), reorder='deprecated'))
    cv_results = cross_validate(model, X, y, cv=StratifiedKFold(9, True, 1), return_train_score=False)
    # print (cv_results.keys())
    print (cv_results['test_score'])
    print("cross validation: ", np.mean(cv_results['test_score']))