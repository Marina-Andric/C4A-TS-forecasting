import numpy as np
from hmmlearn.hmm import GaussianHMM
from multivariate_plotting import create_multi_variate_plot


def fit_hmm(data):
    # print (data)
    # data = data [['interval_start', 'physicalactivity_calories', 'walk_steps']]
    bic, model = learn_hmm_multi(data.iloc[:,1:], 8)
    # clusters = model.predict(data.iloc[:,1:])
    # data['cluster'] = clusters
    # create_multi_variate_plot(data)
    # print (data)
    return model, data


def get_cluster_probabs(model, data):
    probabs = model.predict_proba(data.iloc[:,1:])
    # print (probabs)
    probabs_np = np.array(probabs)
    max_probab = np.amax(probabs_np, 1)
    data['max_probab'] = max_probab
    return data


def bic_criteria(data, log_likelihood, model):
    '''
    :param data:
    :param log_likelihood:
    :param model:
    :return:
    '''
    n_features = data.shape[1]  ### here adapt for multi-variate
    n_states=len(model.means_)
    n_params = n_states * (n_states - 1) + 2 * n_features * n_states
    logN = np.log(len(data))
    bic = -2 * log_likelihood + n_params * logN
    return(bic)


def aic_criteria(data, log_likelihood, model):
    '''
    :param data:
    :param log_likelihood:
    :param model:
    :return:
    '''
    n_features = data.shape[1]  ### here adapt for multi-variate
    n_states=len(model.means_)
    n_params = n_states * (n_states - 1) + 2 * n_features * n_states
    aic = -2 * log_likelihood + n_params
    return(aic)


def learn_hmm_multi(data, max_clusters):
    best_value = np.inf
    best_model = None
    # print('data to fit ', data)
    for n_clusters in range(1, max_clusters):
        model = GaussianHMM(n_components=n_clusters, covariance_type='diag', n_iter=1000).fit(data)
        log_likelihood = model.score(data)
        criteria_bic = bic_criteria(data, log_likelihood, model)
        if criteria_bic < best_value:
            best_value, best_model = criteria_bic, model
    return best_value, best_model


