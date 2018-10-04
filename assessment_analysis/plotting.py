import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

import plotly.graph_objs as go
import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('marina09', '7Ki6XR0QqZt91vd5xpZm')

# single feature
def scatter_with_color_dimension_graph(feature, target, layout_labels):
    """
    Scatter with color dimension graph to visualize the density of the
    Given feature with target
    :param feature:
    :param target:
    :param layout_labels:
    :return:
    """
    trace1 = go.Scatter(
        y=feature,
        mode='markers',
        marker=dict(
            size='16',
            color=target,
            colorscale='red',
            showscale=True
        )
    )
    layout = go.Layout(
        title=layout_labels[2],
        xaxis=dict(title=layout_labels[0]), yaxis=dict(title=layout_labels[1]))
    data = [trace1]
    fig = Figure(data=data, layout=layout)
    # plot_url = py.plot(fig)
    py.image.save_as(fig, filename='Images\\' + layout_labels[1] + '_Density.png')

# plotting in two dimensions
def plot_decision_regions(X, y, classifier, labels, resolution = 0.02):
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('lightgreen', 'red', 'orange', 'gray', 'cyan')

    cmap = ListedColormap(colors[:len(np.unique(y))])

    # decision surface
    x1_min, x1_max = X[:, 0].min() -1, X[:, 0].max()-1
    x2_min, x2_max = X[:, 1].min() -1, X[:, 1].max()-1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))

    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha = 0.4, cmap = cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    risk_mapping = {'Risk alert': 2, 'Risk warning': 1, 'No risk': 0}
    inv_risk_mapping = {v:k for k,v in risk_mapping.items()}

    # samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0], y=X[y==cl, 1], alpha = 0.8, c = cmap(idx), marker = markers[idx], label = inv_risk_mapping.get(cl))
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.legend(loc = 'upper left')
    plt.savefig('Images\decision_regions.png')

