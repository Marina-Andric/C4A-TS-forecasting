import numpy as np
from hmmlearn.hmm import GaussianHMM

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


