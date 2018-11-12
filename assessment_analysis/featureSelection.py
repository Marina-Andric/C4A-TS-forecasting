from sklearn.feature_selection import VarianceThreshold, RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import modelAccuracy as ma

# Additionally, embedded methods to be considered

# remove features with low variance
def remove_fea_low_variance(data):
    # print ('shape before remove_fea_low_variance: ', data.shape)
    features_old = data.columns
    print (len(features_old))
    fsel = VarianceThreshold(threshold=0.7)
    fsel.fit_transform(data)
    features_new = data.columns
    print (len(features_new))
    # print ('shape after remove_fea_low_variance: ', data.shape)
    print (list(set(features_old).difference(set(features_new))))


# recursive feature elimination
def rfecv(X, y, name, k):
    logReg = LogisticRegression(multi_class='multinomial', solver = 'newton-cg', C = 1000.0, random_state=1)
    # svc = SVC(kernel='sigmoid')
    rfecv = RFECV(estimator = logReg, step=1, cv=StratifiedKFold(k, True, 1))
    rfecv.fit(X, y)
    print ("Optimal number of features: ", rfecv.n_features_)
    # plotting
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.grid()
    plt.savefig("Images\\FeatureSelectionPlots\\" + name + ".png")
    # print (rfecv.support_)
    # print (rfecv.ranking_)
    ma.get_prediction_accuracy(logReg, X, y, k)
    print (rfecv.ranking_)
    return rfecv.support_

# tree-based feature selection
# def tbfe():


