import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

def corr_visualization(data):
    corr = data.corr(method = 'spearman')
    dim = data.__len__()
    # print ("correlation matrix", corr)
    mask = np.zeros((11, 11)) # hardcoded
    mask[np.triu_indices_from(mask, k=1)] = True
    fig, ax = plt.subplots(figsize = (10, 8))
    sns.heatmap(corr, cmap=sns.diverging_palette(220, 10, as_cmap=True), square=True, ax=ax, vmin = -1, vmax = 1, fmt = ".2f", annot=True) # mask=mask for lower diagonal
    plt.savefig('feature corr.png')
    plt.show()

def plot_feature_correlations(data):
    plt.title('Feature correlations')
    plt.matshow(data.iloc[1:].corr(method='spearman'))